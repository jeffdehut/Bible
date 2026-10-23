# Raw sources

These are the files exactly as received in `the Bible, OG Languages.zip`. The contents are
unchanged. Only the file names were normalized to the `NN-book-name.txt` scheme. The
originals used a `.md` extension, but they are plain text, not Markdown. Don't edit these
files. Regenerate `text/` with `python3 scripts/build.py` instead.

## hebrew-uxlc/

Unicode/XML Leningrad Codex (UXLC 2.5, Build 27.6, 31 Mar 2026; layout Full, content
Accents). Each verse line is `verse ׃chapter text` wrapped in Unicode bidi control
characters, and the files use CRLF line endings.

Original names that changed in a notable way:

| Original | Now |
|---|---|
| `13 1 Samuel.md` | `09-1-samuel.txt` |
| `142 Samuel.md` (2 Samuel) | `10-2-samuel.txt` |
| `11 1 Kings.md`, `12 2 Kings.md` | `11-1-kings.txt`, `12-2-kings.txt` |
| `09 1 Chronicles.md`, `10 2 Chronicles.md` | `13-1-chronicles.txt`, `14-2-chronicles.txt` |
| `Song of Songs.md` | `22-song-of-songs.txt` |

The other books had no number, or already had the right one.

## greek-tr-scrivener/

Scrivener's 1894 Textus Receptus, one verse per line as `chapter:verse text`, in a
lowercase ASCII transliteration without accents:

```
a b g d e z h y i k l m n x o p r s t u f c q w v
α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω ς
```
