"""The Visual Bible: a page for each book, made from the book's own words, and the page that
gathers them (visual/index.html).

    python3 scripts/visual.py            (after reader.py and wisdom.py)

Reads   data/bible/books.json, data/bible/text/ (our English) and data/bible/words/ (each word of
        the Hebrew and Greek with its Strong's number and grammar)
Writes  visual/index.html               every book of the Bible, and the ones with pages
        visual/<book>.html               a book's page (so far 1, 2 and 3 John), from
                                         scripts/templates/visual-letters.html

Nothing here is commentary: every chart counts the book's own words, by their Strong's numbers,
or the grammar of its verbs, and every mark leads to its verse. The themes are lists of
Strong's numbers (THEMES); a sentence pattern is a run of words in the Greek (PATTERNS).
"""

import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webpages                                  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
TEMPLATES = os.path.join(ROOT, "scripts", "templates")
OUT = os.path.join(ROOT, "visual")

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
        write("visual-letters.html", os.path.join(OUT, PAGES[stem]), data)
        print(f"{name}: {len(data['verses'])} verses, {len(data['themes'])} themes, "
              f"{sum(len(p['h']) for p in data['patterns'])} pattern hits, {sum(len(l['l']) for l in data['links'])} links")
    index = [{"n": b["n"], "osis": b["osis"], "slug": b["slug"], "t": b["t"], "c": len(b["s"]), "page": PAGES.get(b["slug"])} for b in books]
    write("visual-index.html", os.path.join(OUT, "index.html"), {"books": index})
    print(f"visual/index.html: {sum(1 for b in index if b['page'])} of {len(index)} books have pages")


if __name__ == "__main__":
    main()
