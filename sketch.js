// Sketches: drawings in ink, kept as vectors. The reader uses them two ways: a sketch on a small
// square of paper (a 3 × 3 inch sticky note), kept with the words it was drawn for and gathered
// in the sketchbook; and ink drawn over the text itself (index.html, "Ink on the page"), which
// uses the same pen.
//
// A stroke is a list of points [x, y, pressure, ...]. It is drawn as a filled outline whose width
// follows the pressure (or, without a pen, the speed: slower is broader), smoothed as it is drawn
// and tapered at its ends, so it reads as ink from a good pen rather than a line of pixels. The
// eraser rubs out what it passes over: a stroke it crosses is cut in two.
//
// Kept as text: "1|" then each stroke as "color,size,x,y,p,dx,dy,dp,..." (whole numbers: tenths
// of a unit, pressure in fifteenths, each point after the first as the change from the one
// before), strokes separated by ";". A sketch's square is 288 units (3 inches at 96 per inch).
(() => {
  const PAD = 288;
  const PAPER = "#fbf8ef";
  // Inks, the same on the paper in every theme. "ink" is the pen's own black (on the page, the
  // text's color, so it shows in a dark theme too).
  // Sketches keep each stroke's color as its place in KEYS, so new colors go at the end; PICK is
  // the order they are offered in: black, then the rainbow (brown stays for older sketches).
  const COLORS = { ink: "#1f2430", blue: "#1f6fe0", red: "#e0312b", green: "#1f9e45", purple: "#b03fc6", brown: "#9a6a1c", orange: "#ee7d12", yellow: "#e8b100", violet: "#9b3fd8", indigo: "#3b44c4" };
  const KEYS = Object.keys(COLORS);
  const PICK = ["ink", "red", "orange", "yellow", "green", "blue", "indigo", "violet"];
  const SIZES = [1.5, 2.8, 5.2];          // pen widths, in units
  const ERASERS = [4, 9, 18];             // eraser radii: small, medium, large

  /* ---------- The ink: an outline for a stroke ---------- */
  const r2 = n => Math.round(n * 100) / 100;
  function outline(p, size) {
    const n = p.length / 3;
    if (!n) return "";
    const W = i => size * (0.38 + 0.62 * p[i * 3 + 2]);
    const cum = [0];
    for (let i = 1; i < n; i++) cum.push(cum[i - 1] + Math.hypot(p[i * 3] - p[i * 3 - 3], p[i * 3 + 1] - p[i * 3 - 2]));
    const total = cum[n - 1];
    if (n === 1 || total < 0.6) {
      const r = Math.max(0.5, W(0) * 0.55), x = p[0], y = p[1];
      return `M${r2(x - r)} ${r2(y)}a${r2(r)} ${r2(r)} 0 1 0 ${r2(2 * r)} 0a${r2(r)} ${r2(r)} 0 1 0 ${r2(-2 * r)} 0Z`;
    }
    const L = [], R = [], w = [];
    for (let i = 0; i < n; i++) {
      const a = Math.max(0, i - 1), b = Math.min(n - 1, i + 1);
      let dx = p[b * 3] - p[a * 3], dy = p[b * 3 + 1] - p[a * 3 + 1];
      const len = Math.hypot(dx, dy) || 1;
      dx /= len; dy /= len;
      // A gentle taper: a little at the start, more at the lift of the pen.
      const t = Math.min(1, cum[i] / (size * 1.2 + 0.5), (total - cum[i]) / (size * 2.4 + 1));
      const wi = W(i) * (0.55 + 0.45 * t) / 2;
      w.push(wi);
      L.push(p[i * 3] - dy * wi, p[i * 3 + 1] + dx * wi);
      R.push(p[i * 3] + dy * wi, p[i * 3 + 1] - dx * wi);
    }
    const side = (pts, out) => {
      const m = pts.length / 2;
      for (let i = 1; i < m - 1; i++) {
        const mx = (pts[i * 2] + pts[i * 2 + 2]) / 2, my = (pts[i * 2 + 1] + pts[i * 2 + 3]) / 2;
        out.push(`Q${r2(pts[i * 2])} ${r2(pts[i * 2 + 1])} ${r2(mx)} ${r2(my)}`);
      }
      out.push(`L${r2(pts[m * 2 - 2])} ${r2(pts[m * 2 - 1])}`);
    };
    const out = [`M${r2(L[0])} ${r2(L[1])}`];
    side(L, out);
    const re = w[n - 1], rs = w[0];
    // Round caps, bulging out past the ends (sweep 0: from one side, round the tip, to the other).
    out.push(`A${r2(re)} ${r2(re)} 0 0 0 ${r2(R[n * 2 - 2])} ${r2(R[n * 2 - 1])}`);
    const back = [];
    for (let i = n - 1; i >= 0; i--) back.push(R[i * 2], R[i * 2 + 1]);
    side(back, out);
    out.push(`A${r2(rs)} ${r2(rs)} 0 0 0 ${r2(L[0])} ${r2(L[1])}Z`);
    return out.join("");
  }

  /* ---------- Keeping strokes as text ---------- */
  // Fewer points where a line runs straight (Ramer–Douglas–Peucker), so a sketch stays small.
  function simplify(p, tol) {
    const n = p.length / 3;
    if (n < 3) return p.slice();
    const keep = new Uint8Array(n); keep[0] = keep[n - 1] = 1;
    const stack = [[0, n - 1]];
    while (stack.length) {
      const [a, b] = stack.pop();
      const ax = p[a * 3], ay = p[a * 3 + 1], bx = p[b * 3], by = p[b * 3 + 1];
      const len = Math.hypot(bx - ax, by - ay) || 1e-9;
      let far = -1, fd = tol;
      for (let i = a + 1; i < b; i++) {
        const d = Math.abs((bx - ax) * (ay - p[i * 3 + 1]) - (ax - p[i * 3]) * (by - ay)) / len;
        const dp = Math.abs(p[i * 3 + 2] - (p[a * 3 + 2] + p[b * 3 + 2]) / 2) * 4;   // keep changes of pressure too
        if (d + dp > fd) { fd = d + dp; far = i; }
      }
      if (far > 0) { keep[far] = 1; stack.push([a, far], [far, b]); }
    }
    const out = [];
    for (let i = 0; i < n; i++) if (keep[i]) out.push(p[i * 3], p[i * 3 + 1], p[i * 3 + 2]);
    return out;
  }
  function encode(strokes) {
    return "1|" + strokes.filter(s => s.p.length).map(s => {
      const p = simplify(s.p, 0.18), out = [Math.max(0, KEYS.indexOf(s.c)), s.s];
      let px = 0, py = 0, pp = 0;
      for (let i = 0; i < p.length; i += 3) {
        const x = Math.round(p[i] * 10), y = Math.round(p[i + 1] * 10), q = Math.round(Math.max(0, Math.min(1, p[i + 2])) * 15);
        out.push(x - px, y - py, q - pp); px = x; py = y; pp = q;
      }
      return out.join(",");
    }).join(";");
  }
  function decode(text) {
    if (!text || typeof text !== "string" || !text.startsWith("1|")) return [];
    return text.slice(2).split(";").filter(Boolean).map(s => {
      const v = s.split(",").map(Number);
      const st = { c: KEYS[v[0]] || "ink", s: Math.max(0, Math.min(2, v[1] | 0)), p: [] };
      let x = 0, y = 0, q = 0;
      for (let i = 2; i + 2 < v.length + 1; i += 3) { x += v[i]; y += v[i + 1]; q += v[i + 2]; st.p.push(x / 10, y / 10, q / 15); }
      return st;
    });
  }

  /* ---------- The eraser: rub out what it passes over ---------- */
  const distSeg = (px, py, ax, ay, bx, by) => {
    const dx = bx - ax, dy = by - ay, l = dx * dx + dy * dy;
    const t = l ? Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / l)) : 0;
    return Math.hypot(px - ax - t * dx, py - ay - t * dy);
  };
  // Points close enough together that a cut falls where the eraser was.
  function densify(p, step) {
    const out = [p[0], p[1], p[2]];
    for (let i = 3; i < p.length; i += 3) {
      const d = Math.hypot(p[i] - p[i - 3], p[i + 1] - p[i - 2]);
      const k = Math.ceil(d / step);
      for (let j = 1; j < k; j++) {
        const t = j / k;
        out.push(p[i - 3] + (p[i] - p[i - 3]) * t, p[i - 2] + (p[i + 1] - p[i - 2]) * t, p[i - 1] + (p[i + 2] - p[i - 1]) * t);
      }
      out.push(p[i], p[i + 1], p[i + 2]);
    }
    return out;
  }
  // The strokes, with the eraser's path from (ax, ay) to (bx, by) of radius r rubbed out.
  // Returns the new list, or null if nothing was touched.
  function erase(strokes, ax, ay, bx, by, r, widthOf = s => SIZES[s.s]) {
    let changed = false;
    const out = [];
    for (const st of strokes) {
      const reach = r + widthOf(st) / 2;
      // Quick test: is any point of it near the eraser's path?
      let near = false;
      for (let i = 0; i < st.p.length; i += 3) if (distSeg(st.p[i], st.p[i + 1], ax, ay, bx, by) < reach + 6) { near = true; break; }
      if (!near) { out.push(st); continue; }
      const p = densify(st.p, Math.max(0.6, r / 3));
      let run = [], cut = false;
      const flush = () => { if (run.length >= 3) out.push({ ...st, p: run }); run = []; };
      for (let i = 0; i < p.length; i += 3) {
        if (distSeg(p[i], p[i + 1], ax, ay, bx, by) < reach) { cut = true; flush(); }
        else run.push(p[i], p[i + 1], p[i + 2]);
      }
      if (!cut) { out.push(st); continue; }
      flush();
      changed = true;
    }
    return changed ? out : null;
  }

  /* ---------- The pen: smoothed points with pressure, from pointer events ---------- */
  // pen(toLocal) gives { start(ev), move(ev), points } for one stroke; toLocal(ev) -> [x, y].
  let sawPen = false;
  function pen(toLocal, minGap = 0.5) {
    let p = [], last = null, lastT = 0, pr = 0.6;
    const add = (ev, first) => {
      const [x, y] = toLocal(ev);
      const now = ev.timeStamp || performance.now();
      if (ev.pointerType === "pen" && ev.pressure > 0) pr = pr * 0.4 + ev.pressure * 0.6;
      else if (!first) {
        const v = last ? Math.hypot(x - last[0], y - last[1]) / Math.max(1, now - lastT) : 0;
        pr = pr * 0.8 + Math.max(0.35, Math.min(1, 0.95 - v * 0.35)) * 0.2;
      }
      if (first) { p = [x, y, pr]; last = [x, y]; lastT = now; return; }
      // Streamlined: each point drawn halfway toward the pointer, which smooths the hand's jitter.
      const sx = last[0] + (x - last[0]) * 0.55, sy = last[1] + (y - last[1]) * 0.55;
      if (Math.hypot(sx - last[0], sy - last[1]) < minGap) return;
      p.push(sx, sy, pr); last = [sx, sy]; lastT = now;
    };
    return {
      start(ev) { if (ev.pointerType === "pen") sawPen = true; pr = ev.pointerType === "pen" && ev.pressure > 0 ? ev.pressure : 0.6; add(ev, true); },
      move(ev) { const all = ev.getCoalescedEvents ? ev.getCoalescedEvents() : []; for (const e of all.length ? all : [ev]) add(e, false); },
      end(ev) { if (ev && ev.type === "pointerup") { const [x, y] = toLocal(ev); if (last && Math.hypot(x - last[0], y - last[1]) > minGap) p.push(x, y, pr * 0.9); } },
      get points() { return p; },
    };
  }

  // On an iPad the system may take a pencil's stroke for a scroll and cancel it; holding the
  // pencil's own touches keeps them for drawing (a finger still scrolls).
  // fingers: also hold a finger's touches ("one" for one finger at a time, "all" for any).
  function holdStylus(el, when = () => true, fingers = () => null) {
    const hold = e => {
      if (!when()) return;
      const f = fingers();
      if ([...e.changedTouches].some(t => t.touchType === "stylus") || f === "all" || (f === "one" && e.touches.length === 1)) e.preventDefault();
    };
    el.addEventListener("touchstart", hold, { passive: false });
    el.addEventListener("touchmove", hold, { passive: false });
  }

  /* ---------- Drawing into SVG ---------- */
  const NS = "http://www.w3.org/2000/svg";
  const svgEl = (tag, attrs = {}) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); return n; };
  const colorOf = (c, onPage) => (onPage && c === "ink" ? "currentColor" : COLORS[c] || COLORS.ink);
  // The paths of a sketch: [{d, color}], in its own units.
  const paths = data => decode(data).map(s => ({ d: outline(s.p, SIZES[s.s]), color: COLORS[s.c] || COLORS.ink }));
  // A sketch as a small picture on its paper.
  function picture(data, { size = 96, paper = true } = {}) {
    const svg = svgEl("svg", { viewBox: `0 0 ${PAD} ${PAD}`, width: size, height: size, class: "sk-pic", "aria-hidden": "true" });
    if (paper) svg.append(svgEl("rect", { width: PAD, height: PAD, fill: PAPER }));
    for (const x of paths(data)) svg.append(svgEl("path", { d: x.d, fill: x.color }));
    return svg;
  }

  /* ---------- The pad ---------- */
  const STYLE = `
.sk-scrim { position: fixed; inset: 0; z-index: 90; display: grid; place-items: center; padding: 12px; background: rgb(15 18 26 / 45%); animation: sk-in .16s ease-out; }
@keyframes sk-in { from { opacity: 0; } }
.sk-box { width: min(100%, 360px); max-height: 100%; overflow: auto; background: var(--surface, #fff); color: var(--ink, #161b26); border-radius: 18px; padding: 14px 14px 12px; box-shadow: 0 18px 50px rgb(0 0 0 / 30%); display: grid; gap: 10px; }
.sk-head { display: flex; align-items: flex-start; gap: 8px; }
.sk-head .t { flex: 1; min-width: 0; }
.sk-head b { display: block; font: 600 16px/1.25 var(--sans, system-ui, sans-serif); }
.sk-head b a { color: inherit; text-decoration: none; }
.sk-head b a:hover { color: var(--lapis, #2646a1); }
.sk-head small { display: block; margin-top: 2px; font: 400 13px/1.35 var(--read, Georgia, serif); color: var(--muted, #5b6475); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sk-x { flex: none; width: 34px; height: 34px; border: 0; border-radius: 10px; background: transparent; color: inherit; font-size: 18px; cursor: pointer; }
.sk-x:hover { background: var(--lapis-soft, #e7ecf8); }
.sk-paper { position: relative; justify-self: center; width: min(288px, calc(100vw - 72px)); aspect-ratio: 1; background: ${PAPER}; border-radius: 3px;
  box-shadow: 0 1px 2px rgb(0 0 0 / 12%), 0 6px 16px rgb(60 45 10 / 16%); touch-action: none; cursor: crosshair; overflow: hidden; }
.sk-paper svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
.sk-paper.erasing { cursor: cell; }
.sk-ring { position: absolute; border: 1.5px solid rgb(31 36 48 / 45%); border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); display: none; }
.sk-tools { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 6px; }
.sk-tools .sep { width: 1px; height: 24px; background: var(--line, #e4e2db); margin: 0 2px; }
.sk-tools .brk { flex-basis: 100%; height: 0; }
.sk-bar .sk-tools .brk { flex-basis: auto; width: 1px; height: 24px; background: var(--line, #e4e2db); }
@media (max-width: 520px) { .sk-bar .sk-tools .brk { flex-basis: 100%; width: auto; height: 0; background: none; } }
.sk-c { width: 24px; height: 24px; margin: 2px; border-radius: 50%; border: 0; cursor: pointer; padding: 0; background: var(--c); transition: box-shadow .12s; }
.sk-c[aria-pressed="true"] { box-shadow: 0 0 0 2.5px var(--surface, #fff), 0 0 0 4.5px var(--c); }
.sk-b { display: inline-grid; place-items: center; min-width: 34px; height: 34px; padding: 0 6px; border: 1px solid transparent; border-radius: 10px; background: transparent; color: inherit; cursor: pointer; }
.sk-b:hover { background: var(--lapis-soft, #e7ecf8); }
.sk-b[aria-pressed="true"] { background: var(--lapis-soft, #e7ecf8); border-color: var(--lapis, #2646a1); color: var(--lapis, #2646a1); }
.sk-b:disabled { opacity: .35; cursor: default; background: transparent; }
.sk-b svg { width: 20px; height: 20px; }
.sk-dot { display: block; border-radius: 50%; background: currentColor; }
.sk-dot.ring { background: transparent; border: 1.6px solid currentColor; }
.sk-foot { display: flex; gap: 8px; justify-content: flex-end; flex-wrap: wrap; }
.sk-foot button { border: 1px solid var(--line, #e4e2db); background: var(--surface, #fff); color: inherit; border-radius: 10px; padding: 8px 14px; font: 600 14px/1.2 var(--sans, system-ui, sans-serif); cursor: pointer; }
.sk-foot button.solid { background: var(--lapis, #2646a1); border-color: var(--lapis, #2646a1); color: var(--surface, #fff); }
.sk-foot button.del { margin-inline-end: auto; color: #b3261e; }
.sk-foot button[hidden] { display: none; }
.sk-pic { display: block; border-radius: 2px; }
.sk-bar { position: fixed; z-index: 70; left: 10px; right: 10px; margin-inline: auto; width: fit-content; bottom: max(14px, env(safe-area-inset-bottom)); display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 6px;
  max-width: calc(100vw - 20px); padding: 8px 10px; border-radius: 16px; background: var(--surface, #fff); color: var(--ink, #161b26); border: 1px solid var(--line, #e4e2db); box-shadow: 0 10px 30px rgb(0 0 0 / 22%); }
.sk-bar .done { border: 0; border-radius: 10px; padding: 8px 14px; background: var(--lapis, #2646a1); color: var(--surface, #fff); font: 600 14px/1.2 var(--sans, system-ui, sans-serif); cursor: pointer; }
.sk-bar .sk-c[data-c="ink"] { --c: var(--ink, #161b26) !important; }
`;
  function css() {
    if (document.getElementById("sk-style")) return;
    const st = document.createElement("style"); st.id = "sk-style"; st.textContent = STYLE; document.head.append(st);
  }
  const ICON = {
    pen: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16Z"/><path d="m13.5 6.5 4 4"/></svg>',
    eraser: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7 21-4.3-4.3a1.5 1.5 0 0 1 0-2.1L13.6 3.7a1.5 1.5 0 0 1 2.1 0l4.6 4.6a1.5 1.5 0 0 1 0 2.1L10 21Z"/><path d="M22 21H7M5 12l7 7"/></svg>',
    undo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg>',
    redo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 14 5-5-5-5"/><path d="M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/></svg>',
    clear: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/></svg>',
  };
  const T = s => (window.I18N ? window.I18N.t(s) : s);
  const btn = (cls, attrs, html) => {
    const b = document.createElement("button");
    b.type = "button"; b.className = cls;
    for (const [k, v] of Object.entries(attrs)) b.setAttribute(k, v);
    if (html) b.innerHTML = html;
    return b;
  };
  // The tools: colors, three sizes, pen or eraser, undo and redo (and clear on the pad). Shared by
  // the pad and the bar for ink on the page. state: {c, s, erase}; onChange() after each choice.
  function toolbar(state, { undo, redo, clear, page }) {
    const box = document.createElement("div");
    box.className = "sk-tools";
    const render = () => {
      box.replaceChildren();
      for (const c of PICK) {
        const b = btn("sk-c", { "data-c": c, "aria-label": T(c === "ink" ? "Black" : c[0].toUpperCase() + c.slice(1)), title: T(c === "ink" ? "Black" : c[0].toUpperCase() + c.slice(1)), "aria-pressed": String(!state.erase && state.c === c) });
        b.style.setProperty("--c", COLORS[c]);
        b.onclick = () => { state.c = c; state.erase = false; render(); state.changed?.(); };
        box.append(b);
      }
      box.append(Object.assign(document.createElement("span"), { className: "sep" }));
      SIZES.forEach((w, i) => {
        // The pen's sizes, or, with the eraser in hand, the eraser's own (shown as rings).
        const name = T((state.erase ? ["Small eraser", "Medium eraser", "Large eraser"] : ["Fine", "Medium", "Broad"])[i]);
        const b = btn("sk-b", { "aria-label": name, title: name, "aria-pressed": String((state.erase ? state.es : state.s) === i) });
        const d = state.erase ? 8 + i * 5 : 4 + i * 4;
        b.innerHTML = `<span class="sk-dot${state.erase ? " ring" : ""}" style="width:${d}px;height:${d}px"></span>`;
        b.onclick = () => { if (state.erase) state.es = i; else state.s = i; render(); state.changed?.(); };
        box.append(b);
      });
      box.append(Object.assign(document.createElement("span"), { className: "brk" }));
      const p = btn("sk-b", { "aria-label": T("Pen"), title: T("Pen"), "aria-pressed": String(!state.erase) }, ICON.pen);
      p.onclick = () => { state.erase = false; render(); state.changed?.(); };
      const e = btn("sk-b", { "aria-label": T("Eraser"), title: T("Eraser"), "aria-pressed": String(!!state.erase) }, ICON.eraser);
      e.onclick = () => { state.erase = true; render(); state.changed?.(); };
      const u = btn("sk-b", { "aria-label": T("Undo"), title: T("Undo") }, ICON.undo);
      u.disabled = !undo.can(); u.onclick = () => { undo.run(); render(); };
      const r = btn("sk-b", { "aria-label": T("Redo"), title: T("Redo") }, ICON.redo);
      r.disabled = !redo.can(); r.onclick = () => { redo.run(); render(); };
      box.append(p, e, u, r);
      if (clear) {
        const x = btn("sk-b", { "aria-label": T("Clear the page"), title: T("Clear the page") }, ICON.clear);
        x.onclick = () => { clear(); render(); };
        box.append(x);
      }
    };
    render();
    box.refresh = render;
    if (page) box.classList.add("page");
    return box;
  }
  // A history of states for undo and redo.
  function history(get, set, onMove) {
    const back = [], fwd = [];
    return {
      mark() { back.push(get()); if (back.length > 60) back.shift(); fwd.length = 0; },
      undo: { can: () => back.length > 0, run() { if (!back.length) return; fwd.push(get()); set(back.pop()); onMove?.(); } },
      redo: { can: () => fwd.length > 0, run() { if (!fwd.length) return; back.push(get()); set(fwd.pop()); onMove?.(); } },
    };
  }
  const tools = { c: "ink", s: 0, es: 1, erase: false };
  try { Object.assign(tools, JSON.parse(localStorage.getItem("pe.sketchTools")) || {}, { erase: false }); } catch (e) { /* storage unavailable */ }
  if (!PICK.includes(tools.c)) tools.c = { purple: "violet", brown: "orange" }[tools.c] || "ink";
  const keepTools = () => { try { localStorage.setItem("pe.sketchTools", JSON.stringify({ c: tools.c, s: tools.s, es: tools.es })); } catch (e) { /* storage unavailable */ } };

  // Open the pad. opts: {title, href, sub, data, onSave(data or null), onShare(data), onDelete, onGo}.
  function open(opts) {
    css();
    let strokes = decode(opts.data);
    const scrim = document.createElement("div");
    scrim.className = "sk-scrim";
    const box = document.createElement("div");
    box.className = "sk-box"; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-label", T("Sketch"));
    const head = document.createElement("div"); head.className = "sk-head";
    const t = document.createElement("div"); t.className = "t";
    const b = document.createElement("b");
    if (opts.onGo) { const a = document.createElement("a"); a.href = "#"; a.textContent = opts.title || T("Sketch"); a.title = T("Read the passage"); a.onclick = ev => { ev.preventDefault(); close(); opts.onGo(); }; b.append(a); }
    else b.textContent = opts.title || T("Sketch");
    t.append(b);
    if (opts.sub) { const s = document.createElement("small"); s.textContent = opts.sub; s.title = opts.sub; t.append(s); }
    const x = btn("sk-x", { "aria-label": T("Close") }, "✕");
    head.append(t, x);
    const paper = document.createElement("div"); paper.className = "sk-paper";
    const svg = svgEl("svg", { viewBox: `0 0 ${PAD} ${PAD}` });
    const live = svgEl("path");
    const ring = document.createElement("div"); ring.className = "sk-ring";
    paper.append(svg, ring);
    const draw = () => {
      svg.replaceChildren(...strokes.map(s => svgEl("path", { d: outline(s.p, SIZES[s.s]), fill: COLORS[s.c] || COLORS.ink })), live);
    };
    const hist = history(() => strokes.map(s => ({ ...s, p: s.p.slice() })), v => { strokes = v; draw(); });
    tools.changed = () => { keepTools(); paper.classList.toggle("erasing", tools.erase); };
    const bar = toolbar(tools, { undo: hist.undo, redo: hist.redo, clear: () => { if (!strokes.length) return; hist.mark(); strokes = []; draw(); } });
    paper.classList.toggle("erasing", tools.erase);
    const foot = document.createElement("div"); foot.className = "sk-foot";
    const del = btn("del", {}, ""); del.textContent = T("Delete sketch"); del.hidden = !opts.onDelete;
    const share = btn("", {}, ""); share.textContent = T("Share");
    const done = btn("solid", {}, ""); done.textContent = T("Done");
    foot.append(del, share, done);
    box.append(head, paper, bar, foot);
    scrim.append(box);
    document.body.append(scrim);
    draw();

    // Drawing and erasing.
    const local = ev => { const r = paper.getBoundingClientRect(); return [(ev.clientX - r.left) * PAD / r.width, (ev.clientY - r.top) * PAD / r.height]; };
    let stroke = null, erasing = null, pid = null;
    const showRing = ev => {
      if (!tools.erase) { ring.style.display = "none"; return; }
      const r = paper.getBoundingClientRect(), d = ERASERS[tools.es] * 2 * r.width / PAD;
      Object.assign(ring.style, { display: "block", width: d + "px", height: d + "px", left: ev.clientX - r.left + "px", top: ev.clientY - r.top + "px" });
    };
    paper.addEventListener("pointerdown", ev => {
      if (pid !== null) return;
      if (ev.pointerType === "touch" && sawPen) return;   // the hand resting while a pen writes
      ev.preventDefault();
      paper.setPointerCapture(ev.pointerId); pid = ev.pointerId;
      hist.mark();
      if (tools.erase) { erasing = local(ev); const n = erase(strokes, ...erasing, ...erasing, ERASERS[tools.es]); if (n) { strokes = n; draw(); } showRing(ev); bar.refresh(); return; }
      stroke = pen(local); stroke.start(ev);
      live.setAttribute("fill", COLORS[tools.c]); live.setAttribute("d", outline(stroke.points, SIZES[tools.s]));
    });
    paper.addEventListener("pointermove", ev => {
      showRing(ev);
      if (ev.pointerId !== pid) return;
      if (erasing) {
        const to = local(ev);
        const n = erase(strokes, ...erasing, ...to, ERASERS[tools.es]);
        erasing = to;
        if (n) { strokes = n; draw(); }
        return;
      }
      if (!stroke) return;
      stroke.move(ev);
      live.setAttribute("d", outline(stroke.points, SIZES[tools.s]));
    });
    const up = ev => {
      if (ev.pointerId !== pid) return;
      pid = null;
      if (erasing) { erasing = null; bar.refresh(); return; }
      if (!stroke) return;
      stroke.end(ev);
      strokes.push({ c: tools.c, s: tools.s, p: stroke.points });
      stroke = null; live.setAttribute("d", "");
      draw(); bar.refresh();
    };
    paper.addEventListener("pointerup", up);
    paper.addEventListener("pointercancel", up);
    holdStylus(paper, () => true, () => "all");
    paper.addEventListener("pointerleave", () => { if (pid === null) ring.style.display = "none"; });

    const result = () => (strokes.length ? encode(strokes) : null);
    let closed = false;
    function close(save = true) {
      if (closed) return;
      closed = true;
      removeEventListener("keydown", esc);
      scrim.remove();
      if (save) opts.onSave?.(result());
    }
    const esc = e => { if (e.key === "Escape") close(); };
    addEventListener("keydown", esc);
    x.onclick = () => close();
    done.onclick = () => close();
    scrim.addEventListener("pointerdown", e => { if (e.target === scrim) close(); });
    del.onclick = () => { if (confirm(T("Delete this sketch?"))) { close(false); opts.onDelete?.(); } };
    share.onclick = () => { const d = result(); if (!d) return; close(); opts.onShare?.(d); };
    done.focus();
    return { close };
  }

  window.Sketch = { holdStylus, PAD, PAPER, COLORS, KEYS, PICK, SIZES, ERASERS, outline, encode, decode, erase, pen, paths, picture, toolbar, history, open, css, colorOf, svgEl, tools, keepTools,
    get sawPen() { return sawPen; } };
})();
