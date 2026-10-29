"""Family relationships from STEPBible TIPNR, for the person notes in connections/.

TIPNR's header line for each person has columns for parents ("Father + Mother"), siblings,
partners and offspring, each a list of TIPNR ids. An id may carry flags:
  (?)  the identification is uncertain
  (a)  an ancestor rather than the immediate parent or child
  (d)  a group descended from this person
  (f)  the founder of a place or group
Relationships are recorded on both sides in TIPNR, but not always consistently, so the
two directions are merged here.
"""

import collections
import re

ITEM = re.compile(r"([^\s,+()]+@[^\s,+()]+)\s*((?:\([adf?]{1,2}\))*)")
FLAG_TEXT = {"?": "uncertain", "a": "ancestor", "d": "descendants", "f": "founder"}


def parse_items(text):
    return [(i, frozenset(re.findall(r"[adf?]", flags))) for i, flags in ITEM.findall(text or "")]


# TIPNR fills two gaps in the genealogies with people of its own making: nine generations
# between Matthan and Jacob in Matthew 1:15, "inferred from the number of generations in Luke 3",
# and four between Ithamar and Eli, "inferred from 1 Kings 2:27". No verse names or counts them,
# so they are left out and the named ends joined as the text has them. Matthew 1:15 calls Matthan
# the father of Jacob, so that link is a father's. No verse says how many generations came
# between Ithamar and Eli, so that one is an ancestor's (a), as is any other gap TIPNR fills.
STATED_AS_FATHER = {"Mat.1.15"}


def _bridge_inferred(family, inferred):
    """Join the named people on either side of each run of inferred placeholders."""
    def named_end(pid, step, flags):
        while pid in inferred:
            nxt = step(pid)
            if nxt is None:
                return None, flags
            pid, more = nxt
            flags |= more
        return pid, flags

    def up(pid):
        return family.get(pid, {}).get("father") or family.get(pid, {}).get("mother")

    def down(pid):
        kids = family.get(pid, {}).get("offspring") or []
        return kids[0] if kids else None

    for pid, fam in family.items():
        if pid in inferred:
            continue
        for role in ("father", "mother"):
            if fam[role] and fam[role][0] in inferred:
                gap = fam[role][0].split("@", 1)[1]
                anc, flags = named_end(fam[role][0], up, set(fam[role][1]))
                if gap not in STATED_AS_FATHER:
                    flags.add("a")
                fam[role] = (anc, frozenset(flags)) if anc else None
        kids = []
        for cid, flags in fam["offspring"]:
            if cid in inferred:
                gap = cid.split("@", 1)[1]
                desc, flags = named_end(cid, down, set(flags))
                if gap not in STATED_AS_FATHER:
                    flags.add("a")
                if desc:
                    kids.append((desc, frozenset(flags)))
            else:
                kids.append((cid, flags))
        fam["offspring"] = kids
        for key in ("siblings", "partners"):
            fam[key] = [(o, f) for o, f in fam[key] if o not in inferred]
    for pid in inferred:
        family.pop(pid, None)


def load_family(path):
    """({tipnr id: {"sex", "tribe", "father", "mother", "siblings", "partners", "offspring"}},
    {the ids of TIPNR's inferred placeholders, which are left out: see _bridge_inferred})"""
    family, kind, inferred = {}, None, set()
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("$=========="):
            kind = line.strip("$= \t").split()[0] if line.strip("$= \t") else None
            continue
        f = line.split("\t")
        if kind != "PERSON(s)" or line.startswith(("–", "@")) or "@" not in f[0] or "=" not in f[0]:
            continue
        f += [""] * (9 - len(f))
        father_txt, _, mother_txt = f[2].partition("+")
        father, mother = parse_items(father_txt), parse_items(mother_txt)
        uid = f[0].split("=")[0].strip()
        if uid.startswith("Unnamed#") and "inferred from" in f[7]:
            inferred.add(uid)
        family[uid] = {
            "sex": f[8].strip(),
            "tribe": f[6].strip() if f[6].strip() not in ("", ">") else None,
            "father": father[0] if father else None,
            "mother": mother[0] if mother else None,
            "siblings": parse_items(f[3]),
            "partners": parse_items(f[4]),
            "offspring": parse_items(f[5]),
        }
    _bridge_inferred(family, inferred)
    return family, inferred


