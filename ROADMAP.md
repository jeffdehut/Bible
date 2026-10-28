# Roadmap

The next iteration turns this repository into a web app for reading and studying the Bible:
a reader for the Open Plain English Translation with the Hebrew, Aramaic and Greek beneath it,
Bible maps, and a genealogy viewer, all built for phones first. After that comes a Traditional
Chinese translation.

## Decisions so far

| Question | Decision |
|---|---|
| Who it's for | Phone users first; tablets and desktops follow from the same design. |
| Hosting | Static hosting, so there are no servers to run and no fees. Cloudflare Pages is recommended; not yet chosen. |
| Domain | Not yet chosen. Candidates: `bibledata.org`, `bibledata.info`, `bibledata.app` (unregistered as of 28 Oct 2026). |
| Annotations | Saved on the device first. Accounts come later, and signing in merges the device's highlights and notes into the account. |
| Versions | Only the Open Plain English Translation, beside the Hebrew, Aramaic and Greek it is translated from. |
| Draft status | Every chapter is clearly labeled as a draft until it is reviewed (see *Draft labels* below). |
| Map style | After the Eilers Sunday School wall maps of the Bible lands, but more legible (see *Map style* under *Maps*). |
| Next language | Traditional Chinese, once the English is finished. |

## Principles

- **Open.** Every text, map and dataset is openly licensed and credited, and builds from this
  repository with one command.
- **Honest.** Uncertain things look uncertain: draft chapters, disputed sites, alternative routes.
- **Fast on a phone.** Each screen loads only what it shows. The app works offline after the
  first visit and can be installed like an app.
- **One product.** The reader, maps and genealogy share one design, one search and one set of links.
  Tapping a place in the reader opens the map, and tapping a map route opens the reader.

## Foundation

1. **Data build.** A script turns the repository into small files the app loads on demand:
   one per chapter (English, notes, Hebrew or Greek, word data), one per map, and one for the
   genealogy.
2. **App shell.** One static web app that installs on a phone and works offline. It grows out of
   the design of `site/genealogy.html` and `site/history.html`.
3. **Hosting.** Every push to the main branch publishes the site.

## 1. Reader

- **Choosing a passage.** A book and chapter picker with Old and New Testament tabs, recent
  chapters, and typed references ("jn 3 16", "ps 23"). Swipe or tap to move between chapters.
- **Reading.** Clean text with verse numbers and tap-to-open notes. Adjustable type size,
  light and dark themes, and search across the whole Bible that runs on the device.
- **Original language, stage 1 (verse level).** Tap a verse to see it in Hebrew, Aramaic or
  Greek, with its notes and a word-by-word breakdown: each word's dictionary form, grammar and
  a short definition. Sources: MorphGNT for the Greek (already in `.cache/`), and STEPBible's
  tagged Hebrew and Greek texts and brief lexicons (CC BY 4.0).
- **Original language, stage 2 (phrase level).** Hover over or tap an English phrase to see
  the Hebrew or Greek words it translates, with their meaning. The translation is
  meaning-based, so each chapter needs a file linking its English phrases to source words.
  These links are drafted chapter by chapter, checked automatically so that every source word
  is accounted for, and reviewed with the translation.
- **Verse numbers.** The Old Testament follows the Hebrew numbering, which differs from English
  Bibles in about 1,970 verses. The reader offers English numbering too, using the TVTMS
  mapping already in this project.
- **Draft labels.** A "Draft" badge on every chapter that hasn't been reviewed, a short
  explanation the first time a reader sees one, and a link to the review process in
  `TRANSLATION.md`. The badge changes as a chapter moves to *checked*, *reviewed* and
  *approved*.
- **Highlights and notes (on the device).** Readers can highlight, underline and write notes,
  saved in the browser's storage. Each annotation is tied to a verse reference and a position
  within the verse, not to page layout, so it survives text corrections. Export and import
  keep a backup.

## 2. Maps

- **Style.** See *Map style: after the Eilers wall maps* below. Maps keep their paper look in
  dark mode, dimmed slightly, as a printed sheet would.
- **Open sources** (licenses to confirm before use):
  - Natural Earth for coastlines and rivers
  - open elevation data (SRTM or Copernicus), from which the mountain hachures are drawn
  - OpenBible.info's Bible geocoding, which gives a confidence level for each identification
  - this project's place coordinates (961 of 1,004 places)
  - the Ancient World Mapping Center and Pleiades for ancient coastlines, roads and sites
