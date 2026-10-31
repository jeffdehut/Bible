"""The Visual Bible: a page for each book, made from the book's own words, and the page that
gathers them (visual/index.html).

    python3 scripts/visual.py            (after reader.py and wisdom.py)

Reads   data/bible/books.json, data/bible/text/ (our English) and data/bible/words/ (each word of
        the Hebrew and Greek with its Strong's number and grammar), and data/books-about.json (who
        wrote each book, when, to whom, the kind of writing and its theme, as introductions to the
        Bible commonly give them, with the debated dates marked)
Writes  visual/index.html               every book of the Bible, and the ones with pages
        visual/<book>.html               a page for every book: 1, 2 and 3 John from
                                         scripts/templates/visual-letters.html, the rest from
                                         scripts/templates/visual-book.html (Psalms and Proverbs
                                         keep their own pages). A book's words are those it uses
                                         far more than the rest of its Testament (log-likelihood),
                                         its formulas are runs of words (FORMULAS), and its links
                                         are OpenBible.info's cross-references.

Nothing here is commentary: every chart counts the book's own words, by their Strong's numbers,
or the grammar of its verbs, and every mark leads to its verse. The themes are lists of
Strong's numbers (THEMES); a sentence pattern is a run of words in the Greek (PATTERNS).
"""

import collections
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webpages                                  # noqa: E402
import connections                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
TEMPLATES = os.path.join(ROOT, "scripts", "templates")
OUT = os.path.join(ROOT, "visual")
# Who wrote each book, when, to whom, what kind of writing, its theme (data/books-about.json).
ABOUT = {k: v for k, v in json.load(open(os.path.join(ROOT, "data", "books-about.json"), encoding="utf-8")).items() if not k.startswith("_")}

# The pages there are: book slug -> page (relative to visual/).
PAGES = {"19-psalms": "../psalms.html", "20-proverbs": "../proverbs.html",
         "62-1-john": "1-john.html", "63-2-john": "2-john.html", "64-3-john": "3-john.html"}

# Words that run through John's letters, each a set of Strong's numbers.
THEMES = [
    ("love", "Love", "#d4495a", {25, 26}),
    ("know", "Know", "#2e86c1", {1097, 1492, 6063}),
    ("abide", "Abide, remain", "#16a085", {3306}),
    ("truth", "Truth, true", "#7d3c98", {225, 227, 228}),
    ("lie", "Lie, liar", "#6e2c00", {5574, 5579, 5583}),
    ("light", "Light", "#d4a017", {5457}),
    ("dark", "Darkness", "#34495e", {4653, 4655}),
    ("sin", "Sin", "#a04000", {264, 266}),
    ("world", "World", "#5d6d7e", {2889}),
    ("life", "Life", "#27ae60", {2222, 2198}),
    ("command", "Command", "#b9770e", {1785, 1781}),
    ("witness", "Witness, testify", "#1f618d", {3140, 3141}),
    ("born", "Born of God", "#c0392b", {1080}),
    ("children", "Children", "#e67e22", {5040, 5043, 3813}),
    ("walk", "Walk", "#117a65", {4043}),
    ("fellowship", "Fellowship", "#884ea0", {2842}),
    ("hate", "Hate", "#566573", {3404}),
    ("antichrist", "Antichrist, deceiver", "#7b241c", {500, 4108}),
    ("confess", "Confess", "#2874a6", {3670}),
    ("spirit", "Spirit", "#148f77", {4151}),
]
# Opposites the letters set side by side.
PAIRS = [("light", "dark"), ("truth", "lie"), ("love", "hate"), ("life", "world")]
# Sentence patterns: (id, label, test on the verse's words). Each word is (strong, grammar).
PATTERNS = [
    ("ifwesay", "“If we say …”", lambda ws: seq(ws, [1437, (2036, "1P")])),
    ("whosays", "“Whoever says …”", lambda ws: seq(ws, [3588, (3004, "PAP")])),
    ("bythis", "“By this we know …”", lambda ws: near(ws, [1722, 3778, (1097, "")], 4)),
    ("everyone", "“Everyone who …”", lambda ws: seq(ws, [3956, 3588, ("*", "P-NSM")])),
    ("iwrite", "“I write …”, “I wrote …”", lambda ws: any(s == 1125 and g.endswith("1S") for s, g in ws)),
    ("weknow", "“We know …”", lambda ws: any(s in (1097, 1492, 6063) and g.endswith("1P") for s, g in ws)),
]
# How the letters speak to their readers.
ADDRESS = [
    ("teknia", "“Little children” (teknia)", {5040}, "V"),
    ("paidia", "“Children” (paidia)", {3813}, "V"),
    ("agapetoi", "“Beloved” (agapētoi)", {27}, "V"),
    ("pateres", "“Fathers”", {3962}, "V"),
    ("neaniskoi", "“Young men”", {3495}, "V"),
]
# People and groups named in the short letters.
PEOPLE = [
    ("elder", "The elder", {4245}), ("lady", "The chosen lady", {2959}), ("children", "Children", {5043}),
    ("gaius", "Gaius", {1050}), ("diotrephes", "Diotrephes", {1361}), ("demetrius", "Demetrius", {1216}),
    ("brothers", "The brothers", {80}), ("strangers", "Strangers", {3581}), ("friends", "The friends", {5384}),
    ("deceivers", "Deceivers", {4108}), ("church", "The church", {1577}),
]
# Little words left out when the letters are compared: articles, conjunctions, pronouns, "to be".
COMMON = {3588, 2532, 846, 1510, 1722, 3756, 3754, 3778, 1537, 4771, 3739, 2443, 3361, 575, 1161, 4012, 1519,
          4314, 3326, 1565, 1063, 235, 3165, 1473, 2249, 5210, 1438, 3739, 3745, 3767, 1487, 1437, 5100, 3956,
          2531, 1223, 1909, 3844, 3762, 3367, 5613, 2228, 3303, 3364, 3756, 1063, 2192}