class Genealogy:
    """Family graph over the entities that have notes (indexes into the entity list)."""

    def __init__(self, entities, family):
        index = {e["id"]: i for i, e in enumerate(entities)}
        self.entities = entities
        self.sex = {}
        self.tribe = {}
        # (parent, child) -> {"role": "father"/"mother"/None, "flags": set}
        self.parent_edges = collections.defaultdict(lambda: {"role": None, "flags": set()})
        self.siblings = collections.defaultdict(dict)   # i -> {j: flags}
        self.partners = collections.defaultdict(dict)
        self.unresolved = 0
        for uid, fam in family.items():
            if uid not in index:
                continue
            i = index[uid]
            self.sex[i] = fam["sex"]
            self.tribe[i] = fam["tribe"]
            for role in ("father", "mother"):
                if fam[role]:
                    pid, flags = fam[role]
                    if pid in index:
                        edge = self.parent_edges[(index[pid], i)]
                        edge["role"] = role
                        edge["flags"] |= flags
                    else:
                        self.unresolved += 1
            for cid, flags in fam["offspring"]:
                if cid in index:
                    self.parent_edges[(i, index[cid])]["flags"] |= flags
                else:
                    self.unresolved += 1
            for key, rel in (("siblings", self.siblings), ("partners", self.partners)):
                for oid, flags in fam[key]:
                    if oid in index and index[oid] != i:
                        j = index[oid]
                        rel[i][j] = rel[i].get(j, frozenset()) | flags
                        rel[j][i] = rel[j].get(i, frozenset()) | flags
                    elif oid not in index:
                        self.unresolved += 1
        # Fill in the parent's role from their sex when only the offspring list named them.
        for (p, c), edge in self.parent_edges.items():
            if edge["role"] is None:
                edge["role"] = {"Male": "father", "Female": "mother"}.get(self.sex.get(p))
        self.parents = collections.defaultdict(list)
        self.children = collections.defaultdict(list)
        for (p, c), edge in sorted(self.parent_edges.items()):
            self.parents[c].append((p, edge))
            self.children[p].append((c, edge))

    def father(self, i):
        """The direct father (not an ancestor link), if recorded."""
        for p, edge in self.parents[i]:
            if edge["role"] == "father" and "a" not in edge["flags"]:
                return p
        return None

    def paternal_line(self, i, limit=200):
        """[root, ..., i] following fathers upward."""
        line, seen = [i], {i}
        while len(line) < limit:
            f = self.father(line[-1])
            if f is None or f in seen:
                break
            line.append(f)
            seen.add(f)
        return line[::-1]

    def families(self):
        """Connected groups of people linked as parent and child, largest first.

        Returns [(root, members, generation)] where root is the earliest ancestor (the
        member with the most descendants) and generation[i] counts direct parent-child
        steps down from root (ancestor links count as one step but are marked).
        """
        adj = collections.defaultdict(set)
        for (p, c) in self.parent_edges:
            adj[p].add(c)
            adj[c].add(p)
        seen, groups = set(), []
        for start in sorted(adj):
            if start in seen:
                continue
            comp, stack = set(), [start]
            while stack:
                n = stack.pop()
                if n in comp:
                    continue
                comp.add(n)
                stack.extend(adj[n] - comp)
            seen |= comp
            groups.append(comp)
        out = []
        for comp in groups:
            roots = [n for n in comp if not self.parents[n]]
            root = max(roots or comp, key=lambda n: (self.descendant_count(n), -n))
            out.append((root, comp, self.generations(root, comp)))
        return sorted(out, key=lambda g: (-len(g[1]), g[0]))

    def descendant_count(self, i):
        seen, stack = set(), [c for c, _ in self.children[i]]
        while stack:
            n = stack.pop()
            if n not in seen:
                seen.add(n)
                stack.extend(c for c, _ in self.children[n])
        return len(seen)

    def generations(self, root, comp):
        """Generation numbers within a family group, counted along the longest line of
        parents above each person, so they agree with the person's own line of descent.

        People with no recorded parents start at generation 1; those who only marry into
        the family (no parents, but children here) are placed one generation above their
        earliest child.
        """
        depth = {}

        def d(n, path):
            if n not in depth:
                ps = [p for p, _ in self.parents[n] if p in comp and p not in path]
                depth[n] = 1 + max(d(p, path | {n}) for p in ps) if ps else 1
            return depth[n]

        for n in sorted(comp):
            d(n, frozenset())
        for n in sorted(comp):
            if n != root and not any(p in comp for p, _ in self.parents[n]):
                kids = [depth[c] for c, _ in self.children[n] if c in comp]
                if kids:
                    depth[n] = max(1, min(kids) - 1)
        return depth


def flag_note(flags):
    words = [FLAG_TEXT[f] for f in sorted(flags) if f in FLAG_TEXT]
    return f" ({', '.join(words)})" if words else ""
