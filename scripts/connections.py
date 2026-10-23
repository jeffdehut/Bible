"""Build the Obsidian connection notes in connections/.

    python3 scripts/connections.py [--min-votes N]

Recreates Chris Harrison's "Bible Cross-References" and "Biblical Social Network"
(https://www.chrisharrison.net/index.php/visualizations/BibleViz) as links that Obsidian's
graph view can show. It uses open data in place of the data behind those graphics, which
was never released:

  - Cross-references: OpenBible.info (CC BY), mostly from the public-domain Treasury of
    Scripture Knowledge, filtered by community votes.
  - People and places: STEPBible TIPNR (CC BY 4.0), which ties every person and place to
    its Hebrew/Greek name and every verse it occurs in.
  - Versification: STEPBible TVTMS (CC BY 4.0), used to move English-numbered references
    onto the Hebrew numbering of our Old Testament.

Downloads go to .cache/ (git ignores it). Output, all regenerated on each run:
  connections/books/*.md       one note per book
  connections/chapters/*/*.md  one note per chapter: the text (embedded), cross-references,
                               people and places
  connections/people/*.md      one note per person: names, chapters, who they appear with
  connections/places/*.md      the same for places
"""

import argparse
import collections
import io
import json
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request
import zipfile

from books import BOOKS, file_stem
from build import parse_book_md

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
OUT = os.path.join(ROOT, "connections")

OPENBIBLE_ZIP = "https://a.openbible.info/data/cross-references.zip"
STEPBIBLE_COMMIT = "ed476a8ee6e3f7b3a46fc48af6c7dabc02387b1d"  # 17 Oct 2026
STEPBIBLE_FILES = {
    "tipnr": "Proper Nouns/TIPNR - Translators Individualised Proper Names with all References - STEPBible.org CC BY.txt",
    "tvtms": "Versification/TVTMS - Translators Versification Traditions with Methodology for Standardisation "
             "for Eng+Heb+Lat+Grk+Others - STEPBible.org CC BY.txt",
}

# Harrison's graphic draws 63,779 cross-references. Keeping OpenBible references with at
# least this many votes gives a comparable number (61,387 in the 2026-10-19 data).
DEFAULT_MIN_VOTES = 8

# STEPBible book abbreviations -> OSIS ids used in this repository.
STEP_BOOKS = dict(zip(
    "Gen Exo Lev Num Deu Jos Jdg Rut 1Sa 2Sa 1Ki 2Ki 1Ch 2Ch Ezr Neh Est Job Psa Pro Ecc Sng Isa Jer "
    "Lam Ezk Dan Hos Jol Amo Oba Jon Mic Nam Hab Zep Hag Zec Mal Mat Mrk Luk Jhn Act Rom 1Co 2Co Gal "
    "Eph Php Col 1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jn 2Jn 3Jn Jud Rev".split(),
    [osis for _, osis, _, _ in BOOKS],
))
STEP_BOOKS.update({"Ps": "Ps", "1Sam": "1Sam"})  # spellings that also occur in TVTMS
STEP_BOOKS.update({k.upper(): v for k, v in list(STEP_BOOKS.items())})  # TVTMS has e.g. "PSA.133:3"

# English (KJV/ESV) -> SBLGNT verse numbers where they differ (TVTMS notes these for the NRSV
# standard, which the SBLGNT follows). Verses the SBLGNT omits, such as Acts 8:37 or
# Rom 16:25-27, keep their numbers: they still link to the right chapter.
NT_RENUMBER = {("2Cor", 13, 13): ("2Cor", 13, 12), ("2Cor", 13, 14): ("2Cor", 13, 13)}

SECTIONS = [
    ("Torah", "Gen", "Deut"), ("History", "Josh", "Esth"), ("Wisdom", "Job", "Song"),
    ("Prophets", "Isa", "Mal"), ("Gospels", "Matt", "John"), ("Acts", "Acts", "Acts"),
    ("Pauline Epistles", "Rom", "Phlm"), ("General Epistles", "Heb", "Jude"),
    ("Revelation", "Rev", "Rev"),
]

BOOK = {osis: (num, name, testament) for num, osis, name, testament in BOOKS}
ORDER = [osis for _, osis, _, _ in BOOKS]


def section_of(osis):
    i = ORDER.index(osis)
    for name, first, last in SECTIONS:
        if ORDER.index(first) <= i <= ORDER.index(last):
            return name


