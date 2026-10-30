"""Two pages for the books that are hardest to see whole: the Psalms (psalms.html) and the
Proverbs (proverbs.html).

    python3 scripts/wisdom.py           (after reader.py and connections.py)

psalms.html: the 150 psalms in the five books of the Psalter, each with its heading as the
translation gives it (and the author, kind of song and setting read from it), its type from
data/psalms.csv, its length and first line, and the New Testament chapters the cross-references
tie it to (data/graph.json).

data/psalms.csv is compiled for this project: one common way of sorting the psalms by type
(lament, praise, thanksgiving, trust, royal, wisdom, history), whether a lament is the
community's, groups the psalms are often studied in (penitential, acrostic, imprecatory and so
on), and for the headings that name a moment in David's life, the passage that tells it.
Scholars sort many psalms differently, and many mix types; the page says so.

proverbs.html: every verse of Proverbs in order, in the collections the book itself marks, and
the topics each verse speaks of. A topic is found by the Hebrew words of the verse (by Strong's
number, from data/bible/words/) and by words of the English, so a saying about the tongue is
found whether it says tongue, lips, mouth or words.
"""

import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webpages                                  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
TEMPLATES = os.path.join(ROOT, "scripts", "templates")


def plain(text):
    return re.sub(r"\[\^\w+\]", "", text or "").replace("*", "")


def write(name, data):
    src = open(os.path.join(TEMPLATES, name), encoding="utf-8").read()
    src = src.replace("<!-- APPBAR -->", webpages.appbar(name))
    src = src.replace("<!-- DATA -->", f'<script type="application/json" id="data">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>')
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.document(src))


