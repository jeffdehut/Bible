"""Check the translation against the rules of TRANSLATION.md that a script can test.

    python3 scripts/consistency.py             report every finding
    python3 scripts/consistency.py --summary   counts only

Reads   translation/NN-book/CCC.md      the translation and its notes
        text/hebrew, text/greek          the source verses
        data/bible/words/NN-book.json    each source word's Strong's number (scripts/reader.py)
Writes  translation/CONSISTENCY.md      the findings, rule by rule, for review

Each rule is one function below, named after the line of TRANSLATION.md it tests. A finding is
not always a mistake: the rules allow exceptions "by context", and the report is for a person
(or a careful reader) to decide. Rules marked "error" have no exceptions.
"""

import collections
import json
import os
import re
import sys

from books import BOOKS, file_stem
from build import parse_book_md
from translation import DIVINE_NAME, parse_chapter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATION = os.path.join(ROOT, "translation")
NT = {osis for _, osis, _, t in BOOKS if t == "NT"}
PAUL = {"Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm"}

# American spelling (TRANSLATION.md, checklist): British forms and their American spelling.
BRITISH = {
    r"honour": "honor", r"neighbour": "neighbor", r"colour": "color", r"favour": "favor", r"labour": "labor",
    r"behaviour": "behavior", r"saviour": "savior", r"splendour": "splendor", r"odour": "odor", r"vapour": "vapor",
    r"armour": "armor", r"harbour": "harbor", r"rumour": "rumor", r"valour": "valor", r"vigour": "vigor",
    r"clamour": "clamor", r"ardour": "ardor", r"judgement": "judgment", r"worshipp": "worshiped",
    r"centre": "center", r"theatre": "theater", r"metre": "meter", r"litre": "liter", r"fibre": "fiber",
    r"defence": "defense", r"offence": "offense", r"pretence": "pretense", r"grey": "gray", r"plough": "plow",
    r"jewellery": "jewelry", r"travell": "traveled", r"counsell": "counseled", r"quarrell": "quarreled",
    r"marvell": "marveled", r"cancell": "canceled", r"fulfil(?!l)": "fulfill", r"enrol(?!l)": "enroll",
    r"sceptre": "scepter", r"sepulchre": "sepulcher", r"mould": "mold", r"storey": "story",
    r"practise": "practice", r"recognis": "recognize", r"realis": "realize", r"apologis": "apologize",
    r"organis": "organize", r"baptis(?!m|t)": "baptize", r"amongst": "among", r"whilst": "while",
}
BRITISH_RE = re.compile(r"\b(?!greyhound)(" + "|".join(BRITISH) + r")\w*", re.I)


def plain(text):
    """A verse without its note markers or italics."""
    return re.sub(r"\[\^\w+\]", "", text).replace("*", "")


class Chapter:
    def __init__(self, osis, name, c, path, verses, notes, src, words, para_end):
        self.osis, self.name, self.c, self.path = osis, name, c, path
        self.verses, self.notes, self.src, self.words = verses, notes, src, words
        self.para_end = para_end   # verses that end a paragraph in the source

    def ref(self, v):
        return f"{self.name} {self.c}:{v}"

    def strongs(self, v):
        """The Strong's numbers of verse v's words (prefixes and suffixes too), as numbers."""
        out = []
        for w in (self.words.get(str(v)) or "").split("¦"):
            f = w.split("|")
            if len(f) > 2:
                out += [int(m) for m in re.findall(r"\d+", f[2])]
        return out


def load():
    chapters = []
    for num, osis, name, testament in BOOKS:
        stem = file_stem(num, name)
        folder = os.path.join(TRANSLATION, stem)
        src_path = os.path.join(ROOT, "text", "hebrew" if testament == "OT" else "greek", stem + ".md")
        src = collections.defaultdict(dict)
        for c, v, t in parse_book_md(src_path):
            src[c][v] = t
        words_path = os.path.join(ROOT, "data", "bible", "words", stem + ".json")
        words = {ch["c"]: ch["w"] for ch in json.load(open(words_path, encoding="utf-8"))["chapters"]}
        text = json.load(open(os.path.join(ROOT, "data", "bible", "text", stem + ".json"), encoding="utf-8"))
        para = {ch["c"]: {r[0] for r in ch["v"] if len(r) > 3 and (r[3] or {}).get("p")} for ch in text["chapters"]}
        for f in sorted(os.listdir(folder)):
            if not re.fullmatch(r"\d{3}\.md", f):
                continue
            c = int(f[:3])
            meta, verses, notes = parse_chapter(os.path.join(folder, f))
            chapters.append(Chapter(osis, name, c, os.path.join("translation", stem, f), verses, notes, src[c],
                                    words.get(c, {}), para.get(c, set())))
    return chapters


