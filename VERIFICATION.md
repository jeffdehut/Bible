# Text verification

This report records how the texts in this repository were checked against their published
reference editions, what was found, and what was changed. Run `python3 scripts/verify.py`
to repeat the checks. It downloads the reference editions and compares every verse.

Last verified: 23 Oct 2026.

## Summary

| | Reference edition | Result |
|---|---|---|
| Hebrew OT | UXLC 2.6 (Build 27.7, 18 Oct 2026), [tanach.us](https://tanach.us) | **Identical**, all 23,213 verses, after updating from 2.5 |
| Greek NT | Robinson's Scrivener 1894, [byztxt/greektext-scrivener](https://github.com/byztxt/greektext-scrivener) | **Identical**, all 7,957 verses, word for word |
| `text/greek` | Round trip back to the ASCII source | **Identical**, after one conversion fix (Rev 13:18) |

## Hebrew Old Testament

**What was received.** The zip file held UXLC 2.5 (Build 27.6, 31 Mar 2026). Every verse
matched UXLC 2.5 exactly. Some files had been re-saved with LF instead of CRLF line endings,
but their content was unchanged.

**What changed.** UXLC 2.6 came out on 18 Oct 2026. Its official change log
([2026.10.19 - Changes](https://tanach.us/Changes/2026.10.19%20-%20Changes/2026.10.19%20-%20Changes.html))
lists 140 change items: 79 accent corrections, 4 vowel corrections, 33 transcription-note-only
changes, and 24 items reviewed with no change. No consonants changed. Each item was checked
against the Leningrad Codex folio images.

Comparing our 2.5 files with 2.6 found 113 differing verses. **Every one of them is an item
in the official change log**, and no verse differed for any other reason. The sources were
replaced with the official 2.6 text files, byte for byte. These are the corrected verses:

| Book | Verses | References |
|---|---|---|
| Gen | 1 | 40:17 |
| Exod | 4 | 7:20, 11:6, 20:3, 38:12 |
| Lev | 4 | 7:25, 15:8, 16:21, 25:20 |
| Deut | 2 | 5:8, 33:28 |
| Josh | 4 | 5:1, 9:23, 10:24, 19:8 |
| Judg | 2 | 11:24, 21:16 |
| 1Sam | 2 | 7:10, 28:12 |
| 2Sam | 3 | 5:21, 11:11, 24:10 |
| 1Kgs | 3 | 2:30, 7:40, 12:5 |
| 2Kgs | 3 | 2:9, 8:18, 11:7 |
| 1Chr | 6 | 2:46, 4:28, 5:11, 5:16, 7:18, 14:11 |
| 2Chr | 6 | 1:10, 13:12, 16:2, 21:19, 24:27, 31:9 |
| Ezra | 2 | 6:2, 8:18 |
| Neh | 1 | 7:1 |
| Esth | 1 | 8:14 |
| Job | 3 | 17:3, 34:20, 39:28 |
| Ps | 38 | 5:11, 14:7, 15:5, 17:14, 19:15, 31:12, 31:24, 35:10, 37:40, 40:5, 40:6, 40:13, 42:3, 44:13, 46:12, 47:5, 50:23, 53:3, 53:7, 55:20, 58:10, 59:12, 60:3, 65:10, 69:1, 72:4, 86:9, 93:2, 94:6, 105:40, 106:29, 106:38, 118:17, 119:51, 119:61, 119:77, 119:109, 143:10 |
| Prov | 5 | 8:13, 19:7, 23:7, 28:3, 30:15 |
| Jer | 8 | 3:24, 8:9, 10:3, 12:10, 28:9, 46:4, 49:19, 51:9 |
| Ezek | 8 | 8:6, 11:1, 16:12, 23:11, 32:21, 33:28, 36:3, 44:6 |
| Dan | 2 | 5:3, 10:19 |
| Hos | 1 | 5:6 |
| Amos | 2 | 3:10, 8:12 |
| Mic | 1 | 1:14 |
| Zech | 1 | 12:5 |

**Things to know when using the Hebrew text.** These come from the source, not from errors.

- **Transcription notes** in square brackets are editorial marks from UXLC and the
  Westminster/Groves Center, not part of the codex:

  | Note | Meaning |
  |---|---|
  | `[c]` | Text is correct relative to the Leningrad Codex (a peculiarity of the LC) |
  | `[d]` | This tipeha is a dehi in other texts |
  | `[m]` | This meteg is a merkha in other texts |
  | `[q]` | UXLC differs from the conventional word for the qere |
  | `[t]` | Transcription uncertain. Check the LC image |
  | `[y]` | Yatir: the preceding letter is "superfluous" |
  | `[4]` | Puncta extraordinaria |
  | `[5]` `[6]` `[7]` | Large, small, or suspended letter(s) |
  | `[8]` | Inverted nun |
  | `[X]` | Verse does **not** occur in the Leningrad Codex |

- **Ketiv/qere.** The written form (ketiv) is marked `*` and is unpointed. The read form
  (qere) is marked `**`. Both are kept.
- **Joshua 21:36–37 are not in the Leningrad Codex.** UXLC supplies them, marked `[X]`, so
  the verse numbering stays continuous.

## Greek New Testament

**What was received.** The files match Dr. Maurice Robinson's public-domain digital text
of Scrivener's 1894 Textus Receptus word for word in all 7,957 verses. Readings typical of
Scrivener, such as Rev 16:5 ὁ ἐσόμενος, Acts 8:37, and 1 John 5:7, confirm the edition.

**Conversion fix.** In Rev 13:18 the number 666 (`cxv` in the source) is the Greek numeral
χξϛ, which uses a *stigma* (ϛ = 6). The converter had turned it into χξς, with a final
sigma. It now outputs χξϛ.

**Known limitations of the digital Scrivener text.** It matches its own source exactly.
But that source does not reproduce the printed 1894 page in every detail:

1. **No accents, breathings, capitals, punctuation, or elision marks.** Elided words appear
   without the apostrophe, e.g. `απ` for ἀπ᾿ and `δι` for δι᾿.
2. **Movable nu appears to be regularized.** Robinson's file has words like εγεννησεν
   before consonants throughout. Scrivener's printed Greek, checked in the OCR of his
   1882 *Parallel New Testament* on archive.org, prints ἐγέννησε τὸν, παρέλαβε τὴν,
   καλέσουσι τὸ, ἔτεκε τὸν, ἠκρίβωσε παρ᾿. An independent accented TR shows the same
   pattern in about 2,000 verses. That TR is eBible.org's *grctr*, which follows
   Stephanus 1550. These are spelling differences, not differences in wording. Only a
   carefully proofread digitization of the printed edition could fix them reliably.
   Rule-based removal would introduce new errors.

**Cross-check against a second TR.** eBible.org's accented `grctr` text was compared
verse by verse as an independent witness. Apart from spelling, it differs in 151
verses. The ones examined fit the known differences between Stephanus 1550 and Scrivener
1894: Ναζαρέτ/Ναζαρέθ, Rev 16:5 ὅσιος/ἐσόμενος, and the subscriptions added after the
Pauline letters. The least obvious readings were checked against the OCR of Scrivener's
printed Greek. All of them support our text: Heb 6:10 ἐνδείξασθε, Col 2:13
συνεζωοποίησε, 1 Thess 1:9 ἔσχομεν, Acts 27:29 ἐκπέσωμεν. Not all 151 verses have been
checked one by one against a page image.
