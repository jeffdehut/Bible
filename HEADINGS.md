# Section headings and book introductions

Phase 2 of the study helps (see ROADMAP.md, *Study helps*): headings through every chapter of
the Open Plain English Translation, and a short introduction to each of the 66 books. This
file is both the guide for writing them and the plan for drafting them all in one overnight
run. Like the translation, everything written here is a **draft** until a person reviews it.

## What we're making

- **Section headings**: a short title over each passage (a story, a speech, an oracle, a
  section of a letter), like "Jesus and Nicodemus" over John 3:1. About 2,500–3,500 in all:
  roughly one every 8–20 verses, more often in fast-moving narrative and less often in long
  speeches, laws and lists.
- **Book introductions**: for each book, about 350–550 words a reader can take in before
  starting: what the book is, who wrote it and when (as far as anyone knows), its setting, an
  outline that links into the text, and its main themes.

## Decisions

Defaults, chosen so the run can go ahead; any can be changed before it does.

1. **Psalms have no section headings.** Each psalm is a unit, and most already carry a title
   in the text itself (verse 1 in our numbering). The introduction outlines the five books of
   the Psalms instead. *(Open: a short heading for every psalm, as many Bibles have, is
   possible.)*
2. **Proverbs 10:1–22:16 and 25–29** (the collections of single sayings) get headings only
   where the text starts a new collection (10:1, 22:17, 24:23, 25:1, 30:1, 31:1, 31:10), not
   topic by topic: the sayings aren't grouped by topic in the Hebrew.
3. **Lists and genealogies** get one heading for the whole list ("The descendants of Esau"),
   not one per family.
4. **Parallel passages share wording.** Where the Gospels tell the same event (the sections of
   Robertson's harmony in `data/bible/study/parallels.json`), or Chronicles retells Samuel and
   Kings, the headings use the same words, so a reader can recognize them.
5. **Headings appear by default**, with a setting to turn them off (*Display → Section
   headings*), as the translation notes have now.
6. **Authorship and date** are stated the way a careful study Bible states them: what the book
   itself says, what tradition holds, and, where scholars widely disagree, that they disagree,
   without taking a side. *(Open: whether to mention critical views at all.)*

## Heading style

Headings follow the translation's own rules (TRANSLATION.md): plain English for a reader of
about 12–14, nothing added, nothing interpreted.

- **Describe, don't interpret.** Say what happens or what is said: "Jesus heals a man born
  blind", not "The light of the world". No doctrine, no application, no moral.
- **Short.** At most 60 characters, ideally 3–7 words. No final full stop.
- **Sentence case**: capital letter only at the start and for names ("Paul sails for Rome").
- **The translation's own names and terms**, spelled as it spells them (its glossary decides:
  *the LORD*, *Messiah*, *Holy Spirit*, place and personal names as in the text). A heading
  never uses a word the passage itself doesn't support.
- **The subject named**, not "he" or "they": "Abraham bargains for Sodom".
- **No verse references** in the heading text.
- **Where a passage starts**: at a verse where the source text starts a paragraph (the
  Masoretic paragraph marks in the Old Testament, STEPBible's in the New; the reader's data
  marks the verse before with `"p": 1`), or at the first verse of a chapter. The checker warns
  about any other place, and the heading's author must say why in the run's report.
- **Every book starts with a heading at 1:1.** A heading may span a chapter break; a chapter
  needn't start with one if the passage carries on.
