"""Three pages for exploring and using the Bible's data: the cross-references as arcs
(arcs.html), the Visual Bible: the books as a bookshelf, and a page for each (library.html) and the open data to download
(downloads.html, with the archives in downloads/).

    python3 scripts/explore.py          (after reader.py and connections.py)

arcs.html loads data/graph.json when opened. library.html carries its numbers, counted here
from data/bible/text/ and data/bible/words/. downloads.html lists the files with their sizes,
and the archives are rebuilt each time with fixed dates, so an unchanged archive is unchanged.
"""

import datetime
import html
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webpages                                  # noqa: E402
from books import BOOKS, file_stem               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
TEMPLATES = os.path.join(ROOT, "scripts", "templates")

SECTIONS = [  # name, first book (index), colors for light and dark
    ("The Law", 0, ["#f2c45a", "#a8790a"]), ("History", 5, ["#f59a62", "#bf5a1f"]),
    ("Poetry and Wisdom", 17, ["#8fdc8a", "#2f8a3c"]), ("The Prophets", 22, ["#ff7272", "#c43434"]),
    ("The Gospels", 39, ["#6fb0ff", "#2459c4"]), ("Acts", 43, ["#4fd6cb", "#0f8c83"]),
    ("The Letters", 44, ["#b996ff", "#6d43c9"]), ("Revelation", 65, ["#ff86c0", "#c23a7c"]),
]
ARAMAIC = {"Ezra", "Dan"}


def section_of(i):
    return max(k for k, (_, first, _) in enumerate(SECTIONS) if i >= first)


def plain(text):
    text = re.sub(r"\[\^\w+\]", "", text or "")
    return text.replace("*", "")


def write(name, body):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.document(body.replace("<!-- APPBAR -->", webpages.appbar(name))))


def library():
    books = []
    for i, (num, osis, name, testament) in enumerate(BOOKS):
        stem = file_stem(num, name)
        text = json.load(open(os.path.join(DATA, "text", stem + ".json"), encoding="utf-8"))
        words = json.load(open(os.path.join(DATA, "words", stem + ".json"), encoding="utf-8"))
        verses = [row for ch in text["chapters"] for row in ch["v"] if row[1]]
        english = sum(len(plain(row[1]).split()) for row in verses)
        original = sum(len(v.split("¦")) for ch in words["chapters"] for v in ch["w"].values() if v)
        first = plain(text["chapters"][0]["v"][0][1])
        first = first if len(first) < 180 else first[:first.rfind(" ", 0, 170)] + " …"
        books.append({"n": name, "osis": osis, "t": testament, "s": section_of(i), "c": len(text["chapters"]),
                      "v": len(verses), "w": english, "o": original, "first": first,
                      "p": {"Ps": "psalms.html", "Prov": "proverbs.html"}.get(osis, f"visual/{stem[3:]}.html"),
                      "lang": "Greek" if testament == "NT" else "Hebrew and Aramaic" if osis in ARAMAIC else "Hebrew"})
    data = {"books": books, "sections": [{"n": n, "c": c} for n, _, c in SECTIONS]}
    src = open(os.path.join(TEMPLATES, "library.html"), encoding="utf-8").read()
    write("library.html", src.replace("<!-- DATA -->", f'<script type="application/json" id="data">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'))
    return len(books)


FIXED = (2026, 1, 1, 0, 0, 0)


def archive(name, files, readme):
    """downloads/NAME: the files (paths from the repository root), with a README."""
    os.makedirs(os.path.join(ROOT, "downloads"), exist_ok=True)
    path = os.path.join(ROOT, "downloads", name)
    with zipfile.ZipFile(path + ".part", "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(zipfile.ZipInfo("README.txt", FIXED), readme)
        for f in sorted(files):
            info = zipfile.ZipInfo(f, FIXED)
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(os.path.join(ROOT, f), "rb") as fh:
                z.writestr(info, fh.read())
    os.replace(path + ".part", path)
    return f"downloads/{name}"


def listing(folder, ext=".json"):
    return [os.path.join(folder, f) for f in sorted(os.listdir(os.path.join(ROOT, folder))) if f.endswith(ext)]


def size(path):
    full = os.path.join(ROOT, path)
    n = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(full) for f in fs) if os.path.isdir(full) else os.path.getsize(full)
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


