"""Who "he" is: for each pronoun, and each verb whose subject is not named, the person or thing
it refers to, from Clear Bible's MACULA Hebrew and Greek.

    python3 scripts/referents.py        (after reader.py)

Reads   MACULA Hebrew (WLC, as UXLC) and MACULA Greek (SBLGNT) word tables (downloaded once into
        .cache/macula/), our source texts (text/hebrew, text/greek) and data/bible/people.json
Writes  data/bible/referents/NN-book.json   {"book", "c": {chapter: {verse: [entry, ...]}}}, each
        entry [word, form, kind, name, chapter, verse, place, person]:
            word     the referring word's place in our verse (from 0), as the reader counts them
            form     MACULA's English for the referring part ("his", "he", or the verb: "said")
            kind     "p" a pronoun or pronoun ending; "s" the unnamed subject of a verb
            name     MACULA's English for what it refers to, followed back through other
                     pronouns to a noun or a name ("Abram", "the woman")
            chapter, verse, place  where that noun is, in our numbering and words
            person   its number in data/bible/people.json, when it names one person the verse
                     names under that name; else omitted

Only MACULA's own CC BY 4.0 fields are used: its word ids and references, the English glosses
of Clear's "english" column, part of speech, and the referent fields (participantref and subjref
in Hebrew, referent and subjref in Greek). Its UBS word senses (SDBH, SDBG and Louw-Nida, "used
with permission") and its Hebrew "gloss" column (from SIL, under SIL's terms) are not read.

MACULA Hebrew/Greek Linguistic Datasets, Biblica, CC BY 4.0,
https://github.com/Clear-Bible/macula-hebrew and https://github.com/Clear-Bible/macula-greek
"""

import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
from build import parse_book_md               # noqa: E402
import connections                            # noqa: E402
from reader import hebrew_tokens, greek_norm, align, write_json, OUT   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEBREW_COMMIT = "47db250bd55d0d8577f2a94fba114ef16c35b23c"
GREEK_COMMIT = "8423afe47b9e8f24b7772e808af45c7159a6fe7e"
SOURCES = {
    # The Hebrew table is kept in Git LFS, so it comes from GitHub's media host.
    "hebrew": (f"https://media.githubusercontent.com/media/Clear-Bible/macula-hebrew/{HEBREW_COMMIT}/WLC/tsv/macula-hebrew.tsv",
               f"hebrew-{HEBREW_COMMIT[:7]}/macula-hebrew.tsv"),
    "greek": (f"https://raw.githubusercontent.com/Clear-Bible/macula-greek/{GREEK_COMMIT}/SBLGNT/tsv/macula-greek-SBLGNT.tsv",
              f"greek-{GREEK_COMMIT[:7]}/macula-greek-SBLGNT.tsv"),
}
# MACULA's book codes, in our book order.
CODES = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH",
         "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS",
         "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
         "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH",
         "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
REF = re.compile(r"(\w+) (\d+):(\d+)!(\d+)")
PRONOUN = {"pron", "pronoun", "suffix"}


def table(lang):
    url, rel = SOURCES[lang]
    path = connections.fetch(url, os.path.join(connections.CACHE, "macula", rel))
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            yield row


def load(lang):
    """MACULA's words: {id: {...}} and, verse by verse, its words in order (each a list of ids,
    for Hebrew the parts of one word)."""
    rows, verses = {}, collections.defaultdict(lambda: collections.OrderedDict())
    for r in table(lang):
        m = REF.match(r["ref"] or "")
        if not m or m[1] not in CODES:
            continue
        key = (CODES.index(m[1]), int(m[2]), int(m[3]))
        rid = r["xml:id"]
        if lang == "hebrew":
            rid = rid.lstrip("o")
            pos, refs = r["pos"], (r["participantref"] or "").split()
        else:
            pos, refs = r["class"], (r["referent"] or "").split()
        rows[rid] = {"key": key, "word": int(m[4]), "text": r["text"], "pos": pos, "english": (r["english"] or "").strip(),
                     "refs": refs, "subj": (r["subjref"] or "").split()}
        verses[key].setdefault(int(m[4]), []).append(rid)
    return rows, verses


def consonants(t):
    return "".join(re.findall(r"[א-ת]", t))


def place_words(lang, verses, rows):
    """Each MACULA word's place in our verse: {id: (chapter, verse, place)}."""
    where = {}
    for bi, (num, osis, name, testament) in enumerate(BOOKS):
        if (testament == "OT") != (lang == "hebrew"):
            continue
        source = parse_book_md(os.path.join(ROOT, "text", "hebrew" if testament == "OT" else "greek", file_stem(num, name) + ".md"))
        for c, v, text in source:
            words = list(verses.get((bi, c, v), {}).values())
            if not words:
                continue
            if lang == "hebrew":
                toks = hebrew_tokens(text)
                ours = [consonants(t) if kind != "k" else "\0" for t, kind in toks]
                theirs = ["".join(consonants(rows[i]["text"]) for i in w) for w in words]
            else:
                ours = [greek_norm(t) for t in text.split() if greek_norm(t)]
                theirs = [greek_norm(rows[w[0]]["text"]) for w in words]
            for i, j in enumerate(align(ours, theirs)):
                if j is not None:
                    for rid in words[j]:
                        where[rid] = (c, v, i)
    return where


def follow(rows, rid, seen=()):
    """The noun a pronoun comes back to: its antecedent, and that one's, and so on."""
    r = rows.get(rid)
    if r is None or rid in seen or len(seen) > 6:
        return None
    if r["pos"] in PRONOUN and r["refs"]:
        return follow(rows, r["refs"][0], seen + (rid,)) or rid
    return rid


def main():
    people = json.load(open(os.path.join(OUT, "people.json"), encoding="utf-8"))
    stats = collections.Counter()
    out = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    for lang in ("hebrew", "greek"):
        rows, verses = load(lang)
        where = place_words(lang, verses, rows)
        for rid, r in rows.items():
            for kind, targets in (("p", r["refs"] if r["pos"] in PRONOUN else []), ("s", r["subj"])):
                if not targets or rid not in where:
                    continue
                stats[lang + " " + kind] += 1
                names = []
                for t in targets:
                    end = follow(rows, t)
                    if end is None or end not in where:
                        continue
                    e = rows[end]
                    c, v, i = where[end]
                    entry = [where[rid][2], r["english"], kind, e["english"] or e["text"], c, v, i]
                    osis = BOOKS[e["key"][0]][1]
                    named = [k for k in people["verses"].get(osis, {}).get(f"{c}:{v}", [])
                             if people["n"][k].lower() == (e["english"] or "").lower()]
                    if len(named) == 1:
                        entry.append(named[0])
                        stats["people"] += 1
                    names.append(entry)
                if names:
                    stats[lang + " placed"] += 1
                    bi = r["key"][0]
                    c, v, _ = where[rid]
                    out[bi][c][v].extend(names)
    os.makedirs(os.path.join(OUT, "referents"), exist_ok=True)
    for bi, (num, osis, name, testament) in enumerate(BOOKS):
        chapters = {str(c): {str(v): out[bi][c][v] for v in sorted(out[bi][c])} for c in sorted(out[bi])}
        write_json(os.path.join(OUT, "referents", file_stem(num, name) + ".json"), {"book": name, "c": chapters})
    print("Referents: " + ", ".join(f"{k} {n:,}" for k, n in sorted(stats.items())))


if __name__ == "__main__":
    main()
