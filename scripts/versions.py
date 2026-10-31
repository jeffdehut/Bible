"""Other Bible versions for the reader: open translations a reader can switch to.

    python3 scripts/versions.py            (after reader.py)

Reads   each version's USFM from eBible.org (downloaded once into .cache/versions/) and our own
        data/bible/text/NN-book.json, for our verse numbering
Writes  data/bible/versions/<id>/NN-book.json   {"book", "chapters": [{"c", "v": [[verse, text, extra?], ...]}]}
            in our numbering: the Hebrew numbering in the Old Testament, as the reader shows it.
            {"to": n}: the version joins this verse and the ones after it up to n into one.
            The versions follow the English numbering; each verse goes to the verse of ours that
            stands for it (row[3]["e"] in our files). extra: {"p": 1} a paragraph ends after the
            verse; {"x": 1} a verse ours doesn't have (as Matthew 17:21 in the King James).
        data/bible/versions.json   the versions, with their names, languages and licenses

Each version is the translation as published, with its footnotes, cross-references, headings
and Strong's numbers left out. Their licenses allow this (public domain, or CC BY-SA 4.0 with
attribution, which the reader shows with the version).
"""

import collections
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
import connections                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "bible")
CACHE = os.path.join(ROOT, ".cache", "versions")

# id: (eBible id, language, short name, full name, license line, source page)
VERSIONS = {
    "bsb": ("engbsb", "en", "BSB", "Berean Standard Bible", "Public domain. The Holy Bible, Berean Standard Bible, BSB, is produced in cooperation with Bible Hub, Discovery Bible, OpenBible.com, and the Berean Bible Translation Committee.", "https://berean.bible"),
    "web": ("engwebp", "en", "WEB", "World English Bible", "Public domain. World English Bible, by eBible.org.", "https://ebible.org/web/"),
    "kjv": ("eng-kjv2006", "en", "KJV", "King James Version", "Public domain (outside the United Kingdom). King James Version, 1769 text.", "https://ebible.org/kjv/"),
    "lsv": ("englsv", "en", "LSV", "Literal Standard Version", "Literal Standard Version, © 2020 Covenant Press. Licensed CC BY-SA 4.0 (creativecommons.org/licenses/by-sa/4.0).", "https://www.lsvbible.com"),
    "net": ("engnet", "en", "NET", "NET Bible®", "Scripture quoted by permission. Quotations designated (NET) are from the NET Bible® copyright ©1996, 2019 by Biblical Studies Press, L.L.C. https://netbible.com All rights reserved.", "https://netbible.org"),
    "cuv": ("cmn-cu89t", "zh-Hant", "和合本", "和合本（繁體）", "公有領域。中文和合本，新標點繁體版。", "https://ebible.org/cmn-cu89t/"),
    "ccb": ("cmncbt", "zh-Hant", "當代譯本", "當代譯本（開放資源版）", "聖經當代譯本（開放資源版），© 1979, 2005, 2007, 2012, 2023 Biblica, Inc. 按照 CC BY-SA 4.0 授權使用（creativecommons.org/licenses/by-sa/4.0）。", "https://ebible.org/cmncbt/"),
}
# What a version asks to be shown with its words: a line under each chapter (with its name linked
# to its site), and how a copied verse or a shared picture names it.
NOTICES = {
    "net": {"notice": "Scripture quoted by permission. Quotations designated (NET) are from the NET Bible® copyright ©1996, 2019 by Biblical Studies Press, L.L.C. All rights reserved.",
            "cite": "NET", "share": "NET Bible® · netbible.com"},
    "lsv": {"notice": "Literal Standard Version, © 2020 Covenant Press. Licensed CC BY-SA 4.0.", "cite": "LSV", "share": "Literal Standard Version (CC BY-SA 4.0)"},
    "ccb": {"notice": "聖經當代譯本（開放資源版）© Biblica, Inc. 按照 CC BY-SA 4.0 授權使用。", "cite": "當代譯本", "share": "當代譯本（CC BY-SA 4.0）"},
}
# USFM book codes, in our order.
CODES = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH",
         "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS",
         "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
         "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH",
         "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