def downloads():
    cite = ("The Open Plain English Translation (draft), CC BY 4.0, https://bibledata.org. "
            "Source texts: the Unicode/XML Leningrad Codex (UXLC 2.6) and the SBL Greek New Testament (CC BY 4.0).\n")
    md = archive("plain-english-bible-markdown.zip", listing("text/english", ".md") + ["translation/LICENSE.md"],
                 "The Open Plain English Translation: each book as Markdown, with its notes.\n\n" + cite)
    js = archive("plain-english-bible-json.zip", listing("data/bible/text") + ["data/bible/books.json", "translation/LICENSE.md"],
                 "The Open Plain English Translation as JSON, one file per book: for each chapter its status and\n"
                 "verses, each [number, English with [^note] markers, Hebrew or Greek, {p: paragraph end, e: English\n"
                 "verse number}], and its notes. The format is described in scripts/reader.py.\n\n" + cite)
    sections = [
        ("The translation", [
            (md, "Markdown, every book", "Each book as Markdown with its notes: the easiest to read or print.", "ZIP", "CC BY 4.0"),
            (js, "JSON, every book", "Each book as JSON, verse by verse, with the Hebrew or Greek beside the English.", "ZIP", "CC BY 4.0"),
            ("data/bible/search.json", "Every verse as plain text", "One file, verse by verse, without notes; what the reader searches.", "JSON", "CC BY 4.0"),
        ]),
        ("Words and lexicons", [
            ("data/bible/words/01-genesis.json", "Word-by-word data (Genesis; one file per book)", "Each verse's Hebrew or Greek words with a transliteration, gloss, Strong's number and grammar, from STEPBible's tagged texts. The other books are beside it in data/bible/words/.", "JSON", "CC BY 4.0"),
            ("data/bible/lexicon/h00.json", "Brief lexicons (one file per thousand words)", "STEPBible's abridged Brown–Driver–Briggs (Hebrew) and Abbott-Smith (Greek), by Strong's number, in data/bible/lexicon/.", "JSON", "CC BY 4.0"),
            ("data/bible/lexicon/bdb/00.json", "Brown–Driver–Briggs and Liddell–Scott–Jones in full", "The full entries, by Strong's number, in data/bible/lexicon/bdb/ and lsj/ (Open Scriptures; STEPBible).", "JSON", "CC BY 4.0"),
            ("data/bible/footprint/h00.json", "Where each word appears", "For each Strong's number, the chapters it appears in and how often, in data/bible/footprint/.", "JSON", "CC BY 4.0"),
        ]),
        ("People, places and connections", [
            ("data/graph.json", "The web of Scripture", "Every chapter, person, place and event, and the threads between them: cross-references, names, families and events, with the web's layout.", "JSON", "CC BY-SA 4.0"),
            ("data/genealogy.json", "The genealogy", "3,000 people with their parents, spouses, tribes and the verses that name them, laid out as a family tree.", "JSON", "CC BY-SA 4.0"),
            ("data/bible/people.json", "People, verse by verse", "The people each verse names, by their number in the genealogy.", "JSON", "CC BY-SA 4.0"),
            ("data/bible/places.json", "Places, verse by verse", "The places each verse names that the maps show, with the map to open each on.", "JSON", "CC BY 4.0"),
            ("data/history.json", "The timeline", "World history beside the Bible: eras, reigns, lives and events, with the synchronisms and the Bible's own chronology.", "JSON", "CC BY-SA 4.0"),
            ("data/rulers.csv", "Tables behind the timeline", "Rulers, periods, world events and synchronisms, compiled for this project (data/*.csv).", "CSV", "CC BY-SA 4.0"),
        ]),
        ("Study helps", [
            ("data/bible/study/topics.json", "Topics and dictionary", "Nave's Topical Bible and Easton's Bible Dictionary (both public domain), with the verses each cites, in data/bible/study/; Easton's comes through Theographic.", "JSON", "CC BY-SA 4.0"),
            ("data/bible/study/plans.json", "Reading plans", "Five plans, day by day, chapter by chapter.", "JSON", "CC BY 4.0"),
            ("data/bible/markings/rules.json", "Study markings", "The inductive markings: each marking's Strong's numbers and word forms, and in data/bible/markings/en/ every mark in the Bible.", "JSON", "CC BY 4.0"),
        ]),
        ("Maps", [
            ("maps/data/kingdoms.json", "The maps' data (one file per sheet)", "Every layer of each map as SVG path data and points, in maps/data/; each sheet also downloads as SVG from its page.", "JSON", "CC BY 4.0"),
            ("maps/atlas", "The 1915 historical atlas", "Forty plates of Smith and Bartholomew's Atlas of the Historical Geography of the Holy Land, in maps/atlas/.", "JPEG", "Public domain"),
        ]),
    ]
    out = []
    for head, items in sections:
        lis = []
        for path, title, desc, fmt, lic in items:
            href = path if not os.path.isdir(os.path.join(ROOT, path)) else "maps/atlas.html"
            lis.append(f'    <li><b>{html.escape(title)}</b><p>{html.escape(desc)}</p>'
                       f'<div class="meta"><span>{fmt}</span><span>{size(path)}</span><span class="lic">{lic}</span></div>'
                       f'<a class="dl" href="{href}"{" download" if href.endswith((".zip", ".csv")) else ""}>{"Open" if href.endswith(".html") else "Download"}</a></li>')
        out.append(f'  <h2>{html.escape(head)}</h2>\n  <ul class="items">\n' + "\n".join(lis) + "\n  </ul>")
    src = open(os.path.join(TEMPLATES, "downloads.html"), encoding="utf-8").read()
    write("downloads.html", src.replace("{{SECTIONS}}", "\n".join(out))
          .replace("{{DATE}}", datetime.date.today().strftime("%-d %B %Y")))


# The open-data page is turned off for now: downloads.html only sends visitors to the reader, and
# no archives are built. Set this to True to bring the page and its archives back.
DOWNLOADS = False
OFF = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=index.html">
<title>BibleData.org</title>
</head>
<body><p><a href="index.html">BibleData.org</a></p></body>
</html>
"""


def main():
    n = library()
    write("arcs.html", open(os.path.join(TEMPLATES, "arcs.html"), encoding="utf-8").read())
    if DOWNLOADS:
        downloads()
    else:
        with open(os.path.join(ROOT, "downloads.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(OFF)
    print(f"library.html: {n} books; arcs.html; downloads.html {'and downloads/' if DOWNLOADS else '(turned off)'}")


if __name__ == "__main__":
    main()