def num(strong):
    m = re.match(r"\d+", strong)
    return int(m.group()) if m else 0


def seq(ws, want):
    """Words in a row: each item a Strong's number, or (number or "*", grammar fragment)."""
    for i in range(len(ws) - len(want) + 1):
        ok = True
        for (s, g), w in zip(ws[i:i + len(want)], want):
            n, frag = (w, "") if isinstance(w, int) else w
            if (n != "*" and s != n) or (frag and frag not in g):
                ok = False
                break
        if ok:
            return True
    return False


def near(ws, want, span):
    """The words in order, within a few words of one another."""
    for i, (s, g) in enumerate(ws):
        if s != want[0]:
            continue
        j, k = i, 1
        while k < len(want) and j < min(len(ws), i + span + 2):
            j += 1
            if j < len(ws):
                n, frag = (want[k], "") if isinstance(want[k], int) else want[k]
                if ws[j][0] == n and frag in ws[j][1]:
                    k += 1
        if k == len(want):
            return True
    return False


def plain(text):
    return re.sub(r"\[\^\w+\]", "", text or "").replace("*", "").strip()


def load(stem):
    text = json.load(open(os.path.join(DATA, "text", stem + ".json"), encoding="utf-8"))
    words = json.load(open(os.path.join(DATA, "words", stem + ".json"), encoding="utf-8"))
    verses = []
    for ch, wch in zip(text["chapters"], words["chapters"]):
        c = int(ch["c"])
        for row in ch["v"]:
            raw = wch["w"].get(str(row[0]), "")
            ws, gl = [], []
            for t in raw.split("¦") if raw else []:
                p = t.split("|")
                if len(p) >= 4:
                    ws.append((num(p[2]), p[3]))
                    gl.append(p[1])
            verses.append({"c": c, "v": row[0], "t": plain(row[1]), "ws": ws, "gl": gl})
    return verses


def rates(themes):
    """Each theme per 1,000 words: in the Gospel of John, and in the rest of the New Testament."""
    books = json.load(open(os.path.join(DATA, "books.json"), encoding="utf-8"))
    counts = {"john": collections.Counter(), "nt": collections.Counter()}
    totals = collections.Counter()
    for b in books:
        if b["t"] != "NT":
            continue
        key = "john" if b["osis"] == "John" else None if b["osis"] in ("1John", "2John", "3John") else "nt"
        if not key:
            continue
        for v in load(b["slug"]):
            totals[key] += len(v["ws"])
            for s, _ in v["ws"]:
                for tid, _, _, nums in themes:
                    if s in nums:
                        counts[key][tid] += 1
    return {k: {tid: round(1000 * counts[k][tid] / totals[k], 2) for tid, *_ in themes} for k in counts}


