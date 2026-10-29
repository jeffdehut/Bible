"""The web of connections: every chapter, person, place and event in connections/, and the
links between them, laid out once for the graph page (graph.html).

    Called by scripts/connections.py, which has already loaded everything the graph shows.

Writes  data/graph.json         the nodes, the links and their places on the page (see write())
        data/graph-briefs.json  a short description of each person and place, for the cards

Nodes: the 1,189 chapters in order, then the people and places the Bible names, then the
events of Theographic's chronology. Links:
    xref      the cross-references between chapters (OpenBible.info): each chapter's ten
              strongest, by the votes of the verse-to-verse references between them
    seq       each chapter to the next, so a book reads as a string of beads
    names     a chapter to each person and place it names
    together  two people or places named together in at least two verses
    family    parent and child (STEPBible TIPNR)
    event     an event to its passages, people and places

The layout follows the model of d3-force: links pull their ends to a set distance, more
gently for well-linked nodes, and every node pushes every other away. The push between all
pairs is worked out on a mesh with FFTs (a particle-mesh method), with the exact push added
between near neighbours, so 5,600 nodes lay out in seconds.
It starts from the wheel the page opens with (the chapters round a circle in order, everyone
else at the middle of their chapters), so the opening animation from wheel to web is smooth.
"""

import collections
import json
import math
import os
import re

import numpy as np
from scipy.spatial import cKDTree

from notes import BOOK, ORDER, ROOT, SECTIONS, section_of

THREADS = 10              # cross-references kept for each chapter
TOGETHER = 2              # verses two names must share to be linked
LINK_STRENGTH = {"xref": 2.5, "seq": 3.0, "names": 1.0, "together": 0.6, "family": 1.0, "event": 0.8}


def collect(ctx, xrefs, together):
    """The nodes and links, before layout."""
    ents = ctx.entities
    chapters = sorted({(b, c) for b, vs in ctx.texts.items() for c, _ in vs}, key=lambda r: (ORDER.index(r[0]), r[1]))
    cid = {ch: k for k, ch in enumerate(chapters)}
    nodes = [("chapter", ch) for ch in chapters]
    node_of = {}
    for kind in ("person", "place"):
        for i, e in enumerate(ents):
            if e["kind"] == kind and e["named"]:
                node_of[i] = len(nodes)
                nodes.append((kind, i))
    event_node = {}
    for k, ev in enumerate(ctx.chron.events):
        event_node[k] = len(nodes)
        nodes.append(("event", k))

    links = {t: set() for t in LINK_STRENGTH}
    refs, votes = collections.Counter(), collections.Counter()
    for a, b, _, v in xrefs:
        ka, kb = cid.get((a[0], a[1])), cid.get((b[0], b[1]))
        if ka is None or kb is None or ka == kb:
            continue
        pair = (min(ka, kb), max(ka, kb))
        refs[pair] += 1
        votes[pair] += v
    best = collections.defaultdict(list)
    for (x, y), v in votes.items():
        best[x].append((v, y))
        best[y].append((v, x))
    for x, lst in best.items():
        for v, y in sorted(lst, reverse=True)[:THREADS]:
            links["xref"].add((min(x, y), max(x, y)))
    links["seq"] = {(k, k + 1) for k in range(len(chapters) - 1)}
    for i, n in node_of.items():
        for ch in {(b, c) for b, c, _ in ents[i]["verses"]}:
            if ch in cid:
                links["names"].add((cid[ch], n))
    for i, row in together.items():
        for j, count in row.items():
            if i < j and count >= TOGETHER and i in node_of and j in node_of:
                links["together"].add((node_of[i], node_of[j]))
    for p, c in ctx.gen.parent_edges:
        if p in node_of and c in node_of:
            links["family"].add((min(node_of[p], node_of[c]), max(node_of[p], node_of[c])))
    for k, ev in enumerate(ctx.chron.events):
        for ch in {(b, c) for b, c, _ in ev["verses"]}:
            if ch in cid:
                links["event"].add((cid[ch], event_node[k]))
        for i in ev["people"] + ev["places"]:
            if i in node_of:
                links["event"].add((min(node_of[i], event_node[k]), max(node_of[i], event_node[k])))
    links = {t: sorted(s) for t, s in links.items()}
    weight = [refs[pair] for pair in links["xref"]]
    return chapters, nodes, node_of, links, weight


def wheel(n_chapters, n, a, b, seed=1):
    """The opening arrangement: chapters round a circle from Genesis at the top, clockwise; every
    other node at the circular mean of the chapters it links to, nearer the rim the more those
    chapters agree."""
    R = 900.0
    ang = np.zeros(n)
    rad = np.zeros(n)
    ang[:n_chapters] = -math.pi / 2 + 2 * math.pi * np.arange(n_chapters) / n_chapters
    rad[:n_chapters] = R
    near = collections.defaultdict(list)
    for x, y in zip(a, b):
        if x < n_chapters <= y:
            near[y].append(x)
        elif y < n_chapters <= x:
            near[x].append(y)
    rng = np.random.default_rng(seed)
    for k in range(n_chapters, n):
        cs = near.get(k)
        if cs:
            v = np.exp(1j * ang[cs]).mean()
            ang[k] = np.angle(v)
            rad[k] = R * (0.25 + 0.6 * abs(v)) * (0.9 + 0.1 * rng.random())
        else:
            ang[k] = rng.random() * 2 * math.pi
            rad[k] = R * 0.2 * rng.random()
    return np.c_[rad * np.cos(ang), rad * np.sin(ang)]