PARA = {"p", "m", "pi", "pi1", "pi2", "mi", "nb", "b", "pc", "cls", "li", "li1", "q1", "qa", "pmo", "pm"}


def usfm_dir(src):
    folder = os.path.join(CACHE, src)
    if not os.path.isdir(folder) or not os.listdir(folder):
        z = connections.fetch(f"https://ebible.org/Scriptures/{src}_usfm.zip", os.path.join(CACHE, src + ".zip"))
        with zipfile.ZipFile(z) as f:
            f.extractall(folder)
    return folder


def clean(text):
    text = re.sub(r"\\f\s.*?\\f\*", "", text, flags=re.S)          # footnotes
    text = re.sub(r"\\x\s.*?\\x\*", "", text, flags=re.S)          # cross-references
    text = re.sub(r"\\fig\s.*?\\fig\*", "", text, flags=re.S)
    text = re.sub(r"\\\+?w\s+([^|\\]*?)(?:\|[^\\]*?)?\\\+?w\*", r"\1", text)   # \w word|strong\w*
    text = re.sub(r"\\\+?[a-z]+[0-9]?\*", "", text)                 # closing markers
    text = re.sub(r"\\\+?[a-z]+[0-9]?\s?", "", text)                # opening markers
    text = text.replace("¶", "")
    return re.sub(r"\s+", " ", text).strip()


def parse(path):
    """{(chapter, verse): text}, with "c:0" for a psalm's title, and the verses after which a
    paragraph ends."""
    verses, breaks, spans = {}, set(), {}
    c, v, buf, title = 0, None, [], []
    last = None
    pending_break = False

    def flush():
        nonlocal buf
        if v is not None and buf:
            t = clean(" ".join(buf))
            if t:
                verses[(c, v)] = (verses.get((c, v), "") + " " + t).strip()
        buf = []

    for line in open(path, encoding="utf-8-sig"):
        line = line.rstrip("\n")
        m = re.match(r"\\(\w+)\s?(.*)", line)
        tag, rest = (m.group(1), m.group(2)) if m else (None, line)
        if tag == "c":
            flush(); c = int(rest.split()[0]); v = None; last = None
            continue
        if tag in ("id", "h", "toc1", "toc2", "toc3", "mt", "mt1", "mt2", "mt3", "ms", "ms1", "s", "s1", "s2", "s3", "r", "rem", "ide", "sp", "cl", "imt", "ip", "is"):
            continue
        if tag == "d":          # a psalm's title
            flush(); v = None
            t = clean(rest)
            if t:
                verses[(c, 0)] = (verses.get((c, 0), "") + " " + t).strip()
            continue
        if tag in PARA or tag in ("q", "q2", "q3", "qr", "qc"):
            if tag in PARA and last is not None:
                pending_break = True
            if not rest.strip():
                continue
            if not rest.startswith("\\v"):
                buf.append(rest)
                continue
            line = rest
        for part in re.split(r"(?=\\v\s+\d)", line):
            mv = re.match(r"\\v\s+(\d+)(?:-(\d+))?\s?(.*)", part, re.S)
            if mv:
                flush()
                if pending_break and last is not None:
                    breaks.add(last)
                pending_break = False
                v = int(mv.group(1)); last = (c, v)
                if mv.group(2):
                    spans[(c, v)] = int(mv.group(2))   # verses joined into one: "20-21"
                buf = [mv.group(3)]
            elif part.strip():
                buf.append(part)
    flush()
    return verses, breaks, spans


