"""The names of people and places in Traditional Chinese, as the Chinese Union Version spells them.

    python3 scripts/names_zh.py        (after connections.py and maps.py)

Reads   the Chinese Union Version (Traditional, new punctuation, public domain), as USFM from
        eBible.org (downloaded once into .cache/cuv/), which marks every proper noun (\\pn);
        data/bible/people.json and data/bible/places.json: each person and place, and the verses
        that name them (Hebrew numbering in the Old Testament, turned into the English numbering
        the Union Version follows, through TVTMS); Theographic's people and places (in
        .cache/theographic/, from connections.py), which give every verse that names each one,
        where the site's own lists name a place only where a map shows it; data/graph.json for
        the names as the
        Connections page and the 3D web show them ("Abdi (1 Chronicles 6.29)")
Writes  i18n/zh-Hant.names.js   I18N.add({English name: Chinese name, ...})

How a name is found: among the proper nouns of the verses that name a person or place, the one
that is found in most of them (recall) and seldom elsewhere (precision) is its Chinese. People
and places of the same name are taken together, as the Union Version spells them alike. A name
whose verses don't settle it (one verse in a list of names) is matched by order: in such a verse,
once the names found already are set aside, the remaining English names and Chinese proper nouns
are paired in the order they come. A name still unsettled is left out, and shows in English.
Corrections go in OVERRIDES below, never in the written file.
"""

import ast
import collections
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS                                   # noqa: E402
import connections                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUV_ZIP = "https://ebible.org/Scriptures/cmn-cu89t_usfm.zip"
OUT = os.path.join(ROOT, "i18n", "zh-Hant.names.js")
# The Union Version's book codes, in our book order.
CODES = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH",
         "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS",
         "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
         "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH",
         "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
# Hand corrections: English name -> Chinese, or None to leave a name out.
OVERRIDES = {
    "God": None, "LORD": None, "Lord": None,
    "Jesus": "耶穌", "Christ": "基督", "Pharaoh": "法老", "Nebaioth": "尼拜約", "Perez": "法勒斯",
    # Found with others in every verse, so the verses can't tell them apart:
    "Simon": "西門", "Philip": "腓力", "Pilate": "彼拉多", "Galilee": "加利利", "Jordan": "約旦河",
    "Sinai": "西奈", "Huldah": "戶勒大", "Darda": "達大", "Telah": "他拉", "Heldai": "黑玳",
    "Ibhar": "益轄", "Gaddi": "迦底", "Suah": "書亞", "Shua": "書亞", "Mica": "米迦",
    "Ezrah": "以斯拉", "Elpalet": "以利法列",
}


def cuv_text():
    """{(osis, chapter, verse): [proper nouns, in order]} and {osis: book name}, from the USFM."""
    folder = os.path.join(connections.CACHE, "cuv", "usfm")
    if not os.path.isdir(folder):
        import zipfile
        z = connections.fetch(CUV_ZIP, os.path.join(connections.CACHE, "cuv", "cuv.zip"))
        zipfile.ZipFile(z).extractall(folder)
    osis_of = {code: BOOKS[i][1] for i, code in enumerate(CODES)}
    nouns, names = {}, {}
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".usfm"):
            continue
        code = fn.split("-")[1][:3]
        if code not in osis_of:
            continue
        osis, c, vs = osis_of[code], 0, []
        for line in open(os.path.join(folder, fn), encoding="utf-8-sig"):
            line = re.sub(r"\\f .*?\\f\*", "", line)      # footnotes
            if (m := re.match(r"\\toc1 (.+)", line)):
                names[osis] = m[1].strip()
            if (m := re.match(r"\\c (\d+)", line)):
                c = int(m[1])
                continue
            if (m := re.match(r"\\v (\d+)(?:-(\d+))?", line)):
                vs = list(range(int(m[1]), int(m[2] or m[1]) + 1))
            if not vs or line.startswith(("\\s", "\\r", "\\ms", "\\mt", "\\d ")):
                continue
            for n in re.findall(r"\\pn (.+?)\\pn\*", line):
                n = n.strip()
                for v in vs:
                    nouns.setdefault((osis, c, v), []).append(n)
    return nouns, names


def hebrew_numbering():
    """{(osis, English chapter, verse): (osis, Hebrew chapter, verse)} where they differ."""
    vers = connections.Versification(connections.fetch_stepbible("tvtms"), connections.load_texts())
    return dict(vers.to_hebrew)