def voices(ws):
    """Who the verbs and pronouns speak of: I, we, you, they (he, she, it)."""
    out = collections.Counter()
    for _, g in ws:
        m = re.search(r"-(1|2|3)([SP])$", g) or re.search(r"^P-(1|2)[NGDA]([SP])", g)
        if not m:
            continue
        person, number = m.groups()
        out[{"1S": "I", "1P": "we", "2S": "you", "2P": "you", "3S": "they", "3P": "they"}[person + number]] += 1
    return out


def book_data(stem, name, osis, others, nt_rates):
    verses = load(stem)
    total = sum(len(v["ws"]) for v in verses)
    out = {"book": name, "slug": stem, "osis": osis, "words": total, "verses": [], "themes": [], "patterns": [],
           "address": [], "people": [], "pairs": [list(p) for p in PAIRS], "links": []}
    tcount = collections.Counter()
    for v in verses:
        th = collections.Counter()
        for s, g in v["ws"]:
            for tid, _, _, nums in THEMES:
                if s in nums:
                    th[tid] += 1
        tcount.update(th)
        vo = voices(v["ws"])
        out["verses"].append({"c": v["c"], "v": v["v"], "t": v["t"], "th": dict(th), "vo": dict(vo)})
    for tid, label, color, nums in THEMES:
        if tcount[tid]:
            out["themes"].append({"id": tid, "n": label, "c": color, "k": tcount[tid],
                                  "r": round(1000 * tcount[tid] / total, 2), "john": nt_rates["john"][tid], "nt": nt_rates["nt"][tid]})
    out["themes"].sort(key=lambda t: -t["k"])
    for pid, label, test in PATTERNS:
        hits = [[v["c"], v["v"]] for v in verses if test(v["ws"])]
        if hits:
            out["patterns"].append({"id": pid, "n": label, "h": hits})
    # Why it says it was written, in its own words: "I write ... so that ..." (hina).
    out["purpose"] = [[v["c"], v["v"]] for v in verses
                      if any(s == 1125 and g.endswith("1S") for s, g in v["ws"]) and any(s == 2443 for s, _ in v["ws"])]
    for aid, label, nums, case in ADDRESS:
        hits = [[v["c"], v["v"]] for v in verses if any(s in nums and re.search(r"-V[SP]", g) for s, g in v["ws"])]
        if hits:
            out["address"].append({"id": aid, "n": label, "h": hits})
    for pid, label, nums in PEOPLE:
        hits = [[v["c"], v["v"]] for v in verses if any(s in nums for s, _ in v["ws"])]
        if hits:
            out["people"].append({"id": pid, "n": label, "h": hits})
    # The sister letters: verses that share words of substance (not the little words).
    def lemmas(v):
        return {s: g for (s, _), g in zip(v["ws"], v["gl"]) if s not in COMMON and s}
    mine = [lemmas(v) for v in verses]
    for oname, ostem in others:
        theirs = load(ostem)
        links = []
        for i, a in enumerate(mine):
            for j, ov in enumerate(theirs):
                shared = set(a) & set(lemmas(ov))
                if len(shared) >= 2:
                    links.append([verses[i]["c"], verses[i]["v"], ov["c"], ov["v"], sorted({re.sub(r"[\[\]<>—,.;:]", "", a[s]).strip() for s in shared})[:6]])
        out["links"].append({"book": oname, "slug": ostem, "verses": [{"c": v["c"], "v": v["v"], "t": v["t"]} for v in theirs], "l": links})
    return out


# ---------- Every other book: one engine, the same sections, each book's own data ----------
# Little words in Hebrew left out of a book's words: the object marker, prepositions, particles,
# pronouns, "to be", "say", "all", "not", "this".
HEB_COMMON = {853, 834, 3588, 3605, 3808, 413, 5921, 4480, 1961, 559, 2088, 1931, 589, 859, 1992, 3651, 518, 5973, 854,
              3541, 408, 1571, 637, 176, 6258, 8033, 3605, 2063, 428, 1768, 1836, 1459, 3809, 5922, 4481, 1934, 3606,
              5704, 8478, 3966, 3602, 3644, 4100, 4310, 3117, 6440, 1697, 3027, 5869, 7200, 935, 3318, 1980, 5414, 6213,
              7725, 3947, 3427, 7971, 6965, 5975, 1004, 376, 802, 1121, 1323, 251, 1, 5650, 4428}
