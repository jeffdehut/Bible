"""Verify sources/ and text/ against the published reference editions.

    python3 scripts/verify.py

Downloads (into .cache/, which git ignores):
  - UXLC text files from https://tanach.us (current release)
  - SBLGNT from https://github.com/LogosBible/SBLGNT (official SBL/Logos release)
  - MorphGNT SBLGNT from https://github.com/morphgnt/sblgnt (independent tokenization)
  - Robinson's Scrivener 1894 from https://github.com/byztxt/greektext-scrivener

Checks, verse by verse:
  1. Hebrew:   sources/hebrew-uxlc == UXLC reference text
  2. SBLGNT:   sources/greek-sblgnt == official text and apparatus files (byte for byte),
               == the official XML edition, and == MorphGNT (word for word)
  3. TR:       sources/greek-tr-scrivener == Robinson's Scrivener 1894 (word for word)
  4. Output:   every text/*.md file parses back to exactly its source text
Exits non-zero if anything differs.
"""

import filecmp
import io
import os
import re
import subprocess
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

from books import BOOKS, file_stem
from build import (SBLGNT_MARKERS, parse_book_md, parse_greek_tr, parse_hebrew,
                   parse_sblgnt)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
SOURCES = os.path.join(ROOT, "sources")

UXLC_ZIP = "https://tanach.us/TextFiles/Tanach.txt.zip"
REPOS = {
    "sblgnt": "https://github.com/LogosBible/SBLGNT",
    "morphgnt": "https://github.com/morphgnt/sblgnt",
    "scrivener": "https://github.com/byztxt/greektext-scrivener",
}

UXLC_NAMES = {
    "1 Samuel": "Samuel_1", "2 Samuel": "Samuel_2", "1 Kings": "Kings_1", "2 Kings": "Kings_2",
    "1 Chronicles": "Chronicles_1", "2 Chronicles": "Chronicles_2", "Song of Songs": "Song_of_Songs",
}
SCRIVENER_CODES = ("MT MR LU JOH AC RO 1CO 2CO GA EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM "
                   "HEB JAS 1PE 2PE 1JO 2JO 3JO JUDE RE").split()
# Verses where MorphGNT (text as of Jan 2024) differs from the official SBLGNT v1.2 release.
# All were reviewed: MorphGNT lacks John 7:53-8:11 (added in SBLGNT v1.2) and some later
# corrections in the official files (capitalized proper nouns, apparatus markers, punctuation).
# See VERIFICATION.md. Any difference not listed here fails the check.
MORPHGNT_KNOWN = {
    ("Matt", 21, 15), ("Matt", 27, 24), ("Mark", 4, 2), ("Mark", 7, 19), ("Luke", 18, 5),
    *(("John", 7, 53),), *(("John", 8, v) for v in range(1, 12)),
    ("Acts", 3, 25), ("Acts", 4, 9), ("Acts", 10, 29), ("Acts", 13, 43), ("1Cor", 13, 3),
    ("Titus", 3, 13), ("Jas", 2, 11), ("1Pet", 1, 6), ("2Pet", 3, 6), ("2Pet", 3, 16),
    ("1John", 1, 7), ("1John", 3, 7), ("Rev", 9, 11),
}

MORPHGNT_CODES = ("Mt Mk Lk Jn Ac Ro 1Co 2Co Ga Eph Php Col 1Th 2Th 1Ti 2Ti Tit Phm "
                  "Heb Jas 1Pe 2Pe 1Jn 2Jn 3Jn Jud Re").split()


def fetch_uxlc():
    out = os.path.join(CACHE, "uxlc")
    if not os.path.isdir(out):
        print(f"Downloading {UXLC_ZIP}")
        req = urllib.request.Request(UXLC_ZIP, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req) as r:
            zipfile.ZipFile(io.BytesIO(r.read())).extractall(out)
    return os.path.join(out, "TextFiles")


def fetch_repo(key):
    out = os.path.join(CACHE, key)
    if not os.path.isdir(out):
        print(f"Cloning {REPOS[key]}")
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPOS[key], out], check=True)
    return out


def words(text):
    return " ".join(text.split())


def parse_scrivener(path):
    """Robinson's .SCV files: free-flowing text, 'c:v' markers, [bracketed] book titles."""
    with open(path, encoding="ascii") as f:
        text = re.sub(r"\[[^\]]*\]", " ", f.read())
    verses, cur = {}, None
    for tok in text.split():
        m = re.fullmatch(r"(\d+):(\d+)", tok)
        if m:
            cur = (int(m[1]), int(m[2]))
            verses[cur] = []
        else:
            verses[cur].append(tok)
    return {k: " ".join(v) for k, v in verses.items()}


