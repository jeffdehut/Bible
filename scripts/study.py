"""Build the reader's topical index and Bible dictionary.

    python3 scripts/study.py

Reads   Nave's Topical Bible     CrossWire's "Nave" module (public domain, from CCEL's edition),
                                 downloaded once into .cache/crosswire/
        Easton's Bible Dictionary  Theographic's easton.json (CC BY-SA 4.0; Easton's text is
                                 public domain), cloned once into .cache/theographic/
        STEPBible TVTMS          to move both books' English (KJV) verse numbers to ours
Writes  data/bible/study/topics.json     every topic's name, in order: the index for search
        data/bible/study/dictionary.json every dictionary entry's name, in order
        data/bible/study/tNN.json        topics in chunks of 200, by number: each topic's
                                         subtopics, their references and "see also" topics
        data/bible/study/dNN.json        dictionary entries in chunks of 200, by number
        data/bible/study/NN-book.json    for each book, verse by verse, the topics and the
                                         dictionary entries that cite the verse ("t", "d"),
                                         and its cross-references ("x"), most-voted first
        OpenBible.info cross-references  (CC BY), those with at least 3 votes

References are written as "Gen.11.26" or "Gen.11.26-28" or "Gen.15" (a whole chapter), in
this repository's verse numbering (Hebrew numbering in the Old Testament).
"""

import collections
import html
import json
import os
import re
import struct
import sys
import zipfile
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402
import chronology                             # noqa: E402
import connections                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
OUT = os.path.join(ROOT, "data", "bible", "study")
NAVE_ZIP = "https://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/Nave.zip"
CHUNK = 200
OSIS = {osis for _, osis, _, _ in BOOKS}


# ---------------------------------------------------------------- references

class Refs:
    """Parse OSIS references and move them into our verse numbering."""

    def __init__(self, vers, texts):
        self.vers, self.texts = vers, texts
        self.last = {osis: collections.defaultdict(int) for osis in texts}
        for osis, verses in texts.items():
            for c, v in verses:
                self.last[osis][c] = max(self.last[osis][c], v)
        self.bad = 0

    def point(self, s):
        """'Gen.11.26' -> ('Gen', 11, 26); 'Gen.13' -> ('Gen', 13, None); None if not ours."""
        m = re.fullmatch(r"([1-3]?[A-Za-z]+)\.(\d+)(?:\.(\d+))?", s)
        if not m or m[1] not in OSIS:
            return None
        c, v = int(m[2]), int(m[3]) if m[3] else None
        if v is not None:
            _, c, v = self.vers.hebrew(m[1], c, v)
        if c not in self.last[m[1]] or (v is not None and v > self.last[m[1]][c]):
            return None
        return m[1], c, v

    def parse(self, ref):
        """'Gen.11.26-Gen.11.28' -> ('Gen.11.26-28', [verses]) or None."""
        a, _, b = ref.partition("-")
        p = self.point(a.strip())
        q = self.point(b.strip()) if b else p
        if not p or not q or q[0] != p[0]:
            self.bad += 1
            return None
        book, c, v = p
        if v is None:   # a whole chapter (or chapters)
            c2 = q[1]
            label = f"{book}.{c}" + (f"-{c2}" if c2 != c else "")
            verses = [(book, ch, vv) for ch in range(c, c2 + 1) for vv in range(1, self.last[book][ch] + 1)]
            return label, verses
        c2, v2 = q[1], q[2] or self.last[book][q[1]]
        if (c2, v2) < (c, v):
            c2, v2 = c, v
        label = f"{book}.{c}.{v}"
        if (c2, v2) != (c, v):
            label += f"-{v2}" if c2 == c else f"-{c2}.{v2}"
        verses = []
        for ch in range(c, c2 + 1):
            lo = v if ch == c else 1
            hi = v2 if ch == c2 else self.last[book][ch]
            verses += [(book, ch, vv) for vv in range(lo, hi + 1)]
        return label, verses


# ---------------------------------------------------------------- Nave's

def fetch_nave():
    base = os.path.join(CACHE, "crosswire", "nave")
    dict_base = os.path.join(base, "modules", "lexdict", "zld", "nave", "dict")
    if not os.path.exists(dict_base + ".idx"):
        z = connections.fetch(NAVE_ZIP, os.path.join(CACHE, "crosswire", "Nave.zip"))
        zipfile.ZipFile(z).extractall(base)
    return dict_base