- **Interactive and printable.** Interactive maps use MapLibre, with the map data packed into
  one static file, so there's no map server. The same maps also export as SVG, PDF and PNG
  at Letter, A4 and 16:9 slide sizes, for printing and slide shows.
- **Period maps** (notable places, no routes):
  - the patriarchs
  - the Exodus and the conquest
  - the tribal allotments
  - the united kingdom
  - Israel and Judah
  - the Assyrian, Babylonian and Persian empires
  - Jesus' Palestine
  - the Roman world of Acts
- **Journey maps:**
  - Abraham
  - Jacob
  - the Exodus
  - David
  - Elijah and Elisha
  - the exile and return
  - Jesus' ministry, one Gospel at a time
  - Paul's three journeys and his voyage to Rome
- **Linked to the text.** Every route leg links to its verses. Tapping a leg opens the reader.
- **Uncertainty shown.**
  - Disputed routes and sites, such as the Exodus route and Mount Sinai, appear as labeled
    alternatives.
  - Doubtful identifications are drawn differently from certain ones.
  - Each map credits its sources.

### Map style: after the Eilers wall maps

A. H. Eilers & Co. of St. Louis published Sunday School wall maps of the Bible lands from
about 1890 to 1930 (dealers' dates vary). The reference copies for this style are Map No. 4
*Western Asia*, Map No. 5 *The Exodus* and Map No. 7 *The Kingdoms Judah Israel*. They were
published before 1931, so they are in the public domain in the United States. Even so, our
maps are drawn fresh from open data, not traced.

**What we keep:**

- **Flat tints.** Each region, tribe or kingdom gets one flat color with no gradients, from a
  small chromolithograph palette. The seas stay paper-colored. Starting values, sampled from
  the reference photos and adjusted for contrast:

  | Tint | Hex | Eilers use |
  |---|---|---|
  | Paper | `#f6f0dd` | margins and seas |
  | Chrome yellow | `#f6e27f` | Israel, Egypt, Syria |
  | Salmon | `#f2b98a` | Judah |
  | Blush | `#f8d8c0` | the Sinai deserts, Mesopotamia |
  | Pale lime | `#e3e6a2` | tribal areas |
  | Sage | `#c9d8a5` | Gilead, Philistia |
  | Olive | `#d9c784` | Assyria |
  | Water | `#c6d7d8` | lakes and the Salt Sea |
  | Ink | `#1f1b16` | all type and linework |
  | Vermilion | `#d8432a` | routes |
  | Deep red | `#a8301a` | kingdom names and titles |

- **Coastlines.** Shores are drawn with ripple lines, fine lines repeated outward from the
  shore, and a darker edge along the coast.
- **Mountains.** Mountains are hachured ridges and peaks, as on the Sinai inset of Map No. 5,
  drawn from real elevation data so they sit where the mountains really are.
- **Region names.** Regions, tribes and deserts are named in large, widely spaced condensed
  capitals that follow the shape of the region (A S H E R, D E S E R T  O F  P A R A N).
- **Kingdom names.** Kingdoms and empires are overprinted in big red capitals (ISRAEL,
  JUDAH).
- **Place names.** Places are set in bold roman beside a dot, sized by importance.
- **Three name styles.** A key explains them, as on Map No. 4: Bible names in bold, Greek
  and Roman names in roman, and modern names in italic.
- **Journeys.** Each journey is a bold vermilion line with numbered stations. A station
  table gives each stop's identification, its certainty and its Bible references, as on Map
  No. 5. Uncertain stretches are labeled "Conjectural route", as Eilers did.
- **Finding places.** Thin latitude and longitude lines run across the map, numbered in the
  margin, with an index of places keyed to them, as on Map No. 7.
- **Insets.** Maps can carry insets: a plan of Jerusalem, close-ups such as "Vicinity of
  Mt. Sinai", and a small locator map.
- **Title block.** The title block uses mixed Victorian type in red and black: the series
  and map number, the title, a "showing…" line, the dates, and a credit line. Our maps are
  numbered as a series too. Dates come from this project's chronology, which the title block
  names.
- **Border.** A paper margin surrounds the map, with a ruled border line.

**What we change, for legibility:**

- **No overlaps.** Eilers let names run over each other and under the red overprints. Ours
  never overlap: labels are placed in priority order, each has a thin paper-colored halo,
  and lesser names appear only when zoomed in or printed large.
- **Minimum sizes.** Type is at least 7 pt in print and 11 px on screen.
- **Tighter region spacing.** Region capitals are spaced less widely than Eilers' (whose
  M A N A S S E H runs down much of the sheet), so they still read as one word.
