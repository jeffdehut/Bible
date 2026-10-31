"""Word maps: where each word of the Hebrew, Aramaic or Greek falls in each translation's verse.

    python3 scripts/wordmaps.py            (after reader.py and versions.py)

Reads   .cache/versions/<eBible id>/       the versions' USFM, whose words carry Strong's numbers
        data/bible/versions/<id>/NN-book.json   the versions as the reader shows them (to check)
        data/bible/text/NN-book.json       our own English, as the reader shows it
        data/bible/words/NN-book.json      the source words of each verse, with their glosses
Writes  data/bible/wordmaps/<wording>/NN-book.json
            {"chapters": [{"c": 1, "v": {"1": [gap, length, strong, gap, length, strong, ...]}}]}
            each word's start counted from the end of the word before (the first from the start
            of the verse), in the characters of the verse as the reader shows it; strong is the
            number alone (H in the Old Testament, G in the New), its letter left off.
        data/bible/wordmaps/index.json     the wordings that have a map

Why: a highlight, a note or an emoji is made on the words of one wording, and the reader shows
it in every other by the words of the original they stand for: the words marked are found by
their Strong's numbers (and which time in the verse each comes), and marked where that wording
has them. The study markings, defined by Strong's numbers, are found the same way. A wording
with no map (a translation without Strong's numbers, as the Chinese ones for now) falls back to
finding the words' own text, or the end of the verse.

Our own English has no Strong's numbers of its own, so its map is made by alignment: each word
is matched to a word of the Berean Standard Bible's same verse with the same stem (which carries
a number), or else to a source word whose gloss has that stem. Words that match nothing (the
small words, mostly) are left out of the map, which is all the mapping needs.
"""

import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
import versions                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
OUT = os.path.join(DATA, "wordmaps")
A, B, C = "\x01", "\x02", "\x03"     # around a word and its number, while the text is cleaned


def clean_keep(text):
    """versions.clean, keeping each tagged word as A word B number C."""
    text = re.sub(r"\\f\s.*?\\f\*", "", text, flags=re.S)
    text = re.sub(r"\\x\s.*?\\x\*", "", text, flags=re.S)
    text = re.sub(r"\\fig\s.*?\\fig\*", "", text, flags=re.S)

    def word(m):
        n = re.search(r'strong="[HG]?0*(\d+)', m.group(2) or "")
        return A + m.group(1) + B + (n.group(1) if n else "") + C if n else m.group(1)
    text = re.sub(r"\\\+?w\s+([^|\\]*?)(?:\|([^\\]*?))?\\\+?w\*", word, text)
    text = re.sub(r"\\\+?[a-z]+[0-9]?\*", "", text)
    text = re.sub(r"\\\+?[a-z]+[0-9]?\s?", "", text)
    text = text.replace("¶", "")
    return re.sub(r"\s+", " ", text).strip()


def unmark(text):
    """The plain text, and its words: [start, end, strong]."""
    out, flat, i = [], [], 0
    for m in re.finditer(A + "(.*?)" + B + "(.*?)" + C, text):
        out.append(text[i:m.start()])
        at = sum(len(x) for x in out)
        out.append(m.group(1))
        if m.group(2):
            flat += [at, at + len(m.group(1)), int(m.group(2))]
        i = m.end()
    out.append(text[i:])
    return "".join(out), flat


def packed(flat):
    """[start, end, strong, ...] as [gap, length, strong, ...]: each start counted from the end of
    the word before, which keeps the numbers (and the files) small."""
    out, last = [], 0
    for i in range(0, len(flat), 3):
        out += [flat[i] - last, flat[i + 1] - flat[i], flat[i + 2]]
        last = flat[i + 1]
    return out