def read_zld(base):
    """A SWORD compressed lexicon (zLD): [(key, entry text)] in the module's order."""
    idx, dat = open(base + ".idx", "rb").read(), open(base + ".dat", "rb").read()
    zdx, zdt = open(base + ".zdx", "rb").read(), open(base + ".zdt", "rb").read()
    blocks = {}

    def block(b):
        if b not in blocks:
            off, size = struct.unpack_from("<II", zdx, 8 * b)
            raw = zlib.decompress(zdt[off:off + size])
            n = struct.unpack_from("<I", raw, 0)[0]
            blocks[b] = (raw, [struct.unpack_from("<II", raw, 4 + 8 * k) for k in range(n)])
        return blocks[b]

    out = []
    for k in range(len(idx) // 8):
        off, size = struct.unpack_from("<II", idx, 8 * k)
        key, _, rest = dat[off:off + size].partition(b"\n")
        raw, entries = block(struct.unpack_from("<II", rest, 0)[0])
        eo, es = entries[struct.unpack_from("<II", rest, 0)[1]]
        out.append((key.strip(b"\r").decode("utf-8"), raw[eo:eo + es].rstrip(b"\0").decode("utf-8")))
    return out


def title_case(s):
    """'JESUS, THE CHRIST' -> 'Jesus, the Christ'; small words stay lower case."""
    small = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with"}
    words = re.split(r"(\s+|-)", s.lower())
    out = []
    for k, w in enumerate(words):
        out.append(w if (k and w in small) else w[:1].upper() + w[1:])
    return "".join(out)


def nave_topics(refs):
    """[{n, s: [[heading, depth, [refs]]], see: [names]}], and {verse: [topic numbers]}."""
    entries = read_zld(fetch_nave())
    topics, by_verse = [], collections.defaultdict(list)
    names = [title_case(k) for k, _ in entries]
    number = {k: i for i, (k, _) in enumerate(entries)}
    for t, (key, body) in enumerate(entries):
        body = re.sub(r"</?(entryFree|def)[^>]*>", "", body)
        lines = []
        # Each <lb/> starts a subtopic; a <list> under it holds sub-subtopics, one per <item>.
        for part in re.split(r"<lb/>", body):
            head, _, rest = part.partition("<list>")
            lines.append((head, 0))
            lines += [(it, 1) for it in re.findall(r"<item>(.*?)</item>", rest, re.S)]
        subs, see = [], []
        for text, depth in lines:
            text = text.replace("→", "").strip()
            if not text:
                continue
            targets = re.findall(r'<ref target="Nave:([^"]+)">', text)
            if re.match(r"\s*See\b", re.sub(r"<[^>]+>", "", text)) and targets:
                see += [number[x] for x in targets if x in number and number[x] != t]
                continue
            rs, verses = [], []
            for r in re.findall(r'<ref osisRef="([^"]+)"', text):
                parsed = refs.parse(r)
                if parsed:
                    rs.append(parsed[0])
                    verses += parsed[1]
            # The heading is what is left once the references, as printed ("Ge 11:26; 14:2"),
            # are taken out; a reference to another topic keeps its words.
            heading = re.sub(r'<ref osisRef="[^"]*">.*?</ref>', "", text)
            heading = html.unescape(re.sub(r"<[^>]+>", "", heading))
            heading = re.sub(r"(\s*[;,.:]\s*)+$", "", re.sub(r"\s*([;,]\s*){2,}", "; ", heading))
            # Verse numbers printed outside the tags (", 6; :21") go too.
            heading = re.sub(r"(\s*[;,]\s*:?\d[\d:\-–,\s]*)+(?=[;,]|$)", "", heading)
            heading = re.sub(r"\s{2,}", " ", heading).strip(" ;,")
            heading = re.sub(r"^0f\b", "Of", heading)   # a slip in the source
            if heading.isupper():
                heading = title_case(heading)
            for b, c, v in verses:
                if not by_verse[(b, c, v)] or by_verse[(b, c, v)][-1] != t:
                    by_verse[(b, c, v)].append(t)
            if heading or rs:
                subs.append([heading, depth, rs])
        topic = {"n": names[t], "s": subs}
        if see:
            topic["see"] = sorted(set(see), key=see.index)
        topics.append(topic)
    return topics, by_verse


# ---------------------------------------------------------------- Easton's

def easton_entries(refs):
    """[{n, s: [paragraphs, with refs as [[Gen.10.22|Gen. 10:22]]]}], and {verse: [entry numbers]}."""
    path = os.path.join(chronology.fetch(CACHE), "easton.json")
    records = [r["fields"] for r in json.load(open(path, encoding="utf-8"))]
    records.sort(key=lambda f: f["index"])
    groups = collections.OrderedDict()
    for f in records:
        groups.setdefault(f["termID"], []).append(f)
    entries, by_verse = [], collections.defaultdict(list)

    def link(m):
        label, href = m[1], m[2]
        target = href.partition("#")[2]
        parsed = refs.parse(target) if target else None
        if not parsed:
            return label
        for b, c, v in parsed[1]:
            cite.add((b, c, v))
        return f"[[{parsed[0]}|{label}]]"

    for k, (term_id, fs) in enumerate(groups.items()):
        cite = set()
        senses = []
        for f in fs:
            text = (f.get("dictText") or "").strip()
            text = re.sub(r"\[([^\]]+)\]\(([^)]*)\)", link, text)
            text = "\n\n".join(p.strip() for p in re.split(r"\n\s*\n", text) if p.strip())
            if text:
                senses.append(text)
        if not senses:
            continue
        n = len(entries)
        entries.append({"n": fs[0]["termLabel"], "s": senses})
        for verse in cite:
            by_verse[verse].append(n)
    return entries, by_verse


# ---------------------------------------------------------------- cross-references

XREF_MIN_VOTES = 3


def cross_references(vers, texts):
    """{verse: [(target, votes)]}, most-voted first; targets as "Rom.5.8" or "Rom.5.8-10"."""
    refs, _, _ = connections.load_cross_references(connections.fetch_openbible(), XREF_MIN_VOTES, vers, texts)
    out = collections.defaultdict(list)
    for a, b, e, votes in refs:
        if e[0] != b[0] or e < b:
            e = b
        label = f"{b[0]}.{b[1]}.{b[2]}"
        if e != b:
            label += f"-{e[2]}" if e[1] == b[1] else f"-{e[1]}.{e[2]}"
        out[a].append((label, votes))
    for a in out:
        seen, kept = set(), []
        for label, votes in sorted(out[a], key=lambda x: -x[1]):
            if label not in seen:
                seen.add(label)
                kept.append((label, votes))
        out[a] = kept
    return out


# ---------------------------------------------------------------- output

def write_json(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def main():
    texts = connections.load_texts()
    vers = connections.Versification(connections.fetch_stepbible("tvtms"), texts)
    refs = Refs(vers, texts)
    topics, topic_verses = nave_topics(refs)
    nave_bad, refs.bad = refs.bad, 0
    entries, dict_verses = easton_entries(refs)
    xrefs = cross_references(vers, texts)
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        os.remove(os.path.join(OUT, name))
    write_json(os.path.join(OUT, "topics.json"), [t["n"] for t in topics])
    write_json(os.path.join(OUT, "dictionary.json"), [e["n"] for e in entries])
    for k in range(0, len(topics), CHUNK):
        write_json(os.path.join(OUT, f"t{k // CHUNK:02d}.json"), topics[k:k + CHUNK])
    for k in range(0, len(entries), CHUNK):
        write_json(os.path.join(OUT, f"d{k // CHUNK:02d}.json"), entries[k:k + CHUNK])
    for num, osis, name, _ in BOOKS:
        t = {f"{c}:{v}": ts for (b, c, v), ts in sorted(topic_verses.items()) if b == osis}
        d = {f"{c}:{v}": sorted(ds) for (b, c, v), ds in sorted(dict_verses.items()) if b == osis}
        x = {f"{c}:{v}": [r for r, _ in rs] for (b, c, v), rs in sorted(xrefs.items()) if b == osis}
        write_json(os.path.join(OUT, file_stem(num, name) + ".json"), {"t": t, "d": d, "x": x})
    n_refs = sum(len(s[2]) for t in topics for s in t["s"])
    print(f"Topics: {len(topics)} with {n_refs} references ({nave_bad} not found in our text), "
          f"{len(topic_verses)} verses indexed")
    print(f"Cross-references: {sum(len(v) for v in xrefs.values())} from {len(xrefs)} verses "
          f"(OpenBible.info, at least {XREF_MIN_VOTES} votes)")
    print(f"Dictionary: {len(entries)} entries ({refs.bad} references not found), {len(dict_verses)} verses indexed")


if __name__ == "__main__":
    main()