- **Contrast.** Ink on every tint has a contrast ratio of at least 9.8:1. Vermilion on
  salmon is only 2.5:1, so routes get a paper-colored edge.
- **Color blindness.** Red routes are set apart by width and numbered stations, not by color
  alone. Chrome yellow and pale lime are equally light, so they are never used side by side
  without a drawn boundary. Every map is checked with a color-blindness simulator.
- **Modern features.** Railways, canals and modern towns go on an optional layer. Eilers
  printed them on the map itself.
- **Fonts.** The fonts are open (SIL Open Font License) with a Victorian flavor, chosen in
  the style study. Candidates:
  - Old Standard TT for place names and italics
  - a condensed slab such as Rokkitt or Zilla Slab for regions
  - Bodoni Moda or Playfair Display for the red overprints

**Style study.** The first map redraws Map No. 7, *The Kingdoms of Judah and Israel*, so the
two can be compared side by side. Exodus routes and station tables (Map No. 5) come next.

**Boundaries.** Tribal and kingdom boundaries have no open dataset that we know of. We will
draw them from the boundary lists in Joshua 13–19 and the identified sites, and mark them as
approximate.

## 3. Genealogy viewer

- **Everyone connected.** All 1,025 people in Adam's family across 78 generations, the line
  from Adam to Jesus highlighted, and the other families linked by marriage.
- **Built for phones.**
  - The tree is laid out once when the site is built, not on the phone.
  - It's drawn on a canvas instead of thousands of page elements.
  - Names appear only when zoomed in far enough to read them.
  - The data holds only what the viewer draws, in a compact format. Today's file is 866 KB
    (146 KB compressed) and should shrink well below that.
  - Targets: smooth pinch-zoom and panning on a mid-range phone, usable within 2 seconds.
- **Finding people.** Search, a focused view of one person's family (the present hourglass
  view), and links to the passages where they appear and the places they lived.

## 4. Accounts (later)

- Optional sign-in. Reading and on-device annotations never require an account.
- Signing in merges that device's highlights and notes into the account, then keeps devices in
  sync.
- Recommended service: Supabase, which is open source and can be self-hosted later. This is the
  first part with running costs, personal data and security obligations, so it comes last and
  gets its own privacy policy.

## 5. Traditional Chinese translation (after the English is finished)

A new translation into Traditional Chinese (繁體中文), made like the English one.

- **Starting point.** When the English has been reviewed, so that its notes and glossary are
  settled.
- **Translated from the source.** The Chinese is translated from the Hebrew, Aramaic and
  Greek, not from the English. The English translation and its notes serve as a guide to the
  decisions already made.
- **Its own guide.** A `TRANSLATION.zh-Hant.md` with goals, a glossary and a checklist, like
  `TRANSLATION.md`. Decisions to make first:
  - **God:** 上帝 or 神. This is the long-standing "term question"; the Chinese Union Version
    is printed in both forms.
  - **The divine name:** 耶和華, the Chinese Union Version's form, or 雅威, which matches the
    English "Yahweh".
  - **Proper names:** follow the Chinese Union Version's familiar transliterations, so
    readers recognize them, with notes where they differ from the original pronunciation.
  - **Key terms:** 聖靈, 彌賽亞 and 基督 (matching the English "the Messiah" and "Christ"),
    and the rest of the glossary.
  - **Register:** plain modern written Chinese for the same readers as the English, about age
    12–14 and up.
  - **Punctuation:** Taiwan's standard: 「」 and 『』 for quotations, full-width marks.
- **Format and checks.** `translation-zh-Hant/NN-book/CCC.md`, with the same front matter and
  the same automated checks: every verse present, notes linked, draft status. It compiles to
  `text/chinese-traditional/`.
- **In the reader.** A language switch for the text and for the app's own interface, and
  Chinese beside English or the original languages.
- **Review.** Native speakers who read Hebrew or Greek, in the same draft → checked → reviewed
  → approved process.
- **License.** CC BY 4.0, like the English.

## Order of work

1. Foundation and the reader, with verse-level original language and draft labels.
2. Maps, beginning with the style study (Eilers Map No. 7 redrawn), then the Exodus map.
3. Genealogy viewer.
4. Phrase-level original language, alongside human review of the English.
5. Accounts.
6. Traditional Chinese, once the English is finished.

## Open questions

- Domain and hosting account (see *Decisions so far*).
- Fonts and final tints, settled in the style study.
- How to source tribal and kingdom boundaries.
- Reviewers for the English, and later the Chinese.
