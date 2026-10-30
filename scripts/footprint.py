"""Where each Hebrew, Aramaic and Greek word appears: the data for a word's footprint in the
reader's word panel.

    python3 scripts/footprint.py          (after reader.py)

Reads   data/bible/words/NN-book.json     each verse's words, with their Strong's numbers
Writes  data/bible/footprint/hNN.json     Old Testament words, by thousands of Strong's number
        data/bible/footprint/gNN.json     New Testament words, the same
        Each maps a word's Strong's key, as the words files give it ("7225G", "3056"), to
        [total, chapter, count, chapter, count, ...]: the chapters it appears in, numbered
        through the whole Bible from 0 (Genesis 1) to 1188 (Revelation 22), and how often.

A word is counted by the part of it that carries its meaning (the "main" morpheme), so the
prefixes of Hebrew words (and, the, in) are not counted as words of their own.
"""

import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS, file_stem            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bible")
OUT = os.path.join(DATA, "footprint")


def main():
    counts = {"h": collections.defaultdict(collections.Counter), "g": collections.defaultdict(collections.Counter)}
    chapter = 0
    for num, osis, name, testament in BOOKS:
        words = json.load(open(os.path.join(DATA, "words", file_stem(num, name) + ".json"), encoding="utf-8"))
        lang = "h" if testament == "OT" else "g"
        for ch in words["chapters"]:
            for verse in ch["w"].values():
                for w in verse.split("¦"):
                    f = w.split("|")
                    if len(f) < 3 or not f[2]:
                        continue
                    parts = f[2].split("/")
                    main = int(f[4]) if len(f) > 4 and f[4] != "" else len(parts) - 1
                    key = parts[main] if main < len(parts) else parts[-1]
                    m = re.match(r"\d+", key)
                    if not m or int(m.group()) >= 9000:
                        continue
                    counts[lang][key][chapter] += 1
            chapter += 1
    os.makedirs(OUT, exist_ok=True)
    for lang, by_key in counts.items():
        chunks = collections.defaultdict(dict)
        for key, chs in by_key.items():
            flat = [sum(chs.values())]
            for c in sorted(chs):
                flat += [c, chs[c]]
            chunks[int(re.match(r"\d+", key).group()) // 1000][key] = flat
        for k, data in chunks.items():
            with open(os.path.join(OUT, f"{lang}{k:02d}.json"), "w", encoding="utf-8", newline="\n") as f:
                json.dump(data, f, separators=(",", ":"), sort_keys=True)
                f.write("\n")
        print(f"{lang}: {len(by_key)} words in {len(chunks)} files")
    print(f"{chapter} chapters")


if __name__ == "__main__":
    main()
