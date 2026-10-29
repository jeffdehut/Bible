"""Build the Bible maps in maps/.

    python3 scripts/maps.py

The maps are drawn in the manner of the Eilers Sunday School wall maps (see ROADMAP.md),
from open data only:
  - elevation: AWS Terrain Tiles (Mapzen terrarium encoding; SRTM, GMTED2010, ETOPO1),
    downloaded once into .cache/dem/
  - places: OpenBible.info Bible Geocoding Data (CC BY 4.0), cloned into .cache/openbible-geo/
  - rivers and lakes: Natural Earth (public domain), downloaded once into .cache/naturalearth/
  - lands and borders: grown from the towns the text gives each people (see territories())
  - journeys: lists of stops below, each named in its verse of the translation (check_verses())

Needs numpy, scipy and Pillow, unlike the other scripts, which use only the standard library.

Writes, for each map,
        maps/data/NAME.json   every layer as SVG path data and points
        maps/NAME.html        scripts/templates/map.html with the map's words and data filled in
and maps/index.html, the list of the sheets.

    python3 scripts/maps.py exodus     build one map (see MAPS at the end for the names)

Map No. 7, The Kingdoms of Judah and Israel, was the style study: a redrawing of the Eilers
map of the same name. The other sheets follow the Eilers series: Nos. 1 to 6 and a plan of
Ancient Jerusalem (see INDEX).
"""

import json
import math
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
SITE = ROOT                                   # the website is served from the repository root
GEO_REPO = "https://github.com/openbibleinfo/Bible-Geocoding-Data"


# --- The sheet ------------------------------------------------------------------------------

class Sheet:
    """A map extent on a plate carree grid, squared at the middle latitude.

    Map units are kilometres east and south of the north-west corner, so y grows downward
    as in SVG. The raster grid has `res` km cells."""

    def __init__(self, west, east, south, north, res):
        self.west, self.east, self.south, self.north, self.res = west, east, south, north, res
        self.lat0 = (south + north) / 2
        self.kx = 111.32 * math.cos(math.radians(self.lat0))  # km per degree of longitude
        self.ky = 110.95                                        # km per degree of latitude
        self.width = (east - west) * self.kx
        self.height = (north - south) * self.ky
        self.nx = int(round(self.width / res))
        self.ny = int(round(self.height / res))

    def xy(self, lon, lat):
        return (lon - self.west) * self.kx, (self.north - lat) * self.ky

    def lonlat(self, x, y):
        return self.west + x / self.kx, self.north - y / self.ky

    def cell_centres(self):
        """Longitude and latitude of every cell centre, as two (ny, nx) arrays."""
        x = (np.arange(self.nx) + 0.5) * self.res
        y = (np.arange(self.ny) + 0.5) * self.res
        lon = self.west + x / self.kx
        lat = self.north - y / self.ky
        return np.meshgrid(lon, lat)


# --- Elevation ------------------------------------------------------------------------------

TILE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"


def _tile(z, x, y):
    path = os.path.join(CACHE, "dem", str(z), str(x), f"{y}.png")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = urllib.request.urlopen(TILE_URL.format(z=z, x=x, y=y), timeout=60).read()
        with open(path, "wb") as f:
            f.write(data)
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64)
    return rgb[..., 0] * 256 + rgb[..., 1] + rgb[..., 2] / 256 - 32768


