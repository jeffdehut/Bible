# The Bible in Its Original Languages

A working library of the full Bible in Hebrew, Aramaic, and Greek: the Old Testament from the
Leningrad Codex and the New Testament from the Greek Textus Receptus. The texts are organized
one verse per line so they're easy to read, search, and build tools on.

| | Books | Chapters | Verses | Language | Base text |
|---|---|---|---|---|---|
| Old Testament | 39 | 929 | 23,213 | Hebrew (some Aramaic) | Leningrad Codex: UXLC 2.6, fully pointed with accents |
| New Testament | 27 | 260 | 7,957 | Koine Greek | Textus Receptus (Scrivener 1894), unaccented |

## Layout

```
books.json                     Index of all 66 books: number, OSIS id, name, language,
                               chapter/verse counts, file paths, Tanakh order
text/
  hebrew/01-genesis.tsv ...    Old Testament, Unicode Hebrew
  greek/40-matthew.tsv ...     New Testament, Unicode Greek
sources/
  hebrew-uxlc/                 Official UXLC 2.6 text files, byte for byte (renamed only)
  greek-tr-scrivener/          Robinson's Scrivener 1894 transliteration (renamed only)
scripts/
  books.py                     Canonical book list, Tanakh order, Aramaic passages
  build.py                     Regenerates text/ and books.json from sources/
  verify.py                    Checks every verse against the published reference editions
VERIFICATION.md                What was checked, what was found, what was fixed
```

Files are numbered 01–66 in the common English book order. Hebrew Bibles use a different
order (Torah, Prophets, Writings). That order is stored as `tanakh_order` in `books.json`.

## Text format

Each `text/` file is UTF-8, tab-separated, with a header row:

```
chapter	verse	text
1	1	בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃
```

The files open directly in a spreadsheet, `pandas.read_csv(path, sep="\t")`, or any text editor.

Chapter and verse numbers follow each source's own numbering. That means Hebrew numbering
in the OT, where some verse numbers differ from English Bibles (for example, Psalm titles
are counted as verse 1, and Malachi has 3 chapters, not 4).

## Rebuilding

```
python3 scripts/build.py
```

The script uses only the Python standard library. It checks every chapter and book against
the verse counts declared in the UXLC headers, catches duplicate references, and rejects
unexpected characters in the Greek.

To check the texts against their published reference editions (needs network access):

```
python3 scripts/verify.py
```

See [VERIFICATION.md](VERIFICATION.md) for the results and known limitations.

## Notes on the sources

**Hebrew (OT).** UXLC is the Unicode/XML Leningrad Codex (UXLC 2.6, Build 27.7,
18 Oct 2026), with full vowel points and cantillation marks. It is not the Westminster
Leningrad Codex (WLC), though it descends from it. Paragraph markers (פ/ס) are kept at the
end of verses where the codex has them. Ketiv is marked `*` and qere `**`. Editorial
transcription notes appear in square brackets, e.g. `[t]` for an uncertain transcription.
Joshua 21:36–37 are marked `[X]` because they are not in the codex. VERIFICATION.md has
the full legend. Citation: *Unicode/XML Leningrad Codex: UXLC 2.6 (27.7), Tanach.us Inc.,
West Redding, CT, USA, Oct 2026.* The Aramaic passages are listed in `books.json`
(`aramaic_passages`): Gen 31:47, Jer 10:11, Dan 2:4b–7:28, Ezra 4:8–6:18 and 7:12–26.

**Greek (NT).** The source files use an ASCII transliteration (`y`=θ, `c`=χ, `q`=ψ, `w`=ω,
`h`=η, `x`=ξ, `v`=final ς). `build.py` converts it to Unicode Greek. The source has no
accents, breathings, capitals, punctuation, or elision marks, and the converted text
doesn't either. It also appears to regularize movable nu (εγεννησεν where the printed
1894 edition has ἐγέννησε before a consonant). See VERIFICATION.md.
Readings such as Acts 8:37, 1 John 5:7 (the Comma Johanneum), and Rev 16:5 "ὁ ἐσόμενος"
mark it as Scrivener's 1894 Textus Receptus. The text is Dr. Maurice Robinson's public-domain
digitization ([byztxt/greektext-scrivener](https://github.com/byztxt/greektext-scrivener)).

See [sources/README.md](sources/README.md) for the original file names.

## Ideas for next steps

- Add a critical Greek text (e.g. SBLGNT or Nestle-style) alongside the TR for comparison
- Add an accented Greek text, or morphology tagging (lemma, parsing, Strong's numbers)
- A lexicon/word-study layer keyed to verses
- A small reader app or search tool built on `books.json` + `text/`