# ---------------------------------------------------------------- the rules

RULES = []


def rule(title, level="review"):
    def wrap(fn):
        RULES.append((fn, title, level))
        return fn
    return wrap


@rule("American spelling: “honor”, “neighbor”, “judgment”, “worshiped” (checklist, Text)", "error")
def spelling(ch):
    for v, t in ch.verses.items():
        for m in BRITISH_RE.finditer(plain(t)):
            yield v, f"“{m[0]}”"
    for k, t in ch.notes.items():
        for m in BRITISH_RE.finditer(t):
            if not re.search(r"Hebrew|Greek|King James|Textus", t[:m.start()][-60:]):
                yield None, f"note {k}: “{m[0]}”"


@rule("Dashes: unspaced em dashes, not hyphens or spaced dashes (checklist, Text)", "error")
def dashes(ch):
    for v, t in ch.verses.items():
        if re.search(r" — |\s--\s|--| - ", t):
            yield v, re.search(r".{0,20}( — |\s--\s|--| - ).{0,20}", t)[0]


@rule("Verse ranges in notes take an en dash: “1–3” (checklist, Text)", "error")
def ranges(ch):
    for k, t in ch.notes.items():
        for m in re.finditer(r"\b\d+:\d+-\d+\b|\b(?:verses?|vv\.) \d+-\d+\b", t):
            yield None, f"note {k}: “{m[0]}”"


@rule("“Yahweh” appears only in the note on Exodus 3:15 (glossary, YHWH)", "error")
def yahweh(ch):
    for v, t in ch.verses.items():
        if "Yahweh" in t:
            yield v, "Yahweh in the text"
    if not (ch.osis == "Exod" and ch.c == 3):
        for k, t in ch.notes.items():
            if re.search(r"\bYahweh\b", t):
                yield None, f"note {k}"


@rule("Every YHWH is “the LORD”, or “GOD” beside “Lord” (glossary, YHWH): a verse with fewer LORD/GOD than YHWH")
def divine_name(ch):
    if ch.osis in NT:
        return
    for v, src in ch.src.items():
        n = len(DIVINE_NAME.findall(src.replace("־", " ")))
        t = plain(ch.verses.get(v, ""))
        m = len(re.findall(r"\b(LORD|GOD)\b", t))
        if n > m:
            yield v, f"{n} YHWH, {m} LORD/GOD"


@rule("The LORD note at the first LORD in each chapter (checklist, Notes)", "error")
def lord_note(ch):
    if ch.osis in NT:
        return
    first = next((v for v in sorted(ch.verses) if re.search(r"\bLORD\b", plain(ch.verses[v]))), None)
    if first and not any("God's personal name" in t or "personal name, YHWH" in t or "name YHWH" in t for t in ch.notes.values()):
        yield first, "no note on what LORD stands for"


@rule("Notes are numbered in the order they first appear (checklist, Notes)", "error")
def note_order(ch):
    seen = []
    for v in sorted(ch.verses):
        for k in re.findall(r"\[\^(\w+)\]", ch.verses[v]):
            if k not in seen:
                seen.append(k)
    nums = [int(k) for k in seen if k.isdigit()]
    if nums != sorted(nums) or (nums and nums != list(range(1, len(nums) + 1))):
        yield None, f"order {nums[:12]}{'…' if len(nums) > 12 else ''}"


@rule("Numbers: words up to one hundred, never “eleven hundred” (checklist, Numbers)")
def numbers(ch):
    for v, t in ch.verses.items():
        p = plain(t)
        if re.search(r"\b(eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen) hundred\b", p, re.I):
            yield v, re.search(r"\w+ hundred", p, re.I)[0]
    # Small numbers in digits, in a chapter with no list of large ones.
    digits = {v: re.findall(r"(?<![\d,:–])\b\d[\d,]*\b(?![\d:])", plain(t)) for v, t in ch.verses.items()}
    big = sum(1 for ds in digits.values() for d in ds if int(d.replace(",", "")) > 100)
    if big == 0:
        for v, ds in digits.items():
            for d in ds:
                if int(d.replace(",", "")) <= 100:
                    yield v, f"“{d}” in digits"


