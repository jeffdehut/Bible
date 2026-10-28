"""Build the Bible maps in site/maps/.

    python3 scripts/maps.py

The maps are drawn in the manner of the Eilers Sunday School wall maps (see ROADMAP.md),
from open data only:
  - elevation: AWS Terrain Tiles (Mapzen terrarium encoding; SRTM, GMTED2010, ETOPO1),
    downloaded once into .cache/dem/
  - places: OpenBible.info Bible Geocoding Data (CC BY 4.0), cloned into .cache/openbible-geo/
  - tribal territories: allotted from the town lists of Joshua 13-19 and 21 (see territories())

Needs numpy, scipy and Pillow, unlike the other scripts, which use only the standard library.

Writes  site/maps/data/kingdoms.json   every layer of Map No. 7 as SVG path data and points
        site/maps/kingdoms.html        site/src/map-kingdoms.html with its data inlined

Map No. 7, The Kingdoms of Judah and Israel, is the style study: a redrawing of the Eilers
map of the same name.
"""

import json
import math
import os
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
SITE = os.path.join(ROOT, "site")
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
    move, then relative steps on a grid of 10^-digits units."""
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


def territories(sheet, elev, wet, flow, seed_list, step=4, cap_km=30):
    """Allot every land cell to the territory whose towns are nearest, measured on foot.

    Distance runs over a grid `step` times coarser than the sheet. Lakes cannot be crossed;
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
    # The Jordan: follow the drainage from the springs at Dan to the Dead Sea.
    jordan = np.zeros((ny, nx), bool)
    x, y = sheet.xy(35.651, 33.248)
    i = int(y / (sheet.res * fstep)) * fx + int(x / (sheet.res * fstep))
    while i >= 0:
        r, c = divmod(i, fx)
        rr, cc = r // k, c // k
        if rr < ny and cc < nx:
            jordan[rr, cc] = True
        i = recv[i]
    jordan = ndimage.binary_dilation(jordan, iterations=1)
    river[jordan] = 60
    names = list(NEIGHBOURS) + [t[0] for t in TRIBES]
    index = {n: i for i, n in enumerate(names)}
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
        if d > dist[i] or d > cap_km:
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
    owner[dist > cap_km] = -1
    owner = owner.reshape(ny, nx)
    # Tidy: a majority filter, then keep only each territory's largest piece, giving the
    # rest (towns of one list inside another's land) to the nearest other territory.
    owner = ndimage.generic_filter(owner, lambda v: np.bincount(v.astype(int) + 1).argmax() - 1, size=5, mode="nearest")
    for t in range(len(names)):
        lab, n = ndimage.label(owner == t)
        if n > 1:
            sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
            keep = int(np.argmax(sizes)) + 1
            owner[(lab > 0) & (lab != keep)] = -2
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
BOOK_ORDER = {b: i for i, b in enumerate(["Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg",
    "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps",
    "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad",
    "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"])}
OSIS_LABEL = {"Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers",
              "Deut": "Deuteronomy", "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth",
              "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Kings", "2Kgs": "2 Kings",
              "1Chr": "1 Chronicles", "2Chr": "2 Chronicles", "Ezra": "Ezra", "Neh": "Nehemiah",
              "Esth": "Esther", "Job": "Job", "Ps": "Psalm", "Prov": "Proverbs",
              "Eccl": "Ecclesiastes", "Song": "Song of Songs", "Isa": "Isaiah", "Jer": "Jeremiah",
              "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel", "Hos": "Hosea",
              "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah",
              "Mic": "Micah", "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah",
              "Hag": "Haggai", "Zech": "Zechariah", "Mal": "Malachi"}


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


def follow(lines, lon, lat, sheet, length_km):
    """The stretch of the nearest polyline (km units) around a point, about `length_km` long."""
    x, y = sheet.xy(lon, lat)
    best = None
    for ln in lines:
        d = np.hypot(ln[:, 0] - x, ln[:, 1] - y)
        i = int(np.argmin(d))
        if best is None or d[i] < best[0]:
            best = (d[i], ln, i)
    if best is None or best[0] > 6:
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