GRK_COMMON = COMMON | {3004, 2036, 1096, 4160, 2064, 2983, 1325, 3708, 1492, 191, 2192, 444, 3778, 3762, 5207, 2316}
PALETTE = ["#d4495a", "#2e86c1", "#16a085", "#7d3c98", "#d4a017", "#a04000", "#27ae60", "#b9770e", "#1f618d", "#c0392b", "#5d6d7e", "#884ea0"]
# Formulas a book may come back to: (label, testament, test on the verse's words [(number, grammar)]).
FORMULAS = [
    ("“Thus says the LORD”", "OT", lambda ws: seq(ws, [3541, 559, 3068])),
    ("“declares the LORD”", "OT", lambda ws: seq(ws, [5002, 3068])),
    ("“The word of the LORD came”", "OT", lambda ws: near(ws, [1961, 1697, 3068], 2)),
    ("“Then you will know that I am the LORD”", "OT", lambda ws: any(s == 3045 for s, _ in ws) and seq(ws, [3588, 589, 3068])),
    ("“did what was evil in the eyes of the LORD”", "OT", lambda ws: seq(ws, [7451, 5869, 3068])),
    ("“the LORD of Armies”", "OT", lambda ws: seq(ws, [3068, 6635])),
    ("“the day of the LORD”", "OT", lambda ws: seq(ws, [3117, 3068])),
    ("“his faithful love endures forever”", "OT", lambda ws: seq(ws, [5769, 2617])),
    ("“As surely as the LORD lives”", "OT", lambda ws: seq(ws, [2416, 3068])),
    ("“These are the generations of …”", "OT", lambda ws: any(s == 8435 for s, _ in ws)),
    ("“Do not be afraid”", "OT", lambda ws: seq(ws, [408, (3372, "")])),
    ("“Woe …”", "OT", lambda ws: any(s in (1945, 188) for s, _ in ws)),
    ("“And it came to pass …”", "OT", lambda ws: bool(ws) and ws[0][0] == 1961 and "w3ms" in ws[0][1]),
    ("“Selah”", "OT", lambda ws: any(s == 5542 for s, _ in ws)),
    ("“Truly I tell you”", "NT", lambda ws: seq(ws, [281, (3004, "1S")])),
    ("“It is written”", "NT", lambda ws: any(s == 1125 and "RPI-3S" in g for s, g in ws)),
    ("“the kingdom of God”", "NT", lambda ws: near(ws, [932, 2316], 2)),
    ("“the kingdom of heaven”", "NT", lambda ws: near(ws, [932, 3772], 2)),
    ("“the Son of Man”", "NT", lambda ws: seq(ws, [5207, 3588, 444])),
    ("“I am …” (egō eimi)", "NT", lambda ws: seq(ws, [1473, (1510, "1S")])),
    ("“in Christ”", "NT", lambda ws: near(ws, [1722, 5547], 2)),
    ("“Grace and peace”", "NT", lambda ws: near(ws, [5485, 1515], 3)),
    ("“Do not be afraid”", "NT", lambda ws: seq(ws, [3361, (5399, "")])),
    ("“Woe …”", "NT", lambda ws: any(s == 3759 for s, _ in ws)),
    ("“the word of God”", "NT", lambda ws: near(ws, [3056, 2316], 2)),
    ("“We know …”", "NT", lambda ws: any(s in (1097, 1492, 6063) and g.endswith("1P") for s, g in ws)),
]
HEB_VOICE = [re.compile(r"^V[a-zA-Z][a-z]([123])[mfbc]([sp])"), re.compile(r"^S[ph]?([123])[mfbc]([sp])"), re.compile(r"^Pp([123])[mfbc]([sp])")]
PERSON = {"1s": "I", "1p": "we", "2s": "you", "2p": "you", "3s": "they", "3p": "they"}
_LEX = {}
# A few of the lexicon's short glosses, in plainer English.
GLOSS_FIX = {"to workout": "to work out", "to pay respects to": "to greet", "the man": "man", "an age": "age", "a people": "people", "Water": "water", "River": "river"}