def quote_events(verses):
    """Follow the quotation marks through a chapter's verses ({number: text}) as a stack, and
    yield (verse, kind, message): kind "reopen" where a continuing speech reopens at the start of
    a verse (a new paragraph, TRANSLATION.md), "error" for a mark that opens or closes out of turn.

    A mark opens at the start of a verse, after a space, a bracket or a dash, or right after
    another opening mark ("'I said); otherwise it closes. A single quote between letters is an
    apostrophe (father's), and one that would close when no single quote is open is a plural's
    apostrophe (brothers'). Quotes nest double, single, double."""
    stack, opened = [], None
    for v in sorted(verses):
        t = plain(verses[v])
        last_open = -2
        for m in re.finditer(r"[\"']", t):
            q, i = m[0], m.start()
            before = t[i - 1] if i else " "
            after = t[i + 1] if i + 1 < len(t) else " "
            if q == "'" and before.isalnum() and after.isalpha():
                continue
            opening = i == 0 or before in " ([—" or (before in "\"'" and last_open == i - 1)
            if q == "'" and not opening and not (stack and stack[-1] == "'"):
                continue
            if opening:
                last_open = i
                if i == 0 and stack == ['"'] and q == '"':
                    yield v, "reopen", ""
                    continue
                want = '"' if not stack or stack[-1] == "'" else "'"
                if q != want:
                    yield v, "error", f"opens with {q} inside {stack[-1] if stack else 'nothing'} (expected {want})"
                stack.append(q)
                opened = v
            elif not stack:
                yield v, "error", f"closes {q} with nothing open"
            elif stack[-1] != q:
                yield v, "error", f"closes {q} but {stack[-1]} is open (since verse {opened})"
                stack.pop()
            else:
                stack.pop()


@rule("Quotation marks nest double, single, double (checklist, Notes): a mark that opens or closes out of turn")
def quotes(ch):
    for v, kind, msg in quote_events(ch.verses):
        if kind == "error":
            yield v, msg


def has(ch, v, pattern):
    return re.search(pattern, plain(ch.verses.get(v, "")), re.I)


def note_near(ch, v, pattern):
    keys = re.findall(r"\[\^(\w+)\]", ch.verses.get(v, ""))
    return any(re.search(pattern, ch.notes.get(k, ""), re.I) for k in keys)


def word_rule(strongs, books, pattern, label, note=None):
    """Each verse with one of these source words should use this English (or explain it in a note)."""
    def check(ch):
        if books == "OT" and ch.osis in NT or books == "NT" and ch.osis not in NT:
            return
        if isinstance(books, set) and ch.osis not in books:
            return
        for v in ch.verses:
            if set(ch.strongs(v)) & strongs and not has(ch, v, pattern) and not (note and note_near(ch, v, note)):
                yield v, label
    return check


GLOSSARY = [
    ({2617}, "OT", r"faithful love", "chesed without “faithful love” (glossary)", r"chesed"),
    ({7585}, "OT", r"\bSheol\b", "Sheol without “Sheol” (glossary)", r"Sheol"),
    ({7706}, "OT", r"\bAlmighty\b", "Shaddai without “the Almighty” (glossary)", r"Shaddai"),
    ({5542}, "OT", r"\bSelah\b", "Selah missing (glossary)", None),
    ({1067}, "NT", r"\bhell\b", "gehenna without “hell” (glossary)", r"Gehenna"),
    ({86}, "NT", r"\bHades\b", "hades without “Hades” (glossary)", r"Hades"),
    ({2098}, "NT", r"good news", "euangelion without “good news” (glossary)", None),
    ({1577}, "NT", r"\bchurch(es)?\b|\bassembly\b", "ekklesia without “church” or “assembly” (glossary)", None),
    ({2665}, "NT", r"\bveil\b", "katapetasma without “veil” (glossary)", None),
]
for strongs, books, pattern, label, note in GLOSSARY:
    rule(label)(word_rule(strongs, books, pattern, label, note))


@rule("Paul's dikaioo is “declare righteous” (glossary): a verse in Paul with dikaioo but without it")
def dikaioo(ch):
    if ch.osis not in PAUL:
        return
    for v in ch.verses:
        if 1344 in ch.strongs(v) and not has(ch, v, r"declare[sd]? (\w+ )?righteous|declaring (\w+ )?righteous|righteous"):
            yield v, "dikaioo"


@rule("The LORD of Armies (glossary): YHWH tseva'ot as “hosts” or “Almighty”")
def armies(ch):
    for v, t in ch.verses.items():
        p = plain(t)
        if re.search(r"LORD (God )?of hosts|LORD Almighty|LORD God Almighty", p) and ch.osis not in NT:
            yield v, re.search(r"LORD (God )?of hosts|LORD (God )?Almighty", p)[0]


