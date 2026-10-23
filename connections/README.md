# Connections: start here

These notes recreate Chris Harrison's [Bible visualizations](https://www.chrisharrison.net/index.php/visualizations/BibleViz) as links you can explore in Obsidian's graph view, using open data and the original-language texts in this repository.

Open the repository folder as an Obsidian vault, then open **Graph view**.

## 1. Cross-references (Harrison's arc diagram)

Graph filter: `path:connections/chapters` (the default). Each of the 1,189 nodes is a chapter, colored by section from Torah (red) to Revelation (violet). Each line is a cross-reference between two chapters. 61,387 cross-references connect 33,542 pairs of chapters. Harrison's graphic draws 63,779.

Open any chapter note to read the text with its cross-references verse by verse. Obsidian's *Backlinks* pane lists the chapters that point back to it, and *Local graph* shows its neighbors.

## 2. People and places (Harrison's social network)

Graph filter: `path:connections/people OR path:connections/places`. Each node is a person (3,004) or place (1,004). Two are linked when they are named in the same verse (15,322 pairs), as in Harrison's graph.

## 3. Where names occur (Harrison's distribution chart)

Each person and place note lists every chapter it appears in, in canonical order, with the number of verses. Its *Local graph* shows the same thing visually.

## How this differs from Harrison's data

| | Harrison (2007) | Here |
|---|---|---|
| Cross-references | 63,779, compiled by Christoph Römhild (not released) | 61,387 from [OpenBible.info](https://www.openbible.info/labs/cross-references/) (2026-10-19), those with at least 8 votes out of 344,799. Mostly from the public-domain *Treasury of Scripture Knowledge* |
| Names | 2,619 English names found in the KJV text | 4,008 people and places tagged in the Hebrew and Greek text by [STEPBible TIPNR](https://github.com/STEPBible/STEPBible-Data). Different people who share a name are kept apart (e.g. the many Zechariahs) |
| Text | King James Version | Hebrew (UXLC) and Greek (SBLGNT). Chapters use Hebrew numbering in the Old Testament |

**Verse numbering.** Both datasets use English verse numbers. Old Testament references are converted to the Hebrew numbering of our text using STEPBible's [TVTMS](https://github.com/STEPBible/STEPBible-Data) mapping. That mapping comes with tests for detecting which numbering a Bible follows. Run against our text, 4,953 of 4,957 Hebrew-tradition rows pass. The rest are for Bibles that number Psalm titles separately, which ours doesn't. This yields 1,970 renumbered verses, e.g. English Malachi 4:5 = Hebrew Malachi 3:23. Unresolved references: 0 cross-references, 0 name references.

**Names.** Each note is titled with TIPNR's main English name, and its other names are Obsidian aliases, so searching for *Jacob* finds the patriarch, whom TIPNR files under *Israel*. TIPNR's *Israel* covers both the patriarch and the nation named after him, so it is the largest hub in the network, as it is in Harrison's.

**Left out:** names of groups and nations (e.g. Amorites), unnamed people (e.g. "the father of …"), and names found only in the Greek Septuagint. The cross-reference list per verse is sorted by votes, highest first.

## Regenerating

```
python3 scripts/connections.py               # rebuild every note in connections/
python3 scripts/connections.py --min-votes 3 # denser network (more, weaker cross-references)
```

Everything in `connections/` is generated. Edit `scripts/connections.py`, not the notes.

## Sources and licenses

- Cross-references: OpenBible.info, CC BY. *Data from OpenBible.info.*
- People, places and versification: STEPBible TIPNR and TVTMS, CC BY 4.0, *data created by www.STEPBible.org based on work at Tyndale House Cambridge*. Source: https://STEPBible.github.io/STEPBible-Data (commit `ed476a8`). **Changes made here:** reformatted as one note per person or place; references converted to Hebrew verse numbering; groups, unnamed people and Septuagint-only names left out; underscores in names replaced with spaces.
- Inspired by Chris Harrison and Christoph Römhild's *Bible Cross-References* (2007). No data or images from that work are used.
