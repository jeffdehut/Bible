# Study markings

The reader can mark the key words of the whole Bible, as a reader does by hand in an inductive
study: God, Jesus and the Holy Spirit; themes such as love, faith, sin and covenant; life and
death; time and place; and the small words that join an argument together. They are off until a
reader turns them on (**Display → Study markings**, or **Study markings** in the menu), and each
marking can be turned off on its own, to follow one or two words through a book.

## The symbols

The symbols are our own. Their shape says what kind of word it is, and their color which word:

- **Outlines** are for God: a box for God and for Jesus, a dashed cloud for the Spirit.
- **Lines beneath** are for the themes: a single line, a double line, a dotted line, a wavy line
  for sin.
- **A wash of color** is for the words of worship and character: love, holy, glory.
- **A line through** is for the enemy, Satan.
- **A small sign** before the word gives a theme a second cue (♔ kingdom, ↻ repent, § law,
  ◷ time), and on its own marks the connecting words: ∴ therefore, ⇄ but, → so that.

Every marking is drawn with text decoration, borders and backgrounds, so it is sharp at any
size, follows the light and dark themes, and copies and searches as plain text.

| Marking | How it looks | Color | Source words (Strong's) |
|---|---|---|---|
| **God** | | | |
| God | a box | gold | H410 H426 H430 H433 H3050 H3068 H3069 H136 G2316 G3962 |
| Jesus | a box | crimson | G2424 G5547 G3323 G5207 G721 G286 |
| The Holy Spirit | a dashed cloud | teal | H7307 G4151 |
| Satan | struck through | red | H7854 G4567 G1228 G954 G1404 |
| **Key themes** | | | |
| Love | a wash of color | pink | G25 G26 G27 G5368 G5360 H157 H160 H2617 |
| Faith | double underline | blue | G4102 G4100 G4103 G4135 H539 H530 |
| Grace | underlined | green | G5485 G5483 H2580 H2603 |
| Sin | wavy underline | brown | G266 G264 G268 G265 G3900 G458 G93 H2403 H2398 H2399 H2400 H5771 H6588 H6586 H7563 |
| Repent | underlined, with ↻ | orange | G3340 G3341 G1994 H7725 |
| Covenant | a ring | indigo | H1285 G1242 |
| Kingdom | underlined, with ♔ | purple | G932 H4467 H4438 H4437 |
| Salvation | double underline | green | G4982 G4991 G4990 G4992 H3467 H3444 H3468 H8668 |
| Righteousness | underlined | navy | G1342 G1343 G1344 G1345 H6662 H6664 H6666 H6663 |
| Holy | a wash of color | violet | G40 G37 G38 G42 H6944 H6918 H6942 |
| Glory | a wash of color | amber | G1391 G1392 H3519 |
| Prayer | a ring | sky | G4336 G4335 G1189 G1162 H6419 H8605 |
| Law | underlined, with § | slate | G3551 H8451 |
| Truth | dotted underline | teal | G225 G227 G228 H571 |
| **Life and death** | | | |
| Life | dotted underline | green | G2222 G2198 H2416 H2421 H2425 |
| Death | dotted underline | gray | G2288 G599 G3498 G2348 H4194 H4191 |
| **Time and place** | | | |
| Time | dotted underline, with ◷ | olive | G2250 G5610 G2540 G5550 G4594 H3117 H6256 H8141 G2094 H3119 H6258 G3568 |
| Places | double underline | leaf | proper nouns of place |
| **Connecting words** | | | |
| Therefore | a sign before it: ∴ | ink | G3767 G1352 G686 G5105 G1223 H3651 H6258 H5921 |
| But | a sign before it: ⇄ | ink | G235 G1161 G4133 H61 H3588 H389 H657 |
| So that | a sign before it: → | ink | G2443 G3704 G5620 G1519 H4616 H5668 |
## How a word is chosen

A marking is defined by meaning, not by English spelling. Each lists the Strong's numbers of the
Hebrew, Aramaic and Greek words it stands for, and the forms those words take in English. A form
is marked only in a verse whose source has one of the words. So "Spirit" is marked where the
Greek has *pneuma* or the Hebrew *ruach*, and only where the translation capitalizes it as God's
Spirit; "love" is marked in a verse about love, not in "I would love to". A few forms carry
their own word: "Lord" is marked as God only where the Hebrew is *Adonai* (written `Lord@H136`),
not where a servant says "my lord". Places are found from the source itself: every proper noun
of place in the verse (the OSHB and TAGNT grammar codes) is marked where its name appears.

Where two markings would cover the same words, the longer wins, and the markings of God come
first: "Lord Jesus Christ" is one mark, not three.

The markings are only as good as the alignment of word and meaning, and some words are left
unmarked on purpose: pronouns (*he*, *you*) are not marked as God, since that needs a reading of
each sentence; MACULA's referent data could add them later.

## Building them

```
python3 scripts/markings.py            # after reader.py: data/bible/markings/
python3 scripts/markings.py --check    # also list verses whose source words call for a marking
                                        # but where no English form matched, to tune the forms
```

`data/bible/markings/rules.json` holds the groups and markings: how each looks, its Strong's
numbers, and its name, note, sample and forms for each language. `data/bible/markings/en/` holds
each book: for each chapter, for each verse, a flat list `[start, end, marking, ...]`, counting
the characters of the verse as the reader shows them (without note markers or the asterisks of
italics), the same way partial highlights count.

## Another language

A translation in another language needs no new symbols. Add its forms to each marking in
`scripts/markings.py` (and its names, notes and samples), point the script at that language's
text, and it writes `data/bible/markings/<language>/`. The reader reads `MARK_LANG` to choose the
folder and the names in the key. Because the words are chosen by their Strong's numbers, the same
verses are marked in every language, and a reader comparing two translations sees the same
words lit in both.

## Later

- Personal markings: let a reader choose a symbol from this set for a word or phrase they select,
  kept and synced with their highlights.
- Pronouns and other references to God, from MACULA's referent data (its CC BY parts).
- More markings: light and darkness, the word of God, commands, "if" conditions.
