"""Build the data for the web reader, index.html.

    python3 scripts/reader.py

Reads   translation/NN-book/CCC.md   the Open Plain English Translation, with its notes and status
        text/hebrew, text/greek       the source texts (UXLC and SBLGNT)
        STEPBible TAHOT and TAGNT     word-by-word English glosses, Strong's numbers and grammar
        STEPBible TBESH and TBESG     brief lexicons, keyed by Strong's number
        (the STEPBible files are downloaded once into .cache/stepbible/)
Writes  data/bible/books.json            the books, their chapters and each chapter's status
        data/bible/text/NN-book.json     each book: English verses and notes, the source
                                          text, paragraph breaks and English verse numbers
        data/bible/words/NN-book.json    each book's words, verse by verse, in the order the
                                          reader splits the source verse into words: each
                                          "transliteration|gloss|Strong's|grammar[|main]",
                                          words separated by "¦". Strong's numbers drop their
                                          H or G and leading zeros; the grammar starts with H
                                          (Hebrew) or A (Aramaic) in the Old Testament; "main"
                                          is the morpheme that carries the meaning, if not
                                          the last
        data/bible/variants/NN-book.json where the editions and manuscripts differ, verse by
                                          verse (see variants_note below)
        data/bible/lexicon/xNN.json      the lexicon entries the words use, in chunks
        data/bible/search.json           every English verse as plain text, for search

The words come from STEPBible's tagged texts, which follow the same manuscripts as ours (the
Leningrad Codex; for the New Testament, the words TAGNT marks as being in the SBLGNT). Each of
our words is matched to a STEPBible word by its letters, verse by verse; the few that differ
have no gloss.
"""

import collections
import difflib
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
from build import parse_book_md               # noqa: E402
import connections                            # noqa: E402
from translation import parse_chapter         # noqa: E402
from consistency import quote_events          # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "bible")

STEP_FILES = {
    "tahot": ["Translators Amalgamated OT+NT/TAHOT " + part +
              " - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt"
              for part in ("Gen-Deu", "Jos-Est", "Job-Sng", "Isa-Mal")],
    "tagnt": ["Translators Amalgamated OT+NT/TAGNT " + part +
              " - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt"
              for part in ("Mat-Jhn", "Act-Rev")],
    "tbesh": ["Lexicons/TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt"],
    "tbesg": ["Lexicons/TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt"],
}
# STEPBible's book codes, in our book order.
STEP_CODES = ["Gen", "Exo", "Lev", "Num", "Deu", "Jos", "Jdg", "Rut", "1Sa", "2Sa", "1Ki", "2Ki",
              "1Ch", "2Ch", "Ezr", "Neh", "Est", "Job", "Psa", "Pro", "Ecc", "Sng", "Isa", "Jer",
              "Lam", "Ezk", "Dan", "Hos", "Jol", "Amo", "Oba", "Jon", "Mic", "Nam", "Hab", "Zep",
              "Hag", "Zec", "Mal",
              "Mat", "Mrk", "Luk", "Jhn", "Act", "Rom", "1Co", "2Co", "Gal", "Eph", "Php", "Col",
              "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "2Jn",
              "3Jn", "Jud", "Rev"]
OSIS_OF = {code: b[1] for code, b in zip(STEP_CODES, BOOKS)}
SLUG_OF = {b[1]: file_stem(b[0], b[2]) for b in BOOKS}

HEB_LETTER = re.compile(r"[א-ת]")


def step_paths(key):
    out = []
    for rel in STEP_FILES[key]:
        connections.STEPBIBLE_FILES[key + rel] = rel
        out.append(connections.fetch_stepbible(key + rel))
    return out


# --- Tagged texts ---------------------------------------------------------------------------

def hebrew_words():
    """TAHOT words by (osis, chapter, verse) in Hebrew numbering, and the English number of
    each Hebrew verse where they differ."""
    words, english, extra = collections.defaultdict(list), {}, collections.defaultdict(list)
    ref = re.compile(r"([1-3]?[A-Z][a-z]{1,2})\.(\d+)\.(\d+)(?:\((\d+)\.(\d+)\))?#\d+=(\S+)\t")
    for path in step_paths("tahot"):
        for line in open(path, encoding="utf-8"):
            m = ref.match(line)
            if not m:
                continue
            code, c, v, hc, hv, kind = m.groups()
            osis = OSIS_OF[code]
            key = (osis, int(hc), int(hv)) if hc else (osis, int(c), int(v))
            if kind.startswith("X"):              # an extra word, restored from the Septuagint
                cols = line.rstrip("\n").split("\t")
                extra[key].append((len(words[key]), cols[1], cols[3]))
                continue
            if kind.startswith("K"):              # a written form not read
                continue
            if hc and (int(c), int(v)) != key[1:]:
                english[key] = (int(c), int(v))
            cols = line.rstrip("\n").split("\t")
            cols.append(kind)
            words[key].append(cols)
    return words, english, extra


