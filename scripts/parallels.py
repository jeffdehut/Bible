"""Build the reader's parallel passages and reading plans.

    python3 scripts/parallels.py

Reads   A. T. Robertson, A Harmony of the Gospels (1922; Project Gutenberg #36264, public
        domain): its outline of 184 sections, each with the Gospel passages that tell it
        The Companion Bible, Appendix 56 (E. W. Bullinger, about 1910; public domain): the
        passages of Samuel and Kings told again in Chronicles (and Isaiah)
        Theographic's verse dates (Ussher, via the Treasury of Scripture Knowledge), for the
        chronological reading plan
        STEPBible TVTMS, to move both books' English verse numbers to ours
Writes  data/bible/study/parallels.json   {sets: [{t, part, refs: [ref, ...]}], parts: [...]};
                                           the Gospel sections keep Robertson's numbers
        data/bible/study/plans.json       reading plans: [{id, n, about, days: [[ref, ...]]}]
        data/bible/study/NN-book.json     adds "p": verse -> the parallel sets that include it
                                           (run scripts/study.py first; this adds to its files)

References are written as in scripts/study.py: "Matt.3.1-6", "1Chr.10", in our verse numbers.
"""

import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
import chronology                             # noqa: E402
import connections                            # noqa: E402
from study import OUT, Refs, write_json       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
ROBERTSON_URL = "https://www.gutenberg.org/cache/epub/36264/pg36264.txt"
COMPANION_URL = "https://therain.org/appendixes/app56.html"

# English book names and abbreviations, as these two books print them -> OSIS.
NAMES = {"Matt": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts", "1 Cor": "1Cor",
         "1 Sam": "1Sam", "2 Sam": "2Sam", "1 Kings": "1Kgs", "2 Kings": "2Kgs",
         "1 Chron": "1Chr", "2 Chron": "2Chr", "Isaiah": "Isa"}
BOOK_RE = re.compile(r"\b(" + "|".join(re.escape(k) for k in sorted(NAMES, key=len, reverse=True)) + r")\.?\s")

SMALL = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "of", "on", "or", "the", "to", "upon", "with"}


def title_case(s):
    words = s.lower().split()
    return " ".join(w if (k and w in SMALL) else w[:1].upper() + w[1:] for k, w in enumerate(words)) \
        .replace("(logos)", "(Logos)").replace("Jesus'", "Jesus’").replace("'s", "’s")


def ref_list(osis, text):
    """'3: 1-14; 4: 9' or '15 & 16' or '5: 2- 7: 10' or '22: 5-7, 9' -> ['Book.3.1-Book.3.14', ...]."""
    out, chapter = [], None
    text = re.sub(r"\s+", "", text.replace("&", ";")).rstrip(".")
    for part in filter(None, text.split(";")):
        for piece in filter(None, part.split(",")):
            piece = re.sub(r"(?<=\d)[ab]\b", "", piece)
            m = re.fullmatch(r"(?:(\d+):)?(\d+)(?:-(?:(\d+):)?(\d+))?", piece)
            if not m:
                raise ValueError(f"unparsed reference {osis} {piece!r} in {text!r}")
            c, a, c2, b = m.groups()
            if c is None and ":" not in part and chapter is None:   # whole chapters: '27', '15-16'
                out.append(f"{osis}.{a}" + (f"-{osis}.{b}" if b else ""))
                continue
            if c is not None:
                chapter = c
            if chapter is None:
                raise ValueError(f"no chapter for {osis} {piece!r}")
            start = f"{osis}.{chapter}.{a}"
            if b:
                end_c = c2 or chapter
                out.append(f"{start}-{osis}.{end_c}.{b}")
                chapter = end_c
            else:
                out.append(start)
    return out


def chunks(text):
    """'Mark 1:2-6; Matt. 3:1-6' -> [('Mark', '1:2-6'), ('Matt', '3:1-6')]."""
    hits = list(BOOK_RE.finditer(text))
    return [(NAMES[m[1]], text[m.end():hits[k + 1].start() if k + 1 < len(hits) else len(text)].strip(" ;."))
            for k, m in enumerate(hits)]