def lex(lang):
    """Each Strong's entry's short English gloss and part of speech: {"7704G": ("land", "H:N-M")}."""
    if lang not in _LEX:
        out = {}
        for path in sorted(glob.glob(os.path.join(DATA, "lexicon", lang + "*.json"))):
            for key, row in json.load(open(path, encoding="utf-8")).items():
                gloss = re.split(r"[:/;,(]", row[3])[0].strip()
                gloss = GLOSS_FIX.get(gloss, gloss)
                out[key] = (gloss, row[2])
        _LEX[lang] = out
    return _LEX[lang]


def load_any(stem, ot):
    """A book's verses: each with its words as (number, grammar), the Hebrew's prefixes left out."""
    text = json.load(open(os.path.join(DATA, "text", stem + ".json"), encoding="utf-8"))
    words = json.load(open(os.path.join(DATA, "words", stem + ".json"), encoding="utf-8"))
    verses = []
    for ch, wch in zip(text["chapters"], words["chapters"]):
        for row in ch["v"]:
            raw = wch["w"].get(str(row[0]), "")
            ws, ks, voices = [], [], collections.Counter()
            for t in raw.split("¦") if raw else []:
                p = t.split("|")
                if len(p) < 4:
                    continue
                if ot:
                    nums, parts = p[2].split("/"), re.sub(r"^[HA]", "", p[3]).split("/")
                    for i, part in enumerate(parts):
                        for rx in HEB_VOICE:
                            m = rx.match(part)
                            if m:
                                voices[PERSON[m.group(1) + m.group(2)]] += 1
                                break
                    for i, n in enumerate(nums):
                        if 0 < num(n) < 9000:
                            ws.append((num(n), parts[i] if i < len(parts) else ""))
                            ks.append(n)
                else:
                    ws.append((num(p[2]), p[3]))
                    ks.append(p[2])
                    voices.update(voices_of(p[3]))
            verses.append({"c": int(ch["c"]), "v": row[0], "t": plain(row[1]), "ws": ws, "ks": ks, "vo": voices})
    return verses


def voices_of(g):
    m = re.search(r"-(1|2|3)([SP])$", g) or re.search(r"^P-(1|2)[NGDA]([SP])", g)
    return {PERSON[m.group(1) + m.group(2).lower()]: 1} if m else {}


def cross_references():
    """{(book, chapter): Counter of the books its verses point to}, from OpenBible.info."""
    path = connections.fetch_openbible()
    out = collections.defaultdict(collections.Counter)
    for line in open(path, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) < 3 or not p[2].lstrip("-").isdigit() or int(p[2]) < 5:
            continue
        a, b = p[0].split("."), p[1].split("-")[0].split(".")
        out[(a[0], int(a[1]))][b[0]] += 1
    return out


