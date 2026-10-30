"""Inductive study markings for the whole Bible: the key words of each verse, marked with the
symbols set out in MARKINGS.md.

    python3 scripts/markings.py            build the markings (after reader.py)
    python3 scripts/markings.py --check    also list, for each marking, verses whose source
                                            words call for it but where no English form matched

Reads   data/bible/text/NN-book.json    the English verses as the reader shows them
        data/bible/words/NN-book.json   the source words with their Strong's numbers and grammar
Writes  data/bible/markings/rules.json          the markings: how each looks, what it marks, and
                                                 its name and word forms in each language
        data/bible/markings/en/NN-book.json     each book, chapter by chapter: for each verse a
                                                 flat list [start, end, marking, ...], counting
                                                 the characters of the verse as the reader shows
                                                 it (no note markers or asterisks)

A marking is defined by meaning, not by English spelling: each lists the Strong's numbers of the
Hebrew, Aramaic and Greek words it stands for, and, for each language the Bible is shown in, the
word forms those words take there. A verse is marked only where its source has one of the
words, so "spirit" in "a broken spirit" is not taken for the Holy Spirit, and "love" is marked
in a verse about love, not in one that only says "I would love to". A new language needs only
its forms (and, if its text uses other markup, its own reading of the text below).
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
OUT = os.path.join(DATA, "markings")

# Groups shown together in the reader's key, and turned on and off together.
GROUPS = [
    ("god", "God"),
    ("themes", "Key themes"),
    ("life", "Life and death"),
    ("time", "Time and place"),
    ("links", "Connecting words"),
]

# Each marking: id, group, how it looks (style, color, glyph), its Strong's numbers (H for
# Hebrew and Aramaic, G for Greek), and its English name and forms. A form is matched as a
# whole word or phrase, exactly as written (so "God" is not "god", and "Spirit" not "spirit").
# The styles: box, cloud, circle (outlines); under, double, dotted, wavy (lines beneath);
# strike (a line through); tint (a wash of color); a glyph is a small sign set before the word.
def forms(*words):
    """Each word as written and capitalized, for forms that open a sentence."""
    out = []
    for w in words:
        out += [w, w[0].upper() + w[1:]]
    return sorted(set(out), key=len, reverse=True)


def inflect(*stems):
    """Simple English inflections: love → love, loves, loved, loving."""
    out = []
    for s in stems:
        out.append(s)
        if s.endswith("e"):
            out += [s + "s", s + "d", s[:-1] + "ing"]
        else:
            out += [s + "s", s + "ed", s + "ing"]
    return out


MARKINGS = [
    # God
    dict(id="god", group="god", style="box", color="gold",
         strongs="H410 H426 H430 H433 H3050 H3068 H3069 H136 G2316 G3962",
         name="God", note="God, the LORD, the Father",
         en=["God", "God's", "LORD", "LORD's", "GOD", "Father", "Father's", "Lord@H136", "Lord's@H136"]),
    dict(id="jesus", group="god", style="box", color="crimson",
         strongs="G2424 G5547 G3323 G5207 G721 G286",
         name="Jesus", note="Jesus, Christ, the Messiah, the Son, the Lamb",
         en=["Lord Jesus Christ", "Lord Jesus", "Jesus Christ", "Christ Jesus", "Jesus", "Jesus'", "Christ", "Christ's", "Messiah",
             "Son of Man", "Son of God", "Son", "Lamb", "Lamb's"]),
    dict(id="spirit", group="god", style="cloud", color="teal",
         strongs="H7307 G4151",
         name="The Holy Spirit", note="where the Spirit is God's own",
         en=["Holy Spirit", "Spirit of God", "Spirit of the LORD", "Spirit"]),
    dict(id="satan", group="god", style="strike", color="red",
         strongs="H7854 G4567 G1228 G954 G1404",
         name="Satan", note="Satan, the devil, the dragon",
         en=forms("the devil", "devil's") + ["Satan", "Satan's", "Beelzebul", "dragon"]),
    # Key themes
    dict(id="love", group="themes", style="tint", color="pink",
         strongs="G25 G26 G27 G5368 G5360 H157 H160 H2617",
         name="Love", note="love, beloved, steadfast love",
         en=forms(*inflect("love"), "lovingkindness", "beloved", "steadfast love", "faithful love",
                  "loyal love", "unfailing love", "faithful kindness", "loyalty", "kindness")),
    dict(id="faith", group="themes", style="double", color="blue",
         strongs="G4102 G4100 G4103 G4135 H539 H530",
         name="Faith", note="faith, believe, faithful",
         en=forms("faith", "faithful", "faithfulness", "faithfully", *inflect("believe"),
                  "believer", "believers", "belief", "unbelief", "trust", "trusted", "trusts")),
    dict(id="grace", group="themes", style="under", color="green",
         strongs="G5485 G5483 H2580 H2603",
         name="Grace", note="grace, favor, gracious",
         en=forms("grace", "gracious", "graciously", "favor", "freely given")),
    dict(id="sin", group="themes", style="wavy", color="brown",
         strongs="G266 G264 G268 G265 G3900 G458 G93 H2403 H2398 H2399 H2400 H5771 H6588 H6586 H7563",
         name="Sin", note="sin, iniquity, transgression, wickedness",
         en=forms("sin", "sins", "sinned", "sinning", "sinner", "sinners", "sinful", "iniquity",
                  "iniquities", "guilt", "transgression", "transgressions", "trespass",
                  "trespasses", "rebellion", "rebellions", "rebelled", "wickedness", "wicked",
                  "lawlessness", "unrighteousness", "wrongdoing", "wrongdoings", "offense", "offenses")),
    dict(id="repent", group="themes", style="under", color="orange", glyph="↻",
         strongs="G3340 G3341 G1994 H7725",
         name="Repent", note="repent, turn back to God",
         en=forms("repent", "repents", "repented", "repenting", "repentance")),
    dict(id="covenant", group="themes", style="circle", color="indigo",
         strongs="H1285 G1242",
         name="Covenant", en=forms("covenant", "covenants", "treaty", "treaties")),
    dict(id="kingdom", group="themes", style="under", color="purple", glyph="♔",
         strongs="G932 H4467 H4438 H4437",
         name="Kingdom", en=forms("kingdom", "kingdoms", "kingship")),
    dict(id="save", group="themes", style="double", color="green",
         strongs="G4982 G4991 G4990 G4992 H3467 H3444 H3468 H8668",
         name="Salvation", note="save, salvation, Savior",
         en=forms("salvation", "Savior", *inflect("save"), "deliverance", "rescue", "rescued",
                  "rescues", "deliver", "delivered", "delivers", "deliverer", "victory")),
    dict(id="righteous", group="themes", style="under", color="navy",
         strongs="G1342 G1343 G1344 G1345 H6662 H6664 H6666 H6663",
         name="Righteousness", note="righteous, justify",
         en=forms("righteous", "righteousness", "righteously", "justify", "justified", "justifies",
                  "justification", "upright", "in the right", "justice")),
    dict(id="holy", group="themes", style="tint", color="violet",
         strongs="G40 G37 G38 G42 H6944 H6918 H6942",
         name="Holy", note="holy, holiness, sanctify, saints",
         en=forms("holy", "holiness", "sanctify", "sanctified", "sanctifies", "sanctification",
                  "consecrate", "consecrated", "saints", "set apart", "Holy Place", "most holy", "sacred")),
    dict(id="glory", group="themes", style="tint", color="amber",
         strongs="G1391 G1392 H3519",
         name="Glory", note="glory, glorify",
         en=forms("glory", "glorious", "glorify", "glorified", "glorifies", "glorifying", "honor")),
    dict(id="pray", group="themes", style="circle", color="sky",
         strongs="G4336 G4335 G1189 G1162 H6419 H8605",
         name="Prayer", note="pray, prayer",
         en=forms("pray", "prays", "prayed", "praying", "prayer", "prayers")),
    dict(id="law", group="themes", style="under", color="slate", glyph="§",
         strongs="G3551 H8451",
         name="Law", note="the law, instruction",
         en=forms("law", "laws", "Law", "instruction", "instructions", "teaching")),
    dict(id="truth", group="themes", style="dotted", color="teal",
         strongs="G225 G227 G228 H571",
         name="Truth", note="truth, true",
         en=forms("truth", "true", "truly")),
    # Life and death
    dict(id="life", group="life", style="dotted", color="green",
         strongs="G2222 G2198 H2416 H2421 H2425",
         name="Life", note="life, live, living",
         en=forms("eternal life", "life", "lives", *inflect("live"), "alive")),
    dict(id="death", group="life", style="dotted", color="gray",
         strongs="G2288 G599 G3498 G2348 H4194 H4191",
         name="Death", note="death, die, dead",
         en=forms("death", "die", "dies", "died", "dying", "dead", "put to death", "kill", "kills", "killed")),
    # Time and place
    dict(id="time", group="time", style="dotted", color="olive", glyph="◷",
         strongs="G2250 G5610 G2540 G5550 G4594 H3117 H6256 H8141 G2094 H3119 H6258 G3568",
         name="Time", note="day, hour, season, year, now",
         en=forms("that day", "this day", "today", "day", "days", "hour", "hours", "season",
                  "seasons", "time", "times", "year", "years", "now")),
    dict(id="place", group="time", style="double", color="leaf",
         strongs="",
         name="Places", note="towns, lands, rivers, mountains",
         en=[]),
    # Connecting words
    dict(id="therefore", group="links", style="glyph", color="ink", glyph="∴",
         strongs="G3767 G1352 G686 G5105 G1223 H3651 H6258 H5921",
         name="Therefore", note="a conclusion: ask what it is there for",
         en=forms("therefore", "so then", "for this reason")),
    dict(id="but", group="links", style="glyph", color="ink", glyph="⇄",
         strongs="G235 G1161 G4133 H61 H3588 H389 H657",
         name="But", note="a contrast",
         en=forms("but", "nevertheless", "however")),
    dict(id="purpose", group="links", style="glyph", color="ink", glyph="→",
         strongs="G2443 G3704 G5620 G1519 H4616 H5668",
         name="So that", note="a purpose or result",
         en=forms("so that", "in order that", "in order to")),
]


# The word shown in the reader's key for each marking, where it is not the marking's name.
SAMPLES = {"spirit": "Spirit", "satan": "the devil", "repent": "repent", "save": "saved", "righteous": "righteous",
           "holy": "holy", "pray": "prayed", "life": "life", "death": "died", "time": "day", "place": "Jerusalem",
           "therefore": "therefore", "but": "but", "purpose": "so that", "love": "love", "faith": "faith",
           "grace": "grace", "sin": "sin", "covenant": "covenant", "kingdom": "kingdom", "glory": "glory",
           "law": "law", "truth": "truth"}


def strongs_of(word):
    """The Strong's numbers of one source word: '9002/9009/776G' → {776}."""
    out = set()
    for part in word.split("/"):
        m = re.match(r"\d+", part)
        if m and int(m.group()) < 9000:
            out.add(int(m.group()))
    return out


