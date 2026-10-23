"""Build the Markdown reading texts and books.json from the raw sources.

    python3 scripts/build.py

Reads  sources/hebrew-uxlc/*.txt              UXLC Leningrad Codex text files
       sources/greek-sblgnt/text/*.txt        SBL Greek New Testament
       sources/greek-sblgnt/apparatus/*.txt   SBLGNT apparatus
       sources/greek-tr-scrivener/*.txt       Scrivener 1894 TR (ASCII transliteration)
Writes text/hebrew/*.md, text/greek/*.md, text/greek-tr/*.md, apparatus/greek/*.md, books.json
"""

import json
import os
import re
import sys

from books import ARAMAIC, BOOKS, TANAKH_ORDER, file_stem

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "sources")

BIDI = dict.fromkeys(map(ord, "‪‫‬‎‏"))

# Transliteration used by the Scrivener source: one ASCII letter per Greek letter,
# with "v" for final sigma.
GREEK = dict(zip(
    "abgdezhyiklmnxoprstufcqwv",
    "αβγδεζηθικλμνξοπρστυφχψως",
))

# Words that are not ordinary Greek words. "cxv" is the numeral 666 in Rev 13:18,
# printed with a stigma (ϛ = 6), not a final sigma.
GREEK_SPECIAL = {"cxv": "χξϛ"}

# SBLGNT apparatus markers in the running text. They only point into the apparatus,
# so the reading text leaves them out (the raw source keeps them).
SBLGNT_MARKERS = dict.fromkeys(map(ord, "⸀⸁⸂⸃⸄⸅"))

# Characters with meaning in Markdown that occur in the texts (*ketiv, [notes], brackets).
MD_SPECIAL = "\\`*_[]<>#|"

EDITIONS = {
    "hebrew": {
        "title": "Unicode/XML Leningrad Codex (UXLC) 2.6",
        "credit": "Unicode/XML Leningrad Codex: UXLC 2.6 (27.7), Tanach.us Inc., West Redding, CT, USA, Oct 2026. "
                  "Text may be copied without restriction.",
    },
    "greek": {
        "title": "SBL Greek New Testament (SBLGNT) v1.2",
        "credit": "Scripture quotations marked SBLGNT are from the SBL Greek New Testament. "
                  "Copyright © 2010 Society of Biblical Literature and Logos Bible Software. "
                  "Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).",
    },
    "greek-tr": {
        "title": "Textus Receptus, Scrivener 1894 (digitized by Maurice A. Robinson)",
        "credit": "Public domain. Digital text by Maurice A. Robinson (https://github.com/byztxt/greektext-scrivener). "
                  "Unaccented, as in the digital source.",
    },
}


def parse_hebrew(path):
    """Return (book name, [(chapter, verse, text)]), checking the declared verse counts."""
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
    if word in GREEK_SPECIAL:
        return GREEK_SPECIAL[word]
    out = "".join(GREEK[c] for c in word)
    return out[:-1] + "ς" if out.endswith("σ") else out


def parse_greek_tr(path):
    """Scrivener source: 'c:v text' lines. Returns [(chapter, verse, Unicode text)]."""
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
            bad = {c for w in words for c in w if c not in GREEK} - set().union(*map(set, GREEK_SPECIAL))
            if bad:
                sys.exit(f"{path} {m.group(1)}:{m.group(2)}: unexpected characters {bad}")
            verses.append((int(m.group(1)), int(m.group(2)), " ".join(map(greek_word, words))))
    return verses


def parse_sblgnt(path, osis):
    """SBLGNT text: a title line, then 'Book c:v<TAB>text' lines.

    Returns (title, [(chapter, verse, text with apparatus markers)]).
    """
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    title, verses = lines[0].strip(), []
    for line in lines[1:]:
        if not line.strip():
            continue
        m = re.match(rf"{re.escape(osis)} (\d+):(\d+)\t(.*)$", line)
        if not m:
            sys.exit(f"{path}: unrecognized line: {line!r}")
        verses.append((int(m.group(1)), int(m.group(2)), m.group(3).strip()))
    return title, verses


def parse_sblgnt_apparatus(path, name):
    """Apparatus: a title line, then 'Name c:v' headings, each followed by entry lines.

    Returns (title, [(chapter, verse, [entry lines])]).
    """
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip() for l in f.read().split("\n")]
    title, entries, cur = lines[0].strip(), [], None
    for line in lines[1:]:
        if not line:
            continue
        m = re.fullmatch(rf"{re.escape(name)} (\d+):(\d+)", line)
        if m:
            cur = (int(m.group(1)), int(m.group(2)), [])
            entries.append(cur)
        elif cur is None:
            sys.exit(f"{path}: apparatus entry before any reference: {line!r}")
        else:
            cur[2].append(line.strip())
    return title, entries


def md_escape(text):
    return "".join("\\" + c if c in MD_SPECIAL else c for c in text)


def md_unescape(text):
    return re.sub(r"\\(.)", r"\1", text)