def generic_data(book, all_books, totals, xrefs, nearest):
    osis, stem, name, ot = book["osis"], book["slug"], book["n"], book["t"] == "OT"
    verses = BOOKV[stem]
    lexicon = lex("h" if ot else "g")
    common = HEB_COMMON if ot else GRK_COMMON
    chapters = sorted({v["c"] for v in verses})
    by_chapter = len(chapters) > 1
    unit = (lambda v: v["c"]) if by_chapter else (lambda v: v["v"])
    units = chapters if by_chapter else [v["v"] for v in verses]
    count = collections.Counter(k for v in verses for k in v["ks"])
    total = sum(len(v["ws"]) for v in verses) or 1
    rest = totals["ot" if ot else "nt"]
    rest_total = sum(rest.values()) - total
    # The book's words: those it uses far more than the rest of its Testament (log-likelihood).
    scored = []
    for s, a in count.items():
        gloss, pos = lexicon.get(s, ("", ""))
        if num(s) in common or not gloss or a < max(3, total // 4000) or not re.match(r"[HAG]:(N|V|A)\b", pos):
            continue
        b = rest[s] - a
        e1 = total * (a + b) / (total + rest_total)
        e2 = rest_total * (a + b) / (total + rest_total)
        if a <= e1:
            continue
        g2 = 2 * (a * math.log(a / e1) + (b * math.log(b / e2) if b else 0))
        scored.append((g2, s))
    scored.sort(reverse=True)
    themes = []
    for i, (_, s) in enumerate(scored[:12]):
        per = collections.Counter(unit(v) for v in verses for k in v["ks"] if k == s)
        hits = [[v["c"], v["v"]] for v in verses if s in v["ks"]]
        themes.append({"id": s, "n": lexicon[s][0], "c": PALETTE[i % len(PALETTE)], "k": count[s], "h": hits,
                       "r": round(1000 * count[s] / total, 2), "rest": round(1000 * (rest[s] - count[s]) / rest_total, 2),
                       "by": [per.get(u, 0) for u in units]})
    unit_words = collections.Counter()
    vo = collections.defaultdict(collections.Counter)
    for v in verses:
        unit_words[unit(v)] += len(v["ws"])
        vo[unit(v)].update(v["vo"])
    # People and places, from the site's own lists.
    people, places = [], []
    pv = PEOPLE_DATA["verses"].get(osis, {})
    pc = collections.Counter()
    ph = collections.defaultdict(list)
    for ref, ids in pv.items():
        c, v = map(int, ref.split(":"))
        for k in set(ids):
            pc[k] += 1
            ph[k].append([c, v])
    for k, n in pc.most_common(10):
        people.append({"n": re.sub(r" \(.*\)$", "", PEOPLE_DATA["n"][k]), "k": n, "h": sorted(ph[k])})
    lv = PLACES_DATA["verses"].get(osis, {})
    lc = collections.Counter()
    lh = collections.defaultdict(list)
    for ref, hits in lv.items():
        c, v = map(int, ref.split(":"))
        for k in {h[0] for h in hits}:
            lc[k] += 1
            lh[k].append([c, v])
    for k, n in lc.most_common(8):
        places.append({"n": PLACES_DATA["places"][k][1], "k": n, "h": sorted(lh[k])})
    # Its formulas.
    patterns = []
    seen = set()
    for label, testament, test in FORMULAS:
        if (testament == "OT") != ot or label in seen:
            continue
        hits = [[v["c"], v["v"]] for v in verses if test(v["ws"])]
        if len(hits) >= (3 if len(verses) > 150 else 2):
            seen.add(label)
            patterns.append({"n": label, "h": hits})
    patterns.sort(key=lambda p: -len(p["h"]))
    purpose = [[v["c"], v["v"]] for v in verses if not ot and any(s == 1125 for s, _ in v["ws"]) and any(s == 2443 for s, _ in v["ws"])]
    # Cross-references: the books it points to most (itself aside).
    linked = collections.Counter()
    for c in chapters:
        linked.update(xrefs.get((osis, c), {}))
    linked.pop(osis, None)
    names = {b["osis"]: b["n"] for b in all_books}
    links = [{"n": names.get(o, o), "slug": next((b["slug"] for b in all_books if b["osis"] == o), ""), "k": k} for o, k in linked.most_common(8)]
    text = {f'{v["c"]}:{v["v"]}': v["t"] for v in verses}
    quotes = {r: text[r] for r in {f"{c}:{v}" for c, v in purpose} | {f'{verses[0]["c"]}:{verses[0]["v"]}', f'{verses[-1]["c"]}:{verses[-1]["v"]}'}}
    return {"book": name, "slug": stem, "osis": osis, "t": book["t"], "chapters": len(chapters), "verses": len(verses), "words": total,
            "unit": "chapter" if by_chapter else "verse", "units": units,
            "vc": [sum(1 for v in verses if v["c"] == c) for c in chapters], "uw": [unit_words[u] for u in units],
            "vo": [dict(vo[u]) for u in units], "themes": themes, "people": people, "places": places,
            "patterns": patterns, "purpose": purpose, "links": links, "near": nearest.get(osis, []),
            "first": [verses[0]["c"], verses[0]["v"]], "last": [verses[-1]["c"], verses[-1]["v"]], "quotes": quotes,
            "about": ABOUT.get(osis)}


BOOKV, PEOPLE_DATA, PLACES_DATA = {}, {}, {}


def build_all(books):
    """Pages for every book that has none of its own."""
    global PEOPLE_DATA, PLACES_DATA
    PEOPLE_DATA = json.load(open(os.path.join(DATA, "people.json"), encoding="utf-8"))
    PLACES_DATA = json.load(open(os.path.join(DATA, "places.json"), encoding="utf-8"))
    totals = {"ot": collections.Counter(), "nt": collections.Counter()}
    for b in books:
        BOOKV[b["slug"]] = load_any(b["slug"], b["t"] == "OT")
        totals["ot" if b["t"] == "OT" else "nt"].update(k for v in BOOKV[b["slug"]] for k in v["ks"])
    xrefs = cross_references()
    # The books nearest in wording, within each Testament: cosine of their word rates.
    vec = {}
    for b in books:
        common = HEB_COMMON if b["t"] == "OT" else GRK_COMMON
        c = collections.Counter(k for v in BOOKV[b["slug"]] for k in v["ks"] if num(k) not in common)
        n = sum(c.values()) or 1
        vec[b["osis"]] = (b["t"], {s: k / n for s, k in c.items()})
    # Words most books share say little about which two are alike: weigh each by how few books use it.
    df = collections.Counter(s for t, v in vec.values() for s in v)
    for o, (t, v) in vec.items():
        vec[o] = (t, {s: x * math.log(len(books) / df[s]) for s, x in v.items() if df[s] < len(books)})
    nearest = {}
    for b in books:
        t, a = vec[b["osis"]]
        na = math.sqrt(sum(x * x for x in a.values())) or 1
        sims = []
        for o in books:
            if o["osis"] == b["osis"] or vec[o["osis"]][0] != t:
                continue
            bb = vec[o["osis"]][1]
            dot = sum(x * bb.get(s, 0) for s, x in a.items())
            sims.append((dot / (na * (math.sqrt(sum(x * x for x in bb.values())) or 1)), o["n"], o["slug"]))
        sims.sort(reverse=True)
        nearest[b["osis"]] = [{"n": n, "slug": s, "sim": round(x, 3)} for x, n, s in sims[:3]]
    made = {b["slug"]: b["slug"][3:] + ".html" for b in books if b["slug"] not in PAGES}
    pages = {**PAGES, **made}
    for b in books:
        if b["slug"] not in made:
            continue
        data = generic_data(b, books, totals, xrefs, nearest)
        for x in data["links"] + data["near"]:
            x["page"] = pages.get(x.pop("slug"))
        write("visual-book.html", os.path.join(OUT, made[b["slug"]]), data)
    return made


def write(template, path, data, title=None):
    src = open(os.path.join(TEMPLATES, template), encoding="utf-8").read()
    src = src.replace("<!-- APPBAR -->", webpages.appbar(os.path.relpath(path, ROOT), "../"))
    src = src.replace("<!-- DATA -->", f'<script type="application/json" id="data">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>')
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.document(src, "../"))


