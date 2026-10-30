"""The web of Scripture in three dimensions: the nodes and links of data/graph.json laid out
again in space, for web3d.html.

    python3 scripts/web3d.py            (after connections.py, which writes data/graph.json)
    python3 scripts/web3d.py page       (only the page, from scripts/templates/web3d.html)

Writes  web3d.html        the page
        data/web3d.json   {"s": scale, "p": [x0, y0, z0, x1, ...]}: each node's place as whole
                          numbers, in the order of data/graph.json, which the page also loads.

The layout is the graph page's (scripts/graph.py) in one more dimension: links pull their ends
to a set distance, every node pushes every other away (on a mesh with FFTs, with the exact push
between near neighbours), and a little gravity holds the whole together. It starts from a ball
with the chapters wound round it in order, from Genesis at the top to Revelation at the bottom,
and everything else at the middle of its chapters, so the Bible's order still shows in the end.
"""

import json
import math
import os
import sys

import numpy as np
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = ["xref", "seq", "names", "together", "family", "event"]
LINK_STRENGTH = {"xref": 2.5, "seq": 3.0, "names": 1.0, "together": 0.6, "family": 1.0, "event": 0.8}


def unpack(D):
    """The links as arrays (a, b, type), as graph.html unpacks them."""
    nc = D["kinds"][0]
    A, B, T = list(range(nc - 1)), list(range(1, nc)), [1] * (nc - 1)
    for t, flat in D["links"].items():
        ti = TYPES.index(t)
        a = b = 0
        for j in range(0, len(flat), 2):
            if j and flat[j] == 0:
                b += flat[j + 1]
            else:
                a += flat[j]
                b = a + flat[j + 1]
            A.append(a); B.append(b); T.append(ti)
    return np.array(A), np.array(B), np.array(T)


def ball(nc, n, a, b, seed=1):
    """Chapters on a sphere in order, top to bottom, winding round as they go; everyone else at
    the middle of the chapters they link to, a little way in."""
    R = 600.0
    pos = np.zeros((n, 3))
    k = np.arange(nc)
    z = 1 - 2 * (k + 0.5) / nc
    r = np.sqrt(1 - z ** 2)
    th = k * math.pi * (3 - math.sqrt(5))
    pos[:nc] = R * np.c_[r * np.cos(th), z, r * np.sin(th)]
    near = [[] for _ in range(n)]
    for x, y in zip(a, b):
        if x < nc <= y:
            near[y].append(x)
        elif y < nc <= x:
            near[x].append(y)
    rng = np.random.default_rng(seed)
    for i in range(nc, n):
        if near[i]:
            pos[i] = pos[near[i]].mean(0) * (0.75 + 0.1 * rng.random())
        else:
            pos[i] = rng.normal(0, R * 0.2, 3)
    return pos


def mesh_push(pos, G=64, soft=1.5):
    """For each node, the sum over all others of (p_i - p_j) / |p_i - p_j|^2, on a G^3 mesh."""
    lo = pos.min(0) - 1e-6
    h = (pos.max(0) - lo).max() * (1 + 2 / G) / G + 1e-9
    g = (pos - lo) / h
    i0 = np.clip(np.floor(g).astype(int), 0, G - 2)
    f = g - i0
    corners = []
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                corners.append((dx, dy, dz, w))
    rho = np.zeros((2 * G,) * 3)
    for dx, dy, dz, w in corners:
        np.add.at(rho, (i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz), w)
    k = np.arange(2 * G)
    k[k >= G] -= 2 * G
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    # The push in 3D falls off as 1/r, like the page's 2D push, so the web keeps its shape.
    r2 = kx ** 2 + ky ** 2 + kz ** 2 + soft ** 2
    R = np.fft.rfftn(rho)
    out = np.zeros_like(pos)
    for c, kc in enumerate((kx, ky, kz)):
        fc = np.fft.irfftn(R * np.fft.rfftn(kc / r2), s=rho.shape, axes=(0, 1, 2))[:G, :G, :G] / h
        for dx, dy, dz, w in corners:
            out[:, c] += w * fc[i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz]
    return out


def layout(pos, a, b, mult, iters=300, distance=24.0, charge=40.0, gravity=0.02, near=60.0):
    n = len(pos)
    deg = np.bincount(np.concatenate([a, b]), minlength=n).astype(float)
    strength = mult / np.minimum(deg[a], deg[b])
    bias = deg[a] / (deg[a] + deg[b])
    vel = np.zeros_like(pos)
    alpha, decay = 1.0, 1 - 0.001 ** (1 / iters)
    for _ in range(iters):
        alpha -= alpha * decay
        x = pos[b] + vel[b] - pos[a] - vel[a]
        length = np.sqrt((x ** 2).sum(1)) + 1e-9
        s = ((length - distance) / length * alpha * strength)[:, None] * x
        for c in range(3):
            vel[:, c] -= np.bincount(b, s[:, c] * bias, n)
            vel[:, c] += np.bincount(a, s[:, c] * (1 - bias), n)
        vel += mesh_push(pos) * charge * alpha
        pairs = cKDTree(pos).query_pairs(near, output_type="ndarray")
        if len(pairs):
            d = pos[pairs[:, 1]] - pos[pairs[:, 0]]
            push = d / ((d ** 2).sum(1) + 1.0)[:, None] * charge * alpha
            for c in range(3):
                vel[:, c] -= np.bincount(pairs[:, 0], push[:, c], n)
                vel[:, c] += np.bincount(pairs[:, 1], push[:, c], n)
        vel -= pos * gravity * alpha
        vel *= 0.6
        pos = pos + vel
        pos -= pos.mean(0)
    return pos


def page():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import webpages
    src = open(os.path.join(ROOT, "scripts", "templates", "web3d.html"), encoding="utf-8").read()
    with open(os.path.join(ROOT, "web3d.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.document(src.replace("<!-- APPBAR -->", webpages.appbar("web3d.html")), colors=("#05070d", "#05070d")))


def main():
    page()
    if sys.argv[1:] == ["page"]:
        print("web3d.html")
        return
    D = json.load(open(os.path.join(ROOT, "data", "graph.json"), encoding="utf-8"))
    nc = D["kinds"][0]
    n = sum(D["kinds"])
    a, b, t = unpack(D)
    mult = np.array([LINK_STRENGTH[TYPES[x]] for x in t])
    pos = layout(ball(nc, n, a, b), a, b, mult)
    # Turn it so Genesis is above Revelation, the way it started.
    up = pos[:nc // 3].mean(0) - pos[-nc // 3:].mean(0)
    up /= np.linalg.norm(up)
    y = np.array([0.0, 1.0, 0.0])
    v, c = np.cross(up, y), float(up @ y)
    if np.linalg.norm(v) > 1e-9:
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rot = np.eye(3) + vx + vx @ vx / (1 + c)
        pos = pos @ rot.T
    # Loosen the crowded middle and draw in the far strays: each node's distance from the middle
    # goes to the power 0.7, so the core opens out and the web keeps a rounder shape.
    r = np.sqrt((pos ** 2).sum(1))[:, None] + 1e-9
    r0 = np.percentile(r, 50)
    pos = pos / r * r0 * (r / r0) ** 0.7
    scale = 2000 / np.abs(pos).max()
    out = {"s": round(1 / scale, 6), "p": [int(round(x)) for x in (pos * scale).ravel()]}
    with open(os.path.join(ROOT, "data", "web3d.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, separators=(",", ":"))
        f.write("\n")
    print(f"web3d.json: {n} nodes, {len(a)} links")


if __name__ == "__main__":
    main()
