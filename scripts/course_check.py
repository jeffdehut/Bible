"""Check the lessons of The Complete Bible Story (data/course/qNN.json).

    python3 scripts/course_check.py            every quarter there is
    python3 scripts/course_check.py 3 4        quarters 3 and 4

Each lesson needs a title, passages, a key passage, points, readings and history in English and
Chinese (the same number of each), and resources from the lists below. Every reference must
name a book, chapter and verses that exist in this site's Bible (data/bible/text, the Hebrew
numbering in the Old Testament), and the key passage must be four verses or fewer.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = {b["osis"]: b for b in json.load(open(os.path.join(ROOT, "data", "bible", "books.json"), encoding="utf-8"))}
MAPS = {"western-asia", "exodus", "palestine-history", "kingdoms", "empires", "palestine", "roman-empire", "jerusalem", "atlas"}
STORIES = {"creation", "fall", "noah", "abraham", "moses", "david", "daniel", "jonah", "nativity", "ministry", "resurrection", "church"}
REF = re.compile(r"^(?P<b>[1-3]?[A-Za-z]+)\.(?P<c1>\d+)(?:\.(?P<v1>\d+))?(?:-(?:(?P<c2>\d+)\.)?(?P<e>\d+))?$")
_verses = {}


def verses(b, c):
    """The verse numbers of a chapter, in this site's numbering."""
    key = (b, c)
    if key not in _verses:
        book = json.load(open(os.path.join(ROOT, "data", "bible", "text", BOOKS[b]["slug"] + ".json"), encoding="utf-8"))
        for ch in book["chapters"]:
            _verses[(b, int(ch["c"]))] = [row[0] for row in ch["v"]]
        _verses.setdefault(key, [])
    return _verses[key]


def check_ref(ref, where, problems, key=False):
    m = REF.match(ref or "")
    if not m:
        problems.append(f"{where}: {ref!r} is not a reference like Gen.1.3-10, Gen.6-8 or Gen.29.31-30.24")
        return
    b, c1, v1, c2, e = m["b"], int(m["c1"]), m["v1"], m["c2"], m["e"]
    if b not in BOOKS:
        problems.append(f"{where}: {ref!r}: no book {b!r} (use the osis codes in data/bible/books.json)")
        return
    nch = len(BOOKS[b]["s"])
    if not 1 <= c1 <= nch:
        problems.append(f"{where}: {ref!r}: {b} has {nch} chapters")
        return
    if v1 is None:                                  # whole chapters: Gen.3 or Gen.6-8
        if e is not None and not c1 <= int(e) <= nch:
            problems.append(f"{where}: {ref!r}: chapters out of range")
        if key:
            problems.append(f"{where}: the key passage must be verses, not whole chapters")
        return
    v1 = int(v1)
    if v1 not in verses(b, c1):
        problems.append(f"{where}: {ref!r}: {b} {c1} has no verse {v1} here")
    count = 1
    if e is not None:
        c_end = int(c2) if c2 else c1
        e = int(e)
        if not c1 <= c_end <= nch or e not in verses(b, c_end):
            problems.append(f"{where}: {ref!r}: no verse {c_end}:{e} here")
        elif c_end == c1:
            if e < v1:
                problems.append(f"{where}: {ref!r}: the range runs backwards")
            count = e - v1 + 1
        else:
            count = 99
    if key and count > 4:
        problems.append(f"{where}: the key passage {ref!r} is {count} verses; four at most")


def check_text(v, where, problems, limit):
    if not isinstance(v, str) or not v.strip():
        problems.append(f"{where}: empty")
    elif len(v) > limit:
        problems.append(f"{where}: {len(v)} characters; keep it under {limit}")


def check_zh(v, where, problems):
    for bad, good in (("裡", "裏"), ("什麼", "甚麼"), ("祂", "他"), ("上帝", "神")):
        if bad in v:
            problems.append(f"{where}: {bad} (this site writes {good})")
    if re.search(r"[,;:?!]", v.replace("...", "")):
        problems.append(f"{where}: ASCII punctuation in Chinese text: {v!r}")


