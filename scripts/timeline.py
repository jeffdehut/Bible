"""Genealogy and timeline notes for connections/ (called from connections.py).

  connections/genealogy/   one note per family group, each a register by generation, and
                           an index with the cross-check against Theographic
  connections/events/      one note per Theographic event (dates after Floyd Nolen Jones)
  connections/timeline/    one note per century from Creation (4004 BC) to the 1st century
                           AD, in the manner of Adams' Synchronological Chart: Bible events,
                           births and deaths, the passages dated to that century (Ussher),
                           and the foreign rulers reigning then (modern dates)
"""

import collections
import datetime
import csv
import os

from chronology import century_label, century_of, year_label
from genealogy import flag_note
from notes import ROOT, chapter_path, frontmatter, link, ref_label, safe_filename, write

EVENTS = "connections/events"
WORLD = "connections/world"
TIMELINE = "connections/timeline"
GENEALOGY = "connections/genealogy"
MAX_TREE = 24  # most siblings/children drawn in a person's family tree


PRESENT = datetime.date.today().year  # the end year of anything still running ("present")


def parse_year(s):
    """'745 BC' / 'AD 14' / 'present' -> astronomical year."""
    s = s.strip()
    if s == "present":
        return PRESENT
    return 1 - int(s[:-3]) if s.endswith("BC") else int(s[3:])


def end_label(r):
    """The end of a ruler, period or life: 'present' for one still running."""
    return "present" if r.get("end") == "present" else year_label(r["end_y"])


def century_path(c):
    return f"{TIMELINE}/{century_label(c)}"


def year_link(y, label=None):
    return link(century_path(century_of(y)), label or year_label(y))


