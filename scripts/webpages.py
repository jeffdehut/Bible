"""Build two pages of the website: the Bible genealogy and the world-history timeline.

    Called by scripts/connections.py, which has already built everything the pages show.

Writes  data/genealogy.json   every person, their family links, names and dates
        data/history.json     the world-history streams, rulers, events and synchronisms
        genealogy.html        scripts/templates/genealogy.html with its data inlined
        history.html          scripts/templates/history.html with its data inlined
Each page is a single file that opens in any browser, with no server and no network
beyond its web fonts and one charting library.
"""

import json
import os
import re
import unicodedata

import familytree
from books import BOOKS
from chronology import year_label
from notes import ROOT, ref_label

# The website is served from the repository root; its page sources are in scripts/templates/.
SITE = ROOT
TEMPLATES = os.path.join(ROOT, "scripts", "templates")

# The world-history streams, grouped for the page's filters, in drawing order.
STREAM_GROUPS = [
    ("Bible lands", ["Egypt", "Sumer and Akkad", "Babylon", "Assyria", "Anatolia", "Aram", "Tyre", "Persia",
                     "Seleucid", "Nabataea", "Herodian", "Roman officials", "High priests"]),
    ("Faith and scripture", ["Jewish history", "Church", "Bible transmission", "Islamic world"]),
    ("Mediterranean and Europe", ["Greece", "Rome", "Carthage", "Byzantine Empire", "Europe", "Russia"]),
    ("Asia", ["Mongols", "India", "China", "Japan"]),
    ("Africa and the Americas", ["Africa", "Americas"]),
    ("The wider world", ["World", "World events", "Thinkers and writers"]),
]


