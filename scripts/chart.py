"""An open reconstruction of Adams' Synchronological Chart (1871) as SVG.

Sebastian C. Adams drew biblical and world history as parallel streams along one time
axis, using Archbishop Ussher's chronology. This chart does the same with open data:

  upper half  Bible history after Ussher/Jones (Theographic): the patriarchs' lifetimes,
              the judges and kingdoms, the kings of Israel and Judah, the prophets, the
              Gospels and Acts, and every dated event
  middle      synchronisms: each event the Bible narrates and outside evidence also dates,
              drawn at its Ussher date and at its modern date and joined by a line
  lower half  the surrounding nations and the wider world, at modern dates: eras and
              dynasties (data/periods.csv), rulers (data/rulers.csv), and world events and
              thinkers (data/world_events.csv)

One full chart and five era charts are written to connections/timeline/.
"""

import collections
import html
import re

from chronology import year_label

ERAS = [
    ("Creation to the Flood", -4003, -2347),
    ("The Flood to the Exodus", -2347, -1490),
    ("The Exodus to the Divided Kingdom", -1490, -974),
    ("The Divided Kingdom to the Return", -974, -535),
    ("The Return to the Apostles", -535, 100),
]

JUDAH = {"Rehoboam", "Abijam", "Asa", "Jehoshaphat", "Jehoram", "Ahaziah (Jehoahaz)", "Athaliah", "Joash",
         "Amaziah", "Uzziah", "Jotham", "Ahaz", "Hezekiah", "Manasseh", "Amon", "Josiah", "Jehoiakim",
         "Johoahaz (Shallum)", "Jeconiah", "Zedekiah"}  # "Johoahaz" is Theographic's spelling
ISRAEL = {"Jeroboam I", "Nadab", "Baasha", "Elah", "Tibni", "Omri", "Ahab", "Ahaziah", "Joram", "Jehu",
          "Jehoahaz", "Jehoash", "Jeroboam II", "Zachariah", "Shallum", "Menahem", "Pekahiah", "Pekah",
          "Hoshea", "Zimri"}
UNITED = {"Saul", "David", "Solomon"}

# (stream, colour) for the Bible half, top to bottom.
BIBLE_STREAMS = [
    ("Patriarchs", "#8c6d3f"), ("Judges and kingdom", "#6b8e23"), ("Kingdom of Israel", "#3b6ea5"),
    ("Kingdom of Judah", "#b03a2e"), ("Prophets", "#7d3c98"), ("Jesus and the apostles", "#138d75"),
    ("Other events", "#5d4e37"),
]
# Streams top to bottom, roughly west to east as on Adams' chart.
STREAM_ORDER = ["Egypt", "Sumer and Akkad", "Babylon", "Assyria", "Anatolia", "Aram", "Tyre", "Persia", "Greece",
                "Seleucid", "Rome", "Carthage", "Herodian", "Nabataea", "Roman officials", "High priests", "India",
                "China", "Thinkers and writers"]
WORLD_COLOURS = {
    "Tyre": "#884ea0", "Egypt": "#c9a227", "Aram": "#7f6a93", "Assyria": "#d35400", "Babylon": "#34495e",
    "Persia": "#16a085", "Greece": "#2e86c1", "Seleucid": "#5dade2", "Rome": "#922b21", "Herodian": "#a04000",
    "Nabataea": "#7f8c8d", "Roman officials": "#cd6155", "High priests": "#5d6d7e",
    "Sumer and Akkad": "#7b6d3a", "Anatolia": "#b9770e", "Carthage": "#6c3483", "India": "#ca6f1e",
    "China": "#c0392b", "Thinkers and writers": "#1f618d",
}

PAPER, INK, DECADE = "#fbf6e9", "#2b2116", "#e8c4bd"
ROW, GAP, LEFT, FONT = 18, 4, 170, "Georgia, 'Times New Roman', serif"