def slug(s):
    return s.lower().replace(" ", "-")


# ---------------------------------------------------------------- downloads

def fetch(url, dest):
    if not os.path.exists(dest):
        print(f"Downloading {url}")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req) as r, open(dest, "wb") as f:
            f.write(r.read())
    return dest


def fetch_openbible():
    path = os.path.join(CACHE, "openbible", "cross_references.txt")
    if not os.path.exists(path):
        z = fetch(OPENBIBLE_ZIP, os.path.join(CACHE, "openbible", "cross-references.zip"))
        zipfile.ZipFile(z).extractall(os.path.dirname(path))
    return path


def fetch_stepbible(key):
    rel = STEPBIBLE_FILES[key]
    url = (f"https://raw.githubusercontent.com/STEPBible/STEPBible-Data/{STEPBIBLE_COMMIT}/"
           + urllib.parse.quote(rel))
    return fetch(url, os.path.join(CACHE, "stepbible", STEPBIBLE_COMMIT[:7], os.path.basename(rel)))


# ---------------------------------------------------------------- our texts

def load_texts():
    """{osis: {(chapter, verse): text}} from text/hebrew (OT) and text/greek (NT)."""
    texts = {}
    for num, osis, name, testament in BOOKS:
        folder = "hebrew" if testament == "OT" else "greek"
        path = os.path.join(ROOT, "text", folder, file_stem(num, name) + ".md")
        texts[osis] = {(c, v): t for c, v, t in parse_book_md(path)}
    return texts


# ---------------------------------------------------------------- versification

REF_RE = re.compile(r"([1-3]?[A-Za-z]+)\.(\d+):(\d+)(?:[.!]?([0-9a-z]+))?")


class Versification:
    """English (KJV/NRSV) -> Hebrew verse numbers for the Old Testament, from TVTMS.

    TVTMS lists, for each Bible tradition, how its verse numbers map to a standard (English)
    numbering, guarded by tests such as "Gen.32:33=Last". We run those tests against our
    own Hebrew text and keep only the rows whose tests pass, so the mapping is proven
    against this exact text rather than assumed.
    """

    def __init__(self, path, texts):
        self.texts = texts
        self.to_hebrew = {}
        self.rows_checked = self.rows_passed = 0
        self.failed = []
        lines = open(path, encoding="utf-8-sig").read().split("\n")
        start = next(i for i, l in enumerate(lines) if l.startswith("#DataStart(Expanded)"))
        end = next(i for i, l in enumerate(lines) if l.startswith("#DataEnd(Expanded)"))
        for line in lines[start:end]:
            row = line.split("\t")
            if len(row) < 9 or "Hebrew" not in row[0].split("+"):
                continue
            src, std = REF_RE.match(row[1]), REF_RE.match(row[2])
            if not src or not std or STEP_BOOKS.get(src[1]) not in texts:
                continue
            self.rows_checked += 1
            if not all(self.test(t.strip()) for t in row[8].split("&") if t.strip()):
                self.failed.append((row[1], row[8]))
                continue
            self.rows_passed += 1
            heb = (STEP_BOOKS[src[1]], int(src[2]), int(src[3]))
            eng = (STEP_BOOKS[std[1]], int(std[2]), int(std[3]))
            if heb != eng and int(std[3]) > 0:  # verse 0 = a Psalm title, which English doesn't number
                self.to_hebrew.setdefault(eng, heb)

    def verse(self, ref):
        """Text of a TVTMS reference in our Hebrew Bible, or None if it doesn't exist."""
        m = REF_RE.fullmatch(ref)
        if not m or STEP_BOOKS.get(m[1]) not in self.texts:
            return None
        sub = m[4]
        if sub and sub not in ("0", "a"):  # our text has no subverses beyond the verse itself
            return None
        return self.texts[STEP_BOOKS[m[1]]].get((int(m[2]), int(m[3])))

    def words(self, expr):
        total = 0
        for term in expr.split("+"):
            ref, _, mult = term.partition("*")
            text = self.verse(ref.strip())
            total += len(re.split(r"[\s־]+", text.strip())) * int(mult or 1) if text else 0
        return total

    def test(self, t):
        m = re.fullmatch(r"(.+?)(TextBeforeV1)?=(Last|Exist|NotExist)", t)
        if m:
            ref, before, cond = m.groups()
            if before:  # UXLC numbers Psalm titles as verse 1, so nothing comes before v.1
                return cond == "NotExist"
            exists = self.verse(ref) is not None
            if cond == "Exist":
                return exists
            if cond == "NotExist":
                return not exists
            r = REF_RE.fullmatch(ref)
            book, c, v = STEP_BOOKS.get(r[1]), int(r[2]), int(r[3])
            return exists and (c, v + 1) not in self.texts[book]
        m = re.fullmatch(r"(.+?)([<>])(.+)", t)
        if m:
            a, op, b = self.words(m[1]), m[2], self.words(m[3])
            return a > b if op == ">" else a < b
        raise ValueError(f"unknown TVTMS test: {t!r}")

    def hebrew(self, osis, c, v):
        """Map an English-numbered verse to our numbering (identity outside the OT)."""
        ref = (osis, c, v)
        return self.to_hebrew.get(ref) or NT_RENUMBER.get(ref, ref)


