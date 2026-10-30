"""The plates of George Adam Smith and J. G. Bartholomew's Atlas of the Historical Geography of
the Holy Land (London: Hodder and Stoughton, 1915), for the maps section.

    python3 scripts/atlas.py

Reads   the Columbia University Libraries copy scanned for the Internet Archive,
        https://archive.org/details/ldpd_7032971_000 ("Digital version available with no
        restrictions"; the atlas is in the public domain: Smith died in 1942, Bartholomew in
        1920). Each page is downloaded once into .cache/atlas/.
Writes  maps/atlas/ID.jpg       each plate, at most 2400 pixels on its long side; a plate
                                printed across two pages is joined into one picture
        maps/atlas/ID-t.jpg     a small picture of it for its card
        maps/atlas.html         the catalogue of the plates, with a viewer that zooms

The 16 large-scale sheets of Palestine in sections (Maps 15-30) are left for later.
"""

import html
import json
import os
import sys
import urllib.request

from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webpages                                  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", "atlas")
OUT = os.path.join(ROOT, "maps", "atlas")
ITEM = "ldpd_7032971_000"

# Each plate: its id, the scan's page numbers (two for a plate across two pages), the atlas's
# own map number, its title and its years.
PARTS = [
    ("Part I · The Bible lands", [
        ("semitic-world", [36], "1", "The Semitic World", ""),
        ("western-asia-1400", [37], "2", "Western Asia before 1400 B.C.", "Before 1400 BC"),
        ("ancient-empires", [38, 39], "3–5", "Empires of the Ancient World", "Egypt, Babylon and Persia; Alexander; Rome"),
        ("western-asia-greek", [40], "6", "Western Asia in the Fourth to Second Centuries B.C.", "The Greek kingdoms after Alexander"),
        ("table-of-nations", [41], "", "The World and Its Races according to the Old Testament", "The table of nations, Genesis 10"),
        ("egypt", [42], "7", "Egypt", "The land of the sojourn and the Exodus"),
        ("sinai", [43], "8", "The Sinai Peninsula", "The wilderness wanderings"),
    ]),
    ("Part II · The land", [
        ("trade-routes", [44], "9", "Ancient Trade Routes to Palestine", ""),
        ("palestine-roads", [46, 47, "turn"], "11–12", "Palestine: Its Mountains, Roads and Communications", "The general map of the land"),
        ("geology", [48], "13", "The Geology of Palestine", ""),
        ("vegetation", [49], "14", "The Vegetation of Palestine", ""),
        ("economic", [45], "10", "Economic Map of Palestine", "As it was in 1915"),
    ]),
    ("Part III · Palestine through Israel’s history", [
        ("before-israel", [74], "31", "Palestine before the Coming of Israel", "1500–1250 BC"),
        ("judges", [75], "32", "Israel’s Settlement and the Judges", "Before 1050 BC"),
        ("saul", [76], "33", "Palestine in the Time of Saul", "About 1020 BC"),
        ("david-solomon", [77], "34", "Palestine under David and Solomon", "About 1015–930 BC"),
        ("elijah-elisha", [78], "35", "The Times of Elijah and Elisha", "About 860–800 BC"),
        ("to-the-exile", [79], "36", "From 720 B.C. to the Exile of Judah", "720–586 BC"),
        ("persians", [80], "37", "Palestine under the Persians", "538–332 BC"),
        ("maccabees", [81], "38", "The Time of the Maccabees", "168–135 BC"),
        ("jannaeus", [82], "39", "Alexander Jannaeus and Queen Alexandra", "103–67 BC"),
        ("pompey", [83], "40", "After Pompey’s Rearrangement", "63–48 BC"),
        ("mark-antony", [84], "41", "Palestine under Mark Antony", "About 42–31 BC"),
        ("herod", [85], "42", "Palestine under Herod the Great", "31–4 BC"),
        ("time-of-christ", [86], "43", "Under Herod’s Will and in the Time of Christ", "4 BC–AD 37"),
        ("agrippa-i", [87], "44", "Palestine in the Time of Agrippa I", "AD 37–44"),
        ("procurators", [88], "45", "Palestine under the Roman Procurators", "AD 6–41 and 44–70"),
        ("agrippa-ii", [89], "46", "Palestine in the Time of Agrippa II", "AD 48–70"),
        ("jerusalem-periods", [90, 91, "cut:0.044"], "47–48", "Jerusalem at Different Periods", "From David to the three northern walls"),
        ("jerusalem-1915", [92, 93, "stack"], "49–50", "Modern Jerusalem, Illustrating Recent Discoveries", "As it was in 1915"),
    ]),
    ("Part IV · The Christian era", [
        ("paul", [94], "51", "St. Paul’s Travels", "The eastern Mediterranean"),
        ("seven-churches", [95], "52", "Asia Minor, Showing the Seven Churches", "Revelation 2–3"),
        ("church-and-empire", [96], "53", "The Church and the Empire in the East", "Under Trajan and under Constantine"),
        ("eusebius", [97], "54", "Palestine in the Fourth Century", "After Eusebius and Jerome"),
        ("peutinger", [98], "55", "Palestine after the Peutinger Table", "A Roman road map"),
        ("sanutus", [99], "56", "Palestine after Marinus Sanutus", "A map of about 1320"),
        ("crusades", [100], "57", "Syria and Palestine in the Time of the Crusades", ""),
        ("expansion", [101], "58", "Europe in the Time of the Crusades; the Expansion of Christianity", ""),
        ("palestine-1915", [102], "59", "The Political Divisions of Palestine", "As they were in 1915"),
        ("missions", [103], "60", "Christian Missions in Palestine", "As they were in 1915"),
    ]),
]