def elevation(sheet, z):
    """Elevation in metres at every cell centre, bilinearly sampled from Web Mercator tiles."""
    lon, lat = sheet.cell_centres()
    n = 2 ** z * 256
    px = (lon + 180) / 360 * n
    py = (1 - np.log(np.tan(np.radians(lat)) + 1 / np.cos(np.radians(lat))) / math.pi) / 2 * n
    tx0, tx1 = int(px.min() // 256), int(px.max() // 256)
    ty0, ty1 = int(py.min() // 256), int(py.max() // 256)
    mosaic = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256))
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            mosaic[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = _tile(z, tx, ty)
    coords = np.array([py - ty0 * 256 - 0.5, px - tx0 * 256 - 0.5])
    return ndimage.map_coordinates(mosaic, coords, order=1, mode="nearest")


# --- Raster to vector -----------------------------------------------------------------------

def contours(field, level):
    """Marching squares: the polylines where `field` crosses `level`, in cell units.

    Returns a list of (k, 2) arrays of (x, y) points, joined end to end; closed rings repeat
    their first point at the end."""
    f = field.astype(np.float64)
    a, b, c, d = f[:-1, :-1], f[:-1, 1:], f[1:, 1:], f[1:, :-1]  # tl, tr, br, bl
    code = (a > level) * 8 + (b > level) * 4 + (c > level) * 2 + (d > level) * 1
    ys, xs = np.nonzero((code > 0) & (code < 15))

    def interp(p, q):
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(q != p, (level - p) / (q - p), 0.5)
        return np.clip(t, 0, 1)

    # Edge points for every cell: top, right, bottom, left.
    top = np.stack([xs + interp(a[ys, xs], b[ys, xs]), ys + 0.0], 1)
    right = np.stack([xs + 1.0, ys + interp(b[ys, xs], c[ys, xs])], 1)
    bottom = np.stack([xs + interp(d[ys, xs], c[ys, xs]), ys + 1.0], 1)
    left = np.stack([xs + 0.0, ys + interp(a[ys, xs], d[ys, xs])], 1)
    edges = {0: top, 1: right, 2: bottom, 3: left}
    # Edge pairs per case; saddles (5, 10) are split by the cell-centre value.
    table = {1: [(3, 2)], 2: [(2, 1)], 3: [(3, 1)], 4: [(0, 1)], 6: [(0, 2)], 7: [(3, 0)],
             8: [(3, 0)], 9: [(0, 2)], 11: [(0, 1)], 12: [(3, 1)], 13: [(2, 1)], 14: [(3, 2)]}
    centre = (a + b + c + d)[ys, xs] / 4 > level
    codes = code[ys, xs]
    segs = []
    for i in range(len(xs)):
        k = codes[i]
        if k == 5:
            pairs = [(3, 0), (2, 1)] if centre[i] else [(3, 2), (0, 1)]
        elif k == 10:
            pairs = [(0, 1), (3, 2)] if centre[i] else [(3, 0), (2, 1)]
        else:
            pairs = table[k]
        for e1, e2 in pairs:
            segs.append((tuple(np.round(edges[e1][i], 6)), tuple(np.round(edges[e2][i], 6))))
    return _join(segs)


def _join(segs):
    """Join segments sharing endpoints into polylines."""
    nbr = {}
    for s in segs:
        for p in s:
            nbr.setdefault(p, []).append(s)
    used = set()
    lines = []
    for s in segs:
        if id(s) in used:
            continue
        used.add(id(s))
        line = [s[0], s[1]]
        for forward in (True, False):
            while True:
                end = line[-1] if forward else line[0]
                nxt = next((t for t in nbr[end] if id(t) not in used), None)
                if nxt is None:
                    break
                used.add(id(nxt))
                p = nxt[1] if nxt[0] == end else nxt[0]
                if forward:
                    line.append(p)
                else:
                    line.insert(0, p)
        lines.append(np.array(line))
    return lines


def simplify(line, tol):
    """Douglas-Peucker simplification of a polyline."""
    if len(line) < 3:
        return line
    keep = np.zeros(len(line), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(line) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        p, q = line[i], line[j]
        d = q - p
        n = math.hypot(*d)
        seg = line[i + 1:j] - p
        dist = np.abs(seg[:, 0] * d[1] - seg[:, 1] * d[0]) / n if n else np.hypot(seg[:, 0], seg[:, 1])
        k = int(np.argmax(dist))
        if dist[k] > tol:
            keep[i + 1 + k] = True
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return line[keep]


def densify(line, max_seg):
    """Add points so that no segment is longer than `max_seg`."""
    out = [line[:1]]
    for p, q in zip(line[:-1], line[1:]):
        k = max(1, int(math.ceil(math.hypot(*(q - p)) / max_seg)))
        t = np.arange(1, k + 1)[:, None] / k
        out.append(p + (q - p) * t)
    return np.vstack(out)


def chaikin(line, rounds=2):
    """Corner-cutting smoothing; keeps the ends of open lines."""
    closed = len(line) > 3 and np.allclose(line[0], line[-1])
    for _ in range(rounds):
        p, q = line[:-1], line[1:]
        a, b = 0.75 * p + 0.25 * q, 0.25 * p + 0.75 * q
        mid = np.empty((2 * len(p), 2))
        mid[0::2], mid[1::2] = a, b
        line = np.vstack([mid, mid[:1]]) if closed else np.vstack([line[:1], mid, line[-1:]])
    return line


def path_d(lines, scale, digits=2, close=False):
    """Compact SVG path data for polylines in cell units, scaled to map units: an absolute
    move, then relative steps on a grid of 10^-digits units. Sheets finer than the 130 m
    grid of the maps of the land (the plan of a city) get more digits, in proportion."""
    digits += max(0, math.ceil(math.log10(0.13 / scale)))
    q = 10 ** digits
    out = []

    def num(v):
        s = f"{v / q:.{digits}f}".rstrip("0").rstrip(".")
        return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s

    for ln in lines:
        pts = np.round(ln * scale * q).astype(np.int64)
        keep = np.r_[True, np.any(np.diff(pts, axis=0) != 0, axis=1)]
        pts = pts[keep]
        if len(pts) < 2:
            continue
        steps = np.diff(pts, axis=0)
        body = []
        for dx, dy in steps:
            a, b = num(dx), num(dy)
            body.append(a + ("" if b.startswith("-") else " ") + b)
        s = f"M{num(pts[0][0])} {num(pts[0][1])}l" + " ".join(body).replace(" -", "-")
        out.append(s + ("z" if close else ""))
    return "".join(out)


# --- Terrain layers -------------------------------------------------------------------------

def _component(mask, sheet, lon, lat):
    """The connected part of `mask` that contains the cell at lon, lat."""
    x, y = sheet.xy(lon, lat)
    lab, _ = ndimage.label(mask)
    k = lab[int(y / sheet.res), int(x / sheet.res)]
    if k == 0:
        raise ValueError(f"no water at {lon}, {lat}")
    return lab == k


def water(sheet, elev):
    """Masks for the sea and the lakes, each as the lake stood in antiquity.

    The Sea of Galilee and the Dead Sea are cut at their old shorelines (the Dead Sea at
    about 392 m below sea level, its level around 1900, which brings back the southern
    basin). Lake Huleh, drained in the 1950s, is the lowest part of its old basin."""
    sea = _component(elev <= 0, sheet, sheet.west + 0.01, sheet.north - 0.01)
    galilee = _component(ndimage.binary_opening(elev <= -208, iterations=3), sheet, 35.59, 32.82)
    dead = _component(elev <= -392, sheet, 35.50, 31.50)
    huleh = elev <= 63.3
    x, y = sheet.xy(35.6, 33.15)
    huleh[:int(y / sheet.res)] = False
    x, y = sheet.xy(35.6, 33.0)
    huleh[int(y / sheet.res):] = False
    huleh = _component(ndimage.binary_opening(huleh, iterations=2), sheet, 35.612, 33.07)
    lakes = {"Sea of Galilee": galilee, "Dead Sea": dead, "Lake Huleh": huleh}
    lakes = {k: ndimage.binary_fill_holes(ndimage.binary_closing(v, iterations=2)) for k, v in lakes.items()}
    return {"sea": sea, **lakes}


def outlines(mask, smooth=1.0, tol=0.6, rounds=2, closed=True, min_points=4):
    """Smoothed outlines of a mask, in cell units: the 0.5 contour of the blurred mask.

    With `closed`, rings are closed along the sheet edge, for filling; otherwise the lines
    stop at the edge, for stroking."""
    field = ndimage.gaussian_filter(mask.astype(np.float64), smooth)
    if closed:
        field = np.pad(field, 1)
    lines = []
    for ln in contours(field, 0.5):
        if closed:
            ln = ln - 1
        if len(ln) < min_points:
            continue
        lines.append(chaikin(densify(simplify(ln, tol), 3), rounds))
    return lines


def ripples(sheet, land, offsets_km, reach_km=None):
    """Water lines: offsets of the shore into the water, at the given distances (km)."""
    dist = ndimage.distance_transform_edt(~land) * sheet.res
    out = []
    for d in offsets_km:
        for ln in contours(np.pad(dist, 1, constant_values=0), d):
            ln = ln - 1
            if len(ln) < 6:
                continue
            out.append(chaikin(densify(simplify(ln, 0.8), 4), 2))
    return out


def drainage(sheet, elev, sinks, step=2):
    """Flow accumulation (km^2 of drainage area) on a grid `step` times coarser.

    Pits are filled by priority flood from the sheet edges and the sinks (sea, Dead Sea), so
    every cell drains somewhere. Returns (area, receiver index, grid shape)."""
    import heapq
    ny, nx = elev.shape[0] // step, elev.shape[1] // step
    f = elev[:ny * step, :nx * step].reshape(ny, step, nx, step).mean((1, 3))
    sink = sinks[:ny * step:step, :nx * step:step]
    edge = np.zeros((ny, nx), bool)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    start = np.flatnonzero(sink | edge)
    hs = f.ravel().tolist()
    n = ny * nx
    recv = [-1] * n
    seen = bytearray(n)
    pq = [(hs[i], i) for i in start]
    heapq.heapify(pq)
    for i in start:
        seen[i] = 1
    order = []
    nbrs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while pq:
        h, i = heapq.heappop(pq)
        order.append(i)
        r, c = divmod(i, nx)
        for dr, dc in nbrs:
            rr, cc = r + dr, c + dc
            if 0 <= rr < ny and 0 <= cc < nx:
                j = rr * nx + cc
                if not seen[j]:
                    seen[j] = 1
                    recv[j] = i
                    hj = hs[j]
                    heapq.heappush(pq, (hj if hj > h else h + 1e-4, j))
    acc = [1.0] * n
    for i in reversed(order):
        j = recv[i]
        if j >= 0:
            acc[j] += acc[i]
    cell_km2 = (sheet.res * step) ** 2
    return np.array(acc).reshape(ny, nx) * cell_km2, recv, (ny, nx)


def rivers(sheet, area, recv, shape, step, wet, min_km2):
    """Streams draining at least `min_km2`, as polylines (in fine-cell units) with the
    drainage area at their mouth. Stops at the sea and lakes."""
    ny, nx = shape
    a = area.ravel()
    wet2 = wet[:ny * step:step, :nx * step:step].ravel()
    stream = (a >= min_km2) & ~wet2
    has_up = np.zeros(ny * nx, bool)
    for i in np.flatnonzero(stream):
        j = recv[i]
        if j >= 0:
            has_up[j] = True
    done = np.zeros(ny * nx, bool)
    lines = []
    # Trace from every source, largest catchments first so main stems stay whole.
    sources = [i for i in np.flatnonzero(stream) if not has_up[i]]
    for s in sources:
        i, pts = s, []
        while True:
            r, c = divmod(i, nx)
            pts.append(((c + 0.5) * step, (r + 0.5) * step))
            if done[i]:
                break
            done[i] = True
            j = recv[i]
            if j < 0 or wet2[j]:
                if j >= 0:
                    r, c = divmod(j, nx)
                    pts.append(((c + 0.5) * step, (r + 0.5) * step))
                break
            i = j
        if len(pts) > 2:
            lines.append((np.array(pts), float(a[i])))
    return lines


def hachures(sheet, elev, wet, spacing_km=1.0, min_slope=3.5, seed=7):
    """Short engraved strokes running downhill, darker on slopes facing away from a light in
    the north-west. Returns a list of (polyline in fine-cell units, weight 0..1)."""
    rng = np.random.default_rng(seed)
    z = ndimage.gaussian_filter(elev, 2.0)
    gy, gx = np.gradient(z, sheet.res * 1000)          # metres per metre
    slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    # Light from the north-west: shade is 0 on lit slopes, 1 on those facing south-east.
    shade = np.clip(0.5 - 0.5 * (gx + gy) / (np.hypot(gx, gy) * math.sqrt(2) + 1e-9), 0, 1)
    step = spacing_km / sheet.res
    ny, nx = elev.shape
    ys, xs = np.mgrid[step / 2:ny:step, step / 2:nx:step]
    xs = xs.ravel() + rng.uniform(-0.4, 0.4, xs.size) * step
    ys = ys.ravel() + rng.uniform(-0.4, 0.4, ys.size) * step
    out = []
    for x, y in zip(xs, ys):
        c, r = int(x), int(y)
        if not (0 <= r < ny and 0 <= c < nx) or wet[r, c]:
            continue
        s = slope[r, c]
        if s < min_slope:
            continue
        length = min(1.0, 0.35 + s / 25) * step * 0.9
        pts = [(x, y)]
        px, py = x, y
        for _ in range(2):
            cc, rr = int(px), int(py)
            if not (0 <= rr < ny and 0 <= cc < nx):
                break
            dx, dy = -gx[rr, cc], -gy[rr, cc]   # downhill
            n = math.hypot(dx, dy)
            if n < 1e-6:
                break
            px, py = px + dx / n * length / 2, py + dy / n * length / 2
            pts.append((px, py))
        if len(pts) > 2:
            w = min(1.0, (s - min_slope) / 18) * (0.35 + 0.65 * shade[r, c])
            out.append((np.array(pts), float(w)))
    return out


# --- Places ---------------------------------------------------------------------------------

def _geo_repo():
    path = os.path.join(CACHE, "openbible-geo", "repo")
    if not os.path.isdir(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--depth", "1", GEO_REPO, path], check=True)
    return path


def _verse_key(osis):
    book, ch, vs = osis.split(".")[:3]
    return book, int(ch), int(vs)


def places():
    """Every Bible place OpenBible.info can locate, with its most likely location.

    Each place: id, name, types, lon, lat, score (0-1000: the confidence of current
    scholarship in the identification), exact (False when the location is only the centre of
    an area the place lies in), modern (the modern site's name), verses ((book, ch, v)...)."""
    repo = _geo_repo()
    modern = {}
    with open(os.path.join(repo, "data", "modern.jsonl"), encoding="utf-8") as f:
        for line in f:
            m = json.loads(line)
            modern[m["id"]] = m.get("friendly_id") or m.get("name", "")
    out = []
    with open(os.path.join(repo, "data", "ancient.jsonl"), encoding="utf-8") as f:
        for line in f:
            a = json.loads(line)
            best = None
            for idn in a.get("identifications", []):
                score = idn.get("score", {}).get("time_total", 0)
                for r in idn.get("resolutions", []):
                    if "lonlat" not in r:
                        continue
                    key = (score, r.get("best_path_score", 0))
                    if best is None or key > best[0]:
                        best = (key, r)
            if best is None:
                continue
            (score, _), r = best
            lon, lat = map(float, r["lonlat"].split(","))
            out.append({
                "id": a["id"],
                "slug": a.get("url_slug", ""),
                "name": a["friendly_id"],
                "spellings": a.get("translation_name_counts", {}),
                "types": a.get("types", []),
                "lon": lon, "lat": lat,
                "score": min(score, 1000),
                "exact": r.get("lonlat_type") in ("point", "settlement"),
                "modern": modern.get(r.get("modern_basis_id"), ""),
                "verses": [_verse_key(v["osis"]) for v in a.get("verses", [])],
            })
    return out


# --- Territories ----------------------------------------------------------------------------

# The tribal allotments: each tribe's town lists in Joshua (ranges of verses), and its side of
# the Jordan. Boundary descriptions (Josh 15:1-12, 18:11-20) are left out, since the places
# they name lie on a border rather than inside it.
TRIBES = [
    # name,              kingdom,  sections
    ("Simeon",           "Judah",  [(19, 1, 9)]),
    ("Dan",              "Judah",  [(19, 40, 46), (21, 23, 24)]),
    ("Benjamin",         "Judah",  [(18, 21, 28), (21, 17, 18)]),
    ("Ephraim",          "Israel", [(16, 1, 10), (17, 8, 9), (21, 20, 22)]),
    ("Issachar",         "Israel", [(19, 17, 23), (21, 28, 29)]),
    ("Zebulun",          "Israel", [(19, 10, 16), (21, 34, 35)]),
    ("Asher",            "Israel", [(19, 24, 31), (21, 30, 31)]),
    ("Naphtali",         "Israel", [(19, 32, 39), (21, 32, 32)]),
    ("Manasseh",         "Israel", [(17, 7, 11), (21, 25, 25)]),
    ("Judah",            "Judah",  [(15, 13, 19), (15, 21, 62), (21, 9, 16)]),
    ("Reuben",           "Israel", [(13, 15, 23), (21, 36, 37)]),
    ("Gad",              "Israel", [(13, 24, 28), (21, 38, 39)]),
    ("Manasseh (east)",  "Israel", [(13, 29, 31), (21, 27, 27)]),
]
# The neighbouring peoples, seeded from their chief cities. These win over the tribal lists,
# which include cities Israel never held (Gaza, Ekron, Sidon: Judges 1:18-19, 31).
NEIGHBOURS = {
    "Philistia": ["Gaza", "Ashkelon", "Ashdod", "Ekron", "Gath 1"],
    "Phoenicia": ["Sidon", "Zarephath", "Tyre"],
    "Aram": ["Damascus"],
    "Ammon": ["Rabbah 1"],
    "Moab": ["Kir-hareseth", "Ar"],
    "Edom": ["Bozrah 1"],
}
# Single places given to a tribe other than the first list that names them.
# None leaves a place out: border points, and identifications far from the rest of the list.
PLACE_TRIBE = {
    "Bethel 1": "Ephraim",   # on the border; held by Joseph's house (Judg 1:22-26, 1 Chr 7:28)
    "Luz 1": "Ephraim",      # Bethel's older name
    "En-dor": None,          # a Manassite town inside Issachar (Josh 17:11)
    "Tappuah 1": "Ephraim",  # "the town of Tappuah belonged to the Ephraimites" (Josh 17:8)
    "Shiloh": "Ephraim",     # north of Bethel (Judg 21:19), in Ephraim's hill country
    "Timnath-heres": "Ephraim",  # Timnath-serah, "in the hill country of Ephraim" (Josh 24:30)
    "Shechem": "Manasseh",   # the clans of Shechem and Tirzah (Josh 17:2-3)
    "Tirzah": "Manasseh",
    "Michmethath": None,     # border points of Josh 16:6-8 and 17:7-9
    "Taanath-shiloh": None,
    "Janoah 1": None,
    "Kibzaim": None,         # location unknown; the proposed site lies in Zebulun
    "Dimonah": None,         # the proposed site lies east of the Dead Sea
}


def seeds(all_places):
    """(name, territory, lon, lat) for every located town in the lists above."""
    by_name = {p["name"]: p for p in all_places}
    out, taken = [], set()
    for terr, names in NEIGHBOURS.items():
        for n in names:
            p = by_name[n]
            out.append((n, terr, p["lon"], p["lat"]))
            taken.add(n)
    for n, terr in PLACE_TRIBE.items():
        taken.add(n)
        if terr:
            p = by_name[n]
            out.append((n, terr, p["lon"], p["lat"]))
    for tribe, _, sections in TRIBES:
        for p in all_places:
            if p["name"] in taken or not p["exact"] or p["score"] < 250 or "settlement" not in p["types"]:
                continue
            if any(b == "Josh" and c == ch and v0 <= v <= v1
                   for b, c, v in p["verses"] for ch, v0, v1 in sections):
                out.append((p["name"], tribe, p["lon"], p["lat"]))
                taken.add(p["name"])
    return out


def territories(sheet, elev, wet, flow, seed_list, step=4, cap_km=30, names=None, barrier=(35.651, 33.248),
                keep_seeded=False):
    """Allot every land cell to the territory whose towns are nearest, measured on foot.

    Distance runs over a grid `step` times coarser than the sheet. `cap_km` is one reach for all,
    or a reach for each territory by name. Lakes cannot be crossed;
    the Jordan costs 60 km to cross and other streams up to 20 km, so borders settle along
    rivers, as the boundary lists in Joshua describe. Land more than `cap_km` from any town
    is left unallotted (wilderness). Returns an int array on the sheet grid: -1 for none,
    else the index into the territory names, which are also returned."""
    import heapq
    area, recv, (fy, fx), fstep = flow
    ny, nx = elev.shape[0] // step, elev.shape[1] // step
    wet_c = wet[:ny * step:step, :nx * step:step]
    # River crossing cost, from the drainage area on the flow grid.
    k = step // fstep
    a = area[:ny * k:k, :nx * k:k][:ny, :nx]
    river = np.where(a > 300, np.clip(np.log10(a / 300) * 10, 0, 20), 0)
    # A barrier river, such as the Jordan: follow the drainage down from its source
    # (by default the springs at Dan) to its mouth.
    jordan = np.zeros((ny, nx), bool)
    x, y = sheet.xy(*barrier) if barrier else (-1, -1)
    inside = 0 <= x < sheet.width and 0 <= y < sheet.height
    i = int(y / (sheet.res * fstep)) * fx + int(x / (sheet.res * fstep)) if inside else -1
    while i >= 0:
        r, c = divmod(i, fx)
        rr, cc = r // k, c // k
        if rr < ny and cc < nx:
            jordan[rr, cc] = True
        i = recv[i]
    jordan = ndimage.binary_dilation(jordan, iterations=1)
    river[jordan] = 60
    names = names or list(NEIGHBOURS) + [t[0] for t in TRIBES]
    index = {n: i for i, n in enumerate(names)}
    reach = np.array([cap_km.get(n, 0) if isinstance(cap_km, dict) else cap_km for n in names] + [0], float)
    cell = sheet.res * step
    dist = np.full(ny * nx, np.inf)
    owner = np.full(ny * nx, -1, np.int32)
    pq = []
    for _, terr, lon, lat in seed_list:
        x, y = sheet.xy(lon, lat)
        r = min(max(int(y / cell), 0), ny - 1)
        c = min(max(int(x / cell), 0), nx - 1)
        i = r * nx + c
        if wet_c[r, c] or dist[i] == 0:
            continue
        dist[i] = 0
        owner[i] = index[terr]
        pq.append((0.0, i))
    heapq.heapify(pq)
    cost = (cell + river).ravel()
    wetf = wet_c.ravel()
    nbrs = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),
            (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142)]
    while pq:
        d, i = heapq.heappop(pq)
        if d > dist[i] or d > reach[owner[i]]:
            continue
        r, c = divmod(i, nx)
        for dr, dc, m in nbrs:
            rr, cc = r + dr, c + dc
            if 0 <= rr < ny and 0 <= cc < nx:
                j = rr * nx + cc
                if wetf[j]:
                    continue
                nd = d + cost[j] * m
                if nd < dist[j]:
                    dist[j] = nd
                    owner[j] = owner[i]
                    heapq.heappush(pq, (nd, j))
    owner[dist > reach[owner]] = -1
    owner = owner.reshape(ny, nx)
    # Tidy: a majority filter, then keep only each territory's largest piece, giving the
    # rest (towns of one list inside another's land) to the nearest other territory.
    classes = np.unique(owner)           # a 5x5 majority filter; ties go to the lowest index
    votes = np.stack([ndimage.correlate((owner == c).astype(np.int32), np.ones((5, 5), np.int32), mode="nearest")
                      for c in classes])
    owner = classes[np.argmax(votes, axis=0)].astype(np.int32)
    seeded = {}
    for _, terr, lon, lat in seed_list:
        x, y = sheet.xy(lon, lat)
        seeded.setdefault(index[terr], []).append((min(max(int(y / cell), 0), ny - 1), min(max(int(x / cell), 0), nx - 1)))
    for t in range(len(names)):
        lab, n = ndimage.label(owner == t)
        if n > 1:
            sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
            keep = {int(np.argmax(sizes)) + 1}
            if keep_seeded:         # islands and coasts across the water, with towns of their own
                keep |= {int(lab[r, c]) for r, c in seeded.get(t, []) if lab[r, c] > 0}
            owner[(lab > 0) & ~np.isin(lab, list(keep))] = -2
    stray = owner == -2
    if stray.any():
        _, (ri, ci) = ndimage.distance_transform_edt(owner < 0, return_indices=True)
        owner[stray] = owner[ri[stray], ci[stray]]
    full = np.repeat(np.repeat(owner, step, 0), step, 1)
    full = np.pad(full, ((0, elev.shape[0] - full.shape[0]), (0, elev.shape[1] - full.shape[1])), mode="edge")
    full[wet] = -1
    return full, names


# --- Names ----------------------------------------------------------------------------------

OT_BOOKS = {"Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs",
            "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov", "Eccl", "Song",
            "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic",
            "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"}
NT_ORDER = ["Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col",
            "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John",
            "2John", "3John", "Jude", "Rev"]
NT_BOOKS = set(NT_ORDER)
BOOK_ORDER = {b: i for i, b in enumerate(["Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg",
    "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps",
    "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad",
    "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"] + NT_ORDER)}
OSIS_LABEL = {"Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers",
              "Deut": "Deuteronomy", "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth",
              "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Kings", "2Kgs": "2 Kings",
              "1Chr": "1 Chronicles", "2Chr": "2 Chronicles", "Ezra": "Ezra", "Neh": "Nehemiah",
              "Esth": "Esther", "Job": "Job", "Ps": "Psalm", "Prov": "Proverbs",
              "Eccl": "Ecclesiastes", "Song": "Song of Songs", "Isa": "Isaiah", "Jer": "Jeremiah",
              "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel", "Hos": "Hosea",
              "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah",
              "Mic": "Micah", "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah",
              "Hag": "Haggai", "Zech": "Zechariah", "Mal": "Malachi",
              "Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
              "Rom": "Romans", "1Cor": "1 Corinthians", "2Cor": "2 Corinthians", "Gal": "Galatians",
              "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians", "1Thess": "1 Thessalonians",
              "2Thess": "2 Thessalonians", "1Tim": "1 Timothy", "2Tim": "2 Timothy", "Titus": "Titus",
              "Phlm": "Philemon", "Heb": "Hebrews", "Jas": "James", "1Pet": "1 Peter", "2Pet": "2 Peter",
              "1John": "1 John", "2John": "2 John", "3John": "3 John", "Jude": "Jude", "Rev": "Revelation"}


def our_spellings():
    """How often each capitalised name (up to four words, with hyphens) occurs in the Open
    Plain English Translation, so the maps can spell places as our translation does."""
    import collections
    import glob
    import re
    counts = collections.Counter()
    word = r"[A-Z][a-z'’]*(?:-[a-z'’]+|-[A-Z][a-z'’]*)*"
    pattern = re.compile(rf"(?=({word}(?: (?:of |the |in )?{word}){{0,3}}))")
    for path in glob.glob(os.path.join(ROOT, "text", "english", "*.md")):
        text = open(path, encoding="utf-8").read()
        for m in pattern.finditer(text):
            name = m.group(1)
            parts = name.split(" ")
            for k in range(1, len(parts) + 1):
                counts[" ".join(parts[:k])] += 1
    return counts


_VERSES = {}


def english_verse(ref):
    """The text of a verse of the Open Plain English Translation, without its note markers, from
    a reference such as "Acts 13:4" (the first verse of a range)."""
    m = re.match(r"(.+) (\d+):(\d+)", ref)
    label, ch, v = m.group(1), int(m.group(2)), int(m.group(3))
    osis = next(k for k, n in OSIS_LABEL.items() if n == label)
    if osis not in _VERSES:
        import glob
        number = next(b["number"] for b in json.load(open(os.path.join(ROOT, "books.json"), encoding="utf-8"))
                      if b["osis"] == osis)
        path = glob.glob(os.path.join(ROOT, "text", "english", f"{number:02d}-*.md"))[0]
        verses, chap, key = {}, 0, None
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if line.startswith("## Chapter "):
                chap, key = int(line.split()[-1]), None
                continue
            mm = re.match(r"\*\*(\d+)\*\* (.*)", line)
            if mm:
                key = (chap, int(mm.group(1)))
                verses[key] = mm.group(2)
            elif key and line and not line.startswith(("#", "[^", "*Status", ">")):
                verses[key] += " " + line.strip()
            elif not line:
                key = None if key and verses.get(key) else key
        _VERSES[osis] = {k: re.sub(r"\[\^[^\]]+\]", "", t) for k, t in verses.items()}
    return _VERSES[osis].get((ch, v), "")


def verse_name(place, ours, first=None, books=None):
    """The name as the first verse that names the place spells it: "Thessalonica", not
    "Thessalonians"; "Antipatris" in Acts, not "Aphek". `first` is that verse, (book, ch, v), or
    else the first in `books`."""
    name = display_name(place, ours)
    named = [v for v in place["verses"] if books is None or v[0] in books]
    if first is None and named:
        first = min(named, key=lambda v: (BOOK_ORDER[v[0]], v[1], v[2]))
    if first is None:
        return name
    text = english_verse(f"{OSIS_LABEL[first[0]]} {first[1]}:{first[2]}")
    if not re.search(rf"\b{re.escape(name)}\b", text):
        name = next((n for n in sorted(place["spellings"], key=lambda n: -place["spellings"][n])
                     if re.search(rf"\b{re.escape(n)}\b", text)), name)
    # A people's name where the place has its own ("the Lycaonian cities", "the region of the
    # Gerasenes"): use the place's, from the text if it has one, else OpenBible's (Gerasa).
    people = r"(ians?|eans?|ites?|enes?)$"
    if re.search(people, name):
        plain = [n for n in place["spellings"] if n[:5] == name[:5] and not re.search(people, n)]
        own = re.sub(r" \d+$", "", place["name"])
        if plain:
            name = max(plain, key=lambda n: place["spellings"][n])
        elif own[:5] == name[:5] and not re.search(people, own):
            name = own
    return name


def display_name(place, ours):
    """The place's name as our translation spells it, else OpenBible's name without its
    disambiguating number."""
    sp = place["spellings"]
    top = max(sp.values(), default=0)
    # Only the usual spellings: rare renderings ("Galilee" for Chinnereth) don't count.
    usual = [n for n in sp if sp[n] >= top / 5]
    best = max(usual, key=lambda n: (ours.get(n, 0), sp[n]), default=None)
    if best and ours.get(best, 0) > 0:
        return best
    name = place["name"]
    head, _, tail = name.rpartition(" ")
    return head if tail.isdigit() else name


# --- Labels ---------------------------------------------------------------------------------

def spine(mask, sheet, step=3, bins=10, trim=12):
    """A gently curved line through the length of a region, for spreading its name along.

    Returns (points in km, cross-width in km). Reads left to right, or top to bottom when
    the region runs more north-south than east-west."""
    ys, xs = np.nonzero(mask[::step, ::step])
    if len(xs) < 20:
        return None, 0
    pts = np.c_[xs, ys] * step * sheet.res
    c = pts.mean(0)
    evals, evecs = np.linalg.eigh(np.cov((pts - c).T))
    u = evecs[:, np.argmax(evals)]
    if abs(u[0]) >= 0.42:
        u = u if u[0] > 0 else -u
    else:
        u = u if u[1] > 0 else -u
    v = np.array([-u[1], u[0]])
    a, b = (pts - c) @ u, (pts - c) @ v
    lo, hi = np.percentile(a, [trim, 100 - trim])
    edges = np.linspace(lo, hi, bins + 1)
    mid = [((edges[i] + edges[i + 1]) / 2, np.median(b[(a >= edges[i]) & (a < edges[i + 1])]))
           for i in range(bins) if ((a >= edges[i]) & (a < edges[i + 1])).sum() > 3]
    mid = np.array(mid)
    coef = np.polyfit(mid[:, 0], mid[:, 1], 2 if len(mid) >= 5 else 1)
    t = np.linspace(lo, hi, 16)
    line = c + np.outer(t, u) + np.outer(np.polyval(coef, t), v)
    width = float(np.percentile(np.abs(b - np.polyval(coef, a)), 70) * 2)
    return np.round(line, 2).tolist(), width


def follow(lines, lon, lat, sheet, length_km, reach_km=6):
    """The stretch of the nearest polyline (km units) around a point, about `length_km` long."""
    x, y = sheet.xy(lon, lat)
    best = None
    for ln in lines:
        d = np.hypot(ln[:, 0] - x, ln[:, 1] - y)
        i = int(np.argmin(d))
        if best is None or d[i] < best[0]:
            best = (d[i], ln, i)
    if best is None or best[0] > reach_km:
        return None
    _, ln, i = best
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(ln, axis=0).T))]
    s0 = max(seg[i] - length_km / 2, 0)
    s1 = min(s0 + length_km, seg[-1])
    s0 = max(s1 - length_km, 0)
    keep = (seg >= s0) & (seg <= s1)
    out = ln[keep]
    if out[-1][1] < out[0][1] and abs(out[-1][0] - out[0][0]) < abs(out[-1][1] - out[0][1]):
        out = out[::-1]                 # mostly vertical: read downward
    elif out[-1][0] < out[0][0] and abs(out[-1][0] - out[0][0]) >= abs(out[-1][1] - out[0][1]):
        out = out[::-1]                 # mostly horizontal: read rightward
    return np.round(out[::max(1, len(out) // 16)], 2).tolist()


# --- Shared by every map ----------------------------------------------------------------------

def sheet_info(sheet):
    return {"width": round(sheet.width, 2), "height": round(sheet.height, 2), "west": sheet.west,
            "east": sheet.east, "south": sheet.south, "north": sheet.north, "kx": sheet.kx, "ky": sheet.ky}


def terrain_layers(sheet, land, lakes, flow, wet, river_km2, hachure_km, no_rivers=None,
                   ripple_km=(0.45, 1.0, 1.7, 2.6, 3.7, 5.0), river_classes=(1000, 8000), min_slope=5):
    """Coast, water lines, lakes, rivers (from the drainage) and hachures, as SVG path data.
    `no_rivers` masks out ground where drainage lines mislead, such as a flat delta or a
    desert. The water lines and river widths scale with the sheet: `ripple_km` are the
    distances of the lines from the shore, `river_classes` the drainage areas (km^2) at
    which a river is drawn wider."""
    res = sheet.res
    d = lambda lines, close=False, digits=2: path_d(lines, res, digits, close)
    lake_km = [ripple_km[0] * 2 / 3, ripple_km[1] * 0.7]
    layers = {
        "land": d(outlines(land), True),
        "coast": d(outlines(land, closed=False)),
        "ripples": d(ripples(sheet, land, list(ripple_km)), digits=1),
        "lakes": d(outlines(lakes, smooth=0.8), True),
        "lakeRipples": d(ripples(sheet, ~lakes, lake_km), digits=1),
    }
    area, recv, shape = flow
    blocked = wet if no_rivers is None else (wet | no_rivers)
    river_lines = rivers(sheet, area, recv, shape, 2, blocked, river_km2)
    smooth = [(chaikin(densify(simplify(p, 1.2), 4), 2), a) for p, a in river_lines]
    lo1, lo2 = river_classes
    layers["rivers"] = [d([p for p, a in smooth if lo <= a < hi], digits=1)
                        for lo, hi in ((0, lo1), (lo1, lo2), (lo2, 1e12))]
    hs = hachures(sheet, sheet.elev, wet, spacing_km=hachure_km, min_slope=min_slope)
    layers["hachures"] = [d([p for p, wt in hs if k / 4 <= wt < (k + 1) / 4 or (k == 3 and wt >= 1)], digits=1)
                          for k in range(4)]
    return layers, [p * res for p, _ in smooth]


def territory_layers(sheet, terr, names, groups, tints):
    """Fills for each territory, its name along its length, and the borders between them,
    each drawn once: between nations (different groups) or between tribes (the same group)."""
    d = lambda lines, close=False, digits=2: path_d(lines, sheet.res, digits, close)
    fills, labels = [], []
    borders = {"nation": [], "tribe": []}
    for i, n in enumerate(names):
        m = terr == i
        if not m.any():
            continue
        line, width = spine(m, sheet)
        tint = tints.get(n, tints.get(groups[n]))      # a territory's own tint, else its group's
        fills.append({"name": n, "group": groups[n], "tint": tint, "d": d(outlines(m, smooth=1.5), True)})
        if line:
            labels.append({"text": n.replace(" (east)", "").upper(), "style": "nation" if groups[n] == n else "tribe",
                           "pts": line, "width": round(width, 1)})
        field = ndimage.gaussian_filter(m.astype(np.float64), 1.5)
        for ln in contours(field, 0.5):
            if len(ln) < 6:
                continue
            ln = densify(simplify(ln, 0.5), 2)
            tang = np.gradient(ln, axis=0)
            nrm = np.c_[tang[:, 1], -tang[:, 0]]
            nrm /= np.hypot(*nrm.T)[:, None] + 1e-9
            probe = np.round(ln + nrm * 1.5).astype(int)
            probe[:, 0] = probe[:, 0].clip(0, field.shape[1] - 1)
            probe[:, 1] = probe[:, 1].clip(0, field.shape[0] - 1)
            if np.mean(field[probe[:, 1], probe[:, 0]] > 0.5) > 0.5:
                nrm = -nrm
            out_pt = np.round(ln + nrm * 3).astype(int)
            out_pt[:, 0] = out_pt[:, 0].clip(0, terr.shape[1] - 1)
            out_pt[:, 1] = out_pt[:, 1].clip(0, terr.shape[0] - 1)
            other = terr[out_pt[:, 1], out_pt[:, 0]]
            kind = [None if (o < 0 or o <= i) else ("tribe" if groups[names[o]] == groups[n] else "nation")
                    for o in other]
            run = []
            for pt, k in zip(ln, kind + [None]):
                if run and k != run[0][1]:
                    if run[0][1] and len(run) > 3:
                        borders[run[0][1]].append(chaikin(np.array([p for p, _ in run]), 2))
                    run = []
                if k:
                    run.append((pt, k))
            if run and len(run) > 3:
                borders[run[0][1]].append(chaikin(np.array([p for p, _ in run]), 2))
    return fills, labels, {k: d(v, digits=1) for k, v in borders.items() if v}


def line_km(sheet, lonlats, n=16):
    """A polyline given in longitude and latitude, as n evenly spaced points in km."""
    pts = np.array([sheet.xy(lon, lat) for lon, lat in lonlats])
    t = np.linspace(0, 1, n)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    seg /= seg[-1]
    return np.round(np.c_[np.interp(t, seg, pts[:, 0]), np.interp(t, seg, pts[:, 1])], 2).tolist()


def place_records(sheet, all_places, books, ours, terr=None, names=None, capitals=None, min_score=200, kinds=None):
    """Towns named in the given books, one per site, in the order the labels are placed. `kinds`
    lets other kinds of place in too (pools, springs, gardens, hills), for a plan of a city."""
    import collections
    by_site = collections.defaultdict(list)
    for p in all_places:
        if not (sheet.west <= p["lon"] <= sheet.east and sheet.south <= p["lat"] <= sheet.north):
            continue
        named = [v for v in p["verses"] if v[0] in books]
        if not (set(p["types"]) & set(kinds or ["settlement"])) or not named or p["score"] < min_score:
            continue
        by_site[(round(p["lon"], 3), round(p["lat"], 3))].append((len(named), p, named))
    out = []
    for site in by_site.values():
        site.sort(key=lambda t: -t[0])
        _, p, named = site[0]
        x, y = sheet.xy(p["lon"], p["lat"])
        first = min(named, key=lambda v: (BOOK_ORDER[v[0]], v[1], v[2]))
        rec = {"n": verse_name(p, ours, first), "x": round(x, 2), "y": round(y, 2),
               "v": sum(t[0] for t in site), "s": p["score"],
               "c": 1 if p["score"] >= 500 and p["exact"] else 0,
               "f": f"{OSIS_LABEL[first[0]]} {first[1]}:{first[2]}",
               "id": p["id"] + "/" + p["slug"]}
        if p["modern"]:
            rec["m"] = p["modern"]
        if terr is not None:
            r, c = int(y / sheet.res), int(x / sheet.res)
            t = terr[min(r, terr.shape[0] - 1), min(c, terr.shape[1] - 1)]
            if t >= 0:
                rec["t"] = names[t]
        aka = sorted({display_name(q, ours) for _, q, _ in site[1:]} - {rec["n"]})
        if aka:
            rec["a"] = aka
        if capitals and p["name"] in capitals:
            rec["cap"] = capitals[p["name"]]
        out.append(rec)
    out.sort(key=lambda r: (-("cap" in r), -r["c"], -r["v"]))
    # One name for one town: OpenBible sometimes has two sites a few km apart for a town (the
    # Jericho of Joshua and the Jericho of the Gospels); keep the better known.
    kept = []
    for r in out:
        if not any(k["n"] == r["n"] and math.hypot(k["x"] - r["x"], k["y"] - r["y"]) < 5 for k in kept):
            kept.append(r)
    return kept


def cost_grid(sheet, wet, step=4, slope_weight=25.0):
    """Cost of crossing each cell of a coarse grid on foot: steep ground costs more, water
    can't be crossed."""
    ny, nx = sheet.elev.shape[0] // step, sheet.elev.shape[1] // step
    e = ndimage.gaussian_filter(sheet.elev, 1.5)[:ny * step:step, :nx * step:step]
    cell = sheet.res * step
    gy, gx = np.gradient(e, cell * 1000)
    cost = cell * (1 + slope_weight * np.hypot(gx, gy))
    cost[wet[:ny * step:step, :nx * step:step]] = np.inf
    return cost, step


def _pull_straight(path, cost):
    """Drop the corners of a grid path wherever the straight line between the points left
    stays on cells no dearer than the path's own, so courses run straight across open water."""
    def clear(u, v):
        n = int(max(abs(v[0] - u[0]), abs(v[1] - u[1]))) * 2 + 1
        rr = np.rint(np.linspace(u[0], v[0], n)).astype(int)
        cc = np.rint(np.linspace(u[1], v[1], n)).astype(int)
        return np.all(cost[rr, cc] <= max(cost[u], cost[v]))
    out, i = [path[0]], 0
    while i < len(path) - 1:
        j = len(path) - 1
        while j > i + 1 and not clear(path[i], path[j]):
            j -= 1
        out.append(path[j])
        i = j
    return out


def easiest_way(sheet, grid, a, b, ends=(True, True), straight=False):
    """The least-cost path between two points (lon, lat), as a smoothed polyline in km. With
    `ends` false at either end, the line stops where the grid can first be crossed (at the
    water's edge, for a voyage to an island) rather than at the point itself."""
    import heapq
    cost, step = grid
    ny, nx = cost.shape
    cell = sheet.res * step

    def node(lon, lat):
        x, y = sheet.xy(lon, lat)
        r, c = min(max(int(y / cell), 0), ny - 1), min(max(int(x / cell), 0), nx - 1)
        if np.isinf(cost[r, c]):            # on an island or in the water: the nearest dry cell
            dry = np.argwhere(~np.isinf(cost[max(r - 12, 0):r + 13, max(c - 12, 0):c + 13]))
            if len(dry):
                k = np.argmin(np.hypot(dry[:, 0] - min(r, 12), dry[:, 1] - min(c, 12)))
                r, c = dry[k][0] + max(r - 12, 0), dry[k][1] + max(c - 12, 0)
        return r, c
    s, g = node(*a), node(*b)
    floor = float(np.min(cost))
    dist = {s: 0.0}
    prev = {}
    pq = [(0.0, s)]
    nbrs = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142)]
    while pq:
        f, u = heapq.heappop(pq)
        if u == g:
            break
        du = dist[u]
        for dr, dc, m in nbrs:
            v = (u[0] + dr, u[1] + dc)
            if not (0 <= v[0] < ny and 0 <= v[1] < nx) or np.isinf(cost[v]):
                continue
            nd = du + m * (cost[u] + cost[v]) / 2
            if nd < dist.get(v, np.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd + math.hypot(v[0] - g[0], v[1] - g[1]) * floor, v))
    if g not in prev and g != s:
        pts = np.array([sheet.xy(*a), sheet.xy(*b)])
    else:
        path = [g]
        while path[-1] != s:
            path.append(prev[path[-1]])
        path.reverse()
        if np.ptp(cost[np.isfinite(cost)]) < 1e-9 or straight:
            path = _pull_straight(path, cost)
        pts = (np.array(path)[:, ::-1] + 0.5) * cell
        if ends[0]:
            pts[0] = sheet.xy(*a)
        if ends[1]:
            pts[-1] = sheet.xy(*b)
    # Smooth at about a kilometre on a map of a land, and in proportion on a finer sheet.
    tol = 1.2 if sheet.res >= 0.1 else sheet.res * 9
    return chaikin(densify(simplify(pts, tol), tol * 2.5), 3)


def about_html(intro, kept, changed, made, sources):
    li = lambda items: "  <ul>\n" + "".join(f"    <li>{x}</li>\n" for x in items) + "  </ul>\n"
    return (f"  <p>{intro}</p>\n  <h3>What we kept from Eilers</h3>\n{li(kept)}  <h3>What we changed</h3>\n{li(changed)}"
            f"  <h3>How it was made</h3>\n{li(made)}  <h3>Sources</h3>\n{li(sources)}").rstrip("\n")


KEPT = ["Flat tints for each kingdom and people, with the seas left as paper",
        "Water lines along the coasts, and hachured relief",
        "Widely spaced capitals for regions and peoples, and red capitals for the kingdoms",
        'A "?" after places whose location is uncertain',
        "A grid with an index of places keyed to it"]
CHANGED = ["Labels never overlap. More appear as you zoom in.",
           "Type is never smaller than 11 pixels on screen",
           "Borders are drawn as lines as well as tints, so they don't depend on color"]
SOURCES = ['Places: <a href="https://www.openbible.info/geo/">OpenBible.info Bible Geocoding Data</a>, CC BY 4.0',
           "Elevation: AWS Terrain Tiles (SRTM, GMTED2010, ETOPO1)",
           "Style: the Eilers Sunday School wall maps, published before 1931"]
PLACES_MADE = ("<strong>Places</strong> are the towns named in {books} that OpenBible.info can locate. "
               'Places scored below 500 out of 1,000 are marked "?".')
NAMES_MADE = "<strong>Names</strong> are spelled as in this project's Open Plain English Translation."


# --- Map No. 7: The Kingdoms of Judah and Israel ---------------------------------------------

SHEET7 = (34 + 10 / 60, 36.5, 30 + 50 / 60, 33 + 40 / 60)   # west, east, south, north

TINTS = {"Israel": "yellow", "Judah": "salmon", "Philistia": "sage", "Phoenicia": "blush",
         "Aram": "olive", "Ammon": "sage", "Moab": "olive", "Edom": "blush"}
CAPITALS = {"Jerusalem": "Capital of Judah", "Samaria 1": "Capital of Israel from Omri",
            "Tirzah": "Capital of Israel before Samaria", "Shechem": "Jeroboam's first capital"}
MOUNTAINS = ["Mount Hermon", "Mount Carmel", "Mount Tabor", "Mount Gilboa", "Mount Ebal",
             "Mount Gerizim", "Mount Nebo", "Mount of Olives"]
RIVERS = {"Jordan": 70, "Jabbok": 26, "Arnon": 22, "Kishon": 20, "Zered": 14, "Besor": 18,
          "Kanah 1": 14, "Me-jarkon": 14}