def write_md(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def book_md(name, subtitle, edition, verses):
    """One book as Markdown: '## Chapter N' headings, one '**v** text' paragraph per verse."""
    ed = EDITIONS[edition]
    lines = [f"# {name}", ""]
    if subtitle:
        lines += [md_escape(subtitle), ""]
    lines += [f"> **Text:** {ed['title']}  ", f"> {ed['credit']}", ""]
    chapter = None
    for c, v, text in verses:
        if c != chapter:
            chapter = c
            lines += [f"## Chapter {c}", ""]
        lines += [f"**{v}** {md_escape(text)}", ""]
    return lines


def parse_book_md(path):
    """Inverse of book_md: returns [(chapter, verse, text)]. Used by verify.py."""
    verses, chapter = [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = re.fullmatch(r"## Chapter (\d+)", line)
            if m:
                chapter = int(m.group(1))
                continue
            m = re.fullmatch(r"\*\*(\d+)\*\* (.*)", line)
            if m:
                verses.append((chapter, int(m.group(1)), md_unescape(m.group(2))))
    return verses


APPARATUS_KEY = [
    "> **Apparatus:** SBLGNT v1.2, edited by Michael W. Holmes. Each entry gives the SBLGNT reading",
    "> and its support, then `]`, then the variant readings.  ",
    "> **WH** Westcott & Hort, *The New Testament in the Original Greek* (1881) ·",
    "> **WHmarg** a WH marginal reading ·",
    "> **Treg** Tregelles, *The Greek New Testament* (1857–1879) ·",
    "> **NIV** Goodrich & Lukaszewski, *A Reader's Greek New Testament* (2003), the Greek behind the NIV ·",
    "> **RP** Robinson & Pierpont, *Byzantine Textform* (2005) ·",
    "> **NA27 / NA28** Nestle–Aland 27th / 28th edition.  ",
    "> **–** omitted by · **+** added by · **•** separates variation units · **;** separates variants.",
    "> " + EDITIONS["greek"]["credit"],
]


def apparatus_md(name, title, entries):
    lines = [f"# {name}: SBLGNT apparatus", "", md_escape(title), ""] + APPARATUS_KEY + [""]
    for c, v, items in entries:
        lines += [f"## {c}:{v}", ""]
        for i, item in enumerate(items):
            item = item.lstrip("• ").strip()
            if i == 0:  # the first entry repeats the verse number ("1:1 ..." or "2 ...")
                item = re.sub(r"^(\d+:)?\d+ ", "", item)
            lines += [f"- {md_escape(item)}"]
        lines += [""]
    return lines


def main():
    index = []
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        entry = {"number": num, "osis": osis, "name": name, "testament": testament}
        texts = {}
        if testament == "OT":
            src = os.path.join(SOURCES, "hebrew-uxlc", stem + ".txt")
            title, verses = parse_hebrew(src)
            if title != name:
                sys.exit(f"{src}: header names {title!r}, expected {name!r}")
            texts["hebrew"] = (verses, None, src)
            entry["language"] = "Hebrew/Aramaic" if osis in ARAMAIC else "Hebrew"
            entry["tanakh_order"] = TANAKH_ORDER.index(osis) + 1
            if osis in ARAMAIC:
                entry["aramaic_passages"] = ARAMAIC[osis]
        else:
            src = os.path.join(SOURCES, "greek-sblgnt", "text", stem + ".txt")
            title, verses = parse_sblgnt(src, osis)
            clean = [(c, v, " ".join(t.translate(SBLGNT_MARKERS).split())) for c, v, t in verses]
            texts["greek"] = (clean, title, src)
            src_tr = os.path.join(SOURCES, "greek-tr-scrivener", stem + ".txt")
            texts["greek-tr"] = (parse_greek_tr(src_tr), None, src_tr)
            entry["language"] = "Greek"

            app_src = os.path.join(SOURCES, "greek-sblgnt", "apparatus", stem + ".txt")
            app_title, entries = parse_sblgnt_apparatus(app_src, name)
            refs = {(c, v) for c, v, _ in verses}
            stray = [(c, v) for c, v, _ in entries if (c, v) not in refs]
            if stray:
                sys.exit(f"{app_src}: apparatus entries for verses not in the text: {stray}")
            app_out = os.path.join("apparatus", "greek", stem + ".md")
            write_md(os.path.join(ROOT, app_out), apparatus_md(name, app_title, entries))
            entry["apparatus"] = {"path": app_out, "source": os.path.relpath(app_src, ROOT),
                                  "verses_with_entries": len(entries)}

        entry["texts"] = {}
        for edition, (verses, subtitle, src) in texts.items():
            refs = [(c, v) for c, v, _ in verses]
            if len(set(refs)) != len(refs):
                sys.exit(f"{src}: duplicate verse references")
            out = os.path.join("text", edition, stem + ".md")
            write_md(os.path.join(ROOT, out), book_md(name, subtitle, edition, verses))
            entry["texts"][edition] = {
                "edition": EDITIONS[edition]["title"],
                "path": out,
                "source": os.path.relpath(src, ROOT),
                "chapters": len({c for c, _ in refs}),
                "verses": len(verses),
            }
        index.append(entry)

    with open(os.path.join(ROOT, "books.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")

    for edition in EDITIONS:
        books = [b["texts"][edition] for b in index if edition in b["texts"]]
        print(f"{edition}: {len(books)} books, {sum(b['chapters'] for b in books)} chapters, "
              f"{sum(b['verses'] for b in books)} verses")


if __name__ == "__main__":
    main()
