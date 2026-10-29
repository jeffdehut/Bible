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
    ents, gen = ctx.entities, ctx.gen
    people = [i for i, e in enumerate(ents) if e["kind"] == "person"]
    pos = {i: k for k, i in enumerate(people)}
    out = []
    for i in people:
        e = ents[i]
        rec = {"n": e["name"], "t": ctx.title(i)}
        if not e["named"]:
            rec["u"] = 1
        if gen.sex.get(i) in ("Male", "Female"):
            rec["s"] = gen.sex[i][0]
        if gen.tribe.get(i):
            rec["tr"] = gen.tribe[i]
        if e["brief"]:
            rec["b"] = e["brief"]
        if e["aliases"]:
            rec["a"] = e["aliases"]
        forms = [f for f, _ in e["forms"] if f and not re.fullmatch(r"[\w\s.'-]*", f, re.A)]
        if forms:
            rec["o"] = forms[:4]
        rec["f"] = ref_label(*e["first"])
        rec["v"] = len(e["verses"])
        if i in ctx.born:
            rec["by"] = ctx.born[i]
        if i in ctx.died:
            rec["dy"] = ctx.died[i]
        parents = [[pos[p], {"father": "f", "mother": "m"}.get(edge["role"], ""),
                    "".join(sorted(f for f in edge["flags"] if f in "a?"))]
                   for p, edge in gen.parents[i] if p in pos]
        if parents:
            rec["p"] = parents
        for key, rel in (("sp", gen.partners), ("sb", gen.siblings)):
            js = sorted(pos[j] for j in rel.get(i, {}) if j in pos)
            if js:
                rec[key] = js
        if i in family_of:
            rec["g"] = family_of[i][1]
        out.append(rec)
    by_root = []
    for path, root, members, gens in groups[:40]:
        by_root.append({"r": pos[root], "m": len(members), "g": max(gens.values())})
    jesus = next((i for i in people if ents[i]["id"].startswith("Jesus@Isa.7.14")), None)
    line = [pos[k] for k in gen.paternal_line(jesus)] if jesus is not None else []
    stats = {"people": sum(1 for i in people if ents[i]["named"]), "unnamed": sum(1 for i in people if not ents[i]["named"]),
             "links": sum(1 for (p, c) in gen.parent_edges if p in pos and c in pos),
             "families": len(groups), "largest": len(groups[0][2]), "generations": max(groups[0][3].values())}
    return {"people": out, "families": by_root, "line": line, "stats": stats}


def history_data(ctx):
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
    syncs = [{"n": s["event"], "ref": ref_label(*s["verse"]), "m": s["modern_y"], "us": s["ussher_y"],
              "c": 1 if s["approximate"] == "yes" else 0, "ev": s["evidence"]} for s in ctx.syncs]
    used = {r["s"] for r in out}
    streams = [{"name": s, "group": group_of[s]} for s in order if s in used]
    return {"streams": streams, "groups": [g for g, _ in STREAM_GROUPS], "items": out, "syncs": syncs,
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
    return (f'<link rel="icon" href="{root}icons/icon.svg" type="image/svg+xml">\n'
            f'<link rel="apple-touch-icon" href="{root}icons/icon-192.png">\n'
            f'<meta name="theme-color" content="{light}" media="(prefers-color-scheme: light)">\n'
            f'<meta name="theme-color" content="{dark}" media="(prefers-color-scheme: dark)">\n{THEME}')


def document(body, root="", colors=("#fbfaf7", "#0d111b")):
    return STANDALONE.format(head=head(root, colors), page=body)


# The bar across the top of the pages beside the reader: the name, which leads to the reader,
# and the four parts of the site, with the one shown marked. It takes the page's own colors
# (--bg, --ink, --muted, --line, --lapis, --lapis-soft), so it sits on any of them.
NAV = [("index.html", "Read"), ("maps/index.html", "Maps"), ("genealogy.html", "Genealogy"),
       ("history.html", "Timeline")]
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
.appnav { margin-inline-start: auto; display: flex; gap: 2px; }
.appnav a {
  display: inline-flex; align-items: center; min-height: 40px; padding: 0 12px; border-radius: 10px; white-space: nowrap;
  font: 600 14px/1 "Libre Franklin", system-ui, -apple-system, "Segoe UI", sans-serif; color: var(--muted); text-decoration: none;
}
.appnav a:hover { background: var(--lapis-soft); color: var(--ink); }
.appnav a[aria-current="page"] { background: var(--lapis-soft); color: var(--lapis); }
.appbar a:focus-visible { outline: 2px solid var(--lapis); outline-offset: 0; }
@media (max-width: 640px) { .appbar .brand span { display: none; } .appnav a { padding: 0 9px; } }
@media (max-width: 359px) { .appbar .brand { display: none; } .appnav { margin-inline: auto; } }
@media print { .appbar { display: none; } }
</style>"""


def appbar(current, root=""):
    """The shared bar, for the page whose address (from the site root) is `current`."""
    mark = ' aria-current="page"'
    links = "".join(f'<a href="{root}{href}"{mark if href == current else ""}>{text}</a>' for href, text in NAV)
    return (f'{APPBAR_CSS}\n<header class="appbar">\n'
            f'  <a class="brand" href="{root}index.html"><img src="{root}icons/icon.svg" alt="Plain English Bible">'
            f'<span aria-hidden="true">Plain English Bible</span></a>\n'
            f'  <nav class="appnav" aria-label="Plain English Bible">{links}</nav>\n</header>')


def page(name, data):
    """The page body (title, styles, markup, scripts) with its data inlined."""
    src = open(os.path.join(TEMPLATES, f"{name}.html"), encoding="utf-8").read()
    marker = "<!-- DATA -->"
    if marker not in src:
        raise ValueError(f"scripts/templates/{name}.html has no {marker} marker")
    src = src.replace("<!-- APPBAR -->", appbar(f"{name}.html"))
    return src.replace(marker, f'<script type="application/json" id="data">{_dump(data)}</script>')


def build(ctx, family_of, groups):
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    pages = {"genealogy": genealogy_data(ctx, family_of, groups), "history": history_data(ctx)}
    for name, data in pages.items():
        with open(os.path.join(SITE, "data", f"{name}.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write("\n")
        if os.path.exists(os.path.join(TEMPLATES, f"{name}.html")):
            with open(os.path.join(SITE, f"{name}.html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(document(page(name, data)))
    g, h = pages["genealogy"], pages["history"]
    return (f"Site: {len(g['people'])} people, {g['stats']['links']} parent-child links; "
            f"{len(h['items'])} world-history items in {len(h['streams'])} streams")