def graph_echoes():
    """For each psalm, the New Testament chapters the cross-references tie it to, strongest first."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from web3d import unpack
    D = json.load(open(os.path.join(ROOT, "data", "graph.json"), encoding="utf-8"))
    a, b, t = unpack(D)
    starts, k = [], 0
    for _, _, _, n in D["books"]:
        starts.append(k)
        k += n
    ps, nt = starts[18], starts[39]
    name = {}
    for bi, (bname, _, _, n) in enumerate(D["books"]):
        for c in range(n):
            name[starts[bi] + c] = (bname, c + 1)
    weights = iter(D["w"])
    out = {n: [] for n in range(1, 151)}
    for x, y, ty in zip(a, b, t):
        w = next(weights) if ty == 0 else 0
        if ty != 0:
            continue
        for p, q in ((x, y), (y, x)):
            if ps <= p < ps + 150 and q >= nt:
                out[p - ps + 1].append((w, name[q]))
    return {n: [f"{bk} {c}" for _, (bk, c) in sorted(v, key=lambda r: -r[0])[:6]] for n, v in out.items()}


TITLE = re.compile(r"^(For the director|A (psalm|song|maskil|miktam|shiggaion|prayer|testimony|love song)|Of (David|Solomon|Asaph|the sons of Korah|the servant)"
                   r"|With |According to |For Jeduthun|To bring to remembrance|For teaching|A song of ascents|A song of praise)")
AUTHORS = [("David", r"\bDavid\b"), ("Asaph", r"\bAsaph\b"), ("Sons of Korah", r"\bsons of Korah\b"), ("Solomon", r"\bSolomon\b"),
           ("Moses", r"\bMoses\b"), ("Heman", r"\bHeman\b"), ("Ethan", r"\bEthan\b")]
KINDS = [("psalm", r"\bpsalm\b"), ("song", r"\bsong\b"), ("maskil", r"\bmaskil\b"), ("miktam", r"\bmiktam\b"),
         ("prayer", r"\bprayer\b"), ("shiggaion", r"\bshiggaion\b")]
BOOKS = [(1, 41, "41:13"), (42, 72, "72:18–20"), (73, 89, "89:52"), (90, 106, "106:48"), (107, 150, "150")]


def psalms():
    text = json.load(open(os.path.join(DATA, "text", "19-psalms.json"), encoding="utf-8"))["chapters"]
    table = {int(r["psalm"]): r for r in csv.DictReader(open(os.path.join(ROOT, "data", "psalms.csv"), encoding="utf-8"))}
    echoes = graph_echoes()
    out = []
    for n, ch in enumerate(text, 1):
        # The heading is in the verses the English numbers 0; those verses can also hold the
        # psalm's first words, so the heading is their leading sentences that read as one.
        heading = [v for v in ch["v"] if len(v) > 3 and isinstance(v[3], dict) and str(v[3].get("e", "")).endswith(":0")]
        body = [v for v in ch["v"] if v not in heading]
        parts, lead = re.split(r"(?<=[.?!])\s+", " ".join(plain(v[1]) for v in heading)) if heading else [], []
        while parts and TITLE.match(parts[0]):
            lead.append(parts.pop(0))
        title, rest = " ".join(lead), " ".join(parts)
        first = rest or plain(body[0][1])
        verses = len(body) + (1 if rest else 0)
        r = table[n]
        tags = r["tags"].split()
        if 120 <= n <= 134:
            tags.insert(0, "ascents")
        if 113 <= n <= 118:
            tags.insert(0, "hallel")
        if 146 <= n <= 150:
            tags.insert(0, "final-hallel")
        out.append({
            "n": n, "t": title, "f": first, "v": verses, "g": r["type"], "c": bool(r["community"]), "tags": tags,
            "a": [a for a, rx in AUTHORS if re.search(rx, title)], "k": [k for k, rx in KINDS if re.search(rx, title, re.I)],
            "d": "For the director" in title, "s": r["setting"] or None, "nt": echoes[n],
        })
    return {"psalms": out, "books": [{"from": a, "to": z, "dox": d} for a, z, d in BOOKS]}


# Topics: [key, name, Strong's numbers (a "~gloss" after one keeps only the words whose gloss
# has it), English words]
TOPICS = [
    ("speech", "Words and the tongue", "3956 8193 6310 1697", r"\b(tongues?|lips?|mouths?|words?|speak\w*|speech|talk\w*|gossip\w*|whisper\w*|slander\w*)\b"),
    ("honesty", "Honesty and lies", "8267 4820 3576 3577 3976 7810", r"\b(lying|liars?|lies(?! (in wait|open|down))|false\w*|deceit\w*|deceiv\w*|bribes?|scales|weights?|honest\w*|truth\w*)\b"),
    ("wealth", "Wealth and poverty", "6239 7326 1800 6041 34 3701 2091 1952", r"\b(rich\w*|wealth\w*|poor|poverty|money|silver|gold|treasures?|needy|lend\w*|borrow\w*|debts?)\b"),
    ("work", "Work and laziness", "6102 6103 7503~idle 2742~dilig", r"\b(lazy|laziness|sluggards?|diligent\w*|hard work|work\w* (his|the) land|skilled in his work|outdoor work|labou?r\w*|toil\w*|idle|plow\w*|ants|a little sleep|love sleep|sleeps at harvest|gathers in summer|folding of the hands)\b"),
    ("anger", "Anger and self-control", "639 2534 3708 7116", r"\b(anger|angry|rage|temper\w*|wrath|quarrel\w*|strife|patien\w*|calm\w*|self-control|fights?)\b"),
    ("pride", "Pride and humility", "1347 1363 6038 1346 2087 1364", r"\b(pride|proud|arrogan\w*|haughty|humble|humility|boast\w*|lowly)\b"),
    ("friends", "Friends and neighbors", "7453 4828", r"\b(friends?|friendship|neighbou?rs?|companions?)\b"),
    ("family", "Parents and children", "1 517 4148 7626 3256", r"\b(fathers?|mothers?|sons?|child|children|discipline\w*|rod|grandchildren)\b"),
    ("marriage", "Marriage and faithfulness", "802 5237 2181 5003", r"\b(wife|wives|wom[ae]n|adulter\w*|prostitutes?|husbands?|marri\w*)\b"),
    ("kings", "Kings and rulers", "4428 7336 5057 8269 4910", r"\b(kings?|rulers?|princes?|throne|nobles?|officials?)\b"),
    ("justice", "Justice", "4941 6664 6666", r"\b(justice|judge\w*|judgment|innocent|guilty|witness\w*|court)\b"),
    ("fools", "Fools and mockers", "3684 191 3887 6612 5036 200", r"\b(fools?|foolish\w*|folly|mock\w*|naive)\b"),
    ("wisdom", "Wisdom and knowledge", "2451 2450 998 8394 1847", r"\b(wis(e|dom)|understanding|knowledge|insight|prudent\w*|discern\w*|instruction|counsel|advice)\b"),
    ("lord", "The LORD", "3068 3374", r"\bLORD\b"),
    ("righteous", "The righteous and the wicked", "6662 7563", r"\b(righteous|wicked)\b"),
    ("drink", "Food and drink", "3196 7941 3899", r"\b(wine|strong drink|drunk\w*|glutton\w*|food|bread|honey|feast\w*)\b"),
    ("life", "Life and death", "2416 4194 7585", r"\b(life|death|dies?|Sheol|grave)\b"),
    ("heart", "The heart", "3820 3824", r"\bhearts?\b"),
]
COLLECTIONS = [
    ("Wisdom's call", (1, 1), (9, 18), "A father's talks to his son, and Wisdom calling out in the streets: why wisdom is worth more than anything, before the short sayings begin. At the end, Wisdom and Folly invite the simple to their houses (chapter 9)."),
    ("The proverbs of Solomon", (10, 1), (22, 16), "375 sayings, nearly all a single couplet. In chapters 10 to 15 most set two things side by side with “but”: the wise and the fool, the righteous and the wicked. From chapter 16 more of them build one thought."),
    ("Sayings of the wise", (22, 17), (24, 22), "Longer sayings of two or three couplets, from a teacher to a pupil: on the poor, the hot-tempered, debt, the king's table, drink and envy."),
    ("More sayings of the wise", (24, 23), (24, 34), "A short appendix: on judging fairly, and the field of the lazy man."),
    ("Solomon's, copied by Hezekiah's men", (25, 1), (29, 27), "More proverbs of Solomon, which the men of Hezekiah king of Judah copied (25:1): many pictures and comparisons from life, much on kings and fools."),
    ("The words of Agur", (30, 1), (30, 33), "Agur son of Jakeh: humble questions about God, and sayings that count things off: “three things … four”."),
    ("The words of King Lemuel", (31, 1), (31, 9), "What King Lemuel's mother taught him: about wine, women, and speaking up for the poor."),
    ("The capable wife", (31, 10), (31, 31), "A poem in praise of a capable wife, each verse beginning with the next letter of the Hebrew alphabet."),
]


def proverbs():
    text = json.load(open(os.path.join(DATA, "text", "20-proverbs.json"), encoding="utf-8"))["chapters"]
    words = json.load(open(os.path.join(DATA, "words", "20-proverbs.json"), encoding="utf-8"))["chapters"]
    rules = []
    for _, _, codes, rx in TOPICS:
        want = {}
        for c in codes.split():
            num, _, gloss = c.partition("~")
            want[num] = gloss
        rules.append((want, re.compile(rx)))
    verses = []
    for ch, wch in zip(text, words):
        for row in ch["v"]:
            v, english = row[0], plain(row[1])
            found = set()
            for w in (wch["w"].get(str(v)) or "").split("¦"):
                f = w.split("|")
                if len(f) < 3:
                    continue
                for code in f[2].split("/"):
                    num = re.sub(r"[A-Za-z]$", "", code)
                    for k, (want, _) in enumerate(rules):
                        if num in want and (not want[num] or want[num] in f[1].lower()):
                            found.add(k)
            for k, (_, rx) in enumerate(rules):
                if rx.search(english):
                    found.add(k)
            col = next(i for i, (_, a, z, _) in enumerate(COLLECTIONS) if a <= (ch["c"], v) <= z)
            # A saying that turns on "but": two things set side by side.
            verses.append([ch["c"], v, english, sorted(found), col, 1 if re.search(r"[,;] but\b", english) else 0])
    return {"verses": verses, "topics": [[k, n] for k, n, _, _ in TOPICS],
            "collections": [{"n": n, "from": a, "to": z, "about": about} for n, a, z, about in COLLECTIONS]}


def main():
    p = psalms()
    write("psalms.html", p)
    q = proverbs()
    write("proverbs.html", q)
    print(f"psalms.html: {len(p['psalms'])} psalms; proverbs.html: {len(q['verses'])} verses, {len(q['topics'])} topics")


if __name__ == "__main__":
    main()
