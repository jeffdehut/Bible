// The artist's studio, in Felt Stories: new artwork drawn here is shipped to everyone. Only the
// artist's account sees it (storyboard.js loads this file only then, and the server takes artwork
// only from that account: supabase/art.sql).
//
// Three canvases: a scene (the whole board, 1600 x 1000), a person (300 x 600) and an object
// (500 x 500). Each drawing has two layers: colour underneath, and black lines on top. On a
// colouring page the colour turns white and the lines stay. Drawings are kept on this device as
// drafts while they are drawn, and sent to everyone with Publish. Tags are chosen from the words
// the project already uses (the pieces, the stories, the Bible's people and places), so a
// misspelt tag can't hide a piece from search; a new word is allowed, marked, with a "did you mean".
(() => {
  const SB = window.SB, $ = id => document.getElementById(id);
  const DRAFTS = "sb.studio.v1";
  const KINDS = {
    scene: { label: "Scene", w: 1600, h: 1000, s: 1, cat: "scenes", hint: "The whole board, behind everything" },
    person: { label: "Person", w: 300, h: 600, s: 0.55, cat: "people", hint: "Someone standing, head to feet" },
    object: { label: "Object", w: 500, h: 500, s: 0.5, cat: "things", hint: "An animal, a thing, a plant" },
  };
  // A faint guide behind a person (never saved): the built-in people's shape and proportions
  // (their 120 x 260 box, made 2.25 times larger), with lines at the top of the head, the chin,
  // the shoulders, the waist, the hem and the feet, so every person comes out the same size.
  const PERSON_GUIDE = `<g transform="translate(15 7) scale(2.25)" fill="#5b6475" stroke="none">
    <circle cx="60" cy="38" r="21"/><rect x="53" y="54" width="14" height="18"/>
    <path d="M38 72Q60 62 82 72L102 238Q60 250 18 238Z"/>
    <path d="M40 76Q24 112 28 152h13Q40 114 50 88Z"/><path d="M80 76Q96 112 92 152H79Q80 114 70 88Z"/>
    <circle cx="34" cy="156" r="7.5"/><circle cx="86" cy="156" r="7.5"/>
    <ellipse cx="47" cy="246" rx="10" ry="5"/><ellipse cx="73" cy="246" rx="10" ry="5"/></g>
    <g stroke="#2646a1" stroke-width="1.5" stroke-dasharray="6 6" fill="none">${[17, 59, 72, 135, 238, 251].map(y => `<path d="M0 ${Math.round(7 + y * 2.25)}H300"/>`).join("")}</g>`;
  const CATS = [["animals", "Animals"], ["things", "Things"], ["nature", "Nature"]];
  // The felt colours of the built-in pieces, then skin, hair, sky and grass.
  const PALETTE = ["#b8403a", "#d9772b", "#e2b23c", "#3d8a4a", "#5fa84a", "#2f8c87", "#5b8fd1", "#2f5fa8", "#6f4a9e", "#7d2f3f", "#e59a9a",
    "#8a5a2b", "#7a5232", "#c9a46a", "#d8bb84", "#efe7d4", "#f7f4ec", "#9a948a", "#7c7f86", "#3a3430",
    "#e8bb94", "#c98e5f", "#a8703f", "#7e4f2c", "#2a1d16", "#5a3720", "#ece8de", "#7fb2e5", "#9ccbef", "#6fae58", "#4f9440", "#1b2747"];
  const LINE_SIZES = [1.5, 2.8, 5.2], COLOR_SIZES = [7, 18, 44], ERASE = [5, 12, 30];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const store = {
    get() { try { return JSON.parse(localStorage.getItem(DRAFTS)) || {}; } catch (e) { return {}; } },
    set(v) { try { localStorage.setItem(DRAFTS, JSON.stringify(v)); } catch (e) { SB.notice("This device's storage is full; the drawing couldn't be kept."); } },
  };

  /* ---------- Strokes: kept compactly, drawn as ink outlines ---------- */
  // A stroke: {c: colour (colour layer only), w: width, p: [x, y, pressure, ...]} in canvas units.
  // Kept as "c,w,x,y,p,dx,dy,dp..." (halves of a unit, pressure in fifteenths), strokes joined by ";".
  function enc(strokes) {
    return strokes.filter(s => s.p.length).map(s => {
      const out = [(s.c || "").replace("#", ""), Math.round(s.w * 10)];
      let px = 0, py = 0, pp = 0;
      for (let i = 0; i < s.p.length; i += 3) {
        const x = Math.round(s.p[i] * 2), y = Math.round(s.p[i + 1] * 2), q = Math.round(Math.max(0, Math.min(1, s.p[i + 2])) * 15);
        out.push(x - px, y - py, q - pp); px = x; py = y; pp = q;
      }
      return out.join(",");
    }).join(";");
  }
  function dec(text) {
    if (typeof text !== "string" || !text) return [];
    return text.split(";").map(st => {
      const v = st.split(","), c = v[0] ? "#" + v[0] : "", w = (+v[1] || 30) / 10, p = [];
      let x = 0, y = 0, q = 0;
      for (let i = 2; i + 2 < v.length + 1; i += 3) { x += +v[i]; y += +v[i + 1]; q += +v[i + 2]; p.push(x / 2, y / 2, q / 15); }
      return { c, w, p };
    }).filter(s => s.p.length);
  }
  const trim = d => d.replace(/(\d+\.\d)\d+/g, "$1");
  const outlineOf = s => trim(Sketch.outline(s.p, s.w));
  // What the server keeps: the colour layer as [fill, path], the lines as paths, the strokes.
  function layersOut(a) {
    const k = KINDS[a.kind];
    const color = [];
    if (a.paper && /^#[0-9a-f]{6}$/i.test(a.paper)) color.push([a.paper, `M0 0H${k.w}V${k.h}H0Z`]);
    for (const s of a.color) color.push([s.c, outlineOf(s)]);
    return { color, line: a.line.map(outlineOf), src: { v: 1, color: enc(a.color), line: enc(a.line), paper: a.paper || "" } };
  }
  function fromRow(r) {
    const src = r.src || {};
    return { id: r.id, pub: r.id, kind: r.kind, cat: r.cat, sub: r.sub || "", name: r.name, name_zh: r.name_zh || "", tags: r.tags || [], stories: r.stories || [],
      s: r.s, paper: src.paper || "", color: dec(src.color), line: dec(src.line), t: Date.parse(r.updated_at) || Date.now(), sent: Date.parse(r.updated_at) || 0 };
  }
  const toDraft = a => ({ ...a, color: enc(a.color), line: enc(a.line) });
  const fromDraft = d => ({ ...d, color: dec(d.color), line: dec(d.line) });
  function pictureOf(a, mode) {
    const k = KINDS[a.kind], o = layersOut(a);
    const col = o.color.map(([f, d]) => `<path fill="${mode === "line" ? "#fff" : f}" d="${d}"/>`).join("");
    return `<svg viewBox="0 0 ${k.w} ${k.h}" aria-hidden="true">${col}${o.line.map(d => `<path fill="#1d1d1d" d="${d}"/>`).join("")}</svg>`;
  }

  /* ---------- Words for tags ---------- */
  let vocab = null;
  async function words() {
    if (vocab) return vocab;
    const w = new Map();   // word -> weight
    const add = (s, n) => { for (const x of String(s || "").toLowerCase().split(/[\s,;/()]+/)) { const k = x.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, ""); if (k.length > 1 && !/^\d+$/.test(k)) w.set(k, Math.max(w.get(k) || 0, n)); } };
    const addWhole = (s, n) => { const k = String(s || "").toLowerCase().trim(); if (k.length > 1) w.set(k, Math.max(w.get(k) || 0, n)); };
    for (const p of SB.ART.pieces) { add(p.name, 1000); add(p.tags, 900); add(p.id.replace(/-/g, " "), 900); addWhole(p.name, 1000); }
    for (const s of SB.ART.scenes) { add(s.name, 800); add(s.tags, 800); }
    for (const st of SB.ART.stories) { add(st.name, 800); addWhole(st.name, 700); }
    for (const list of Object.values(SB.ART.subs || {})) for (const [, n] of list) add(n, 700);
    for (const d of Object.values(store.get())) for (const tg of d.tags || []) addWhole(tg, 950);
    try {
      const g = await (await fetch("data/graph.json")).json();
      (g.n || []).forEach((n, i) => addWhole(String(n).replace(/\s*\(.*$/, ""), Math.min(600, 100 + ((g.v || [])[i] || 0))));
    } catch (e) { /* the names are a help, not a need */ }
    vocab = [...w.entries()].sort((a, b) => b[1] - a[1]);
    return vocab;
  }
  function near(a, b) {   // edit distance, stopping past 2
    if (Math.abs(a.length - b.length) > 2) return 3;
    let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
    for (let i = 1; i <= a.length; i++) {
      const cur = [i];
      for (let j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      if (Math.min(...cur) > 2) return 3;
      prev = cur;
    }
    return prev[b.length];
  }

  /* ---------- The studio ---------- */
  const CSS = `
.st { position: fixed; inset: 0; z-index: 120; display: flex; flex-direction: column; background: var(--bg, #f6f3ec); color: var(--ink, #1f2430); font-family: var(--sans, system-ui, sans-serif); }
.st button { font: inherit; color: inherit; }
.st-head { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-bottom: 1px solid var(--line, #ddd6c8); background: var(--raised, #fff); }
.st-head h2 { margin: 0; flex: 1; font: 600 19px/1.2 var(--serif, Georgia, serif); }
.st-head .name { flex: 1; min-width: 0; height: 38px; padding: 0 10px; border: 1px solid var(--line, #ddd6c8); border-radius: 10px; background: var(--surface, #fff); font: 600 16px/1 var(--sans, system-ui); color: inherit; }
.st-b { display: inline-flex; align-items: center; justify-content: center; gap: 6px; height: 38px; padding: 0 12px; border: 1px solid var(--line, #ddd6c8); border-radius: 10px; background: var(--surface, #fff); cursor: pointer; white-space: nowrap; }
.st-b svg { width: 20px; height: 20px; }
.st-b.primary { background: var(--lapis, #2646a1); border-color: var(--lapis, #2646a1); color: #fff; }
.st-b.danger { color: #b3261e; }
.st-b[aria-pressed="true"] { background: var(--lapis-soft, #e7ecf8); border-color: var(--lapis, #2646a1); }
.st-b:disabled { opacity: .45; cursor: default; }
.st-home { flex: 1; overflow: auto; padding: 18px 16px 40px; }
.st-home h3 { margin: 18px 0 10px; font: 600 13px/1.3 var(--sans); letter-spacing: .06em; text-transform: uppercase; color: var(--muted, #6b6457); }
.st-kinds { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 12px; }
.st-kind { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 18px 12px; border: 1px solid var(--line, #ddd6c8); border-radius: 16px; background: var(--raised, #fff); cursor: pointer; text-align: center; }
.st-kind i { display: block; border: 2px dashed var(--lapis, #2646a1); border-radius: 6px; background: var(--lapis-soft, #e7ecf8); }
.st-kind b { font-size: 16px; } .st-kind small { color: var(--muted, #6b6457); font-size: 13px; }
.st-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; margin: 0; padding: 0; list-style: none; }
.st-card { border: 1px solid var(--line, #ddd6c8); border-radius: 14px; background: var(--raised, #fff); overflow: hidden; }
.st-card button { display: block; width: 100%; padding: 0 0 8px; border: 0; background: none; cursor: pointer; text-align: start; }
.st-card svg { display: block; width: 100%; height: 120px; background: repeating-conic-gradient(#eee 0 25%, #fff 0 50%) 0 0 / 16px 16px; }
.st-card b { display: block; padding: 6px 10px 0; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.st-card small { display: block; padding: 0 10px; font-size: 12px; color: var(--muted, #6b6457); }
.st-card small.new { color: #b95f00; } .st-card small.pub { color: #2f7d45; }
.st-empty { color: var(--muted, #6b6457); }
.st-main { flex: 1; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) 340px; }
@media (max-width: 860px) { .st-main { grid-template-columns: 1fr; grid-template-rows: minmax(0, 1fr) auto; } .st-side { max-height: 42vh; border-left: 0 !important; border-top: 1px solid var(--line, #ddd6c8); } }
.st-work { display: flex; flex-direction: column; min-height: 0; }
.st-canvas { flex: 1; min-height: 0; display: grid; place-items: center; padding: 12px; }
.st-canvas svg { max-width: 100%; max-height: 100%; touch-action: none; background: repeating-conic-gradient(#ebe7de 0 25%, #fbf9f4 0 50%) 0 0 / 24px 24px; box-shadow: 0 2px 14px rgb(0 0 0 / 16%); border-radius: 4px; cursor: crosshair; }
.st-canvas svg.scene { background: #fff; }
.st-tools { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; padding: 8px 12px 12px; border-top: 1px solid var(--line, #ddd6c8); background: var(--raised, #fff); }
.st-layers { display: flex; gap: 6px; width: 100%; }
.st-layer { flex: 1; display: flex; align-items: center; gap: 8px; height: 40px; padding: 0 6px 0 12px; border: 1px solid var(--line, #ddd6c8); border-radius: 10px; background: var(--surface, #fff); cursor: pointer; font-weight: 600; }
.st-layer[aria-pressed="true"] { border-color: var(--lapis, #2646a1); box-shadow: inset 0 0 0 1px var(--lapis, #2646a1); background: var(--lapis-soft, #e7ecf8); }
.st-layer span { flex: 1; text-align: start; }
.st-eye { width: 32px; height: 32px; border: 0; border-radius: 8px; background: transparent; cursor: pointer; display: grid; place-items: center; }
.st-eye svg { width: 18px; height: 18px; }
.st-eye[aria-pressed="false"] { opacity: .4; }
.st-sw { width: 30px; height: 30px; border-radius: 50%; border: 2px solid rgb(0 0 0 / 12%); background: var(--c); cursor: pointer; padding: 0; }
.st-sw[aria-pressed="true"] { outline: 3px solid var(--lapis, #2646a1); outline-offset: 2px; }
.st-sw.custom { background: conic-gradient(red, yellow, lime, cyan, blue, magenta, red); position: relative; overflow: hidden; }
.st-sw.custom input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
.st-sep { width: 1px; height: 26px; background: var(--line, #ddd6c8); margin: 0 4px; }
.st-tb { width: 40px; height: 40px; display: grid; place-items: center; border: 1px solid var(--line, #ddd6c8); border-radius: 10px; background: var(--surface, #fff); cursor: pointer; }
.st-tb svg { width: 20px; height: 20px; }
.st-tb[aria-pressed="true"] { background: var(--lapis-soft, #e7ecf8); border-color: var(--lapis, #2646a1); }
.st-tb:disabled { opacity: .4; }
.st-dot { display: block; border-radius: 50%; background: currentColor; }
.st-ring { position: fixed; pointer-events: none; border: 1.5px solid #2646a1; border-radius: 50%; transform: translate(-50%, -50%); display: none; z-index: 130; }
.st-side { overflow: auto; padding: 14px 16px 30px; border-left: 1px solid var(--line, #ddd6c8); background: var(--raised, #fff); }
.st-side label, .st-side .lab { display: block; margin: 14px 0 6px; font: 600 13px/1.3 var(--sans); color: var(--muted, #6b6457); }
.st-side input[type=text], .st-side select { width: 100%; height: 40px; padding: 0 10px; border: 1px solid var(--line, #ddd6c8); border-radius: 10px; background: var(--surface, #fff); color: inherit; font: 15px/1 var(--sans); box-sizing: border-box; }
.st-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.st-chip { display: inline-flex; align-items: center; gap: 4px; height: 30px; padding: 0 10px; border: 1px solid var(--line, #ddd6c8); border-radius: 15px; background: var(--surface, #fff); cursor: pointer; font-size: 14px; }
.st-chip[aria-pressed="true"] { background: #c23a7c; border-color: #c23a7c; color: #fff; }
.st-tag { display: inline-flex; align-items: center; gap: 2px; height: 30px; padding: 0 4px 0 10px; border-radius: 15px; background: var(--lapis-soft, #e7ecf8); font-size: 14px; }
.st-tag.new { background: #fff3e0; outline: 1.5px dashed #d9772b; }
.st-tag button { width: 24px; height: 24px; border: 0; border-radius: 12px; background: transparent; cursor: pointer; }
.st-tagbox { position: relative; margin-top: 8px; }
.st-sug { position: absolute; left: 0; right: 0; top: 100%; z-index: 5; margin: 4px 0 0; padding: 4px; list-style: none; border: 1px solid var(--line, #ddd6c8); border-radius: 12px; background: var(--raised, #fff); box-shadow: 0 10px 30px rgb(0 0 0 / 18%); }
.st-sug li { padding: 8px 10px; border-radius: 8px; cursor: pointer; font-size: 15px; }
.st-sug li[aria-selected="true"] { background: var(--lapis-soft, #e7ecf8); }
.st-sug li small { color: var(--muted, #6b6457); }
.st-sug li.warn { color: #b95f00; }
.st-hint { margin: 6px 0 0; font-size: 13px; color: var(--muted, #6b6457); }
.st-acts { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.st-status { margin: 10px 0 0; font-size: 13px; color: var(--muted, #6b6457); }
.st-preview { display: flex; gap: 10px; margin-top: 8px; }
.st-preview div { flex: 1; text-align: center; font-size: 12px; color: var(--muted, #6b6457); }
.st-preview svg { display: block; width: 100%; height: 90px; border: 1px solid var(--line, #ddd6c8); border-radius: 8px; background: #fff; margin-bottom: 4px; }
`;
  const IC = {
    back: '<path d="M15 6l-6 6 6 6"/>',
    pen: '<path d="M4 20h4L19 9l-4-4L4 16Z"/><path d="m13.5 6.5 4 4"/>',
    eraser: '<path d="m7 21-4.3-4.3a1.5 1.5 0 0 1 0-2.1L13.6 3.7a1.5 1.5 0 0 1 2.1 0l4.6 4.6a1.5 1.5 0 0 1 0 2.1L10 21Z"/><path d="M22 21H7M5 12l7 7"/>',
    undo: '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
    redo: '<path d="m15 14 5-5-5-5"/><path d="M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/>',
    eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    paper: '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8"/>',
  };
  const icon = k => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${IC[k]}</svg>`;
  const el = (tag, cls, html) => { const n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; };
  const button = (cls, html, fn, label) => { const b = el("button", cls, html); b.type = "button"; if (fn) b.onclick = fn; if (label) { b.setAttribute("aria-label", label); b.title = label; } return b; };

  let root = null, server = {};   // server: published artwork by id, with its strokes
  async function loadServer() {
    try {
      const rows = await SB.Sync.call("/rest/v1/art?select=*&order=updated_at.desc");
      server = Object.fromEntries((rows || []).map(r => [r.id, r]));
      return true;
    } catch (e) {
      return e.status === 404 ? "missing" : false;
    }
  }
  function open() {
    if (root) return;
    if (!document.getElementById("st-style")) { const st = el("style"); st.id = "st-style"; st.textContent = CSS; document.head.append(st); }
    root = el("div", "st"); root.setAttribute("role", "dialog"); root.setAttribute("aria-modal", "true"); root.setAttribute("aria-label", "Artist's studio");
    document.body.append(root);
    document.body.style.overflow = "hidden";
    if (!window.Sketch) { const sc = document.createElement("script"); sc.src = "sketch.js?v=10"; sc.onload = home; document.head.append(sc); root.textContent = ""; } else home();
  }
  function close() { if (!root) return; root.remove(); root = null; document.body.style.overflow = ""; removeEventListener("keydown", onKey, true); }
  let onKey = null;

  /* ---------- Home: start something new, or pick up a drawing ---------- */
  async function home() {
    removeEventListener("keydown", onKey, true);
    root.textContent = "";
    const head = el("div", "st-head");
    head.append(el("h2", "", "Artist's studio"), button("st-b", "Close", close));
    const body = el("div", "st-home");
    body.append(el("h3", "", "New artwork"));
    const kinds = el("div", "st-kinds");
    for (const [k, v] of Object.entries(KINDS)) {
      const r = Math.min(70 / v.w, 70 / v.h);
      const b = button("st-kind", `<i style="width:${Math.round(v.w * r)}px;height:${Math.round(v.h * r)}px"></i><b>${v.label}</b><small>${v.hint}</small>`, () => edit(blank(k)));
      kinds.append(b);
    }
    body.append(kinds);
    const mineH = el("h3", "", "Your artwork"), list = el("ul", "st-grid"), note = el("p", "st-empty", "Loading…");
    body.append(mineH, note, list);
    root.append(head, body);
    onKey = e => { if (e.key === "Escape") close(); };
    addEventListener("keydown", onKey, true);
    const ok = await loadServer();
    if (!root) return;
    const drafts = store.get();
    const all = new Map();
    for (const r of Object.values(server)) if (!r.deleted) all.set(r.id, { a: fromRow(r), state: "pub" });
    for (const d of Object.values(drafts)) {
      const a = fromDraft(d), key = a.pub || a.id;
      all.set(key, { a, state: a.pub && server[a.pub] && !server[a.pub].deleted ? (a.t > a.sent ? "changed" : "pub") : "draft" });
    }
    note.textContent = ok === "missing" ? "The artwork table isn't on the server yet, so drawings are kept on this device as drafts until it is." : ok ? (all.size ? "" : "Nothing drawn yet. Choose a canvas above.") : "Your account couldn't be reached; drafts on this device are shown.";
    note.hidden = !note.textContent;
    for (const { a, state } of [...all.values()].sort((x, y) => y.a.t - x.a.t)) {
      const li = el("li", "st-card");
      const b = button("", pictureOf(a) + "<b></b><small></small>", () => edit(a));
      b.querySelector("b").textContent = a.name || "Untitled";
      const sm = b.querySelector("small");
      sm.textContent = KINDS[a.kind].label + " · " + { pub: "Published", changed: "Changes not published", draft: "Draft on this device" }[state];
      sm.className = state === "pub" ? "pub" : "new";
      li.append(b); list.append(li);
    }
  }
  function blank(kind) {
    const k = KINDS[kind];
    return { id: "d" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), pub: null, kind, cat: k.cat, sub: "", name: "", name_zh: "", tags: [], stories: [], s: k.s, paper: kind === "scene" ? "#9ccbef" : "", color: [], line: [], t: Date.now(), sent: 0 };
  }

  /* ---------- Drawing ---------- */
  function edit(a) {
    removeEventListener("keydown", onKey, true);
    root.textContent = "";
    const k = KINDS[a.kind], unit = Math.max(k.w, k.h) / 288;
    const tool = { layer: "line", c: "#b8403a", s: 1, erase: false, show: { color: true, line: true, guide: true } };
    const keep = () => { a.t = Date.now(); const all = store.get(); all[a.id] = toDraft(a); store.set(all); status(); preview(); };

    // Header.
    const head = el("div", "st-head");
    const name = el("input", "name"); name.type = "text"; name.placeholder = "Name, e.g. Shepherd with a lamb"; name.value = a.name; name.maxLength = 80;
    name.oninput = () => { a.name = name.value; keep(); };
    head.append(button("st-b", icon("back"), () => home(), "Back to the studio"), name);
    const pub = button("st-b primary", a.pub ? "Update for everyone" : "Publish", () => publish());
    head.append(pub);

    // The canvas.
    const NS = "http://www.w3.org/2000/svg", svgEl = (tag, at) => { const n = document.createElementNS(NS, tag); for (const [x, v] of Object.entries(at || {})) n.setAttribute(x, v); return n; };
    const svg = svgEl("svg", { viewBox: `0 0 ${k.w} ${k.h}`, class: a.kind === "scene" ? "scene" : "" });
    svg.style.aspectRatio = k.w + " / " + k.h;
    const paperG = svgEl("g"), guideG = svgEl("g", { opacity: "0.16", "pointer-events": "none" }), colG = svgEl("g"), linG = svgEl("g"), live = svgEl("path");
    if (a.kind === "person") guideG.innerHTML = PERSON_GUIDE;
    svg.append(paperG, guideG, colG, linG, live);
    const draw = () => {
      paperG.innerHTML = a.paper ? `<rect width="${k.w}" height="${k.h}" fill="${a.paper}"/>` : "";
      colG.replaceChildren(...a.color.map(s => svgEl("path", { d: outlineOf(s), fill: s.c })));
      linG.replaceChildren(...a.line.map(s => svgEl("path", { d: outlineOf(s), fill: "#1d1d1d" })));
      colG.style.display = paperG.style.display = tool.show.color ? "" : "none";
      linG.style.display = tool.show.line ? "" : "none";
      guideG.style.display = tool.show.guide ? "" : "none";
    };
    const snap = () => JSON.stringify({ c: enc(a.color), l: enc(a.line), p: a.paper });
    const back = [], fwd = [];
    const mark = () => { back.push(snap()); if (back.length > 80) back.shift(); fwd.length = 0; };
    const restore = v => { const o = JSON.parse(v); a.color = dec(o.c); a.line = dec(o.l); a.paper = o.p; draw(); keep(); tools(); };
    const canvas = el("div", "st-canvas"); canvas.append(svg);
    const ring = el("div", "st-ring"); root.append(ring);
    const local = ev => { const r = svg.getBoundingClientRect(); return [(ev.clientX - r.left) * k.w / r.width, (ev.clientY - r.top) * k.h / r.height]; };
    const sizes = () => (tool.layer === "color" ? COLOR_SIZES : LINE_SIZES);
    const strokesOf = () => (tool.layer === "color" ? a.color : a.line);
    const showRing = ev => {
      if (!tool.erase) { ring.style.display = "none"; return; }
      const r = svg.getBoundingClientRect(), d = ERASE[tool.s] * unit * 2 * r.width / k.w;
      Object.assign(ring.style, { display: "block", width: d + "px", height: d + "px", left: ev.clientX + "px", top: ev.clientY + "px" });
    };
    let stroke = null, erasing = null, pid = null;
    svg.addEventListener("pointerdown", ev => {
      if (pid !== null) return;
      if (ev.pointerType === "touch" && Sketch.sawPen) return;
      if (!tool.show[tool.layer]) { tool.show[tool.layer] = true; draw(); tools(); }
      ev.preventDefault();
      svg.setPointerCapture(ev.pointerId); pid = ev.pointerId;
      mark();
      if (tool.erase) {
        erasing = local(ev);
        const n = Sketch.erase(strokesOf(), ...erasing, ...erasing, ERASE[tool.s] * unit, s => s.w);
        if (n) { if (tool.layer === "color") a.color = n; else a.line = n; draw(); }
        showRing(ev); return;
      }
      stroke = Sketch.pen(local, 0.5 * unit); stroke.start(ev);
      live.setAttribute("fill", tool.layer === "color" ? tool.c : "#1d1d1d");
      live.setAttribute("d", Sketch.outline(stroke.points, sizes()[tool.s] * unit));
    });
    svg.addEventListener("pointermove", ev => {
      showRing(ev);
      if (ev.pointerId !== pid) return;
      if (erasing) {
        const to = local(ev);
        const n = Sketch.erase(strokesOf(), ...erasing, ...to, ERASE[tool.s] * unit, s => s.w);
        erasing = to;
        if (n) { if (tool.layer === "color") a.color = n; else a.line = n; draw(); }
        return;
      }
      if (!stroke) return;
      stroke.move(ev);
      live.setAttribute("d", Sketch.outline(stroke.points, sizes()[tool.s] * unit));
    });
    const up = ev => {
      if (ev.pointerId !== pid) return;
      pid = null;
      if (erasing) { erasing = null; keep(); tools(); return; }
      if (!stroke) return;
      stroke.end(ev);
      const s = { c: tool.layer === "color" ? tool.c : "", w: sizes()[tool.s] * unit, p: stroke.points };
      strokesOf().push(s);
      stroke = null; live.setAttribute("d", "");
      draw(); keep(); tools();
    };
    svg.addEventListener("pointerup", up);
    svg.addEventListener("pointercancel", up);
    svg.addEventListener("pointerleave", () => { if (pid === null) ring.style.display = "none"; });
    Sketch.holdStylus(svg, () => true, () => "all");

    // The tools: which layer, its colours, sizes, pen or eraser, undo and redo.
    const bar = el("div", "st-tools");
    function tools() {
      bar.textContent = "";
      const layers = el("div", "st-layers");
      for (const [id, label] of [["color", "Colour"], ["line", "Black lines"]]) {
        const b = button("st-layer", `<span>${label}</span>`, () => { tool.layer = id; tools(); });
        b.setAttribute("aria-pressed", String(tool.layer === id));
        const eye = button("st-eye", icon("eye"), e => { e.stopPropagation(); tool.show[id] = !tool.show[id]; draw(); tools(); }, (tool.show[id] ? "Hide " : "Show ") + label.toLowerCase());
        eye.setAttribute("aria-pressed", String(tool.show[id]));
        b.append(eye); layers.append(b);
      }
      if (a.kind === "person") {
        const g = button("st-layer", "<span>Guide</span>", () => { tool.show.guide = !tool.show.guide; draw(); tools(); }, tool.show.guide ? "Hide the person guide" : "Show the person guide");
        g.style.flex = "0 0 auto";
        g.setAttribute("aria-pressed", String(tool.show.guide));
        const eye = el("span", "st-eye", icon("eye")); eye.setAttribute("aria-pressed", String(tool.show.guide)); g.append(eye);
        layers.append(g);
      }
      bar.append(layers);
      if (tool.layer === "color") {
        const colors = [...new Set([...PALETTE, ...a.color.map(s => s.c)])].slice(0, PALETTE.length + 6);
        for (const c of colors) {
          const b = button("st-sw", "", () => { tool.c = c; tool.erase = false; tools(); }, c);
          b.style.setProperty("--c", c);
          b.setAttribute("aria-pressed", String(!tool.erase && tool.c === c));
          bar.append(b);
        }
        const cu = el("label", "st-sw custom"); cu.title = "Any colour";
        const inp = el("input"); inp.type = "color"; inp.value = tool.c; inp.oninput = () => { tool.c = inp.value; tool.erase = false; }; inp.onchange = () => tools();
        cu.append(inp); bar.append(cu);
        if (a.kind === "scene") {
          const pb = button("st-tb", icon("paper"), () => { mark(); a.paper = tool.c; draw(); keep(); }, "Fill the background with this colour");
          bar.append(pb);
        }
        bar.append(el("span", "st-sep"));
      }
      sizes().forEach((w, i) => {
        const d = tool.erase ? 8 + i * 6 : tool.layer === "color" ? 8 + i * 6 : 4 + i * 4;
        const b = button("st-tb", `<span class="st-dot" style="width:${d}px;height:${d}px;${tool.erase ? "background:none;border:1.5px solid currentColor" : ""}"></span>`, () => { tool.s = i; tools(); }, ["Small", "Medium", "Large"][i]);
        b.setAttribute("aria-pressed", String(tool.s === i));
        bar.append(b);
      });
      bar.append(el("span", "st-sep"));
      const p = button("st-tb", icon("pen"), () => { tool.erase = false; tools(); }, tool.layer === "color" ? "Brush" : "Pen");
      p.setAttribute("aria-pressed", String(!tool.erase));
      const e = button("st-tb", icon("eraser"), () => { tool.erase = true; tools(); }, "Eraser");
      e.setAttribute("aria-pressed", String(tool.erase));
      const u = button("st-tb", icon("undo"), () => { if (back.length) { fwd.push(snap()); restore(back.pop()); } }, "Undo"); u.disabled = !back.length;
      const r = button("st-tb", icon("redo"), () => { if (fwd.length) { back.push(snap()); restore(fwd.pop()); } }, "Redo"); r.disabled = !fwd.length;
      bar.append(p, e, u, r);
    }

    // The details: names, drawer, group, stories, tags; a preview in colour and as a colouring page.
    const side = el("div", "st-side");
    const field = (label, input) => { const l = el("label"); l.textContent = label; side.append(l, input); return input; };
    const zh = el("input"); zh.type = "text"; zh.placeholder = "e.g. 抱着小羊的牧人"; zh.value = a.name_zh; zh.maxLength = 40;
    zh.oninput = () => { a.name_zh = zh.value; keep(); };
    field("Chinese name", zh);
    if (a.kind === "object") {
      const sel = el("select");
      for (const [v, n] of CATS) sel.append(new Option(n, v, false, a.cat === v));
      sel.onchange = () => { a.cat = sel.value; a.sub = ""; keep(); subs(); };
      field("Drawer", sel);
    }
    const subSel = el("select");
    const subs = () => {
      const list = (SB.ART.subs || {})[a.cat] || [];
      subSel.replaceChildren(new Option("None", ""), ...list.map(([v, n]) => new Option(n, v, false, a.sub === v)));
      subSel.parentElement && (subSel.previousElementSibling.hidden = subSel.hidden = !list.length);
    };
    subSel.onchange = () => { a.sub = subSel.value; keep(); };
    if (a.kind !== "scene") { field("Group in the drawer", subSel); subs(); }
    side.append(Object.assign(el("div", "lab"), { textContent: "Stories" }));
    const sts = el("div", "st-chips");
    for (const st of SB.ART.stories) {
      const b = button("st-chip", "", () => { a.stories = a.stories.includes(st.id) ? a.stories.filter(x => x !== st.id) : [...a.stories, st.id]; b.setAttribute("aria-pressed", String(a.stories.includes(st.id))); keep(); });
      b.textContent = st.name; b.setAttribute("aria-pressed", String(a.stories.includes(st.id)));
      sts.append(b);
    }
    side.append(sts);
    // Tags.
    side.append(Object.assign(el("div", "lab"), { textContent: "Tags (words people search for)" }));
    const tagList = el("div", "st-chips"), tagBox = el("div", "st-tagbox");
    const tagIn = el("input"); tagIn.type = "text"; tagIn.placeholder = "Type a tag…"; tagIn.setAttribute("autocomplete", "off"); tagIn.setAttribute("aria-autocomplete", "list");
    const sug = el("ul", "st-sug"); sug.hidden = true; sug.setAttribute("role", "listbox");
    tagBox.append(tagIn, sug);
    const hint = el("p", "st-hint", "Choose from the suggestions so every tag is spelled the way the project spells it. A dashed tag is a new word.");
    side.append(tagList, tagBox, hint);
    let known = new Set(), opts = [], at = 0;
    words().then(v => { known = new Set(v.map(x => x[0])); drawTags(); });
    function drawTags() {
      tagList.replaceChildren(...a.tags.map(tg => {
        const c = el("span", "st-tag" + (known.size && !known.has(tg) ? " new" : ""));
        c.append(document.createTextNode(tg), button("", "×", () => { a.tags = a.tags.filter(x => x !== tg); keep(); drawTags(); }, "Remove " + tg));
        if (known.size && !known.has(tg)) c.title = "A new word: not used anywhere else in the project yet";
        return c;
      }));
    }
    function addTag(tg) {
      tg = tg.toLowerCase().trim().replace(/\s+/g, " ").slice(0, 40);
      if (tg && !a.tags.includes(tg) && a.tags.length < 40) { a.tags.push(tg); keep(); drawTags(); }
      tagIn.value = ""; suggest();
    }
    async function suggest() {
      const q = tagIn.value.toLowerCase().trim();
      if (!q) { sug.hidden = true; opts = []; return; }
      const v = await words();
      if (tagIn.value.toLowerCase().trim() !== q) return;
      const starts = [], has = [];
      for (const [w] of v) { if (a.tags.includes(w)) continue; if (w.startsWith(q)) starts.push(w); else if (w.includes(q)) has.push(w); if (starts.length >= 8) break; }
      opts = [...starts, ...has].slice(0, 8).map(w => ({ w }));
      if (!known.has(q)) {
        const close = opts.length ? [] : v.filter(([w]) => near(q, w) <= (q.length > 5 ? 2 : 1)).slice(0, 3).map(([w]) => ({ w, mean: true }));
        opts.push(...close, { w: q, add: true });
      }
      at = 0;
      sug.replaceChildren(...opts.map((o, i) => {
        const li = el("li", o.add ? "warn" : "");
        li.setAttribute("role", "option"); li.setAttribute("aria-selected", String(i === at));
        if (o.add) li.innerHTML = `Add “${esc(o.w)}” as a new word <small>(not in the project yet)</small>`;
        else if (o.mean) li.innerHTML = `Did you mean <b>${esc(o.w)}</b>?`;
        else li.textContent = o.w;
        li.onpointerdown = e => { e.preventDefault(); addTag(o.w); };
        return li;
      }));
      sug.hidden = !opts.length;
    }
    const mark2 = () => [...sug.children].forEach((li, i) => li.setAttribute("aria-selected", String(i === at)));
    tagIn.oninput = suggest;
    tagIn.onkeydown = e => {
      if (e.key === "ArrowDown" && opts.length) { e.preventDefault(); at = (at + 1) % opts.length; mark2(); }
      else if (e.key === "ArrowUp" && opts.length) { e.preventDefault(); at = (at - 1 + opts.length) % opts.length; mark2(); }
      else if ((e.key === "Enter" || e.key === "Tab" || e.key === ",") && tagIn.value.trim()) { e.preventDefault(); if (opts[at]) addTag(opts[at].w); }
      else if (e.key === "Escape") { e.stopPropagation(); sug.hidden = true; }
    };
    tagIn.onblur = () => setTimeout(() => { sug.hidden = true; }, 150);
    drawTags();
    // Preview and actions.
    side.append(Object.assign(el("div", "lab"), { textContent: "How it looks" }));
    const pv = el("div", "st-preview");
    side.append(pv);
    function preview() { pv.innerHTML = `<div>${pictureOf(a)}Felt</div><div>${pictureOf(a, "line")}Colouring page</div>`; }
    const st = el("p", "st-status");
    const acts = el("div", "st-acts");
    const unpub = button("st-b danger", "Unpublish", async () => {
      if (!confirm("Take this artwork away from everyone? Boards that use it will lose the piece.")) return;
      try {
        await SB.Sync.call("/rest/v1/art?id=eq." + encodeURIComponent(a.pub), "PATCH", { deleted: true, updated_at: new Date().toISOString() }, { Prefer: "return=minimal" });
        delete server[a.pub]; a.pub = null; a.sent = 0; keep(); pub.textContent = "Publish"; unpub.hidden = true; SB.notice("Unpublished. It's kept here as a draft.");
        refreshEveryone();
      } catch (e) { SB.notice("Couldn't unpublish: " + e.message); }
    });
    unpub.hidden = !a.pub;
    const del = button("st-b", "Delete draft", () => {
      if (a.pub) { const all = store.get(); delete all[a.id]; store.set(all); home(); return; }
      if (!confirm("Delete this drawing? This can't be undone.")) return;
      const all = store.get(); delete all[a.id]; store.set(all); home();
    });
    acts.append(unpub, del);
    side.append(acts, st);
    function status() {
      const changed = a.pub && a.t > a.sent;
      st.textContent = a.pub ? (changed ? "Saved on this device. Changes not published yet." : "Published: everyone has this.") : "Saved on this device as a draft. Publish to send it to everyone.";
      del.textContent = a.pub ? "Forget local changes" : "Delete draft";
      del.hidden = a.pub && !changed;
    }

    // Publishing: checks, then the artwork goes to the server and into everyone's drawers.
    async function publish() {
      const why = !a.name.trim() ? "Give it a name first." : !a.line.length && !a.color.length ? "Draw something first." : !a.tags.length ? "Add at least one tag, so people can find it." : "";
      if (why) { SB.notice(why); (why.includes("name") ? name : why.includes("tag") ? tagIn : svg).focus?.(); return; }
      const fresh = a.tags.filter(tg => known.size && !known.has(tg));
      if (fresh.length && !confirm(`These tags are new words in the project: ${fresh.join(", ")}. Publish anyway?`)) return;
      let id = a.pub;
      if (!id) {
        const base = a.name.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || a.kind;
        id = base.length < 2 ? a.kind + "-" + base : base;
        let n = 2;
        while (SB.byId[id] || SB.sceneById[id] || server[id]) id = base + "-" + n++;
      }
      const o = layersOut(a);
      const row = { id, kind: a.kind, cat: a.kind === "scene" ? "scenes" : a.cat, sub: a.sub || "", name: a.name.trim(), name_zh: a.name_zh.trim(), tags: a.tags, stories: a.stories,
        w: k.w, h: k.h, s: a.s, color: o.color, line: o.line, src: o.src, deleted: false, updated_at: new Date().toISOString() };
      pub.disabled = true; pub.textContent = "Publishing…";
      try {
        await SB.Sync.call("/rest/v1/art?on_conflict=id", "POST", row, { Prefer: "resolution=merge-duplicates,return=minimal" });
        server[id] = row;
        const all = store.get(); delete all[a.id]; store.set(all);
        a.id = id; a.pub = id; a.sent = a.t = Date.parse(row.updated_at);
        const all2 = store.get(); all2[a.id] = toDraft(a); store.set(all2);
        status(); unpub.hidden = false;
        SB.notice("Published: “" + row.name + "” is in everyone's drawers now.");
        refreshEveryone();
      } catch (e) {
        SB.notice(e.status === 404 ? "The artwork table isn't on the server yet. Your drawing is kept here as a draft." : e.status === 401 || e.status === 403 ? "The server didn't accept it from this account." : "Couldn't publish just now: " + e.message);
      }
      pub.disabled = false; pub.textContent = a.pub ? "Update for everyone" : "Publish";
    }
    async function refreshEveryone() {
      try {
        const res = await fetch(SB.ABASE + "/rest/v1/art?select=id,kind,cat,sub,name,name_zh,tags,stories,w,h,s,color,line,updated_at&deleted=is.false&order=updated_at.asc", { headers: { apikey: SB.ACFG.key } });
        if (res.ok) SB.installed(await res.json());
      } catch (e) { /* the next visit brings it */ }
    }

    const work = el("div", "st-work"); work.append(canvas, bar);
    const main = el("div", "st-main"); main.append(work, side);
    root.append(head, main);
    onKey = e => {
      if (e.target.closest && e.target.closest("input, select, textarea")) return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") { e.preventDefault(); (e.shiftKey ? fwd : back).length && (e.shiftKey ? (back.push(snap()), restore(fwd.pop())) : (fwd.push(snap()), restore(back.pop()))); }
      else if (e.key === "Escape") home();
    };
    addEventListener("keydown", onKey, true);
    draw(); tools(); status(); preview();
    if (!a.name) name.focus();
  }

  window.Studio = { open, close };
})();
