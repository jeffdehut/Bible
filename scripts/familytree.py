"""Lay out the whole family of Adam for the genealogy viewer, once, when the site is built.

Time runs from left to right: each generation is a column, and each person a row in it. The
line from Adam to Jesus runs straight along one row, and every parent sits level with one
child (the next in that line, or else the child with the most descendants), so long lines of
descent run straight and the branches leave them. Branches are packed as close as their
outlines allow (the tidy-tree algorithm of Walker, as improved by Buchheim, Jünger and
Leipert), so no two lines of descent cross.

The tree follows each person's father, or their mother when no father is recorded. A wife
whose own family is recorded, or who has none, is set beside her husband, with her family
above her; the links to the children she bore are drawn separately. Families joined to
Adam's only by a marriage (Saul's, through Michal) are set beside it the same way.
"""

import collections


def components(people):
    """Each person's family: the people linked to them by parents and children."""
    kids = collections.defaultdict(list)
    for i, p in enumerate(people):
        for j, _, _ in p.get("p", []):
            kids[j].append(i)
    comp = {}
    for s in range(len(people)):
        if s in comp:
            continue
        comp[s], stack = s, [s]
        while stack:
            x = stack.pop()
            for y in [q[0] for q in people[x].get("p", [])] + kids[x]:
                if y not in comp:
                    comp[y] = s
                    stack.append(y)
    return comp


class Node:
    __slots__ = ("i", "children", "parent", "number", "x", "mod", "thread", "ancestor", "change", "shift",
                 "heir", "virtual", "depth", "weight")

    def __init__(self, i, virtual=False):
        self.i, self.children, self.parent, self.number = i, [], None, 1
        self.x = self.mod = self.change = self.shift = 0.0
        self.thread, self.ancestor, self.heir, self.virtual = None, self, None, virtual
        self.depth = self.weight = 0

    def left(self):
        return self.thread or (self.children[0] if self.children else None)

    def right(self):
        return self.thread or (self.children[-1] if self.children else None)

    def lbrother(self):
        return self.parent.children[self.number - 2] if self.parent and self.number > 1 else None

    def lmost_sibling(self):
        return self.parent.children[0] if self.parent and self.number > 1 else None


# ---- Walker's algorithm in linear time (Buchheim, Jünger and Leipert 2002), with each
# parent level with its heir rather than centred on its children.

def _firstwalk(v, gap):
    if not v.children:
        w = v.lbrother()
        v.x = w.x + gap(w, v) if w else 0.0
        return
    default = v.children[0]
    for w in v.children:
        _firstwalk(w, gap)
        default = _apportion(w, default, gap)
    _execute_shifts(v)
    anchor = v.heir.x if v.heir else (v.children[0].x + v.children[-1].x) / 2
    w = v.lbrother()
    if w:
        v.x = w.x + gap(w, v)
        v.mod = v.x - anchor
    else:
        v.x = anchor


def _apportion(v, default, gap):
    w = v.lbrother()
    if w is None:
        return default
    vir = vor = v
    vil, vol = w, v.lmost_sibling()
    sir = sor = v.mod
    sil, sol = vil.mod, vol.mod
    while vil.right() and vir.left():
        vil, vir, vol, vor = vil.right(), vir.left(), vol.left(), vor.right()
        vor.ancestor = v
        shift = (vil.x + sil) - (vir.x + sir) + gap(vil, vir)
        if shift > 0:
            a = vil.ancestor if vil.ancestor.parent is v.parent else default
            _move_subtree(a, v, shift)
            sir += shift
            sor += shift
        sil += vil.mod
        sir += vir.mod
        sol += vol.mod
        sor += vor.mod
    if vil.right() and not vor.right():
        vor.thread = vil.right()
        vor.mod += sil - sor
    else:
        if vir.left() and not vol.left():
            vol.thread = vir.left()
            vol.mod += sir - sol
        default = v
    return default


def _move_subtree(wl, wr, shift):
    n = wr.number - wl.number
    wr.change -= shift / n
    wr.shift += shift
    wl.change += shift / n
    wr.x += shift
    wr.mod += shift


def _execute_shifts(v):
    shift = change = 0.0
    for w in reversed(v.children):
        w.x += shift
        w.mod += shift
        change += w.change
        shift += w.shift + change


