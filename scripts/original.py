"""The Hebrew, Aramaic and Greek as a version the reader can show, alone or beside another.

    python3 scripts/original.py            (after build.py; again after versions.py)

Reads   text/hebrew/NN-book.md (UXLC 2.6) and text/greek/NN-book.md (SBLGNT v1.2)
Writes  data/bible/versions/orig/NN-book.json   in the same form as the other versions
            ({"book", "chapters": [{"c", "v": [[verse, text], ...]}]}), in our numbering, which
            is the Hebrew numbering in the Old Testament and the SBLGNT's in the New, so each
            verse goes to its own place.
        data/bible/versions.json   adds (or refreshes) the "orig" entry

Ketiv and qere: the word as read (qere) stands in the text, with the word as written (ketiv)
after it in brackets; a word written but not read is in brackets alone. The UXLC note
marks ([t], [c], [q]...) are left out.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
from build import parse_book_md               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "bible")

ENTRY = {
    "id": "orig", "lang": "he", "short": "Hebrew & Greek", "name": "Hebrew, Aramaic and Greek",
    "license": "The original languages: the Hebrew and Aramaic of the Leningrad Codex (UXLC 2.6, Tanach.us; may be copied without restriction) and the SBL Greek New Testament (© 2010 Society of Biblical Literature and Logos Bible Software, CC BY 4.0). In the Hebrew, the word as written (ketiv) follows the word as read (qere) in brackets.",
    "url": "https://tanach.us",
    "notice": "Hebrew and Aramaic: Unicode/XML Leningrad Codex (UXLC 2.6), Tanach.us. Greek: SBL Greek New Testament, © 2010 Society of Biblical Literature and Logos Bible Software, CC BY 4.0.",
    "cite": "Hebrew/Greek", "share": "Leningrad Codex (UXLC) · SBL Greek New Testament",
}


def ketiv_qere(text):
    text = re.sub(r"\[[a-z]\]", "", text)                        # the UXLC's note marks ([t], [q]...)
    text = re.sub(r"\*(\S+) \*\*(\S+)", r"\2 [\1]", text)       # written, then read
    text = re.sub(r"(?<!\*)\*\*(\S+)", r"\1", text)              # read but not written
    text = re.sub(r"(?<![\*\[])\*(\S+)", r"[\1]", text)          # written but not read
    return text.replace("*", "")


def main():
    out_dir = os.path.join(OUT, "versions", "orig")
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        folder = "hebrew" if testament == "OT" else "greek"
        chapters = {}
        for c, v, t in parse_book_md(os.path.join(ROOT, "text", folder, stem + ".md")):
            t = ketiv_qere(t.strip()) if testament == "OT" else t.strip()
            chapters.setdefault(c, []).append([v, t])
            total += 1
        data = {"book": name, "chapters": [{"c": c, "v": chapters[c]} for c in sorted(chapters)]}
        with open(os.path.join(out_dir, stem + ".json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
            fh.write("\n")
    path = os.path.join(OUT, "versions.json")
    with open(path, encoding="utf-8") as fh:
        listing = [v for v in json.load(fh) if v.get("id") != "orig"]
    listing.append(ENTRY)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(listing, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"orig: {total:,} verses")


if __name__ == "__main__":
    main()