def place_rows(theirs, ours, testament, stats=None):
    """Each verse of a version, in our numbering: ({English verse: our verse}, {our verse: text},
    [(chapter, verse, text) of verses ours doesn't have])."""
    stats = stats if stats is not None else collections.Counter()
    place = {}
    for ch in ours["chapters"]:
        for row in ch["v"]:
            e = row[3].get("e") if len(row) > 3 and isinstance(row[3], dict) else None
            ec, ev = map(int, e.split(":")) if e else (int(ch["c"]), row[0])
            place.setdefault((ec, ev), (int(ch["c"]), row[0]))
    # Each verse of the version goes to ours. One with no verse of ours of its own joins a
    # neighbor: in the Old Testament the verse before (a psalm's title and first line
    # share a verse in the Hebrew), and a title the verse after it; in the New Testament
    # it is a verse ours leaves out (Matthew 17:21), kept with its own number.
    rows, extra = {}, []
    for (ec, ev), text in sorted(theirs.items()):
        if (ec, ev) in place:
            key = place[(ec, ev)]
            rows[key] = (rows[key] + " " + text) if key in rows else text
            stats["placed"] += 1
            continue
        if ev == 0 and (ec, 1) in place:
            key = place[(ec, 1)]
            rows[key] = (text + " " + rows[key]) if key in rows else text
            stats["joined"] += 1
            continue
        prev = next((place[(ec, w)] for w in range(ev - 1, -1, -1) if (ec, w) in place), None)
        if testament == "OT" and prev:
            rows[prev] = (rows[prev] + " " + text) if prev in rows else text
            stats["joined"] += 1
        elif ev:
            extra.append((ec, ev, text))
            stats["extra"] += 1
    return place, rows, extra


def main():
    os.makedirs(os.path.join(OUT, "versions"), exist_ok=True)
    listing = []
    for vid, (src, lang, short, name, lic, url) in VERSIONS.items():
        folder = usfm_dir(src)
        # The book's code follows its number: "02-GENengbsb.usfm" -> "GEN".
        files = {re.match(r"\d+-(\w{3})", f).group(1): f for f in os.listdir(folder) if re.match(r"\d+-\w{3}", f)}
        out_dir = os.path.join(OUT, "versions", vid)
        os.makedirs(out_dir, exist_ok=True)
        stats = collections.Counter()
        for bi, (num, osis, bname, testament) in enumerate(BOOKS):
            stem = file_stem(num, bname)
            ours = json.load(open(os.path.join(OUT, "text", stem + ".json"), encoding="utf-8"))
            f = files.get(CODES[bi])
            if not f:
                stats["books missing"] += 1
                continue
            theirs, breaks, spans = parse(os.path.join(folder, f))
            place, rows, extra = place_rows(theirs, ours, testament, stats)
            chapters = collections.defaultdict(list)
            back = {v: k for k, v in place.items()}   # our verse -> the English verse it stands for
            for (c, v), text in rows.items():
                row = [v, text]
                eng = back.get((c, v))
                if eng in spans and (eng[0], spans[eng]) in place:
                    row += [{"to": place[(eng[0], spans[eng])][1]}]
                if eng in breaks:
                    row += [{}] if len(row) == 2 else []
                    row[2]["p"] = 1
                chapters[c].append(row)
            for ec, ev, text in extra:
                chapters[ec].append([ev, text, {"x": 1, **({"p": 1} if (ec, ev) in breaks else {})}])
            data = {"book": bname, "chapters": [{"c": c, "v": sorted(chapters[c], key=lambda r: r[0])} for c in sorted(chapters)]}
            with open(os.path.join(out_dir, stem + ".json"), "w", encoding="utf-8", newline="\n") as fh:
                json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
                fh.write("\n")
        listing.append({"id": vid, "lang": lang, "short": short, "name": name, "license": lic, "url": url, **NOTICES.get(vid, {})})
        print(f"{vid}: " + ", ".join(f"{k} {n:,}" for k, n in sorted(stats.items())))
    with open(os.path.join(OUT, "versions.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(listing, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
