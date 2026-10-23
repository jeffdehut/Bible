"""Show the source text of a chapter, for translating it.

    python3 scripts/source.py mark 14
    python3 scripts/source.py 41-mark 14
    python3 scripts/source.py "1 samuel" 3

Prints each verse of the chapter from text/hebrew (Old Testament) or text/greek (New Testament,
SBLGNT), with the information a translation note may cite:
  - New Testament: the SBLGNT apparatus for each verse (see TRANSLATION.md for the sigla).
  - Old Testament: ketiv/qere pairs, spelled out, and the English (KJV/NRSV) verse number
    wherever it differs from the Hebrew, from the TVTMS mapping used in connections/.
"""

import os
import re
import sys

from books import BOOKS, file_stem
from build import parse_book_md

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_book(arg):
    key = arg.lower().replace("_", " ")
    for book in BOOKS:
        num, osis, name, testament = book
        if key in (file_stem(num, name), name.lower(), osis.lower(), str(num)):
            return book
    sys.exit(f"unknown book {arg!r}; use a name such as 'Mark' or a stem such as '41-mark'")


def unescape(text):
    return re.sub(r"\\(.)", r"\1", text)


def english_numbers(osis):
    """{(c, v) Hebrew: (c, v) English} for one book, where they differ."""
    from connections import Versification, fetch_stepbible, load_texts
    vers = Versification(fetch_stepbible("tvtms"), load_texts())
    return {(hc, hv): (ec, ev) for (eb, ec, ev), (hb, hc, hv) in vers.to_hebrew.items() if hb == osis}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    num, osis, name, testament = find_book(sys.argv[1])
    chapter = int(sys.argv[2])
    stem = file_stem(num, name)
    folder = "hebrew" if testament == "OT" else "greek"
    verses = [(v, unescape(t)) for c, v, t in parse_book_md(os.path.join(ROOT, "text", folder, stem + ".md"))
              if c == chapter]
    if not verses:
        sys.exit(f"{name} has no chapter {chapter}")
    print(f"# {name} {chapter} ({'UXLC 2.6' if testament == 'OT' else 'SBLGNT v1.2'}), "
          f"{len(verses)} verses: {verses[0][0]}-{verses[-1][0]}\n")

    if testament == "NT":
        for v, t in verses:
            print(f"{v} {t}")
        app = open(os.path.join(ROOT, "apparatus", "greek", stem + ".md"), encoding="utf-8").read()
        print("\n## Apparatus (SBLGNT reading ] other readings)")
        for m in re.finditer(rf"^## {chapter}:(\d+)\n\n((?:- .*\n)+)", app, re.M):
            items = [unescape(line[2:]) for line in m.group(2).splitlines()]
            print(f"{m.group(1)}: " + " | ".join(items))
        return

    eng = english_numbers(osis)
    notes = []
    for v, t in verses:
        label = f"{v}" + (f" [English {eng[(chapter, v)][0]}:{eng[(chapter, v)][1]}]" if (chapter, v) in eng else "")
        print(f"{label} {t}")
        for k, q in re.findall(r"\*(\S+) \*\*(\S+)", t):
            notes.append(f"{v}: ketiv (written) {k} / qere (read) {q}")
        for k in re.findall(r"(?<!\*)\*(\S+)(?! \*\*)", re.sub(r"\*\S+ \*\*\S+", "", t)):
            notes.append(f"{v}: ketiv {k}, with no qere word (written but not read)")
        for q in re.findall(r"(?<!\*)\*\*(\S+)", re.sub(r"\*\S+ \*\*\S+", "", t)):
            notes.append(f"{v}: qere {q}, with no ketiv word (read but not written)")
    if notes:
        print("\n## Ketiv/qere (the marked word `*` is written; `**` is the reading tradition)")
        print("\n".join(notes))
    if any(key[0] == chapter for key in eng) or any(val[0] == chapter for val in eng.values()):
        print("\nEnglish verse numbers differ in this chapter; they are shown in brackets above.")


if __name__ == "__main__":
    main()