def page(n, width=2000):
    """One page of the scan, downloaded once."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"n{n}_w{width}.jpg")
    if not os.path.exists(path):
        url = f"https://archive.org/download/{ITEM}/page/n{n}_w{width}.jpg"
        req = urllib.request.Request(url, headers={"User-Agent": "PlainEnglishBible/1.0 (https://bibledata.org)"})
        with urllib.request.urlopen(req, timeout=120) as r, open(path + ".part", "wb") as f:
            f.write(r.read())
        os.replace(path + ".part", path)
    return Image.open(path).convert("RGB")


def trim(im, dark=60):
    """Cut away the scanner's black surround, keeping the paper."""
    g = ImageOps.grayscale(im)
    w, h = g.size
    px = g.load()
    def paper(x0, y0, dx, dy, n):
        x, y = x0, y0
        for i in range(n):
            if px[x, y] > dark:
                return i
            x += dx; y += dy
        return 0
    # Sample several lines in from each edge; take the deepest edge of black found.
    left = max(paper(0, int(h * f), 1, 0, w // 4) for f in (0.3, 0.5, 0.7))
    right = max(paper(w - 1, int(h * f), -1, 0, w // 4) for f in (0.3, 0.5, 0.7))
    top = max(paper(int(w * f), 0, 0, 1, h // 4) for f in (0.3, 0.5, 0.7))
    bottom = max(paper(int(w * f), h - 1, 0, -1, h // 4) for f in (0.3, 0.5, 0.7))
    return im.crop((left, top, w - right, h - bottom))


def gutter(im):
    """A right-hand page begins with the dark of the binding: cut it away."""
    g = ImageOps.grayscale(im)
    w, h = g.size
    band = g.crop((0, int(h * 0.1), w // 6, int(h * 0.9))).resize((w // 6, 1), Image.BOX).load()
    cut = 0
    for x in range(w // 6):
        if band[x, 0] < 110:
            cut = x + 1
    return im.crop((cut, 0, w, h))


def plate(pages):
    """The plate's picture: a page, or two pages joined. Side by side at the same height,
    unless marked "stack" (one above the other) or "turn" (printed sideways: north to the left)."""
    how = [p for p in pages if isinstance(p, str)]
    ims = [trim(page(n)) for n in pages if not isinstance(n, str)]
    if len(ims) == 1:
        return ims[0]
    if "stack" in how:
        w = min(im.width for im in ims)
        ims = [im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) for im in ims]
        out = Image.new("RGB", (w, sum(im.height for im in ims)), "white")
        y = 0
        for im in ims:
            out.paste(im, (0, y))
            y += im.height
        return out
    ims = ims[:1] + [gutter(im) for im in ims[1:]]
    # A strip of the fold the gutter test leaves: "cut:F" trims F of the second page's width.
    for f in [float(p[4:]) for p in how if p.startswith("cut:")]:
        ims[1] = ims[1].crop((round(ims[1].width * f), 0, ims[1].width, ims[1].height))
    h = min(im.height for im in ims)
    ims = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    out = Image.new("RGB", (sum(im.width for im in ims), h), "white")
    x = 0
    for im in ims:
        out.paste(im, (x, 0))
        x += im.width
    return out.rotate(-90, expand=True) if "turn" in how else out


def main():
    os.makedirs(OUT, exist_ok=True)
    data, sections = [], []
    for part, plates in PARTS:
        cards = []
        for pid, pages, no, title, when in plates:
            full = os.path.join(OUT, pid + ".jpg")
            thumb = os.path.join(OUT, pid + "-t.jpg")
            if not os.path.exists(full) or not os.path.exists(thumb):
                im = plate(pages)
                big = im.copy()
                big.thumbnail((2400, 2400), Image.LANCZOS)
                big.save(full, "JPEG", quality=80, optimize=True, progressive=True)
                small = im.copy()
                small.thumbnail((560, 560), Image.LANCZOS)
                small.save(thumb, "JPEG", quality=76, optimize=True, progressive=True)
            w, h = Image.open(full).size
            data.append({"id": pid, "no": no, "title": title, "when": when, "page": pages[0],
                         "image": f"atlas/{pid}.jpg", "thumb": f"atlas/{pid}-t.jpg", "w": w, "h": h})
            cards.append(
                f'    <li><a href="#{pid}" data-plate="{pid}">'
                f'<div class="thumb"><img src="atlas/{pid}-t.jpg" alt="" loading="lazy" decoding="async"></div>'
                f'<div class="txt"><span class="no">{"Map " + no if no else "Plate"}</span>'
                f'<h2>{html.escape(title)}</h2>' + (f'<p class="when">{html.escape(when)}</p>' if when else "")
                + '</div></a></li>')
            print(f"{pid}: {w}x{h}")
        sections.append(f'  <p class="part">{html.escape(part)}</p>\n  <ul class="plates">\n' + "\n".join(cards) + "\n  </ul>")
    body = open(os.path.join(ROOT, "scripts", "templates", "atlas.html"), encoding="utf-8").read()
    body = (body.replace("{{PLATES}}", "\n".join(sections))
            .replace("{{DATA}}", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
            .replace("<!-- APPBAR -->", webpages.appbar("maps/index.html", "../")))
    with open(os.path.join(ROOT, "maps", "atlas.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.document(body, "../", ("#f6f0dd", "#191714")))
    print(f"{len(data)} plates")


if __name__ == "__main__":
    main()
