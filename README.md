# The Bible in Its Original Languages

An open, verified library of the whole Bible in Hebrew, Aramaic, and Greek. The aim is a
text as close as possible to what the biblical authors wrote, built only from openly
licensed critical editions and checked verse by verse against them.

| | Books | Chapters | Verses | Language | Text | License |
|---|---|---|---|---|---|---|
| Old Testament | 39 | 929 | 23,213 | Hebrew (some Aramaic) | Leningrad Codex: UXLC 2.6, fully pointed with accents | Unrestricted |
| New Testament | 27 | 260 | 7,939 | Koine Greek | SBL Greek New Testament (SBLGNT) v1.2, critical text with apparatus | CC BY 4.0 |
| *Comparison* | 27 | 260 | 7,957 | Koine Greek | Textus Receptus, Scrivener 1894, unaccented | Public domain |

**Why these texts.**
- **Hebrew:** the Leningrad Codex (1008 CE) is the oldest complete manuscript of the Hebrew
  Bible.
- **Greek:** the SBLGNT is a critical text. Its editor, Michael W. Holmes, built it from the
  full manuscript evidence, including the early papyri, and it comes with an apparatus of
  variant readings.
- **Comparison:** the Textus Receptus is kept as a historical edition. It rests on the
  handful of late manuscripts behind the KJV.

## Layout

```
text/
  hebrew/01-genesis.md …         Old Testament (UXLC)
  greek/40-matthew.md …          New Testament (SBLGNT): the main Greek text
  greek-tr/40-matthew.md …       Textus Receptus (Scrivener 1894), for comparison
  english/…                      Open Plain English Translation: compiled books (first drafts)
translation/                     Translation source: one file per chapter, plus STATUS.md
apparatus/
  greek/40-matthew.md …          SBLGNT apparatus: variant readings, verse by verse
connections/                     Obsidian notes: cross-references, people, places, genealogy, timeline
  README.md                      Start here: how to explore the connections in Obsidian
  genealogy/                     Family groups, generation by generation
  events/ timeline/              Dated events, century notes, synchronisms, the chart
data/                            Curated rulers, eras, world events and synchronisms (see data/README.md)
site/                            The website: the reader and pages built from the data
  index.html                     The reader: the translation, with the Hebrew, Aramaic and Greek beneath
  data/bible/                    The reader's data, one file per book (built by scripts/reader.py)
  genealogy.html                 The Generations: the line from Adam to Jesus and a family explorer
  history.html                   Streams of Time: world history, AD 30 to today, beside the Bible
  maps/kingdoms.html             Map No. 7, The Kingdoms of Judah and Israel (a style study)
  src/ data/ maps/data/          The page sources and the JSON they are built with
books.json                       Index: names, OSIS ids, languages, counts, paths, Tanakh order
sources/                         Raw upstream files, byte for byte (see sources/README.md)
scripts/
  books.py                       Canonical book list, Tanakh order, Aramaic passages
  build.py                       Regenerates text/, apparatus/ and books.json from sources/
  verify.py                      Checks every verse against the published editions
  translation.py                 Checks each translated chapter against its source and compiles text/english/
  connections.py                 Builds connections/ from open cross-reference and name data
  genealogy.py, chronology.py,   Family graph (TIPNR), dates (Theographic), timeline notes,
  timeline.py, chart.py          and the synchronological chart
  webpages.py                    Builds the two pages in site/ (run by connections.py)
  maps.py                        Builds the maps in site/maps/ from elevation and place data
  reader.py                      Builds the reader's data in site/data/bible/
.obsidian/                       Obsidian settings: graph colors and filters
VERIFICATION.md                  What was checked, what was found, what was fixed
TRANSLATION.md                   Translation goals, principles, decisions, format and review process
ROADMAP.md                       Plans: web reader, maps, genealogy viewer, accounts, Chinese
DEPLOY.md, netlify.toml          Publishing site/ to Netlify (or any static host)
```

Files are numbered 01–66 in the common English book order. Hebrew Bibles use a different
order (Torah, Prophets, Writings). That order is stored as `tanakh_order` in `books.json`.

## Reading the texts

Each book is one Markdown file, with a `## Chapter N` heading for each chapter and one
paragraph per verse:

```markdown
## Chapter 1

**1** Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος.
```

The files read well on GitHub, in Obsidian, or in any Markdown viewer. They are also easy
to parse. `parse_book_md()` in `scripts/build.py` reads a file back into
(chapter, verse, text) rows.

Characters that mean something in Markdown are escaped so they display exactly as in the
source. For example, the Hebrew ketiv mark `*` is stored as `\*` and a note like `[t]` as
`\[t\]`. A Markdown viewer shows the original characters. In a plain-text editor you'll
see the backslashes.