WATERS = {"Great Sea": ["GREAT SEA", (34.24, 32.868), (34.86, 32.858)],
          "Salt Sea": ["SALT SEA", (35.47, 31.69), (35.44, 31.40)]}
# Kingdom names run across the kingdom, as Eilers set them: ISRAEL from the coast to Gilead,
# JUDAH rising from the Negev to the hill country.
KINGDOM_LINES = {"Israel": [(34.98, 32.43), (35.45, 32.52), (35.98, 32.58)],
                 "Judah": [(34.86, 31.31), (35.06, 31.44), (35.28, 31.57)]}
REGIONS = ["Sharon 1", "Shephelah", "Negeb", "Bashan", "Gilead 1", "Lebanon", "Jeshimon",
           "Valley of Jezreel", "Zin 1"]


def mountains(sheet, by_name, ours, names):
    out = []
    for n in names:
        p = by_name[n]
        x, y = sheet.xy(p["lon"], p["lat"])
        name = display_name(p, ours)
        name = name if name.startswith("Mount") else "Mount " + name
        out.append({"n": name.replace("Mount ", "Mt. "), "x": round(x, 2), "y": round(y, 2), "id": p["id"] + "/" + p["slug"]})
    return out


AT_THE_JORDAN = {"word": "Jordan", "at": (35.548, 31.838), "sure": 0, "site": "opposite Jericho (traditional)"}
PROPHETS = [
    {"name": "Elijah", "short": "Elijah", "ref": "1 Kings 17 – 2 Kings 2", "color": "blue", "unit": "Place",
     "note": "From the brook where the ravens fed him to Zarephath, Mount Carmel and Horeb, and across the Jordan, "
             "where he was taken up in a whirlwind.",
     "stops": [
         ("Gilead 1", "Gilead", "1 Kings 17:1", None, {"why": "Not plotted: Elijah came from the settlers of Gilead; the "
                                                             "text names no town."}),
         ("Cherith", "Kerith Ravine", "1 Kings 17:3", "land", {"word": "Kerith", "what": "Fed by ravens"}),
         ("Zarephath", "Zarephath", "1 Kings 17:9", "land", {"what": "The widow's flour and oil; her son raised"}),
         ("Samaria 1", "Samaria", "1 Kings 18:2", "land"),
         ("Mount Carmel", "Mount Carmel", "1 Kings 18:20", "land", {"what": "Fire from heaven; the prophets of Baal"}),
         ("Jezreel 2", "Jezreel", "1 Kings 18:46", "land", {"what": "Elijah runs ahead of Ahab's chariot"}),
         ("Beersheba 1", "Beersheba", "1 Kings 19:3", "land", {"what": "Fleeing from Jezebel"}),
         (None, "Horeb", "1 Kings 19:8", "land", {"why": "Not plotted: Horeb, the mountain of God, lies south of this map "
                                                         "(see Map No. 5)."}),
         ("Abel-meholah", "Abel-meholah", "1 Kings 19:16", "land", {"what": "Elijah calls Elisha"}),
         ("Jezreel 2", "Jezreel", "1 Kings 21:1", "land", {"what": "Naboth's vineyard"}),
         ("Gilgal 2", "Gilgal", "2 Kings 2:1", "land"),
         ("Bethel 1", "Bethel", "2 Kings 2:2", "land"),
         ("Jericho 1", "Jericho", "2 Kings 2:4", "land"),
         (None, "The Jordan", "2 Kings 2:7", "land", AT_THE_JORDAN | {"what": "Elijah is taken up in a whirlwind"}),
     ]},
    {"name": "Elisha", "short": "Elisha", "ref": "1 Kings 19 – 2 Kings 8", "color": "green", "unit": "Place",
     "note": "Called from the plow at Abel-meholah, Elisha took up Elijah's cloak at the Jordan and went about the "
             "land, from Jericho and Shunem to Samaria, Dothan and Damascus.",
     "stops": [
         ("Abel-meholah", "Abel-meholah", "1 Kings 19:16", None, {"what": "Called from the plow"}),
         (None, "The Jordan", "2 Kings 2:13", "land", AT_THE_JORDAN | {"what": "He takes up Elijah's cloak"}),
         ("Jericho 1", "Jericho", "2 Kings 2:18", "land", {"what": "The water made wholesome"}),
         ("Bethel 1", "Bethel", "2 Kings 2:23", "land"),
         ("Mount Carmel", "Mount Carmel", "2 Kings 2:25", "land"),
         ("Samaria 1", "Samaria", "2 Kings 2:25", "land"),
         ("Shunem", "Shunem", "2 Kings 4:8", "land", {"what": "The Shunammite woman's room"}),
         ("Mount Carmel", "Mount Carmel", "2 Kings 4:25", "land", {"what": "She comes to him; her son is raised at Shunem"}),
         ("Gilgal 2", "Gilgal", "2 Kings 4:38", "land", {"what": "Death in the pot"}),
         ("Samaria 1", "Samaria", "2 Kings 5:3", "land", {"what": "Naaman is sent to him and healed"}),
         ("Dothan", "Dothan", "2 Kings 6:13", "land", {"what": "Horses and chariots of fire"}),
         ("Samaria 1", "Samaria", "2 Kings 6:19", "land"),
         ("Damascus", "Damascus", "2 Kings 8:7", "land", {"what": "Ben-hadad's sickness; Hazael"}),
     ]},
]