def pair(obj, where, problems, lo, hi, limit):
    en, zh = (obj or {}).get("en"), (obj or {}).get("zh")
    if not isinstance(en, list) or not isinstance(zh, list):
        problems.append(f"{where}: needs en and zh lists")
        return
    if not lo <= len(en) <= hi:
        problems.append(f"{where}: {len(en)} items; {lo} to {hi}")
    if len(en) != len(zh):
        problems.append(f"{where}: {len(en)} English items, {len(zh)} Chinese")
    for i, s in enumerate(en):
        check_text(s, f"{where}.en[{i}]", problems, limit)
    for i, s in enumerate(zh):
        check_text(s, f"{where}.zh[{i}]", problems, limit)
        if isinstance(s, str):
            check_zh(s, f"{where}.zh[{i}]", problems)


def check_lesson(L, where, problems):
    t = L.get("title") or {}
    check_text(t.get("en"), where + ".title.en", problems, 80)
    check_text(t.get("zh"), where + ".title.zh", problems, 40)
    if isinstance(t.get("zh"), str):
        check_zh(t["zh"], where + ".title.zh", problems)
    ps = L.get("passages")
    if not isinstance(ps, list) or not 1 <= len(ps) <= 4:
        problems.append(f"{where}.passages: one to four references")
    for i, r in enumerate(ps or []):
        check_ref(r, f"{where}.passages[{i}]", problems)
    check_ref(L.get("key"), where + ".key", problems, key=True)
    pair(L.get("points"), where + ".points", problems, 4, 7, 160)
    pair(L.get("history"), where + ".history", problems, 2, 4, 220)
    rd = L.get("readings")
    if not isinstance(rd, list) or not 2 <= len(rd) <= 4:
        problems.append(f"{where}.readings: two to four")
    for i, r in enumerate(rd or []):
        check_ref(r.get("ref"), f"{where}.readings[{i}]", problems)
        a = r.get("about") or {}
        check_text(a.get("en"), f"{where}.readings[{i}].about.en", problems, 70)
        check_text(a.get("zh"), f"{where}.readings[{i}].about.zh", problems, 35)
        if isinstance(a.get("zh"), str):
            check_zh(a["zh"], f"{where}.readings[{i}].about.zh", problems)
    for m in L.get("maps") or []:
        if m not in MAPS:
            problems.append(f"{where}.maps: unknown map {m!r}")
    f = L.get("felt")
    if f is not None:
        if "story" in f and f["story"] not in STORIES:
            problems.append(f"{where}.felt: unknown story {f['story']!r}")
        if not ("story" in f or "find" in f):
            problems.append(f"{where}.felt: needs story or find")
    con = L.get("connections")
    if con is not None and not re.match(r"^[1-3]?[A-Za-z]+\.\d+$", con):
        problems.append(f"{where}.connections: a chapter like Gen.6")
    elif con:
        check_ref(con, where + ".connections", problems)


def main():
    folder = os.path.join(ROOT, "data", "course")
    qs = [int(a) for a in sys.argv[1:]] or [int(f[1:3]) for f in sorted(os.listdir(folder)) if re.match(r"q\d\d\.json$", f)]
    total = bad = 0
    for q in qs:
        path = os.path.join(folder, f"q{q:02d}.json")
        problems = []
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as e:                      # noqa: BLE001
            print(f"q{q:02d}: {e}")
            bad += 1
            continue
        lessons = data.get("lessons", [])
        if len(lessons) != 12:
            problems.append(f"q{q:02d}: {len(lessons)} lessons; twelve")
        for i, L in enumerate(lessons):
            if L.get("n") != i + 1:
                problems.append(f"q{q:02d}: lesson {i + 1} is numbered {L.get('n')}")
            check_lesson(L, f"q{q:02d}.{i + 1}", problems)
        total += len(lessons)
        bad += len(problems)
        print(f"q{q:02d}: {len(lessons)} lessons, " + ("all good" if not problems else f"{len(problems)} problems"))
        for p in problems:
            print("  - " + p)
    print(f"{total} lessons checked, {bad} problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