def write(wording, stem, chapters):
    os.makedirs(os.path.join(OUT, wording), exist_ok=True)
    data = {"chapters": [{"c": c, "v": {str(v): packed(chapters[c][v]) for v in sorted(chapters[c])}} for c in sorted(chapters)]}
    with open(os.path.join(OUT, wording, stem + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, separators=(",", ":"))
        f.write("\n")


def version_maps(vid, src):
    """A version's map, from its own Strong's numbers; None if it has none."""
    folder = versions.usfm_dir(src)
    files = {re.match(r"\d+-(\w{3})", f).group(1): f for f in os.listdir(folder) if re.match(r"\d+-\w{3}", f)}
    original = versions.clean
    versions.clean = clean_keep
    words = mismatch = 0
    maps = {}
    try:
        for bi, (num, osis, bname, testament) in enumerate(BOOKS):
            stem = file_stem(num, bname)
            f = files.get(versions.CODES[bi])
            if not f:
                continue
            ours = json.load(open(os.path.join(DATA, "text", stem + ".json"), encoding="utf-8"))
            shown = json.load(open(os.path.join(DATA, "versions", vid, stem + ".json"), encoding="utf-8"))
            shown = {(ch["c"], r[0]): r[1] for ch in shown["chapters"] for r in ch["v"]}
            theirs, _, _ = versions.parse(os.path.join(folder, f))
            _, rows, extra = versions.place_rows(theirs, ours, testament)
            chapters = collections.defaultdict(dict)
            for (c, v), text in list(rows.items()) + [((ec, ev), t) for ec, ev, t in extra]:
                plain, flat = unmark(text)
                if shown.get((c, v)) != plain:
                    mismatch += 1
                    continue
                if flat:
                    chapters[c][v] = flat
                    words += len(flat) // 3
            maps[stem] = chapters
    finally:
        versions.clean = original
    if words < 1000:
        return None
    print(f"{vid}: {words:,} words mapped" + (f", {mismatch} verses unlike the text shown (left out)" if mismatch else ""))
    return maps


# Our English: aligned to the BSB's tagged words, and to the source words' glosses.
WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
SMALL = {"the", "a", "an", "and", "of", "to", "in", "that", "for", "on", "with", "as", "at", "by", "from", "is", "be", "was", "were", "it", "this", "or", "but", "not"}


def stem_of(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"'s$", "", w)
    for suf in ("ing", "ed", "es", "s", "ly"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def counted(text):
    return re.sub(r"\[\^\w+\]", "", text or "").replace("*", "")


def ours_map(bsb):
    total = matched = 0
    for num, osis, bname, testament in BOOKS:
        stem = file_stem(num, bname)
        text = json.load(open(os.path.join(DATA, "text", stem + ".json"), encoding="utf-8"))
        words = json.load(open(os.path.join(DATA, "words", stem + ".json"), encoding="utf-8"))
        wch = {int(ch["c"]): ch["w"] for ch in words["chapters"]}
        ref = (bsb or {}).get(stem, {})
        shown = {}
        if bsb:
            vb = json.load(open(os.path.join(DATA, "versions", "bsb", stem + ".json"), encoding="utf-8"))
            shown = {(ch["c"], r[0]): r[1] for ch in vb["chapters"] for r in ch["v"]}
        chapters = collections.defaultdict(dict)
        for ch in text["chapters"]:
            c = int(ch["c"])
            for row in ch["v"]:
                v, plain = row[0], counted(row[1])
                # The BSB's numbered words in this verse, by stem.
                cands = []
                flat = ref.get(c, {}).get(v, [])
                btext = shown.get((c, v), "")
                for i in range(0, len(flat), 3):
                    cands.append((stem_of(btext[flat[i]:flat[i + 1]]), flat[i + 2], i // 3 / max(1, len(flat) // 3)))
                # The source words' glosses, by stem.
                gloss = []
                for t in (wch.get(c, {}).get(str(v), "") or "").split("¦"):
                    p = t.split("|")
                    if len(p) < 3:
                        continue
                    nums = [int(m.group()) for part in p[2].split("/") for m in [re.match(r"\d+", part)] if m and int(m.group()) < 9000]
                    if nums:
                        for g in WORD.findall(p[1]):
                            if g.lower() not in SMALL:
                                gloss.append((stem_of(g), nums[-1]))
                found = list(WORD.finditer(plain))
                used = set()
                out = []
                for k, m in enumerate(found):
                    w = m.group()
                    if w.lower() in SMALL:
                        continue
                    total += 1
                    st, pos = stem_of(w), k / max(1, len(found))
                    best = None
                    for j, (cs, num_, cp) in enumerate(cands):
                        if j not in used and cs == st and (best is None or abs(cp - pos) < best[0]):
                            best = (abs(cp - pos), j, num_)
                    if best:
                        used.add(best[1])
                        out += [m.start(), m.end(), best[2]]
                        matched += 1
                        continue
                    g = next((n for gs, n in gloss if gs == st), None)
                    if g:
                        out += [m.start(), m.end(), g]
                        matched += 1
                if out:
                    chapters[c][v] = out
        write("ours-en", stem, chapters)
    print(f"ours-en: {matched:,} of {total:,} words of substance mapped ({100 * matched / max(1, total):.0f}%)")


def main():
    have = []
    bsb = None
    for vid, (src, lang, *_rest) in versions.VERSIONS.items():
        maps = version_maps(vid, src)
        if not maps:
            print(f"{vid}: no Strong's numbers; it falls back to the words' text")
            continue
        for stem, chapters in maps.items():
            write(vid, stem, chapters)
        have.append(vid)
        if vid == "bsb":
            bsb = maps
    ours_map(bsb)
    have.insert(0, "ours-en")
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(have, f)
        f.write("\n")


if __name__ == "__main__":
    main()