def stream_of(ev):
    t = ev["title"]
    if t.startswith("Lifetime of"):
        return "Patriarchs"
    if t.startswith("Prophecies of"):
        return "Prophets"
    if t.startswith("Reign of "):
        king = t[len("Reign of "):]
        if king in JUDAH:
            return "Kingdom of Judah"
        if king in ISRAEL:
            return "Kingdom of Israel"
        if king in UNITED:
            return "Judges and kingdom"
        raise ValueError(f"unclassified reign: {t}")
    if t in ("Southern Kingdom (Judah)",):
        return "Kingdom of Judah"
    if t in ("Northern Kingdom (Israel)",):
        return "Kingdom of Israel"
    if t.startswith(("Subjugation", "Deliverance", "Judgeship", "Usurpation", "Oppression", "Philistine",
                     "United Kingdom", "Sojourn", "Wilderness", "War with")):
        return "Judges and kingdom"
    if ev["year"] > 0:
        return "Jesus and the apostles"
    return "Other events"


def years_of(duration):
    """'40Y' -> 40.0, '7D' -> 7/365, '3M10D' -> 3 months 10 days, in years."""
    units = {"Y": 1, "M": 1 / 12, "W": 7 / 365, "D": 1 / 365}
    return sum(float(n) * units[u] for n, u in re.findall(r"([\d.]+)([YMWD])", duration or ""))


def pack(items, x, label_w):
    """Greedy lane assignment so bars and their labels don't overlap. items: [(start, end, ...)]."""
    lanes, out = [], []
    for it in sorted(items, key=lambda it: (it[0], -it[1])):
        # A label goes inside its bar when it fits, otherwise just after the bar's end.
        x0, bar_end = x(it[0]), x(it[1])
        x1 = bar_end if bar_end - x0 > label_w(it) else bar_end + label_w(it)
        for k, right in enumerate(lanes):
            if right + 6 <= x0:
                lanes[k] = x1
                out.append((k, it))
                break
        else:
            lanes.append(x1)
            out.append((len(lanes) - 1, it))
    return out, max(1, len(lanes))


def esc(s):
    return html.escape(str(s), quote=True)