def kingdoms_map():
    """Map No. 7, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET7, res=0.13)
    sheet.elev = elevation(sheet, 10)
    w = water(sheet, sheet.elev)
    lakes = w["Sea of Galilee"] | w["Dead Sea"] | w["Lake Huleh"]
    wet = w["sea"] | lakes
    flow = drainage(sheet, sheet.elev, w["sea"] | w["Dead Sea"], 2)
    all_places = places()
    names = list(NEIGHBOURS) + [t[0] for t in TRIBES]
    terr, names = territories(sheet, sheet.elev, wet, flow + (2,), seeds(all_places), names=names)
    ours = our_spellings()
    groups = {n: n for n in NEIGHBOURS}
    groups.update({t[0]: t[1] for t in TRIBES})

    layers, river_km = terrain_layers(sheet, ~w["sea"], lakes, flow, wet, 150, 0.9)
    fills, labels, layers["borders"] = territory_layers(sheet, terr, names, groups, TINTS)
    for k in ("Israel", "Judah"):
        west = [t[0] for t in TRIBES if t[1] == k and t[0] not in ("Reuben", "Gad", "Manasseh (east)")]
        _, width = spine(np.isin(terr, [names.index(t) for t in west]), sheet, trim=8)
        labels.append({"text": k.upper(), "style": "kingdom", "pts": line_km(sheet, KINGDOM_LINES[k]), "width": round(width, 1)})
    # The tribe of Judah is named by its kingdom's red name.
    labels = [lb for lb in labels if lb["style"] == "kingdom" or lb["text"] not in ("ISRAEL", "JUDAH")]
    for n, (text, a, b) in WATERS.items():
        labels.append({"text": text, "style": "sea", "pts": line_km(sheet, [a, b], 2)})

    by_name = {p["name"]: p for p in all_places}
    feats = {"mountains": mountains(sheet, by_name, ours, MOUNTAINS), "rivers": [], "waters": [], "regions": []}
    for n, length in RIVERS.items():
        p = by_name[n]
        line = follow(river_km, p["lon"], p["lat"], sheet, length)
        if line:
            name = display_name(p, ours)
            feats["rivers"].append({"n": "River Jordan" if name == "Jordan" else name, "pts": line, "main": name == "Jordan"})
    for lon, lat, text in ((35.585, 32.80, "SEA OF KINNERETH"), (35.612, 33.075, "Waters of Merom")):
        x, y = sheet.xy(lon, lat)
        feats["waters"].append({"n": text, "x": round(x, 2), "y": round(y, 2), "lake": 1})
    for n in REGIONS:
        p = by_name[n]
        x, y = sheet.xy(p["lon"], p["lat"])
        feats["regions"].append({"n": display_name(p, ours), "x": round(x, 2), "y": round(y, 2)})

    pl = place_records(sheet, all_places, OT_BOOKS, ours, terr, names, CAPITALS)
    journeys = build_journeys(sheet, PROPHETS, by_name, cost_grid(sheet, wet), sea_grid(sheet, w["sea"]), pl)
    data = {
        "sheet": sheet_info(sheet), "grid": 10 / 60, "focus": 0.56, "file": "map-07-kingdoms-of-judah-and-israel",
        "layers": layers, "territories": fills, "labels": labels,
        "places": pl, "journeys": journeys, "routeButton": "Prophets", "routesTitle": "Elijah and Elisha",
        "routesNote": "Choose a prophet to follow him place by place. Each place is named in the verse given.",
        "routeLayer": "The journeys of Elijah and Elisha",
        "features": feats, "unallotted": list(NEIGHBOURS),
        "title": {"box": {"x": 5, "y": 5, "w": 66, "h": 76}, "scale": 1, "lines": [
            ["series", "MAP No. 7 · A STYLE STUDY", 7.5], ["head", "THE KINGDOMS", 15.5],
            ["display-fit", "JUDAH & ISRAEL", 26],
            ["italic", "Showing the places of the land named in the", 32.5],
            ["italic", "Old Testament whose location is known, and", 36.4],
            ["italic", "the tribal allotments of Joshua 13–19", 40.3], ["rule", "", 44],
            ["sub", "THE KINGDOM DIVIDED", 50.5], ["plain", "975–588 BC by Ussher’s chronology", 55.5],
            ["plain", "931–586 BC by modern reckoning", 59.5], ["rule", "", 63],
            ["credit", "After the Eilers Sunday School Maps, St. Louis.", 67.5],
            ["credit", "Drawn from open data · CC BY 4.0", 71.5]]},
        "key": {"box": {"x": 5, "y": 97, "w": 44}, "scale": 1, "rows": [
            ["camp", "Place on a journey"], ["journey", "Elijah", "blue"], ["journey", "Elisha", "green"],
            ["conjectural", "Way uncertain"], ["gap", ""],
            ["dot", "Town"], ["unsure", "Site uncertain (?)"], ["royal", "Royal city"], ["mount", "Mountain"],
            ["river", "River"], ["nation", "Border of a nation"], ["tribe", "Tribal border"], ["gap", ""],
            ["names", ["Shiloh", "Tell Seilun"]],
            ["swatch", "Kingdom of Israel", "yellow"], ["swatch", "Kingdom of Judah", "salmon"],
            ["swatch", "Philistia, Ammon", "sage"], ["swatch", "Phoenicia, Edom", "blush"],
            ["swatch", "Aram, Moab", "olive"], ["swatch", "Wilderness", "wild"]]},
    }
    page = {
        "slug": "kingdoms", "NO": "7", "H1": "The Kingdoms of Judah and Israel", "TITLE": "Judah and Israel Map",
        "DESCRIPTION": "Map No. 7, a style study after the Eilers Sunday School wall maps: the tribal allotments "
                       "and the kingdoms of Judah and Israel, drawn from open data.",
        "GRID_LABEL": "Ten-minute squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, redrawing <strong>Eilers Sunday School Map "
            "No. 7</strong>, <em>The Kingdoms Judah Israel</em> (A. H. Eilers &amp; Co., St. Louis), from open data. "
            "It keeps the Eilers look and aims to read more easily.", KEPT, CHANGED,
            ["<strong>Land, water and relief</strong> come from elevation data. Lake Huleh and the Dead Sea are "
             "drawn at their old shorelines.",
             PLACES_MADE.format(books="the Old Testament"),
             "<strong>Tribal territories are approximate.</strong> Each piece of land is given to the tribe whose "
             "towns are nearest (the town lists of Joshua 13–19 and 21). Lakes cannot be crossed, and rivers are "
             "costly to cross, so borders tend to follow the rivers.", NAMES_MADE], SOURCES),
    }
    return data, page


# --- Map No. 5: The Exodus -------------------------------------------------------------------

SHEET5 = (30 + 40 / 60, 36.0, 27 + 40 / 60, 32.0)

TORAH = {"Gen", "Exod", "Lev", "Num", "Deut"}
# The camps of Numbers 33, in order: OpenBible's name for each (None where the text names no
# place of its own), our translation's name, and the verse.
CAMPS = [
    ("Rameses", "Rameses", "Numbers 33:5"), ("Succoth 2", "Succoth", "Numbers 33:5"),
    ("Etham", "Etham", "Numbers 33:6"), ("Pi-hahiroth", "Pi-hahiroth", "Numbers 33:7"),
    ("Marah", "Marah", "Numbers 33:8"), ("Elim", "Elim", "Numbers 33:9"),
    (None, "By the Red Sea", "Numbers 33:10"), ("Sin", "Wilderness of Sin", "Numbers 33:11"),
    ("Dophkah", "Dophkah", "Numbers 33:12"), ("Alush", "Alush", "Numbers 33:13"),
    ("Rephidim", "Rephidim", "Numbers 33:14"), ("Wilderness of Sinai", "Wilderness of Sinai", "Numbers 33:15"),
    ("Kibroth-hattaavah", "Kibroth-hattaavah", "Numbers 33:16"), ("Hazeroth", "Hazeroth", "Numbers 33:17"),
    ("Rithmah", "Rithmah", "Numbers 33:18"), ("Rimmon-perez", "Rimmon-perez", "Numbers 33:19"),
    ("Libnah 2", "Libnah", "Numbers 33:20"), ("Rissah", "Rissah", "Numbers 33:21"),
    ("Kehelathah", "Kehelathah", "Numbers 33:22"), ("Mount Shepher", "Mount Shepher", "Numbers 33:23"),
    ("Haradah", "Haradah", "Numbers 33:24"), ("Makheloth", "Makheloth", "Numbers 33:25"),
    ("Tahath", "Tahath", "Numbers 33:26"), ("Terah", "Terah", "Numbers 33:27"),
    ("Mithkah", "Mithkah", "Numbers 33:28"), ("Hashmonah", "Hashmonah", "Numbers 33:29"),
    ("Moseroth", "Moseroth", "Numbers 33:30"), ("Bene-jaakan", "Bene-jaakan", "Numbers 33:31"),
    ("Hor-haggidgad", "Hor-haggidgad", "Numbers 33:32"), ("Jotbathah", "Jotbathah", "Numbers 33:33"),
    ("Abronah", "Abronah", "Numbers 33:34"), ("Ezion-geber", "Ezion-geber", "Numbers 33:35"),
    ("Kadesh-barnea", "Kadesh", "Numbers 33:36"), ("Mount Hor 1", "Mount Hor", "Numbers 33:37"),
    ("Zalmonah", "Zalmonah", "Numbers 33:41"), ("Punon", "Punon", "Numbers 33:42"),
    ("Oboth", "Oboth", "Numbers 33:43"), ("Iye-abarim", "Iye-abarim", "Numbers 33:44"),
    ("Dibon 1", "Dibon-gad", "Numbers 33:45"), ("Almon-diblathaim", "Almon-diblathaim", "Numbers 33:46"),
    ("Abarim", "Mountains of Abarim", "Numbers 33:47"), ("Abel-shittim", "Plains of Moab", "Numbers 33:48–49"),
]
# Camps left off the route although OpenBible proposes a place for them, and why.
CAMP_NOT_PLOTTED = {
    "Rissah": "One proposal places it at Sharma, on the Arabian coast, which does not fit the order of the camps.",
    "Tahath": "Placed only somewhere in the Negev.", "Terah": "Placed only somewhere in the Negev.",
    "Mithkah": "Placed only somewhere in the Negev.", "Hashmonah": "Placed only somewhere in the Negev.",
    None: "The text names the sea, not a place on its shore.",
}
CAMP_NOTES = {
    "Marah": "Between Pi-hahiroth and Marah the Israelites passed through the sea (Numbers 33:8). Proposed "
             "crossings include the Gulf of Suez, the Bitter Lakes, Lake Timsah, the Ballah Lakes, Lake "
             "Sirbonis (Bardawil) and the Gulf of Aqaba.",
    "Wilderness of Sinai": "The camp at the mountain, plotted at Jebel Musa, the traditional Mount Sinai. The "
                           "site is disputed: the triangles on the map mark other proposals.",
    "Kadesh-barnea": "Also the camp of Numbers 13–14 and 20, where the spies were sent out.",
}
MIN_CAMP_SCORE = 150     # proposals scored lower are listed, not plotted
SURE_CAMP_SCORE = 500    # and those scored at least this, at a point, are drawn as certain
LINE_CAMP_SCORE = 300    # the route is solid only between neighbouring camps scored this or more
SINAI = {"Jebel Musa": "Mt. Sinai (traditional)", "Har Karkom": "Har Karkom?", "Jebel Sin Bishar": "Jebel Sin Bishar?",
         "Jebel Serbal": "Jebel Serbal?", "Jabal al Lawz": "Jabal al-Lawz?"}
# Ancient roads named in the story, through the places that standard reconstructions give them.
ROADS = {
    "Way of the Philistines": [(32.367, 30.935), (32.75, 31.02), (33.25, 31.06), (33.806, 31.13), (34.25, 31.29), (34.464, 31.504)],
    "King's Highway": [(35.0, 29.53), (35.36, 29.95), (35.73, 30.19), (35.604, 30.746), (35.701, 31.181),
                       (35.777, 31.502), (35.795, 31.716), (35.809, 31.801)],
}
ROAD_NOTES = {"Way of the Philistines": "Exodus 13:17", "King's Highway": "Numbers 20:17; 21:22"}
NATIONS5 = {   # territory: (tint, OpenBible seeds, reach in km)
    "Egypt": ("yellow", None, 30),
    "Canaan": ("lime", None, 26),
    "Edom": ("olive", ["Bozrah 1", "Sela 1", "Mount Seir 1"], 34),
    "Moab": ("sage", ["Kir-hareseth", "Ar"], 24),
    "Amorites": ("salmon", ["Heshbon", "Medeba"], 20),
    "Midian": ("wild", ["Midian"], 55),
}
WILDERNESS_LINES = {
    "WILDERNESS OF SHUR": [(32.62, 30.62), (33.55, 30.42)],
    "WILDERNESS OF SIN": [(33.1, 29.32), (33.62, 29.02)],
    "WILDERNESS OF PARAN": [(33.55, 30.02), (34.6, 29.72)],
    "WILDERNESS OF ZIN": [(34.25, 30.85), (35.26, 30.99)],
    "WILDERNESS OF SINAI": [(33.62, 28.3), (34.3, 28.25)],
    "GOSHEN": [(31.45, 30.62), (31.98, 30.66)],
}
SEAS5 = {"GREAT SEA": ("sea", [(30.85, 31.78), (32.15, 31.74)]),
         "RED SEA": ("redsea", [(32.64, 29.6), (33.3, 28.38)]),
         "SALT SEA": ("sea", [(35.47, 31.69), (35.44, 31.40)])}


def natural_earth(layer):
    """The features of a Natural Earth 1:10m layer (public domain), downloaded once."""
    path = os.path.join(CACHE, "naturalearth", f"ne_10m_{layer}.geojson")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        url = f"https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_10m_{layer}.geojson"
        with open(path, "wb") as f:
            f.write(urllib.request.urlopen(url, timeout=300).read())
    return json.load(open(path, encoding="utf-8"))["features"]


def nile(sheet):
    """The Nile and its two branches from Natural Earth, as polylines in km."""
    out = []
    for ft in natural_earth("rivers_lake_centerlines"):
        if ft["properties"].get("name") not in ("Nile", "Rosetta Branch", "Damietta Branch"):
            continue
        g = ft["geometry"]
        for part in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            pts = np.array([sheet.xy(lon, lat) for lon, lat in part])
            keep = (pts[:, 0] > -20) & (pts[:, 0] < sheet.width + 20) & (pts[:, 1] > -20) & (pts[:, 1] < sheet.height + 20)
            if keep.sum() > 1:
                out.append(chaikin(pts[keep], 2))
    return out


def exodus_map():
    """Map No. 5, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET5, res=0.2)
    sheet.elev = elev = elevation(sheet, 10)
    comp = lambda mask, lon, lat: _component(mask, sheet, lon, lat)
    sea = comp(elev <= 0, 31.5, 31.9) | comp(elev <= 0, 32.9, 29.0) | comp(elev <= 0, 34.73, 28.8)
    dead = ndimage.binary_fill_holes(comp(elev <= -392, 35.50, 31.50))
    # The Great Bitter Lake and the lagoons of Manzala and Bardawil (Lake Sirbonis), below sea
    # level in the elevation data. Lake Timsah is too small to show.
    low = (elev <= 0) & ~sea
    lagoons = comp(low, 32.38, 30.35) | comp(low, 32.0, 31.25) | comp(low, 33.16, 31.19)
    lakes = dead | ndimage.binary_fill_holes(lagoons)
    wet = sea | lakes
    land = ~sea
    flow = drainage(sheet, elev, sea | dead, 2)
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    res = sheet.res

    # Peoples and lands. Egypt is the Nile valley and delta: its towns and points along the
    # river. Canaan is the land of its towns named in Genesis.
    nile_km = nile(sheet)
    seeds5 = []
    for p in all_places:
        if "settlement" not in p["types"] or p["score"] < 300 or not p["exact"]:
            continue
        if p["lon"] < 32.6 and p["lat"] > 29.0:
            seeds5.append((p["name"], "Egypt", p["lon"], p["lat"]))
        elif p["lat"] > 31.15 and 34.2 < p["lon"] < 35.45 and any(v[0] == "Gen" for v in p["verses"]):
            seeds5.append((p["name"], "Canaan", p["lon"], p["lat"]))
    for line in nile_km:
        for x, y in line[::12]:
            lon, lat = sheet.lonlat(x, y)
            if lat < 31.3:
                seeds5.append(("Nile", "Egypt", lon, lat))
    for n, (_, names, _) in NATIONS5.items():
        for name in names or []:
            p = by_name[name]
            seeds5.append((name, n, p["lon"], p["lat"]))
    terr_names = list(NATIONS5)
    terr = np.full(elev.shape, -1, np.int32)
    for i, n in enumerate(terr_names):       # each people reaches its own distance
        t, _ = territories(sheet, elev, wet, flow + (2,), [s for s in seeds5 if s[1] == n], cap_km=NATIONS5[n][2],
                           names=terr_names, barrier=None)
        terr[(t == i) & (terr < 0)] = i
    groups = {n: n for n in terr_names}
    tints = {n: v[0] for n, v in NATIONS5.items()}

    no_rivers = np.zeros(elev.shape, bool)                  # the Nile valley and delta
    cols = np.arange(elev.shape[1]) * res
    rows = np.arange(elev.shape[0]) * res
    lon_g = sheet.west + cols / sheet.kx
    lat_g = sheet.north - rows / sheet.ky
    no_rivers[np.ix_(lat_g > 29.4, lon_g < 32.25)] = True
    no_rivers[:, lon_g < 31.45] = True
    layers, river_km = terrain_layers(sheet, land, lakes, flow, wet, 600, 1.4, no_rivers)
    layers["nile"] = path_d([ln / res for ln in nile_km], res, 1)
    fills, labels, layers["borders"] = territory_layers(sheet, terr, terr_names, groups, tints)
    for text, (style, pts) in SEAS5.items():
        labels.append({"text": text, "style": style, "pts": line_km(sheet, pts, 2)})
    labels.append({"text": "Gulf of Aqaba", "style": "sea", "pts": line_km(sheet, [(34.62, 28.62), (34.83, 29.12)], 2), "size": 4.5})
    for text, pts in WILDERNESS_LINES.items():
        labels.append({"text": text, "style": "region", "pts": line_km(sheet, pts, 8), "size": 5.2})

    # The camps of Numbers 33, each named in its verse.
    bad = check_verses([{"name": "The camps", "stops": [(ob, name, ref, None) for ob, name, ref in CAMPS]}])
    if bad:
        raise ValueError("Camps not named in their verses:\n" + "\n".join(bad))
    grid = cost_grid(sheet, wet)
    camps = []
    for n, (ob, name, verse) in enumerate(CAMPS, 1):
        p = by_name.get(ob) if ob else None
        rec = {"n": n, "name": name, "ref": verse}
        if p:
            rec.update({"site": p["modern"] or "", "s": p["score"], "id": p["id"] + "/" + p["slug"]})
            inside = sheet.west <= p["lon"] <= sheet.east and sheet.south <= p["lat"] <= sheet.north
            if ob not in CAMP_NOT_PLOTTED and p["score"] >= MIN_CAMP_SCORE and inside:
                x, y = sheet.xy(p["lon"], p["lat"])
                rec.update({"x": round(x, 2), "y": round(y, 2), "lon": p["lon"], "lat": p["lat"],
                            "sure": 1 if p["score"] >= SURE_CAMP_SCORE and p["exact"] else 0})
            elif ob in CAMP_NOT_PLOTTED:
                rec["why"] = "Not plotted. " + CAMP_NOT_PLOTTED[ob]
            else:
                rec["why"] = f"Not plotted: the best proposal scores only {p['score']} of 1,000."
        else:
            rec["why"] = CAMP_NOT_PLOTTED[None]
        if ob in CAMP_NOTES:
            rec["note"] = CAMP_NOTES[ob]
        camps.append(rec)
    # Camps at the same spot share one marker; the later one says so.
    seen = {}
    for c in camps:
        if "x" not in c:
            continue
        key = (round(c["x"]), round(c["y"]))
        if key in seen:
            first = seen[key]
            c["note"] = (c.get("note", "") + f" Proposed at the same site as camp {first['n']}, {first['name']}.").strip()
            first["note"] = (first.get("note", "") + f" Camp {c['n']}, {c['name']}, is proposed at the same site.").strip()
            first["also"] = first.get("also", []) + [c["n"]]
            for k in ("x", "y", "sure"):
                c.pop(k)
            c["why"] = f"Shown with camp {first['n']}, at the same proposed site."
        else:
            seen[key] = c
    legs = []
    plotted = [c for c in camps if "x" in c]
    for a, b in zip(plotted, plotted[1:]):
        gap = b["n"] - a["n"] > 1 and any("x" not in c and "also" not in c and not c["why"].startswith("Shown with")
                                           for c in camps[a["n"]:b["n"] - 1])
        sure = not gap and a["s"] >= LINE_CAMP_SCORE and b["s"] >= LINE_CAMP_SCORE
        pts = easiest_way(sheet, grid, (a["lon"], a["lat"]), (b["lon"], b["lat"]))
        legs.append({"d": path_d([pts / res], res, 1), "sure": 1 if sure else 0})
    for c in camps:
        c.pop("lon", None)
        c.pop("lat", None)
    roads, road_lines = [], []
    for name, pts in ROADS.items():
        line = []
        for a, b in zip(pts, pts[1:]):
            seg = easiest_way(sheet, grid, a, b)
            line.append(seg if not line else seg[1:])
        line = np.vstack(line)
        road_lines.append({"d": path_d([line / res], res, 1)})
        mid = len(line) // 2
        span = line[max(mid - 40, 0):mid + 40]
        roads.append({"n": name, "pts": np.round(span[::max(1, len(span) // 16)], 2).tolist()})

    # Places named in Genesis to Deuteronomy; those that are camps are shown as camps.
    pl = place_records(sheet, all_places, TORAH, ours, terr, terr_names)
    for p in pl:
        for c in camps:
            if "x" in c and math.hypot(p["x"] - c["x"], p["y"] - c["y"]) < 1.0:
                p["st"] = [[0, c["n"]]]

    feats = {"mountains": mountains(sheet, by_name, ours, ["Mount Nebo"]), "rivers": [], "waters": [],
             "regions": [], "roads": roads, "sinai": []}
    feats["rivers"].append({"n": "NILE", "pts": follow(nile_km, 31.27, 29.6, sheet, 90), "main": True})
    for n, length in {"Brook of Egypt": 60, "Zered": 22, "Arnon": 24}.items():
        p = by_name[n]
        line = follow(river_km, p["lon"], p["lat"], sheet, length)
        if line:
            feats["rivers"].append({"n": display_name(p, ours), "pts": line})
    for lon, lat, text in ((32.40, 30.33, "Bitter Lakes"), (32.0, 31.25, "Lake Manzala"), (33.16, 31.19, "Lake Sirbonis")):
        x, y = sheet.xy(lon, lat)
        feats["waters"].append({"n": text, "x": round(x, 2), "y": round(y, 2), "lake": 1})
    sinai = next(a for a in (json.loads(l) for l in open(os.path.join(_geo_repo(), "data", "ancient.jsonl"), encoding="utf-8"))
                 if a["friendly_id"] == "Mount Sinai")
    for idn in sinai["identifications"]:
        for r in idn.get("resolutions", [])[:1]:
            name = re.sub(r"<[^>]+>", "", r.get("description", ""))
            # Jebel Musa, the traditional site, is where camp 12 is plotted, so the camp marks it.
            if name in SINAI and "lonlat" in r and name != "Jebel Musa":
                lon, lat = map(float, r["lonlat"].split(","))
                x, y = sheet.xy(lon, lat)
                feats["sinai"].append({"n": SINAI[name], "x": round(x, 2), "y": round(y, 2),
                                       "s": idn["score"]["time_total"], "main": name == "Jebel Musa"})

    data = {
        "sheet": sheet_info(sheet), "grid": 20 / 60, "focus": 0.55, "file": "map-05-the-exodus",
        "land": "blush", "layers": layers, "territories": fills, "labels": labels,
        "places": pl, "features": feats, "roads": road_lines, "territoryLabel": "Land of",
        "routeLayer": "The camps of Numbers 33 and the ancient roads",
        "journeys": [{
            "name": "The camps of Numbers 33", "short": "Exodus", "ref": "Numbers 33", "color": "red", "unit": "Camp",
            "note": "From Rameses to the plains of Moab. Camps whose proposed site scores at least "
                    f"{MIN_CAMP_SCORE} of 1,000 are plotted, and marked \"?\" below {SURE_CAMP_SCORE}. The route is "
                    "dashed where the camps between are unknown or doubtful, and drawn along the easiest ground "
                    "between the camps.",
            "stops": camps, "legs": legs}],
        "title": {"box": {"x": 150, "y": 6, "w": 186, "h": 58}, "scale": 1.3, "lines": [
            ["series", "MAP No. 5 · A STYLE STUDY", 7.5], ["display", "THE EXODUS", 18.5],
            ["italic", "From Egypt to the plains of Moab: the camps of Numbers 33,", 24.5],
            ["italic", "with the places named in Genesis to Deuteronomy", 28.4], ["rule", "", 31.2],
            ["plain", "1491 BC by Ussher’s chronology · about 1446 or 1260 BC by modern reckoning", 36],
            ["credit", "After the Eilers Sunday School Maps, St. Louis · Drawn from open data · CC BY 4.0", 41]]},
        "key": {"box": {"x": 96, "y": 318, "w": 82}, "scale": 1.35, "scale_bars": [[0, 10, 20, 30], [0, 20, 40]], "rows": [
            ["camp", "Camp of Numbers 33"], ["camp-unsure", "Camp, site uncertain (?)"],
            ["route", "Route between proposed sites"], ["conjectural", "Route where the camps are unknown"],
            ["sinai", "Other proposed Mount Sinai"], ["road", "Ancient road (approximate)"], ["gap", ""],
            ["dot", "Town"], ["unsure", "Site uncertain (?)"], ["river", "River or wadi"],
            ["nation", "Border of a land or people"], ["gap", ""],
            ["swatch", "Egypt", "yellow"], ["swatch", "Canaan", "lime"], ["swatch", "Edom", "olive"],
            ["swatch", "Moab", "sage"], ["swatch", "Amorites (Sihon)", "salmon"], ["swatch", "Midian", "wild"],
            ["swatch", "Wilderness", "blush"]]},
    }
    # The title block's height follows its last line.
    data["title"]["box"]["h"] = round((data["title"]["lines"][-1][2] + 4.5) * data["title"]["scale"], 1)
    page = {
        "slug": "exodus", "NO": "5", "H1": "The Exodus", "TITLE": "The Exodus Map",
        "DESCRIPTION": "Map No. 5, a style study after the Eilers Sunday School wall maps: the camps of Numbers 33 "
                       "from Egypt to the plains of Moab, with the places of Genesis to Deuteronomy, drawn from open data.",
        "GRID_LABEL": "Twenty-minute squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, after <strong>Eilers Sunday School Map No. "
            "5</strong>, <em>The Exodus</em> (A. H. Eilers &amp; Co., St. Louis), redrawn from open data. Where "
            "Eilers drew one confident route, this map shows what is known and what is guessed.",
            KEPT[:2] + ["Widely spaced capitals for lands and wildernesses",
                        "A red route with numbered camps, and a table of the camps"] + KEPT[3:], CHANGED + [
                "Only camps with a proposed site are plotted, and the route is dashed where the camps between are "
                "unknown",
                "Mount Sinai is shown at each of its main proposed sites, not one"],
            ["<strong>Land, water and relief</strong> come from elevation data, and the Nile from Natural Earth. "
             "The Dead Sea is drawn at its old shoreline.",
             "<strong>The camps</strong> are those of Numbers 33, at the site OpenBible.info's sources favour. "
             "Most are uncertain; the table of camps gives each one's proposed site and certainty.",
             "<strong>The route</strong> joins the plotted camps along the easiest ground between them. It is a "
             "picture of the order of the camps, not a claim about the path.",
             "<strong>Lands are approximate</strong>, drawn around their towns. The roads follow standard "
             "reconstructions through the places that mark them.",
             PLACES_MADE.format(books="Genesis to Deuteronomy"), NAMES_MADE],
            SOURCES + ["Rivers: Natural Earth (public domain)"]),
    }
    return data, page


# --- Shared by the larger sheets and the journeys ---------------------------------------------

def sea_mask(sheet, elev, points):
    """The sea: ground at or below sea level that is joined to any of the points (lon, lat)."""
    lab, _ = ndimage.label(elev <= 0)
    keep = set()
    for lon, lat in points:
        x, y = sheet.xy(lon, lat)
        r, c = int(y / sheet.res), int(x / sheet.res)
        if 0 <= r < lab.shape[0] and 0 <= c < lab.shape[1] and lab[r, c]:
            keep.add(lab[r, c])
    return np.isin(lab, list(keep))


def ne_lakes(sheet, skip=()):
    """Natural lakes from Natural Earth as a mask on the sheet grid. Reservoirs are left out."""
    from PIL import ImageDraw
    img = Image.new("1", (sheet.nx, sheet.ny), 0)
    draw = ImageDraw.Draw(img)
    for ft in natural_earth("lakes"):
        pr = ft["properties"]
        if pr.get("featurecla") not in ("Lake", "Alkaline Lake") or pr.get("name") in skip:
            continue
        g = ft["geometry"]
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            for k, ring in enumerate(poly):
                pts = [(x / sheet.res, y / sheet.res) for x, y in (sheet.xy(lon, lat) for lon, lat in ring)]
                if len(pts) > 2:
                    draw.polygon(pts, fill=0 if k else 1)
    return np.asarray(img, bool)


def sea_grid(sheet, sea, step=2):
    """Cost of sailing across each cell of a coarse grid. Any cell with water in it can be
    crossed, so narrow straits such as Messina stay open, but cells that touch land cost eight
    times as much, so a ship takes a channel only when the way round is much longer."""
    ny, nx = sea.shape[0] // step, sea.shape[1] // step
    blocks = sea[:ny * step, :nx * step].reshape(ny, step, nx, step)
    water, open_ = blocks.any((1, 3)), blocks.all((1, 3))
    open_ = ndimage.binary_erosion(open_, iterations=1, border_value=1)
    cost = np.where(open_, 1.0, 8.0) * sheet.res * step
    return np.where(water, cost, np.inf), step


def give_islands(terr, land, max_cells):
    """Small pieces of land left out of every territory (islands with no town of their own)
    go to the nearest territory."""
    lab, n = ndimage.label(land & (terr < 0))
    if not n:
        return terr
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    small = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz <= max_cells])
    _, (ri, ci) = ndimage.distance_transform_edt(terr < 0, return_indices=True)
    out = terr.copy()
    out[small] = terr[ri[small], ci[small]]
    return out


def check_verses(journeys):
    """Every stop of every journey must be named in the verse it cites, as our translation
    spells it (a capital at the start of a stop's name may be small in the verse: "the
    wilderness of Sin"). Returns the stops that are not."""
    bad = []
    for J in journeys:
        for st in J["stops"]:
            ob, name, ref, how, extra = (list(st) + [{}])[:5]
            word = (extra or {}).get("word", name)
            if word and word.lower() not in english_verse(ref).lower():
                bad.append(f"{J['name']}: {name} is not in {ref}: {english_verse(ref)[:120]}")
    return bad


def build_journeys(sheet, specs, by_name, land_grid, water_grid, places_out):
    """The journeys on a sheet: numbered stops and the lines between them.

    Each spec has a name, short name, verses, color, unit ("Stop", "Camp") and note, and its
    stops as (OpenBible name, our name, verse, how, extra). `how` is how the stop was reached:
    "land", "sea", or None for the start. `extra` may give `via` (places passed on the way:
    OpenBible names or (lon, lat)), `guess` (the way between is a reconstruction, so the line is
    dashed), `at` ((lon, lat) for a stop OpenBible doesn't locate, such as a region's town),
    `sure` (0 to mark the stop uncertain), `word` (the name as the verse spells it), `what` (what
    happened there), `note`, and `why` (why a stop isn't plotted). Places in `places_out` that are
    stops get `st`, so the page can show them as stops instead. Every stop must be named in its
    verse; the build stops if one isn't."""
    bad = check_verses(specs)
    if bad:
        raise ValueError("Stops not named in their verses:\n" + "\n".join(bad))
    res = sheet.res
    out = []
    for j, spec in enumerate(specs):
        stops = []
        for n, st in enumerate(spec["stops"], 1):
            ob, name, ref, how, extra = (list(st) + [{}])[:5]
            extra = extra or {}
            rec = {"n": n, "name": name, "ref": ref}
            p = by_name[ob] if ob else None
            region = p and "region" in p["types"] and "settlement" not in p["types"]
            lonlat = extra.get("at") or ((p["lon"], p["lat"]) if p and not region else None)
            if p:
                rec.update({"site": p["modern"] or "", "s": p["score"], "id": p["id"] + "/" + p["slug"]})
            elif lonlat:
                rec.update({"site": extra.get("site", ""), "s": 300})
            if lonlat and sheet.west <= lonlat[0] <= sheet.east and sheet.south <= lonlat[1] <= sheet.north:
                x, y = sheet.xy(*lonlat)
                sure = extra.get("sure", 1 if p and p["score"] >= 500 and p["exact"] else 0)
                if p and "island" in p["types"] and "settlement" not in p["types"]:
                    sure = extra.get("sure", 1 if p["score"] >= 500 else 0)
                rec.update({"x": round(x, 2), "y": round(y, 2), "sure": sure})
                rec["_ll"], rec["_island"] = lonlat, bool(p and "settlement" not in p["types"])
            else:
                rec["why"] = extra.get("why", "Not plotted: the text names a region, not a place in it.")
            rec["_how"], rec["_extra"] = how, extra
            for k in ("what", "note"):
                if extra.get(k):
                    rec[k] = extra[k]
            stops.append(rec)
        # The lines: from each plotted stop to the next, by land or by sea, through the places
        # the way passed.
        legs, plotted = [], [s for s in stops if "x" in s]
        for a, b in zip(plotted, plotted[1:]):
            ex = b["_extra"]
            way = [(a["_ll"], None)]
            for v in ex.get("via", []):
                v, how = (v["p"], v["how"]) if isinstance(v, dict) else (v, b["_how"])
                way.append(((by_name[v]["lon"], by_name[v]["lat"]) if isinstance(v, str) else v, how))
            way.append((b["_ll"], b["_how"]))
            parts = []
            for k, ((u, _), (v, how)) in enumerate(zip(way, way[1:])):
                sea = how == "sea"
                ends = (not (sea and k == 0 and a["_island"]), not (sea and k == len(way) - 2 and b["_island"]))
                seg = easiest_way(sheet, water_grid if sea else land_grid, u, v, ends, straight=sea)
                parts.append(seg if not parts else seg[1:])
            line = np.vstack(parts)
            skipped = any("x" not in s for s in stops[a["n"]:b["n"] - 1])
            sure = a["sure"] and b["sure"] and not ex.get("guess") and not skipped
            legs.append({"d": path_d([line / res], res, 1), "sure": 1 if sure else 0})
        # A stop at a place visited before shares its marker. "The same place" is within 2 km on a
        # map of a land, and within a few tens of metres on the plan of a city.
        near = min(2.0, sheet.res * 15)
        seen = {}
        for c in stops:
            if "x" not in c:
                continue
            key = (round(c["x"] / near), round(c["y"] / near))
            if key in seen:
                first = seen[key]
                first["also"] = first.get("also", []) + [c["n"]]
                for k in ("x", "y", "sure"):
                    c.pop(k)
                c["why"] = f"Shown with {spec.get('unit', 'stop').lower()} {first['n']}, the same place."
            else:
                seen[key] = c
        for c in stops:
            for k in ("_ll", "_island", "_how", "_extra"):
                c.pop(k, None)
        for pl in places_out:
            for c in stops:
                if "x" in c and math.hypot(pl["x"] - c["x"], pl["y"] - c["y"]) < near:
                    pl.setdefault("st", []).append([j, c["n"]])
        out.append({k: spec[k] for k in ("name", "short", "ref", "color", "unit", "note", "summary") if k in spec}
                   | {"stops": stops, "legs": legs})
    return out


def region_labels(sheet, by_name, ours, names, books=None):
    """Names of districts and islands, set in italic capitals at OpenBible's point for each, as
    the first verse in `books` that names them spells them."""
    out = []
    for n in names:
        text = None
        if isinstance(n, tuple):
            n, text = n
        p = by_name[n]
        x, y = sheet.xy(p["lon"], p["lat"])
        out.append({"n": text or verse_name(p, ours, books=books), "x": round(x, 2), "y": round(y, 2)})
    return out


def furniture_height(block):
    """The title block's height follows its last line."""
    block["box"]["h"] = round((block["lines"][-1][2] + 4.5) * block["scale"], 1)
    return block


# --- Map No. 3: The Roman Empire and the travels of Paul --------------------------------------

SHEET3 = (12.0, 37.0, 29.0, 43.0)
ACTS_ON = {"Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim",
           "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"}
# Provinces about AD 50, each grown from its towns: OpenBible places and, where the Bible names
# none, a few well-known cities (lon, lat). Tint, towns, reach in km.
PROVINCES = {
    "Italy": ("yellow", ["Rome", "Puteoli", "Three Taverns", "Forum of Appius", "Rhegium"],
              [(16.87, 41.12), (17.94, 40.63), (15.80, 40.64), (16.25, 39.30), (14.25, 40.85), (13.40, 42.35)], 160),
    "Sicily": ("lime", ["Syracuse", "Malta"], [(13.36, 38.12), (15.55, 38.19), (12.50, 37.80), (14.25, 37.50)], 160),
    "Macedonia": ("lime", ["Philippi", "Thessalonica", "Berea", "Amphipolis", "Apollonia", "Neapolis"],
                  [(21.0, 40.6), (20.0, 41.0), (19.45, 41.32), (21.4, 41.3), (22.42, 39.64)], 150),
    "Achaia": ("salmon", ["Corinth", "Athens", "Cenchreae", "Nicopolis"],
               [(22.43, 37.07), (21.73, 38.25), (21.68, 37.64), (22.95, 38.40), (23.60, 38.46)], 150),
    "Thrace": ("olive", ["Samothrace"], [(26.55, 41.68), (24.75, 42.15), (28.98, 41.01), (27.96, 40.98), (25.9, 41.1)], 150),
    "Dalmatia": ("sage", [], [(18.10, 42.65), (19.26, 42.44), (17.5, 43.0)], 120),
    "Asia": ("yellow", ["Ephesus", "Smyrna", "Pergamum", "Sardis", "Thyatira", "Philadelphia", "Laodicea",
                        "Colossae", "Hierapolis", "Troas", "Assos", "Miletus", "Mitylene", "Chios", "Samos", "Cos",
                        "Rhodes 1", "Adramyttium", "Cnidus"], [(30.17, 38.07), (28.6, 39.4)], 150),
    "Bithynia and Pontus": ("sage", [], [(29.72, 40.43), (29.92, 40.77), (31.60, 41.25), (35.15, 42.02),
                                         (36.33, 41.29), (33.8, 41.6)], 160),
    "Galatia": ("salmon", ["Antioch 2", "Iconium", "Lystra", "Derbe"],
                [(32.86, 39.94), (34.0, 39.3), (33.6, 40.6), (35.8, 40.6), (31.5, 38.9)], 200),
    "Lycia and Pamphylia": ("lime", ["Perga", "Attalia", "Patara", "Myra"], [(29.8, 36.6), (31.6, 36.8), (30.3, 37.2)], 90),
    "Cilicia": ("sage", ["Tarsus"], [(35.32, 36.98), (35.55, 36.96), (33.93, 36.38), (33.2, 36.2), (36.15, 36.9)], 90),
    "Cappadocia": ("olive", [], [(35.49, 38.72), (34.6, 37.84), (36.5, 39.0), (34.2, 38.6)], 170),
    "Syria": ("yellow", ["Antioch 1", "Seleucia", "Damascus", "Sidon", "Tyre", "Ptolemais"],
              [(36.4, 35.1), (36.72, 34.73), (35.85, 34.43), (35.5, 33.9), (36.0, 35.6)], 140),
    "Judea": ("salmon", ["Jerusalem", "Caesarea", "Joppa", "Lod", "Gaza"], [(35.45, 32.75), (35.3, 32.25)], 80),
    "Arabia": ("olive", [], [(35.44, 30.33), (36.48, 32.52), (35.7, 31.2), (36.3, 31.0)], 140),
    "Egypt": ("yellow", ["Alexandria"], [], 40),
    "Cyprus": ("sage", ["Salamis", "Paphos"], [(33.0, 35.1)], 150),
    "Crete": ("salmon", ["Fair Havens", "Phoenix"], [(23.6, 35.4), (25.9, 35.2), (25.13, 35.33)], 150),
    "Cyrene": ("salmon", ["Cyrene"], [(20.07, 32.12), (22.64, 32.76), (21.0, 32.5)], 110),
    "Africa": ("olive", [], [(13.18, 32.90), (14.29, 32.64), (12.47, 32.79)], 100),
}
# The kingdom of the Nabataeans, and the provinces that were joined under one governor.
PROVINCE_GROUPS = {"Crete": "Crete and Cyrene", "Cyrene": "Crete and Cyrene"}
DISTRICTS = ["Mysia", "Phrygia", "Pisidia", "Lycaonia", "Pamphylia", "Lycia", "Pontus", "Bithynia",
             "Phoenicia", "Illyricum", ("Galilee 1", "GALILEE"), "Samaria 2"]
ISLANDS3 = [("Cyprus", "CYPRUS"), ("Crete", "CRETE"), ("Malta", "MALTA")]
SEAS3 = [("MEDITERRANEAN SEA", [(16.6, 33.4), (24.6, 33.2)], None), ("ADRIATIC SEA", [(18.0, 36.6), (20.4, 37.9)], 30),
         ("AEGEAN SEA", [(24.6, 39.4), (25.2, 37.6)], 30), ("BLACK SEA", [(31.0, 42.55), (34.6, 42.45)], 30),
         ("Sea of Cilicia", [(32.2, 35.85), (34.2, 36.25)], 20)]
RIVERS3 = {"Tiber": (12.48, 42.25, 120), "Orontes": (36.45, 35.45, 160), "Halys": (34.2, 40.95, 220),
           "Sangarius": (30.45, 40.3, 180), "Maeander": (28.2, 37.75, 140), "Hermus": (27.9, 38.62, 140),
           "Axius": (22.45, 41.15, 150), "Strymon": (23.45, 41.25, 120), "Nile": (31.15, 30.4, 200)}
# Paul's journeys, stop by stop, each named in the verse given.
PAUL = [
    {"name": "Paul's early years", "short": "Early years", "ref": "Acts 9–11; Galatians 1", "color": "brown", "unit": "Stop",
     "note": "From Jerusalem to Damascus, where Paul met the risen Jesus; then Arabia, Jerusalem, Tarsus and Antioch.",
     "stops": [
         ("Jerusalem", "Jerusalem", "Acts 9:2", None, {"what": "Paul asks for letters against the followers of the Way"}),
         ("Damascus", "Damascus", "Acts 9:3", "land", {"what": "Jesus appears to him on the road"}),
         ("Arabia 2", "Arabia", "Galatians 1:17", "land", {"why": "Not plotted: Paul names only the region, the Nabataean kingdom of Arabia."}),
         ("Damascus", "Damascus", "Galatians 1:17", "land", {"what": "He returns, and escapes over the wall (Acts 9:25)"}),
         ("Jerusalem", "Jerusalem", "Acts 9:26", "land", {"what": "Barnabas brings him to the apostles"}),
         ("Caesarea", "Caesarea", "Acts 9:30", "land"),
         ("Tarsus", "Tarsus", "Acts 9:30", "sea", {"what": "His home city"}),
         ("Antioch 1", "Antioch", "Acts 11:26", "land", {"what": "The disciples are first called Christians"}),
     ]},
    {"name": "Paul's first journey", "short": "First journey", "ref": "Acts 13–14", "color": "red", "unit": "Stop",
     "note": "With Barnabas, sent out by the church at Antioch: across Cyprus and into the hill country of Galatia, and back.",
     "stops": [
         ("Antioch 1", "Antioch", "Acts 13:1", None, {"what": "The church sends Barnabas and Saul"}),
         ("Seleucia", "Seleucia", "Acts 13:4", "land"),
         ("Salamis", "Salamis", "Acts 13:5", "sea"),
         ("Paphos", "Paphos", "Acts 13:6", "land", {"what": "The proconsul Sergius Paulus believes"}),
         ("Perga", "Perga", "Acts 13:13", "sea", {"what": "John Mark leaves them"}),
         ("Antioch 2", "Antioch", "Acts 13:14", "land", {"what": "Paul speaks in the synagogue"}),
         ("Iconium", "Iconium", "Acts 13:51", "land"),
         ("Lystra", "Lystra", "Acts 14:6", "land", {"what": "A lame man is healed; Paul is stoned"}),
         ("Derbe", "Derbe", "Acts 14:20", "land"),
         ("Lystra", "Lystra", "Acts 14:21", "land"),
         ("Iconium", "Iconium", "Acts 14:21", "land"),
         ("Antioch 2", "Antioch", "Acts 14:21", "land"),
         ("Perga", "Perga", "Acts 14:25", "land"),
         ("Attalia", "Attalia", "Acts 14:25", "land"),
         ("Antioch 1", "Antioch", "Acts 14:26", "sea"),
     ]},
    {"name": "Paul's second journey", "short": "Second journey", "ref": "Acts 15:36–18:22", "color": "blue", "unit": "Stop",
     "note": "With Silas, and Timothy from Lystra: through Galatia to Troas, then across to Macedonia and Achaia.",
     "stops": [
         ("Antioch 1", "Antioch", "Acts 15:35", None),
         ("Derbe", "Derbe", "Acts 16:1", "land", {"via": [(36.6, 36.85), "Tarsus", (34.85, 37.30)]}),
         ("Lystra", "Lystra", "Acts 16:1", "land", {"what": "Timothy joins them"}),
         ("Troas", "Troas", "Acts 16:8", "land", {"via": ["Iconium", "Antioch 2", (30.53, 39.78)], "guess": True,
                                                  "what": "Paul's vision of a man of Macedonia"}),
         ("Samothrace", "Samothrace", "Acts 16:11", "sea"),
         ("Neapolis", "Neapolis", "Acts 16:11", "sea"),
         ("Philippi", "Philippi", "Acts 16:12", "land", {"what": "Lydia; prison and the earthquake"}),
         ("Amphipolis", "Amphipolis", "Acts 17:1", "land"),
         ("Apollonia", "Apollonia", "Acts 17:1", "land"),
         ("Thessalonica", "Thessalonica", "Acts 17:1", "land"),
         ("Berea", "Berea", "Acts 17:10", "land"),
         ("Athens", "Athens", "Acts 17:15", "sea", {"via": [(22.62, 40.40)], "what": "Paul speaks at the Areopagus"}),
         ("Corinth", "Corinth", "Acts 18:1", "land", {"what": "Eighteen months with Aquila and Priscilla"}),
         ("Cenchreae", "Cenchreae", "Acts 18:18", "land"),
         ("Ephesus", "Ephesus", "Acts 18:19", "sea"),
         ("Caesarea", "Caesarea", "Acts 18:22", "sea"),
         ("Antioch 1", "Antioch", "Acts 18:22", "land"),
     ]},
    {"name": "Paul's third journey", "short": "Third journey", "ref": "Acts 18:23–21:17", "color": "green", "unit": "Stop",
     "note": "Through Galatia and Phrygia to Ephesus for three years, to Macedonia and Greece, and by sea to Jerusalem.",
     "stops": [
         ("Antioch 1", "Antioch", "Acts 18:22", None),
         ("Ephesus", "Ephesus", "Acts 19:1", "land", {"via": [(36.6, 36.85), "Tarsus", (34.85, 37.30), "Derbe", "Lystra",
                                                              "Iconium", "Antioch 2"], "guess": True,
                                                      "what": "Two years in the lecture hall of Tyrannus; the riot"}),
         ("Macedonia", "Macedonia", "Acts 20:1", "sea", {"why": "Not plotted: the text names only the province."}),
         ("Corinth", "Greece", "Acts 20:2", "land", {"via": ["Troas", {"p": "Neapolis", "how": "sea"}, "Philippi",
                                                             "Amphipolis", "Thessalonica", "Berea"],
                                                    "sure": 0, "guess": True,
                                                    "note": "Acts names only Greece. Paul probably stayed at Corinth, where he wrote "
                                                            "Romans (Romans 16:1, 23)."}),
         ("Philippi", "Philippi", "Acts 20:6", "land", {"via": ["Berea", "Thessalonica", "Amphipolis"], "guess": True}),
         ("Troas", "Troas", "Acts 20:6", "sea", {"what": "Eutychus falls from the window"}),
         ("Assos", "Assos", "Acts 20:13", "land", {"what": "Paul goes on foot; the others sail"}),
         ("Mitylene", "Mitylene", "Acts 20:14", "sea"),
         ("Chios", "Chios", "Acts 20:15", "sea"),
         ("Samos", "Samos", "Acts 20:15", "sea"),
         ("Miletus", "Miletus", "Acts 20:15", "sea", {"what": "Farewell to the elders of Ephesus"}),
         ("Cos", "Cos", "Acts 21:1", "sea"),
         ("Rhodes 1", "Rhodes", "Acts 21:1", "sea"),
         ("Patara", "Patara", "Acts 21:1", "sea"),
         ("Tyre", "Tyre", "Acts 21:3", "sea", {"via": [(32.5, 34.3)]}),
         ("Ptolemais", "Ptolemais", "Acts 21:7", "sea"),
         ("Caesarea", "Caesarea", "Acts 21:8", "sea", {"what": "Agabus warns Paul"}),
         ("Jerusalem", "Jerusalem", "Acts 21:15", "land", {"what": "Paul is arrested in the temple"}),
     ]},
    {"name": "Paul's voyage to Rome", "short": "To Rome", "ref": "Acts 27–28", "color": "violet", "unit": "Stop",
     "note": "A prisoner, under the centurion Julius: by ship to Crete, the storm and the wreck on Malta, and on to Rome.",
     "stops": [
         ("Caesarea", "Caesarea", "Acts 25:4", None, {"what": "Two years in custody; Paul appeals to Caesar"}),
         ("Sidon", "Sidon", "Acts 27:3", "sea"),
         ("Myra", "Myra", "Acts 27:5", "sea", {"via": [(34.75, 35.75), (33.0, 36.05)], "what": "They change to a ship of Alexandria"}),
         ("Cnidus", "Cnidus", "Acts 27:7", "sea"),
         ("Salmone", "Salmone", "Acts 27:7", "sea"),
         ("Fair Havens", "Fair Havens", "Acts 27:8", "sea"),
         ("Cauda", "Cauda", "Acts 27:16", "sea", {"via": [(24.4, 34.95)], "what": "The storm drives them past"}),
         ("Malta", "Malta", "Acts 28:1", "sea", {"what": "Shipwreck; three months on the island"}),
         ("Syracuse", "Syracuse", "Acts 28:12", "sea"),
         ("Rhegium", "Rhegium", "Acts 28:13", "sea"),
         ("Puteoli", "Puteoli", "Acts 28:13", "sea"),
         ("Forum of Appius", "Forum of Appius", "Acts 28:15", "land"),
         ("Three Taverns", "Three Taverns", "Acts 28:15", "land"),
         ("Rome", "Rome", "Acts 28:16", "land", {"what": "Two years in a rented house"}),
     ]},
]


def roman_map():
    """Map No. 3, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET3, res=1.5)
    sheet.elev = elev = elevation(sheet, 7)
    sea = sea_mask(sheet, elev, [(18.0, 34.0), (25.0, 38.5), (33.0, 42.8), (32.55, 29.9), (14.0, 40.0)])
    lakes = ne_lakes(sheet) | ndimage.binary_fill_holes(_component(elev <= -392, sheet, 35.50, 31.50))
    lakes &= ~sea
    wet = sea | lakes
    land = ~sea
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    res = sheet.res
    lon_g, lat_g = sheet.cell_centres()
    # Rivers are traced from the drainage, except in the deserts, where it finds dry wadis.
    flow = drainage(sheet, elev, wet, 2)
    desert = (lat_g < 33.0) & ~((lon_g > 35.0) & (lon_g < 36.7) & (lat_g > 31.0))
    nile_km = nile(sheet)

    seeds3 = []
    for n, (_, towns, extra, _) in PROVINCES.items():
        seeds3 += [(t, n, by_name[t]["lon"], by_name[t]["lat"]) for t in towns]
        seeds3 += [(n, n, lon, lat) for lon, lat in extra]
    for line in nile_km:
        for x, y in line[::6]:
            lon, lat = sheet.lonlat(x, y)
            seeds3.append(("Nile", "Egypt", lon, lat))
    names3 = list(PROVINCES)
    terr, _ = territories(sheet, elev, wet, flow + (2,), seeds3, step=2, cap_km={n: v[3] for n, v in PROVINCES.items()},
                          names=names3, barrier=None, keep_seeded=True)
    terr = give_islands(terr, land & ~lakes, max_cells=int(4000 / res ** 2))
    groups = {n: PROVINCE_GROUPS.get(n, n) for n in names3}
    tints = {groups[n]: v[0] for n, v in PROVINCES.items()}

    layers, river_km = terrain_layers(sheet, land, lakes, flow, wet, 2500, 7.0, desert,
                                      ripple_km=(2.6, 6, 10.5, 16, 23, 31), river_classes=(8000, 40000), min_slope=2.2)
    layers["nile"] = path_d([ln / res for ln in nile_km], res, 1)
    fills, labels, layers["borders"] = territory_layers(sheet, terr, names3, groups, tints)
    for lb in labels:                    # provinces are named in full, joined provinces apart
        lb["style"] = "nation"
    for text, pts, size in SEAS3:
        labels.append({"text": text, "style": "sea", "pts": line_km(sheet, pts, 2), **({"size": size} if size else {})})

    pl = place_records(sheet, all_places, ACTS_ON, ours, terr, names3)
    land_grid = cost_grid(sheet, wet, step=2, slope_weight=8.0)
    journeys = build_journeys(sheet, PAUL, by_name, land_grid, sea_grid(sheet, sea), pl)

    feats = {"mountains": [], "rivers": [], "waters": [], "regions": region_labels(sheet, by_name, ours, DISTRICTS + ISLANDS3, ACTS_ON)}
    for n, (lon, lat, length) in RIVERS3.items():
        line = follow(nile_km if n == "Nile" else river_km, lon, lat, sheet, length, reach_km=30)
        if line:
            feats["rivers"].append({"n": n, "pts": line})
    x, y = sheet.xy(35.45, 31.45)
    feats["waters"].append({"n": "Dead Sea", "x": round(x, 2), "y": round(y, 2), "lake": 1})

    key_rows = [["camp", "Stop on a journey"], ["camp-unsure", "Stop, place uncertain (?)"]]
    key_rows += [["journey", f"{J['short']} ({J['ref'].split(';')[0]})", J["color"]] for J in journeys]
    key_rows += [["conjectural", "Way uncertain"], ["gap", ""], ["dot", "Town"], ["unsure", "Site uncertain (?)"],
                 ["river", "River"], ["nation", "Border of a province"], ["gap", ""]]
    by_tint = {}
    for n, v in PROVINCES.items():
        by_tint.setdefault(v[0], []).append(n)
    for tint in ("yellow", "salmon", "lime", "sage", "olive"):
        row = []
        for n in by_tint[tint]:
            if row and len(", ".join(row + [n])) > 34:
                key_rows.append(["swatch", ", ".join(row), tint])
                row = []
            row.append(n)
        key_rows.append(["swatch", ", ".join(row), tint])
    data = {
        "sheet": sheet_info(sheet), "grid": 1, "focus": 0.6, "file": "map-03-the-roman-empire",
        "layers": layers, "territories": fills, "labels": labels,
        "places": pl, "features": feats, "territoryLabel": "Province", "journeys": journeys,
        "routeButton": "Journeys", "routesTitle": "The journeys of Paul",
        "routesNote": "Choose a journey to follow it stop by stop. Each stop is named in the verse given.",
        "routeLayer": "Paul's journeys",
        "title": furniture_height({"box": {"x": 1255, "y": 1095, "w": 640}, "scale": 4.3, "lines": [
            ["series", "MAP No. 3 · A STYLE STUDY", 7.5], ["head", "THE ROMAN EMPIRE", 15.5],
            ["display-fit", "THE TRAVELS OF PAUL", 26.5],
            ["italic", "His journeys in the Acts of the Apostles, with the places", 32.5],
            ["italic", "named in Acts and the letters, and the provinces about AD 50", 36.4], ["rule", "", 39.6],
            ["plain", "About AD 35 to 62 by modern reckoning", 44.5],
            ["credit", "After the Eilers Sunday School Maps, St. Louis · Drawn from open data · CC BY 4.0", 49]]}),
        "key": {"box": {"x": 22, "y": 1018, "w": 330}, "scale": 5.4, "scale_bars": [[0, 50, 100, 150], [0, 100, 200]],
                "rows": key_rows},
    }
    page = {
        "slug": "roman-empire", "NO": "3", "H1": "The Roman Empire and the Travels of Paul", "TITLE": "Travels of Paul Map",
        "DESCRIPTION": "Map No. 3, a style study after the Eilers Sunday School wall maps: the Roman Empire about AD 50 "
                       "and Paul's journeys in Acts, stop by stop, drawn from open data.",
        "GRID_LABEL": "One-degree squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, after <strong>Eilers Sunday School Map No. "
            "3</strong>, <em>Roman Empire and the Routes of the Travels of St. Paul</em> (A. H. Eilers &amp; Co., St. "
            "Louis), redrawn from open data.",
            ["Flat tints for each province, with the seas left as paper", KEPT[1],
             "Each journey in its own color, with the stops numbered", KEPT[3], KEPT[4]], CHANGED + [
                "Choose a journey to follow it stop by stop, with the verse for each stop"],
            ["<strong>Land, water and relief</strong> come from elevation data; rivers are traced from it, and the "
             "Nile and the lakes come from Natural Earth.",
             "<strong>The journeys</strong> follow Acts and Galatians. Every stop is named in the verse given, and "
             "the build checks each name against this project's translation. Sea passages keep to open water and "
             "land journeys to the easiest ground; both are pictures of the order of places, not of the exact way. "
             "Where Acts names only a region, the way through it is dashed.",
             "<strong>Provinces are approximate</strong>, grown from their towns. Boundaries changed often in these "
             "years; the map shows them about AD 50.",
             PLACES_MADE.format(books="Acts to Revelation"), NAMES_MADE],
            SOURCES + ["Rivers and lakes: Natural Earth (public domain)"]),
    }
    return data, page


def ne_rivers(sheet, skip=()):
    """Rivers from Natural Earth on the sheet, as (polyline in km, name, scale rank); a lower
    rank is a larger river. Modern canals are left out."""
    out = []
    for ft in natural_earth("rivers_lake_centerlines"):
        pr = ft["properties"]
        name = pr.get("name") or ""
        if name in skip or "Canal" in name:
            continue
        g = ft["geometry"]
        for part in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            pts = np.array([sheet.xy(lon, lat) for lon, lat in part])
            keep = (pts[:, 0] > -20) & (pts[:, 0] < sheet.width + 20) & (pts[:, 1] > -20) & (pts[:, 1] < sheet.height + 20)
            if keep.sum() > 1:
                out.append((chaikin(pts[keep], 2), name, pr.get("scalerank", 9)))
    return out


def ne_river_layers(sheet, lines, classes=(4, 7)):
    """River widths by Natural Earth rank: the great rivers widest."""
    res = sheet.res
    a, b = classes
    return [path_d([p / res for p, _, r in lines if lo <= r < hi], res, 1) for lo, hi in ((b, 99), (a, b), (0, a))]


# --- Map No. 4: Western Asia, the lands of the Old Testament ---------------------------------

SHEET4 = (28.0, 56.0, 24.0, 42.0)
# Lands of the Old Testament, each grown from its towns: tint, towns (OpenBible), other points,
# reach in km, and the group it belongs to.
LANDS4 = {
    "Egypt": ("yellow", ["Memphis", "Zoan", "Heliopolis"], [], 30),
    "Canaan": ("lime", ["Shechem", "Hebron", "Bethel 1", "Beersheba 1", "Jerusalem", "Dan", "Gaza", "Sidon", "Tyre"], [], 70),
    "Edom": ("olive", ["Bozrah 1", "Sela 1", "Mount Seir 1"], [], 45),
    "Moab": ("olive", ["Kir-hareseth", "Dibon 1"], [], 30),
    "Aram": ("sage", ["Damascus", "Hamath 1", "Tadmor", "Riblah 1"], [(37.10, 36.48), (36.9, 34.3)], 160),
    "Paddan-aram": ("salmon", ["Haran", "Gozan", "Carchemish"], [(39.5, 36.4), (38.6, 37.2)], 170),
    "Assyria": ("olive", ["Nineveh", "Calah", "Asshur"], [(44.01, 36.19), (43.0, 37.0), (42.7, 36.4)], 140),
    "Babylonia": ("yellow", ["Babylon 1", "Ur 2", "Erech", "Accad"], [(45.20, 32.13), (44.0, 33.3), (46.5, 31.0)], 150),
    "Elam": ("lime", ["Susa"], [(48.0, 31.5), (49.5, 32.5), (48.8, 31.0)], 160),
    "Media": ("sage", ["Ecbatana"], [(51.43, 35.60), (47.0, 35.0), (47.5, 36.8), (49.5, 36.5), (52.5, 36.0)], 260),
    "Persia": ("salmon", [], [(52.89, 29.93), (53.17, 30.19), (51.5, 30.5), (54.5, 29.0), (52.0, 28.5)], 260),
    "Ararat": ("yellow", ["Ararat"], [(43.33, 38.50), (41.27, 39.90), (43.0, 39.3), (45.0, 40.2)], 200),
    "Hittites": ("olive", [], [(34.62, 40.02), (35.63, 38.85), (33.0, 39.0), (36.5, 39.5), (31.5, 38.5), (37.5, 38.2)], 250),
    "Arabia": ("blush", ["Tema", "Dedan"], [(39.87, 29.81), (42.0, 27.5), (45.0, 26.0), (37.5, 28.0)], 300),
}
LAND_GROUPS4 = {"Edom": "Edom and Moab", "Moab": "Edom and Moab"}
EGYPT_STOP = {"at": (31.60, 30.65), "site": "Egypt (Genesis names no city)", "sure": 0}
PATRIARCHS = [
    {"name": "Abraham", "short": "Abraham", "ref": "Genesis 11–23", "color": "red", "unit": "Stop",
     "note": "From Ur of the Chaldeans to Haran with Terah, then into Canaan, down to Egypt and back, living in tents "
             "from Shechem to Beersheba.",
     "stops": [
         ("Ur 2", "Ur", "Genesis 11:31", None, {"what": "Terah sets out with Abram, Sarai and Lot"}),
         ("Haran", "Haran", "Genesis 11:31", "land", {"what": "Terah dies; God calls Abram (Genesis 12:1)", "guess": True,
                                                       "via": [(45.20, 32.15), (44.30, 32.95), (42.95, 34.10), (41.90, 34.45),
                                                               (40.90, 34.55), (40.10, 35.30), (39.00, 35.95)],
                                                       "note": "Up the Euphrates, the caravan road; Genesis gives no way."}),
         ("Shechem", "Shechem", "Genesis 12:6", "land", {"what": "The oak of Moreh; the promise of the land"}),
         ("Bethel 1", "Bethel", "Genesis 12:8", "land"),
         ("Negeb", "The Negev", "Genesis 12:9", "land", {"word": "Negev", "why": "Not plotted: a region, the dry south of Canaan."}),
         (None, "Egypt", "Genesis 12:10", "land", EGYPT_STOP | {"what": "Abram goes down in a famine"}),
         ("Bethel 1", "Bethel", "Genesis 13:3", "land", {"what": "Abram and Lot part"}),
         ("Hebron", "Hebron", "Genesis 13:18", "land", {"what": "The oaks of Mamre"}),
         ("Dan", "Dan", "Genesis 14:14", "land", {"what": "Abram pursues the kings to rescue Lot"}),
         ("Hobah", "Hobah", "Genesis 14:15", "land"),
         ("Salem", "Salem", "Genesis 14:18", "land", {"what": "Melchizedek blesses Abram"}),
         ("Gerar", "Gerar", "Genesis 20:1", "land"),
         ("Beersheba 1", "Beersheba", "Genesis 21:31", "land", {"what": "The oath with Abimelech"}),
         ("Moriah", "Land of Moriah", "Genesis 22:2", "land", {"word": "Moriah", "at": (35.2356, 31.7778), "sure": 0,
                                                               "site": "Jerusalem (2 Chronicles 3:1)",
                                                               "what": "Abraham offers Isaac",
                                                               "note": "2 Chronicles 3:1 places Mount Moriah at Jerusalem."}),
         ("Beersheba 1", "Beersheba", "Genesis 22:19", "land"),
         ("Hebron", "Hebron", "Genesis 23:2", "land", {"what": "Sarah dies; the cave of Machpelah"}),
     ]},
    {"name": "Jacob", "short": "Jacob", "ref": "Genesis 28–46", "color": "blue", "unit": "Stop",
     "note": "Jacob flees from Esau to Laban at Haran, returns with his family twenty years later, and at last goes "
             "down with all Israel to Egypt.",
     "stops": [
         ("Beersheba 1", "Beersheba", "Genesis 28:10", None),
         ("Bethel 1", "Bethel", "Genesis 28:19", "land", {"what": "The ladder to heaven"}),
         ("Haran", "Haran", "Genesis 29:4", "land", {"what": "Twenty years with Laban; Leah and Rachel"}),
         ("Mizpah 4", "Mizpah", "Genesis 31:49", "land", {"what": "The covenant with Laban"}),
         ("Mahanaim", "Mahanaim", "Genesis 32:3", "land", {"what": "The angels of God meet him"}),
         ("Penuel", "Peniel", "Genesis 32:31", "land", {"what": "Jacob wrestles with God and is named Israel"}),
         ("Succoth 1", "Succoth", "Genesis 33:17", "land"),
         ("Shechem", "Shechem", "Genesis 33:18", "land"),
         ("Bethel 1", "Bethel", "Genesis 35:6", "land"),
         ("Ephrath", "Ephrath", "Genesis 35:19", "land", {"what": "Rachel dies; Benjamin is born"}),
         ("Hebron", "Hebron", "Genesis 35:27", "land", {"what": "Isaac dies"}),
         ("Beersheba 1", "Beersheba", "Genesis 46:1", "land"),
         ("Goshen 1", "Goshen", "Genesis 46:28", "land", {"at": (31.834, 30.799), "sure": 0, "site": "the Wadi Tumilat (traditional)",
                                                          "what": "Jacob meets Joseph"}),
     ]},
    {"name": "Joseph", "short": "Joseph", "ref": "Genesis 37", "color": "green", "unit": "Stop",
     "note": "Sent by Jacob to find his brothers, Joseph is sold to traders and taken down to Egypt.",
     "stops": [
         ("Hebron", "Hebron", "Genesis 37:14", None, {"what": "Jacob sends Joseph"}),
         ("Shechem", "Shechem", "Genesis 37:14", "land"),
         ("Dothan", "Dothan", "Genesis 37:17", "land", {"what": "Sold to traders for twenty pieces of silver"}),
         (None, "Egypt", "Genesis 37:36", "land", EGYPT_STOP | {"what": "Sold to Potiphar"}),
     ]},
]


def western_asia_map():
    """Map No. 4, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET4, res=2.0)
    sheet.elev = elev = elevation(sheet, 6)
    sea = sea_mask(sheet, elev, [(32.0, 33.5), (31.5, 41.8), (37.5, 41.5), (36.0, 25.0), (51.0, 27.0), (34.6, 28.8)])
    sea |= _component(elev <= -27, sheet, 51.0, 40.0)          # the Caspian, at its old level
    lakes = ne_lakes(sheet, skip=("Lake Razazah",)) & ~sea
    lakes |= ndimage.binary_fill_holes(_component(elev <= -392, sheet, 35.50, 31.50))
    wet = sea | lakes
    land = ~sea
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    res = sheet.res
    flow = drainage(sheet, elev, wet, 2)
    rivers4 = ne_rivers(sheet)
    nile_km = [p for p, n, _ in rivers4 if n in ("Nile", "Rosetta Branch", "Damietta Branch")]

    seeds4 = []
    for n, (_, towns, extra, _) in LANDS4.items():
        seeds4 += [(t, n, by_name[t]["lon"], by_name[t]["lat"]) for t in towns]
        seeds4 += [(n, n, lon, lat) for lon, lat in extra]
    for line in nile_km:
        for x, y in line[::4]:
            lon, lat = sheet.lonlat(x, y)
            if 24 < lat < 31.3:
                seeds4.append(("Nile", "Egypt", lon, lat))
    names4 = list(LANDS4)
    terr, _ = territories(sheet, elev, wet, flow + (2,), seeds4, step=2, cap_km={n: v[3] for n, v in LANDS4.items()},
                          names=names4, barrier=None, keep_seeded=True)
    terr = give_islands(terr, land & ~lakes, max_cells=int(3000 / res ** 2))
    groups = {n: LAND_GROUPS4.get(n, n) for n in names4}
    tints = {groups[n]: v[0] for n, v in LANDS4.items()}

    layers, _ = terrain_layers(sheet, land, lakes, flow, wet, 1e12, 9.0, ripple_km=(3.5, 8, 14, 21, 30, 41), min_slope=1.6)
    layers["rivers"] = ne_river_layers(sheet, rivers4)
    fills, labels, layers["borders"] = territory_layers(sheet, terr, names4, groups, tints)
    for lb in labels:
        lb["style"] = "nation"
    for text, pts, size in [("GREAT SEA", [(29.0, 33.6), (32.6, 33.3)], 34), ("RED SEA", [(36.2, 25.6), (37.9, 24.4)], 30),
                            ("PERSIAN GULF", [(50.0, 28.4), (52.6, 26.8)], 30), ("CASPIAN SEA", [(50.6, 41.5), (51.6, 38.0)], 30),
                            ("BLACK SEA", [(32.5, 42.0), (36.5, 41.8)], 28)]:
        labels.append({"text": text, "style": "redsea" if text == "RED SEA" else "sea", "pts": line_km(sheet, pts, 2), "size": size})

    pl = place_records(sheet, all_places, OT_BOOKS, ours, terr, names4, min_score=300)
    journeys = build_journeys(sheet, PATRIARCHS, by_name, cost_grid(sheet, wet, step=2, slope_weight=8.0),
                              sea_grid(sheet, sea), pl)

    feats = {"mountains": [], "rivers": [], "waters": [],
             "regions": region_labels(sheet, by_name, ours, ["Shinar", "Paddan-aram", "Midian", "Goshen 1", "Chaldea"], OT_BOOKS)}
    for n, lon, lat, length in (("Euphrates", 40.6, 35.0, 260), ("Tigris", 44.6, 33.6, 240), ("Nile", 31.2, 27.5, 260),
                                ("Jordan", 35.57, 32.3, 80), ("Ulai", 48.3, 31.9, 120)):
        line = follow([p for p, *_ in rivers4], lon, lat, sheet, length, reach_km=40)
        if line:
            feats["rivers"].append({"n": n, "pts": line, "main": n in ("Euphrates", "Tigris", "Nile")})
    for name, lon, lat in (("Mt. Ararat", 44.30, 39.70), ("Mt. Sinai (traditional)", 33.97, 28.54), ("Mt. Lebanon", 36.12, 34.30)):
        x, y = sheet.xy(lon, lat)
        feats["mountains"].append({"n": name, "x": round(x, 2), "y": round(y, 2)})

    key_rows = [["camp", "Stop on a journey"], ["camp-unsure", "Stop, place uncertain (?)"]]
    key_rows += [["journey", f"{J['name']} ({J['ref']})", J["color"]] for J in journeys]
    key_rows += [["conjectural", "Way uncertain"], ["gap", ""], ["dot", "Town"], ["unsure", "Site uncertain (?)"],
                 ["mount", "Mountain"], ["river", "River"], ["nation", "Border of a land"], ["gap", ""]]
    by_tint = {}
    for n, v in LANDS4.items():
        by_tint.setdefault(v[0], []).append(n)
    for tint in ("yellow", "salmon", "lime", "sage", "olive", "blush"):
        key_rows.append(["swatch", ", ".join(by_tint[tint]), tint])
    data = {
        "sheet": sheet_info(sheet), "grid": 2, "focus": 0.45, "file": "map-04-western-asia",
        "layers": layers, "territories": fills, "labels": labels,
        "places": pl, "features": feats, "territoryLabel": "Land", "journeys": journeys,
        "routeButton": "Journeys", "routesTitle": "The journeys of the patriarchs",
        "routesNote": "Choose a journey to follow it stop by stop. Each stop is named in the verse given.",
        "routeLayer": "The journeys of Abraham, Jacob and Joseph",
        "title": furniture_height({"box": {"x": 12, "y": 835, "w": 560}, "scale": 4.4, "lines": [
            ["series", "MAP No. 4 · A STYLE STUDY", 7.5], ["display-fit", "WESTERN ASIA", 20],
            ["sub", "THE LANDS OF THE OLD TESTAMENT", 27.5],
            ["italic", "From Egypt to Persia, with the journeys of Abraham, Jacob and Joseph,", 33.5],
            ["italic", "and the places named in the Old Testament whose location is known", 37.4], ["rule", "", 40.6],
            ["plain", "The patriarchs: 1921–1706 BC by Ussher’s chronology,", 45.5],
            ["plain", "about 2000–1700 BC by modern reckoning", 49.5],
            ["credit", "After the Eilers Sunday School Maps, St. Louis · Drawn from open data · CC BY 4.0", 54]]}),
        "key": {"box": {"x": 1100, "y": 1330, "w": 330}, "scale": 5.0, "scale_bars": [[0, 50, 100, 150], [0, 100, 200]],
                "rows": key_rows},
    }
    page = {
        "slug": "western-asia", "NO": "4", "H1": "Western Asia", "TITLE": "Western Asia Map",
        "DESCRIPTION": "Map No. 4, a style study after the Eilers Sunday School wall maps: the lands of the Old Testament "
                       "from Egypt to Persia, with the journeys of Abraham, Jacob and Joseph, drawn from open data.",
        "GRID_LABEL": "Two-degree squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, after <strong>Eilers Sunday School Map No. "
            "4</strong>, <em>Western Asia</em> (A. H. Eilers &amp; Co., St. Louis), redrawn from open data.",
            ["Flat tints for each land, with the seas left as paper", KEPT[1],
             "Each journey in its own color, with the stops numbered", KEPT[3], KEPT[4]], CHANGED,
            ["<strong>Land, water and relief</strong> come from elevation data; the rivers and lakes from Natural "
             "Earth, leaving out modern reservoirs. The Caspian and the Dead Sea are drawn at their old levels.",
             "<strong>The journeys</strong> follow Genesis. Every stop is named in the verse given, and the build "
             "checks each name against this project's translation. Where Genesis names only Egypt, the stop is "
             "placed in the eastern Delta and marked uncertain.",
             "<strong>Lands are approximate</strong>, grown from their towns, and gather peoples of different "
             "centuries onto one sheet, as Eilers did: the Hittites and Paddan-aram of the patriarchs beside the "
             "Media and Persia of the exile.",
             PLACES_MADE.format(books="the Old Testament").replace("Places scored below 500", "Places scored at least "
                                                                    "300 are shown; those below 500"), NAMES_MADE],
            SOURCES + ["Rivers and lakes: Natural Earth (public domain)"]),
    }
    return data, page