class Context:
    """Everything the timeline and genealogy notes need, built once in connections.main()."""

    def __init__(self, entities, texts, gen, chron, vers):
        self.entities, self.texts, self.gen, self.chron, self.vers = entities, texts, gen, chron, vers
        self.title = lambda i: entities[i]["path"].rsplit("/", 1)[-1]
        self.by_id = {e["id"]: i for i, e in enumerate(entities)}
        self.person_of, self.ambiguous_people = chron.crosswalk(entities, "person")
        self.place_of, self.ambiguous_places = chron.crosswalk(entities, "place")
        # Jones birth/death years by entity.
        self.born, self.died = {}, {}
        for tid, i in self.person_of.items():
            f = chron.people[tid]
            if f.get("birthYear"):
                self.born[i] = int(f["birthYear"])
            if f.get("deathYear"):
                self.died[i] = int(f["deathYear"])
        # Events.
        titles = collections.Counter(safe_filename(e["title"]) for e in chron.events)
        for ev in chron.events:
            t = safe_filename(ev["title"])
            ev["path"] = f"{EVENTS}/{t if titles[t] == 1 else f'{t} ({year_label(ev['year'])})'}"
            ev["people"] = sorted({self.person_of[p] for p in ev["participants"] if p in self.person_of})
            ev["places"] = sorted({self.place_of[p] for p in ev["locations"] if p in self.place_of})
        self.event_by_tid = {ev["tid"]: ev for ev in chron.events}
        self.events_of = collections.defaultdict(list)
        for ev in chron.events:
            for i in ev["people"] + ev["places"]:
                self.events_of[i].append(ev)
        # Chapter dates (Ussher) from verse years.
        self.chapter_years = collections.defaultdict(list)
        for (b, c, v), y in chron.verse_year.items():
            self.chapter_years[(b, c)].append(y)
        self.chapter_span = {k: (min(v), max(v)) for k, v in self.chapter_years.items()}
        # Rulers and synchronisms.
        self.rulers = []
        with open(os.path.join(ROOT, "data", "rulers.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                r["start_y"], r["end_y"] = parse_year(r["start"]), parse_year(r["end"])
                r["entity"] = self.by_id.get(r["tipnr"])
                self.rulers.append(r)
        self.ruler_of = {r["entity"]: r for r in self.rulers if r["entity"] is not None}
        # Periods, world events and figures (modern dates); each without a Bible person
        # gets a note in connections/world/.
        self.periods, self.world_events = [], []
        for name, target in (("periods.csv", self.periods), ("world_events.csv", self.world_events)):
            with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    r["start_y"] = parse_year(r["start"])
                    r["end_y"] = parse_year(r["end"]) if r["end"] else r["start_y"]
                    target.append(r)
        for r in self.rulers + self.periods + self.world_events:
            if r.get("entity") is None:
                r["path"] = f"{WORLD}/{safe_filename(r['name'])}"
        self.syncs = []
        with open(os.path.join(ROOT, "data", "synchronisms.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                b, c, v = r["ref"].split(".")
                ref = vers.hebrew(b, int(c), int(v))
                r["verse"] = ref
                r["modern_y"] = parse_year(r["modern_date"])
                r["ussher_y"], r["ussher_from"] = self.verse_year(ref)
                self.syncs.append(r)

    def verse_year(self, ref):
        """(Ussher year, ref it came from): the verse's own date, else the nearest dated
        verse in the same chapter."""
        y = self.chron.verse_year.get(ref)
        if y is not None:
            return y, ref
        b, c, v = ref
        near = sorted((abs(vv - v), vv) for (bb, cc, vv) in self.chron.verse_year if (bb, cc) == (b, c))
        if near:
            r2 = (b, c, near[0][1])
            return self.chron.verse_year[r2], r2
        return None, None

    def ussher_median(self, i):
        """Median Ussher date of the verses naming a person or place. Genealogies and
        later references make the full range misleading (David is named in passages dated
        from 1752 BC to AD 96); the median places David at 1036 BC."""
        ys = sorted(self.chron.verse_year[r] for r in self.entities[i]["verses"] if r in self.chron.verse_year)
        return ys[len(ys) // 2] if ys else None

    def elink(self, i, extra=""):
        return link(self.entities[i]["path"], self.title(i) + extra)


# ---------------------------------------------------------------- person notes

def mermaid_tree(ctx, i):
    g, ids, lines = ctx.gen, {}, ["```mermaid", "flowchart TB"]

    def node(j, cls=None):
        if j not in ids:
            ids[j] = f"n{len(ids)}"
            label = ctx.title(j).replace('"', "'")
            lines.append(f'  {ids[j]}["{label}"]' + (f":::{cls}" if cls else ""))
        return ids[j]

    me = node(i, "me")
    parents = [p for p, _ in g.parents[i]]
    for p in parents:
        for gp, _ in g.parents[p]:
            lines.append(f"  {node(gp)} --> {node(p)}")
        lines.append(f"  {node(p)} --> {me}")
    sibs = sorted(g.siblings[i])[:MAX_TREE]
    for s in sibs:
        for p in parents:
            if any(pp == p for pp, _ in g.parents[s]):
                lines.append(f"  {node(p)} --> {node(s)}")
                break
        else:
            lines.append(f"  {me} ~~~ {node(s)}")
    for sp in sorted(g.partners[i]):
        lines.append(f"  {me} -.- {node(sp, 'spouse')}")
    kids = [c for c, _ in g.children[i]]
    for c in kids[:MAX_TREE]:
        lines.append(f"  {me} --> {node(c)}")
    lines += ["  classDef me stroke-width:3px", "  classDef spouse stroke-dasharray:4", "```"]
    more = len(g.siblings[i]) - len(sibs) + max(0, len(kids) - MAX_TREE)
    if len(ids) < 2:
        return []
    return lines + ([f"*{more} more relatives are listed above but not drawn.*"] if more > 0 else [])


def person_sections(ctx, i, family_of):
    """Extra sections for a person note: dates, family, world history, events."""
    e, g, out = ctx.entities[i], ctx.gen, []
    # Dates.
    dates = []
    if i in ctx.born or i in ctx.died:
        b = year_link(ctx.born[i]) if i in ctx.born else "?"
        d = year_link(ctx.died[i]) if i in ctx.died else "?"
        dates.append(f"- **Lived:** {b} – {d} *(Jones)*")
    med = ctx.ussher_median(i)
    if med is not None:
        dates.append(f"- **Placed around:** {year_link(med)} *(Ussher: the median date of the passages naming them)*")
    r = ctx.ruler_of.get(i)
    if r:
        wd = f" · [Wikidata {r['wikidata']}](https://www.wikidata.org/wiki/{r['wikidata']})" if r["wikidata"] else ""
        dates.append(f"- **Reigned / in office:** {'c. ' if r['approximate'] == 'yes' else ''}"
                     f"{year_link(r['start_y'])} – {year_link(r['end_y'])} *(modern dates)* · "
                     f"{r['name']}, {r['stream']}{wd}" + (f" · {r['note']}" if r["note"] else ""))
    if dates:
        out += ["## When", ""] + dates + [""]
    # Family.
    fam = []
    for role, label in (("father", "Father"), ("mother", "Mother"), (None, "Parent")):
        ps = [(p, ed) for p, ed in g.parents[i] if ed["role"] == role]
        if ps:
            fam.append(f"- **{label}:** " + ", ".join(ctx.elink(p, flag_note(ed["flags"])) for p, ed in ps))
    for rel, label in ((g.siblings, "Brothers and sisters"), (g.partners, "Spouses")):
        if rel[i]:
            fam.append(f"- **{label}:** " + ", ".join(ctx.elink(j, flag_note(fl)) for j, fl in sorted(rel[i].items())))
    if g.children[i]:
        fam.append("- **Children:** " + ", ".join(ctx.elink(c, flag_note(ed["flags"])) for c, ed in g.children[i]))
    if g.tribe.get(i):
        fam.append(f"- **Tribe or nation:** {g.tribe[i]}")
    if fam:
        out += ["## Family", ""] + fam + [""]
        line = g.paternal_line(i)
        if len(line) > 2:
            out += [f"**Line of descent** ({len(line)} generations, father to son): "
                    + " → ".join(ctx.elink(j) for j in line[:-1]) + f" → **{ctx.title(i)}**", ""]
        if i in family_of:
            path, gen = family_of[i]
            out += [f"**Family group:** {link(path)}, generation {gen}", ""]
        out += mermaid_tree(ctx, i) + [""]
    # Events.
    evs = ctx.events_of.get(i, [])
    if evs:
        out += ["## Events", ""] + [f"- {year_link(ev['year'])} · {link(ev['path'], ev['title'])}" for ev in evs] + [""]
    return out


def person_frontmatter(ctx, i, family_of):
    fields = {}
    if i in ctx.born:
        fields["born"], fields["born_year"] = year_label(ctx.born[i]), ctx.born[i]
    if i in ctx.died:
        fields["died"], fields["died_year"] = year_label(ctx.died[i]), ctx.died[i]
    med = ctx.ussher_median(i)
    if med is not None:
        fields["placed"], fields["placed_year"] = year_label(med), med
    if i in family_of:
        fields["generation"] = family_of[i][1]
    if ctx.gen.sex.get(i) in ("Male", "Female"):
        fields["sex"] = ctx.gen.sex[i].lower()
    return fields


# ---------------------------------------------------------------- genealogy

def family_groups(ctx):
    """Assign every person in a parent-child group to a family note. Returns
    ({entity: (path, generation)}, [(path, root, members, generations)])."""
    family_of, groups = {}, []
    for root, members, gens in ctx.gen.families():
        # Where a person's father-to-son line reaches the founder, count generations along
        # it, so the number matches the line of descent shown on their note; otherwise
        # use the longest line through any recorded parent.
        for m in members:
            line = ctx.gen.paternal_line(m)
            if line[0] == root:
                gens[m] = len(line)
        lo = min(gens.values())
        gens = {k: v - lo + 1 for k, v in gens.items()}
        path = f"{GENEALOGY}/Family of {ctx.title(root)}"
        groups.append((path, root, members, gens))
        for m in members:
            family_of[m] = (path, gens.get(m, 0))
    return family_of, groups


def write_genealogy(ctx, groups, crosscheck):
    g = ctx.gen
    for path, root, members, gens in groups:
        lines = frontmatter({"type": "family", "root": ctx.title(root), "people": len(members),
                             "generations": max(gens.values()), "tags": ["genealogy"]})
        lines += [f"# {path.rsplit('/', 1)[-1]}", "",
                  f"{len(members)} people over {max(gens.values())} generations, counted down from "
                  f"{ctx.elink(root)}. Generations follow parent-child links in TIPNR; an "
                  "*ancestor* link (TIPNR flag `(a)`) counts as one step but may span several. "
                  "People who join through marriage only appear under their own families.", "",
                  f"[[{GENEALOGY}/Genealogy|All families]]", ""]
        by_gen = collections.defaultdict(list)
        for m in members:
            by_gen[gens.get(m, 0)].append(m)
        for n in sorted(by_gen):
            lines += [f"## Generation {n}", ""]
            for m in sorted(by_gen[n], key=lambda m: ctx.title(m)):
                ps = [ctx.elink(p) + flag_note(ed["flags"]) for p, ed in g.parents[m]]
                lines.append(f"- {ctx.elink(m)}" + (f" — child of {' & '.join(ps)}" if ps else ""))
            lines.append("")
        write(path, lines)

    agree, theo_only, diffs = crosscheck
    lines = frontmatter({"type": "index", "tags": ["genealogy"]})
    lines += ["# Genealogy", "",
              f"Every family relationship recorded in STEPBible's TIPNR, for {sum(len(m) for _, _, m, _ in groups):,} "
              f"people in {len(groups)} family groups. Each person note has a **Family** section with "
              "parents, siblings, spouses and children, a family tree, and the line of descent "
              "from father to son as far back as the records go.", "",
              "## Notes on the data", "",
              "- **Uncertain links** are marked *(uncertain)*: TIPNR's `(?)` flag. *(ancestor)* marks "
              "a link to an ancestor rather than a parent, e.g. where a genealogy skips generations.",
              "- **Unnamed people** the text mentions (\"the wife of Heli\") are included when a line "
              "of descent passes through them.",
              "- **TIPNR's own placeholders are left out.** TIPNR fills two gaps with unnamed generations "
              "of its own: nine between Matthan and Jacob, to match the count of Luke 3, and four between "
              "Ithamar and Eli. No verse names or counts them. Matthew 1:15 calls Matthan the father of "
              "Jacob, so they are joined as father and son; Eli is linked to Ithamar as a descendant "
              "*(ancestor)*, since no verse says how many generations came between.",
              "- **Luke's genealogy** includes Cainan between Arpachshad and Shelah (Luke 3:36). He "
              "is not in Genesis 11 in the Hebrew text, but TIPNR includes him in the line.",
              "- **Mary** is given as the daughter of Heli, following the reading of Luke 3:23 as "
              "Mary's line.",
              "- **Israel** is the patriarch Jacob; TIPNR files him under that name.", "",
              "## Cross-check with Theographic", "",
              f"Theographic records parents independently. Where both datasets name a parent for the same "
              f"person, **{agree:,} links agree** and **{len(diffs)} differ**; {theo_only} more are in "
              "Theographic only. The differences are usually different identifications of people "
              "with the same name:", "",
              "| Person | Theographic says | TIPNR says |", "|---|---|---|"]
    lines += [f"| {ctx.elink(c)} | {role}: {ctx.elink(p)} | "
              f"{', '.join(ctx.elink(x) for x in tip) or '—'} |" for c, role, p, tip in diffs]
    lines += ["", "## Families", "", "| Family | People | Generations |", "|---|---|---|"]
    lines += [f"| {link(path)} | {len(members)} | {max(gens.values())} |"
              for path, root, members, gens in groups if len(members) > 2]
    small = [link(path) for path, root, members, gens in groups if len(members) <= 2]
    lines += ["", f"**Families of two:** " + " · ".join(small), ""]
    write(f"{GENEALOGY}/Genealogy", lines)


def genealogy_crosscheck(ctx):
    agree = theo_only = 0
    diffs = []
    for tid, c in sorted(ctx.person_of.items(), key=lambda kv: ctx.title(kv[1])):
        f = ctx.chron.people[tid]
        tipnr = [p for p, ed in ctx.gen.parents[c] if "a" not in ed["flags"]]
        for role in ("father", "mother"):
            for pt in f.get(role) or []:
                if pt not in ctx.person_of:
                    continue
                p = ctx.person_of[pt]
                if p in tipnr:
                    agree += 1
                elif not tipnr:
                    theo_only += 1
                else:
                    diffs.append((c, role, p, tipnr))
    return agree, theo_only, diffs


# ---------------------------------------------------------------- events and timeline

def write_events(ctx):
    for ev in ctx.chron.events:
        lines = frontmatter({"type": "event", "year": ev["year"], "date": year_label(ev["year"]),
                             "duration": ev["duration"], "tags": ["event"]})
        lines += [f"# {ev['title']}", "", f"**When:** {year_link(ev['year'])}"
                  + (f" · lasting {ev['duration']}" if ev["duration"] and ev["duration"] != "1D" else "")
                  + " *(Jones's chronology, via Theographic)*", ""]
        if ev["people"]:
            lines.append("**People:** " + ", ".join(ctx.elink(i) for i in ev["people"]))
        if ev["places"]:
            lines.append("**Places:** " + ", ".join(ctx.elink(i) for i in ev["places"]))
        chs = []
        for b, c, v in ev["verses"]:
            if (b, c) in ctx_chapters(ctx) and (b, c) not in [x[:2] for x in chs]:
                chs.append((b, c, v))
        if chs:
            lines.append("**Passages:** " + ", ".join(link(chapter_path(b, c), ref_label(b, c, v)) for b, c, v in chs))
        for key, label in (("predecessor", "Follows"), ("part_of", "Part of")):
            rel = [ctx.event_by_tid[t] for t in ev[key] if t in ctx.event_by_tid]
            if rel:
                lines.append(f"**{label}:** " + ", ".join(link(r["path"], r["title"]) for r in rel))
        write(ev["path"], lines + [""])


def ctx_chapters(ctx):
    if not hasattr(ctx, "_chapters"):
        ctx._chapters = {(b, c) for b, vs in ctx.texts.items() for c, _ in vs}
    return ctx._chapters


def write_timeline(ctx, order):
    """One note per century, from Creation to the latest century in the world-history data."""
    first = century_of(min(ev["year"] for ev in ctx.chron.events))
    last = century_of(max(max(ev["year"] for ev in ctx.chron.events), max(y for _, y in ctx.chapter_span.values()),
                          max(r["end_y"] for r in ctx.rulers + ctx.periods + ctx.world_events)))
    cents = [c for c in range(first, last + 1) if c != 0]
    chapters_in = collections.defaultdict(list)
    for (b, c), (lo, hi) in ctx.chapter_span.items():
        for cent in range(century_of(lo), century_of(hi) + 1):
            if cent:
                chapters_in[cent].append((b, c))
    for k, cent in enumerate(cents):
        nav = []
        if k:
            nav.append("← " + link(century_path(cents[k - 1])))
        nav.append(link(f"{TIMELINE}/Synchronisms", "Synchronisms"))
        nav.append(link(f"{TIMELINE}/Synchronological Chart", "Chart"))
        if k + 1 < len(cents):
            nav.append(link(century_path(cents[k + 1])) + " →")
        lo_y = -(abs(cent) * 100) + 1 if cent < 0 else (cent - 1) * 100 + 1
        hi_y = lo_y + 99
        lines = frontmatter({"type": "century", "century": century_label(cent), "from": year_label(lo_y),
                             "to": year_label(hi_y), "tags": ["timeline"]})
        lines += [f"# {century_label(cent)}", "", f"{year_label(lo_y)} – {year_label(hi_y)}", "", " · ".join(nav), ""]
        evs = [ev for ev in ctx.chron.events if century_of(ev["year"]) == cent]
        if evs:
            lines += ["## Bible events *(Jones)*", ""]
            lines += [f"- {year_label(ev['year'])} · {link(ev['path'], ev['title'])}" for ev in evs] + [""]
        births = sorted((y, i) for i, y in ctx.born.items() if century_of(y) == cent)
        deaths = sorted((y, i) for i, y in ctx.died.items() if century_of(y) == cent)
        if births or deaths:
            lines += ["## Births and deaths *(Jones)*", ""]
            lines += [f"- {year_label(y)} · born: {ctx.elink(i)}" for y, i in births]
            lines += [f"- {year_label(y)} · died: {ctx.elink(i)}" for y, i in deaths] + [""]
        current = lambda r: century_of(r["start_y"]) <= cent <= century_of(r["end_y"])
        rulers = [r for r in ctx.rulers if current(r)]
        periods = [r for r in ctx.periods if current(r)]
        worldev = [r for r in ctx.world_events if current(r)]
        syncs = [s for s in ctx.syncs if cent in (century_of(s["modern_y"]),
                                                    century_of(s["ussher_y"]) if s["ussher_y"] is not None else None)]
        if rulers or periods or worldev or syncs:
            lines += ["## World history *(modern dates)*", ""]
            by_stream = collections.OrderedDict()
            for r in periods + rulers:
                by_stream.setdefault(r["stream"], []).append(r)
            for stream, rs in by_stream.items():
                lines.append(f"- **{stream}:** " + ", ".join(
                    world_link(ctx, r) + f" {year_label(r['start_y'])}–{end_label(r)}" for r in rs))
            for r in worldev:
                when = year_label(r["start_y"]) if r["kind"] == "event" else f"{year_label(r['start_y'])}–{end_label(r)}"
                lines.append(f"- **{'Event' if r['kind'] == 'event' else r['stream']}:** {world_link(ctx, r)} {when}")
            for s in syncs:
                u = year_label(s["ussher_y"]) if s["ussher_y"] is not None else "—"
                lines.append(f"- **Synchronism:** {s['event']} ({link(chapter_path(*s['verse'][:2]), ref_label(*s['verse']))}) "
                             f"— modern {s['modern_date']}, Ussher {u}")
            lines.append("")
        chs = sorted(chapters_in.get(cent, []), key=lambda bc: (order.index(bc[0]), bc[1]))
        if chs:
            lines += [f"## Passages dated to this century *(Ussher)*", "",
                      " · ".join(link(chapter_path(b, c), ref_label(b, c)) for b, c in chs), ""]
        write(century_path(cent), lines)
    return cents


def write_synchronisms(ctx):
    lines = frontmatter({"type": "index", "tags": ["timeline"]})
    lines += ["# Synchronisms", "",
              "Adams' *Synchronological Chart* (1871) set biblical history side by side with the "
              "nations around Israel, dated by Archbishop Ussher's chronology. The events below "
              "are those the Bible narrates and outside evidence (Assyrian annals, Babylonian "
              "chronicles, inscriptions, Roman historians) also dates. Comparing the two shows "
              "where Ussher's chronology, and so Adams' chart, departs from modern dating.", "",
              "| Event | Passage | Ussher | Modern | Ussher − modern | Evidence |", "|---|---|---|---|---|---|"]
    for s in ctx.syncs:
        u = s["ussher_y"]
        diff = f"{u - s['modern_y']:+d} years" if u is not None else "—"
        if u is not None and u - s["modern_y"] == 0:
            diff = "0"
        note = "" if s["ussher_from"] in (s["verse"], None) else f" (from {ref_label(*s['ussher_from'])})"
        lines.append(f"| {s['event']} | {link(chapter_path(*s['verse'][:2]), ref_label(*s['verse']))} | "
                     f"{year_link(u) + note if u is not None else '—'} | "
                     f"{'c. ' if s['approximate'] == 'yes' else ''}{year_link(s['modern_y'])} | {diff} | {s['evidence']} |")
    lines += ["", "*Negative differences mean Ussher dates the event earlier.* Ussher's dates are the "
              "marginal dates of the *Treasury of Scripture Knowledge* as recorded by Theographic. "
              "In the divided monarchy they run 30–45 years earlier than modern dates, which count "
              "overlapping reigns (co-regencies) from the Assyrian eponym lists. From Josiah on, "
              "the two agree within a few years.", "",
              "## Rulers", "", "| Stream | Ruler | In the Bible | Reign (modern) | Wikidata |", "|---|---|---|---|---|"]
    for r in ctx.rulers:
        who = ctx.elink(r["entity"]) if r["entity"] is not None else (r["biblical_name"] or "—")
        wd = f"[{r['wikidata']}](https://www.wikidata.org/wiki/{r['wikidata']})" if r["wikidata"] else "—"
        lines.append(f"| {r['stream']} | {r['name']} | {who} | {'c. ' if r['approximate'] == 'yes' else ''}"
                     f"{year_link(r['start_y'])} – {year_link(r['end_y'])} | {wd} |")
    lines += ["", "Reign dates are conventional modern dates; *c.* marks approximate ones. The curated "
              "lists are in `data/rulers.csv` and `data/synchronisms.csv`.", ""]
    write(f"{TIMELINE}/Synchronisms", lines)


def write_chart_note(ctx):
    import chart
    files = chart.write_charts(ctx, os.path.join(ROOT, TIMELINE))
    lines = frontmatter({"type": "chart", "tags": ["timeline"]})
    lines += ["# Synchronological Chart", "",
              "An open reconstruction of Sebastian C. Adams' *Synchronological Chart, or Map of History* "
              "(1871), which drew Bible history and world history as parallel streams along one time axis "
              "using Archbishop Ussher's chronology.", "",
              "- **Upper streams:** Bible history after Ussher's chronology, as Adams used it. Lifetimes, reigns "
              "and events come from Theographic, which follows Floyd Nolen Jones's refinement of Ussher.",
              "- **Synchronisms:** each event the Bible narrates that outside evidence also dates, drawn at "
              "its Ussher date (upper dot) and its modern date (lower dot). Red lines mark differences of "
              "more than five years. See [[connections/timeline/Synchronisms|Synchronisms]].",
              "- **Lower streams:** the wider world at modern dates: Egypt, Sumer and Akkad, Babylon, "
              "Assyria, the Hittites and Lydia, Aram, Tyre, Persia, Greece, the Seleucids, Rome, Carthage, the "
              "Herods and Roman officials, India and China; from about AD 30 also the Byzantine Empire, Europe, "
              "Russia, the Islamic world, the Mongols, Japan, Africa, the Americas, Jewish history, the Church and "
              "the transmission of the Bible's text. Each stream shows eras (palest), then dynasties, "
              "then rulers. A lane of thinkers and writers and a lane of world events come last. Each item has a "
              "note in `connections/world/` (or its Bible person's note).",
              "- **Two chronologies side by side:** the upper streams follow Ussher, as Adams did, and the "
              "lower ones follow modern dating. Before about 1000 BC the two diverge widely. For example, on "
              "modern dates Egypt's Old Kingdom and Sumer's city-states run straight through Ussher's date for "
              "the Flood (2348 BC). The chart shows both as they are dated and doesn't try to reconcile them.",
              "- **Axis:** black lines mark centuries and pink lines decades, as on Adams' chart; "
              "years of the world (AM) run along the bottom.", "",
              "Each era chart is wider and easier to read than the whole. Open an SVG in a web browser to zoom "
              "and to see details when you hover over a bar.", ""]
    for title, name in files[1:] + files[:1]:
        lines += [f"## {title}", "", f"![[{TIMELINE}/{name}]]", ""]
    write(f"{TIMELINE}/Synchronological Chart", lines)
    return files


def world_link(ctx, r):
    """Link a ruler, period, event or figure: to the Bible person's note when there is one,
    otherwise to its note in connections/world/."""
    if r.get("entity") is not None:
        extra = f" ({r['name']})" if r.get("biblical_name") and r["biblical_name"] != r["name"] else ""
        return ctx.elink(r["entity"], extra)
    return link(r["path"], r["name"])


def write_world(ctx):
    """One note per period, non-biblical ruler, world event and figure."""
    items = [(r, "period" if r in ctx.periods else "ruler") for r in ctx.periods + ctx.rulers if r.get("path")]
    items += [(r, r["kind"]) for r in ctx.world_events]
    for r, kind in items:
        lo, hi = r["start_y"], r["end_y"]
        approx = "c. " if r["approximate"] == "yes" else ""
        when = f"{approx}{year_link(lo)}" + (f" – {year_link(hi, end_label(r))}" if hi != lo else "")
        lines = frontmatter({"type": kind, "stream": r["stream"], "start": year_label(lo), "start_year": lo,
                             "end": end_label(r), "end_year": None if r.get("end") == "present" else hi, "approximate": r["approximate"] == "yes",
                             "wikidata": r["wikidata"] or None, "tags": ["world", kind]})
        lines += [f"# {r['name']}", "", f"**{r['stream']}** · {when} *(modern dates)*", ""]
        if r.get("level"):
            lines += [f"*{r['level'].capitalize()}*", ""]
        if r.get("note"):
            lines += [r["note"], ""]
        if r["wikidata"]:
            lines += [f"[Wikidata {r['wikidata']}](https://www.wikidata.org/wiki/{r['wikidata']})", ""]
        cents = [c for c in range(century_of(lo), century_of(hi) + 1) if c]
        lines += ["**Centuries:** " + " · ".join(link(century_path(c)) for c in cents), ""]
        same = [x for x in ctx.rulers + ctx.periods if x is not r and x["stream"] == r["stream"]
                and x["start_y"] <= hi and x["end_y"] >= lo]
        if same and kind in ("period", "ruler"):
            lines += [f"**Also in {r['stream']} at this time:** " + ", ".join(
                world_link(ctx, x) for x in sorted(same, key=lambda x: x["start_y"])), ""]
        evs = [ev for ev in ctx.chron.events if lo <= ev["year"] <= hi]
        if evs:
            lines += ["## Bible events in these years *(Ussher–Jones dates)*", ""]
            shown = evs if len(evs) <= 25 else evs[:12] + [None] + evs[-12:]
            lines += [f"- {year_label(ev['year'])} · {link(ev['path'], ev['title'])}" if ev else
                      f"- … {len(evs) - 24} more in the century notes" for ev in shown]
            lines += ["", "*Bible events are dated by Ussher's chronology (as refined by Jones), this entry by "
                      "modern dating. Before about 1000 BC the two can differ by decades or more.*", ""]
        write(r["path"], lines)
    return len(items)

