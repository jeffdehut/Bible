# Roadmap

The next iteration turns this repository into a web app for reading and studying the Bible:
a reader for the Open Plain English Translation with the Hebrew, Aramaic and Greek beneath it,
Bible maps, and a genealogy viewer, all built for phones first. After that comes a Traditional
Chinese translation.

## Decisions so far

| Question | Decision |
|---|---|
| Who it's for | Phone users first; tablets and desktops follow from the same design. |
| Hosting | For now, a test site on Netlify (`biblemadeplain.netlify.app`), published from GitHub: `main` live, other branches as free previews. Each live publish uses 15 of the free plan's 300 monthly credits. Later, perhaps Porkbun (domain, static hosting and email in one place) or Cloudflare Pages, together with the owner's other sites. |
| Domain | `bibledata.org`, registered at Porkbun on 29 Oct 2026 (renews 29 Oct each year). Being pointed at the Netlify test site (see DEPLOY.md, *The bibledata.org domain*), with the sign-in emails sent from it through Resend and `privacy@bibledata.org` forwarded to the owner. |
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

1. **Data build (done for the reader).** `scripts/reader.py` turns the repository into small
   files the app loads on demand: for each book, its text and notes, and separately its word
   data, which loads only when a verse is opened; the lexicon in twenty parts; and one file
   for search. `scripts/maps.py` does the same for the maps.
2. **App shell (done).** `index.html` is one static web app that installs on a phone and
   works offline, in the design of `genealogy.html` and `history.html`.
3. **Hosting (test site ready).** The repository root is the website, so Netlify can publish it
   straight from GitHub: `main` as the live site, every other branch at a preview address
   (see DEPLOY.md).

## 1. Reader

**Stage 1 is built** (`index.html`, with its data from `scripts/reader.py`):

- **Choosing a passage:** a book and chapter picker with Old and New Testament tabs, recent
  chapters, and typed references ("jn 3 16", "ps 23"). Swipe, tap or use the arrow keys to
  move between chapters.
- **Reading:** verse numbers and lettered notes that open on a tap. Paragraphs follow the
  Masoretic paragraph marks and, in the New Testament, STEPBible's. Poetry (Job, Psalms,
  Proverbs, Song of Songs, Lamentations) is set a verse to a line. There are text sizes,
  light and dark themes, and search across the whole Bible on the device.
- **Original language, verse level:** tap a verse to see it in Hebrew, Aramaic or Greek, with
  its notes and a word-by-word breakdown. Tap a word for its dictionary form, gloss, grammar,
  parts (prefixes and suffixes) and a short definition. Sources: STEPBible's TAHOT and TAGNT
  for words and glosses, and TBESH and TBESG for definitions, all CC BY 4.0. Each of our words
  is matched to STEPBible's by its letters; 99.5% match.
- **Verse numbers:** Hebrew numbering, with English numbering as a setting.
- **Draft labels:** a badge on every chapter, a one-time notice, and an explanation of the
  review stages.
- **Highlights and notes, on the device:** five highlight colors and a note per verse, stored
  by verse reference. A backup can be copied or saved and restored, keeping the newer of
  each.
- **Offline:** a web app manifest and a service worker, so the reader installs on a phone and
  keeps the books it has opened.

**Next:**

- **Original language, stage 2 (phrase level).** Hover over or tap an English phrase to see
  the Hebrew or Greek words it translates. The translation is meaning-based, so each chapter
  needs a file linking its English phrases to source words. These links are drafted chapter
  by chapter, checked automatically so that every source word is accounted for, and reviewed
  with the translation.
- Highlights on part of a verse (the stored format already allows a position within the
  verse), and notes on a passage.
- Links from people to the genealogy and from places to the maps are done: a verse lists the
  people it names under *People* and the places under *On the maps*.
- Cross-references beside each verse (OpenBible.info, already in `connections/`).

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

  All of these are drawn now, on eight sheets: see *The set* below.
- **Linked to the text.** Every stop's verse, and the verse that first names each place, opens
  the reader. A place opened from the reader links back to its verse. Still to come: tapping a
  route leg to read the verses it covers.
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

**Style study (done).** Map No. 7, *The Kingdoms of Judah and Israel*
(`maps/kingdoms.html`, built by `scripts/maps.py`), redraws the Eilers map from open data
so the two can be compared side by side. It settled:

- **Fonts:** Abril Fatface for the red kingdom names and the title; Rokkitt for the tribes and
  peoples, set as upright letters spaced along a line through each region, as Eilers did;
  Old Standard TT for places, water and the key.
- **Tints:** the palette above, unchanged. Kingdoms take one tint each, and neighbouring
  peoples share the remaining tints only where they don't touch.
