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