- **Prophets and letters**: one heading per oracle or argument, named by its subject ("Against
  Edom", "Faith and works"), keeping the prophet's or writer's own framing.

## Introduction style

The same plain English, in this order, under these headings:

1. **In brief**: one or two sentences: what kind of book it is and what it's about.
2. **Who wrote it, and when**: what the book says about itself; what Jewish and Christian
   tradition holds; where scholars differ, a sentence saying so, without choosing. Dates as
   ranges ("about 700 BC", "probably in the 60s AD"), never more precise than the evidence.
3. **Setting**: where and when its events or first readers were, and what was happening.
4. **Outline**: four to ten parts, each a verse range and a title, covering the whole book in
   order with no gaps or overlaps. The titles may reuse the section headings.
5. **Themes**: three to five, each one or two sentences with a verse that shows it.
6. **Connections**: where the book is quoted or echoed elsewhere in the Bible, with references
   (the cross-references in `connections/` and the parallels help here).

Every factual claim about the book's contents gives a verse. Nothing is said about history,
archaeology or authorship that a standard study Bible wouldn't say; when unsure, leave it out.

## Files

Beside each book's chapters in `translation/NN-book/`:

`headings.md`: one heading per line, chapter:verse then the heading.

```markdown
---
book: Ruth
status: draft          # draft → checked → reviewed → approved, as for the translation
author: Claude (AI), draft
reviewers: []
---

1:1 Naomi loses her husband and her sons
1:6 Ruth goes with Naomi to Bethlehem
2:1 Ruth gleans in the field of Boaz
```

`intro.md`: the introduction, its outline as a list of ranges.

```markdown
---
book: Ruth
status: draft
author: Claude (AI), draft
reviewers: []
---

## In brief
...

## Outline
- 1:1–22 Naomi and Ruth return from Moab
- 2:1–23 Ruth meets Boaz
...
```

Verse numbers are this translation's (Hebrew numbering in the Old Testament).

## Tools to build first

1. **`scripts/headings.py`**: checks every `headings.md` and `intro.md` and reports, book by
   book:
   - *errors* (the run must fix them): bad front matter; a reference that isn't a verse;
     headings out of order or repeated; no heading at 1:1; any heading in Psalms; a heading
     over 60 characters, ending in a full stop, or containing a verse reference; an outline
     that doesn't cover the book exactly; an introduction section missing; a reference in an
     introduction that isn't a verse.
   - *warnings* (allowed, but listed in the report): a heading not at a paragraph start; more
     than 30 verses or fewer than 3 between headings (outside lists and Psalms); an
     introduction under 300 or over 650 words; a name in a heading that the chapter's English
     doesn't contain; parallel passages whose headings differ.
2. **`scripts/reader.py`** adds each chapter's headings to `data/bible/text/NN-book.json`
   (`"h": [[verse, "heading"], ...]`) and writes the introductions to
   `data/bible/intros/NN-book.json`.
3. **The reader**: headings set above their verse in a small sans-serif, as print Bibles do;
   the *Display* setting to hide them; *About this book* on each book's first chapter and in
   the book picker, opening the introduction, whose outline links into the text; and the
   headings used as titles for the Kings and Chronicles parallels, which have none yet.
4. **Calibration samples**, written by hand before the run and reviewed by the owner: Ruth
   (narrative), Amos (prophecy), Mark (a Gospel) and Philippians (a letter). These become the
   examples the run imitates.

## The overnight run

A workflow of agents, started only when the owner asks for it ("run the phase 2 workflow"),
on the working branch, never on `main`.

**Stage 1: drafting.** Ten agents in parallel, one per batch, each working through its books in
order. The batches are balanced by length and keep related books together:

| Batch | Books | Chapters | Words of translation |
|---|---|---|---|
| 1 | Genesis – Leviticus | 117 | 89,000 |
| 2 | Numbers – Joshua | 94 | 74,000 |
| 3 | Judges – 2 Samuel | 80 | 62,000 |
| 4 | 1 Kings – 2 Chronicles | 112 | 87,000 |
| 5 | Ezra – Psalms | 225 | 81,000 |
| 6 | Proverbs – Isaiah | 117 | 57,000 |
| 7 | Jeremiah – Ezekiel | 105 | 81,000 |
| 8 | Daniel – Malachi | 79 | 40,000 |
| 9 | Matthew – John | 89 | 80,000 |
| 10 | Acts – Revelation | 171 | 97,000 |

Each agent, for each book: reads this guide, TRANSLATION.md's glossary and the calibration
samples; reads **every chapter** of the book's translation (`translation/NN-book/*.md`) and the
paragraph marks; writes `headings.md`, then `intro.md`; runs `python3 scripts/headings.py
BOOK` and fixes every error; and lists what it was unsure of. It edits only those two files
for its own books: never the translation, the data or the scripts.

**Stage 2: review.** Three agents, once drafting is done, each reading the drafts fresh:

- *Parallels*: makes the headings of every Gospel section in `parallels.json`, and of Samuel
  and Kings beside Chronicles, use the same wording.
- *Style*: reads all the headings against the style rules above and the glossary, and fixes
  wording that interprets, runs long, or names things the passage doesn't.
- *Facts*: reads every introduction, checks each claim against its verse, and softens or
  removes any claim about authorship, date or history that goes beyond what's said above;
  everything it changes or doubts goes in the report.

**Stage 3: checking and handing over** (the session that started the run):

1. `scripts/headings.py` reports no errors for any book; `scripts/translation.py` still passes
   (the translation is untouched).
2. `scripts/reader.py` rebuilds the reader's data; the reader is checked in a browser on a
   phone and a wide screen, light and dark, with headings on and off.
3. One commit per batch on the working branch, pushed; nothing is merged into `main`.
4. A morning report: headings and words written per book, every warning left, everything an
   agent was unsure of, and a few sample pages to look at.

**Cost and time.** No money: it runs on the Claude plan, and building and previewing are local.
It reads the whole translation (about 750,000 words) once to draft and the drafts again to
review: a few million tokens of usage, in a burst. Expect two to four hours.

**If something goes wrong**, each batch stands alone: a failed batch is re-run by itself, and a
batch whose drafts fail review is left out of the commits and listed in the report.

## Done when

- Every book has `headings.md` (Psalms: none) and `intro.md`, and the checker reports no
  errors.
- The reader shows headings and introductions, labelled as drafts, on phone and desktop.
- The owner has read the samples and the morning report, and decides what to merge.

## After this

- Human review of the headings and introductions, with the translation (TRANSLATION.md,
  *Process and review*).
- The consistency read of the whole translation against TRANSLATION.md's rules can follow the
  same pattern: a script for the mechanical rules, then agents batch by batch for the rest,
  reporting rather than editing.
