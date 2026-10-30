"""The site's own wording, and what each language's dictionary still lacks.

    python3 scripts/i18n.py                 how much of the wording each language has
    python3 scripts/i18n.py --missing zh-Hant   the wording that language lacks, as JSON to
                                            translate (English: "")
    python3 scripts/i18n.py --built         wording a script builds with ${...}, which needs
                                            I18N.t("... {n} ...", {n}) to be translatable

Reads   the pages (*.html, maps/*.html) and the site's scripts (nav.js, account.js, share.js,
        themes.js), and the dictionaries i18n/<code>.js (see i18n.js)
Finds   the wording a reader sees: text in the pages (not in scripts, styles or anything marked
        translate="no"), the title, aria-label, placeholder and alt of elements, and, in
        scripts, quoted wording given as text, a title or a label, or passed to I18N.t,
        I18N.plural, toast or a button. Names of people and places are kept apart, in
        i18n/<code>.names.js (scripts/names_zh.py).
"""

import glob
import html.parser
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "maps", "*.html")))
SCRIPTS = [os.path.join(ROOT, f) for f in ("nav.js", "account.js", "share.js", "themes.js")]
ATTRS = {"title", "aria-label", "placeholder", "alt", "data-tip"}
LATIN = re.compile(r"[A-Za-z]{2}")

# A quoted string in a script, after one of the ways the site gives wording to the page.
JS_TEXT = re.compile(r"""(?:\btext\s*:\s*|\btextContent\s*=\s*|\btitle\s*[:=]\s*|["']aria-label["']\s*[:,]\s*|\bplaceholder\s*[:=]\s*|"""
                     r"""\balt\s*[:=]\s*|\btoast\(\s*|\bI18N\.t\(\s*|\bL\.t\(\s*|\bconfirm\(\s*|\bsay\(\s*|"""
                     r"""(?:el|h)\(\s*["'][a-z0-9]+["']\s*,\s*(?:\{[^{}]*\}|null|\{\})\s*,\s*)"""
                     r"""(["'`])((?:\\.|(?!\1).){2,400}?)\1""", re.S)
PLURAL = re.compile(r"""\b(?:I18N|L)\.plural\([^,]+,\s*(["'])((?:\\.|(?!\1).)+)\1\s*,\s*(["'])((?:\\.|(?!\3).)+)\3""")


def wanted(s):
    s = s.strip()
    return bool(s) and bool(LATIN.search(s)) and len(s) <= 400 and not re.fullmatch(r"[\w.#:/?=&%-]+\.(html|js|json|svg|png)\b.*", s) \
        and not s.startswith(("http", "mailto:", "#", "data:"))


class Page(html.parser.HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.found, self.scripts = [], set(), []

    def skipping(self):
        return any(tag in ("script", "style", "textarea", "code", "pre") or no for tag, no in self.stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type") == "application/json":
            no = True
        else:
            no = a.get("translate") == "no"
        if not (no or self.skipping()):
            for k, v in attrs:
                if k in ATTRS and v and wanted(v):
                    self.found.add(v.strip())
        if tag not in self.VOID:
            self.stack.append((tag, no))
        self.script = tag == "script" and a.get("type") != "application/json" and "src" not in a

    def handle_endtag(self, tag):
        while self.stack:
            t, _ = self.stack.pop()
            if t == tag:
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] == "script" and getattr(self, "script", False):
            self.scripts.append(data)
        elif not self.skipping() and wanted(data):
            self.found.add(" ".join(data.split()))


def from_script(src, found, built):
    for m in JS_TEXT.finditer(src):
        q, s = m.group(1), m.group(2)
        if q == "`" and "${" in s:
            if LATIN.search(re.sub(r"\$\{[^}]*\}", "", s)):
                built.add(s)
            continue
        s = s.replace("\\'", "'").replace('\\"', '"')
        if wanted(s) and not re.search(r"[<>{};]|^\w+(\.\w+)+$|^[a-z]+(-[a-z]+)+$", s):
            found.add(s)
    for m in PLURAL.finditer(src):
        found.add(m.group(2) + "|" + m.group(4))


def collect():
    found, built = set(), set()
    for path in PAGES:
        p = Page()
        p.feed(open(path, encoding="utf-8").read())
        found |= p.found
        for s in p.scripts:
            from_script(s, found, built)
    for path in SCRIPTS:
        from_script(open(path, encoding="utf-8").read(), found, built)
    return found, built


def dictionary(code, kind=""):
    path = os.path.join(ROOT, "i18n", f"{code}{kind}.js")
    if not os.path.exists(path):
        return {}
    src = open(path, encoding="utf-8").read()
    m = re.search(r"I18N\.add\((\{.*\})\);", src, re.S)
    return json.loads(re.sub(r",(\s*\})", r"\1", m.group(1))) if m else {}


def main():
    args = sys.argv[1:]
    found, built = collect()
    if args[:1] == ["--built"]:
        print("\n".join(sorted(built)))
        return
    langs = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ROOT, "i18n", "*.js")) if ".names." not in f)
    if args[:1] == ["--missing"] and len(args) > 1:
        d = dictionary(args[1])
        print(json.dumps({s: "" for s in sorted(found) if s not in d}, ensure_ascii=False, indent=1))
        return
    print(f"{len(found):,} pieces of wording on the site; {len(built):,} more built by scripts (--built).")
    for code in langs:
        d = dictionary(code)
        have = sum(1 for s in found if s in d)
        print(f"  {code}: {have:,} of {len(found):,} ({100 * have / max(1, len(found)):.0f}%); "
              f"{len(dictionary(code, '.names')):,} names")


if __name__ == "__main__":
    main()