Chapter and verse numbers follow each edition's own numbering. Some Hebrew verse numbers
differ from English Bibles: Psalm titles count as verse 1, and Malachi has 3 chapters.

## The Open Plain English Translation

A new translation into plain English, made directly from the Hebrew and Greek above. It
gives a note wherever the source could be read another way, so readers can always see what
the original says. The whole Bible is drafted, Genesis to Revelation: all 1,189 chapters, every verse with its
notes. Every chapter is a first draft awaiting review. Read [TRANSLATION.md](TRANSLATION.md) for the principles and the decisions still
open, and [translation/STATUS.md](translation/STATUS.md) for progress. Every chapter carries
its review status, and drafts are marked as AI-generated until people who read Hebrew or
Greek have reviewed them.

## Exploring connections in Obsidian

Open this folder as an Obsidian vault. `connections/` recreates the three parts of Chris
Harrison's [Bible visualizations](https://www.chrisharrison.net/index.php/visualizations/BibleViz)
as links that Obsidian's graph view can show:

1. **Cross-references:** 1,189 chapter notes, each embedding its Hebrew or Greek text and
   linking to the chapters it cross-references. That gives 61,387 cross-references,
   comparable to Harrison's 63,779.
2. **People and places:** 4,008 notes, each linked to the people and places named in the
   same verse, as in Harrison's social network.
3. **Where names occur:** every person and place note lists the chapters it appears in.

It adds a genealogy and a timeline modeled on Sebastian C. Adams' *Synchronological Chart*
(1871):

4. **Genealogy:** every family relationship in STEPBible's TIPNR, covering
   1,921 parent-child links in 330 family groups. Each person note has a
   family section, a family tree, and the line of descent from father to son. The Family of
   Adam runs 78 generations. The genealogy is cross-checked against Theographic.
5. **Timeline:** 62 century notes from Creation to the 21st century AD, and 450 dated Bible
   events. Ussher's dates appear on 28,020 verses, the chronology Adams used. A table
   compares Ussher with modern dates for events outside sources also date. An SVG chart in
   Adams' style draws the Bible's streams beside the wider world. That covers the eras,
   dynasties and rulers of Egypt, Mesopotamia, the Hittites, Persia, Greece, Rome, India and
   China. From the death and resurrection of Jesus (about AD 30) to today, it adds the
   Byzantine Empire, Europe, Russia, the Islamic world, the Mongols, Japan, Africa and the
   Americas, Jewish history, the Church, and the transmission of the Bible's own text, from
   Papyrus 52 to the editions this project uses. World events and thinkers run throughout,
   all at modern dates.

## Web pages

`site/index.html` is the reader, the home page of the site. Pick a book and chapter, or type a
reference ("jn 3:16", "ps 23"), and swipe or use the arrow keys to turn the page. Every chapter
shows its review status, and all are marked *Draft* until they are reviewed. Tap a verse to see
it in Hebrew, Aramaic or Greek, word by word: each word's transliteration, a gloss, its grammar
and a short dictionary entry. The words and glosses come from STEPBible's tagged texts, matched
to our Hebrew and Greek word by word (99.5% of words match; the rest show without a gloss).
Readers can highlight verses and write notes, which stay on their device, with a backup they
can copy or save. The reader searches the whole Bible on the device, follows the light or dark
setting, offers English Bible verse numbers for the Old Testament, and works offline once
installed. `scripts/reader.py` rebuilds its data from the translation. Because it loads its
data as separate files, it needs a web server: `python3 -m http.server -d site` and then
http://localhost:8000. To publish the site, see [DEPLOY.md](DEPLOY.md): Netlify serves
`site/` as it is, with no build step.

`site/genealogy.html` (*The Generations*) and `site/history.html` (*Streams of Time*) present
the genealogy and the timeline for readers who don't use Obsidian. Each is a single file
that opens in a browser, works on phones, and follows the reader's light or dark setting.
`scripts/connections.py` rebuilds them from `site/src/` and the same data as the notes.

`site/maps/kingdoms.html` is the first of the Bible maps: Map No. 7, *The Kingdoms of Judah
and Israel*, a style study redrawing the Eilers Sunday School wall map of that name from open
data (see the map style in [ROADMAP.md](ROADMAP.md)). It zooms and pans on phones, adds names
as you zoom in without letting them overlap, prints on a Letter page with an index of places,
and downloads as SVG. The land, water and relief come from elevation data; the places from
OpenBible.info's Bible geocoding, with a "?" where the location is uncertain. The tribal
territories are approximate: each piece of land goes to the tribe whose towns in Joshua 13–19
and 21 are nearest. `scripts/maps.py` rebuilds it.

The data is open: OpenBible.info cross-references; STEPBible's tagged names, family links and
verse-numbering mapping; Theographic's dates; and Wikidata identifiers. Start with
[connections/README.md](connections/README.md).

## Rebuilding and verifying