def robertson():
    path = connections.fetch(ROBERTSON_URL, os.path.join(CACHE, "gutenberg", "pg36264.txt"))
    lines = open(path, encoding="utf-8").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("PART I: THE SOURCES") and i > 250)
    end = next(i for i, l in enumerate(lines) if "TABLE FOR FINDING ANY PASSAGE" in l and i > start)
    sets, parts, part = [], [], None
    k = start
    while k < end:
        line = lines[k].strip()
        m = re.match(r"PART ([IVXL]+): (.+)", line)
        if m:
            part = len(parts)
            parts.append(title_case(m[2]))
        m = re.match(r"Sect\. (\d+[a-z]?): (.+)", line)
        if m:
            no, title = m[1], m[2]
            k += 1
            # The title may run on to the next line, indented further; then come the references.
            while k < end and lines[k].strip() and not BOOK_RE.match(lines[k].strip() + " "):
                title += " " + lines[k].strip()
                k += 1
            refs_text = ""
            # The section's own references; a sub-section's title and references may follow.
            while k < end and (BOOK_RE.match(lines[k].strip() + " ") or (refs_text and re.match(r"\d", lines[k].strip()))):
                refs_text += " " + lines[k].strip()
                k += 1
            refs = [r for osis, t in chunks(refs_text + " ") for r in ref_list(osis, t)]
            sets.append({"no": no, "t": title_case(title), "part": part, "refs": refs})
            continue
        k += 1
    return sets, parts


def companion():
    path = connections.fetch(COMPANION_URL, os.path.join(CACHE, "companion", "app56.html"))
    import html as _html
    text = _html.unescape(re.sub(r"<[^>]+>", " ", open(path, encoding="latin-1").read()))
    text = re.sub(r"\s+", " ", text)
    text = text[text.index("The following is the table"):text.index("Appendix Index")]
    text = re.sub(r"(\s\.)+\s", " | ", text.split(":", 1)[1])
    rows = []
    # Each row is "Samuel or Kings | Chronicles or Isaiah"; the next row's left side follows the
    # right side directly.
    pieces = chunks(text + " ")
    left = []
    for osis, t in pieces:
        refs_text, bar, _ = t.partition("|")
        refs = ref_list(osis, refs_text)
        if osis in ("1Sam", "2Sam", "1Kgs", "2Kgs"):
            left += refs
        else:
            rows.append((tuple(left), refs))
            left = []
    # One set for each Samuel or Kings passage, with every passage that tells it again.
    sets = collections.OrderedDict()
    for l, r in rows:
        sets.setdefault(l, []).extend(r)
    return [{"refs": list(l) + r} for l, r in sets.items()]


# ---------------------------------------------------------------- reading plans

def split_days(chapters, days, weight):
    """Divide chapters into `days` consecutive days of about equal weight."""
    total = sum(weight(c) for c in chapters)
    out, cur, acc = [], [], 0.0
    for k, ch in enumerate(chapters):
        cur.append(ch)
        acc += weight(ch)
        left_days = days - len(out) - 1
        left_ch = len(chapters) - k - 1
        if (acc >= total * (len(out) + 1) / days and left_days > 0) or left_ch == left_days:
            if left_days > 0:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