def _mesh_push(pos, G=256, soft=1.5):
    """For each node, the sum over all others of (p_i - p_j) / |p_i - p_j|^2, on a G x G mesh."""
    lo = pos.min(0) - 1e-6
    h = (pos.max(0) - lo).max() * (1 + 2 / G) / G + 1e-9
    g = (pos - lo) / h
    i0 = np.clip(np.floor(g).astype(int), 0, G - 2)
    f = g - i0
    corners = ((0, 0, (1 - f[:, 0]) * (1 - f[:, 1])), (1, 0, f[:, 0] * (1 - f[:, 1])),
               (0, 1, (1 - f[:, 0]) * f[:, 1]), (1, 1, f[:, 0] * f[:, 1]))
    rho = np.zeros((2 * G, 2 * G))
    for dx, dy, w in corners:
        np.add.at(rho, (i0[:, 0] + dx, i0[:, 1] + dy), w)
    k = np.arange(2 * G)
    k[k >= G] -= 2 * G
    kx, ky = np.meshgrid(k, k, indexing="ij")
    r2 = kx ** 2 + ky ** 2 + soft ** 2
    R = np.fft.rfft2(rho)
    fx = np.fft.irfft2(R * np.fft.rfft2(kx / r2), s=rho.shape)[:G, :G] / h
    fy = np.fft.irfft2(R * np.fft.rfft2(ky / r2), s=rho.shape)[:G, :G] / h
    out = np.zeros_like(pos)
    for dx, dy, w in corners:
        out[:, 0] += w * fx[i0[:, 0] + dx, i0[:, 1] + dy]
        out[:, 1] += w * fy[i0[:, 0] + dx, i0[:, 1] + dy]
    return out


def force_layout(pos, a, b, strength_mult, iters=320, distance=24.0, charge=40.0, gravity=0.02, near=60.0, seed=7):
    n = len(pos)
    deg = np.bincount(np.concatenate([a, b]), minlength=n).astype(float)
    strength = strength_mult / np.minimum(deg[a], deg[b])
    bias = deg[a] / (deg[a] + deg[b])
    vel = np.zeros_like(pos)
    alpha, decay = 1.0, 1 - 0.001 ** (1 / iters)
    for _ in range(iters):
        alpha -= alpha * decay
        x = pos[b] + vel[b] - pos[a] - vel[a]
        length = np.sqrt((x ** 2).sum(1)) + 1e-9
        s = ((length - distance) / length * alpha * strength)[:, None] * x
        for c in (0, 1):
            vel[:, c] -= np.bincount(b, s[:, c] * bias, n)
            vel[:, c] += np.bincount(a, s[:, c] * (1 - bias), n)
        vel += _mesh_push(pos) * charge * alpha
        pairs = cKDTree(pos).query_pairs(near, output_type="ndarray")
        if len(pairs):
            d = pos[pairs[:, 1]] - pos[pairs[:, 0]]
            push = d / ((d ** 2).sum(1) + 1.0)[:, None] * charge * alpha
            for c in (0, 1):
                vel[:, c] -= np.bincount(pairs[:, 0], push[:, c], n)
                vel[:, c] += np.bincount(pairs[:, 1], push[:, c], n)
        vel -= pos * gravity * alpha
        vel *= 0.6
        pos = pos + vel
        pos -= pos.mean(0)
    # Last, part any two nodes that overlap.
    radius = 2.0 + np.sqrt(deg) * 0.9
    rng = np.random.default_rng(seed)
    for _ in range(60):
        pairs = cKDTree(pos).query_pairs(2 * radius.max(), output_type="ndarray")
        if not len(pairs):
            break
        i, j = pairs[:, 0], pairs[:, 1]
        d = pos[j] - pos[i]
        dist = np.sqrt((d ** 2).sum(1)) + 1e-9
        over = radius[i] + radius[j] + 1.0 - dist
        m = over > 0
        if not m.any():
            break
        push = (d[m] / dist[m][:, None]) * (over[m] / 2)[:, None] + rng.normal(0, 0.01, (m.sum(), 2))
        for c in (0, 1):
            pos[:, c] -= np.bincount(i[m], push[:, c], n)
            pos[:, c] += np.bincount(j[m], push[:, c], n)
    return pos


