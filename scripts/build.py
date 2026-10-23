"""Build normalized verse-per-line texts and books.json from the raw sources.

    python3 scripts/build.py

Reads  sources/hebrew-uxlc/*.txt        (UXLC Leningrad Codex export)
       sources/greek-tr-scrivener/*.txt (ASCII-transliterated Greek)
Writes text/hebrew/*.tsv, text/greek/*.tsv, books.json
"""

import json
import os
import re
import sys

from books import ARAMAIC, BOOKS, TANAKH_ORDER, file_stem

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEBREW_SRC = os.path.join(ROOT, "sources", "hebrew-uxlc")
GREEK_SRC = os.path.join(ROOT, "sources", "greek-tr-scrivener")

BIDI = dict.fromkeys(map(ord, "‪‫‬‎‏"))

# Transliteration used by the Greek source: one ASCII letter per Greek letter,
# with "v" for final sigma.
GREEK = dict(zip(
    "abgdezhyiklmnxoprstufcqwv",
    "αβγδεζηθικλμνξοπρστυφχψως",
))


def parse_hebrew(path):
    """Return (book name, declared chapters, declared verses, [(ch, vs, text)])."""
    title = declared = None
    chapter_counts = {}
    verses = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.translate(BIDI).rstrip("\r\n").strip()
            if line.startswith("xxxx"):
                line = line[4:].strip()
                m = re.match(r"(?!End of)(.+?) \((\d+) chapters, (\d+) verses\)\.$", line)
                if m:
                    title, declared = m.group(1), (int(m.group(2)), int(m.group(3)))
                m = re.match(r"Chapter (\d+)\s+\((\d+) verses\)$", line)
                if m:
                    chapter_counts[int(m.group(1))] = int(m.group(2))
                continue
            if not line:
                continue
            m = re.match(r"(\d+)\s*׃(\d+)\s+(.+)$", line)
            if not m:
                sys.exit(f"{path}: unrecognized line: {line!r}")
            verses.append((int(m.group(2)), int(m.group(1)), m.group(3).strip()))
    for ch, n in chapter_counts.items():
        actual = sum(1 for c, _, _ in verses if c == ch)
        if actual != n:
            sys.exit(f"{path}: chapter {ch} declares {n} verses, found {actual}")
    if declared != (len(chapter_counts), len(verses)):
        sys.exit(f"{path}: header says {declared}, found {len(chapter_counts)} chapters / {len(verses)} verses")
    return title, verses


def greek_word(word):
    out = "".join(GREEK[c] for c in word)
    return out[:-1] + "ς" if out.endswith("σ") else out


def parse_greek(path):
    verses = []
    with open(path, encoding="ascii") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = re.match(r"(\d+):(\d+) (.+)$", line)
            if not m:
                sys.exit(f"{path}: unrecognized line: {line!r}")
            words = m.group(3).split()
            bad = {c for w in words for c in w if c not in GREEK}
            if bad:
                sys.exit(f"{path} {m.group(1)}:{m.group(2)}: unexpected characters {bad}")
            verses.append((int(m.group(1)), int(m.group(2)), " ".join(map(greek_word, words))))
    return verses


def write_tsv(path, verses):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("chapter\tverse\ttext\n")
        for ch, vs, text in verses:
            f.write(f"{ch}\t{vs}\t{text}\n")


def main():
    index = []
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        if testament == "OT":
            src = os.path.join(HEBREW_SRC, stem + ".txt")
            title, verses = parse_hebrew(src)
            if title != name:
                sys.exit(f"{src}: header names {title!r}, expected {name!r}")
            out = os.path.join("text", "hebrew", stem + ".tsv")
            language = "Hebrew/Aramaic" if osis in ARAMAIC else "Hebrew"
        else:
            src = os.path.join(GREEK_SRC, stem + ".txt")
            verses = parse_greek(src)
            out = os.path.join("text", "greek", stem + ".tsv")
            language = "Greek"
        refs = [(c, v) for c, v, _ in verses]
        if len(set(refs)) != len(refs):
            sys.exit(f"{src}: duplicate verse references")
        write_tsv(os.path.join(ROOT, out), verses)
        entry = {
            "number": num,
            "osis": osis,
            "name": name,
            "testament": testament,
            "language": language,
            "chapters": len({c for c, _ in refs}),
            "verses": len(verses),
            "text": out,
            "source": os.path.relpath(src, ROOT),
        }
        if testament == "OT":
            entry["tanakh_order"] = TANAKH_ORDER.index(osis) + 1
        if osis in ARAMAIC:
            entry["aramaic_passages"] = ARAMAIC[osis]
        index.append(entry)

    with open(os.path.join(ROOT, "books.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")

    for t in ("OT", "NT"):
        books = [b for b in index if b["testament"] == t]
        print(f"{t}: {len(books)} books, {sum(b['chapters'] for b in books)} chapters, "
              f"{sum(b['verses'] for b in books)} verses")


if __name__ == "__main__":
    main()