VARIANT = re.compile(r"(\S+) \(\w=([^)]*)\) (.*?) - (G\d+\w?)=([\w-]+) in: ([^;]*)")


def greek_words():
    """TAGNT words of the SBLGNT by (osis, chapter, verse), each as [Greek, transliteration,
    gloss, Strong's, grammar, dictionary form], and the verses that end a paragraph."""
    words, paragraph = collections.defaultdict(list), set()
    # The words of other editions: all the words of each verse (for the few verses the SBLGNT
    # prints in double brackets, which TAGNT does not count as its own), and the words of
    # other editions that the SBLGNT lacks, after the SBLGNT word they follow.
    every, added = collections.defaultdict(list), collections.defaultdict(list)
    ref = re.compile(r"([1-3]?[A-Z][a-z]{1,2})\.(\d+)\.(\d+)(?:\[\d+\])?#\d+=\S+\t")
    for path in step_paths("tagnt"):
        for line in open(path, encoding="utf-8"):
            m = ref.match(line)
            if not m:
                continue
            key = (OSIS_OF[m[1]], int(m[2]), int(m[3]))
            cols = line.rstrip("\n").split("\t")
            greek, _, translit = cols[1].partition(" (")
            if "¶" in greek:
                paragraph.add(key)
            eds = editions(cols[5])
            strong, _, grammar = cols[3].partition("=")
            word = [greek.replace("¶", ""), translit.rstrip(")"), cols[2], strong, grammar, cols[4].split("=")[0]]
            others = [[vm[1], plain_gloss(vm[3]), editions(vm[6])] for vm in VARIANT.finditer(cols[6])]
            every[key].append(word + [{"x": missing(eds)} if missing(eds) else {}])
            # A word the SBLGNT has in another place (marked SBL»1) is not counted as its own.
            if "SBL" in cols[5].split("+"):
                note = {}
                if missing(eds):
                    note["x"] = missing(eds)
                if others:
                    note["r"] = others
                words[key].append(word + [note])
                continue
            # Where the SBLGNT reads differently from this edition, TAGNT gives its reading
            # among the variants; this edition's reading is then the other one.
            for vm in VARIANT.finditer(cols[6]):
                if "SBL" in editions(vm[6]):
                    note = {"r": [[word[0], plain_gloss(word[2]), eds]] + [o for o in others if "SBL" not in o[2]]}
                    words[key].append([vm[1], vm[2], vm[3], vm[4], vm[5], "", note])
                    break
            else:
                if "SBL" not in eds:
                    added[key].append((len(words[key]), word[0], word[2], eds))
    return words, paragraph, every, added


# The editions TAGNT compares. A word in all of them needs no note.
EDITIONS = ["NA28", "NA27", "Tyn", "SBL", "WH", "Treg", "TR", "Byz"]


def editions(field):
    """TAGNT's "+"-joined editions, without its marks of word order (TR»1)."""
    out = []
    for e in re.split(r"[+\s]+", field.strip()):
        e = re.sub(r"[»«]\d*$", "", e)
        if e and e not in out:
            out.append(e)
    return out


def missing(eds):
    return [e for e in EDITIONS if e not in eds] if any(e in EDITIONS for e in eds) else []


HEB_VARIANT = re.compile(r"(?:^|;\s*|\s)([A-Z])=\s*([^\s(\"]*)\s*(?:\(([^)]*)\))?\s*\"([^\"]*)\"")


def heb_clean(h):
    return re.sub(r"[\\׃]", "", h.split("\\")[0]).replace("/", "")


def plain_gloss(g):
    """A gloss without STEPBible's marks for words implied (<the>) or supplied ([is])."""
    return re.sub(r"[<>\[\]]", "", gloss_clean(g))


