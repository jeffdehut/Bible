"""Shared helpers for writing the connection notes in connections/."""

import json
import os
import re

from books import BOOKS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECTIONS = [
    ("Torah", "Gen", "Deut"), ("History", "Josh", "Esth"), ("Wisdom", "Job", "Song"),
    ("Prophets", "Isa", "Mal"), ("Gospels", "Matt", "John"), ("Acts", "Acts", "Acts"),
    ("Pauline Epistles", "Rom", "Phlm"), ("General Epistles", "Heb", "Jude"),
    ("Revelation", "Rev", "Rev"),
]

BOOK = {osis: (num, name, testament) for num, osis, name, testament in BOOKS}
ORDER = [osis for _, osis, _, _ in BOOKS]


def section_of(osis):
    i = ORDER.index(osis)
    for name, first, last in SECTIONS:
        if ORDER.index(first) <= i <= ORDER.index(last):
            return name


def slug(s):
    return s.lower().replace(" ", "-")


def ref_label(osis, c, v=None, v_end=None):
    name = BOOK[osis][1]
    if v is None:
        return f"{name} {c}"
    label = f"{name} {c}:{v}"
    if v_end and v_end != (c, v):
        label += f"–{v_end[1]}" if v_end[0] == c else f"–{v_end[0]}:{v_end[1]}"
    return label


def chapter_path(osis, c):
    num, name, _ = BOOK[osis]
    return f"connections/chapters/{num:02d}-{slug(name)}/{name} {c}"


def link(path, label=None):
    """A wikilink by full path (names like "Ruth" are both a book and a person), shown
    with a short label instead of the path."""
    return f"[[{path}|{label or path.rsplit('/', 1)[-1]}]]"


def safe_filename(name):
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "-", name).strip()


def frontmatter(fields):
    out = ["---"]
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            out.append(f"{k}: [{', '.join(json.dumps(x, ensure_ascii=False) for x in v)}]")
        else:
            out.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return out + ["---", ""]


def write(path, lines):
    full = os.path.join(ROOT, path + ".md")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")

