"""Check and compile the Open Plain English Translation.

    python3 scripts/translation.py                   check everything, then compile
    python3 scripts/translation.py --check [BOOK ...]  only check (all books, or the named ones,
                                                      e.g. "genesis" or "01-genesis"); writes nothing

Reads   translation/NN-book/CCC.md   one file per translated chapter (see TRANSLATION.md)
Checks  every chapter against its source chapter in text/hebrew or text/greek:
          - one translated line for every source verse, and no others
          - every note referenced in the text is defined, and every defined note is used
          - the front matter has a known status
          - an Old Testament chapter whose Hebrew has the divine name YHWH says "LORD" (or "GOD",
            after "Lord"), and no verse writes the name "Yahweh"
Writes  text/english/NN-book.md      the translated chapters of each book, with notes
        translation/STATUS.md        progress by book and status
Exits non-zero if any check fails.
"""

import collections
import os
import re
import sys

from books import BOOKS, file_stem
from build import parse_book_md

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATION = os.path.join(ROOT, "translation")
OUT = os.path.join(ROOT, "text", "english")
STATUSES = ["draft", "checked", "reviewed", "approved"]
LICENSE_LINE = ("Open Plain English Translation. License: CC BY 4.0. "
                "New Testament translated from the SBL Greek New Testament (CC BY 4.0, © 2010 Society of "
                "Biblical Literature and Logos Bible Software); Old Testament from the Unicode/XML "
                "Leningrad Codex (UXLC 2.6, Tanach.us).")

VERSE = re.compile(r"\*\*(\d+)\*\* (.+)")
# YHWH as a whole word, with up to three one-letter prefixes (and, in, to, like, from, that).
# The maqaf joins words, so it is read as a space: Aramaic di-hawah ("who was") is not the name.
DIVINE_NAME = re.compile(r"(?<![\u05D0-\u05EA])[ובלכמש]{0,3}יהוה(?![\u05D0-\u05EA])")
# The divine name in English: "the LORD", "LORD" where God is addressed, "GOD" next to "Lord".
DIVINE_NAME_EN = re.compile(r"\b(LORD|GOD)\b")
NOTE_DEF = re.compile(r"\[\^(\w+)\]: (.+)")
NOTE_REF = re.compile(r"\[\^(\w+)\](?!:)")


def parse_chapter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.split("#")[0].strip()
        meta[key.strip()] = value
    verses, notes = {}, {}
    for line in text[m.end():].splitlines():
        if (vm := VERSE.fullmatch(line)):
            v = int(vm[1])
            if v in verses:
                raise ValueError(f"verse {v} appears twice")
            verses[v] = vm[2]
        elif (nm := NOTE_DEF.fullmatch(line)):
            notes[nm[1]] = nm[2]
        elif line.strip():
            raise ValueError(f"unexpected line: {line[:60]!r}")
    return meta, verses, notes