- **Labels:** placed by priority on the reader's screen (royal cities and the most-named
  places first, then regions, then the rest), so none overlap and more appear on zooming in.
  The same placement lays out the printed page and the SVG.
- **Water and relief:** the coast and lakes come from elevation data, with Lake Huleh and the
  Dead Sea at their old shorelines; rivers follow the drainage of the land.

**The set (done).** Eight sheets, numbered as the Eilers series where a sheet of the same
subject is known (dealers' listings give No. 1 Palestine, No. 2 Palestine, Old Testament
History, No. 3 the Roman Empire, No. 4 Western Asia, No. 5 the Exodus and No. 7 the kingdoms,
with an unnumbered Ancient Jerusalem). No Eilers No. 6 is known, so it goes to the empires of
the exile. `maps/index.html` lists them in the order of the Bible's history:

| Sheet | Lands | Journeys |
|---|---|---|
| No. 4, Western Asia | Egypt to Persia, as Eilers tinted them | Abraham, Jacob, Joseph |
| No. 5, The Exodus | Egypt, Canaan, Edom, Moab, the Amorites, Midian | the camps of Numbers 33 |
| No. 2, Old Testament history | the peoples of Canaan; David and Solomon's kingdom | Joshua south and north, Samuel, the ark, David |
| No. 7, The Kingdoms | the tribes and the two kingdoms | Elijah, Elisha |
| No. 6, The Empires | Assyria, Babylon or Persia, one at a time | Israel and Judah exiled, Jonah, Jeremiah, Ezra, Nehemiah |
| No. 1, Palestine | the realms of Luke 3:1 | the places each Gospel names, in its order |
| Plan of Jerusalem | hills, valleys and known sites; no walls | Jesus' last week, David's flight from Absalom |
| No. 3, The Roman Empire | the provinces about AD 50 | Paul's early years, three journeys, voyage to Rome |

What the set settled, beyond the style study:

- **Journeys.** Each is a list of stops, each named in the verse given, and the build checks
  every name against the translation. Land journeys follow the easiest ground; voyages keep to
  open water and run straight. A way the text leaves unsaid (Ur to Haran, Lystra to Troas) is
  dashed, and a stop the text names only as a region is listed but not plotted.
