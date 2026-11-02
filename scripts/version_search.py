"""Build a search index for another version of the Bible, like data/bible/search.json for ours.

    python3 scripts/version_search.py bsb      ->  data/bible/versions/bsb/search.json

Each verse as [book slug, chapter, verse, plain text]. The reader searches this version while our
own translation is hidden for review (i18n.js).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = json.load(open(os.path.join(ROOT, "data", "bible", "books.json"), encoding="utf-8"))


def plain(s):
    s = re.sub(r"\[\^\w+\]", "", s or "")
    s = re.sub(r"[*_]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def main(ver):
    folder = os.path.join(ROOT, "data", "bible", "versions", ver)
    out = []
    for b in BOOKS:
        path = os.path.join(folder, b["slug"] + ".json")
        if not os.path.exists(path):
            continue
        for ch in json.load(open(path, encoding="utf-8"))["chapters"]:
            for row in ch["v"]:
                if len(row) > 2 and isinstance(row[2], dict) and row[2].get("x"):
                    continue
                t = plain(row[1])
                if t:
                    out.append([b["slug"], int(ch["c"]), row[0], t])
    with open(os.path.join(folder, "search.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(ver, len(out), "verses")


if __name__ == "__main__":
    for v in sys.argv[1:] or ["bsb"]:
        main(v)