# --- Map No. 6: The empires of Assyria, Babylon and Persia ------------------------------------

# Each period's lands, grown from their towns: name: (tint, empire, towns, other points, reach).
# Lands of one empire share a dashed border; a land's own tint marks a province or vassal.
EUPHRATES_ROAD = [(37.15, 36.20), "Carchemish", (38.75, 35.85), (40.10, 35.30), (40.90, 34.55), (41.90, 34.45),
                  (42.95, 34.10), (44.30, 32.95)]
EMPIRES6 = [
    {"name": "Assyria, about 670 BC", "short": "Assyria",
     "note": "Under Esarhaddon, who also held Lower Egypt from 671 BC. Judah under Manasseh paid tribute.",
     "lands": {
         "Assyria": ("olive", "Assyria", ["Nineveh", "Calah", "Asshur", "Babylon 1", "Ur 2", "Erech", "Haran", "Gozan",
                                          "Carchemish", "Damascus", "Hamath 1", "Arpad", "Samaria 1", "Megiddo", "Sidon",
                                          "Riblah 1", "Tadmor"],
                     [(36.2, 36.2), (35.3, 36.9), (39.5, 36.4), (41.0, 35.5), (42.5, 34.5), (44.0, 33.3), (45.5, 32.0)], 200),
         "Judah": ("salmon", "Assyria", ["Jerusalem", "Lachish", "Hebron", "Beersheba 1"], [], 40),
         "Egypt": ("yellow", "Egypt", ["Memphis", "Zoan", "Tahpanhes"], [], 30),
         "Media": ("sage", "Media", ["Ecbatana"], [(51.43, 35.60), (47.0, 35.0), (47.5, 36.8), (49.5, 36.5), (52.5, 36.0)], 260),
         "Elam": ("lime", "Elam", ["Susa"], [(48.0, 31.5), (49.5, 32.5), (48.8, 31.0), (51.5, 30.5), (52.89, 29.93)], 260),
         "Urartu": ("yellow", "Urartu", ["Ararat"], [(43.33, 38.50), (41.27, 39.90), (43.0, 39.3), (45.0, 40.2)], 200),
         "Lydia": ("salmon", "Lydia", ["Sardis"], [(29.0, 38.6), (30.5, 39.0), (31.5, 38.5)], 180),
         "Arabia": ("blush", "Arabia", ["Tema", "Dedan"], [(39.87, 29.81), (42.0, 27.5), (45.0, 26.0), (37.5, 28.0)], 300),
     }},
    {"name": "Babylon, about 570 BC", "short": "Babylon",
     "note": "Under Nebuchadnezzar, after the fall of Nineveh (612 BC) and of Jerusalem (586 BC). The Medes held the "
             "north and east, to the Halys.",
     "lands": {
         "Babylonia": ("yellow", "Babylon", ["Babylon 1", "Ur 2", "Erech", "Asshur", "Haran", "Carchemish", "Riblah 1",
                                             "Hamath 1", "Damascus", "Tyre", "Sidon", "Jerusalem", "Lachish", "Gaza", "Tadmor"],
                       [(41.0, 35.5), (42.5, 34.5), (44.0, 33.3), (45.5, 32.0), (36.2, 36.2), (43.15, 36.0)], 200),
         "Elam": ("lime", "Babylon", ["Susa"], [(48.0, 31.5), (49.5, 32.5), (48.8, 31.0)], 160),
         "Media": ("sage", "Media", ["Ecbatana", "Ararat"], [(51.43, 35.60), (47.0, 35.0), (47.5, 36.8), (49.5, 36.5),
                                                             (43.33, 38.50), (41.27, 39.90), (45.0, 40.2), (37.5, 38.5),
                                                             (35.49, 38.72), (44.0, 37.2)], 300),
         "Persia": ("salmon", "Media", [], [(52.89, 29.93), (53.17, 30.19), (51.5, 30.5), (54.5, 29.0), (52.0, 28.5)], 260),
         "Lydia": ("lime", "Lydia", ["Sardis"], [(29.0, 38.6), (30.5, 39.0), (32.0, 39.5), (33.3, 40.0), (31.5, 38.5)], 200),
         "Cilicia": ("olive", "Cilicia", ["Tarsus"], [(35.3, 37.0), (33.9, 36.4)], 90),
         "Egypt": ("yellow", "Egypt", ["Memphis", "Zoan", "Tahpanhes"], [], 30),
         "Arabia": ("blush", "Arabia", ["Tema", "Dedan"], [(39.87, 29.81), (42.0, 27.5), (45.0, 26.0), (37.5, 28.0)], 300),
     }},
    {"name": "Persia, about 500 BC", "short": "Persia",
     "note": "Under Darius I, whose empire ran from Egypt and Lydia to India (Esther 1:1). Judah was a small province "
             "of the land Beyond the River.",
     "lands": {
         "Persia": ("salmon", "Persia", [], [(52.89, 29.93), (53.17, 30.19), (51.5, 30.5), (54.5, 29.0), (52.0, 28.5)], 260),
         "Elam": ("lime", "Persia", ["Susa"], [(48.0, 31.5), (49.5, 32.5), (48.8, 31.0)], 160),
         "Media": ("sage", "Persia", ["Ecbatana"], [(51.43, 35.60), (47.0, 35.0), (47.5, 36.8), (49.5, 36.5), (52.5, 36.0)], 260),
         "Babylon": ("yellow", "Persia", ["Babylon 1", "Ur 2", "Erech", "Accad"], [(45.20, 32.13), (44.0, 33.3), (46.5, 31.0)], 160),
         "Assyria": ("olive", "Persia", ["Nineveh", "Calah", "Asshur", "Haran", "Gozan", "Carchemish"],
                     [(39.5, 36.4), (41.0, 35.5), (42.7, 36.4)], 160),
         "Beyond the River": ("lime", "Persia", ["Damascus", "Hamath 1", "Riblah 1", "Tadmor", "Tyre", "Sidon", "Samaria 1",
                                                 "Megiddo", "Gaza", "Arpad"], [(36.2, 36.2)], 140),
         "Judah": ("salmon", "Persia", ["Jerusalem", "Bethlehem 1", "Mizpah 3"], [], 22),
         "Egypt": ("yellow", "Persia", ["Memphis", "Zoan", "Tahpanhes"], [], 30),
         "Armenia": ("blush", "Persia", ["Ararat"], [(43.33, 38.50), (41.27, 39.90), (43.0, 39.3), (45.0, 40.2)], 200),
         "Cappadocia": ("yellow", "Persia", [], [(35.49, 38.72), (34.6, 37.84), (36.5, 39.0), (34.2, 38.6), (34.62, 40.02)], 220),
         "Lydia": ("sage", "Persia", ["Sardis"], [(29.0, 38.6), (30.5, 39.0), (31.5, 38.5), (32.0, 39.5)], 200),
         "Cilicia": ("salmon", "Persia", ["Tarsus"], [(35.3, 37.0), (33.9, 36.4)], 90),
         "Arabia": ("blush", "Arabia", ["Tema", "Dedan"], [(39.87, 29.81), (42.0, 27.5), (45.0, 26.0), (37.5, 28.0)], 300),
     }},
]
EXILES = [
    {"name": "Israel taken to Assyria", "short": "Israel exiled", "ref": "2 Kings 17", "color": "brown", "unit": "Place",
     "note": "Samaria fell to Assyria in 722 BC, and its people were settled in the places 2 Kings names. The order of "
             "the places here is the map's.",
     "stops": [
         ("Samaria 1", "Samaria", "2 Kings 17:6", None, {"what": "The city falls after a three-year siege"}),
         ("Gozan", "Gozan, on the Habor", "2 Kings 17:6", "land", {"word": "Gozan", "via": ["Damascus", "Hamath 1", (37.15, 36.20),
                                                                                         "Carchemish"], "guess": True}),
         ("Halah", "Halah", "2 Kings 17:6", "land"),
         ("Media", "Towns of the Medes", "2 Kings 17:6", "land", {"word": "Medes", "why": "Not plotted: the text names no town."}),
     ]},
    {"name": "Jonah", "short": "Jonah", "ref": "Jonah 1–3", "color": "green", "unit": "Place",
     "note": "Sent to Nineveh, Jonah sails for Tarshish instead; after the storm and the fish, he goes to Nineveh.",
     "stops": [
         ("Gath-hepher", "Gath-hepher", "2 Kings 14:25", None, {"what": "Jonah's home"}),
         ("Joppa", "Joppa", "Jonah 1:3", "land", {"what": "He finds a ship going to Tarshish"}),
         ("Tarshish 1", "Tarshish", "Jonah 1:3", "sea", {"why": "Not plotted: Jonah never reached it. Tarshish lay far to the "
                                                                 "west, perhaps in Spain."}),
         ("Nineveh", "Nineveh", "Jonah 3:3", "land", {"via": ["Damascus", "Tadmor"], "guess": True, "what": "Nineveh repents"}),
     ]},
    {"name": "Judah taken to Babylon", "short": "Judah exiled", "ref": "2 Kings 25; Ezekiel 3", "color": "red", "unit": "Place",
     "note": "Nebuchadnezzar took Jerusalem in 586 BC. King Zedekiah was judged at Riblah and taken to Babylon, and the "
             "exiles were settled by the river Chebar.",
     "stops": [
         ("Jerusalem", "Jerusalem", "2 Kings 25:1", None, {"what": "The siege; the temple burned"}),
         ("Riblah 1", "Riblah", "2 Kings 25:6", "land", {"what": "Zedekiah is judged and blinded"}),
         ("Babylon 1", "Babylon", "2 Kings 25:7", "land", {"via": EUPHRATES_ROAD, "guess": True}),
         ("Tel-abib", "Tel-abib", "Ezekiel 3:15", "land", {"what": "Ezekiel among the exiles by the river Chebar"}),
     ]},
    {"name": "Jeremiah taken to Egypt", "short": "Jeremiah", "ref": "Jeremiah 40–43", "color": "violet", "unit": "Place",
     "note": "After the murder of the governor Gedaliah, the people left in Judah fled to Egypt and took Jeremiah with them.",
     "stops": [
         ("Mizpah 3", "Mizpah", "Jeremiah 40:6", None, {"what": "Jeremiah stays with Gedaliah"}),
         ("Geruth Chimham", "Geruth-chimham", "Jeremiah 41:17", "land"),
         ("Tahpanhes", "Tahpanhes", "Jeremiah 43:7", "land", {"what": "Jeremiah's last prophecies"}),
     ]},
    {"name": "Ezra's return", "short": "Ezra", "ref": "Ezra 7–8", "color": "blue", "unit": "Place",
     "note": "Ezra the scribe led a company back from Babylon in 458 BC, by the long road up the Euphrates and down "
             "through Syria.",
     "stops": [
         ("Babylon 1", "Babylon", "Ezra 7:6", None),
         ("Ahava", "Ahava", "Ezra 8:15", "land", {"what": "Fasting and prayer by the river"}),
         ("Jerusalem", "Jerusalem", "Ezra 8:32", "land", {"via": EUPHRATES_ROAD[::-1][:-1] + ["Hamath 1", "Damascus"], "guess": True}),
     ]},
    {"name": "Nehemiah", "short": "Nehemiah", "ref": "Nehemiah 1–2", "color": "black", "unit": "Place",
     "note": "Cupbearer to the king at Susa, Nehemiah went to Jerusalem in 445 BC to rebuild its walls.",
     "stops": [
         ("Susa", "Susa", "Nehemiah 1:1", None, {"what": "News of Jerusalem's broken walls"}),
         ("Jerusalem", "Jerusalem", "Nehemiah 2:11", "land", {"via": ["Babylon 1"] + EUPHRATES_ROAD[::-1][:-1] + ["Hamath 1", "Damascus"],
                                                               "guess": True, "what": "The walls rebuilt in 52 days"}),
     ]},
]