def site_names():
    """{English name: set of (osis, chapter, verse)}, in our (Hebrew) numbering."""
    where = collections.defaultdict(set)

    def add(name, osis, cv):
        if name:
            c, v = map(int, cv.split(":"))
            where[name].add((osis, c, v))

    people = json.load(open(os.path.join(ROOT, "data", "bible", "people.json"), encoding="utf-8"))
    for osis, vs in people["verses"].items():
        for cv, ks in vs.items():
            for k in ks:
                add(people["n"][k], osis, cv)
    places = json.load(open(os.path.join(ROOT, "data", "bible", "places.json"), encoding="utf-8"))
    for osis, vs in places["verses"].items():
        for cv, entries in vs.items():
            for e in entries:
                add(e[2] if len(e) > 2 else places["places"][e[0]][1], osis, cv)
    for n in [p[1] for p in places["places"]] + people["n"]:
        if n:
            where.setdefault(n, set())
    return where


def theographic_names(heb):
    """{name: set of verses} from Theographic's people and places, which list every verse that
    names them (the site's own lists name a place only where a map shows it). Its references are
    in English numbering, turned into ours."""
    folder = os.path.join(connections.CACHE, "theographic", "json")
    load = lambda f: json.load(open(os.path.join(folder, f), encoding="utf-8"))
    ref = {}
    for r in load("verses.json"):
        b, c, v = r["fields"]["osisRef"].split(".")
        ref[r["id"]] = heb.get((b, int(c), int(v)), (b, int(c), int(v)))
    ids = lambda x: ast.literal_eval(x) if isinstance(x, str) else (x or [])
    where = collections.defaultdict(set)
    for f, keys in (("people.json", ("name",)), ("places.json", ("displayTitle", "kjvName", "esvName"))):
        for r in load(f):
            vs = {ref[i] for i in ids(r["fields"].get("verses")) if i in ref}
            for k in keys:
                if r["fields"].get(k):
                    where[r["fields"][k]] |= vs
    return where


def english_text():
    """{(osis, chapter, verse): our English text}, for the order names come in."""
    text = {}
    folder = os.path.join(ROOT, "data", "bible", "text")
    for fn in sorted(os.listdir(folder)):
        d = json.load(open(os.path.join(folder, fn), encoding="utf-8"))
        for ch in d["chapters"]:
            for row in ch["v"]:
                text[(d["osis"], int(ch["c"]), row[0])] = re.sub(r"\[\^\w+\]", "", row[1] or "")
    return text


def onset(name):
    """How an English name begins, for its sound: its first consonants ("sh", "t"), or its first
    vowel."""
    m = re.match(r"[^aeiouy]+|[aeiouy]", name.lower().replace("-", ""))
    return m[0][:2] if m else ""


def match(where, nouns):
    """The names their verses settle: {English: Chinese}, and the rest. Each proper noun is
    scored for a name by recall (the share of the name's verses that have it), squared, times a
    little of its precision (the share of its verses that are the name's: a little, as the Union
    Version gives many people one name, 雅各 for Jacob and James), times how well its first character fits the
    sound the English begins with (learned from the pairs the verses settle clearly: "H" is
    usually 哈 or 希, rarely 特), which tells apart names always found together (Huldah,
    daughter-in-law of Tikvah). A name takes its best proper noun when that is clearly ahead of
    the next; one already given to a name found in the same verses is not given again (Pedahzur,
    father of Gamaliel). The names are gone over until nothing changes."""
    df = collections.Counter(n for ns in nouns.values() for n in set(ns))
    base = {}
    for name, vs in where.items():
        cands = collections.Counter(n for key in vs for n in set(nouns.get(key, [])))
        hits = sum(1 for key in vs if nouns.get(key))
        base[name] = {n: (cnt / hits) ** 2 * (cnt / df[n]) ** 0.3 for n, cnt in cands.items() if cnt / hits >= 0.2 or len(vs) < 5}
    # The sound: first characters of the clearly settled pairs, by how the English begins.
    sound = collections.defaultdict(collections.Counter)
    for name, sc in base.items():
        top = sorted(sc.items(), key=lambda x: -x[1])
        if top and top[0][1] >= 0.5 and (len(top) == 1 or top[0][1] >= 3 * top[1][1]) and len(where[name]) >= 3:
            sound[onset(name)][top[0][0][0]] += 1
    def fit(name, n):
        c = sound.get(onset(name))
        if not c:
            return 1.0
        return 0.25 + 0.75 * (c[n[0]] + 0.5) / (max(c.values()) + 0.5)
    scores = {name: {n: sc * fit(name, n) for n, sc in cs.items()} for name, cs in base.items()}
    found, given = {}, collections.defaultdict(list)
    blocked = lambda n, name: any(where[o] & where[name] for o in given[n])
    pairs = sorted(((sc, name, n) for name, cs in scores.items() for n, sc in cs.items()), reverse=True)
    changed = True
    while changed:
        changed = False
        for sc, name, n in pairs:
            if name in found or sc < 0.1 or blocked(n, name):
                continue
            second = max((x for m, x in scores[name].items() if m != n and not blocked(m, name)), default=0)
            if sc < 1.5 * second:
                continue
            # One verse is little to go on: then the sound must fit well, and the next be far behind.
            if len(where[name]) < 2 and (fit(name, n) < 0.6 or sc < 2.5 * second):
                continue
            # A people named after a place ("Gittites") is written with 人, which the
            # Union Version doesn't mark: left to the dictionary.
            if re.search(r"(ite|ites|ians)$", name) and not n.endswith("人"):
                continue
            found[name] = n
            given[n].append(name)
            changed = True
    unsure = [name for name in where if name not in found]
    return found, unsure


