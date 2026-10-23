"""Dates for the timeline in connections/, from Theographic Bible Metadata (CC BY-SA 4.0).

Theographic (https://github.com/robertrouse/theographic-bible-metadata) supplies:
  - verse years: the marginal dates of the Treasury of Scripture Knowledge, which follow
    Archbishop Ussher, the chronology Adams used for his Synchronological Chart
  - 450 events, and birth/death years for the patriarchs, judges and kings, following
    Floyd Nolen Jones, who builds on Ussher and mostly agrees with him to within a year

All years are astronomical (ISO 8601): 0 = 1 BC, -4003 = 4004 BC.
"""

import collections
import json
import os
import re
import subprocess

THEOGRAPHIC_REPO = "https://github.com/robertrouse/theographic-bible-metadata"
THEOGRAPHIC_COMMIT = "744355c7a5f38efd407bc67a5257c99aca9532bc"  # 22 Oct 2026

# Anchor dates that identify Ussher's chronology (as used by Adams), checked against the
# verse years. Astronomical years.
USSHER_ANCHORS = [
    ("Creation", "Gen.1.1", -4003),
    ("The Flood", "Gen.7.11", -2347),
    ("Terah dies; Abram leaves Haran", "Gen.11.32", -1920),
    ("The Exodus", "Exod.12.41", -1490),
    ("Temple begun", "1Kgs.6.1", -1011),
]


def year_label(y):
    """Astronomical year -> '4004 BC' / 'AD 30'."""
    return f"{1 - y} BC" if y <= 0 else f"AD {y}"


def century_of(y):
    """Astronomical year -> signed century number: -41 = 41st century BC, 1 = 1st century AD."""
    return -((-y) // 100 + 1) if y <= 0 else (y - 1) // 100 + 1


def century_label(c):
    n = abs(c)
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix} century {'BC' if c < 0 else 'AD'}"


def fetch(cache):
    out = os.path.join(cache, "theographic")
    if not os.path.isdir(out):
        print(f"Cloning {THEOGRAPHIC_REPO}")
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", THEOGRAPHIC_REPO, out], check=True)
    subprocess.run(["git", "-C", out, "checkout", "-q", THEOGRAPHIC_COMMIT], check=True)
    return os.path.join(out, "json")


def parse_start(s):
    """events.startDate: '-4003' or '0030-04-04' -> astronomical year."""
    m = re.fullmatch(r"(-?\d+)(?:-\d\d-\d\d)?", s.strip())
    return int(m[1])


class Chronology:
    def __init__(self, json_dir, vers):
        load = lambda name: json.load(open(os.path.join(json_dir, name + ".json"), encoding="utf-8"))
        verses = load("verses")
        self.osis_of = {}            # Theographic verse record id -> our (osis, c, v)
        self.verse_year = {}         # our (osis, c, v) -> Ussher year
        for r in verses:
            f = r["fields"]
            book, c, v = f["osisRef"].split(".")
            ref = vers.hebrew(book, int(c), int(v))
            self.osis_of[r["id"]] = ref
            if f.get("yearNum") is not None:
                self.verse_year.setdefault(ref, int(f["yearNum"]))
        people = load("people")
        self.people = {r["id"]: r["fields"] for r in people}
        self.places = {r["id"]: r["fields"] for r in load("places")}
        self.events = []
        for r in load("events"):
            f = r["fields"]
            self.events.append({
                "tid": r["id"], "id": f["eventID"], "title": f["title"].strip(),
                "year": parse_start(f["startDate"]), "date": f["startDate"],
                "duration": f.get("duration"), "sort": f.get("sortKey", 0),
                "participants": f.get("participants", []), "locations": f.get("locations", []),
                "verses": [self.osis_of[v] for v in f.get("verses", []) if v in self.osis_of],
                "predecessor": f.get("predecessor", []), "part_of": f.get("partOf", []),
            })
        self.events.sort(key=lambda e: (e["sort"], e["id"]))

    def anchors(self):
        """[(label, expected, found)] for the Ussher anchor dates."""
        out = []
        for label, ref, expected in USSHER_ANCHORS:
            book, c, v = ref.split(".")
            out.append((label, expected, self.verse_year.get((book, int(c), int(v)))))
        return out

    def crosswalk(self, entities, kind="person"):
        """Theographic person (or place) id -> entity index, by name and shared verses.

        A Theographic record is matched to the TIPNR person or place with the same name (or
        alias) whose verses overlap most. Ties and zero overlap are left unmatched.
        """
        records = self.people if kind == "person" else self.places
        by_name = collections.defaultdict(list)
        for i, e in enumerate(entities):
            if e["kind"] != kind:
                continue
            for n in [e["name"]] + e["aliases"]:
                by_name[n.lower()].append(i)
        match, ambiguous = {}, 0
        for tid, f in records.items():
            refs = {self.osis_of[v] for v in f.get("verses", []) if v in self.osis_of}
            if kind == "person":
                names = [f["name"]] + [s.strip() for s in (f.get("alsoCalled") or "").split(",") if s.strip()]
            else:
                names = [f.get(k) for k in ("displayTitle", "esvName", "kjvName") if f.get(k)]
            cands = {i for n in names for i in by_name.get(n.lower(), [])}
            scored = sorted(((len(refs & (entities[i]["verses"] | entities[i]["mentioned"])), i) for i in cands),
                            reverse=True)
            if scored and scored[0][0] > 0 and (len(scored) == 1 or scored[0][0] > scored[1][0]):
                match[tid] = scored[0][1]
            elif len(scored) > 1 and scored[0][0] > 0:
                ambiguous += 1
        return match, ambiguous