def empires_map():
    """Map No. 6, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET4, res=2.0)
    sheet.elev = elev = elevation(sheet, 6)
    sea = sea_mask(sheet, elev, [(32.0, 33.5), (31.5, 41.8), (37.5, 41.5), (36.0, 25.0), (51.0, 27.0), (34.6, 28.8)])
    sea |= _component(elev <= -27, sheet, 51.0, 40.0)
    lakes = ne_lakes(sheet, skip=("Lake Razazah",)) & ~sea
    lakes |= ndimage.binary_fill_holes(_component(elev <= -392, sheet, 35.50, 31.50))
    wet = sea | lakes
    land = ~sea
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    res = sheet.res
    flow = drainage(sheet, elev, wet, 2)
    rivers6 = ne_rivers(sheet)
    nile_km = [p for p, n, _ in rivers6 if n in ("Nile", "Rosetta Branch", "Damietta Branch")]
    nile_seeds = []
    for line in nile_km:
        for x, y in line[::4]:
            lon, lat = sheet.lonlat(x, y)
            if 24 < lat < 31.3:
                nile_seeds.append(("Nile", "Egypt", lon, lat))

    layers, _ = terrain_layers(sheet, land, lakes, flow, wet, 1e12, 9.0, ripple_km=(3.5, 8, 14, 21, 30, 41), min_slope=1.6)
    layers["rivers"] = ne_river_layers(sheet, rivers6)
    layers["borders"] = {}
    periods = []
    for P in EMPIRES6:
        lands = P["lands"]
        seeds6 = list(nile_seeds)
        for n, (_, _, towns, extra, _) in lands.items():
            seeds6 += [(t, n, by_name[t]["lon"], by_name[t]["lat"]) for t in towns]
            seeds6 += [(n, n, lon, lat) for lon, lat in extra]
        names6 = list(lands)
        terr, _ = territories(sheet, elev, wet, flow + (2,), seeds6, step=2, cap_km={n: v[4] for n, v in lands.items()},
                              names=names6, barrier=None, keep_seeded=True)
        terr = give_islands(terr, land & ~lakes, max_cells=int(3000 / res ** 2))
        groups = {n: v[1] for n, v in lands.items()}
        tints = {n: v[0] for n, v in lands.items()}
        fills, labels, borders = territory_layers(sheet, terr, names6, groups, tints)
        for lb in labels:
            lb["style"] = "nation"
        periods.append({"name": P["name"], "note": P["note"], "territories": fills, "labels": labels, "borders": borders})

    labels = []
    for text, pts, size in [("GREAT SEA", [(29.0, 33.6), (32.6, 33.3)], 34), ("RED SEA", [(36.2, 25.6), (37.9, 24.4)], 30),
                            ("PERSIAN GULF", [(50.0, 28.4), (52.6, 26.8)], 30), ("CASPIAN SEA", [(50.6, 41.5), (51.6, 38.0)], 30),
                            ("BLACK SEA", [(32.5, 42.0), (36.5, 41.8)], 28)]:
        labels.append({"text": text, "style": "redsea" if text == "RED SEA" else "sea", "pts": line_km(sheet, pts, 2), "size": size})

    pl = place_records(sheet, all_places, OT_BOOKS, ours, min_score=300)
    journeys = build_journeys(sheet, EXILES, by_name, cost_grid(sheet, wet, step=2, slope_weight=8.0), sea_grid(sheet, sea), pl)

    feats = {"mountains": [], "rivers": [], "waters": [], "regions": region_labels(sheet, by_name, ours, ["Chaldea"], OT_BOOKS)}
    for n, lon, lat, length in (("Euphrates", 40.6, 35.0, 260), ("Tigris", 44.6, 33.6, 240), ("Nile", 31.2, 27.5, 260),
                                ("Ulai", 48.3, 31.9, 120)):
        line = follow([p for p, *_ in rivers6], lon, lat, sheet, length, reach_km=40)
        if line:
            feats["rivers"].append({"n": n, "pts": line, "main": n in ("Euphrates", "Tigris", "Nile")})
    x, y = sheet.xy(45.23, 32.13)
    feats["waters"].append({"n": "River Chebar", "x": round(x, 2), "y": round(y, 2), "lake": 1})

    key_rows = [["camp", "Place on a journey"], ["camp-unsure", "Place uncertain (?)"]]
    key_rows += [["journey", f"{J['name']} ({J['ref']})", J["color"]] for J in journeys]
    key_rows += [["conjectural", "Way uncertain"], ["gap", ""], ["dot", "Town"], ["unsure", "Site uncertain (?)"],
                 ["river", "River"], ["nation", "Border of an empire or kingdom"], ["tribe", "Border of a province"], ["gap", ""]]
    for k, P in enumerate(EMPIRES6):
        by_tint = {}
        for n, v in P["lands"].items():
            by_tint.setdefault(v[0], []).append(n)
        for tint, names in by_tint.items():
            key_rows.append(["swatch", ", ".join(names), tint, k])
    data = {
        "sheet": sheet_info(sheet), "grid": 2, "focus": 0.45, "file": "map-06-the-empires",
        "layers": layers, "territories": [], "labels": labels, "periods": periods,
        "places": pl, "features": feats, "territoryLabel": "Land", "journeys": journeys,
        "routeButton": "Journeys", "routesTitle": "Exile and return",
        "routesNote": "Choose a journey to follow it place by place. Each place is named in the verse given.",
        "routeLayer": "The exiles, Jonah, and the return",
        "title": furniture_height({"box": {"x": 12, "y": 835, "w": 560}, "scale": 4.4, "lines": [
            ["series", "MAP No. 6 · A STYLE STUDY", 7.5], ["display-fit", "THE EMPIRES", 20],
            ["sub", "ASSYRIA · BABYLON · PERSIA", 27.5],
            ["italic", "The empires of the prophets, with the exiles of Israel and Judah,", 33.5],
            ["italic", "the return, and the places of the Old Testament whose location is known", 37.4], ["rule", "", 40.6],
            ["plain", "Shown: Assyria at its height, about 670 BC", 45.5, 0],
            ["plain", "Shown: Babylon under Nebuchadnezzar, about 570 BC", 45.5, 1],
            ["plain", "Shown: Persia under Darius I, about 500 BC", 45.5, 2],
            ["credit", "After the Eilers Sunday School Maps, St. Louis · Drawn from open data · CC BY 4.0", 50.5]]}),
        "key": {"box": {"x": 1100, "y": 1290, "w": 360}, "scale": 4.7, "scale_bars": [[0, 50, 100, 150], [0, 100, 200]],
                "rows": key_rows},
    }
    page = {
        "slug": "empires", "NO": "6", "H1": "The Empires: Assyria, Babylon, Persia", "TITLE": "Bible Empires Map",
        "DESCRIPTION": "Map No. 6, a style study after the Eilers Sunday School wall maps: the empires of Assyria, Babylon "
                       "and Persia, with the exiles of Israel and Judah and the return, drawn from open data.",
        "GRID_LABEL": "Two-degree squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, in the manner of the Eilers Sunday School wall "
            "maps (A. H. Eilers &amp; Co., St. Louis). No Eilers Map No. 6 is known to us, so this sheet fills the "
            "number with the empires of the exile.",
            ["Flat tints for each land, with the seas left as paper", KEPT[1],
             "Each journey in its own color, with the places numbered", KEPT[3], KEPT[4]], CHANGED + [
                "One sheet shows three empires: choose Assyria, Babylon or Persia from the title or under Layers"],
            ["<strong>Land, water and relief</strong> come from elevation data; the rivers and lakes from Natural "
             "Earth, leaving out modern reservoirs.",
             "<strong>The journeys</strong> follow 2 Kings, Jonah, Jeremiah, Ezekiel, Ezra and Nehemiah. Every place is "
             "named in the verse given, and the build checks each name against this project's translation. The "
             "roads between are reconstructions, so they are dashed.",
             "<strong>Empires are approximate</strong>, grown from their cities, and their borders moved within each "
             "period. Provinces and vassals have their own tints inside an empire's border.",
             PLACES_MADE.format(books="the Old Testament").replace("Places scored below 500", "Places scored at least "
                                                                    "300 are shown; those below 500"), NAMES_MADE],
            SOURCES + ["Rivers and lakes: Natural Earth (public domain)"]),
    }
    return data, page


# --- Map No. 2: Palestine, Old Testament history ----------------------------------------------

HISTORY_BOOKS = {"Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "1Chr", "2Chr"}
# The peoples of Canaan before the conquest, each grown from the towns the text gives it:
# name: (tint, towns, other points, reach, verses).
PEOPLES2 = {
    "Canaanites": ("lime", ["Hazor 1", "Megiddo", "Taanach", "Beth-shan", "Ibleam", "Dor", "Acco", "Gezer", "Arad 2"], [], 20,
                   "Joshua 17:11–12; Judges 1:27–33; Numbers 21:1"),
    "Amorites": ("salmon", ["Hebron", "Jarmuth 1", "Lachish", "Eglon", "Heshbon", "Ashtaroth", "Edrei 1"], [], 26,
                 "Joshua 10:5; Deuteronomy 3:8"),
    "Jebusites": ("sage", ["Jerusalem"], [], 8, "Joshua 15:63"),
    "Hivites": ("olive", ["Gibeon", "Chephirah", "Beeroth", "Kiriath-jearim", "Shechem"], [(35.75, 33.30), (35.85, 33.20)], 12,
                "Joshua 9:7, 17; 11:3; Genesis 34:2"),
    "Perizzites": ("yellow", ["Bezek 2"], [(35.30, 32.30)], 12, "Judges 1:4; Joshua 17:15"),
    "Philistines": ("blush", ["Gaza", "Ashkelon", "Ashdod", "Ekron", "Gath 1"], [], 18, "Joshua 13:3"),
    "Sidonians": ("blush", ["Sidon", "Tyre", "Zarephath"], [], 18, "Joshua 13:4–6"),
    "Edom": ("olive", ["Bozrah 1", "Sela 1"], [], 35, "Numbers 20:14–21"),
    "Moab": ("sage", ["Kir-hareseth", "Ar"], [], 25, "Numbers 21:13–15"),
    "Ammon": ("yellow", ["Rabbah 1"], [], 25, "Numbers 21:24"),
}
# The kingdom of David and Solomon: Israel, and the peoples David made subject (2 Samuel 8).
KINGDOM2 = {"Israel": "yellow", "Edom": "olive", "Moab": "sage", "Ammon": "salmon", "Aram": "lime",
            "Philistia": "sage", "Phoenicia": "blush"}
SUBJECT2 = {"Edom", "Moab", "Ammon", "Aram"}
OT_HISTORY = [
    {"name": "Joshua in the south", "short": "Joshua, south", "ref": "Joshua 4–10", "color": "red", "unit": "Place",
     "note": "From the camp at Gilgal: Jericho and Ai, the altar on Mount Ebal, and the campaign that began at "
             "Gibeon and swept the cities of the south.",
     "stops": [
         ("Gilgal 1", "Gilgal", "Joshua 4:19", None, {"what": "The camp after crossing the Jordan"}),
         ("Jericho 1", "Jericho", "Joshua 6:2", "land", {"what": "The walls fall"}),
         ("Ai 1", "Ai", "Joshua 8:1", "land"),
         ("Mount Ebal", "Mount Ebal", "Joshua 8:30", "land", {"what": "The altar, and the law read aloud"}),
         ("Gilgal 1", "Gilgal", "Joshua 9:6", "land", {"what": "The Gibeonites' covenant"}),
         ("Gibeon", "Gibeon", "Joshua 10:10", "land", {"what": "The sun stands still"}),
         ("Beth-horon", "Beth-horon", "Joshua 10:11", "land"),
         ("Azekah", "Azekah", "Joshua 10:11", "land"),
         ("Makkedah", "Makkedah", "Joshua 10:16", "land", {"what": "The five kings in the cave"}),
         ("Libnah 1", "Libnah", "Joshua 10:29", "land"),
         ("Lachish", "Lachish", "Joshua 10:31", "land"),
         ("Eglon", "Eglon", "Joshua 10:34", "land"),
         ("Hebron", "Hebron", "Joshua 10:36", "land"),
         ("Debir 1", "Debir", "Joshua 10:38", "land"),
         ("Gilgal 1", "Gilgal", "Joshua 10:43", "land"),
     ]},
    {"name": "Joshua in the north", "short": "Joshua, north", "ref": "Joshua 11", "color": "blue", "unit": "Place",
     "note": "Against the kings of the north led by Jabin of Hazor: the battle at the waters of Merom and the pursuit "
             "to Sidon.",
     "stops": [
         ("Gilgal 1", "Gilgal", "Joshua 10:43", None),
         ("Merom", "Waters of Merom", "Joshua 11:7", "land", {"word": "Merom", "what": "The kings of the north defeated"}),
         ("Sidon", "Greater Sidon", "Joshua 11:8", "land", {"word": "Sidon"}),
         ("Misrephoth-maim", "Misrephoth-maim", "Joshua 11:8", "land"),
         ("Hazor 1", "Hazor", "Joshua 11:10", "land", {"what": "The head of all these kingdoms, burned"}),
     ]},
    {"name": "Samuel's circuit", "short": "Samuel", "ref": "1 Samuel 7", "color": "brown", "unit": "Place",
     "note": "Every year Samuel judged Israel at Bethel, Gilgal and Mizpah, and came home to Ramah.",
     "stops": [
         ("Ramah 7", "Ramah", "1 Samuel 7:17", None, {"what": "Samuel's home"}),
         ("Bethel 1", "Bethel", "1 Samuel 7:16", "land"),
         ("Gilgal 1", "Gilgal", "1 Samuel 7:16", "land"),
         ("Mizpah 3", "Mizpah", "1 Samuel 7:16", "land"),
         ("Ramah 7", "Ramah", "1 Samuel 7:17", "land"),
     ]},
    {"name": "The ark of the covenant", "short": "The ark", "ref": "1 Samuel 4–7; 2 Samuel 6", "color": "green", "unit": "Place",
     "note": "Taken into battle from Shiloh and captured by the Philistines, the ark passed from city to city until "
             "it came back to Israel, and David brought it up to Jerusalem.",
     "stops": [
         ("Shiloh", "Shiloh", "1 Samuel 4:4", None, {"what": "The ark is brought to the camp"}),
         ("Ebenezer 1", "Ebenezer", "1 Samuel 4:1", "land", {"what": "Israel defeated; the ark captured"}),
         ("Ashdod", "Ashdod", "1 Samuel 5:1", "land", {"what": "Dagon falls before the ark"}),
         ("Gath 1", "Gath", "1 Samuel 5:8", "land"),
         ("Ekron", "Ekron", "1 Samuel 5:10", "land"),
         ("Beth-shemesh 1", "Beth-shemesh", "1 Samuel 6:12", "land", {"what": "The cows bring the ark home"}),
         ("Kiriath-jearim", "Kiriath-jearim", "1 Samuel 7:1", "land", {"what": "Twenty years in Abinadab's house"}),
         ("Jerusalem", "Jerusalem", "2 Samuel 6:12", "land", {"word": "City of David", "what": "David dances before the ark"}),
     ]},
    {"name": "David's flight from Saul", "short": "David", "ref": "1 Samuel 19–27; 2 Samuel 2–5", "color": "violet", "unit": "Place",
     "note": "David fled from Saul to Samuel, then to the Philistines, the caves and the wilderness of Judah, until he "
             "became king at Hebron and took Jerusalem.",
     "stops": [
         ("Ramah 7", "Ramah", "1 Samuel 19:18", None, {"what": "David flees to Samuel"}),
         ("Nob", "Nob", "1 Samuel 21:2", "land", {"what": "The holy bread and Goliath's sword"}),
         ("Gath 1", "Gath", "1 Samuel 21:11", "land"),
         ("Adullam", "Adullam", "1 Samuel 22:1", "land", {"what": "The cave; four hundred men gather"}),
         ("Mizpeh 3", "Mizpeh in Moab", "1 Samuel 22:3", "land", {"word": "Mizpeh", "what": "His parents left with the king of Moab"}),
         ("Hereth", "Forest of Hereth", "1 Samuel 22:5", "land", {"word": "Hereth"}),
         ("Keilah", "Keilah", "1 Samuel 23:5", "land", {"what": "David saves the town from the Philistines"}),
         ("Ziph 1", "Ziph", "1 Samuel 23:14", "land"),
         ("Maon", "Maon", "1 Samuel 23:24", "land"),
         (None, "En-gedi", "1 Samuel 24:1", "land", {"at": (35.390, 31.461), "site": "Ein Gedi", "sure": 1,
                                                     "what": "David spares Saul in the cave"}),
         ("Carmel 1", "Carmel", "1 Samuel 25:2", "land", {"what": "Nabal and Abigail"}),
         ("Ziph 1", "Ziph", "1 Samuel 26:2", "land", {"what": "David spares Saul again"}),
         ("Gath 1", "Gath", "1 Samuel 27:2", "land"),
         ("Ziklag", "Ziklag", "1 Samuel 27:6", "land"),
         ("Hebron", "Hebron", "2 Samuel 2:1", "land", {"what": "Anointed king over Judah"}),
         ("Jerusalem", "Jerusalem", "2 Samuel 5:6", "land", {"what": "David takes the stronghold of Zion"}),
     ]},
]


def palestine_history_map():
    """Map No. 2, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET7, res=0.13)
    sheet.elev = elevation(sheet, 10)
    w = water(sheet, sheet.elev)
    lakes = w["Sea of Galilee"] | w["Dead Sea"] | w["Lake Huleh"]
    wet = w["sea"] | lakes
    flow = drainage(sheet, sheet.elev, w["sea"] | w["Dead Sea"], 2)
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    layers, river_km = terrain_layers(sheet, ~w["sea"], lakes, flow, wet, 150, 0.9)
    layers["borders"] = {}

    # The peoples before the conquest.
    seeds_a = []
    for n, (_, towns, extra, _, _) in PEOPLES2.items():
        seeds_a += [(t, n, by_name[t]["lon"], by_name[t]["lat"]) for t in towns]
        seeds_a += [(n, n, lon, lat) for lon, lat in extra]
    names_a = list(PEOPLES2)
    terr_a, _ = territories(sheet, sheet.elev, wet, flow + (2,), seeds_a, names=names_a,
                            cap_km={n: v[3] for n, v in PEOPLES2.items()})
    fills_a, labels_a, borders_a = territory_layers(sheet, terr_a, names_a, {n: n for n in names_a},
                                                    {n: v[0] for n, v in PEOPLES2.items()})
    # The kingdom of David and Solomon: the tribes' land as one kingdom, and its neighbours,
    # those David made subject inside its border.
    seeds_b = [(n, "Israel" if t in {x[0] for x in TRIBES} else t, lon, lat) for n, t, lon, lat in seeds(all_places)]
    seeds_b += [("Damascus", "Aram", 36.2, 33.3), ("Aram", "Aram", 36.0, 33.55)]
    names_b = list(KINGDOM2)
    terr_b, _ = territories(sheet, sheet.elev, wet, flow + (2,), seeds_b, names=names_b,
                            cap_km={**{n: 30 for n in names_b}, "Aram": 45, "Edom": 40})
    groups_b = {n: "Israel" if n in SUBJECT2 | {"Israel"} else n for n in names_b}
    fills_b, labels_b, borders_b = territory_layers(sheet, terr_b, names_b, groups_b, KINGDOM2)
    for lb in labels_a + labels_b:
        lb["style"] = "nation"
    for lb in labels_b:
        if lb["text"] == "ISRAEL":
            lb["style"] = "kingdom"
            lb["pts"] = line_km(sheet, [(34.98, 32.43), (35.25, 32.05), (35.20, 31.45)])
    periods = [
        {"name": "The peoples of Canaan", "note": "Before the conquest, about 1400 BC: the peoples the text places in each town.",
         "territories": fills_a, "labels": labels_a, "borders": borders_a},
        {"name": "David and Solomon", "note": "The united kingdom, about 970 BC, with the peoples David made subject (2 Samuel 8).",
         "territories": fills_b, "labels": labels_b, "borders": borders_b},
    ]
    labels = [{"text": "GREAT SEA", "style": "sea", "pts": line_km(sheet, [(34.24, 32.868), (34.86, 32.858)], 2)},
              {"text": "SALT SEA", "style": "sea", "pts": line_km(sheet, [(35.47, 31.69), (35.44, 31.40)], 2)}]

    pl = place_records(sheet, all_places, HISTORY_BOOKS, ours, min_score=200)
    journeys = build_journeys(sheet, OT_HISTORY, by_name, cost_grid(sheet, wet), sea_grid(sheet, w["sea"]), pl)

    feats = {"mountains": mountains(sheet, by_name, ours, ["Mount Hermon", "Mount Carmel", "Mount Tabor", "Mount Gilboa",
                                                           "Mount Ebal", "Mount Gerizim"]),
             "rivers": [], "waters": [], "regions": []}
    for n, length in RIVERS.items():
        p = by_name[n]
        line = follow(river_km, p["lon"], p["lat"], sheet, length)
        if line:
            name = display_name(p, ours)
            feats["rivers"].append({"n": "River Jordan" if name == "Jordan" else name, "pts": line, "main": name == "Jordan"})
    for lon, lat, text in ((35.585, 32.80, "SEA OF KINNERETH"), (35.612, 33.075, "Waters of Merom")):
        x, y = sheet.xy(lon, lat)
        feats["waters"].append({"n": text, "x": round(x, 2), "y": round(y, 2), "lake": 1})

    key_rows = [["camp", "Place on a journey"], ["camp-unsure", "Place uncertain (?)"]]
    key_rows += [["journey", J["name"], J["color"]] for J in journeys]
    key_rows += [["conjectural", "Way uncertain"], ["gap", ""], ["dot", "Town"], ["unsure", "Site uncertain (?)"],
                 ["mount", "Mountain"], ["river", "River"], ["nation", "Border of a people"], ["gap", ""]]
    by_tint = {}
    for n, v in PEOPLES2.items():
        by_tint.setdefault(v[0], []).append(n)
    key_rows += [["swatch", ", ".join(v), t, 0] for t, v in by_tint.items()]
    key_rows += [["swatch", "Kingdom of Israel", "yellow", 1], ["swatch", "Edom (subject)", "olive", 1],
                 ["swatch", "Moab (subject), Philistia", "sage", 1], ["swatch", "Ammon (subject)", "salmon", 1],
                 ["swatch", "Aram (subject)", "lime", 1], ["swatch", "Phoenicia (ally)", "blush", 1]]
    data = {
        "sheet": sheet_info(sheet), "grid": 10 / 60, "focus": 0.56, "file": "map-02-palestine-old-testament-history",
        "layers": layers, "territories": [], "labels": labels, "periods": periods,
        "places": pl, "features": feats, "territoryLabel": "Land", "journeys": journeys,
        "routeButton": "Journeys", "routesTitle": "From Joshua to David",
        "routesNote": "Choose a journey to follow it place by place. Each place is named in the verse given.",
        "routeLayer": "Joshua's campaigns, Samuel, the ark and David",
        "title": furniture_height({"box": {"x": 5, "y": 5, "w": 66}, "scale": 1, "lines": [
            ["series", "MAP No. 2 · A STYLE STUDY", 7.5], ["display-fit", "PALESTINE", 19],
            ["sub", "OLD TESTAMENT HISTORY", 26.5],
            ["italic", "The conquest of Canaan, the judges and the", 32.5],
            ["italic", "kingdom of David and Solomon, with the places", 36.4],
            ["italic", "named in Joshua to 2 Chronicles", 40.3], ["rule", "", 44],
            ["plain", "Shown: the peoples of Canaan", 49.5, 0], ["plain", "Shown: David and Solomon’s kingdom", 49.5, 1],
            ["plain", "The conquest: 1451 BC by Ussher,", 53.5],
            ["plain", "1400 or 1200 BC by modern reckoning", 57.5], ["rule", "", 61],
            ["credit", "After the Eilers Sunday School Maps, St. Louis.", 65.5],
            ["credit", "Drawn from open data · CC BY 4.0", 69.5]]}),
        "key": {"box": {"x": 5, "y": 96, "w": 47}, "scale": 0.95, "rows": key_rows},
    }
    page = {
        "slug": "palestine-history", "NO": "2", "H1": "Palestine: Old Testament History", "TITLE": "Old Testament History Map",
        "DESCRIPTION": "Map No. 2, a style study after the Eilers Sunday School wall maps: the conquest of Canaan, the "
                       "judges and the kingdom of David and Solomon, with Joshua's campaigns, the ark and David's flight, "
                       "drawn from open data.",
        "GRID_LABEL": "Ten-minute squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, after <strong>Eilers Sunday School Map No. "
            "2</strong>, <em>Palestine, Old Testament History</em> (A. H. Eilers &amp; Co., St. Louis), redrawn from "
            "open data.",
            ["Flat tints for each people and kingdom, with the seas left as paper", KEPT[1],
             "Each journey in its own color, with the places numbered", KEPT[3], KEPT[4]], CHANGED + [
                "Two periods on one sheet: choose the peoples of Canaan or the kingdom of David and Solomon"],
            ["<strong>Land, water and relief</strong> come from elevation data. Lake Huleh and the Dead Sea are drawn "
             "at their old shorelines.",
             "<strong>The journeys</strong> follow Joshua, 1 and 2 Samuel. Every place is named in the verse given, "
             "and the build checks each name against this project's translation.",
             "<strong>The peoples of Canaan are approximate.</strong> Each is grown from the towns the text gives it "
             "(the five Amorite kings of Joshua 10, the Hivite towns of Joshua 9, the Canaanite cities of Judges 1), "
             "and the Bible's lists overlap.",
             "<strong>The kingdom of David and Solomon</strong> is the land of the tribes as on Map No. 7, with Edom, "
             "Moab, Ammon and Aram made subject (2 Samuel 8). Solomon's rule reached north to Tiphsah on the "
             "Euphrates (1 Kings 5:4), beyond this sheet.",
             PLACES_MADE.format(books="Joshua to 2 Chronicles"), NAMES_MADE], SOURCES),
    }
    return data, page