- **Periods.** One sheet can carry lands of different times (the empires; the peoples of
  Canaan and David's kingdom), chosen from the title tag.
- **Names.** Each place takes the spelling of the first verse that names it (Thessalonica,
  Shunem), and a people's name gives way to the place's (Lycaonia, Gerasa).
- **Larger sheets.** Lakes, and rivers where the elevation data can't trace them, come from
  Natural Earth, leaving out modern reservoirs.

**Next for the maps:**
- Review of the lands, the borders and the journeys by someone who knows the historical
  geography; the camps of Map No. 5 especially.
- Relief closer to engraved hachures: strokes in tiers between contours rather than scattered
  dashes.
- Walls on the plan of Jerusalem, if an open survey of the ancient walls can be found.
- Links from the reader to the maps (done): a verse lists the places it names, and each opens
  on the sheet that suits the book, zoomed in, with a link back. Next, the reverse for whole
  journeys: a route leg opening its verses.

**Map No. 5, The Exodus (done).** `maps/exodus.html` follows the camps of Numbers 33
and turned the style study into a series: one page template (`scripts/templates/map.html`) filled from
each map's data, with a route layer, numbered camps, a camp list and a printed camp table.

- **Camps:** plotted at OpenBible.info's best proposed site when it scores at least 150, and
  marked "?" below 500. Two camps proposed at one site share a marker, so 31 markers show 33
  of the 42 camps. The other 9 are listed with the reason: camp 7 is named only by the sea;
  Rimmon-perez, Libnah and Makheloth have no proposal scoring 150; Rissah's one proposal is far
  off in Arabia; and four camps are placed only "somewhere in the Negev".
- **Route:** the easiest way across the land between camps, from the elevation data. It is
  solid only between consecutive camps that both score at least 300.
- **Mount Sinai:** the camp is drawn at Jebel Musa, the traditional site. Triangles mark four
  other proposals: Har Karkom, Jebel Sin Bishar, Jebel Serbal and Jabal al-Lawz.
- **Peoples:** Egypt, Canaan, Edom, Moab, the Amorites under Sihon, and Midian, allotted the
  same way as the tribes. Wilderness names follow the books of Exodus and Numbers.
- **Needs review:** the camp identifications and the drawn route, by someone who knows the
  geography of the Sinai and the Negev.

**Boundaries.** No open dataset of tribal and kingdom boundaries is known to us, so the
territories are allotted automatically. Each piece of land goes to the tribe whose towns in
Joshua 13–19 and 21 are nearest on foot. Lakes cannot be crossed, and rivers are costly to
cross, so borders tend to follow them. A few towns are assigned by hand, with their verses,
in `scripts/maps.py`. The result is marked as approximate and needs review by someone who
knows the historical geography.

## 3. Genealogy viewer (built)

- **Everyone connected.** The whole family of Adam on one chart: 1,061 people over 76
  generations, with the families who married into it (Saul's through Michal, Ruth beside
  Boaz). The line from Adam to Jesus runs straight through in gold; choosing anyone draws
  their line back to Adam and their links to a mother or spouse set elsewhere on the chart.
- **Built for phones.**
  - The chart is laid out once when the site is built (`scripts/familytree.py`), not on the
    phone, in a tidy-tree layout where no two lines of descent cross.
  - It's drawn on a canvas instead of thousands of page elements.
  - Names appear inside the boxes once there is room; zoomed out, the best-known names show
    wherever they fit, and the eras of the line stay in view along the top.
  - The data is in columns, with the layout: 420 KB for the whole page (111 KB compressed),
    down from 617 KB (141 KB), though it now holds the chart too.
  - Measured on a phone-sized screen with the processor slowed four times: usable in 1.1
    seconds, and every frame of panning and pinching drawn in under 8 ms.
- **Finding people.** Search; the hourglass of one person's close family, for anyone,
  inside Adam's family or not; and the verses that name each person, each a link to the
  reader. The reader lists the people a verse names, each opening in the genealogy.
- **Still to come:** the places each person lived, linked to the maps.

## 3b. The Web of Scripture (built)

- **Everything connected, at once.** `graph.html` draws the connection notes as one
  web: 5,646 chapters, people, places and events, and 32,045
  threads, colored by section of the Bible, with people as points, places as rings and events
  as diamonds.
- **The opening.** The chapters light up round a wheel in order, the cross-references draw in
  across it, and the wheel unfolds into the web. The animation runs on the graphics card, from
  timings set once, so it costs the phone almost nothing; a tap moves it straight to the web,
  and readers who ask for less motion get the web at once.
- **Built for phones.** Laid out when the site is built (`scripts/graph.py`); the data is 121 KB
  compressed. Measured on a phone-sized screen with the processor slowed four times: ready to
  draw in 1.1 seconds, and about 2.5 ms of script per frame while panning.
- **Exploring.** Search, a card for whatever is chosen, links to the reader, the genealogy and
  the maps, the key as a filter, and *Wheel* to see the chapters in order. Each chapter in the
  reader and each person in the genealogy links to its place in the web.
- **Still to come:** threads for the cross-references within a chapter, and following a
  thread from verse to verse.

## 4. Accounts (built; waiting on a Supabase project)

- **Optional sign-in.** Reading and on-device annotations never require an account. With
  `config.js` empty, as it is now, the reader shows no sign-in at all.
- **Signing in** is by a code sent by email (or the link in the same email): no passwords to
  keep or leak. It merges the device's highlights and notes into the account, verse by verse,
  the newest change winning, then keeps devices in sync: each change is sent a few seconds after
  it is made, and other devices pick it up when the reader opens or comes back into view. A
  note removed on one device is removed on the others.
- **Service:** Supabase, reached through its REST interface, so the reader loads no extra
  library (`account.js`). The table and its rules are in `supabase/schema.sql`: each person
  can read and write only their own rows, and a write keeps whichever version of a verse is
  newer. Setup steps are in DEPLOY.md, *Accounts*.
- **Privacy:** `privacy.html` says what is kept (an email address and the highlights and
  notes) and how to delete it; **Delete my account** in the reader removes everything at once.
- **Tested** against a stand-in for the Supabase service: two devices merging, a deletion
  carried across, an expired sign-in renewed, a sign-in link, signing out and deleting.
- **To do before turning it on:** a Supabase project, a mail service for the sign-in emails,
  and a contact address for privacy questions (see *Open questions*).

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
  - **The divine name:** 耶和華, the Chinese Union Version's form, or 上主, a title like the
    English "the LORD".
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

1. Foundation and the reader, with verse-level original language and draft labels (stage 1
   done).
2. Maps: the set of eight sheets is done, as drafts for review, and linked both ways with the
   reader.
3. Genealogy viewer (built).
4. Phrase-level original language, alongside human review of the English.
5. Accounts (built and on, with the "Plain Bible" Supabase project; open to others once a mail service is set up).
6. Traditional Chinese, once the English is finished.

## Open questions

- Pointing `bibledata.org` at the site, and a long-term home for the hosting (see *Decisions so far*).
- Accounts: a mail service to send sign-in emails from the site's domain (until then Supabase's
  own mail reaches only the project's team, with a link and no code), and a contact address for
  privacy questions (DEPLOY.md, *Accounts*).
- Review of the maps: the approximate lands and borders on every sheet, the camps on Map No. 5,
  and the journeys.
- Reviewers for the English, and later the Chinese.