def by_order(unsure, found, where, nouns, text):
    """Pair the rest verse by verse: once the names already found are set aside on both sides,
    if a verse has as many English names left as Chinese proper nouns, they pair in order. A name
    is taken when every verse that pairs it agrees."""
    at = collections.defaultdict(list)
    for name, vs in where.items():
        for key in vs:
            at[key].append(name)
    added = {}
    changed = True
    while changed:
        changed = False
        known = {**found, **added}
        votes = collections.defaultdict(collections.Counter)
        for key, names in at.items():
            left = [x for x in names if x not in known]
            if not left or key not in text:
                continue
            en = text[key]
            pos = {x: en.find(x) for x in left}
            if any(p < 0 for p in pos.values()):
                continue                       # a name not written out (a pronoun): no pairing
            done = {known[x] for x in names if x in known}
            zh = [n for n in dict.fromkeys(nouns.get(key, [])) if n not in done]
            if len(zh) != len(left):
                continue
            for x, n in zip(sorted(left, key=pos.get), zh):
                votes[x][n] += 1
        for x, v in votes.items():
            if len(v) == 1 and x in unsure:
                added[x] = next(iter(v))
                unsure.remove(x)
                changed = True
    return added


def main():
    cuv, book_names = cuv_text()
    heb = hebrew_numbering()
    nouns = {}
    for (osis, c, v), ns in cuv.items():
        nouns.setdefault(heb.get((osis, c, v), (osis, c, v)), []).extend(ns)
    where = site_names()
    for name, vs in theographic_names(heb).items():
        where[name] |= vs          # its names the site lacks too: a map or the timeline may show them
    found, unsure = match(where, nouns)
    found.update(by_order(unsure, found, where, nouns, english_text()))
    for k, v in OVERRIDES.items():
        if v is None:
            found.pop(k, None)
        else:
            found[k] = v

    # The Connections page and the 3D web tell people of one name apart by a verse:
    # "Abdi (1 Chronicles 6.29)" -> "亞伯底（歷代志上 6.29）".
    zh_book = {name: book_names[osis] for num, osis, name, t in BOOKS if osis in book_names}
    graph = json.load(open(os.path.join(ROOT, "data", "graph.json"), encoding="utf-8"))
    words = dict(found)
    for n in graph["n"]:
        m = re.fullmatch(r"(.+) \((\d? ?[A-Z][a-z]+(?: [A-Z][a-z]+)*) (\d+\.\d+)\)", n)
        if m and m[1] in found and m[2] in zh_book:
            words[n] = f"{found[m[1]]}（{zh_book[m[2]]} {m[3]}）"

    names = sorted(where)
    print(f"Names: {len(names):,}; in Chinese {sum(1 for n in names if n in found):,}; "
          f"left in English {sum(1 for n in names if n not in found):,}; with the graph's forms, {len(words):,} entries")
    import random
    random.seed(7)
    sample = random.sample(sorted(found), min(40, len(found)))
    print("  ".join(f"{k}={found[k]}" for k in sample))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("// The names of people and places in Traditional Chinese, as the Chinese Union Version\n"
                "// (public domain) spells them. Written by scripts/names_zh.py: don't edit by hand;\n"
                "// corrections go in OVERRIDES there.\n"
                "I18N.add({\n")
        for k in sorted(words):
            f.write(f"{json.dumps(k, ensure_ascii=False)}:{json.dumps(words[k], ensure_ascii=False)},\n")
        f.write("});\n")


if __name__ == "__main__":
    main()
