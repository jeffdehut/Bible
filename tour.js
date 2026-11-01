// A short tour of the reader for a first visit: the reader itself, finding a book and chapter,
// versions, marking words, then (in the menu) Connections, the Resource Room and the account.
// A light shines on each part in turn, with a card that says what it is; Back, Next, and Skip.
// Shown once after the welcome; "Take the tour" in About this project shows it again.
(() => {
  const T = s => (window.L && L.t ? L.t(s) : s);
  const q = s => document.querySelector(s);
  const visible = n => !!n && !n.hidden && n.getClientRects().length > 0;
  // The first verse number on the screen, below the bar.
  const verseOnScreen = () => [...document.querySelectorAll("#text .vn")].find(v => { const r = v.getBoundingClientRect(); return r.top > 90 && r.bottom < innerHeight - 160; });
  // A paragraph of the chapter on the screen (the tour never moves the reader from its place).
  const textOnScreen = () => [...document.querySelectorAll("#text .chap p")].find(p => { const r = p.getBoundingClientRect(); return r.height > 60 && r.top > 70 && r.top < innerHeight * 0.5; });
  // Opens or closes the menu; says whether it changed (then the sheet is still sliding).
  const menuOpen = on => {
    const m = q("#menu");
    if (on && m && m.hidden) { q("#open-menu")?.click(); return true; }
    if (!on && m && !m.hidden) { m.querySelector("[data-close]")?.click(); return true; }
    return false;
  };
  const STEPS = [
    { t: "The reader", d: "Read the Bible here. Keep scrolling and one chapter flows into the next. Tap the play button to listen.", at: () => textOnScreen() || q("#text"), menu: false },
    { t: "Go anywhere", d: "Tap the book and chapter to go to any book and chapter, or search for a passage like John 3:16.", at: () => q("#where"), menu: false },
    { t: "Versions", d: "Choose the version you read. Add a second one underneath to compare them verse by verse, even with the Hebrew and Greek.", at: () => q("#ver"), menu: false },
    { t: "Highlights and marks", d: "Tap a verse number, or hold a word, to choose words. A menu opens to highlight, underline, add a note, a sketch or a bookmark. Tap a verse to see its original words.", at: () => verseOnScreen() || q("#text .vn"), menu: false },
    { t: "Draw on the page", d: "Tap the pencil to write and draw right on the page, with a finger or a pen; tap it again when you're done. Two fingers scroll. There's room in the margins beside the text too: on a phone, slide the page sideways to write there.", at: () => q("#bar-draw"), menu: false },
    { t: "Connections", d: "Every chapter, person and place in the Bible, and the threads between them. Maps, the timeline and family trees are here too, in Explore.", at: () => q('#menu a[href$="graph.html"]'), menu: true },
    { t: "The Resource Room", d: "Teaching resources: The Complete Bible Story, three years of lessons; Felt Stories, to tell a story on a felt board; and maps.", at: () => q("#menu .menu-group.menu-resources"), wide: () => q("#menu ul.menu-resources"), menu: true },
    { t: "Keep it on every device", d: "Sign in to keep your highlights, notes, bookmarks and Felt Stories boards the same on your phone, tablet and computer. Reading never needs an account.", at: () => (visible(q("#open-account")) ? q("#open-account") : q("#menu .menu-group.menu-you")), menu: true },
    { t: "That's the tour", d: "You can take it again from About this project, in the menu. Enjoy reading!", at: () => null, menu: false },
  ];
  let i = 0, box = null, spot = null, card = null, onKey = null;
  function build() {
    box = document.createElement("div"); box.className = "tour";
    spot = document.createElement("div"); spot.className = "tour-spot";
    card = document.createElement("div"); card.className = "tour-card"; card.setAttribute("role", "dialog"); card.setAttribute("aria-modal", "true"); card.setAttribute("aria-live", "polite");
    box.append(spot, card);
    document.body.append(box);
    requestAnimationFrame(() => box.classList.add("in"));
    box.addEventListener("click", e => { if (e.target === box) next(); });
    onKey = e => { if (e.key === "Escape") end(); else if (e.key === "ArrowRight") next(); else if (e.key === "ArrowLeft") back(); };
    addEventListener("keydown", onKey, true);
    addEventListener("resize", place);
  }
  // Each step: the card fades out, its words change, and it fades in where the light has moved.
  let swapTimer = 0;
  function show() {
    clearTimeout(swapTimer);
    if (card.childElementCount) { card.classList.add("out"); swapTimer = setTimeout(fill, 170); } else fill();
  }
  function fill() {
    const s = STEPS[i];
    const moving = menuOpen(!!s.menu);
    card.innerHTML = "";
    const top = document.createElement("div"); top.className = "tour-top";
    const n = document.createElement("span"); n.className = "tour-n"; n.textContent = T("{n} of {all}").replace("{n}", i + 1).replace("{all}", STEPS.length);
    const x = document.createElement("button"); x.type = "button"; x.className = "tour-x"; x.setAttribute("aria-label", T("Skip the tour")); x.textContent = T("Skip");
    x.onclick = end;
    top.append(n, x);
    const h = document.createElement("h2"); h.textContent = T(s.t);
    const p = document.createElement("p"); p.textContent = T(s.d);
    const dots = document.createElement("div"); dots.className = "tour-dots";
    STEPS.forEach((_, k) => { const d = document.createElement("i"); if (k === i) d.className = "on"; dots.append(d); });
    const bar = document.createElement("div"); bar.className = "tour-bar";
    const b = document.createElement("button"); b.type = "button"; b.className = "tour-back"; b.textContent = T("Back"); b.onclick = back; b.hidden = i === 0;
    const f = document.createElement("button"); f.type = "button"; f.className = "tour-next"; f.textContent = T(i === STEPS.length - 1 ? "Start reading" : "Next"); f.onclick = next;
    bar.append(b, dots, f);
    card.append(top, h, p, bar);
    // In the menu, its item is brought into view once the sheet has opened; the reader stays put.
    const settle = () => {
      const target = s.at();
      if (target && s.menu) { const r = target.getBoundingClientRect(); if (r.top < 80 || r.bottom > innerHeight - 200) target.scrollIntoView({ block: "center" }); }
      place(); card.classList.remove("out"); f.focus({ preventScroll: true });
    };
    if (moving) setTimeout(settle, 420); else requestAnimationFrame(settle);
  }
  function place() {
    if (!box) return;
    const s = STEPS[i];
    const t = s.at(), w = s.wide ? s.wide() : null;
    let r = null;
    if (t && visible(t)) {
      r = t.getBoundingClientRect();
      if (w && visible(w)) { const r2 = w.getBoundingClientRect(); r = { left: Math.min(r.left, r2.left), top: Math.min(r.top, r2.top), right: Math.max(r.right, r2.right), bottom: Math.max(r.bottom, r2.bottom) }; }
    }
    const pad = 8;
    if (r) {
      Object.assign(spot.style, { left: r.left - pad + "px", top: r.top - pad + "px", width: r.right - r.left + 2 * pad + "px", height: r.bottom - r.top + 2 * pad + "px", opacity: 1 });
    } else Object.assign(spot.style, { left: innerWidth / 2 + "px", top: innerHeight / 2 + "px", width: "0px", height: "0px", opacity: 1 });
    // The card below the light, or above it where there is no room; in the middle with none.
    const cw = Math.min(360, innerWidth - 24), ch = card.offsetHeight;
    card.style.width = cw + "px";
    let top, left;
    if (!r) { top = (innerHeight - ch) / 2; left = (innerWidth - cw) / 2; }
    else {
      top = r.bottom + pad + 12;
      if (top + ch > innerHeight - 12) top = r.top - pad - 12 - ch;
      if (top < 12) top = Math.max(12, innerHeight - ch - 12);
      top = Math.min(top, innerHeight - ch - 12);
      left = Math.min(Math.max(12, (r.left + r.right) / 2 - cw / 2), innerWidth - cw - 12);
    }
    card.style.top = top + "px"; card.style.left = left + "px";
  }
  function next() { if (i < STEPS.length - 1) { i++; show(); } else end(); }
  function back() { if (i > 0) { i--; show(); } }
  function end() {
    menuOpen(false);
    try { localStorage.setItem("pe.toured", "1"); } catch (e) { /* storage */ }
    removeEventListener("keydown", onKey, true); removeEventListener("resize", place);
    const b = box; box = null;
    if (b) { b.classList.remove("in"); setTimeout(() => b.remove(), 320); }
    q("#where")?.focus();
  }
  function start() { if (box) return; i = 0; build(); show(); }
  const seen = () => { try { return localStorage.getItem("pe.toured") === "1"; } catch (e) { return true; } };
  window.Tour = { start, seen };
})();