def counted(text):
    """The verse as the reader shows it, without note markers or the asterisks of italics."""
    text = re.sub(r"\[\^\w+\]", "", text)
    return text.replace("*", "")


def place_names(words):
    """The names of the places in a verse, from the glosses of its proper nouns of place."""
    names = set()
    # A name split into two words ("Beth-" and "-el") is joined again.
    joined = []
    for w in words:
        f = w.split("|")
        if len(f) < 4:
            continue
        if joined and joined[-1][1].endswith("-") and f[1].startswith("-") and joined[-1][2] == f[2]:
            joined[-1][1] += f[1][1:]
        else:
            joined.append(f)
    for f in joined:
        gloss, morph = f[1], f[3]
        if "Npl" in morph or re.search(r"-L$", morph) or "-LI" in morph:
            for name in re.findall(r"[A-Z][a-z]+(?:-[A-Za-z]+| [A-Z][a-z]+)*", gloss.replace("[", "").replace("]", "")):
                if name not in {"The", "In", "To", "From", "And", "Of", "At", "On", "By", "Into"}:
                    names.add(name)
                    if "-" in name:                     # Beth-el is Bethel in our text
                        names.add(name[0] + name[1:].replace("-", "").lower())
    return names


def main():
    check = "--check" in sys.argv
    rules = []
    for i, m in enumerate(MARKINGS):
        m["strong_set"] = {(s[0], int(s[1:])) for s in m["strongs"].split()}
        m["written"] = list(m["en"])
        # A form written "Lord@H136" is marked only where the verse has that word.
        m["gated"] = [(f.split("@")[0], {(g[0], int(g[1:])) for g in f.split("@")[1].split(",")}) for f in m["en"] if "@" in f]
        plain = [f for f in m["en"] if "@" not in f]
        m["regex"] = re.compile(r"(?<![\w'’])(?:" + "|".join(re.escape(f) for f in sorted(plain, key=len, reverse=True)) + r")(?![\w])") if plain else None
        m["en"] = plain + [f for f, _ in m["gated"]]
        rules.append({"id": m["id"], "group": m["group"], "style": m["style"], "color": m["color"],
                      **({"glyph": m["glyph"]} if m.get("glyph") else {}),
                      "strongs": m["strongs"].split(),
                      "name": {"en": m["name"]}, "sample": {"en": SAMPLES.get(m["id"], m["name"])}, **({"note": {"en": m["note"]}} if m.get("note") else {}),
                      "forms": {"en": m["written"]}})
    os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
    with open(os.path.join(OUT, "rules.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"groups": [{"id": g, "name": {"en": n}} for g, n in GROUPS], "markings": rules},
                  f, ensure_ascii=False, indent=1)
        f.write("\n")
    place_i = next(i for i, m in enumerate(MARKINGS) if m["id"] == "place")
    totals = [0] * len(MARKINGS)
    missed = [[] for _ in MARKINGS]
    for num, osis, name, _ in BOOKS:
        stem = file_stem(num, name)
        text = json.load(open(os.path.join(DATA, "text", stem + ".json"), encoding="utf-8"))
        words = json.load(open(os.path.join(DATA, "words", stem + ".json"), encoding="utf-8"))
        lang = "G" if text["t"] == "NT" else "H"
        out = []
        for ch, wch in zip(text["chapters"], words["chapters"]):
            marks = {}
            for row in ch["v"]:
                n, en = row[0], row[1]
                if not en:
                    continue
                ws = wch["w"].get(str(n), "").split("¦") if wch["w"].get(str(n)) else []
                nums = set()
                for w in ws:
                    f = w.split("|")
                    if len(f) > 2:
                        nums |= strongs_of(f[2])
                verse = counted(en)
                found = []           # (start, end, marking)
                for i, m in enumerate(MARKINGS):
                    if i == place_i:
                        for name in place_names(ws):
                            for x in re.finditer(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", verse):
                                found.append((x.start(), x.end(), i))
                        continue
                    if not any((lang, s) in m["strong_set"] for s in nums):
                        continue
                    hits = list(m["regex"].finditer(verse))
                    for f, need in m["gated"]:
                        if any((lang, x) in need for x in nums):
                            hits += re.finditer(r"(?<![\w'’])" + re.escape(f) + r"(?![\w])", verse)
                    if not hits and check:
                        missed[i].append(f"{osis}.{ch['c']}.{n} {verse[:110]}")
                    found += [(x.start(), x.end(), i) for x in hits]
                # Longer marks first; a word takes one marking (the God markings before the rest).
                found.sort(key=lambda t: (MARKINGS[t[2]]["group"] != "god", -(t[1] - t[0]), t[0]))
                taken, keep = [], []
                for s, e, i in found:
                    if any(s < te and ts < e for ts, te in taken):
                        continue
                    taken.append((s, e))
                    keep.append((s, e, i))
                    totals[i] += 1
                if keep:
                    marks[str(n)] = [x for t in sorted(keep) for x in t]
            out.append(marks)
        with open(os.path.join(OUT, "en", stem + ".json"), "w", encoding="utf-8", newline="\n") as f:
            f.write("[\n" + ",\n".join(json.dumps(c, separators=(",", ":")) for c in out) + "\n]\n")
    for m, t in zip(MARKINGS, totals):
        print(f"{m['id']:10} {t:6}")
    if check:
        for m, ms in zip(MARKINGS, missed):
            if ms:
                print(f"\n== {m['id']}: {len(ms)} verses with the word but no form matched")
                for x in ms[:12]:
                    print("  " + x)


if __name__ == "__main__":
    main()