def hebrew_note(r):
    """Where a Hebrew word's manuscripts differ in sense: the written form (ketiv) of a word
    read otherwise (qere), and readings of other manuscripts that change the meaning."""
    kind, note = r[-1], {}
    letters = re.search(r"\(([^)]*)\)", kind)
    for m in HEB_VARIANT.finditer(r[6] if len(r) > 6 else ""):
        siglum, translit, hebrew, gloss = m[1], m[2], (m[3] or "").replace("/", ""), m[4]
        if siglum == "K" and kind.startswith("Q(K)"):
            note["k"] = [heb_clean(hebrew), translit.replace("/", "").replace(".", ""), plain_gloss(gloss)]
        elif letters and siglum in letters[1] and siglum != "K":
            note.setdefault("r", []).append([siglum, heb_clean(hebrew), plain_gloss(gloss)])
    return note


def hebrew_tokens(text):
    """Our Hebrew verse as words: split at spaces and after each maqaf. A written form
    (ketiv, marked *) is kept for display but not matched; its reading (qere, **) is."""
    out = []
    for tok in text.split():
        if tok in ("׀", "פ", "ס", "׆"):
            continue
        for part in re.findall(r"[^־]+־?", tok):
            kind = "q" if part.startswith("**") else "k" if part.startswith("*") else ""
            part = part.lstrip("*")
            if HEB_LETTER.search(part):
                out.append((part, kind))
    return out


def greek_norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(ch for ch in w if "α" <= ch <= "ω" or ch == "ς").replace("ς", "σ")