def _dump(obj):
    """JSON safe to inline in a <script> element."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def genealogy_data(ctx, family_of, groups):
    """The genealogy page's data, in columns: one entry per person in each list.

    n names; s sex (M, F or -); f the first verse naming them, as [book, chapter, verse]
    with the books in "books"; v how many verses name them; tr tribe (1 + its index in
    "tribes", or 0); g their generation in their family (0 if none); p their parents as
    [parent, kind, ...], where kind is 1 for a father, 2 a mother, 0 not known, plus 4 for an
    ancestor link that skips generations and 8 for an uncertain one (0 for none); b a brief
    description. Sparse, keyed by person: u unnamed, o names in the original languages, a
    other names, sp spouses, sb siblings who share no recorded parent, by and dy years of
    birth and death. A title adds the first verse to a name that several people share.

    tree lays out the whole family of Adam, and the families married into it, for the viewer:
    [person, generation, row, ...], the line of Jesus on row 0; beside lists those set next
    to a spouse rather than under a parent."""
    ents, gen = ctx.entities, ctx.gen
    people = [i for i, e in enumerate(ents) if e["kind"] == "person"]
    pos = {i: k for k, i in enumerate(people)}
    order = {osis: k for k, (_, osis, _, _) in enumerate(BOOKS)}
    tribes = sorted({gen.tribe[i] for i in people if gen.tribe.get(i)})
    cols = {k: [] for k in ("n", "s", "f", "v", "tr", "g", "p", "b")}
    sparse = {k: {} for k in ("u", "o", "a", "sp", "sb", "by", "dy")}
    for k, i in enumerate(people):
        e = ents[i]
        cols["n"].append(e["name"])
        cols["s"].append({"Male": "M", "Female": "F"}.get(gen.sex.get(i), "-"))
        cols["f"] += [order[e["first"][0]], e["first"][1], e["first"][2]]
        cols["v"].append(len(e["verses"]))
        cols["tr"].append(tribes.index(gen.tribe[i]) + 1 if gen.tribe.get(i) else 0)
        cols["g"].append(family_of[i][1] if i in family_of else 0)
        ps = []
        for par, edge in gen.parents[i]:
            if par in pos:
                ps += [pos[par], {"father": 1, "mother": 2}.get(edge["role"], 0)
                       + (4 if "a" in edge["flags"] else 0) + (8 if "?" in edge["flags"] else 0)]
        cols["p"].append(ps or 0)
        cols["b"].append(e["brief"])
        if not e["named"]:
            sparse["u"][k] = 1
        forms = [f for f, _ in e["forms"] if f and not re.fullmatch(r"[\w\s.'-]*", f, re.A)]
        if forms:
            sparse["o"][k] = forms[:4]
        if e["aliases"]:
            sparse["a"][k] = e["aliases"]
        if i in ctx.born:
            sparse["by"][k] = ctx.born[i]
        if i in ctx.died:
            sparse["dy"][k] = ctx.died[i]
        spouses = sorted(pos[j] for j in gen.partners.get(i, {}) if j in pos)
        if spouses:
            sparse["sp"][k] = spouses
    parents_of = [set(cols["p"][k][0::2]) if cols["p"][k] else set() for k in range(len(people))]
    for k, i in enumerate(people):
        apart = sorted(pos[j] for j in gen.siblings.get(i, {}) if j in pos and not parents_of[k] & parents_of[pos[j]])
        if apart:
            sparse["sb"][k] = apart
    by_root = [{"r": pos[root], "m": len(members), "g": max(gens.values())} for _, root, members, gens in groups[:40]]
    jesus = next((i for i in people if ents[i]["id"].startswith("Jesus@Isa.7.14")), None)
    line = [pos[k] for k in gen.paternal_line(jesus)] if jesus is not None else []
    stats = {"people": sum(1 for i in people if ents[i]["named"]), "unnamed": sum(1 for i in people if not ents[i]["named"]),
             "links": sum(1 for (p, c) in gen.parent_edges if p in pos and c in pos),
             "families": len(groups), "largest": len(groups[0][2]), "generations": max(groups[0][3].values())}

    # The whole family of Adam, laid out for the viewer.
    plain = [{"p": [[cols["p"][k][j], "f" if cols["p"][k][j + 1] & 3 == 1 else "m" if cols["p"][k][j + 1] & 3 == 2 else "", ""]
                    for j in range(0, len(cols["p"][k]), 2)] if cols["p"][k] else [],
              "sp": sparse["sp"].get(k, [])} for k in range(len(people))]
    first = {k: tuple(cols["f"][3 * k:3 * k + 3]) for k in range(len(people))}
    placed, beside, _ = familytree.layout(plain, by_root[0]["r"], line, lambda k: (first[k], k))
    tree = [x for k in sorted(placed, key=lambda k: (placed[k][0], placed[k][1])) for x in (k, *placed[k])]
    stats["in_tree"] = len(placed)
    books = [ref_label(osis, 1, 1).rsplit(" ", 1)[0] for _, osis, _, _ in BOOKS]
    return {**cols, **sparse, "books": books, "tribes": tribes, "families": by_root, "line": line,
            "tree": tree, "beside": sorted(beside), "stats": stats}


def people_links(ctx):
    """data/bible/people.json, for the reader and the genealogy: the people each verse names.

    b the books, in order (as in genealogy.json's "books"); n the name each person goes by in
    the genealogy (null for those no verse names); verses {book: {"chapter:verse": [person,
    ...]}}, people numbered as in genealogy.json. Verses are in the reader's numbering."""
    ents = ctx.entities
    people = [i for i, e in enumerate(ents) if e["kind"] == "person"]
    # A Psalm's title is verse 0 in English numbering, but our text, like the Hebrew, numbers
    # it from verse 1, and a long title runs into verse 2: take the verse whose Hebrew has the name.
    bare = lambda t: re.sub(r"[^\u05d0-\u05ea]", "", unicodedata.normalize("NFD", t))
    names, verses = [], {}
    for k, i in enumerate(people):
        e = ents[i]
        names.append(e["name"] if e["verses"] else None)
        forms = [bare(f) for f, _ in e["forms"] if bare(f)]
        for osis, c, v in e["verses"]:
            if osis == "Ps" and v == 0:
                v = next((n for n in (1, 2) if any(f in bare(ctx.texts["Ps"].get((c, n), "")) for f in forms)), 1)
            verses.setdefault(osis, {}).setdefault(f"{c}:{v}", [])
            if k not in verses[osis][f"{c}:{v}"]:
                verses[osis][f"{c}:{v}"].append(k)
    order = [osis for _, osis, _, _ in BOOKS]
    out = {"b": order, "n": names,
           "verses": {b: dict(sorted(verses[b].items(), key=lambda kv: tuple(map(int, kv[0].split(":")))))
                      for b in order if b in verses}}
    return out


# The Bible's own count of years, as James Ussher reckoned it (Annales Veteris Testamenti, 1650)
# from the ages in its genealogies and reigns: the lane of key events from Creation, beside the
# lives of the people the genealogy dates. Years are astronomical (0 is 1 BC); each item names
# its verse and the icon the timeline draws for it.
USSHER_LIVES = "Lives in the Bible"
USSHER_EVENTS_STREAM = "From Creation"
USSHER_EVENTS = [
    ("Creation", -4003, "Genesis 1:1", "creation", "In the beginning God created the heavens and the earth."),
    ("The garden of Eden", -4003, "Genesis 2:8", "garden", "Adam and Eve in the garden, and their fall."),
    ("The Flood", -2347, "Genesis 7:11", "flood", "Noah, his family and the animals in the ark."),
    ("The tower of Babel", -2241, "Genesis 11:9", "tower", "The languages confused and the peoples scattered; Ussher's date is approximate."),
    ("The call of Abram", -1920, "Genesis 12:1", "tent", "Abram leaves Harran for the land God will show him."),
    ("Jacob's family goes down to Egypt", -1705, "Genesis 46:6", "pyramid", "Seventy of Jacob's household settle in Goshen."),
    ("The Exodus", -1490, "Exodus 14:21", "waves", "Israel leaves Egypt through the sea."),
    ("The law at Sinai", -1490, "Exodus 20:1", "tablets", "The ten commandments and the covenant at Sinai."),
    ("Solomon begins the temple", -1011, "1 Kings 6:1", "temple", "In the 480th year after the Exodus."),
    ("The kingdom divides", -974, "1 Kings 12:19", "crown", "Israel in the north, Judah in the south."),
    ("Samaria falls", -720, "2 Kings 17:6", "ruin", "Assyria carries the northern kingdom into exile."),
    ("Jerusalem falls", -587, "2 Kings 25:9", "ruin", "Babylon burns the temple; Judah goes into exile (Ussher's year)."),
    ("Cyrus lets the exiles return", -535, "Ezra 1:1", "home", "The first return from Babylon."),
]
USSHER_NOTE = ("Dates follow Ussher's chronology, counted from the Bible's own genealogies and reigns "
               "(through Theographic). Historians date the early chapters very differently, so this "
               "lane is the Bible's own reckoning, set beside the rest.")


def ussher_items(g):
    """The two Ussher lanes, from the genealogy page's data (genealogy_data, or its JSON)."""
    get = lambda d, k: d.get(k, d.get(str(k)))
    out = [{"k": "e", "s": USSHER_EVENTS_STREAM, "n": n, "a": y, "z": y, "c": 1, "ref": ref, "icon": icon,
            "note": note, "u": 1} for n, y, ref, icon, note in USSHER_EVENTS]
    for k in range(len(g["n"])):
        a, z = get(g["by"], k), get(g["dy"], k)
        if a is None or z is None or z < a:
            continue
        b, c, v = g["f"][3 * k:3 * k + 3]
        out.append({"k": "f", "s": USSHER_LIVES, "n": g["n"][k], "a": a, "z": z, "u": 1,
                    "note": g["b"][k], "ref": f"{g['books'][b]} {c}:{v}"})
    return out


def history_data(ctx, genealogy=None):
    order = [s for _, streams in STREAM_GROUPS for s in streams]
    group_of = {s: g for g, streams in STREAM_GROUPS for s in streams}
    items = []
    for r in ctx.periods:
        items.append(("p" + r["level"][0], r))
    for r in ctx.rulers:
        items.append(("r", r))
    for r in ctx.world_events:
        items.append(("e" if r["kind"] == "event" else "f", r))
    out = []
    for kind, r in items:
        rec = {"k": kind, "s": r["stream"], "n": r["name"], "a": r["start_y"], "z": r["end_y"]}
        if r.get("end") == "present":
            rec["now"] = 1
        if r["approximate"] == "yes":
            rec["c"] = 1
        if r.get("note"):
            rec["note"] = r["note"]
        if r.get("wikidata"):
            rec["wd"] = r["wikidata"]
        if r.get("entity") is not None:
            e = ctx.entities[r["entity"]]
            rec["bible"] = r.get("biblical_name") or e["name"]
            rec["ref"] = ref_label(*e["first"])
        out.append(rec)
    unknown = sorted({r["s"] for r in out} - set(order))
    if unknown:
        raise ValueError(f"streams missing from webpages.STREAM_GROUPS: {unknown}")
    if genealogy:
        out += ussher_items(genealogy)
    syncs = [{"n": s["event"], "ref": ref_label(*s["verse"]), "m": s["modern_y"], "us": s["ussher_y"],
              "c": 1 if s["approximate"] == "yes" else 0, "ev": s["evidence"]} for s in ctx.syncs]
    used = {r["s"] for r in out}
    streams = ([{"name": s, "group": "The Bible"} for s in (USSHER_EVENTS_STREAM, USSHER_LIVES) if s in used]
               + [{"name": s, "group": group_of[s]} for s in order if s in used])
    return {"streams": streams, "groups": [g for g, _ in STREAM_GROUPS], "items": out, "syncs": syncs, "ussher": USSHER_NOTE,
            "present": max(r["z"] for r in out)}


STANDALONE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{page}
</body>
</html>
"""

# Every page follows the light or dark choice made in the reader's display settings, which the
# reader keeps in localStorage as "pe.settings"; with no choice made, the system's setting rules.
THEME = ('<script>try { const t = (JSON.parse(localStorage.getItem("pe.settings")) || {}).theme; '
         'if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t); } '
         'catch (e) { /* storage unavailable */ }</script>')


def head(root="", colors=("#fbfaf7", "#0d111b")):
    """The icon, the browser colors and the theme: the same on every page of the site."""
    light, dark = colors
    return (f'<script src="{root}i18n.js?v=3"></script>\n'
            f'<link rel="icon" href="{root}icons/icon.svg" type="image/svg+xml">\n'
            f'<link rel="apple-touch-icon" href="{root}icons/icon-192.png">\n'
            f'<meta name="theme-color" content="{light}" media="(prefers-color-scheme: light)">\n'
            f'<meta name="theme-color" content="{dark}" media="(prefers-color-scheme: dark)">\n{THEME}')


def document(body, root="", colors=("#fbfaf7", "#0d111b")):
    return STANDALONE.format(head=head(root, colors), page=body)


# The bar across the top of the pages beside the reader: the name, which leads to the reader,
# and the menu button (nav.js puts it at the end), which holds every part of the site, the same
# on every page. It takes the page's own colors (--bg, --ink, --muted, --line, --lapis,
# --lapis-soft), so it sits on any of them.
APPBAR_CSS = """<style>
:root { --bar: 56px; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 11; background: var(--bg); }
.appbar {
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; height: var(--bar);
  margin-inline: calc(-1 * max(16px, env(safe-area-inset-left, 0px))) calc(-1 * max(16px, env(safe-area-inset-right, 0px)));
  padding-inline: max(8px, env(safe-area-inset-left, 0px)) max(8px, env(safe-area-inset-right, 0px));
  display: flex; align-items: center; gap: 4px; background: color-mix(in srgb, var(--bg) 92%, transparent);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-bottom: 1px solid var(--line);
}
.appbar .brand {
  display: inline-flex; align-items: center; gap: 10px; min-height: 40px; padding: 0 8px; border-radius: 10px;
  color: var(--ink); text-decoration: none; white-space: nowrap; font: 500 17px/1 "Frank Ruhl Libre", "Noto Serif", Georgia, serif; letter-spacing: 0.01em;
}
.appbar .brand img { width: 26px; height: 26px; border-radius: 7px; flex: none; }
.appbar .sitenav-btn { margin-inline-start: auto; }
.appbar a:focus-visible { outline: 2px solid var(--lapis); outline-offset: 0; }
@media print { .appbar { display: none; } }
</style>"""


def appbar(current, root=""):
    """The shared bar, for the page whose address (from the site root) is `current`; the menu
    marks the page it is on (nav.js)."""
    return (f'{APPBAR_CSS}\n<header class="appbar">\n'
            f'  <a class="brand" href="{root}index.html"><img src="{root}icons/icon.svg" alt="Plain English Bible">'
            f'<span aria-hidden="true">Plain English Bible</span></a>\n</header>\n'
            f'<script src="{root}nav.js?v=33"></script>')


def page(name, data):
    """The page body (title, styles, markup, scripts) with its data inlined."""
    src = open(os.path.join(TEMPLATES, f"{name}.html"), encoding="utf-8").read()
    marker = "<!-- DATA -->"
    if marker not in src:
        raise ValueError(f"scripts/templates/{name}.html has no {marker} marker")
    src = src.replace("<!-- APPBAR -->", appbar(f"{name}.html"))
    return src.replace(marker, f'<script type="application/json" id="data">{_dump(data)}</script>')


def _columns(data):
    """JSON with one key to a line: compact, but a change shows as the keys it touches."""
    return "{\n" + ",\n".join(f"{json.dumps(k)}:{json.dumps(v, ensure_ascii=False, separators=(',', ':'))}"
                               for k, v in data.items()) + "\n}\n"


def write_static(name):
    """A page with no data, such as privacy.html: its template with the site's bar and head."""
    src = open(os.path.join(TEMPLATES, f"{name}.html"), encoding="utf-8").read()
    with open(os.path.join(SITE, f"{name}.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(document(src.replace("<!-- APPBAR -->", appbar(f"{name}.html"))))


def build(ctx, family_of, groups):
    os.makedirs(os.path.join(SITE, "data", "bible"), exist_ok=True)
    pages = {"genealogy": genealogy_data(ctx, family_of, groups)}
    pages["history"] = history_data(ctx, pages["genealogy"])
    for name, data in pages.items():
        with open(os.path.join(SITE, "data", f"{name}.json"), "w", encoding="utf-8", newline="\n") as f:
            if name == "genealogy":
                f.write(_columns(data))
            else:
                json.dump(data, f, ensure_ascii=False, indent=1)
                f.write("\n")
        if os.path.exists(os.path.join(TEMPLATES, f"{name}.html")):
            with open(os.path.join(SITE, f"{name}.html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(document(page(name, data)))
    write_static("privacy")
    write_static("graph")
    links = people_links(ctx)
    with open(os.path.join(SITE, "data", "bible", "people.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(_columns(links))
    g, h = pages["genealogy"], pages["history"]
    pairs = sum(len(ks) for b in links["verses"].values() for ks in b.values())
    return (f"Site: {len(g['n'])} people, {g['stats']['links']} parent-child links, {g['stats']['in_tree']} in the "
            f"tree of Adam's family; {pairs} people named in verses; "
            f"{len(h['items'])} world-history items in {len(h['streams'])} streams")