```
python3 scripts/build.py     # regenerate text/, apparatus/, books.json
python3 scripts/verify.py    # compare everything with the published editions (needs network)
python3 scripts/translation.py   # check and compile the translation into text/english/
python3 scripts/connections.py   # regenerate connections/ (needs network)
python3 scripts/maps.py          # rebuild the maps in site/maps/ (needs network)
python3 scripts/reader.py        # rebuild the reader's data in site/data/bible/ (needs network once)
```

These use only the Python standard library, except `maps.py`, which also needs numpy, scipy
and Pillow. `verify.py` checks every verse against the
upstream releases and an independent edition of the SBLGNT (MorphGNT). It also confirms
that every Markdown file parses back to exactly its source. See
[VERIFICATION.md](VERIFICATION.md).

## About the texts

**Hebrew (OT).** UXLC 2.6 (Build 27.7, 18 Oct 2026) from [tanach.us](https://tanach.us), with
full vowel points and cantillation marks.
- It descends from the Westminster Leningrad Codex (WLC) but is a separate text.
- Paragraph markers (פ/ס) are kept at the end of verses.
- Ketiv is marked `*` and qere `**`.
- Editorial notes appear in square brackets, e.g. `[t]` for an uncertain transcription.
- Joshua 21:36–37 are marked `[X]` because they are not in the codex.
- The Aramaic passages are listed in `books.json`.

VERIFICATION.md has the full legend.

**Greek (NT): SBLGNT.** The official SBL/Logos release
([LogosBible/SBLGNT](https://github.com/LogosBible/SBLGNT)), v1.2 (2023). This version
includes John 7:53–8:11 in double brackets ⟦ ⟧.
- **Brackets in the text:** `[ ]` marks doubtful text and ⟦ ⟧ marks text the editors
  regard as a later addition.
- **Apparatus markers:** the raw source marks variant locations with ⸀ ⸂⸃ ⸁ ⸄⸅. The reading
  text in `text/greek/` leaves them out. The variants are listed verse by verse in
  `apparatus/greek/`, comparing Westcott-Hort, Tregelles, Nestle-Aland, the NIV's Greek
  text, and the Robinson-Pierpont Byzantine text.
- **Where verses differ:** the SBLGNT omits verses that the TR includes but the earliest
  manuscripts lack, such as Acts 8:37 and John 5:4. VERIFICATION.md lists them.

**Greek (NT): Textus Receptus.** Scrivener's 1894 edition as digitized by Maurice A. Robinson
([byztxt/greektext-scrivener](https://github.com/byztxt/greektext-scrivener)), converted
here from its ASCII transliteration to Unicode. It has no accents, breathings, capitals or
punctuation, and it regularizes the movable nu. Use it to compare readings, not to quote
the printed 1894 edition.

## Licenses and attribution

- **UXLC:** the text may be copied without restriction. Please cite: *Unicode/XML Leningrad
  Codex: UXLC 2.6 (27.7), Tanach.us Inc., West Redding, CT, USA, Oct 2026.*
- **SBLGNT** (text and apparatus): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Required attribution: *Scripture quotations marked SBLGNT are from the SBL Greek New
  Testament. Copyright © 2010 Society of Biblical Literature and Logos Bible Software.*
  The license text is in `sources/greek-sblgnt/LICENSE`.
- **Scrivener 1894** (Robinson's digitization): public domain.
- **Open Plain English Translation** (`translation/`, `text/english/`):
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See translation/LICENSE.md.
- **`connections/`**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The notes
  combine OpenBible.info (CC BY), STEPBible (CC BY 4.0) and Theographic (CC BY-SA 4.0) data,
  so they inherit Theographic's share-alike terms. See `connections/README.md` for
  attributions.
- **Reader data** (`site/data/bible/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  It combines the translation, the UXLC and SBLGNT texts, and STEPBible's tagged texts and
  brief lexicons (TAHOT, TAGNT, TBESH and TBESG, CC BY 4.0, from
  [STEPBible.org](https://github.com/STEPBible/STEPBible-Data)).
- **Maps** (`site/maps/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Places
  from the [OpenBible.info Bible Geocoding Data](https://github.com/openbibleinfo/Bible-Geocoding-Data)
  (CC BY 4.0). Elevation from the AWS Terrain Tiles (SRTM, GMTED2010 and ETOPO1; see the
  [attribution list](https://github.com/tilezen/joerd/blob/master/docs/attribution.md)).

## Ideas for next steps

The plan for the web reader, maps, genealogy viewer, accounts and a Traditional Chinese
translation is in [ROADMAP.md](ROADMAP.md). Smaller ideas:

- The modern (Thiele) dates for the kings of Israel and Judah beside Ussher's on the chart
- Add the Robinson-Pierpont Byzantine text (public domain) as a further comparison edition