@rule("Words the glossary sets aside: “saints”, “justify”, “lovingkindness”, “Gehenna” in the text")
def old_words(ch):
    for v, t in ch.verses.items():
        p = plain(t)
        for w, why in ((r"\bsaints?\b", "saints → God's holy people"), (r"\blovingkindness\b", "lovingkindness → faithful love"),
                       (r"\bsteadfast love\b", "steadfast love → faithful love"), (r"\bGehenna\b", "Gehenna → hell"),
                       (r"\bjustif(y|ied|ies|ication)\b", "justify → declare righteous")):
            if "justify" in why and ch.osis not in NT:
                continue
            if re.search(w, p, re.I):
                yield v, why


@rule("“Truly I tell you” for amen lego humin (glossary)")
def truly(ch):
    if ch.osis not in ("Matt", "Mark", "Luke", "John"):
        return
    for v in ch.verses:
        s = ch.strongs(v)
        if 281 in s and 3004 in s and not has(ch, v, r"\btruly\b"):
            yield v, "amen without “Truly”"


@rule("The Accuser (glossary): ha-satan in Job 1–2 and Zechariah 3")
def accuser(ch):
    if (ch.osis, ch.c) in {("Job", 1), ("Job", 2), ("Zech", 3)}:
        for v, t in ch.verses.items():
            if re.search(r"\bSatan\b", plain(t)):
                yield v, "Satan"


@rule("Old Testament notes never say just “some manuscripts” (checklist, Old Testament variants)", "error")
def ot_manuscripts(ch):
    if ch.osis in NT:
        return
    for k, t in ch.notes.items():
        if re.search(r"\b[Ss]ome manuscripts\b(?! of the)", t):
            yield None, f"note {k}"


FAMOUS = {("Mark", 16), ("John", 7), ("John", 8), ("John", 1), ("1Cor", 14), ("Eph", 1), ("1John", 5)}


@rule("New Testament notes don't claim “the earliest manuscripts”, except in the famous passages (checklist, Notes)")
def earliest(ch):
    if ch.osis not in NT or (ch.osis, ch.c) in FAMOUS:
        return
    for k, t in ch.notes.items():
        if re.search(r"(earliest|oldest|best) (\w+ )?manuscripts", t, re.I):
            yield None, f"note {k}"


@rule("Notes explain, they don't preach (checklist, Notes): devotional words in notes")
def preaching(ch):
    for k, t in ch.notes.items():
        if re.search(r"\b(we should|we must|believers today|our lives|applies to us|reminds us|teaches us)\b", t, re.I):
            yield None, f"note {k}: {t[:80]}"


# Findings a person has reviewed and kept: (book, chapter, verse or None, rule function), each
# with the reason.
REVIEWED = {
    ("Esth", 2, 17, "check"): "chesed of the king's favor to Esther: \"grace and favor\" by context",
    ("Rom", 3, 4, "dikaioo"): "Psalm 51:6 quoted: \"proved right\", outside Paul's argument, noted",
    ("Rom", 6, 7, "dikaioo"): "\"set free from sin\": the sense here, noted",
    ("1Tim", 3, 16, "dikaioo"): "\"vindicated by the Spirit\": a hymn, not Paul's argument, noted",
    ("Job", 35, None, "preaching"): "the words quoted in the note are Elihu's",
    ("John", 9, None, "preaching"): "the words quoted in the note are the verse's",
}


def main():
    summary = "--summary" in sys.argv
    chapters = load()
    out = ["# Consistency report", "",
           "Findings of `scripts/consistency.py`: the rules of TRANSLATION.md that a script can test, "
           "checked against every chapter. Rules marked **error** have no exceptions; the others allow "
           "exceptions “by context”, so each finding needs a look.", ""]
    totals = []
    for fn, title, level in RULES:
        found = [(ch, v, msg) for ch in chapters for v, msg in fn(ch)
                 if (ch.osis, ch.c, v, fn.__name__) not in REVIEWED]
        totals.append((title, level, len(found)))
        out += [f"## {title}" + (" (error)" if level == "error" else ""), "", f"{len(found)} found.", ""]
        for ch, v, msg in found[:400]:
            where = ch.ref(v) if v else f"{ch.name} {ch.c}"
            out.append(f"- {where}: {msg}")
        if len(found) > 400:
            out.append(f"- … and {len(found) - 400} more")
        out.append("")
    with open(os.path.join(TRANSLATION, "CONSISTENCY.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    for title, level, n in totals:
        print(f"{n:6d}  {'ERROR ' if level == 'error' and n else '      '}{title}")
    if not summary:
        print("Written translation/CONSISTENCY.md")


if __name__ == "__main__":
    main()
