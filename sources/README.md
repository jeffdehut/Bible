# Raw sources

These are the upstream files, kept exactly as published, byte for byte. Only the file
names were changed, to the `NN-book-name` scheme. Don't edit them. Regenerate the Markdown
texts with `python3 scripts/build.py`, and check everything with
`python3 scripts/verify.py`.

**Why these stay `.txt` when everything else is `.md`.** Each file must stay byte-identical
to its upstream release so it can be checked mechanically. They aren't Markdown either. As
Markdown, the Hebrew ketiv/qere marks (`*`, `**`) would render as italics and bold, and the
`[t]`-style notes as links. The readable Markdown versions, with those characters escaped,
are in `text/` and `apparatus/`.

## hebrew-uxlc/

Unicode/XML Leningrad Codex (UXLC 2.6, Build 27.7, 18 Oct 2026; layout Full, content
Accents). These files are byte-identical to `TextFiles/` in
https://tanach.us/TextFiles/Tanach.txt.zip. Each verse line is `verse ׃chapter text` wrapped
in Unicode bidi control characters, and the files use CRLF line endings.

The zip originally held UXLC 2.5 (Build 27.6). It was replaced with 2.6, which corrects
113 verses. See VERIFICATION.md. The 2.5 files remain in git history.

Original names in the zip that changed in a notable way:

| Original | Now |
|---|---|
| `13 1 Samuel.md` | `09-1-samuel.txt` |
| `142 Samuel.md` (2 Samuel) | `10-2-samuel.txt` |
| `11 1 Kings.md`, `12 2 Kings.md` | `11-1-kings.txt`, `12-2-kings.txt` |
| `09 1 Chronicles.md`, `10 2 Chronicles.md` | `13-1-chronicles.txt`, `14-2-chronicles.txt` |
| `Song of Songs.md` | `22-song-of-songs.txt` |

The other books had no number, or already had the right one.

## greek-tr-scrivener/

Scrivener's 1894 Textus Receptus as digitized by Dr. Maurice A. Robinson (public domain),
one verse per line as `chapter:verse text`, in a lowercase ASCII transliteration without
accents. Every verse matches https://github.com/byztxt/greektext-scrivener word for word.
When converting to Unicode, `build.py` writes the numeral `cxv` (Rev 13:18, 666) as χξϛ,
with a stigma; every other word is converted letter by letter:

```
a b g d e z h y i k l m n x o p r s t u f c q w v
α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω ς
```

## greek-sblgnt/

The SBL Greek New Testament v1.2 (2023), edited by Michael W. Holmes. These files are
byte-identical to the official release at https://github.com/LogosBible/SBLGNT:

- `text/`: `data/sblgnt/text/<Book>.txt`. The first line is the Greek book title, then one
  line per verse: `Book c:v<TAB>text`. The text includes the apparatus markers ⸀ ⸂⸃ ⸁ ⸄⸅.
- `apparatus/`: `data/sblgntapp/text/<Book>.txt`. A `Book c:v` heading, then the variation
  units for that verse, separated by `•`.
- `LICENSE`: Creative Commons Attribution 4.0 International.

Copyright © 2010 Society of Biblical Literature and Logos Bible Software. CC BY 4.0.
