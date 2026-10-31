// The site's panels: one kind of sheet, the same on every page.
//
// Any element with the class "ui-sheet" is a panel. On a phone it is a sheet that rises from the
// bottom, with a handle in the middle of its top edge: drag the handle (or the panel's title) up
// to open it to the full height of the screen, down to bring it back to half, and further down to
// close it. On a tablet or a computer it is a panel down the right-hand side, under the page's
// bar, always the same width. The menu, the reader's sheets and the cards of the web, the
// genealogy, the timeline and the maps are all such panels, so they open in the same place and
// move the same way everywhere.
//
//   <section class="ui-sheet" hidden>          a panel; shown and hidden with `hidden`
//     <div class="ui-grab"></div>              the handle (phones)
//     <header class="ui-head">…<button data-close>…</button></header>
//     …
//   </section>
//
// Options, as attributes: data-detent="full" opens it at full height on a phone (lists);
// data-size="wide" makes the side panel wide (parallel passages); data-tuck lets the panel tuck
// away to an edge instead of closing (cards beside a map or a web) — UI.tuck(el, true/false).
// Closing by dragging presses the panel's [data-close] button, so the page's own closing runs.
// The page can shift its content while a side panel is open: body gets "ui-panel-open" and the
// panel's width is in --ui-panel-w.
(() => {
  const PHONE = "(max-width: 759px)";
  const css = `
:root { --ui-panel-w: 400px; --ui-top: 0px; --ui-ease: cubic-bezier(.2, .8, .2, 1); }
.ui-sheet {
  position: fixed; z-index: 60; box-sizing: border-box; overflow: auto; overscroll-behavior: contain;
  background: var(--raised, var(--surface, #fff)); color: var(--ink, #161b26);
  transition: transform .32s var(--ui-ease), height .32s var(--ui-ease), display .32s allow-discrete, opacity .32s allow-discrete;
}
.ui-sheet[hidden] { display: none; }
.ui-grab, .ui-sheet > .grab { display: none; }
@media ${PHONE} {
  .ui-sheet {
    left: 0; right: 0; bottom: 0; width: auto; top: auto;
    max-height: calc(100dvh - var(--ui-top) - 8px); height: auto;
    border-radius: 20px 20px 0 0; border-top: 1px solid var(--line, #e4e2db); box-shadow: 0 -10px 30px rgb(22 27 38 / 16%);
    padding: 0 max(16px, env(safe-area-inset-right, 0px)) max(20px, env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px));
  }
  .ui-sheet:not([data-detent="full"]):not(.ui-full) { max-height: min(58dvh, calc(100dvh - var(--ui-top) - 8px)); }
  .ui-sheet[data-detent="full"], .ui-sheet.ui-full { height: calc(100dvh - var(--ui-top) - 8px); max-height: none; }
  .ui-sheet[hidden] { transform: translateY(100%); }
  @starting-style { .ui-sheet:not([hidden]) { transform: translateY(100%); } }
  .ui-grab, .ui-sheet > .grab {
    display: block; position: sticky; top: 0; z-index: 3; height: 22px; margin: 0 calc(-1 * max(16px, env(safe-area-inset-left, 0px)));
    background: inherit; cursor: grab; touch-action: none;
  }
  .ui-grab::before, .ui-sheet > .grab::before { content: ""; position: absolute; left: 50%; top: 8px; width: 38px; height: 5px; margin-left: -19px; border-radius: 5px; background: var(--line, #d6d3ca); }
  .ui-sheet.ui-dragging { transition: none; }
  .ui-sheet.tucked { transform: translateY(calc(100% - 92px)); }
}
@media not ${PHONE} {
  .ui-sheet {
    top: var(--ui-top); right: 0; bottom: 0; left: auto; width: var(--ui-panel-w); max-width: 100vw; height: auto; max-height: none;
    border-left: 1px solid var(--line, #e4e2db); border-radius: 0; box-shadow: -12px 0 32px rgb(22 27 38 / 10%);
    padding: 14px max(20px, env(safe-area-inset-right, 0px)) max(20px, env(safe-area-inset-bottom, 0px)) 20px;
  }
  .ui-sheet[data-size="wide"] { width: min(960px, calc(100vw - 48px)); }
  .ui-sheet[hidden] { transform: translateX(100%); }
  @starting-style { .ui-sheet:not([hidden]) { transform: translateX(100%); } }
  .ui-sheet.tucked { transform: translateX(calc(100% - 48px)); }
}
.ui-sheet.tucked > :not(.ui-tuck):not(.ui-grab):not(.grab) { opacity: .25; pointer-events: none; }
.ui-scrim { position: fixed; inset: 0; z-index: 59; background: rgb(10 14 24 / 32%); transition: opacity .32s, display .32s allow-discrete; }
.ui-scrim[hidden] { display: none; opacity: 0; }
@starting-style { .ui-scrim:not([hidden]) { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .ui-sheet, .ui-scrim { transition: none; } }
@media print { .ui-sheet, .ui-scrim { display: none !important; } }`;
  const style = document.createElement("style");
  style.id = "ui-css";
  style.textContent = css;
  document.head.append(style);

  const phone = () => matchMedia(PHONE).matches;
  // The panels sit under the page's bar, wherever it ends.
  function measureTop() {
    // The site's bar, or on a map its toolbar (the map's title tag beside it may run deeper).
    const bar = document.querySelector(".appbar") || document.querySelector(".bar .tools") || document.querySelector("header.bar, .topbar, .bar");
    const b = bar ? Math.max(0, bar.getBoundingClientRect().bottom) : 0;
    document.documentElement.style.setProperty("--ui-top", Math.round(b) + "px");
  }
  addEventListener("resize", measureTop);
  document.addEventListener("DOMContentLoaded", measureTop);

  // While a side panel is open, the page may make room for it.
  function sync() {
    const open = [...document.querySelectorAll(".ui-sheet:not([hidden]):not(.tucked)")];
    document.body.classList.toggle("ui-panel-open", open.length > 0 && !phone());
    document.body.classList.toggle("ui-sheet-open", open.length > 0);
    if (open.length && !phone()) {
      const w = Math.max(...open.map(s => s.getBoundingClientRect().width));
      document.documentElement.style.setProperty("--ui-panel-open-w", w + "px");
    }
  }
  const watch = new MutationObserver(list => {
    for (const m of list) if (m.target.classList && m.target.classList.contains("ui-sheet")) {
      // (only when there is something to change: classList.remove writes the attribute even if
      // nothing changes, which would wake this watcher again)
      if (m.target.hidden) { if (m.target.classList.contains("ui-full")) m.target.classList.remove("ui-full"); }
      else measureTop();
    }
    sync();
  });
  document.addEventListener("DOMContentLoaded", () => watch.observe(document.body, { subtree: true, attributes: true, attributeFilter: ["hidden", "class"] }));

  function close(el) {
    const btn = el.querySelector("[data-close], .close");
    if (btn) btn.click(); else el.hidden = true;
  }
  function tuck(el, on) {
    el.classList.toggle("tucked", on);
    el.dispatchEvent(new CustomEvent("ui:tuck", { detail: on }));
    sync();
  }

  // Dragging the handle, or the panel's title, on a phone.
  let drag = null;
  document.addEventListener("pointerdown", ev => {
    if (!phone() || ev.button > 0) return;
    const sheet = ev.target.closest(".ui-sheet");
    if (!sheet) return;
    const handle = ev.target.closest(".ui-grab, .grab, .ui-head, .sheet-head");
    if (!handle || ev.target.closest("button, a, input, textarea, select, label")) return;
    const r = sheet.getBoundingClientRect();
    drag = { sheet, y0: ev.clientY, h0: r.height, moved: false, id: ev.pointerId, full: innerHeight - parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--ui-top")) - 8 };
  });
  addEventListener("pointermove", ev => {
    if (!drag || ev.pointerId !== drag.id) return;
    const dy = ev.clientY - drag.y0;
    if (!drag.moved && Math.abs(dy) < 6) return;
    if (!drag.moved) { drag.moved = true; drag.sheet.classList.add("ui-dragging"); drag.sheet.style.maxHeight = "none"; }
    const h = Math.max(60, Math.min(drag.full, drag.h0 - dy));
    drag.sheet.style.height = h + "px";
  }, { passive: true });
  function release(ev) {
    if (!drag || (ev && ev.pointerId !== drag.id)) return;
    const { sheet, moved, h0, full } = drag;
    drag = null;
    sheet.classList.remove("ui-dragging");
    if (!moved) { if (sheet.classList.contains("tucked")) tuck(sheet, false); return; }
    const h = sheet.getBoundingClientRect().height;
    sheet.style.height = ""; sheet.style.maxHeight = "";
    const half = Math.min(innerHeight * 0.58, full);
    if (h < Math.min(h0, half) * 0.6) {
      if (sheet.hasAttribute("data-tuck")) tuck(sheet, true); else close(sheet);
    } else if (h > (half + full) / 2 || (h > h0 + 40 && h > half)) {
      sheet.classList.add("ui-full");
    } else {
      sheet.classList.remove("ui-full");
    }
  }
  addEventListener("pointerup", release);
  // A tucked panel comes back when it is tapped anywhere (its own tuck button aside).
  document.addEventListener("click", ev => {
    const sheet = ev.target.closest && ev.target.closest(".ui-sheet.tucked");
    if (!sheet || ev.target.closest(".ui-tuck")) return;
    ev.preventDefault(); ev.stopPropagation();
    tuck(sheet, false);
  }, true);
  addEventListener("pointercancel", release);

  window.UI = {
    phone, close, tuck, sync, measureTop,
    open(el) { el.classList.remove("tucked"); el.hidden = false; },
    // A scrim behind modal panels; pages without their own use this one.
    scrim(on, onclick) {
      let s = document.getElementById("ui-scrim");
      if (!s) { s = document.createElement("div"); s.id = "ui-scrim"; s.className = "ui-scrim"; s.hidden = true; document.body.append(s); }
      s.onclick = onclick || null;
      s.hidden = !on;
    },
  };
})();

// The site's look, the same family on every page: its two typefaces, and a theme of colors that
// reaches every page beside light and dark (UI.season). The themes follow the seasons of the
// year: each sets the paper, the ink and the accent, in light and in dark. "classic" is the
// site's own colors, which every page defines; a season sets them over the page's own.
// Also here, a little motion shared by every page: pages rise in, buttons give under a press,
// and the colors ease from one theme to the next. None of it runs for readers who ask for less.
(() => {
  const SEASONS = {
    spring: {
      light: { bg: "#f7faf3", surface: "#ffffff", raised: "#ffffff", ink: "#17251b", muted: "#55665a", faint: "#8b9a8e", line: "#dbe6d4", lapis: "#3b7a4b", "lapis-soft": "#e1efdf", gold: "#b0557c", "gold-soft": "#f8e4ec" },
      dark: { bg: "#0d140f", surface: "#131c15", raised: "#17221a", ink: "#e5efe6", muted: "#a2b4a6", faint: "#6d8172", line: "#243328", lapis: "#8fd3a0", "lapis-soft": "#1b3322", gold: "#eba0c0", "gold-soft": "#33202a" },
    },
    summer: {
      light: { bg: "#f6f9fc", surface: "#ffffff", raised: "#ffffff", ink: "#12202c", muted: "#526273", faint: "#8796a4", line: "#dbe5ee", lapis: "#1c6db3", "lapis-soft": "#e0edf9", gold: "#bf8200", "gold-soft": "#fbefd2" },
      dark: { bg: "#0a121b", surface: "#101b26", raised: "#152230", ink: "#e5eef6", muted: "#9db0c2", faint: "#687c90", line: "#213346", lapis: "#7cc1f7", "lapis-soft": "#14304b", gold: "#f3c24f", "gold-soft": "#33280e" },
    },
    autumn: {
      light: { bg: "#fbf6ee", surface: "#fffdf9", raised: "#fffdf9", ink: "#2a1c12", muted: "#6d5948", faint: "#a08b78", line: "#eadccd", lapis: "#a3461d", "lapis-soft": "#f6e3d6", gold: "#a8760c", "gold-soft": "#f6ead0" },
      dark: { bg: "#17100b", surface: "#1f1610", raised: "#261c14", ink: "#f2e6d9", muted: "#bca794", faint: "#86705d", line: "#3a2b1f", lapis: "#f2a173", "lapis-soft": "#3b2215", gold: "#e8b955", "gold-soft": "#33260f" },
    },
    winter: {
      light: { bg: "#f4f6f9", surface: "#ffffff", raised: "#ffffff", ink: "#131a25", muted: "#535f73", faint: "#8a94a6", line: "#dde3ec", lapis: "#2c5a8c", "lapis-soft": "#e2e9f4", gold: "#5f7896", "gold-soft": "#e6ecf3" },
      dark: { bg: "#090d14", surface: "#0f151f", raised: "#131b27", ink: "#e8eef7", muted: "#a5b0c3", faint: "#6e7a90", line: "#222c3c", lapis: "#a9c9f2", "lapis-soft": "#18273f", gold: "#c3d1e6", "gold-soft": "#1d2635" },
    },
  };
  const vars = p => Object.entries(p).map(([k, v]) => `--${k}: ${v};`).join(" ") + ` --accent: ${p.lapis};`;
  let css = "";
  for (const [name, s] of Object.entries(SEASONS)) {
    css += `html[data-season="${name}"]:root { ${vars(s.light)} }\n`;
    css += `@media (prefers-color-scheme: dark) { html[data-season="${name}"]:root:not([data-theme="light"]) { ${vars(s.dark)} } }\n`;
    css += `html[data-season="${name}"][data-theme="dark"]:root { ${vars(s.dark)} }\n`;
  }
  css += `
:root { --read: "Frank Ruhl Libre", "Noto Serif", Georgia, serif; --sans: "Libre Franklin", system-ui, -apple-system, "Segoe UI", sans-serif; }
html[data-season] body { transition: background-color .45s ease, color .45s ease; }
html.ui-theming *, html.ui-theming *::before, html.ui-theming *::after { transition: background-color .45s ease, color .45s ease, border-color .45s ease, fill .45s ease, stroke .45s ease !important; }
@keyframes ui-rise { from { opacity: 0; transform: translateY(8px); } }
@keyframes ui-pop { 0% { transform: scale(.4); opacity: 0; } 70% { transform: scale(1.15); } }
@keyframes ui-wash { from { background-color: transparent; box-shadow: none; } }
@media (prefers-reduced-motion: no-preference) {
  body > main, body > .page, body > #parts { animation: ui-rise .5s cubic-bezier(.2, .8, .2, 1) both; }
  :where(button, .btn, a.act, .chip, .swatch, .pen, .sitenav .menu a, .menu a, .menu button, .book, .web-link):active:not(:disabled) { transform: scale(.96); transition: transform .08s ease; }
  :where(.btn, .chip, .book, .glance li, .about > div, .panel, .sitenav .menu a, .menu a, .menu button) { transition: transform .18s ease, box-shadow .18s ease, background-color .18s ease, border-color .18s ease; }
  :where(.book, .glance li, .about > div):hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgb(0 0 0 / 8%); }
  .ui-sheet:not([hidden]) :where(.menu li, .glance li, .about > div, .ver-list li) { animation: ui-rise .38s cubic-bezier(.2, .8, .2, 1) both; }
  ${Array.from({ length: 14 }, (_, i) => `.ui-sheet:not([hidden]) :where(.menu li, .ver-list li):nth-child(${i + 1}), :where(.glance, .about) > :nth-child(${i + 1}) { animation-delay: ${i * 22}ms; }`).join("\n  ")}
  /* No fill mode: if a browser doesn't run the animation, the mark is simply there. */
  .fresh { animation: ui-wash .6s ease; }
  .sticky.fresh, .emo.fresh { animation: ui-pop .45s cubic-bezier(.2, .8, .2, 1); }
}`;
  const style = document.createElement("style");
  style.id = "ui-theme";
  style.textContent = css;
  document.head.append(style);
  // The family's typefaces, on pages that don't load them already.
  if (![...document.querySelectorAll('link[href*="fonts.googleapis"]')].some(l => /Libre\+Franklin/.test(l.href) && /Frank\+Ruhl/.test(l.href))) {
    const l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300..700&family=Libre+Franklin:wght@400;500;600;700&display=swap";
    document.head.append(l);
  }

  const KEY = "pe.settings";
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } };
  function apply(name, animate) {
    const root = document.documentElement;
    if (animate) { root.classList.add("ui-theming"); setTimeout(() => root.classList.remove("ui-theming"), 600); }
    if (SEASONS[name]) root.dataset.season = name; else delete root.dataset.season;
    // The browser's own bar takes the page's paper.
    requestAnimationFrame(() => {
      const bg = getComputedStyle(root).getPropertyValue("--bg").trim();
      if (bg) for (const m of document.querySelectorAll('meta[name="theme-color"]')) m.content = bg;
    });
  }
  apply(read().season);
  // Another page, or the reader's viewer, changed it: follow.
  addEventListener("storage", e => { if (e.key === KEY) apply(read().season, true); });
  window.UI = Object.assign(window.UI || {}, {
    SEASONS: Object.keys(SEASONS),
    season: () => read().season || "classic",
    setSeason(name) {
      const s = read();
      s.season = SEASONS[name] ? name : "classic";
      try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* storage unavailable */ }
      apply(s.season, true);
    },
    seasonColors: name => SEASONS[name],
  });
})();