def parse_sblgnt_xml(path):
    """Rebuild each verse from the XML's <prefix>, <w> and <suffix> elements."""
    verses, cur = {}, None
    for el in ET.parse(path).getroot().iter():
        if el.tag == "verse-number":
            m = re.search(r"(\d+):(\d+)$", el.get("id"))
            cur = (int(m[1]), int(m[2]))
            verses[cur] = ""
        elif el.tag in ("prefix", "w") and cur is not None:
            verses[cur] += el.text or ""
        elif el.tag == "suffix" and cur is not None:
            verses[cur] += el.text or " "  # an empty suffix stands for a plain space
    return {k: words(v) for k, v in verses.items()}


def parse_morphgnt(path):
    """MorphGNT: one word per line, 'BBCCVV pos parsing text word normalized lemma'."""
    verses = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            ref, _, _, text = line.split(" ")[:4]
            # MorphGNT writes the elision mark as U+2019; the SBLGNT text uses U+02BC.
            verses.setdefault((int(ref[2:4]), int(ref[4:6])), []).append(text.replace("\u2019", "\u02bc"))
    return {k: " ".join(v) for k, v in verses.items()}


def compare(label, ours, ref):
    bad = [k for k in sorted(set(ours) | set(ref)) if ours.get(k) != ref.get(k)]
    for c, v in bad[:5]:
        print(f"  {label} {c}:{v}\n    ours: {ours.get((c, v))}\n    ref : {ref.get((c, v))}")
    if bad:
        print(f"{label}: {len(bad)} differing verses")
    return len(bad)


def nfc(verses):
    return {k: unicodedata.normalize("NFC", v) for k, v in verses.items()}


def as_dict(verses):
    return {(c, v): t for c, v, t in verses}


def main():
    uxlc = fetch_uxlc()
    sblgnt = fetch_repo("sblgnt")
    morphgnt = fetch_repo("morphgnt")
    scrivener = fetch_repo("scrivener")

    failures = 0
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        if testament == "OT":
            _, ours = parse_hebrew(os.path.join(SOURCES, "hebrew-uxlc", stem + ".txt"))
            _, ref = parse_hebrew(os.path.join(uxlc, UXLC_NAMES.get(name, name) + ".txt"))
            failures += compare(f"{osis} (UXLC)", as_dict(ours), as_dict(ref))
            failures += compare(f"{osis} (text/hebrew)",
                                as_dict(parse_book_md(os.path.join(ROOT, "text", "hebrew", stem + ".md"))),
                                as_dict(ours))
            continue

        # SBLGNT: byte-identical to the official files, then two independent comparisons.
        src = os.path.join(SOURCES, "greek-sblgnt", "text", stem + ".txt")
        for kind, sub in (("text", "sblgnt"), ("apparatus", "sblgntapp")):
            official = os.path.join(sblgnt, "data", sub, "text", osis + ".txt")
            if not filecmp.cmp(os.path.join(SOURCES, "greek-sblgnt", kind, stem + ".txt"), official, shallow=False):
                print(f"{osis}: sources/greek-sblgnt/{kind} differs from the official SBLGNT file")
                failures += 1
        _, sbl = parse_sblgnt(src, osis)
        sbl = {(c, v): words(t) for c, v, t in sbl}
        # The XML writes "word—word" where the text file has "word— word"; spacing only.
        undash = lambda d: {k: v.replace("— ", "—") for k, v in d.items()}
        failures += compare(f"{osis} (SBLGNT XML)", undash(sbl),
                            undash(parse_sblgnt_xml(os.path.join(sblgnt, "data", "sblgnt", "xml", osis + ".xml"))))
        # MorphGNT is NFC-normalized (e.g. U+037E Greek question mark becomes ';').
        mg = os.path.join(morphgnt, f"{num + 21}-{MORPHGNT_CODES[num - 40]}-morphgnt.txt")
        known = {(c, v) for b, c, v in MORPHGNT_KNOWN if b == osis}
        drop = lambda d: {k: v for k, v in d.items() if k not in known}
        failures += compare(f"{osis} (MorphGNT)", drop(nfc(sbl)), drop(nfc(parse_morphgnt(mg))))
        clean = {k: words(t.translate(SBLGNT_MARKERS)) for k, t in sbl.items()}
        failures += compare(f"{osis} (text/greek)",
                            as_dict(parse_book_md(os.path.join(ROOT, "text", "greek", stem + ".md"))), clean)

        # Scrivener TR.
        tr_src = os.path.join(SOURCES, "greek-tr-scrivener", stem + ".txt")
        raw = {}
        with open(tr_src, encoding="ascii") as f:
            for line in f:
                m = re.match(r"(\d+):(\d+) (.+)", line.strip())
                raw[(int(m[1]), int(m[2]))] = words(m[3])
        failures += compare(f"{osis} (Scrivener)", raw,
                            parse_scrivener(os.path.join(scrivener, "textonly", SCRIVENER_CODES[num - 40] + ".SCV")))
        failures += compare(f"{osis} (text/greek-tr)",
                            as_dict(parse_book_md(os.path.join(ROOT, "text", "greek-tr", stem + ".md"))),
                            as_dict(parse_greek_tr(tr_src)))

    print("All 66 books match their reference editions." if not failures
          else f"{failures} differences found.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
