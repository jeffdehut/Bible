"""Build the full lexicon entries the reader opens from a word: Brown-Driver-Briggs for the
Hebrew and Aramaic, and Liddell-Scott-Jones for the Greek.

    python3 scripts/lexicons.py

Reads   Open Scriptures' Hebrew Lexicon (BrownDriverBriggs.xml and LexicalIndex.xml): the text of
        Brown, Driver and Briggs (1906) is public domain; Open Scriptures' markup is CC BY 4.0.
        Cloned once into .cache/openscriptures/
        STEPBible TFLSJ: the full Liddell-Scott-Jones entries for the words of the New
        Testament, keyed by Strong's number (CC BY 4.0), downloaded once into .cache/stepbible/
Writes  data/bible/lexicon/bdb/NN.json   {Strong's number: [entry, ...]}, 100 numbers a file
        data/bible/lexicon/lsj/NN.json   {Strong's number: entry}, likewise

Entries use the reader's light markup (scripts/reader.py, clean_definition): **bold**,
_italic_, line breaks, and verse links [[NN-book.chapter.verse|label]]. LSJ's citations of
other Greek literature are written {{label|the works cited}}, which the reader shows as a
small label that opens to the list.
"""

import collections
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
import connections                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
OUT = os.path.join(ROOT, "data", "bible", "lexicon")
OSHL_REPO = "https://github.com/openscriptures/HebrewLexicon"
OSHL_COMMIT = "master"
TFLSJ = "Lexicons/TFLSJ  0-5624 - Translators Formatted full LSJ Bible lexicon - STEPBible.org CC BY.txt"
SLUG = {osis: file_stem(num, name) for num, osis, name, _ in BOOKS}
NT = {osis for _, osis, _, t in BOOKS if t == "NT"}


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def chunked(entries, folder):
    for name in os.listdir(folder) if os.path.isdir(folder) else []:
        os.remove(os.path.join(folder, name))
    files = collections.defaultdict(dict)
    for strong, entry in entries.items():
        files[int(re.match(r"\d+", strong)[0]) // 100][strong] = entry
    for n, data in files.items():
        write_json(os.path.join(folder, f"{n:02d}.json"), dict(sorted(data.items(), key=lambda kv: int(re.match(r"\d+", kv[0])[0]))))
    return len(files)


# ---------------------------------------------------------------- Brown-Driver-Briggs

def fetch_oshl():
    out = os.path.join(CACHE, "openscriptures", "HebrewLexicon")
    if not os.path.isdir(out):
        print(f"Cloning {OSHL_REPO}")
        subprocess.run(["git", "clone", "-q", "--depth", "1", OSHL_REPO, out], check=True)
    return out


def bdb_markup(xml):
    """One BDB entry's XML -> light markup."""
    def ref(m):
        target, label = m[1], m[2]
        r = re.fullmatch(r"([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)", target)
        if not r or r[1] not in SLUG:
            return label
        return f"[[{SLUG[r[1]]}.{r[2]}.{r[3]}|{label}]]"
    t = re.sub(r"<status[^>]*>.*?</status>", "", xml, flags=re.S)
    t = re.sub(r'<ref r="([^"]+)"[^>]*>(.*?)</ref>', ref, t, flags=re.S)
    t = re.sub(r'<sense n="([^"]+)">', lambda m: f"\n**{m[1]}.** ", t)
    t = re.sub(r"<stem>(.*?)</stem>", r"**\1**", t, flags=re.S)
    t = re.sub(r"<def>(.*?)</def>", r"**\1**", t, flags=re.S)
    t = re.sub(r"<(em|foreign|pos)\b[^>]*>(.*?)</\1>", r"_\2_", t, flags=re.S)
    t = re.sub(r"<page[^>]*/>", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t\r]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{2,}", "\n", t).strip()
    return t.replace("____", "").replace("****", "")


def bdb():
    base = fetch_oshl()
    text = open(os.path.join(base, "BrownDriverBriggs.xml"), encoding="utf-8-sig").read()
    by_id = {m[1]: bdb_markup(m[2]) for m in re.finditer(r'<entry id="([^"]+)"[^>]*>(.*?)</entry>', text, re.S)}
    index = open(os.path.join(base, "LexicalIndex.xml"), encoding="utf-8-sig").read()
    out = collections.defaultdict(list)
    for m in re.finditer(r'<xref ([^>]*)/>', index):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m[1]))
        if "strong" in attrs and attrs.get("bdb") in by_id:
            for s in attrs["strong"].split():
                if not re.fullmatch(r"\d+[a-z]?", s):
                    continue
                entry = by_id[attrs["bdb"]]
                if entry and entry not in out[s]:
                    out[s].append(entry)
    # The fullest entry first: the main word, before a homonym's short note.
    return {s: sorted(es, key=len, reverse=True) for s, es in out.items()}


# ---------------------------------------------------------------- Liddell-Scott-Jones

def lsj_markup(text):
    """One TFLSJ entry (light HTML) -> light markup."""
    def cite(m):
        title = re.sub(r"\s+", " ", html.unescape(m[1])).strip(" ;,")
        label = re.sub(r"<[^>]+>", "", m[2]).strip()
        return f"{{{{{label}|{title}}}}}"
    t = re.sub(r'<a href="javascript:void\(0\)" title="([^"]*)">(.*?)</a>', cite, text, flags=re.S)
    t = re.sub(r"<Level\d>(.*?)</Level\d>", r"\n\1", t, flags=re.S)
    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
    t = re.sub(r"(?i)</?b>", "**", t)
    t = re.sub(r"(?i)</?i>", "_", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("__", "").replace("****", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{2,}", "\n", t).strip()
    # A bracket that only held a citation: "[{{NT|...}}]" reads better without the brackets.
    return re.sub(r"\[(\{\{[^{}]*\}\})\]", r"\1", t)


def lsj():
    url = ("https://raw.githubusercontent.com/STEPBible/STEPBible-Data/"
           f"{connections.STEPBIBLE_COMMIT}/" + urllib.parse.quote(TFLSJ))
    path = connections.fetch(url, os.path.join(CACHE, "stepbible", connections.STEPBIBLE_COMMIT[:7], os.path.basename(TFLSJ)))
    out = {}
    started = False
    for line in open(path, encoding="utf-8"):
        cols = line.rstrip("\n").split("\t")
        if cols[0] == "eStrong":
            started = True
            continue
        if not started or len(cols) < 8 or not re.fullmatch(r"G\d+[A-Za-z]?", cols[0]):
            continue
        strong = re.sub(r"^G0*", "", cols[0])
        if strong and strong not in out:
            out[strong] = lsj_markup(cols[7])
    return out


def main():
    hb = bdb()
    gk = lsj()
    nb = chunked(hb, os.path.join(OUT, "bdb"))
    ng = chunked(gk, os.path.join(OUT, "lsj"))
    print(f"BDB: {len(hb)} Strong's numbers in {nb} files; LSJ: {len(gk)} in {ng} files")


if __name__ == "__main__":
    main()
