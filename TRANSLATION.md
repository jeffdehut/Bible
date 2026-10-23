# The Open Plain English Translation

A new translation of the Bible into plain English, made directly from the Hebrew, Aramaic and
Greek texts in this repository. It aims to say what the original says, as clearly as everyday
English allows, and to show its work wherever a choice had to be made. It is open: anyone may
use, copy, adapt and redistribute it.

**Status:** pilot. Three chapters are drafted to settle the approach: Genesis 1, Psalm 23 and
John 1. See [translation/STATUS.md](translation/STATUS.md). No chapter has had human review
yet, so nothing here should be quoted as a finished translation.

## Goals

1. **Accurate meaning.** Every verse says what the source text says. Nothing is added, nothing
   is left out, and nothing is softened or sharpened.
2. **Plain English.** Natural modern English that a reader around 12–14 years old can follow.
   Sentences are short, vocabulary is everyday, and idioms are rendered by their meaning.
3. **Transparency.** Where the source can reasonably be read more than one way, where an
   idiom or image has been restated, or where manuscripts differ in a way that matters, a
   note says so. A reader should always be able to find out what the original says.

## Principles

**Translate the source as it stands.** The Old Testament follows the Leningrad Codex (UXLC
2.6) and the New Testament the SBL Greek New Testament (v1.2), the same texts verified in
this repository. Where the Hebrew vowel points (added in the Middle Ages) read awkwardly and
the consonants support a more natural reading, we may follow that reading and give the
pointed reading in a note. Significant differences from other editions, such as those in
the SBLGNT apparatus or the Septuagint, are noted rather than adopted.

**Meaning-based, not a paraphrase.** We translate thought for thought within each verse, not
word for word. We keep:
- the imagery where an English reader can follow it ("Yahweh is my shepherd")
- the repetition and structure of poetry and narrative
- the text's own ambiguity where it is deliberate or unresolved

Where the plain rendering states a meaning the words only imply, the literal wording goes in
a note.

**No interpretation beyond the text.** We don't harmonize passages, resolve doctrinal
questions, or add explanatory words to the text itself. Explanations go in notes.

**Consistency.** Key terms are translated the same way throughout unless context requires
otherwise, and each such case is noted. The glossary below records the decisions.

**Verse numbers follow the source.** In the Old Testament this is the Hebrew numbering, so
Psalm titles are verse 1 and some chapters are divided differently from English Bibles. The
connection notes map between the two.

## Decisions (glossary)

Decisions marked **proposed** are used in the pilot and are open for review.

| Source | Rendering | Notes |
|---|---|---|
| יהוה (YHWH, the divine name) | **Yahweh** | God's personal name, in its probable pronunciation. Most English Bibles write "the LORD"; a note says so at the name's first occurrence in each chapter where it appears. In the New Testament, Greek *kyrios* is "the Lord", with a note where it quotes a passage using the name. |
| אֱלֹהִים (Elohim), θεός | God | |
| אָדָם (adam), when it means humanity | humankind / human beings | When it refers to the man Adam, *Adam*. |
| נֶפֶשׁ (nephesh) | life, self, soul, living being, by context | Not automatically "soul". |
| חֶסֶד (chesed) | faithful love | Loyal, covenant love. Noted where it matters. |
| ὁ χριστός, מָשִׁיחַ | the Messiah | As a title. "Christ" where it functions as a name, e.g. *Jesus Christ*. |
| ὁ λόγος (John 1) | the Word | |
| οἱ Ἰουδαῖοι | the Jews | Kept as written. A note explains where the context shows the religious authorities in Jerusalem are meant (common in John). |
| ἀδελφοί (to a mixed group) | brothers and sisters (proposed) | When the context shows the group includes women; otherwise *brothers*. |
| Units, money, time of day | modern equivalents in the text, the original in a note | e.g. "about four in the afternoon" for "the tenth hour". |

## Format

Each chapter is one file, `translation/NN-book/CCC.md` (e.g. `translation/43-john/001.md`):

```markdown
---
book: John
chapter: 1
source: SBLGNT v1.2
status: draft          # draft → checked → reviewed → approved
translator: Claude (AI), pilot
reviewers: []
---

**1** In the beginning was the Word. The Word was with God, and the Word was God.[^1]

[^1]: *Word*: Greek *logos* ...
```

- One `**N** text` line for every verse in the source chapter, and nothing else.
- Notes are Markdown footnotes, numbered within the chapter.
- `python3 scripts/translation.py` checks every chapter against its source and fails on any
  missing or extra verse, or on unused or undefined notes. It then compiles the chapters into
  `text/english/NN-book.md` and writes `translation/STATUS.md`. The chapter notes in
  `connections/` show the translation beside the original.

## Process and review

1. **Draft.** Translated from the Hebrew or Greek of this repository, verse by verse, with
   notes. Pilot drafts are AI-generated (Claude), and every file's `translator` field says so.
2. **Checked.** Automated checks pass, and the chapter is compared against the source and a
   lexicon for omissions and additions.
3. **Reviewed.** At least one reviewer who reads the source language confirms every verse,
   and their names are recorded in `reviewers`.
4. **Approved.** Accepted for the published translation.

The published text (`text/english/`) shows each chapter's status, so readers know what
they're reading.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): anyone may use, share and adapt the
translation, including commercially, as long as they give attribution. See
[translation/LICENSE.md](translation/LICENSE.md) for the attribution wording.