# --- Plan of Ancient Jerusalem ----------------------------------------------------------------

SHEET_J = (35.220, 35.265, 31.764, 31.794)
CITY_CENTRE = (35.2342, 31.7767)        # where OpenBible puts what it can't place within the city
PLAN_KINDS = ["settlement", "pool", "spring", "garden", "hill", "structure", "field", "altar", "rock", "fortification"]
JERUSALEM_JOURNEYS = [
    {"name": "Jesus' last week", "short": "Jesus", "ref": "Matthew 21 – John 19; Acts 1", "color": "red", "unit": "Place",
     "note": "From Bethany over the Mount of Olives into the city and the temple, to Gethsemane, the judgment seat "
             "and the cross.",
     "stops": [
         ("Bethany 1", "Bethany", "John 12:1", None, {"what": "Mary anoints Jesus"}),
         ("Bethphage", "Bethphage", "Matthew 21:1", "land", {"what": "The disciples fetch the donkey"}),
         ("Mount of Olives", "Mount of Olives", "Luke 19:37", "land", {"what": "The crowd praises God; Jesus weeps over the city"}),
         ("Most Holy Place 2", "The temple", "Matthew 21:12", "land", {"word": "temple", "what": "The money changers driven out"}),
         ("Bethany 1", "Bethany", "Matthew 21:17", "land"),
         ("Most Holy Place 2", "The temple", "Mark 11:27", "land", {"word": "temple", "what": "Teaching; questions from the leaders"}),
         (None, "The upstairs room", "Mark 14:15", "land", {"word": "upstairs room", "why": "Not plotted: its place is not "
                                                            "known. Tradition puts it on Mount Zion."}),
         ("Gethsemane", "Gethsemane", "Mark 14:32", "land", {"what": "Jesus prays and is arrested"}),
         (None, "The high priest's house", "Mark 14:53", "land", {"word": "high priest", "why": "Not plotted: the house of "
                                                                  "Caiaphas has not been found."}),
         ("Gabbatha", "Gabbatha", "John 19:13", "land", {"what": "Pilate's judgment seat",
                                                         "note": "Shown at Herod's palace, where many place Pilate's "
                                                                 "headquarters; others place it at the Antonia fortress, "
                                                                 "north of the temple."}),
         ("Golgotha", "Golgotha", "John 19:17", "land", {"what": "The cross, and the tomb in the garden (John 19:41)",
                                                         "note": "Shown at the Church of the Holy Sepulchre, the "
                                                                 "traditional site."}),
         ("Mount of Olives", "Olivet", "Acts 1:12", "land", {"word": "Olivet", "what": "The disciples return after the ascension"}),
     ]},
    {"name": "David's flight from Absalom", "short": "David", "ref": "2 Samuel 15–16", "color": "blue", "unit": "Place",
     "note": "When Absalom rebelled, David left the city on foot, crossed the Kidron and went up the Mount of Olives, "
             "weeping.",
     "stops": [
         ("City of David", "Jerusalem", "2 Samuel 15:14", None, {"what": "David and his household flee"}),
         (None, "Kidron Valley", "2 Samuel 15:23", "land", {"word": "Kidron", "at": (35.2382, 31.7752), "sure": 0,
                                                            "site": "below the City of David", "what": "The king crosses the brook"}),
         ("Mount of Olives", "Mount of Olives", "2 Samuel 15:30", "land", {"what": "David goes up barefoot, weeping"}),
         ("Bahurim", "Bahurim", "2 Samuel 16:5", "land", {"what": "Shimei curses David"}),
     ]},
]


