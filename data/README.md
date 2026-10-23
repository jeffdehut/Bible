# Curated data

Small hand-curated tables used by `scripts/connections.py` for the timeline in
`connections/timeline/`. Unlike the other sources in this repository, these were compiled
here, so every row is meant to be checked and corrected.

## rulers.csv

Rulers and officials of the nations around Israel, for the world-history streams of the
Synchronological Chart.

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
