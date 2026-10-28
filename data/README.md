# Data

Small hand-curated tables used by `scripts/connections.py` for the timeline in
`connections/timeline/` and the world-history notes in `connections/world/`. Unlike the other
sources in this repository, these were compiled here, so every row is meant to be checked and
corrected.

The folder also holds data built for the website. The scripts regenerate it, so don't edit it
by hand:

- `bible/`: the reader's books, word data, lexicon and search index (`scripts/reader.py`)
- `genealogy.json`, `history.json`: the data inlined in `genealogy.html` and `history.html`
  (`scripts/connections.py`)

## rulers.csv

Rulers and officials, both those the Bible names and other well-known rulers (Hammurabi,
Ramesses II, Ashoka, Qin Shi Huang), for the world-history streams of the Synchronological
Chart.

| Column | Meaning |
|---|---|
| `stream` | The nation or office, drawn as one stream on the chart |
| `name` | Conventional modern name |
| `biblical_name` | The name used in the Bible, if any |
| `tipnr` | The STEPBible TIPNR id of that person, linking to their note in `connections/people/` |
| `wikidata` | Wikidata item, confirmed by matching the item's English label (left blank where no item could be confirmed) |
| `start`, `end` | Reign or term of office in modern scholarship, `BC`/`AD` |
| `approximate` | `yes` where scholars give a range or the dates are uncertain |
| `note` | Identifications that are probable rather than certain, and other caveats |

Reign dates are the conventional ones found in standard references (e.g. the Cambridge
Ancient History and the Babylonian and Assyrian king lists). They are **modern** dates, not
Ussher's.

## synchronisms.csv

Events the Bible narrates that outside evidence also dates. `connections.py` looks up the
Ussher date of the anchor verse (`ref`, OSIS, English verse numbering) and sets it beside
the modern date, in `connections/timeline/Synchronisms.md` and on the chart.

| Column | Meaning |
|---|---|
| `event` | Short description |
| `ref` | Anchor verse, e.g. `2Kgs.18.13` |
| `modern_date` | Date in modern scholarship |
| `approximate` | `yes` where the date is uncertain by a year or more |
| `evidence` | The outside source that fixes the date |

If an anchor verse has no Ussher date in the source data, the nearest dated verse in the
same chapter is used, and the note says so.

## periods.csv

Eras and dynasties of the wider world, drawn as the pale bands of each stream.

| Column | Meaning |
|---|---|
| `stream` | Egypt, Sumer and Akkad, Babylon, Assyria, Anatolia, Persia, Greece, Seleucid, Rome, Carthage, India, China; from about AD 30 also Byzantine Empire, Europe, Russia, Islamic world, Mongols, Japan, Africa, Americas, Jewish history, Church, Bible transmission and World |
| `level` | `era` (e.g. Old Kingdom) or `dynasty` (e.g. Eighteenth Dynasty) |
| `name`, `start`, `end`, `approximate`, `wikidata`, `note` | As in `rulers.csv` |

Dates follow common modern references. Egypt follows the dates in *The Oxford History of
Ancient Egypt* (ed. Shaw), Mesopotamia the "middle chronology", and China the conventional
dynastic dates (the Xia dynasty's dates are traditional and its historicity is debated).
Third-millennium dates are uncertain by decades or more.

## world_events.csv

| Column | Meaning |
|---|---|
| `stream` | `World events`, `Thinkers and writers`, or the stream an event or life belongs to (for example `Church` or `Bible transmission`) |
| `kind` | `event` (a single year in `start`) or `figure` (a lifespan, `start`–`end`) |
| `name`, `start`, `end`, `approximate`, `wikidata`, `note` | As above |

## From AD 30 to the present

The rows from the death and resurrection of Jesus (about AD 30) to today were added in
October 2026. They follow the same conventions, with two additions:

- `end` may be `present` for a state, era or institution that continues. The scripts read it
  as the current year.
- The **Bible transmission** stream lists the manuscripts and editions behind this project's
  own texts, from Papyrus 52 to the Leningrad Codex (the source of the Hebrew), Scrivener's
  Textus Receptus and the SBL Greek New Testament. Manuscript dates are the usual
  palaeographic estimates and are marked approximate.

Dates are the conventional ones of standard references (for example the Oxford and Cambridge
histories). Where scholars give a range, the row uses its usual midpoint or start, says
`approximate`, and gives the range in the note.

## Wikidata identifiers

Every identifier was found by exact English label in Wikidata and checked against its
description. Identifiers are left blank where no item could be confirmed, rather than guessed.
The rows added for AD 30 to the present have no identifiers yet: Wikidata's API refused
requests from the build environment when they were compiled, so they await the same check.
