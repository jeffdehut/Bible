// The site's menu: every part of the Plain English Bible, the same on every page.
//
// This file is the one list of destinations. In the reader (index.html) it fills the menu
// sheet, giving each reader tool the id the reader's script listens for. On every other page it
// adds a menu button to the top bar (or to a map's toolbar) and a menu of its own; a reader
// tool opens the reader with that tool open ("index.html#open=bookmarks"). A new page or tool
// added to MENU appears everywhere at once.
(() => {
  const ROOT = new URL(".", document.currentScript.src).href;
  const svg = d => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const ICON = {
    read: '<path d="M12 6.5C10 5 7 4.5 3.5 5v14c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v14"/><path d="M6.5 9.5h3M6.5 13h3M14.5 9.5h3M14.5 13h3"/>',
    mine: '<path d="m14.5 4.5 5 5L10 19H5v-5z"/><path d="m12 7 5 5"/><path d="M4 21h16"/>',
    bookmarks: '<path d="M6 3h12v18l-6-4.5L6 21Z"/>',
    plans: '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="m9 15 2 2 4-4"/>',
    study: '<path d="M12 6.5C10 5 7 4.5 3.5 5v14c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v14"/>',
    parallels: '<rect x="3" y="4" width="7.5" height="16" rx="1.5"/><rect x="13.5" y="4" width="7.5" height="16" rx="1.5"/><path d="M5.5 8.5h2.5M5.5 12h2.5M5.5 15.5h2.5M16 8.5h2.5M16 12h2.5M16 15.5h2.5"/>',
    marks: '<path d="M4 18.5c2-.6 3.2-.6 5 0s3 .6 5 0 3.2-.6 6 0"/><rect x="4" y="5" width="9" height="8" rx="1.5"/><path d="m16.5 6.5 2 3.5h-4z"/>',
    mymarks: '<path d="m12 3 2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6-4.5-4.2 6.1-.7Z"/>',
    sync: '<path d="M19.5 10A8 8 0 0 0 5.6 7.2L4 9"/><path d="M4 4v5h5"/><path d="M4.5 14a8 8 0 0 0 13.9 2.8L20 15"/><path d="M20 20v-5h-5"/>',
    web: '<circle cx="6" cy="7" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="12" cy="17" r="2.2"/><path d="M8 7.6 15.9 6.4M7.2 9 11 15M16.9 8 13 15"/>',
    web3d: '<path d="M12 2.5 20.5 7v10L12 21.5 3.5 17V7Z"/><path d="M3.5 7 12 11.5 20.5 7M12 11.5v10"/>',
    maps: '<path d="M9 4 3.5 6v14L9 18l6 2 5.5-2V4L15 6 9 4Z"/><path d="M9 4v14M15 6v14"/>',
    atlas: '<path d="M4 4h7v16H4zM13 4h7v16h-7z"/><path d="M6.5 8h2M15.5 8h2M6.5 11h2M15.5 11h2"/>',
    time: '<path d="M3 6.5c3 0 3-2 6-2s3 2 6 2 3-2 6-2"/><path d="M3 12c3 0 3-2 6-2s3 2 6 2 3-2 6-2"/><path d="M3 17.5c3 0 3-2 6-2s3 2 6 2 3-2 6-2"/><path d="M8 21v-2.5M16 21v-2.5"/>',
    gen: '<circle cx="12" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="19" r="2.2"/><path d="M12 7.2V12M6 16.8V12h12v4.8"/>',
    psalms: '<path d="M6 3.5c7 0 12 4.5 12.5 12"/><path d="M6 3.5V20.5h12.5"/><path d="M9.5 7v13.5M13 9.5v11M16 12.5v8"/>',
    proverbs: '<path d="M3.5 13.5h17c0 3-3.6 5-8.5 5s-8.5-2-8.5-5Z"/><path d="M20.5 13.5c1-.7 1.3-1.6 1.2-2.7"/><path d="M8.5 18.5 7.5 21h9l-1-2.5"/><path d="M12 4c1.2 1.6 2 2.6 2 4a2 2 0 0 1-4 0c0-1.4.8-2.4 2-4Z"/>',
    kings: '<path d="M3 8l4.2 4L12 6l4.8 6L21 8l-2 11H5Z"/>',
    arcs: '<path d="M3 19a9 9 0 0 1 18 0"/><path d="M7 19a5 5 0 0 1 10 0"/><path d="M10 19a2 2 0 0 1 4 0"/><path d="M2 19h20"/>',
    shelf: '<path d="M4 20V5h3v15M8 20V7h3v13M13 20l-1.5-14 3-.4L16 19.6"/><path d="M17 20V4h3v16M2 20.5h20"/>',
    project: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.1"/>',
    translation: '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5"/><path d="M9 12.5h7M9 16h5"/>',
    privacy: '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6Z"/><path d="m9 12 2 2 4-4"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
  };
  // Each: [id, label, icon, where, title, extra]. "where" is a page, or "reader:NAME" for a tool
  // of the reader (opened there by its button, #open-NAME). extra.sub gives the reader an
  // element for a live line under the label; extra.hidden starts it hidden.
  const MENU = [
    ["Read and study", "", [
      ["read", "Read", "read", "index.html", "Back to the Bible, where you left off", { away: true }],
      ["mine", "Highlights & notes", "mine", "reader:mine", "Your highlights and notes, saved on this device"],
      ["bookmarks", "Bookmarks", "bookmarks", "reader:bookmarks", "The passages you bookmarked", { sub: "bookmarks-sub" }],
      ["plans", "Reading plans", "plans", "reader:plans", "Through the Bible in a year, and shorter plans", { sub: "plans-sub" }],
      ["study", "Topics & dictionary", "study", "reader:study", "Nave’s topics and Easton’s Bible dictionary"],
      ["parallels", "Parallel passages", "parallels", "reader:parallels", "The Gospels side by side; Kings beside Chronicles"],
      ["marks", "Study markings", "marks", "reader:marks", "Key words marked through the whole Bible", { sub: "marks-sub" }],
      ["mymarks", "My markings", "mymarks", "reader:mymarks", "Your own markings, to trace words as you study"],
      ["account", "Sync devices", "sync", "reader:account", "Keep your highlights and notes on every device", { sub: "account-sub", hidden: true, readerOnly: true }],
    ]],
    ["Explore", "menu-explore", [
      ["graph", "Connections", "web", "graph.html", "Every chapter, person and place, and the threads between them"],
      ["web3d", "Web in 3D", "web3d", "web3d.html", "The web of Scripture in three dimensions"],
      ["maps", "Maps", "maps", "maps/index.html", "Bible maps, and the 1915 historical atlas"],
      ["history", "Timeline", "time", "history.html", "World history beside the Bible, from Creation"],
      ["genealogy", "Genealogy", "gen", "genealogy.html", "From Adam to Jesus, and every family"],
      ["psalms", "Psalms", "psalms", "psalms.html", "All 150 psalms by type, author and story"],
      ["proverbs", "Proverbs", "proverbs", "proverbs.html", "Every proverb, by topic"],
      ["kings", "Kings", "kings", "kings.html", "The kings of Israel and Judah, with the prophets of their days"],
      ["arcs", "Cross-refs", "arcs", "arcs.html", "Every cross-reference in the Bible as an arc"],
      ["library", "Bookshelf", "shelf", "library.html", "The 66 books as a bookshelf"],
    ]],
    ["About", "menu-about", [
      ["project", "This project", "project", "reader:project", "Who made it"],
      ["about", "This translation", "translation", "reader:about", "A first draft, awaiting review"],
      ["privacy", "Privacy", "privacy", "privacy.html", "What this site keeps about you"],
      ["feedback", "Send feedback", "mail", "mailto:info@bibledata.org", "Questions, mistakes and ideas", { id: "menu-feedback" }],
    ]],
  ];
  const here = new URL(location.href);
  const inReader = !!document.getElementById("site-menu");
  const isHere = where => !where.startsWith("reader:") && !where.startsWith("mailto:") && new URL(where, ROOT).pathname === here.pathname;

  function render(into) {
    into.textContent = "";
    for (const [title, cls, items] of MENU) {
      const h = document.createElement("h3");
      h.className = "menu-group"; h.textContent = title;
      const ul = document.createElement("ul");
      ul.className = "menu" + (cls ? " " + cls : "");
      for (const [id, label, icon, where, tip, extra = {}] of items) {
        if (extra.readerOnly && !inReader) continue;
        if (extra.away && inReader) continue;
        const reader = where.startsWith("reader:");
        const li = document.createElement("li");
        const a = document.createElement(reader && inReader ? "button" : "a");
        if (reader && inReader) { a.type = "button"; a.id = "open-" + where.slice(7); }
        else a.href = reader ? ROOT + "index.html#open=" + where.slice(7) : where.startsWith("mailto:") ? where : ROOT + where;
        if (extra.id) a.id = extra.id;
        if (extra.hidden && inReader) a.hidden = true;
        if (isHere(where)) a.setAttribute("aria-current", "page");
        a.title = tip;
        a.innerHTML = svg(ICON[icon]) + `<span>${label.replace(/&/g, "&amp;")}</span>` + (extra.sub ? `<small id="${inReader ? extra.sub : ""}"></small>` : "");
        li.append(a);
        ul.append(li);
      }
      into.append(h, ul);
    }
    // The languages the site speaks: each named in itself. Choosing one shows the page again in it.
    const L = window.I18N;
    if (!L || Object.keys(L.LANGS).length < 2) return;
    const h = document.createElement("h3");
    h.className = "menu-group"; h.textContent = "Language";
    const row = document.createElement("div");
    row.className = "menu-lang"; row.setAttribute("role", "group"); row.setAttribute("aria-label", "Language");
    for (const [code, info] of Object.entries(L.LANGS)) {
      const b = document.createElement("button");
      b.type = "button"; b.lang = code; b.textContent = info.name; b.setAttribute("translate", "no");
      b.setAttribute("aria-pressed", String(code === L.lang));
      b.onclick = () => L.set(code);
      row.append(b);
    }
    into.append(h, row);
    if (!document.getElementById("menu-lang-css")) {
      const st = document.createElement("style");
      st.id = "menu-lang-css";
      st.textContent = `.menu-lang { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 6px; }
.menu-lang button { min-height: 40px; padding: 0 16px; border-radius: 999px; border: 1px solid var(--line, #e4e2db); background: transparent; color: var(--ink, #161b26); font: 500 15px/1 system-ui, -apple-system, "Segoe UI", sans-serif; cursor: pointer; }
.menu-lang button:hover { background: var(--lapis-soft, #e7ecf8); }
.menu-lang button[aria-pressed="true"] { background: var(--lapis, #2646a1); border-color: var(--lapis, #2646a1); color: #fff; }`;
      document.head.append(st);
    }
  }

  // In the reader: fill its menu sheet, now, before the reader's own script runs.
  if (inReader) { render(document.getElementById("site-menu")); window.SiteNav = { MENU, render }; return; }

  // Elsewhere: a menu button and a menu of this page's own.
  const css = document.createElement("style");
  css.textContent = `
.sitenav-btn { flex: none; display: inline-grid; place-items: center; width: 40px; height: 40px; border: 0; border-radius: 10px; background: transparent; color: var(--ink, #161b26); cursor: pointer; margin-inline-start: 2px; }
.sitenav-btn:hover, .sitenav-btn[aria-expanded="true"] { background: var(--lapis-soft, #e7ecf8); }
.sitenav-btn svg { width: 22px; height: 22px; }
.sitenav { font-family: "Libre Franklin", system-ui, -apple-system, "Segoe UI", sans-serif; }
.sitenav-head { display: flex; align-items: center; justify-content: space-between; padding: 4px 0 2px; }
.sitenav-head b { font: 600 19px/1.2 "Frank Ruhl Libre", Georgia, serif; }
.sitenav-head button { width: 40px; height: 40px; border: 0; border-radius: 10px; background: transparent; color: inherit; cursor: pointer; font-size: 20px; }
.sitenav-head button:hover { background: var(--lapis-soft, #e7ecf8); }
.sitenav .menu-group { font: 600 12px/1 "Libre Franklin", system-ui, sans-serif; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted, #5b6475); margin: 14px 2px 8px; }
.sitenav .menu { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(78px, 1fr)); gap: 6px; }
.sitenav .menu a { display: flex; flex-direction: column; align-items: center; gap: 7px; height: 100%; text-align: center; padding: 10px 4px 9px; border-radius: 14px;
  font: 500 13px/1.25 "Libre Franklin", system-ui, sans-serif; color: var(--ink, #161b26); text-decoration: none; }
.sitenav .menu a:hover { background: var(--lapis-soft, #e7ecf8); }
.sitenav .menu a[aria-current="page"] { background: var(--lapis-soft, #e7ecf8); box-shadow: inset 0 0 0 1.5px var(--lapis, #2646a1); }
.sitenav .menu svg { width: 46px; height: 46px; padding: 11px; border-radius: 14px; box-sizing: border-box; flex: none; background: var(--lapis-soft, #e7ecf8); color: var(--lapis, #2646a1); }
.sitenav .menu.menu-explore svg { background: color-mix(in srgb, #d9a520 22%, transparent); color: #8a640b; }
.sitenav .menu.menu-about svg { background: color-mix(in srgb, var(--line, #e4e2db) 60%, transparent); color: var(--muted, #5b6475); }
.sitenav .menu small:empty { display: none; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .sitenav .menu.menu-explore svg { color: #e2bd5c; } }
:root[data-theme="dark"] .sitenav .menu.menu-explore svg { color: #e2bd5c; }
@media print { .sitenav-btn, .sitenav, .sitenav-scrim { display: none !important; } }`;
  document.head.append(css);
  const btn = document.createElement("button");
  btn.type = "button"; btn.className = "sitenav-btn"; btn.setAttribute("aria-label", "Menu: every part of the Plain English Bible");
  btn.setAttribute("aria-expanded", "false"); btn.setAttribute("aria-controls", "sitenav");
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  // The menu is a panel of ui.js, as in the reader: a sheet from the bottom on phones, a panel
  // down the right on larger screens.
  const scrim = document.createElement("div");
  scrim.className = "ui-scrim sitenav-scrim"; scrim.hidden = true;
  const panel = document.createElement("nav");
  panel.className = "ui-sheet sitenav"; panel.id = "sitenav"; panel.hidden = true; panel.setAttribute("aria-label", "Plain English Bible");
  const grab = document.createElement("div");
  grab.className = "ui-grab";
  const head = document.createElement("div");
  head.className = "sitenav-head ui-head";
  head.innerHTML = '<b>Plain English Bible</b><button type="button" data-close aria-label="Close">✕</button>';
  const body = document.createElement("div");
  render(body);
  panel.append(grab, head, body);
  const open = on => {
    panel.hidden = scrim.hidden = !on;
    btn.setAttribute("aria-expanded", String(on));
    if (on) panel.querySelector("[aria-current]")?.focus?.();
  };
  btn.onclick = () => open(panel.hidden);
  scrim.onclick = () => open(false);
  head.querySelector("button").onclick = () => open(false);
  addEventListener("keydown", e => { if (e.key === "Escape" && !panel.hidden) open(false); });
  // Where the button goes: the site's bar, a map's toolbar, or a corner of its own.
  const bar = document.querySelector(".appbar"), tools = document.querySelector(".bar .tools");
  if (bar) bar.append(btn);
  else if (tools) { btn.classList.add("in-tools"); tools.prepend(btn); }
  else { btn.style.cssText = "position:fixed;z-index:59;top:max(10px,env(safe-area-inset-top,0px));right:10px;background:var(--surface,#fff);box-shadow:0 2px 10px rgb(0 0 0 / 15%)"; document.body.append(btn); }
  document.body.append(scrim, panel);
  window.SiteNav = { MENU, render, open };
})();
