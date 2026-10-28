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
</head>
<body>
{page}
</body>
</html>
"""


def page(name, data):
    """The page body (title, styles, markup, scripts) with its data inlined."""
    src = open(os.path.join(TEMPLATES, f"{name}.html"), encoding="utf-8").read()
    marker = "<!-- DATA -->"
    if marker not in src:
        raise ValueError(f"scripts/templates/{name}.html has no {marker} marker")
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
                f.write(STANDALONE.format(page=page(name, data)))
    g, h = pages["genealogy"], pages["history"]
    return (f"Site: {len(g['people'])} people, {g['stats']['links']} parent-child links; "
            f"{len(h['items'])} world-history items in {len(h['streams'])} streams")