def render(ctx, title, start, end, ppy):
    x = lambda y: LEFT + (y - start) * ppy
    width = int(x(end) + 220)  # room for labels of bars that end at the right edge
    text_w = lambda s, size=11: len(s) * size * 0.52
    parts, y = [], 0

    def text(tx, ty, s, size=11, anchor="start", weight="normal", fill=INK, extra=""):
        parts.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{size}" text-anchor="{anchor}" '
                     f'font-weight="{weight}" fill="{fill}" {extra}>{esc(s)}</text>')

    # Title block.
    text(LEFT, 34, title, 26, weight="bold")
    text(LEFT, 58, f"{year_label(start)} – {year_label(end)} · after Sebastian C. Adams, "
         "Synchronological Chart (1871) · open data: Theographic (CC BY-SA 4.0), STEPBible, Wikidata", 13)
    text(LEFT, 78, "Upper streams follow Ussher's chronology as Adams did (Jones/Theographic). "
         "Lower streams follow modern reign dates. Red connectors join the same event in both.", 12,
         fill="#6b5a45")
    y = 100

    def ticks():
        """(astronomical year, is_century) at round calendar years: 900 BC is -899."""
        for y in range(start, end + 1):
            cal = 1 - y if y <= 0 else y
            if cal % 10 == 0:
                yield y, cal % 100 == 0

    def axis(ay, top):
        for c, major in ticks():
            if True:
                parts.append(f'<line x1="{x(c):.1f}" y1="{ay}" x2="{x(c):.1f}" y2="{ay + (10 if major else 5)}" '
                             f'stroke="{INK}" stroke-width="{1.2 if major else 0.5}"/>')
                if major:
                    label = year_label(c) if top else f"AM {c + 4003}" if c + 4003 >= 0 else ""
                    text(x(c), ay + 24, label, 11, "middle")

    axis(y, True)
    y += 34
    grid_top = y

    # Bible streams.
    by_stream = collections.defaultdict(list)
    for ev in ctx.chron.events:
        dur = years_of(ev["duration"])
        if ev["year"] + dur < start or ev["year"] > end:
            continue
        by_stream[stream_of(ev)].append(ev)
    for name, colour in BIBLE_STREAMS:
        evs = by_stream.get(name, [])
        bars = [(ev["year"], ev["year"] + max(years_of(ev["duration"]), 0), ev) for ev in evs
                if years_of(ev["duration"]) >= 1]
        dots = [ev for ev in evs if years_of(ev["duration"]) < 1]
        if not bars and not dots:
            continue
        label = lambda it: text_w(it[2]["title"].replace("Lifetime of ", "").replace("Reign of ", "")
                                  .replace("Prophecies of ", "")) + 8
        placed, nlanes = pack(bars, x, label)
        dot_lane = nlanes if dots else 0
        h = (nlanes + (1 if dots else 0)) * (ROW + GAP)
        parts.append(f'<rect x="0" y="{y - 2}" width="{width}" height="{h + 4}" fill="{colour}" opacity="0.06"/>')
        text(12, y + 14, name, 13, weight="bold", fill=colour)
        for k, (s, e, ev) in placed:
            by = y + k * (ROW + GAP)
            s, e = max(s, start), min(e, end)
            short = ev["title"].replace("Lifetime of ", "").replace("Reign of ", "").replace("Prophecies of ", "")
            parts.append(f'<g><title>{esc(ev["title"])} · {year_label(ev["year"])} · {ev["duration"]}</title>'
                         f'<rect x="{x(s):.1f}" y="{by}" width="{max(x(e) - x(s), 2):.1f}" height="{ROW}" rx="3" '
                         f'fill="{colour}" opacity="0.85"/></g>')
            inside = x(e) - x(s) > text_w(short) + 8
            text(x(s) + 4 if inside else x(e) + 3, by + 13, short, 11, fill="#ffffff" if inside else colour)
        if dots:
            dy = y + dot_lane * (ROW + GAP) + ROW / 2
            parts.append(f'<line x1="{x(start):.1f}" y1="{dy}" x2="{x(end):.1f}" y2="{dy}" stroke="{colour}" '
                         f'stroke-width="0.4"/>')
            for ev in dots:
                parts.append(f'<g><title>{esc(ev["title"])} · {year_label(ev["year"])}</title>'
                             f'<circle cx="{x(ev["year"]):.1f}" cy="{dy}" r="3.2" fill="{colour}"/></g>')
        y += h + 14

    # Synchronisms.
    syncs = [s for s in ctx.syncs if s["ussher_y"] is not None and
             (start <= s["ussher_y"] <= end or start <= s["modern_y"] <= end)]
    if syncs:
        top, bottom = y + 34, y + 104
        parts.append(f'<rect x="0" y="{y}" width="{width}" height="{bottom - y + 16}" fill="#c0392b" opacity="0.05"/>')
        text(12, y + 14, "Synchronisms", 13, weight="bold", fill="#c0392b")
        text(12, top + 4, "Ussher", 11, fill="#6b5a45")
        text(12, bottom + 4, "Modern", 11, fill="#6b5a45")
        for ly in (top, bottom):
            parts.append(f'<line x1="{x(start):.1f}" y1="{ly}" x2="{x(end):.1f}" y2="{ly}" stroke="#6b5a45" '
                         f'stroke-width="0.6" stroke-dasharray="3 3"/>')
        for k, s in enumerate(sorted(syncs, key=lambda s: s["modern_y"])):
            u, m = s["ussher_y"], s["modern_y"]
            col = "#c0392b" if abs(u - m) > 5 else "#7f8c8d"
            parts.append(f'<g><title>{esc(s["event"])}: Ussher {year_label(u)}, modern {year_label(m)} '
                         f'({u - m:+d} years)</title>'
                         f'<line x1="{x(u):.1f}" y1="{top}" x2="{x(m):.1f}" y2="{bottom}" stroke="{col}" stroke-width="1.6"/>'
                         f'<circle cx="{x(u):.1f}" cy="{top}" r="3.5" fill="{col}"/>'
                         f'<circle cx="{x(m):.1f}" cy="{bottom}" r="3.5" fill="{col}"/></g>')
            text(x(u), top - 6 - (k % 3) * 11, s["event"], 9.5, "middle", fill=col)
        y = bottom + 30

    # World streams: eras and dynasties (pale), then rulers and figures (solid), per stream.
    streams = collections.OrderedDict((n, []) for n in STREAM_ORDER)
    for r in ctx.periods + ctx.rulers + [w for w in ctx.world_events if w["kind"] == "figure"]:
        if r["end_y"] >= start and r["start_y"] <= end:
            streams.setdefault(r["stream"], []).append(r)
    for name, rs in streams.items():
        if not rs:
            continue
        colour = WORLD_COLOURS.get(name, "#555")
        label = lambda it: text_w(it[2]["name"]) + 8
        tiers = [[r for r in rs if r.get("level") == "era"], [r for r in rs if r.get("level") == "dynasty"],
                 [r for r in rs if not r.get("level")]]
        s0, e0 = max(min(r["start_y"] for r in rs), start), min(max(r["end_y"] for r in rs), end)
        band_top = y
        text(12, y + 14, name, 13, weight="bold", fill=colour)
        for tier, items in enumerate(tiers):
            if not items:
                continue
            placed, nlanes = pack([(r["start_y"], r["end_y"], r) for r in items], x, label)
            for k, (s_, e_, r) in placed:
                by = y + k * (ROW + GAP)
                s_, e_ = max(s_, start), min(e_, end)
                opacity = (0.30, 0.50, 0.85)[tier] * (0.7 if r["approximate"] == "yes" else 1)
                parts.append(f'<g><title>{esc(r["name"])} · {year_label(r["start_y"])} – {year_label(r["end_y"])}'
                             f'{" (approximate)" if r["approximate"] == "yes" else ""}</title>'
                             f'<rect x="{x(s_):.1f}" y="{by}" width="{max(x(e_) - x(s_), 2):.1f}" height="{ROW}" rx="3" '
                             f'fill="{colour}" opacity="{opacity:.2f}"/></g>')
                inside = x(e_) - x(s_) > text_w(r["name"]) + 8
                ink = "#ffffff" if inside and tier == 2 else INK if inside else colour
                text(x(s_) + 4 if inside else x(e_) + 3, by + 13, r["name"], 11, fill=ink)
            y += nlanes * (ROW + GAP)
        parts.insert(0, f'<rect x="{x(s0):.1f}" y="{band_top - 2}" width="{x(e0) - x(s0):.1f}" '
                        f'height="{y - band_top + 4}" fill="{colour}" opacity="0.08" rx="6"/>')
        y += 12

    # World events: markers with staggered labels.
    wev = [w for w in ctx.world_events if w["kind"] == "event" and start <= w["start_y"] <= end]
    if wev:
        text(12, y + 14, "World events", 13, weight="bold", fill="#444")
        line_y = y + 8
        parts.append(f'<line x1="{x(start):.1f}" y1="{line_y}" x2="{x(end):.1f}" y2="{line_y}" stroke="#444" stroke-width="0.5"/>')
        for k, w in enumerate(sorted(wev, key=lambda w: w["start_y"])):
            parts.append(f'<g><title>{esc(w["name"])} · {"c. " if w["approximate"] == "yes" else ""}'
                         f'{year_label(w["start_y"])}</title><circle cx="{x(w["start_y"]):.1f}" cy="{line_y}" r="4" '
                         f'fill="#444"/></g>')
            text(x(w["start_y"]) + 6, line_y + 16 + (k % 2) * 13, w["name"], 10.5, fill="#444")
        y += 52

    # Century pillars and decade lines behind everything, then the bottom axis.
    grid = []
    for c, major in ticks():
        if True:
            grid.append(f'<line x1="{x(c):.1f}" y1="{grid_top - 6}" x2="{x(c):.1f}" y2="{y}" '
                        f'stroke="{INK if major else DECADE}" stroke-width="{1.4 if major else 0.6}" '
                        f'opacity="{0.55 if major else 0.8}"/>')
    axis(y, False)
    text(LEFT, y + 46, "AM = year of the world as Ussher counts it (4004 − BC year). Hover over a bar for details.",
         11, fill="#6b5a45")
    height = y + 64
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" font-family="{FONT}">'
            f'<rect width="100%" height="100%" fill="{PAPER}"/>' + "".join(grid) + "".join(parts) + "</svg>\n")


def write_charts(ctx, out_dir):
    """Returns [(title, file name)] for the full chart and the era charts."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    files = []
    full_start, full_end = -4003, 100
    svg = render(ctx, "A Synchronological Chart of Bible and World History", full_start, full_end, 3)
    files.append(("The whole chart", "synchronological-chart.svg"))
    with open(os.path.join(out_dir, files[-1][1]), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    for k, (title, s, e) in enumerate(ERAS, 1):
        ppy = max(2.0, 2800 / (e - s))
        name = f"synchronological-chart-{k}.svg"
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(render(ctx, title, s, e, ppy))
        files.append((title, name))
    return files