# ---------------------------------------------------------------- datasets

def load_cross_references(path, min_votes, vers, texts):
    refs, stats = [], collections.Counter()
    with open(path, encoding="utf-8") as f:
        header = next(f)
        stats_date = re.search(r"\d{4}-\d{2}-\d{2}", header)[0]
        for line in f:
            src, dst, votes = line.rstrip("\n").split("\t")
            stats["total"] += 1
            if int(votes) < min_votes:
                continue
            a = parse_osis_ref(src.split("-")[0], vers)
            b_start = parse_osis_ref(dst.split("-")[0], vers)
            b_end = parse_osis_ref(dst.split("-")[-1], vers) if "-" in dst else b_start
            if not a or not b_start or (a[0], a[1]) not in chapters_of(texts) or \
                    (b_start[0], b_start[1]) not in chapters_of(texts):
                stats["unresolved"] += 1
                continue
            stats["kept"] += 1
            refs.append((a, b_start, b_end, int(votes)))
    return refs, stats, stats_date


def parse_osis_ref(ref, vers):
    book, c, v = ref.split(".")
    if book not in BOOK:
        return None
    return vers.hebrew(book, int(c), int(v))


_CHAPTERS = None


def chapters_of(texts):
    global _CHAPTERS
    if _CHAPTERS is None:
        _CHAPTERS = {(b, c) for b, verses in texts.items() for c, _ in verses}
    return _CHAPTERS


NAME_SIGNIFICANCE = {
    "Named", "Name combined", "Spelled", "Spelled combined", "Aramaic", "Aramaic combined",
    "Greek", "(same form with Variant)", "(same form with alt. meaning)",
    "(same ref[s] with alt Tags)", "(same ref[s] with Variant)",
}
TIPNR_REF = re.compile(r"([1-3]?[A-Z][a-z]{1,2})\.(\d+)\.(\d+)[a-z]?")


def load_tipnr(path, vers, texts):
    """People and places: [{id, kind, name, brief, forms, location, verses}]."""
    entities, cur, kind = [], None, None
    unresolved = 0
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("$=========="):
            kind = line.strip("$= \t").split()[0] if line.strip("$= \t") else None
            cur = None
            continue
        if kind not in ("PERSON(s)", "PLACE", "PLACE+PERSON"):
            continue
        fields = line.split("\t")
        if cur is None and "@" in fields[0] and "=" in fields[0] and not line.startswith(("–", "@")):
            uid, _, ustrong = fields[0].partition("=")
            cur = {"id": uid.strip(), "kind": "person" if kind == "PERSON(s)" else "place",
                   "name": uid.split("@")[0].strip().replace("_", " "), "ustrong": ustrong.strip(),
                   "brief": "", "forms": [], "aliases": [], "location": None, "verses": set()}
            if cur["kind"] == "place":
                m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", line)
                if m:
                    cur["location"] = (float(m[1]), float(m[2]))
            entities.append(cur)
            continue
        if cur is None:
            continue
        if line.startswith("@Brief="):
            cur["brief"] = line[len("@Brief="):].strip()
        elif line.startswith("– ") and len(fields) > 4:
            significance = fields[0][2:].strip()
            if significance not in NAME_SIGNIFICANCE:
                continue
            alias = fields[1].split("|")[0].strip().replace("_", " ") if "|" in fields[1] else None
            if alias and significance != "(same form with alt. meaning)" \
                    and alias != cur["name"] and alias not in cur["aliases"]:
                cur["aliases"].append(alias)  # e.g. "Jacob" for the patriarch filed as Israel
            strong, _, form = fields[2].partition("=")
            if form and (form.strip(), strong.split("«")[-1]) not in cur["forms"]:
                cur["forms"].append((form.strip(), strong.split("«")[-1]))
            for m in TIPNR_REF.finditer(fields[4]):
                osis = STEP_BOOKS.get(m[1])
                if not osis:
                    continue
                ref = vers.hebrew(osis, int(m[2]), int(m[3]))
                if (ref[0], ref[1]) not in chapters_of(texts):
                    unresolved += 1
                    continue
                cur["verses"].add(ref)
    return [e for e in entities if e["verses"]], unresolved


