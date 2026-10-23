# The Bible in Its Original Languages

A working library of the full Bible in Hebrew, Aramaic, and Greek: the Old Testament from the
Leningrad Codex and the New Testament from the Greek Textus Receptus. The texts are organized
one verse per line so they're easy to read, search, and build tools on.

| | Books | Chapters | Verses | Language | Base text |
|---|---|---|---|---|---|
| Old Testament | 39 | 929 | 23,213 | Hebrew (some Aramaic) | Leningrad Codex: UXLC 2.5, fully pointed with accents |
| New Testament | 27 | 260 | 7,957 | Koine Greek | Textus Receptus (Scrivener 1894), unaccented |

## Layout

```
books.json                     Index of all 66 books: number, OSIS id, name, language,
                               chapter/verse counts, file paths, Tanakh order
text/
  hebrew/01-genesis.tsv ...    Old Testament, Unicode Hebrew
  greek/40-matthew.tsv ...     New Testament, Unicode Greek
sources/
  hebrew-uxlc/                 Raw source files as received (renamed only)
  greek-tr-scrivener/
scripts/
  books.py                     Canonical book list, Tanakh order, Aramaic passages
  build.py                     Regenerates text/ and books.json from sources/
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

## Notes on the sources

**Hebrew (OT).** UXLC is the Unicode/XML Leningrad Codex (Build 27.6, 31 Mar 2026), with
full vowel points and cantillation marks. Paragraph markers (פ/ס) are kept at the end of
verses where the codex has them. The Aramaic passages are listed in `books.json`
(`aramaic_passages`): Gen 31:47, Jer 10:11, Dan 2:4b–7:28, Ezra 4:8–6:18 and 7:12–26.

**Greek (NT).** The source files use an ASCII transliteration (`y`=θ, `c`=χ, `q`=ψ, `w`=ω,
`h`=η, `x`=ξ, `v`=final ς). `build.py` converts it to Unicode Greek. The source has no
accents, breathings, capitals, or punctuation, and the converted text doesn't either.
Readings such as Acts 8:37, 1 John 5:7 (the Comma Johanneum), and Rev 16:5 "ὁ ἐσόμενος"
mark it as Scrivener's 1894 Textus Receptus.

See [sources/README.md](sources/README.md) for the original file names.

## Ideas for next steps

- Add a critical Greek text (e.g. SBLGNT or Nestle-style) alongside the TR for comparison
- Add an accented Greek text, or morphology tagging (lemma, parsing, Strong's numbers)
- A lexicon/word-study layer keyed to verses
- A small reader app or search tool built on `books.json` + `text/`