def jerusalem_map():
    """The plan of Ancient Jerusalem, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET_J, res=0.004)
    # The finest tiles here come from a coarser survey; smooth them over about 40 m, so the
    # hachures follow the hills and valleys rather than its grid.
    sheet.elev = elev = ndimage.gaussian_filter(elevation(sheet, 15), 10)
    none = np.zeros(elev.shape, bool)
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    flow = drainage(sheet, elev, none, 2)
    layers, valley_km = terrain_layers(sheet, ~none, none, flow, none, 0.25, 0.028, ripple_km=(0.01, 0.02),
                                       river_classes=(1.0, 3.0), min_slope=4.0)
    layers["borders"] = {}
    books = OT_BOOKS | NT_BOOKS
    pl = [p for p in place_records(sheet, all_places, books, ours, min_score=300, kinds=PLAN_KINDS)
          if (round(sheet.lonlat(p["x"], p["y"])[0], 3), round(sheet.lonlat(p["x"], p["y"])[1], 3)) !=
          (round(CITY_CENTRE[0], 3), round(CITY_CENTRE[1], 3))]
    journeys = build_journeys(sheet, JERUSALEM_JOURNEYS, by_name, cost_grid(sheet, none, step=2, slope_weight=12.0),
                              sea_grid(sheet, none), pl)

    feats = {"mountains": [], "rivers": [], "waters": [], "regions": []}
    for n, text in (("Mount of Olives", "Mt. of Olives"), ("Mount Zion", "Mt. Zion"), ("Mount Moriah", "Mt. Moriah")):
        p = by_name[n]
        x, y = sheet.xy(p["lon"], p["lat"])
        feats["mountains"].append({"n": text, "x": round(x, 2), "y": round(y, 2)})
    for text, lon, lat in (("KIDRON VALLEY", 35.2392, 31.7800), ("VALLEY OF HINNOM", 35.2290, 31.7688), ("OPHEL", 35.2368, 31.7752)):
        x, y = sheet.xy(lon, lat)
        feats["regions"].append({"n": text, "x": round(x, 2), "y": round(y, 2)})
    for n, lon, lat, length in (("Brook Kidron", 35.2395, 31.7740, 1.2),):
        line = follow(valley_km, lon, lat, sheet, length, reach_km=0.3)
        if line:
            feats["rivers"].append({"n": n, "pts": line})

    data = {
        "sheet": sheet_info(sheet), "grid": 0.005, "focus": 0.45, "file": "plan-of-ancient-jerusalem",
        "margin": 0.22, "land": "wild", "layers": layers, "territories": [], "labels": [],
        "places": pl, "features": feats, "journeys": journeys,
        "routeButton": "Journeys", "routesTitle": "Journeys in Jerusalem",
        "routesNote": "Choose a journey to follow it place by place. Each place is named in the verse given.",
        "routeLayer": "The last week of Jesus, and David's flight",
        "title": furniture_height({"box": {"x": 0.08, "y": 0.08, "w": 1.30}, "scale": 0.0175, "lines": [
            ["series", "A PLAN · A STYLE STUDY", 7.5], ["display-fit", "ANCIENT JERUSALEM", 19.5],
            ["italic", "The hills and valleys of the city, with the places", 26],
            ["italic", "of the Bible whose location is known, from the", 29.9],
            ["italic", "springs of Gihon and En-rogel to Golgotha", 33.8], ["rule", "", 37],
            ["plain", "The walls are left out: their lines are", 41.5],
            ["plain", "not known well enough to draw", 45.3], ["rule", "", 48.5],
            ["credit", "After the Eilers Sunday School Maps, St. Louis.", 53],
            ["credit", "Drawn from open data · CC BY 4.0", 57]]}),
        "key": {"box": {"x": 3.38, "y": 0.52, "w": 0.82}, "scale": 0.0175,
                "scale_bars": [[0, 0.1, 0.2, 0.3], [0, 0.2, 0.4]],
                "rows": [["camp", "Place on a journey"], ["camp-unsure", "Place uncertain (?)"],
                         ["journey", "Jesus' last week", "red"], ["journey", "David's flight from Absalom", "blue"],
                         ["conjectural", "Way uncertain"], ["gap", ""], ["dot", "Place"], ["unsure", "Site uncertain (?)"],
                         ["mount", "Hill"], ["river", "Watercourse"]]},
    }
    page = {
        "slug": "jerusalem", "NO": "J", "SERIES": "Plan of Ancient Jerusalem", "TAG": "Plan",
        "H1": "Ancient Jerusalem", "TITLE": "Ancient Jerusalem Plan",
        "DESCRIPTION": "A plan of Ancient Jerusalem, a style study after the Eilers Sunday School maps: the hills and "
                       "valleys of the city with the places of the Bible whose location is known, drawn from open data.",
        "GRID_LABEL": "Squares of about 500 metres, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, after the Eilers sheet <em>Ancient "
            "Jerusalem</em> (A. H. Eilers &amp; Co., St. Louis), redrawn from open data.",
            ["Hachured hills and the valleys between them", KEPT[3], KEPT[4]],
            CHANGED[:2] + ["The walls are left out: no open survey of the ancient walls exists, and drawing them from "
                           "guesswork would look more certain than it is"],
            ["<strong>The ground</strong> comes from fine elevation data (about 5 m); the hachures and watercourses "
             "are drawn from it, so the Kidron, the Central Valley and the Valley of Hinnom show as they are today, "
             "partly filled with the debris of centuries.",
             "<strong>Places</strong> are those OpenBible.info locates within the city: springs, pools, hills, "
             "gardens and buildings. Many places it can only put \"in Jerusalem\", such as most of the gates "
             "Nehemiah names, are left off.",
             "<strong>The journeys</strong> follow the Gospels, Acts and 2 Samuel. Every place is named in the verse "
             "given, and the build checks each name against this project's translation.", NAMES_MADE], SOURCES),
    }
    return data, page


# --- Map No. 1: Palestine in the time of Christ ------------------------------------------------

GOSPELS = ["Matt", "Mark", "Luke", "John"]
# The lands about AD 28 (Luke 3:1), each grown from its towns: tint by ruler, so the regions one
# man ruled share a tint and are parted by dashed lines. Ruler, tint, towns, other points, reach.
HERODIAN = {
    "Galilee": ("Herod Antipas", ["Nazareth", "Cana", "Capernaum", "Nain", "Tiberias", "Magdala", "Chorazin"],
                [(35.28, 32.75), (35.45, 33.0), (35.27, 32.83), (35.50, 32.82), (35.20, 32.90), (35.35, 33.05)], 22),
    "Perea": ("Herod Antipas", [], [(35.62, 31.56), (35.66, 32.18), (35.63, 31.83), (35.75, 32.06), (35.70, 31.95),
                                    (35.66, 32.35), (35.70, 31.70)], 16),
    "Samaria": ("Roman Judea", ["Sychar", "Samaria 1"], [(35.30, 32.46), (35.10, 32.30), (35.25, 32.10), (35.40, 32.25)], 20),
    "Judea": ("Roman Judea", ["Jerusalem", "Bethlehem 1", "Bethany 1", "Emmaus", "Jericho 2", "Ephraim 2", "Arimathea",
                              "Joppa", "Lod", "Caesarea"], [(34.90, 31.75), (35.05, 31.90), (34.65, 31.75)], 22),
    "Idumea": ("Roman Judea", ["Hebron"], [(34.90, 31.60), (35.03, 31.50), (35.00, 31.25), (34.80, 31.24)], 24),
    "Decapolis": ("Decapolis", ["Gadara", "Gerasa"], [(35.66, 32.78), (35.62, 32.45), (35.50, 32.50), (35.87, 32.68),
                                                       (35.93, 31.95), (35.93, 32.65), (36.05, 32.75)], 18),
    "Gaulanitis": ("Philip", ["Caesarea Philippi", "Bethsaida 2"], [(35.74, 32.90), (35.80, 33.05), (35.90, 32.90)], 18),
    "Trachonitis": ("Philip", [], [(36.45, 32.97), (36.20, 32.80), (36.35, 32.65)], 20),
    "Ituraea": ("Philip", [], [(35.85, 33.40), (35.95, 33.25)], 16),
    "Abilene": ("Lysanias", [], [(36.10, 33.63), (36.00, 33.55)], 14),
    "Phoenicia": ("Syria", ["Tyre", "Sidon", "Zarephath", "Ptolemais"], [(35.20, 33.10), (35.30, 33.40)], 18),
    "Syria": ("Syria", ["Damascus"], [(36.20, 33.30), (36.40, 33.15)], 22),
    "Arabia": ("Aretas", [], [(35.70, 31.18), (35.85, 31.05), (36.10, 31.40), (35.78, 31.45)], 30),
}
RULER_TINTS = {"Herod Antipas": "yellow", "Roman Judea": "salmon", "Philip": "lime", "Decapolis": "olive",
               "Syria": "blush", "Lysanias": "sage", "Aretas": "sage"}
KURSI = {"at": (35.650, 32.826), "site": "Kursi, on the east shore (traditional)", "sure": 0}
JORDAN_SITE = ("John 1:28 puts John's baptizing at Bethany on the other side of the Jordan; it is shown at the "
               "traditional site, opposite Jericho.")
# The places each Gospel names, in the order it names them, each named in the verse given.
GOSPEL_JOURNEYS = [
    {"name": "The Gospel of Matthew", "short": "Matthew", "ref": "Matthew", "color": "blue", "unit": "Place",
     "note": "The places Matthew names, in his order: from Bethlehem and the flight to Egypt, through Galilee, to "
             "Jerusalem. The Gospels don't map every journey; the line joins the places along the easiest ground.",
     "stops": [
         ("Bethlehem 1", "Bethlehem", "Matthew 2:1", None, {"what": "Jesus is born; the magi come"}),
         ("Egypt", "Egypt", "Matthew 2:14", "land", {"why": "Not plotted: Egypt lies beyond this map."}),
         ("Nazareth", "Nazareth", "Matthew 2:23", "land"),
         ("Bethany 2", "The Jordan", "Matthew 3:13", "land", {"word": "Jordan", "what": "Jesus is baptized by John",
                                                               "note": JORDAN_SITE}),
         ("Capernaum", "Capernaum", "Matthew 4:13", "land", {"what": "Jesus makes his home here"}),
         (None, "Region of the Gadarenes", "Matthew 8:28", "sea", KURSI | {"word": "Gadarenes", "what": "Two men freed from demons",
                                                                           "note": "Named for Gadara, a town of the Decapolis."}),
         ("Gennesaret", "Gennesaret", "Matthew 14:34", "sea"),
         ("Tyre", "Tyre", "Matthew 15:21", "land", {"what": "A Canaanite woman's daughter healed"}),
         ("Magadan", "Magadan", "Matthew 15:39", "land"),
         ("Caesarea Philippi", "Caesarea Philippi", "Matthew 16:13", "land", {"what": "Peter: \"You are the Messiah\""}),
         ("Capernaum", "Capernaum", "Matthew 17:24", "land"),
         ("Jericho 2", "Jericho", "Matthew 20:29", "land", {"via": [(35.62, 32.30), (35.58, 31.95)], "guess": True,
                                                            "note": "From Galilee \"into the region of Judea across the "
                                                                    "Jordan\" (Matthew 19:1)."}),
         ("Bethphage", "Bethphage", "Matthew 21:1", "land"),
         ("Jerusalem", "Jerusalem", "Matthew 21:10", "land", {"what": "The temple; the cross and the empty tomb (Matthew 21–28)"}),
         ("Bethany 1", "Bethany", "Matthew 21:17", "land"),
         ("Galilee 1", "Galilee", "Matthew 28:16", "land", {"why": "Not plotted: Matthew names only Galilee, and a mountain there."}),
     ]},
    {"name": "The Gospel of Mark", "short": "Mark", "ref": "Mark", "color": "red", "unit": "Place",
     "note": "The places Mark names, in his order: from the Jordan to Galilee and the lands around it, then to "
             "Jerusalem. The line joins the places along the easiest ground, and by boat on the lake.",
     "stops": [
         ("Nazareth", "Nazareth", "Mark 1:9", None),
         ("Bethany 2", "The Jordan", "Mark 1:9", "land", {"word": "Jordan", "what": "Jesus is baptized by John", "note": JORDAN_SITE}),
         ("Capernaum", "Capernaum", "Mark 1:21", "land", {"what": "Teaching in the synagogue; healings"}),
         (None, "Region of the Gerasenes", "Mark 5:1", "sea", KURSI | {"word": "Gerasenes", "what": "A man freed from a legion of demons",
                                                                       "note": "Named for Gerasa, a city of the Decapolis."}),
         ("Bethsaida 2", "Bethsaida", "Mark 6:45", "sea"),
         ("Gennesaret", "Gennesaret", "Mark 6:53", "sea"),
         ("Tyre", "Tyre", "Mark 7:24", "land", {"what": "A Syrophoenician woman's daughter healed"}),
         ("Sidon", "Sidon", "Mark 7:31", "land"),
         ("Decapolis", "Decapolis", "Mark 7:31", "land", {"why": "Not plotted: Mark names only the region, east of the lake."}),
         ("Dalmanutha", "Dalmanutha", "Mark 8:10", "land", {"via": [(35.72, 32.92)], "guess": True}),
         ("Bethsaida 2", "Bethsaida", "Mark 8:22", "sea", {"what": "A blind man healed"}),
         ("Caesarea Philippi", "Caesarea Philippi", "Mark 8:27", "land", {"what": "Peter: \"You are the Messiah\""}),
         ("Capernaum", "Capernaum", "Mark 9:33", "land"),
         ("Jericho 2", "Jericho", "Mark 10:46", "land", {"via": [(35.62, 32.30), (35.58, 31.95)], "guess": True,
                                                         "what": "Bartimaeus receives his sight",
                                                         "note": "From Galilee \"into the region of Judea and across the "
                                                                 "Jordan\" (Mark 10:1)."}),
         ("Bethany 1", "Bethany", "Mark 11:1", "land"),
         ("Jerusalem", "Jerusalem", "Mark 11:11", "land", {"what": "The temple; the cross and the empty tomb (Mark 11–16)"}),
     ]},
    {"name": "The Gospel of Luke", "short": "Luke", "ref": "Luke", "color": "green", "unit": "Place",
     "note": "The places Luke names, in his order: Nazareth, Bethlehem and the temple, the ministry in Galilee, "
             "and the long road to Jerusalem.",
     "stops": [
         ("Nazareth", "Nazareth", "Luke 1:26", None, {"what": "Gabriel comes to Mary"}),
         ("Bethlehem 1", "Bethlehem", "Luke 2:4", "land", {"what": "Jesus is born"}),
         ("Jerusalem", "Jerusalem", "Luke 2:22", "land", {"what": "Presented in the temple"}),
         ("Nazareth", "Nazareth", "Luke 2:39", "land"),
         ("Jerusalem", "Jerusalem", "Luke 2:41", "land", {"what": "At twelve, in the temple"}),
         ("Nazareth", "Nazareth", "Luke 2:51", "land"),
         ("Bethany 2", "The Jordan", "Luke 4:1", "land", {"word": "Jordan", "what": "Baptized; then the wilderness", "note": JORDAN_SITE}),
         ("Nazareth", "Nazareth", "Luke 4:16", "land", {"what": "Rejected in the synagogue"}),
         ("Capernaum", "Capernaum", "Luke 4:31", "land"),
         ("Gennesaret", "Lake of Gennesaret", "Luke 5:1", "land", {"word": "Gennesaret", "what": "The catch of fish; Peter called"}),
         ("Nain", "Nain", "Luke 7:11", "land", {"what": "A widow's son raised"}),
         (None, "Region of the Gerasenes", "Luke 8:26", "sea", KURSI | {"word": "Gerasenes", "via": [{"p": "Capernaum", "how": "land"}],
                                                                        "what": "A man freed from a legion of demons"}),
         ("Bethsaida 2", "Bethsaida", "Luke 9:10", "sea", {"what": "Feeding of the five thousand"}),
         ("Samaria 2", "A Samaritan village", "Luke 9:52", "land", {"word": "Samaritan", "why": "Not plotted: Luke doesn't name the village."}),
         ("Jericho 2", "Jericho", "Luke 19:1", "land", {"what": "Zacchaeus"}),
         ("Bethany 1", "Bethany", "Luke 19:29", "land"),
         ("Jerusalem", "Jerusalem", "Luke 19:28", "land", {"what": "The temple; the cross and the empty tomb (Luke 19–24)"}),
         ("Emmaus", "Emmaus", "Luke 24:13", "land", {"what": "The risen Jesus walks with two disciples"}),
         ("Jerusalem", "Jerusalem", "Luke 24:33", "land"),
         ("Bethany 1", "Bethany", "Luke 24:50", "land", {"what": "Jesus is taken up into heaven"}),
     ]},
    {"name": "The Gospel of John", "short": "John", "ref": "John", "color": "violet", "unit": "Place",
     "note": "The places John names, in his order. John follows Jesus to Jerusalem for the festivals again and again.",
     "stops": [
         ("Bethany 2", "Bethany beyond the Jordan", "John 1:28", None, {"word": "Bethany", "what": "John baptizes; the first disciples"}),
         ("Cana", "Cana", "John 2:1", "land", {"what": "Water made wine"}),
         ("Capernaum", "Capernaum", "John 2:12", "land"),
         ("Jerusalem", "Jerusalem", "John 2:13", "land", {"what": "The temple cleared; Nicodemus"}),
         ("Sychar", "Sychar", "John 4:5", "land", {"what": "The woman at the well"}),
         ("Cana", "Cana", "John 4:46", "land", {"what": "An official's son healed"}),
         ("Jerusalem", "Jerusalem", "John 5:1", "land", {"what": "A man healed at the pool of Bethesda"}),
         ("Capernaum", "Capernaum", "John 6:24", "land", {"what": "The bread of life"}),
         ("Jerusalem", "Jerusalem", "John 10:22", "land", {"what": "The Festivals of Booths and Dedication (John 7–10)"}),
         ("Bethany 2", "Across the Jordan", "John 10:40", "land", {"word": "Jordan"}),
         ("Bethany 1", "Bethany", "John 11:18", "land", {"what": "Lazarus raised"}),
         ("Ephraim 2", "Ephraim", "John 11:54", "land"),
         ("Bethany 1", "Bethany", "John 12:1", "land", {"what": "Mary anoints Jesus"}),
         ("Jerusalem", "Jerusalem", "John 12:12", "land", {"what": "The entry, the cross and the empty tomb (John 12–20)"}),
         (None, "Sea of Tiberias", "John 21:1", "land", {"word": "Tiberias", "at": (35.549, 32.873), "site": "Tabgha (traditional)",
                                                         "sure": 0, "what": "The risen Jesus by the lake; Peter restored"}),
     ]},
]


def palestine_map():
    """Map No. 1, as a dict ready for JSON, and the words for its page."""
    sheet = Sheet(*SHEET7, res=0.13)
    sheet.elev = elevation(sheet, 10)
    w = water(sheet, sheet.elev)
    lakes = w["Sea of Galilee"] | w["Dead Sea"] | w["Lake Huleh"]
    wet = w["sea"] | lakes
    flow = drainage(sheet, sheet.elev, w["sea"] | w["Dead Sea"], 2)
    all_places = places()
    by_name = {p["name"]: p for p in all_places}
    ours = our_spellings()
    seeds1 = []
    for n, (_, towns, extra, _) in HERODIAN.items():
        seeds1 += [(t, n, by_name[t]["lon"], by_name[t]["lat"]) for t in towns]
        seeds1 += [(n, n, lon, lat) for lon, lat in extra]
    names = list(HERODIAN)
    terr, names = territories(sheet, sheet.elev, wet, flow + (2,), seeds1, names=names,
                              cap_km={n: v[3] for n, v in HERODIAN.items()})
    groups = {n: v[0] for n, v in HERODIAN.items()}
    for n in ("Decapolis", "Abilene", "Arabia"):     # regions that stand alone are named as nations
        groups[n] = n
    tints = dict(RULER_TINTS, Abilene="sage", Arabia="sage")

    layers, river_km = terrain_layers(sheet, ~w["sea"], lakes, flow, wet, 150, 0.9)
    fills, labels, layers["borders"] = territory_layers(sheet, terr, names, groups, tints)
    for lb in labels:
        lb["style"] = "nation"
    labels += [{"text": "MEDITERRANEAN SEA", "style": "sea", "pts": line_km(sheet, [(34.30, 32.60), (34.70, 33.25)], 2)},
               {"text": "DEAD SEA", "style": "sea", "pts": line_km(sheet, [(35.47, 31.69), (35.44, 31.40)], 2)}]

    pl = place_records(sheet, all_places, NT_BOOKS, ours, terr, names)
    water_grid = sea_grid(sheet, w["sea"] | w["Sea of Galilee"])
    journeys = build_journeys(sheet, GOSPEL_JOURNEYS, by_name, cost_grid(sheet, wet), water_grid, pl)

    feats = {"mountains": mountains(sheet, by_name, ours, ["Mount Hermon", "Mount Tabor", "Mount Gerizim", "Mount of Olives"]),
             "rivers": [], "waters": [], "regions": []}
    line = follow(river_km, 35.57, 32.35, sheet, 70)
    if line:
        feats["rivers"].append({"n": "River Jordan", "pts": line, "main": True})
    x, y = sheet.xy(35.585, 32.80)
    feats["waters"].append({"n": "SEA OF GALILEE", "x": round(x, 2), "y": round(y, 2), "lake": 1})

    key_rows = [["camp", "Place on a journey"], ["camp-unsure", "Place uncertain (?)"]]
    key_rows += [["journey", J["name"].replace("The Gospel of ", "As told by "), J["color"]] for J in journeys]
    key_rows += [["conjectural", "Way uncertain"], ["gap", ""], ["dot", "Town"], ["unsure", "Site uncertain (?)"],
                 ["mount", "Mountain"], ["river", "River"], ["nation", "Border of a realm"],
                 ["tribe", "Border of a region"], ["gap", ""],
                 ["swatch", "Herod Antipas", "yellow"], ["swatch", "Roman Judea (Pilate)", "salmon"],
                 ["swatch", "Philip", "lime"], ["swatch", "The Decapolis", "olive"], ["swatch", "Province of Syria", "blush"],
                 ["swatch", "Lysanias; Aretas of Arabia", "sage"]]
    data = {
        "sheet": sheet_info(sheet), "grid": 10 / 60, "focus": 0.56, "file": "map-01-palestine-in-the-time-of-christ",
        "layers": layers, "territories": fills, "labels": labels,
        "places": pl, "features": feats, "territoryLabel": "Region", "journeys": journeys,
        "routeButton": "Gospels", "routesTitle": "The journeys of Jesus",
        "routesNote": "Choose a Gospel to follow the places it names, in its order. Each place is named in the verse given.",
        "routeLayer": "The places each Gospel names, in order",
        "title": furniture_height({"box": {"x": 5, "y": 5, "w": 66}, "scale": 1, "lines": [
            ["series", "MAP No. 1 · A STYLE STUDY", 7.5], ["display-fit", "PALESTINE", 19],
            ["sub", "IN THE TIME OF CHRIST", 26.5],
            ["italic", "The places of the land named in the New", 32.5],
            ["italic", "Testament whose location is known, and the", 36.4],
            ["italic", "journeys of Jesus as each Gospel tells them", 40.3], ["rule", "", 44],
            ["plain", "About 5 BC to AD 30 by modern reckoning", 49.5],
            ["plain", "The realms as in Luke 3:1, about AD 28", 53.5], ["rule", "", 57],
            ["credit", "After the Eilers Sunday School Maps, St. Louis.", 61.5],
            ["credit", "Drawn from open data · CC BY 4.0", 65.5]]}),
        "key": {"box": {"x": 5, "y": 92, "w": 47}, "scale": 0.95, "rows": key_rows},
    }
    page = {
        "slug": "palestine", "NO": "1", "H1": "Palestine in the Time of Christ", "TITLE": "Time of Christ Map",
        "DESCRIPTION": "Map No. 1, a style study after the Eilers Sunday School wall maps: the land of the Gospels, "
                       "its rulers about AD 28, and the places each Gospel names, drawn from open data.",
        "GRID_LABEL": "Ten-minute squares, as used by the index",
        "ABOUT": about_html(
            "A <strong>style study</strong> for the project's Bible maps, after <strong>Eilers Sunday School Map No. "
            "1</strong>, <em>Palestine</em> in the time of Christ (A. H. Eilers &amp; Co., St. Louis), redrawn from "
            "open data.",
            ["Flat tints for each realm, with the seas left as paper", KEPT[1], KEPT[3], KEPT[4]], CHANGED + [
                "Choose a Gospel to follow the places it names, in its order"],
            ["<strong>Land, water and relief</strong> come from elevation data. Lake Huleh and the Dead Sea are drawn "
             "at their old shorelines.",
             "<strong>The journeys</strong> join the places each Gospel names, in the order it names them, along the "
             "easiest ground and by boat on the lake. The Gospels don't map every journey, so the lines show the "
             "order of places, not the roads taken. Every place is named in the verse given, and the build checks "
             "each name against this project's translation.",
             "<strong>The realms are approximate</strong>, grown from their towns: Herod Antipas, Philip and "
             "Lysanias as tetrarchs, Judea, Samaria and Idumea under the Roman governor, and the free cities of the "
             "Decapolis.", PLACES_MADE.format(books="the New Testament"), NAMES_MADE], SOURCES),
    }
    return data, page


def write_map(data, page):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import webpages
    slug = page["slug"]
    os.makedirs(os.path.join(SITE, "maps", "data"), exist_ok=True)
    with open(os.path.join(SITE, "maps", "data", slug + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    body = open(os.path.join(ROOT, "scripts", "templates", "map.html"), encoding="utf-8").read()
    sh = data["sheet"]
    page = {"SERIES": f"Map No. {page['NO']}", "TAG": f'<span class="wide">Map </span>No. {page["NO"]}',
            "PAGE": "landscape" if sh["width"] >= sh["height"] else "portrait", **page}
    for k, v in page.items():
        body = body.replace("{{" + k + "}}", v)
    body = body.replace("<!-- DATA -->", f'<script type="application/json" id="data">{webpages._dump(data)}</script>')
    with open(os.path.join(SITE, "maps", slug + ".html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.STANDALONE.format(page=body))


# The sheets in the order of the Bible's history, for the index page: slug, number (or the
# word for an unnumbered sheet), title, era and a line about each.
INDEX = [
    ("western-asia", "4", "Western Asia", "The patriarchs · about 2000–1700 BC",
     "The lands of the Old Testament from Egypt to Persia, with the journeys of Abraham, Jacob and Joseph."),
    ("exodus", "5", "The Exodus", "The wilderness years · 1491 BC by Ussher",
     "The 42 camps of Numbers 33 from Rameses to the plains of Moab, and the proposed sites of Mount Sinai."),
    ("palestine-history", "2", "Palestine: Old Testament History", "The conquest to Solomon · about 1400–930 BC",
     "The peoples of Canaan and the kingdom of David and Solomon, with Joshua's campaigns, the ark and David's flight."),
    ("kingdoms", "7", "The Kingdoms of Judah and Israel", "The divided kingdom · 931–586 BC",
     "The tribal allotments of Joshua and the two kingdoms, with the journeys of Elijah and Elisha."),
    ("empires", "6", "The Empires: Assyria, Babylon, Persia", "The exile and return · about 740–440 BC",
     "Three empires on one sheet, with the exiles of Israel and Judah, Jonah, and the return under Ezra and Nehemiah."),
    ("palestine", "1", "Palestine in the Time of Christ", "The life of Jesus · about 5 BC to AD 30",
     "The realms of Herod's sons and the Roman governor, with the places each Gospel names, in its order."),
    ("jerusalem", "Plan", "Ancient Jerusalem", "From David to the apostles",
     "The hills and valleys of the city with its known sites, Jesus' last week and David's flight from Absalom."),
    ("roman-empire", "3", "The Roman Empire and the Travels of Paul", "The church spreads · about AD 35–62",
     "The provinces about AD 50 and Paul's journeys in Acts, from Damascus to Rome."),
]


def write_index():
    """maps/index.html: every sheet built so far, with its journeys and tints."""
    import html
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import webpages
    cards = []
    for slug, no, title, era, blurb in INDEX:
        path = os.path.join(SITE, "maps", "data", slug + ".json")
        if not os.path.exists(path):
            continue
        d = json.load(open(path, encoding="utf-8"))
        fills = d["territories"] + [t for P in d.get("periods", []) for t in P["territories"]]
        tints = list(dict.fromkeys(t["tint"] for t in fills)) or ["wild"]
        journeys = "".join(f'<li style="--jc: var(--route-{J["color"]})">{html.escape(J["short"])}</li>'
                           for J in d.get("journeys", []))
        stops = sum(len(J["stops"]) for J in d.get("journeys", []))
        plate = (f'<span class="lbl">Map No.</span><span class="no">{no}</span>' if no.isdigit()
                 else f'<span class="lbl">Ancient</span><span class="no word">{no}</span>')
        cards.append(
            f'    <li><a class="sheet" href="{slug}.html">\n'
            f'      <div class="plate" aria-hidden="true">{plate}</div>\n'
            f'      <div class="body">\n'
            f'        <p class="era">{html.escape(era)}</p>\n'
            f'        <h2>{html.escape(title)}</h2>\n'
            f'        <p class="blurb">{html.escape(blurb)}</p>\n'
            + (f'        <ul class="journeys" aria-label="Journeys">{journeys}</ul>\n' if journeys else "")
            + f'        <p class="facts">{len(d["places"])} places · {stops} stops on {len(d.get("journeys", []))} '
              f'journey{"" if len(d.get("journeys", [])) == 1 else "s"}</p>\n'
            + f'        <div class="tints" aria-hidden="true">{"".join(f"<span style=\"background: var(--{t})\"></span>" for t in tints)}</div>\n'
            f'      </div>\n    </a></li>')
    body = open(os.path.join(ROOT, "scripts", "templates", "maps-index.html"), encoding="utf-8").read()
    body = body.replace("{{CARDS}}", "\n".join(cards))
    with open(os.path.join(SITE, "maps", "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.STANDALONE.format(page=body))


MAPS = {"palestine": palestine_map, "palestine-history": palestine_history_map, "roman-empire": roman_map,
        "western-asia": western_asia_map, "exodus": exodus_map, "empires": empires_map, "kingdoms": kingdoms_map,
        "jerusalem": jerusalem_map}


def main():
    wanted = sys.argv[1:] or list(MAPS)
    for name in wanted:
        data, page = MAPS[name]()
        write_map(data, page)
        extra = ""
        for J in data.get("journeys", []):
            shown = sum(1 + len(s.get("also", [])) for s in J["stops"] if "x" in s)
            extra += f"; {J['short']}: {shown} of {len(J['stops'])} stops shown"
        lands = len(data["territories"]) or sum(len(P["territories"]) for P in data.get("periods", []))
        print(f"Map No. {page['NO']}, {page['H1']}: {len(data['places'])} places, {lands} territories{extra}")
    write_index()


if __name__ == "__main__":
    main()