def kingdoms_map():
    """All the layers of Map No. 7, as a dict ready for JSON."""
    import collections
    sheet = Sheet(*SHEET7, res=0.13)
    elev = elevation(sheet, 10)
    w = water(sheet, elev)
    lakes = w["Sea of Galilee"] | w["Dead Sea"] | w["Lake Huleh"]
    wet = w["sea"] | lakes
    land = ~w["sea"]
    flow = drainage(sheet, elev, w["sea"] | w["Dead Sea"], 2)
    all_places = places()
    terr, names = territories(sheet, elev, wet, flow + (2,), seeds(all_places))
    ours = our_spellings()
    res = sheet.res
    d = lambda lines, close=False, digits=2: path_d(lines, res, digits, close)
    groups = {n: n for n in NEIGHBOURS}
    groups.update({t[0]: t[1] for t in TRIBES})

    out = {"sheet": {"width": round(sheet.width, 2), "height": round(sheet.height, 2),
                     "west": sheet.west, "east": sheet.east, "south": sheet.south,
                     "north": sheet.north, "kx": sheet.kx, "ky": sheet.ky}}
    layers = out["layers"] = {}
    layers["land"] = d(outlines(land), True)
    layers["coast"] = d(outlines(land, closed=False))
    layers["ripples"] = d(ripples(sheet, land, [0.45, 1.0, 1.7, 2.6, 3.7, 5.0]), digits=1)
    layers["lakes"] = d(outlines(lakes, smooth=0.8), True)
    layers["lakeRipples"] = d(ripples(sheet, ~lakes, [0.3, 0.7]), digits=1)

    # Rivers, in three weights by drainage area.
    area, recv, shape = flow
    river_lines = rivers(sheet, area, recv, shape, 2, wet, 150)
    smooth_rivers = [(chaikin(densify(simplify(p, 1.2), 4), 2), a) for p, a in river_lines]
    layers["rivers"] = [d([p for p, a in smooth_rivers if lo <= a < hi], digits=1)
                        for lo, hi in ((0, 1000), (1000, 8000), (8000, 1e12))]

    # Hachures, in four weights.
    hs = hachures(sheet, elev, wet, spacing_km=0.9, min_slope=5)
    layers["hachures"] = [d([p for p, wt in hs if k / 4 <= wt < (k + 1) / 4 or (k == 3 and wt >= 1)], digits=1)
                          for k in range(4)]

    # Territories: fills, then borders drawn once each, between nations or between tribes.
    terrs = []
    for i, n in enumerate(names):
        m = terr == i
        if not m.any():
            continue
        line, width = spine(m, sheet)
        terrs.append({"name": n, "group": groups[n], "tint": TINTS[groups[n]],
                      "d": d(outlines(m, smooth=1.5), True), "spine": line, "width": round(width, 1)})
    out["territories"] = terrs
    borders = {"nation": [], "tribe": []}
    for i, n in enumerate(names):
        m = terr == i
        if not m.any():
            continue
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
    layers["borders"] = {k: d(v, digits=1) for k, v in borders.items()}

    # Kingdom names along the length of each kingdom west of the Jordan.
    kingdoms = []
    for k in ("Israel", "Judah"):
        west = [t[0] for t in TRIBES if t[1] == k and t[0] not in ("Reuben", "Gad", "Manasseh (east)")]
        m = np.isin(terr, [names.index(t) for t in west])
        line, width = spine(m, sheet, trim=8)
        if k in KINGDOM_LINES:
            pts = np.array([sheet.xy(lon, lat) for lon, lat in KINGDOM_LINES[k]])
            t = np.linspace(0, 1, 16)
            seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
            seg /= seg[-1]
            line = np.round(np.c_[np.interp(t, seg, pts[:, 0]), np.interp(t, seg, pts[:, 1])], 2).tolist()
        kingdoms.append({"name": k.upper(), "spine": line, "width": round(width, 1)})
    out["kingdoms"] = kingdoms

    # Places: towns named in the Old Testament, one per site.
    by_site = collections.defaultdict(list)
    for p in all_places:
        if not (sheet.west <= p["lon"] <= sheet.east and sheet.south <= p["lat"] <= sheet.north):
            continue
        ot = [v for v in p["verses"] if v[0] in OT_BOOKS]
        if "settlement" not in p["types"] or not ot or p["score"] < 200:
            continue
        by_site[(round(p["lon"], 3), round(p["lat"], 3))].append((len(ot), p, ot))
    pl = []
    for site in by_site.values():
        site.sort(key=lambda t: -t[0])
        n_ot, p, ot = site[0]
        x, y = sheet.xy(p["lon"], p["lat"])
        r, c = int(y / res), int(x / res)
        t = terr[min(r, terr.shape[0] - 1), min(c, terr.shape[1] - 1)]
        first = min(ot, key=lambda v: (BOOK_ORDER[v[0]], v[1], v[2]))
        rec = {"n": display_name(p, ours), "x": round(x, 2), "y": round(y, 2),
               "v": sum(t[0] for t in site), "s": p["score"],
               "c": 1 if p["score"] >= 500 and p["exact"] else 0,
               "f": f"{OSIS_LABEL[first[0]]} {first[1]}:{first[2]}",
               "id": p["id"] + "/" + p["slug"]}
        if p["modern"]:
            rec["m"] = p["modern"]
        if t >= 0:
            rec["t"] = names[t]
        aka = sorted({display_name(q, ours) for _, q, _ in site[1:]} - {rec["n"]})
        if aka:
            rec["a"] = aka
        if p["name"] in CAPITALS:
            rec["cap"] = CAPITALS[p["name"]]
        pl.append(rec)
    pl.sort(key=lambda r: (-("cap" in r), -r["c"], -r["v"]))
    out["places"] = pl

    # Mountains, rivers, waters and regions.
    by_name = {p["name"]: p for p in all_places}
    feats = out["features"] = {"mountains": [], "rivers": [], "waters": [], "regions": []}
    for n in MOUNTAINS:
        p = by_name[n]
        x, y = sheet.xy(p["lon"], p["lat"])
        name = display_name(p, ours)
        name = name if name.startswith("Mount") else "Mount " + name
        feats["mountains"].append({"n": name.replace("Mount ", "Mt. "), "x": round(x, 2), "y": round(y, 2),
                                   "id": p["id"] + "/" + p["slug"]})
    km_lines = [p * res for p, _ in smooth_rivers]
    for n, length in RIVERS.items():
        p = by_name[n]
        line = follow(km_lines, p["lon"], p["lat"], sheet, length)
        if line:
            name = display_name(p, ours)
            feats["rivers"].append({"n": "River Jordan" if name == "Jordan" else name, "pts": line})
    for n, (text, a, b) in WATERS.items():
        feats["waters"].append({"n": text, "pts": [list(map(lambda v: round(v, 2), sheet.xy(*a))),
                                                   list(map(lambda v: round(v, 2), sheet.xy(*b)))]})
    for n, (lon, lat, text) in {"Galilee": (35.585, 32.80, "SEA OF KINNERETH"),
                                "Huleh": (35.612, 33.075, "Waters of Merom")}.items():
        x, y = sheet.xy(lon, lat)
        feats["waters"].append({"n": text, "x": round(x, 2), "y": round(y, 2), "lake": 1})
    for n in REGIONS:
        p = by_name[n]
        x, y = sheet.xy(p["lon"], p["lat"])
        feats["regions"].append({"n": display_name(p, ours), "x": round(x, 2), "y": round(y, 2)})
    return out


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import webpages
    data = kingdoms_map()
    os.makedirs(os.path.join(SITE, "maps", "data"), exist_ok=True)
    with open(os.path.join(SITE, "maps", "data", "kingdoms.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    src = os.path.join(SITE, "src", "map-kingdoms.html")
    body = open(src, encoding="utf-8").read().replace(
        "<!-- DATA -->", f'<script type="application/json" id="data">{webpages._dump(data)}</script>')
    with open(os.path.join(SITE, "maps", "kingdoms.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.STANDALONE.format(page=body))
    print(f"Map No. 7: {len(data['places'])} places, {len(data['territories'])} territories")


if __name__ == "__main__":
    main()
