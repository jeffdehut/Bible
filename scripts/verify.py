"""Verify the texts in sources/ and text/ against their published reference editions.

    python3 scripts/verify.py

Downloads (into .cache/, which git ignores):
  - UXLC text files from https://tanach.us (current release)
  - Dr. Maurice Robinson's Scrivener 1894 files from https://github.com/byztxt/greektext-scrivener

Then checks, verse by verse:
  1. sources/hebrew-uxlc   == UXLC reference text
  2. sources/greek-tr-...  == Robinson's Scrivener 1894 (word for word)
  3. text/greek            == sources/greek-tr-... after transliteration (round trip)
Exits non-zero if anything differs.
"""

import csv
import io
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

from books import BOOKS, file_stem
from build import GREEK, GREEK_SPECIAL, parse_greek, parse_hebrew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")

UXLC_ZIP = "https://tanach.us/TextFiles/Tanach.txt.zip"
SCRIVENER_GIT = "https://github.com/byztxt/greektext-scrivener"

UXLC_NAMES = {
    "1 Samuel": "Samuel_1", "2 Samuel": "Samuel_2", "1 Kings": "Kings_1", "2 Kings": "Kings_2",
    "1 Chronicles": "Chronicles_1", "2 Chronicles": "Chronicles_2", "Song of Songs": "Song_of_Songs",
}
SCRIVENER_CODES = ("MT MR LU JOH AC RO 1CO 2CO GA EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM "
                   "HEB JAS 1PE 2PE 1JO 2JO 3JO JUDE RE").split()


def fetch_uxlc():
    out = os.path.join(CACHE, "uxlc")
    if not os.path.isdir(out):
        print(f"Downloading {UXLC_ZIP}")
        req = urllib.request.Request(UXLC_ZIP, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req) as r:
            zipfile.ZipFile(io.BytesIO(r.read())).extractall(out)
    return os.path.join(out, "TextFiles")


def fetch_scrivener():
    out = os.path.join(CACHE, "greektext-scrivener")
    if not os.path.isdir(out):
        print(f"Cloning {SCRIVENER_GIT}")
        subprocess.run(["git", "clone", "-q", "--depth", "1", SCRIVENER_GIT, out], check=True)
    return os.path.join(out, "textonly")


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


def report(label, ours, ref):
    bad = [k for k in sorted(set(ours) | set(ref)) if ours.get(k) != ref.get(k)]
    for c, v in bad[:5]:
        print(f"  {label} {c}:{v}\n    ours: {ours.get((c, v))}\n    ref : {ref.get((c, v))}")
    return len(bad)


def main():
    uxlc = fetch_uxlc()
    scrivener = fetch_scrivener()
    to_greek = {v: k for k, v in GREEK_SPECIAL.items()}
    failures = 0
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        if testament == "OT":
            _, ours = parse_hebrew(os.path.join(ROOT, "sources", "hebrew-uxlc", stem + ".txt"))
            _, ref = parse_hebrew(os.path.join(uxlc, UXLC_NAMES.get(name, name) + ".txt"))
            n = report(osis, {(c, v): t for c, v, t in ours}, {(c, v): t for c, v, t in ref})
        else:
            src = parse_greek(os.path.join(ROOT, "sources", "greek-tr-scrivener", stem + ".txt"))
            raw = {}
            with open(os.path.join(ROOT, "sources", "greek-tr-scrivener", stem + ".txt"), encoding="ascii") as f:
                for line in f:
                    m = re.match(r"(\d+):(\d+) (.+)", line.strip())
                    raw[(int(m[1]), int(m[2]))] = " ".join(m[3].split())
            code = SCRIVENER_CODES[num - 40]
            n = report(osis, raw, parse_scrivener(os.path.join(scrivener, code + ".SCV")))
            # Round trip: text/greek back to the ASCII transliteration.
            back = {v: k for k, v in GREEK.items()}
            back["ς"] = "v"
            built = {}
            with open(os.path.join(ROOT, "text", "greek", stem + ".tsv"), encoding="utf-8") as f:
                for row in list(csv.reader(f, delimiter="\t"))[1:]:
                    words = [to_greek.get(w) or "".join(back[c] for c in w) for w in row[2].split()]
                    built[(int(row[0]), int(row[1]))] = " ".join(words)
            n += report(osis + " (text/)", built, raw)
            if len(src) != len(raw):
                n += 1
        if n:
            print(f"{name}: {n} differing verses")
        failures += n
    print("All 66 books match their reference editions." if not failures
          else f"{failures} differences found.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