def main():
    args = sys.argv[1:]
    if args and args[0] != "--check":
        sys.exit(__doc__)
    check_only = bool(args)
    wanted = {a.lower() for a in args[1:]} if check_only else set()
    errors, chapters = [], collections.defaultdict(dict)
    for num, osis, name, testament in BOOKS:
        folder = os.path.join(TRANSLATION, file_stem(num, name))
        if not os.path.isdir(folder):
            continue
        if wanted and not wanted & {name.lower(), file_stem(num, name), osis.lower()}:
            continue
        src_path = os.path.join(ROOT, "text", "hebrew" if testament == "OT" else "greek", file_stem(num, name) + ".md")
        source, has_name = collections.defaultdict(set), set()
        for c, v, t in parse_book_md(src_path):
            source[c].add(v)
            if testament == "OT" and DIVINE_NAME.search(re.sub(r"[\u0591-\u05BD\u05BF-\u05C7]", "", t.replace("\u05BE", " "))):
                has_name.add(c)
        for fn in sorted(os.listdir(folder)):
            path = os.path.join(folder, fn)
            label = f"{name} {fn}"
            if not re.fullmatch(r"\d{3}\.md", fn):
                errors.append(f"{label}: file names must be three-digit chapter numbers, e.g. 001.md")
                continue
            c = int(fn[:3])
            try:
                meta, verses, notes = parse_chapter(path)
            except ValueError as e:
                errors.append(f"{label}: {e}")
                continue
            if c not in source:
                errors.append(f"{label}: {name} has no chapter {c} in the source")
                continue
            if meta.get("status") not in STATUSES:
                errors.append(f"{label}: status must be one of {', '.join(STATUSES)}")
            if meta.get("book") != name or meta.get("chapter") != str(c):
                errors.append(f"{label}: front matter book/chapter don't match the file")
            missing, extra = sorted(source[c] - set(verses)), sorted(set(verses) - source[c])
            if missing:
                errors.append(f"{label}: missing verses {missing}")
            if extra:
                errors.append(f"{label}: verses not in the source {extra}")
            used = {r for t in verses.values() for r in NOTE_REF.findall(t)}
            if used - set(notes):
                errors.append(f"{label}: undefined notes {sorted(used - set(notes))}")
            if set(notes) - used:
                errors.append(f"{label}: unused notes {sorted(set(notes) - used)}")
            if c in has_name and not any(DIVINE_NAME_EN.search(t) for t in verses.values()):
                errors.append(f"{label}: the Hebrew has the divine name YHWH, but the translation has no \"LORD\"")
            for v, t in verses.items():
                if "Yahweh" in NOTE_REF.sub("", t):
                    errors.append(f"{label}:{v}: the divine name is written \"the LORD\", not \"Yahweh\"")
            chapters[(num, osis, name, testament)][c] = (meta, verses, notes)

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    if check_only:
        print(f"{sum(len(c) for c in chapters.values())} chapters pass the checks ({len(chapters)} books).")
        return

    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    for (num, osis, name, testament), chs in chapters.items():
        lines = [f"# {name}", "", f"> **Text:** {LICENSE_LINE}  ",
                 "> Chapters show their review status: *draft*, *checked*, *reviewed* or *approved*. "
                 "See TRANSLATION.md.", ""]
        for c in sorted(chs):
            meta, verses, notes = chs[c]
            lines += [f"## Chapter {c}", "", f"*Status: {meta['status']}*", ""]
            ref = lambda m: f"[^{c}-{m[1]}]"
            for v in sorted(verses):
                lines += [f"**{v}** {NOTE_REF.sub(ref, verses[v])}", ""]
            lines += [f"[^{c}-{k}]: {t}" for k, t in sorted(notes.items(), key=lambda kv: (0, int(kv[0]), "") if kv[0].isdigit() else (1, 0, kv[0]))]
            lines.append("")
        with open(os.path.join(OUT, file_stem(num, name) + ".md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines).rstrip("\n") + "\n")

    # Status report.
    total = collections.Counter()
    rows = []
    for num, osis, name, testament in BOOKS:
        n_src = len({c for c, _, _ in parse_book_md(os.path.join(
            ROOT, "text", "hebrew" if testament == "OT" else "greek", file_stem(num, name) + ".md"))})
        chs = chapters.get((num, osis, name, testament), {})
        counts = collections.Counter(m["status"] for m, _, _ in chs.values())
        total.update(counts)
        total["chapters"] += n_src
        if chs:
            rows.append(f"| {name} | {n_src} | " + " | ".join(str(counts.get(s, 0) or "") for s in STATUSES)
                        + f" | {', '.join(str(c) for c in sorted(chs))} |")
    done = sum(total[s] for s in STATUSES)
    status = ["# Translation status", "",
              f"{done} of {total['chapters']:,} chapters translated: "
              + ", ".join(f"{total[s]} {s}" for s in STATUSES) + ".", "",
              "| Book | Chapters | Draft | Checked | Reviewed | Approved | Translated chapters |",
              "|---|---|---|---|---|---|---|"] + rows + [""]
    with open(os.path.join(TRANSLATION, "STATUS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(status))
    print(f"{done} chapters checked and compiled into text/english/ ({len(chapters)} books).")


if __name__ == "__main__":
    main()