def plans(texts, verse_year):
    nverses = collections.Counter((b, c) for b, vs in texts.items() for c, _ in vs)
    canon = [(osis, c) for _, osis, _, _ in BOOKS for c in sorted({c for c, _ in texts[osis]})]
    ref = lambda ch: f"{ch[0]}.{ch[1]}"
    w = lambda ch: nverses[ch]
    out = []

    def plan(pid, name, about, days):
        out.append({"id": pid, "n": name, "about": about, "days": [[ref(c) for c in d] for d in days]})

    plan("canon", "Through the Bible in a year", "Every chapter in a year, in the order of the books, "
         "about 85 verses a day.", split_days(canon, 365, w))
    # Chronological: each chapter at the median year of its dated verses (Ussher's dates, from the
    # Treasury of Scripture Knowledge). An undated chapter takes the year of the nearest dated
    # chapter before it in its book, or else after it; Haggai, which has no dated verses, is
    # placed at its own date, the second year of Darius (520 BC, Haggai 1:1).
    years = collections.defaultdict(list)
    for (b, c, v), y in verse_year.items():
        years[(b, c)].append(y)
    median = {ch: sorted(ys)[len(ys) // 2] for ch, ys in years.items()}
    median.update({("Hag", 1): -519, ("Hag", 2): -519})
    # A psalm whose title names David is read within David's life (Ussher: born 1085, died 1015
    # BC) unless the Treasury already dates it there; its other dates for the psalms are sparse
    # and often late. Other undated psalms keep their neighbours' dates.
    psalms = json.load(open(os.path.join(ROOT, "data", "bible", "text", "19-psalms.json"), encoding="utf-8"))
    for ch in psalms["chapters"]:
        title = " ".join(re.split(r"(?<=[.!?])\s", ch["v"][0][1])[:2]) if ch["v"] else ""
        y = median.get(("Ps", ch["c"]))
        if re.search(r"\b(of|for) David\b", title, re.I) and not (y is not None and -1084 <= y <= -1014):
            median[("Ps", ch["c"])] = -1034
    key = {}
    for n, ch in enumerate(canon):
        same = [x for x in canon if x[0] == ch[0]]
        before = [median[x] for x in same if x[1] < ch[1] and x in median]
        after = [median[x] for x in same if x[1] > ch[1] and x in median]
        y = median.get(ch, before[-1] if before else after[0] if after else None)
        # Within a book the chapters keep their order: none goes before the one ahead of it. Not
        # in the Psalms, nor in Chronicles, whose lists (1 Chronicles 9, the return from exile)
        # sit among stories of David.
        prev = canon[n - 1] if n else None
        if prev and prev[0] == ch[0] and ch[0] not in ("Ps", "1Chr", "2Chr"):
            y = max(y, key[prev][0])
        key[ch] = (y, n)
    chrono = sorted(canon, key=lambda ch: key[ch])
    plan("chrono", "The Bible in the order it happened", "Every chapter in a year, in the order of the "
         "events, after Ussher’s dating: Job beside the patriarchs, the Psalms and prophets beside "
         "the kings of their day, the letters beside Acts.", split_days(chrono, 365, w))
    nt = [ch for ch in canon if [b for _, b, _, t in BOOKS if b == ch[0] and t == "NT"]]
    plan("nt", "The New Testament in 90 days", "Matthew to Revelation, about 3 chapters a day.",
         split_days(nt, 90, w))
    gospels = [ch for ch in canon if ch[0] in ("Matt", "Mark", "Luke", "John")]
    plan("gospels", "The Gospels in 30 days", "Matthew, Mark, Luke and John, about 3 chapters a day.",
         split_days(gospels, 30, w))
    psalms = [("Ps", c) for c in range(1, 151)]
    days = []
    for d in range(30):     # the classic pattern: Psalms d+1, d+31, d+61, d+91, d+121, and a Proverb
        days.append([("Ps", d + 1 + 30 * k) for k in range(5)] + [("Prov", d + 1)])
    days.append([("Prov", 31)])
    plan("wisdom", "Psalms and Proverbs in a month", "Five psalms and a chapter of Proverbs a day: "
         "on day 1, Psalms 1, 31, 61, 91 and 121 and Proverbs 1.", days)
    assert sorted(c for d in days for c in d if c[0] == "Ps") == psalms
    return out


def main():
    texts = connections.load_texts()
    vers = connections.Versification(connections.fetch_stepbible("tvtms"), texts)
    refs = Refs(vers, texts)
    gospel, parts = robertson()
    kings = companion()
    sets, by_verse = [], collections.defaultdict(list)
    for kind, group in (("g", gospel), ("k", kings)):
        for s in group:
            ours = []
            for r in s["refs"]:
                parsed = refs.parse(r)
                if parsed:
                    ours.append((parsed[0], parsed[1]))
            if len({p[0].split(".")[0] for p in ours}) < 2 and kind == "k":
                continue
            n = len(sets)
            entry = {"k": kind, "refs": [p[0] for p in ours]}
            if kind == "g":
                entry.update({"no": s["no"], "t": s["t"], "part": s["part"]})
            sets.append(entry)
            for _, verses in ours:
                for v in verses:
                    if n not in by_verse[v]:
                        by_verse[v].append(n)
    write_json(os.path.join(OUT, "parallels.json"), {"parts": parts, "sets": sets})
    verse_year = chronology.Chronology(chronology.fetch(CACHE), vers).verse_year
    ps = plans(texts, verse_year)
    write_json(os.path.join(OUT, "plans.json"), ps)
    for num, osis, name, _ in BOOKS:
        path = os.path.join(OUT, file_stem(num, name) + ".json")
        data = json.load(open(path, encoding="utf-8"))
        data["p"] = {f"{c}:{v}": ss for (b, c, v), ss in sorted(by_verse.items()) if b == osis}
        write_json(path, data)
    many = sum(1 for s in sets if len(s["refs"]) > 1)
    print(f"Parallels: {sum(s['k'] == 'g' for s in sets)} Gospel sections ({many} with more than one passage), "
          f"{sum(s['k'] == 'k' for s in sets)} Samuel-Kings sets; {refs.bad} references not found")
    print("Plans: " + ", ".join(f"{p['n']} ({len(p['days'])} days)" for p in ps))


if __name__ == "__main__":
    main()