# ---------------------------------------------------------------- notes

def ref_label(osis, c, v=None, v_end=None):
    name = BOOK[osis][1]
    if v is None:
        return f"{name} {c}"
    label = f"{name} {c}:{v}"
    if v_end and v_end != (c, v):
        label += f"–{v_end[1]}" if v_end[0] == c else f"–{v_end[0]}:{v_end[1]}"
    return label


def chapter_path(osis, c):
    num, name, _ = BOOK[osis]
    return f"connections/chapters/{num:02d}-{slug(name)}/{name} {c}"


def link(path, label=None):
    """A wikilink by full path (names like "Ruth" are both a book and a person), shown
    with a short label instead of the path."""
    return f"[[{path}|{label or path.rsplit('/', 1)[-1]}]]"


def safe_filename(name):
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "-", name).strip()


def frontmatter(fields):
    out = ["---"]
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            out.append(f"{k}: [{', '.join(json.dumps(x, ensure_ascii=False) for x in v)}]")
        else:
            out.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return out + ["---", ""]


def write(path, lines):
    full = os.path.join(ROOT, path + ".md")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def write_readme(st):
    lines = [
        "# Connections: start here", "",
        "These notes recreate Chris Harrison's [Bible visualizations]"
        "(https://www.chrisharrison.net/index.php/visualizations/BibleViz) as links you can explore "
        "in Obsidian's graph view, using open data and the original-language texts in this repository.",
        "", "Open the repository folder as an Obsidian vault, then open **Graph view**.", "",
        "## 1. Cross-references (Harrison's arc diagram)", "",
        f"Graph filter: `path:connections/chapters` (the default). Each of the {st['chapters']:,} nodes is "
        "a chapter, colored by section from Torah (red) to Revelation (violet). Each line is a "
        f"cross-reference between two chapters. {st['cross_references_kept']:,} cross-references "
        f"connect {st['chapter_pairs']:,} pairs of chapters. Harrison's graphic draws 63,779.", "",
        "Open any chapter note to read the text with its cross-references verse by verse. Obsidian's "
        "*Backlinks* pane lists the chapters that point back to it, and *Local graph* shows its neighbors.", "",
        "## 2. People and places (Harrison's social network)", "",
        "Graph filter: `path:connections/people OR path:connections/places`. Each node is a person "
        f"({st['people']:,}) or place ({st['places']:,}). Two are linked when they are named in the same "
        f"verse ({st['same_verse_pairs']:,} pairs), as in Harrison's graph.", "",
        "## 3. Where names occur (Harrison's distribution chart)", "",
        "Each person and place note lists every chapter it appears in, in canonical order, with the "
        "number of verses. Its *Local graph* shows the same thing visually.", "",
        "## How this differs from Harrison's data", "",
        "| | Harrison (2007) | Here |", "|---|---|---|",
        "| Cross-references | 63,779, compiled by Christoph Römhild (not released) | "
        f"{st['cross_references_kept']:,} from [OpenBible.info](https://www.openbible.info/labs/cross-references/) "
        f"({st['openbible_date']}), those with at least {st['min_votes']} votes out of "
        f"{st['cross_references_total']:,}. Mostly from the public-domain *Treasury of Scripture Knowledge* |",
        "| Names | 2,619 English names found in the KJV text | "
        f"{st['people'] + st['places']:,} people and places tagged in the Hebrew and Greek text by "
        "[STEPBible TIPNR](https://github.com/STEPBible/STEPBible-Data). Different people who share a "
        "name are kept apart (e.g. the many Zechariahs) |",
        "| Text | King James Version | Hebrew (UXLC) and Greek (SBLGNT). Chapters use Hebrew numbering "
        "in the Old Testament |", "",
        "**Verse numbering.** Both datasets use English verse numbers. Old Testament references are "
        "converted to the Hebrew numbering of our text using STEPBible's "
        "[TVTMS](https://github.com/STEPBible/STEPBible-Data) mapping. That mapping comes with "
        "tests for detecting which numbering a Bible follows. Run against our text, "
        f"{st['tvtms_rows_passed']:,} of {st['tvtms_rows_checked']:,} Hebrew-tradition rows pass. The rest "
        "are for Bibles that number Psalm titles separately, which ours doesn't. This yields "
        f"{st['renumberings']:,} renumbered verses, e.g. English Malachi 4:5 = Hebrew Malachi 3:23. "
        f"Unresolved references: {st['cross_references_unresolved']} cross-references, "
        f"{st['tipnr_references_unresolved']} name references.", "",
        "**Names.** Each note is titled with TIPNR's main English name, and its other names are "
        "Obsidian aliases, so searching for *Jacob* finds the patriarch, whom TIPNR files under "
        "*Israel*. TIPNR's *Israel* covers both the patriarch and the nation named after him, so it "
        "is the largest hub in the network, as it is in Harrison's.", "",
        "**Left out:** names of groups and nations (e.g. Amorites), unnamed people (e.g. \"the father "
        "of …\"), and names found only in the Greek Septuagint. The cross-reference list per verse "
        "is sorted by votes, highest first.", "",
        "## Regenerating", "",
        "```", "python3 scripts/connections.py               # rebuild every note in connections/",
        "python3 scripts/connections.py --min-votes 3 # denser network (more, weaker cross-references)", "```",
        "", "Everything in `connections/` is generated. Edit `scripts/connections.py`, not the notes.", "",
        "## Sources and licenses", "",
        "- Cross-references: OpenBible.info, CC BY. *Data from OpenBible.info.*",
        "- People, places and versification: STEPBible TIPNR and TVTMS, CC BY 4.0, *data created by "
        "www.STEPBible.org based on work at Tyndale House Cambridge*. Source: "
        "https://STEPBible.github.io/STEPBible-Data (commit "
        f"`{st['stepbible_commit'][:7]}`). **Changes made here:** reformatted as one note per person or "
        "place; references converted to Hebrew verse numbering; groups, unnamed people and "
        "Septuagint-only names left out; underscores in names replaced with spaces.",
        "- Inspired by Chris Harrison and Christoph Römhild's *Bible Cross-References* (2007). No data "
        "or images from that work are used.",
    ]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def check_links():
    """Every [[link]] and ![[embed]] in connections/ must point to an existing note, and
    every #heading to an existing heading. Returns the number of broken links."""
    headings, broken = {}, 0
    for dirpath, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            with open(os.path.join(dirpath, fn), encoding="utf-8") as f:
                for target in re.findall(r"\[\[([^\]|]+)", f.read()):
                    path, _, heading = target.partition("#")
                    full = os.path.join(ROOT, path + ".md")
                    if full not in headings:
                        headings[full] = None
                        if os.path.exists(full):
                            with open(full, encoding="utf-8") as t:
                                headings[full] = set(re.findall(r"^#+ (.+)$", t.read(), re.M))
                    if headings[full] is None or (heading and heading not in headings[full]):
                        broken += 1
                        if broken <= 5:
                            print(f"  broken link in {fn}: [[{target}]]")
    return broken


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--min-votes", type=int, default=DEFAULT_MIN_VOTES,
                    help=f"minimum OpenBible votes for a cross-reference (default {DEFAULT_MIN_VOTES})")
    args = ap.parse_args()

    texts = load_texts()
    vers = Versification(fetch_stepbible("tvtms"), texts)
    xrefs, xstats, xdate = load_cross_references(fetch_openbible(), args.min_votes, vers, texts)
    entities, ent_unresolved = load_tipnr(fetch_stepbible("tipnr"), vers, texts)

    # Unique note names: the plain name, or "Name (Book c.v)" when several people (or several
    # places) share it.
    by_name = collections.Counter((e["kind"], e["name"]) for e in entities)
    for e in entities:
        first = min(e["verses"], key=lambda r: (ORDER.index(r[0]), r[1], r[2]))
        # Colons can't appear in file names, so "Genesis 11:29" becomes "Genesis 11.29".
        title = e["name"] if by_name[(e["kind"], e["name"])] == 1 else f"{e['name']} ({ref_label(*first).replace(':', '.')})"
        folder = "people" if e["kind"] == "person" else "places"
        e["path"] = f"connections/{folder}/{safe_filename(title)}"
        e["first"] = first

    # Index everything by chapter and by verse.
    out_refs = collections.defaultdict(list)
    in_count = collections.Counter()
    for a, b, b_end, votes in xrefs:
        out_refs[(a[0], a[1])].append((a, b, b_end, votes))
        in_count[(b[0], b[1])] += 1
    in_chapter = collections.defaultdict(collections.Counter)  # chapter -> entity index -> verses
    in_verse = collections.defaultdict(set)
    for i, e in enumerate(entities):
        for ref in e["verses"]:
            in_chapter[(ref[0], ref[1])][i] += 1
            in_verse[ref].add(i)
    together = collections.defaultdict(collections.Counter)  # Harrison: same-verse co-occurrence
    for ids in in_verse.values():
        for i in ids:
            for j in ids:
                if i != j:
                    together[i][j] += 1

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    # Chapter notes.
    meta = {b["osis"]: b for b in json.load(open(os.path.join(ROOT, "books.json"), encoding="utf-8"))}
    all_chapters = sorted(chapters_of(texts), key=lambda r: (ORDER.index(r[0]), r[1]))
    for idx, (osis, c) in enumerate(all_chapters):
        num, name, testament = BOOK[osis]
        verses = sorted(v for (cc, v) in texts[osis] if cc == c)
        edition = "hebrew" if testament == "OT" else "greek"
        text_path = meta[osis]["texts"][edition]["path"][:-3]
        lines = frontmatter({
            "book": name, "chapter": c, "testament": testament, "section": section_of(osis),
            "language": meta[osis]["language"], "verses": len(verses),
            "cross_references_out": len(out_refs[(osis, c)]),
            "cross_references_in": in_count[(osis, c)],
            "tags": ["chapter", testament.lower(), slug(section_of(osis))],
        })
        nav = []
        if idx > 0:
            nav.append("← " + link(chapter_path(*all_chapters[idx - 1]), ref_label(*all_chapters[idx - 1])))
        nav.append(link(f"connections/books/{name}", name))
        if idx + 1 < len(all_chapters):
            nav.append(link(chapter_path(*all_chapters[idx + 1]), ref_label(*all_chapters[idx + 1])) + " →")
        lines += [f"# {name} {c}", "", " · ".join(nav), "", "## Text", "",
                  f"![[{text_path}#Chapter {c}]]", ""]
        if testament == "NT":
            stem = text_path.rsplit("/", 1)[-1]
            lines += [f"Compare: [[text/greek-tr/{stem}#Chapter {c}|Textus Receptus]] · "
                      f"[[apparatus/greek/{stem}|SBLGNT apparatus]]", ""]
        lines += ["## Cross-references", ""]
        by_verse = collections.defaultdict(list)
        for a, b, b_end, votes in sorted(out_refs[(osis, c)], key=lambda r: (r[0][2], -r[3])):
            by_verse[a[2]].append(link(chapter_path(b[0], b[1]), ref_label(b[0], b[1], b[2], (b_end[1], b_end[2]) if b_end[0] == b[0] else None)))
        if by_verse:
            for v in sorted(by_verse):
                lines.append(f"- **{c}:{v}** → " + " · ".join(by_verse[v]))
        else:
            lines.append(f"*No cross-references with at least {args.min_votes} votes.*")
        lines += ["", "## People and places", ""]
        ents = in_chapter[(osis, c)]
        for kind, label in (("person", "People"), ("place", "Places")):
            items = sorted((i for i in ents if entities[i]["kind"] == kind),
                           key=lambda i: (-ents[i], entities[i]["path"]))
            if items:
                lines.append(f"**{label}:** " + ", ".join(
                    link(entities[i]["path"], entities[i]["path"].rsplit("/", 1)[-1]) for i in items))
                lines.append("")
        if not ents:
            lines += ["*None named.*", ""]
        write(chapter_path(osis, c), lines)

    # Book notes.
    for num, osis, name, testament in BOOKS:
        chs = [c for b, c in all_chapters if b == osis]
        lines = frontmatter({
            "book": name, "osis": osis, "testament": testament, "section": section_of(osis),
            "language": meta[osis]["language"], "chapters": len(chs),
            "tags": ["book", testament.lower(), slug(section_of(osis))],
        })
        lines += [f"# {name}", "", f"**{section_of(osis)}** · {meta[osis]['language']} · "
                  f"{len(chs)} chapters", "", "## Chapters", "",
                  " · ".join(link(chapter_path(osis, c), str(c)) for c in chs), ""]
        write(f"connections/books/{name}", lines)

    # People and place notes.
    for i, e in enumerate(entities):
        chs = collections.Counter((r[0], r[1]) for r in e["verses"])
        ordered = sorted(chs, key=lambda r: (ORDER.index(r[0]), r[1]))
        lines = frontmatter({
            "name": e["name"], "aliases": e["aliases"] or None, "type": e["kind"],
            "tipnr": e["id"], "strong": e["ustrong"],
            "original": [f for f, _ in e["forms"]],
            "location": list(e["location"]) if e["location"] else None,
            "verses": len(e["verses"]), "chapters": len(chs),
            "first": ref_label(*e["first"]),
            "tags": ["person" if e["kind"] == "person" else "place"],
        })
        lines += [f"# {e['path'].rsplit('/', 1)[-1]}", ""]
        if e["brief"]:
            lines += [e["brief"], ""]
        if e["aliases"]:
            lines += ["**Also called:** " + ", ".join(e["aliases"]), ""]
        if e["forms"]:
            lines += ["**Original-language names:** " + " · ".join(f"{f} ({s})" for f, s in e["forms"]), ""]
        lines += ["## Appears in", ""]
        lines += [" · ".join(link(chapter_path(*r), ref_label(*r) + (f" ({chs[r]})" if chs[r] > 1 else ""))
                             for r in ordered), ""]
        if together[i]:
            lines += ["## Appears in the same verse as", ""]
            items = sorted(together[i].items(), key=lambda kv: (-kv[1], entities[kv[0]]["path"]))
            lines += [" · ".join(link(entities[j]["path"], entities[j]["path"].rsplit("/", 1)[-1] + (f" ({n})" if n > 1 else ""))
                                 for j, n in items), ""]
        write(e["path"], lines)

    people = sum(e["kind"] == "person" for e in entities)
    pairs = sum(len(t) for t in together.values()) // 2
    chapter_pairs = {tuple(sorted([(a[0], a[1]), (b[0], b[1])])) for a, b, _, _ in xrefs if (a[0], a[1]) != (b[0], b[1])}
    print(f"Versification: {vers.rows_passed}/{vers.rows_checked} TVTMS Hebrew rows pass against our text; "
          f"{len(vers.to_hebrew)} English->Hebrew renumberings")
    print(f"Cross-references ({xdate}): {xstats['kept']} of {xstats['total']} kept (votes >= {args.min_votes}), "
          f"{xstats['unresolved']} unresolved; {len(chapter_pairs)} distinct chapter pairs")
    print(f"People: {people}, places: {len(entities) - people}; {pairs} same-verse pairs; "
          f"{ent_unresolved} references unresolved")
    print(f"Wrote {len(all_chapters)} chapter notes, {len(BOOKS)} book notes, {len(entities)} people/place notes")
    broken = check_links()
    print(f"Links: {broken} broken")
    stats = {
        "openbible_date": xdate, "min_votes": args.min_votes,
        "cross_references_total": xstats["total"], "cross_references_kept": xstats["kept"],
        "cross_references_unresolved": xstats["unresolved"], "chapter_pairs": len(chapter_pairs),
        "stepbible_commit": STEPBIBLE_COMMIT,
        "tvtms_rows_checked": vers.rows_checked, "tvtms_rows_passed": vers.rows_passed,
        "renumberings": len(vers.to_hebrew),
        "people": people, "places": len(entities) - people, "same_verse_pairs": pairs,
        "tipnr_references_unresolved": ent_unresolved,
        "chapters": len(all_chapters),
        "broken_links": broken,
    }
    write_readme(stats)
    with open(os.path.join(OUT, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")
    if broken:
        sys.exit(1)


if __name__ == "__main__":
    main()
