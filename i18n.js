// Languages: the site in the reader's own language, on every page.
//
// Each language is a dictionary in i18n/<code>.js, from the site's English to that language.
// This file chooses the language (the ?lang= address, then the reader's choice, kept on the
// device, then the browser's languages, then English), loads its dictionary before the page's
// own scripts run, and translates the page:
//   - text and labels written in the page, or added to it later, whose whole English wording
//     is in the dictionary (titles, buttons, headings, names), as they appear;
//   - wording built by a script, through I18N.t("{n} days", {n: 3}) and I18N.plural(n, one, other);
//   - text drawn on a canvas, which scripts pass through I18N.t themselves.
// Anything marked translate="no" is left alone: the Bible text, the Hebrew and Greek, notes a
// reader writes. Words missing from a dictionary show in English, so a page is never blank.
// A new language is a line in LANGS and a dictionary; `python3 scripts/i18n.py` lists what it
// still lacks.
(() => {
  const LANGS = {
    en: { name: "English", locale: "en" },
    "zh-Hant": { name: "繁體中文", locale: "zh-Hant-HK", bible: true },
  };
  const KEY = "pe.lang";
  const me = document.currentScript;
  const ROOT = new URL(".", me.src).href;
  const V = new URL(me.src).searchParams.get("v") || "1";

  function choose() {
    const asked = new URLSearchParams(location.search).get("lang");
    if (asked && LANGS[asked]) { remember(asked); return asked; }
    try { const kept = JSON.parse(localStorage.getItem(KEY)); if (kept && LANGS[kept]) return kept; } catch (e) { /* none kept */ }
    for (const l of navigator.languages || [navigator.language || "en"]) {
      const x = String(l).toLowerCase();
      if (/^zh-(hant|tw|hk|mo)\b/.test(x)) return "zh-Hant";
      if (/^zh\b/.test(x)) continue;   // Simplified Chinese: not yet, so try the next language
      const code = Object.keys(LANGS).find(k => k.toLowerCase() === x || k.toLowerCase() === x.split("-")[0]);
      if (code) return code;
    }
    return "en";
  }
  function remember(code) { try { localStorage.setItem(KEY, JSON.stringify(code)); } catch (e) { /* storage unavailable */ } }

  const lang = choose();
  const dict = Object.create(null);
  document.documentElement.lang = lang;

  // Wording: the dictionary's, else the English; {name} filled from vars.
  const fill = (s, vars) => vars ? s.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m)) : s;
  function t(s, vars) {
    const v = dict[s];
    return fill(typeof v === "string" ? v : s, vars);
  }
  // A count: the dictionary gives one wording, or one for each of the language's plural forms
  // ({one, few, many, other}); English picks between the two it is given.
  let rules = null;
  function plural(n, one, other, vars) {
    const all = { n: n.toLocaleString(LANGS[lang].locale), ...vars };
    const v = dict[one + "|" + other];
    if (typeof v === "string") return fill(v, all);
    if (v && typeof v === "object") {
      rules = rules || new Intl.PluralRules(LANGS[lang].locale);
      return fill(v[rules.select(n)] || v.other, all);
    }
    return fill(n === 1 ? one : other, all);
  }

  /* ---------- Translating the page ---------- */
  const ATTRS = ["title", "aria-label", "placeholder", "alt", "data-tip"];
  const SKIP = "script,style,textarea,code,pre,[translate=no],[contenteditable]";
  function textNode(n) {
    const raw = n.nodeValue, s = raw.trim();
    if (!s || s.length > 400) return;
    const v = dict[s];
    if (typeof v !== "string") return;
    const p = n.parentElement;
    if (p && p.closest(SKIP)) return;
    n.nodeValue = raw.replace(s, v);
  }
  function element(el) {
    for (const a of ATTRS) {
      const s = el.getAttribute(a);
      if (s && typeof dict[s.trim()] === "string" && !el.closest(SKIP)) el.setAttribute(a, dict[s.trim()]);
    }
    if (el.tagName === "INPUT" && (el.type === "button" || el.type === "submit") && typeof dict[el.value] === "string") el.value = dict[el.value];
  }
  function translate(root) {
    if (root.nodeType === 3) { textNode(root); return; }
    if (root.nodeType !== 1 && root.nodeType !== 9 && root.nodeType !== 11) return;
    if (root.nodeType === 1) { if (root.closest(SKIP)) return; element(root); }
    const walk = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode: n => n.nodeType === 1 && n.matches(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
    });
    for (let n = walk.nextNode(); n; n = walk.nextNode()) n.nodeType === 3 ? textNode(n) : element(n);
  }
  let watching = false;
  function watch() {
    if (watching || lang === "en") return;
    watching = true;
    translate(document.documentElement);
    if (typeof dict[document.title] === "string") document.title = dict[document.title];
    new MutationObserver(list => {
      for (const m of list) {
        if (m.type === "childList") m.addedNodes.forEach(translate);
        else if (m.type === "characterData") textNode(m.target);
        else if (m.type === "attributes") element(m.target);
      }
    }).observe(document.documentElement, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS });
  }

  window.I18N = {
    lang, LANGS, ROOT,
    locale: LANGS[lang].locale,
    en: lang === "en",
    t, plural,
    // A dictionary file adds its words with I18N.add({...}).
    add(words) { Object.assign(dict, words); },
    has: s => typeof dict[s] === "string",
    // Change the language: kept on this device, and the page shown again in it.
    set(code) {
      if (!LANGS[code] || code === lang) return;
      remember(code);
      const u = new URL(location.href);
      u.searchParams.delete("lang");
      location.replace(u.href);
    },
    translate,
    number: n => Number(n).toLocaleString(LANGS[lang].locale),
    date: (d, opts) => new Date(d).toLocaleDateString(LANGS[lang].locale, opts),
  };

  if (lang !== "en") {
    // The dictionary loads before the page's own scripts run, so they can use it at once.
    document.write(`<script src="${ROOT}i18n/${lang}.js?v=${V}"><\/script>`);
    document.write(`<style>:lang(zh-Hant) em, :lang(zh-Hant) i, :lang(zh-Hant) cite { font-style: normal; }
:lang(zh-Hant) body { font-synthesis: none; }</style>`);
    // Once the page is read, everything in it is translated, and whatever is added later.
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", watch);
    else watch();
  }
})();