def _secondwalk(root):
    out, stack = {}, [(root, 0.0)]
    while stack:
        v, m = stack.pop()
        out[v.i] = (v.depth, v.x + m)
        for w in v.children:
            stack.append((w, m + v.mod))
    return out


def layout(people, root, line, order_key):
    """Positions for the family of `root` and the families married into it.

    people     the genealogy's people: "p" [[parent, "f"|"m"|"", flags]], "sp" [spouses]
    root       Adam's index; line: the line from Adam to Jesus, as indices
    order_key  sorts siblings (by first mention, so the eldest usually comes first)

    Returns {index: (generation, row)}, the rows whole numbers with the line of Jesus at 0,
    and the set of people placed beside a spouse rather than under a parent."""
    comp = components(people)
    main = comp[root]
    families = {main}
    for i, c in comp.items():
        if c == main:
            for j in people[i].get("sp", []):
                families.add(comp[j])
    members = [i for i, c in comp.items() if c in families]
    inside = set(members)

    def primary(i):
        ps = [q for q in people[i].get("p", []) if q[0] in inside and comp[q[0]] == comp[i]]
        f = [q for q in ps if q[1] == "f"]
        return (f or ps or [None])[0]

    nodes = {i: Node(i) for i in members}
    for i in sorted(members, key=order_key):
        q = primary(i)
        if q:
            nodes[q[0]].children.append(nodes[i])
            nodes[i].parent = nodes[q[0]]

    def walk_down(v, depth):
        stack = [(v, depth)]
        while stack:
            n, d = stack.pop()
            n.depth = d
            stack.extend((c, d + 1) for c in n.children)

    roots = [nodes[i] for i in members if nodes[i].parent is None]
    placed = {root}
    walk_down(nodes[root], 0)
    beside = set()

    def in_tree(v):
        while v.parent:
            v = v.parent
        return v.i in placed

    def subtree(v):
        out, stack = [], [v]
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(n.children)
        return out

    # Hang each other tree beside the person it married into, until none is left.
    pending = [r for r in roots if r.i != root]
    while pending:
        progress = False
        for r in list(pending):
            anchor = None
            for m in subtree(r):
                # m bore a child in the tree: set m beside the child's father.
                for c in members:
                    if nodes[c].parent is not None and in_tree(nodes[c]) and \
                            any(q[0] == m.i for q in people[c].get("p", [])) and nodes[c].parent is not m:
                        anchor = (m, nodes[c].parent)
                        break
                if anchor:
                    break
                spouse = next((nodes[j] for j in people[m.i].get("sp", []) if j in nodes and in_tree(nodes[j])), None)
                if spouse:
                    anchor = (m, spouse)
                    break
            if not anchor:
                continue
            m, spouse = anchor
            dm = 0
            v = m
            while v is not r:
                v, dm = v.parent, dm + 1
            # The tree's root goes in the generation above its member's spouse's, by dm steps:
            # under the spouse's ancestor one generation further up, next to the spouse's line.
            up, toward = spouse, spouse
            for _ in range(dm + 1):
                if up.parent is None:
                    break
                toward, up = up, up.parent
            if up is toward:          # no ancestor that far up: hang it from the top
                up = nodes[root]
                toward = up.children[0]
            k = up.children.index(toward) + 1
            up.children.insert(k, r)
            r.parent, r.virtual = up, True
            walk_down(r, up.depth + 1)
            beside.add(r.i)
            placed.add(r.i)
            pending.remove(r)
            progress = True
        if not progress:
            break

    # Number siblings, weigh subtrees, and choose each parent's heir.
    on_line = {i: k for k, i in enumerate(line)}
    order = []
    stack = [nodes[root]]
    while stack:
        v = stack.pop()
        order.append(v)
        for k, c in enumerate(v.children):
            c.number = k + 1
        stack.extend(v.children)
    for v in reversed(order):
        v.weight = 1 + sum(c.weight for c in v.children if not c.virtual)
        real = [c for c in v.children if not c.virtual]
        if real:
            nxt = next((c for c in real if c.i in on_line and v.i in on_line), None)
            v.heir = nxt or max(real, key=lambda c: c.weight)

    def gap(a, b):
        return 1.0

    _firstwalk(nodes[root], gap)
    pos = _secondwalk(nodes[root])
    base = pos[root][1]
    pos = {i: (d, round(y - base)) for i, (d, y) in pos.items()}
    left = [i for i in members if i not in pos]
    return pos, beside, left