def align(ours, theirs):
    """Match two word lists by their keys; returns, for each of ours, the index of its match
    or None. Unequal stretches between matches are paired off only when the same length."""
    match = [None] * len(ours)
    sm = difflib.SequenceMatcher(None, ours, theirs, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                match[i1 + k] = j1 + k
    return match


def translit_heb(t):
    return t.replace("/", "").replace(".", "").replace("-", "").lower()


def short(strong):
    """H0430G -> 430G: the language is known from the testament."""
    return re.sub(r"^[HG]0*", "", strong)


def gloss_clean(g):
    g = re.sub(r"\s+", " ", g.replace("/ ", " ").replace("/", " ")).strip()
    return re.sub(r"[,.;:·?!¶]+$", "", g)


# --- Lexicons -------------------------------------------------------------------------------

STEP_TO_SLUG = {code: SLUG_OF[OSIS_OF[code]] for code in STEP_CODES}


def clean_definition(text):
    """A lexicon entry as light markup: **bold**, _italic_, line breaks, and verse links
    written [[slug.chapter.verse|label]]."""
    def ref(m):
        target, label = m[1], m[2]
        r = re.match(r"([1-3]?[A-Z][a-z]{1,2})\.(\d+)(?:\.(\d+))?", target)
        if not r or r[1] not in STEP_TO_SLUG:
            return label
        return f"[[{STEP_TO_SLUG[r[1]]}.{r[2]}.{r[3] or 1}|{label}]]"
    t = re.sub(r"<ref='([^']*)'>(.*?)</ref>", ref, text)
    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
    t = re.sub(r"(?i)</?b>", "**", t)
    t = re.sub(r"(?i)</?i>", "_", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("__", "").replace("†", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*", "\n", t).strip()
    return t.lstrip(":").strip()


def lexicon(key):
    """{dStrong: [lemma, transliteration, grammar, gloss, definition]}"""
    out = {}
    for path in step_paths(key):
        started = False
        for line in open(path, encoding="utf-8"):
            cols = line.rstrip("\n").split("\t")
            if cols[0].startswith("eStrong"):
                started = True
                continue
            if not started or len(cols) < 8 or not re.match(r"[HG]\d", cols[0]):
                continue
            strong = cols[1].split(" ")[0].strip()
            if strong in out:
                continue
            out[strong] = [cols[3], cols[4], cols[5], cols[6], clean_definition(cols[7])]
    return out


# --- Markup ---------------------------------------------------------------------------------

def plain(text):
    """English verse text without note markers or markup, for search."""
    text = re.sub(r"\[\^\w+\]", "", text)
    return text.replace("*", "")


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")


def group_runs(items):
    """Added words as runs: those at one place in the verse (and, in Greek, in the same
    editions) together, as (place, [words])."""
    out = []
    for it in items:
        if out and out[-1][0] == it[0] and (len(it) < 4 or out[-1][1][0][3] == it[3]):
            out[-1][1].append(it)
        else:
            out.append((it[0], [it]))
    return out


def variants_note(vch, v, wnotes, adds, match):
    """data/bible/variants/NN-book.json, for one verse:
        "w": {word: note}    by our word's place in the verse (from 0):
                               "x": [editions]  the editions that leave the word out
                               "r": [[word, gloss, [editions]]]  other readings and where
                               "k": [Hebrew, transliteration, gloss]  how it is written (ketiv)
                               "r": [[manuscript, Hebrew, gloss]]  other Hebrew manuscripts
        "a": [[after, words, gloss, [editions]]]  words other editions add, after our word
                               "after" (-1 at the verse's start); "LXX" marks the words restored
                               to the Hebrew from the Septuagint.
        "s": [[first, last, [editions]]]  a run of our words the editions leave out
        "b": [editions]  a verse the SBLGNT prints in double brackets, and the editions that
                               leave it out
    Editions are TAGNT's: NA28, NA27, Tyn, SBL, WH, Treg, TR, Byz, and a few manuscripts."""
    entry = vch.get(str(v), {})
    # Three or more words in a row left out by the same editions, with nothing else to say of
    # them, are one span: "s": [[first, last, [editions]]].
    run, spans = [], []
    for i in sorted(wnotes) + [None]:
        n = wnotes.get(i) if i is not None else None
        if n is not None and set(n) == {"x"} and run and i == run[-1] + 1 and wnotes[run[-1]] == n:
            run.append(i)
            continue
        if len(run) >= 3:
            spans.append([run[0], run[-1], wnotes[run[0]]["x"]])
            for k in run:
                del wnotes[k]
        run = [i] if n is not None and set(n) == {"x"} else []
    if spans:
        entry["s"] = spans
    if wnotes:
        entry["w"] = {str(i): n for i, n in wnotes.items()}
    if adds:
        ours = {j: i for i, j in enumerate(match) if j is not None}
        entry["a"] = [[max((ours[j] for j in ours if j < pos), default=-1)] + a[1:] for a in adds for pos in [a[0]]]
    if entry:
        vch[str(v)] = entry


def main():
    heb, english_numbers, heb_extra = hebrew_words()
    grk, greek_paragraphs, grk_every, grk_added = greek_words()
    lex = {"H": lexicon("tbesh"), "G": lexicon("tbesg")}
    used = collections.defaultdict(set)
    books, search = [], []
    stats = collections.Counter()
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        source = {}
        for c, v, t in parse_book_md(os.path.join(ROOT, "text", "hebrew" if testament == "OT" else "greek",
                                                  stem + ".md")):
            source.setdefault(c, {})[v] = t
        chapters, word_chapters, statuses, variants = [], [], [], {}
        for c in sorted(source):
            path = os.path.join(ROOT, "translation", stem, f"{c:03d}.md")
            meta, verses, notes = parse_chapter(path)
            statuses.append(meta.get("status", "draft"))
            ch = {"c": c, "s": meta.get("status", "draft"), "v": [], "n": notes}
            wch, vch = {}, {}
            # Where the translation reopens a continuing speech at a verse, it starts a new
            # paragraph there (TRANSLATION.md), so the reader does too.
            reopen = {v for v, kind, _ in quote_events(verses) if kind == "reopen"}
            for v in sorted(source[c]):
                src = source[c][v]
                en = verses.get(v)
                row = [v, en if en is not None else None, src]
                extra = {}
                if testament == "OT":
                    if re.search(r"\s[פס]\s*$", src):        # an open or closed paragraph mark
                        extra["p"] = 1
                    if (osis, c, v) in english_numbers:
                        extra["e"] = "%d:%d" % english_numbers[(osis, c, v)]
                    toks = hebrew_tokens(src)
                    rows = heb.get((osis, c, v), [])
                    keys = [re.sub(r"[^א-ת]", "", t[0]) if t[1] != "k" else "\0" for t in toks]
                    theirs = ["".join(HEB_LETTER.findall(r[1].split("\\")[0])) for r in rows]
                    match = align(keys, theirs)
                    ws, wnotes = [], {}
                    for i, ((tok, kind), j) in enumerate(zip(toks, match)):
                        stats["words"] += 1
                        if kind == "k":
                            ws.append("|||ketiv")
                            continue
                        if j is None:
                            ws.append("")
                            continue
                        stats["aligned"] += 1
                        r = rows[j]
                        strongs = re.sub(r"\\.*", "", r[4]).split("/")
                        main = next((i for i, s in enumerate(strongs) if s.startswith("{")), len(strongs) - 1)
                        strongs = [s.strip("{}+") for s in strongs]
                        for s in strongs:
                            used["H"].add(s)
                        w = [translit_heb(r[2]), gloss_clean(r[3]), "/".join(short(s) for s in strongs),
                             r[5]]
                        if main != len(strongs) - 1:
                            w.append(str(main))
                        ws.append("|".join(w))
                        note = hebrew_note(r)
                        if note:
                            wnotes[i] = note
                    wch[v] = "¦".join(ws)
                    adds = [[pos, " ".join(heb_clean(x[1]) for x in grp), " ".join(plain_gloss(x[2]) for x in grp), ["LXX"]]
                            for pos, grp in group_runs(heb_extra.get((osis, c, v), []))]
                    variants_note(vch, v, wnotes, adds, match)
                else:
                    if (osis, c, v) in greek_paragraphs:
                        extra["p"] = 1
                    toks = [t for t in src.split() if greek_norm(t)]
                    rows = grk.get((osis, c, v)) or grk_every.get((osis, c, v), [])
                    match = align([greek_norm(t) for t in toks], [greek_norm(r[0]) for r in rows])
                    ws, wnotes = [], {}
                    for i, (tok, j) in enumerate(zip(toks, match)):
                        stats["words"] += 1
                        if j is None:
                            ws.append("")
                            continue
                        stats["aligned"] += 1
                        g, tr, gloss, strong, grammar, _, note = rows[j]
                        used["G"].add(strong)
                        ws.append("|".join([tr, gloss_clean(gloss), short(strong), grammar]))
                        if note:
                            wnotes[i] = note
                    wch[v] = "¦".join(ws)
                    adds = [[pos, " ".join(x[1] for x in grp), " ".join(plain_gloss(x[2]) for x in grp), grp[0][3]]
                            for pos, grp in group_runs(grk_added.get((osis, c, v), []))]
                    if not grk.get((osis, c, v)) and rows:
                        # A verse the SBLGNT prints in double brackets, as not in the earliest
                        # manuscripts: a note on the verse, not on each word.
                        out = sorted(set.intersection(*(set(r[6].get("x", [])) for r in rows)) - {"SBL"}, key=EDITIONS.index)
                        wnotes, adds = {}, []
                        vch[str(v)] = {"b": out}
                    variants_note(vch, v, wnotes, adds, match)
                if v + 1 in reopen:
                    extra["p"] = 1
                if extra:
                    row.append(extra)
                ch["v"].append(row)
                if en:
                    search.append([stem, c, v, plain(en)])
            chapters.append(ch)
            word_chapters.append({"c": c, "w": wch})
            if vch:
                variants[c] = vch
        write_json(os.path.join(OUT, "text", stem + ".json"),
                   {"book": name, "osis": osis, "t": testament, "chapters": chapters})
        write_json(os.path.join(OUT, "words", stem + ".json"), {"book": name, "chapters": word_chapters})
        write_json(os.path.join(OUT, "variants", stem + ".json"), {"book": name, "c": variants})
        books.append({"n": name, "osis": osis, "slug": stem, "t": testament, "s": statuses})
        stats["chapters"] += len(chapters)
    # Lexicon, in chunks of a thousand Strong's numbers, holding only the entries used.
    chunks = collections.defaultdict(dict)
    missing = 0
    for lang in ("H", "G"):
        by_base = {}
        for k in lex[lang]:
            by_base.setdefault(re.match(r"[HG]\d+", k)[0], k)
        for s in sorted(used[lang]):
            base = re.match(r"[HG]\d+", s)
            if not base:
                missing += 1
                continue
            entry = lex[lang].get(s) or lex[lang].get(by_base.get(base[0], ""))
            if not entry:
                missing += 1
                continue
            chunks[f"{lang.lower()}{int(re.match(r'[HG](\d+)', s)[1]) // 1000:02d}"][short(s)] = entry
    for name, data in chunks.items():
        write_json(os.path.join(OUT, "lexicon", name + ".json"), data)
    write_json(os.path.join(OUT, "books.json"), books)
    write_json(os.path.join(OUT, "search.json"), search)
    print(f"Reader: {stats['chapters']} chapters; {stats['aligned']:,} of {stats['words']:,} words matched "
          f"({stats['aligned'] / stats['words']:.2%}); {sum(len(v) for v in chunks.values()):,} lexicon entries "
          f"in {len(chunks)} files ({missing} Strong's numbers without an entry)")


if __name__ == "__main__":
    main()