def map_places(ctx, node_of):
    """Places to open on the maps: the OpenBible place that the verses naming each TIPNR place
    also name, under the same name (data/bible/places.json, written by scripts/maps.py)."""
    path = os.path.join(ROOT, "data", "bible", "places.json")
    if not os.path.exists(path):
        return {}
    links = json.load(open(path, encoding="utf-8"))
    at = collections.defaultdict(list)
    for osis, verses in links["verses"].items():
        for cv, entries in verses.items():
            c, v = map(int, cv.split(":"))
            at[(osis, c, v)] = [e[0] for e in entries]
    plain = lambda s: re.sub(r"[^a-z]", "", s.lower())
    out = {}
    for i, n in node_of.items():
        e = ctx.entities[i]
        if e["kind"] != "place":
            continue
        # sorted, so that a tie goes the same way on every build
        votes = collections.Counter(p for ref in sorted(e["verses"]) for p in at.get(ref, ())
                                    if plain(links["places"][p][1]) == plain(e["name"]))
        if votes:
            pid, _, sheets = links["places"][votes.most_common(1)[0][0]]
            out[n] = [links["sheets"][sheets[0]][0], pid]
    return out


def build(ctx, xrefs, together, people_index):
    chapters, nodes, node_of, links, weight = collect(ctx, xrefs, together)
    n = len(nodes)
    order = list(LINK_STRENGTH)
    a = np.array([x for t in order for x, _ in links[t]])
    b = np.array([y for t in order for _, y in links[t]])
    mult = np.array([LINK_STRENGTH[t] for t in order for _ in links[t]])
    start = wheel(len(chapters), n, a, b)
    pos = force_layout(start.copy(), a, b, mult)
    write(ctx, chapters, nodes, node_of, links, weight, pos, people_index, map_places(ctx, node_of))
    return f"Graph: {n} nodes, {sum(len(s) for s in links.values())} links"


def write(ctx, chapters, nodes, node_of, links, weight, pos, people_index, on_maps):
    """data/graph.json, in columns. books: [name, OSIS id, section, chapters]; sections: names; kinds:
    how many chapters, people, places and events, in that order (chapters are numbered through
    the books). For the nodes after the chapters: n names (a title adds the first verse when
    several share a name), f the first verse that names them [book, chapter, verse], v how many
    verses name them, m [map sheet, OpenBible id] for a place on the maps, yr an event's year;
    g each person's number in genealogy.json, as the step from the person before. x, y: the web
    layout. links: for each kind, the pairs (a, b), a < b, sorted, written as [step, b - a] when a
    is new and [0, step from the b before] when a repeats; w: the cross-references behind each
    thread."""
    ents, events = ctx.entities, ctx.chron.events
    first_chapter = {}
    for k, (osis, c) in enumerate(chapters):
        first_chapter.setdefault(osis, k)
    books = [[BOOK[osis][1], osis, [s for s, _, _ in SECTIONS].index(section_of(osis)), sum(1 for o, _ in chapters if o == osis)]
             for osis in ORDER if osis in first_chapter]
    names, first, verses, gen, maps, years, briefs = [], [], [], [], {}, {}, []
    book_no = {osis: k for k, osis in enumerate(ORDER)}
    for k, (kind, x) in enumerate(nodes):
        if kind == "chapter":
            continue
        j = k - len(chapters)
        if kind in ("person", "place"):
            e = ents[x]
            names.append(ctx.title(x))
            briefs.append(e["brief"])
            ref = e["first"]
            verses.append(len(e["verses"]))
            if kind == "person":
                gen.append(people_index[x])
            if k in on_maps:
                maps[j] = on_maps[k]
        else:
            ev = events[x]
            names.append(ev["title"])
            briefs.append("")
            refs = sorted(ev["verses"], key=lambda r: (ORDER.index(r[0]), r[1], r[2]))
            ref = refs[0] if refs else None
            verses.append(len(refs))
            years[j] = ev["year"]
        first += [book_no[ref[0]], ref[1], ref[2]] if ref else [-1, 0, 0]
    packed = {}
    for t, pairs in links.items():
        if t == "seq":
            continue
        flat, la, lb = [], 0, 0
        for x, y in pairs:
            flat += [0, y - lb] if flat and x == la else [x - la, y - x]
            la, lb = x, y
        packed[t] = flat
    lo = pos.min(0)
    data = {
        "books": books, "sections": [s for s, _, _ in SECTIONS],
        "kinds": [len(chapters)] + [sum(1 for kind, _ in nodes if kind == t) for t in ("person", "place", "event")],
        "n": names, "f": first, "v": verses, "g": [g - (gen[k - 1] if k else 0) for k, g in enumerate(gen)], "m": maps, "yr": years,
        "x": [int(round(v)) for v in pos[:, 0] - lo[0]], "y": [int(round(v)) for v in pos[:, 1] - lo[1]],
        "links": packed, "w": weight,
    }
    with open(os.path.join(ROOT, "data", "graph.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write("{\n" + ",\n".join(f"{json.dumps(k)}:{json.dumps(v, ensure_ascii=False, separators=(',', ':'))}"
                                  for k, v in data.items()) + "\n}\n")
    # TIPNR's short description of each person and place, loaded when a card first needs one.
    with open(os.path.join(ROOT, "data", "graph-briefs.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(briefs, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