def main():
    os.makedirs(OUT, exist_ok=True)
    books = json.load(open(os.path.join(DATA, "books.json"), encoding="utf-8"))
    nt_rates = rates(THEMES)
    letters = [("62-1-john", "1 John", "1John"), ("63-2-john", "2 John", "2John"), ("64-3-john", "3 John", "3John")]
    for stem, name, osis in letters:
        others = [(n, s) for s, n, _ in letters if s != stem]
        data = book_data(stem, name, osis, others, nt_rates)
        data["family"] = [{"n": n, "page": PAGES[s]} for s, n, _ in letters]
        data["about"] = ABOUT.get(osis)
        write("visual-letters.html", os.path.join(OUT, PAGES[stem]), data)
        print(f"{name}: {len(data['verses'])} verses, {len(data['themes'])} themes, "
              f"{sum(len(p['h']) for p in data['patterns'])} pattern hits, {sum(len(l['l']) for l in data['links'])} links")
    PAGES.update(build_all(books))
    print(f"{len(PAGES)} book pages")
    index = [{"n": b["n"], "osis": b["osis"], "slug": b["slug"], "t": b["t"], "c": len(b["s"]), "page": PAGES.get(b["slug"])} for b in books]
    write("visual-index.html", os.path.join(OUT, "index.html"), {"books": index})
    print(f"visual/index.html: {sum(1 for b in index if b['page'])} of {len(index)} books have pages")


if __name__ == "__main__":
    main()
