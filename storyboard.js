// Felt Stories (the Story Board): a felt board for telling Bible stories. Pieces come out of the drawers (tap
// one, or drag it onto the board), and on the board they move with a finger, a mouse or the
// keyboard; two fingers resize and turn the piece picked up. The board is kept on this device.
(() => {
  const ART = window.SB_ART, L = window.L || { t: s => s };
  const t = s => (L.t ? L.t(s) : s);
  const $ = id => document.getElementById(id);
  const NS = "http://www.w3.org/2000/svg";
  const W = 1600, H = 1000;
  const byId = Object.fromEntries(ART.pieces.map(p => [p.id, p]));
  const sceneById = Object.fromEntries(ART.scenes.map(s => [s.id, s]));
  const KEY = "sb.board.v1";
  const stage = $("stage"), itemsG = $("items"), selG = $("sel"), bgG = $("bg");

  // Each piece once, as a symbol the board's pieces use.
  const defs = $("defs");
  function symbol(p) {
    let s = document.getElementById("a-" + p.id);
    if (!s) { s = document.createElementNS(NS, "symbol"); s.id = "a-" + p.id; s.setAttribute("overflow", "visible"); defs.append(s); }
    s.setAttribute("viewBox", `0 0 ${p.w} ${p.h}`);
    s.innerHTML = p.svg;
  }
  ART.pieces.forEach(symbol);

  /* ---------- Artwork from the studio, shipped to everyone ---------- */
  // Drawn in the artist's studio (art-studio.js) and kept on the server as data: a colour layer
  // ([fill, path] pairs) under a layer of black lines (paths). The pictures are built here from
  // that data, checked, so nothing from the server is ever run as markup. On a colouring page the
  // colour layer turns white and the lines stay. A copy is kept on this device for the next visit.
  const ACFG = (window.SITE_CONFIG || {}).supabase || {}, ABASE = (ACFG.url || "").replace(/\/+$/, "");
  const ART_KEY = "sb.art.v1", ARTIST = "jeff@jeffdehut.com";
  const HEX = /^#[0-9a-f]{6}$/i, PATH = /^[MLCQZAHVSTmlcqzahvst0-9.,\s-]+$/;
  const isZh = () => /^zh/.test((window.I18N && window.I18N.lang) || "");
  function artMarkup(r) {
    const col = (Array.isArray(r.color) ? r.color : []).filter(c => Array.isArray(c) && HEX.test(c[0]) && typeof c[1] === "string" && PATH.test(c[1]));
    const ln = (Array.isArray(r.line) ? r.line : []).filter(d => typeof d === "string" && PATH.test(d));
    const lines = ln.map(d => `<path fill="#1d1d1d" d="${d}"/>`).join("");
    return { svg: col.map(([f, d]) => `<path fill="${f}" d="${d}"/>`).join("") + lines, line: col.map(c => `<path fill="#fff" d="${c[1]}"/>`).join("") + lines };
  }
  const num = (v, lo, hi, d) => (Number.isFinite(+v) ? Math.min(hi, Math.max(lo, +v)) : d);
  function installArt(rows) {
    for (const r of rows || []) {
      if (!r || typeof r.id !== "string" || !/^[a-z0-9][a-z0-9-]{1,59}$/.test(r.id) || r.deleted) continue;
      const m = artMarkup(r), name = String((isZh() && r.name_zh) || r.name || r.id).slice(0, 80);
      const tags = [...(Array.isArray(r.tags) ? r.tags : []), r.name, r.name_zh].filter(x => typeof x === "string").join(" ");
      const stories = (Array.isArray(r.stories) ? r.stories : []).filter(x => typeof x === "string");
      if (r.kind === "scene") {
        const base = `<rect width="${W}" height="${H}" fill="#fff"/>`;
        const sc = { id: r.id, name, svg: base + m.svg, line: base + m.line, tags, art: true };
        const i = ART.scenes.findIndex(x => x.id === r.id);
        if (i >= 0) ART.scenes[i] = sc; else ART.scenes.push(sc);
        sceneById[r.id] = sc;
        for (const st of ART.stories) if (stories.includes(st.id) && !st.scenes.includes(r.id)) st.scenes.push(r.id);
        continue;
      }
      const cat = ["people", "animals", "things", "nature"].includes(r.cat) ? r.cat : "things";
      const p = { id: r.id, name, cat, sub: typeof r.sub === "string" ? r.sub : "", tags, stories, w: num(r.w, 50, 2000, 500), h: num(r.h, 50, 2000, 500), s: num(r.s, 0.05, 5, 1), svg: m.svg, line: m.line, art: true };
      if (byId[r.id]) Object.assign(byId[r.id], p); else { ART.pieces.push(p); byId[r.id] = p; }
      symbol(byId[r.id]);
      for (const st of ART.stories) if (stories.includes(st.id) && !st.pieces.includes(r.id)) st.pieces.push(r.id);
    }
  }
  const cachedArt = (() => { try { return JSON.parse(localStorage.getItem(ART_KEY)) || []; } catch (e) { return []; } })();
  installArt(cachedArt);
  // The newest artwork from the server; anything new or changed goes into the drawers now.
  async function fetchArt() {
    if (!ABASE || navigator.onLine === false) return;
    try {
      const res = await fetch(ABASE + "/rest/v1/art?select=id,kind,cat,sub,name,name_zh,tags,stories,w,h,s,color,line,updated_at&deleted=is.false&order=updated_at.asc", { headers: { apikey: ACFG.key } });
      if (!res.ok) return;
      const rows = await res.json();
      const txt = JSON.stringify(rows);
      if (txt === JSON.stringify(cachedArt)) return;
      try { localStorage.setItem(ART_KEY, txt); } catch (e) { /* storage full */ }
      artChanged(rows);
    } catch (e) { /* offline */ }
  }

  /* ---------- The boards: each a saved document, in folders ---------- */
  // lib: { docs: {id: {id, name, folder, data: {bg, items}, t, del?}}, cur: the board open,
  //        folders: [names], foldersT, foldersDirty, dirty: {id: true} not yet sent to the
  //        account, pulled: the server time of the newest change fetched, user: whose account }
  const DOCS = "sb.docs.v1";
  const rid = () => (crypto.randomUUID ? crypto.randomUUID().replace(/-/g, "").slice(0, 20) : Math.random().toString(36).slice(2, 12) + Date.now().toString(36));
  const blank = () => ({ bg: "hills", items: [] });
  const newDoc = (name, folder = "", data = null) => ({ id: rid(), name, folder, data: data || blank(), t: Date.now() });
  const cleanData = d => ({ bg: sceneById[d && d.bg] ? d.bg : "hills", items: ((d && d.items) || []).filter(i => byId[i.a]), ...(d && d.cap && d.cap.text ? { cap: d.cap } : {}), ...(d && d.lesson ? { lesson: d.lesson } : {}), ...(d && d.from ? { from: d.from } : {}) });
  const untitled = () => t("Untitled board");
  let lib = (() => {
    try { const l = JSON.parse(localStorage.getItem(DOCS)); if (l && l.docs) return { folders: [], dirty: {}, ...l }; } catch (e) { /* none yet */ }
    const l = { docs: {}, folders: [], foldersT: 0, dirty: {}, pulled: null };
    let old = null;
    try { old = JSON.parse(localStorage.getItem(KEY)); } catch (e) { /* none */ }
    const d = newDoc(t("My first board"), "", old && Array.isArray(old.items) ? cleanData(old) : null);
    l.docs[d.id] = d; l.cur = d.id; l.dirty[d.id] = true;
    return l;
  })();
  function persist() { try { localStorage.setItem(DOCS, JSON.stringify(lib)); } catch (e) { /* storage full or blocked */ } }
  const live = () => Object.values(lib.docs).filter(d => !d.del);
  function firstDoc() {
    const d = live().sort((a, b) => b.t - a.t)[0];
    if (d) return d;
    const n = newDoc(untitled()); lib.docs[n.id] = n; lib.dirty[n.id] = true; return n;
  }
  let doc = lib.docs[lib.cur] && !lib.docs[lib.cur].del ? lib.docs[lib.cur] : firstDoc();
  lib.cur = doc.id;
  let board = cleanData(doc.data);
  let sel = [], uid = board.items.reduce((m, i) => Math.max(m, i.k), 0);
  const past = [];
  function save() {
    doc.data = board; doc.t = Date.now(); lib.dirty[doc.id] = true;
    persist(); Sync.soon();
  }
  function touch(d) { d.t = Date.now(); lib.dirty[d.id] = true; persist(); Sync.soon(); }
  function openDoc(id, quiet) {
    const d = lib.docs[id];
    doc = d && !d.del ? d : firstDoc();
    lib.cur = doc.id; persist();
    board = cleanData(doc.data);
    uid = board.items.reduce((m, i) => Math.max(m, i.k), 0);
    past.length = 0; $("undo").disabled = true; sel = []; capSel = false; choosing = false;
    itemsG.textContent = "";
    render(); showName();
    if (!quiet) say(t("Opened: ") + doc.name);
  }
  function showName() { $("doc-name").textContent = doc.name || untitled(); document.title = (doc.name || untitled()) + " · " + t("Felt Stories"); }
  function remember() { past.push(JSON.stringify(board)); if (past.length > 60) past.shift(); $("undo").disabled = false; }
  function undo() {
    if (!past.length) return;
    board = JSON.parse(past.pop()); sel = []; capSel = false; choosing = false;
    $("undo").disabled = !past.length;
    render(); save(); say(t("Undone"));
  }
  const say = msg => { $("live").textContent = ""; requestAnimationFrame(() => { $("live").textContent = msg; }); };
  const nameOf = it => t(byId[it.a].name);

  /* ---------- Drawing ---------- */
  // sel: the pieces picked up. A piece clipped to others comes with them (it.g, the clip they
  // share); several can be chosen at once (Shift, or "Choose more"). capSel: the verse picked.
  let capSel = false, choosing = false;
  const groupOf = it => (it.g ? board.items.filter(i => i.g === it.g) : [it]);
  function render() {
    bgG.innerHTML = (sceneById[board.bg] || ART.scenes[0]).svg;
    const keep = new Map([...itemsG.children].map(g => [+g.dataset.k, g]));
    const order = [];
    for (const it of board.items) {
      let g = keep.get(it.k);
      if (!g) g = make(it);
      keep.delete(it.k);
      place(g, it);
      g.classList.toggle("clipped", !!it.g);
      order.push(g);
    }
    for (const g of keep.values()) g.remove();
    order.forEach(g => itemsG.append(g));
    sel = sel.filter(i => board.items.includes(i));
    $("cap").innerHTML = capSVG(board.cap);
    if (!board.cap) capSel = false;
    drawSel();
    $("empty").hidden = board.items.length > 0 || !!board.cap;
    syncScenes();
  }
  function make(it) {
    const p = byId[it.a];
    const g = document.createElementNS(NS, "g");
    g.setAttribute("class", "item"); g.dataset.k = it.k;
    g.setAttribute("tabindex", "0"); g.setAttribute("role", "button");
    g.setAttribute("aria-label", t(p.name));
    g.setAttribute("filter", "url(#felt)");
    const u = document.createElementNS(NS, "use");
    u.setAttribute("href", "#a-" + p.id);
    u.setAttribute("x", -p.w / 2); u.setAttribute("y", -p.h / 2); u.setAttribute("width", p.w); u.setAttribute("height", p.h);
    g.append(u);
    g.addEventListener("focus", () => { const it2 = board.items.find(i => i.k === +g.dataset.k); if (it2 && !sel.includes(it2)) pickItems(groupOf(it2), false); });
    g.addEventListener("keydown", onKey);
    return g;
  }
  const xf = it => `translate(${it.x} ${it.y}) rotate(${it.r || 0}) scale(${it.s * (it.f || 1)} ${it.s})`;
  function place(g, it) { g.setAttribute("transform", xf(it)); }
  // A piece's corners on the board, and the box around several.
  function corners(it) {
    const p = byId[it.a], a = (it.r || 0) * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
    return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([u, v]) => {
      const x = u * p.w / 2 * it.s * (it.f || 1), y = v * p.h / 2 * it.s;
      return [it.x + x * c - y * s, it.y + x * s + y * c];
    });
  }
  function boxOf(items) {
    const pts = items.flatMap(corners);
    const xs = pts.map(q => q[0]), ys = pts.map(q => q[1]);
    const x0 = Math.min(...xs), y0 = Math.min(...ys), x1 = Math.max(...xs), y1 = Math.max(...ys);
    return { x0, y0, x1, y1, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 };
  }
  const CLIP_SVG = '<path d="M15.5 7.5 9 14a2 2 0 0 0 2.8 2.8l7-7a4 4 0 0 0-5.6-5.6l-7.1 7.1a6 6 0 0 0 8.5 8.5L20 14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
  // With a mouse, a knob above what is picked up turns it (fingers twist instead, so a touch
  // screen never shows it).
  let mouse = false;
  const knob = () => mouse && !choosing;
  function drawSel() {
    selG.innerHTML = "";
    if (capSel && board.cap) {
      const b = capBox(board.cap);
      selG.innerHTML = `<rect class="sel-box" x="${b.x - 8}" y="${b.y - 8}" width="${b.w + 16}" height="${b.h + 16}" rx="16"/><rect class="sel-box2" x="${b.x - 8}" y="${b.y - 8}" width="${b.w + 16}" height="${b.h + 16}" rx="16"/>`;
      Pop.show(); return;
    }
    if (!sel.length) { Pop.hide(); return; }
    let out = "";
    // Each piece chosen gets its own outline when there are several; the handles go round them all.
    if (sel.length > 1) for (const it of sel) {
      const c = corners(it);
      out += `<polygon class="sel-one" points="${c.map(q => q.join(",")).join(" ")}"/>`;
    }
    if (sel.length === 1) {
      const it = sel[0], p = byId[it.a], pad = 10 / it.s, x0 = -p.w / 2 - pad, y0 = -p.h / 2 - pad, w = p.w + 2 * pad, h = p.h + 2 * pad, r = 15 / it.s;
      out += `<g transform="translate(${it.x} ${it.y}) rotate(${it.r || 0}) scale(${it.s})"><rect class="sel-box" x="${x0}" y="${y0}" width="${w}" height="${h}" rx="${14 / it.s}"/><rect class="sel-box2" x="${x0}" y="${y0}" width="${w}" height="${h}" rx="${14 / it.s}"/>` +
        (knob() ? `<line class="knob-stem" x1="0" y1="${y0}" x2="0" y2="${y0 - 40 / it.s}"/><circle class="handle rot" data-h="rot" cx="0" cy="${y0 - 40 / it.s}" r="${r}"><title>${t("Drag to turn")}</title></circle>` : "") + `</g>`;
    } else {
      const b = boxOf(sel), x0 = b.x0 - 12, y0 = b.y0 - 12, w = b.x1 - b.x0 + 24, h = b.y1 - b.y0 + 24;
      out += `<rect class="sel-box" x="${x0}" y="${y0}" width="${w}" height="${h}" rx="14"/><rect class="sel-box2" x="${x0}" y="${y0}" width="${w}" height="${h}" rx="14"/>`;
      if (knob()) out += `<line class="knob-stem" x1="${b.cx}" y1="${y0}" x2="${b.cx}" y2="${y0 - 40}"/><circle class="handle rot" data-h="rot" cx="${b.cx}" cy="${y0 - 40}" r="15"><title>${t("Drag to turn")}</title></circle>`;
      if (sel.every(i => i.g && i.g === sel[0].g)) out += `<g transform="translate(${x0 - 14} ${y0 - 14})"><circle cx="14" cy="14" r="16" fill="#fff" stroke="#2646a1" stroke-width="2.5"/><g transform="translate(2 2)" color="#2646a1">${CLIP_SVG}</g></g>`;
    }
    selG.innerHTML = out;
    Pop.show();
  }
  function pickItems(items, announce = true) {
    sel = items ? [...items] : [];
    capSel = false;
    if (!sel.length) choosing = false;
    drawSel();
    if (sel.length && announce) say(t("Picked up: ") + sel.map(nameOf).join(", "));
    // The first time on a touch screen: how to make it bigger or turn it.
    if (sel.length && matchMedia("(pointer: coarse)").matches && !storeGet("sb.pinchHint", false)) {
      storeSet("sb.pinchHint", true);
      notice(t("Pinch with two fingers to make it bigger or smaller, and twist to turn it."));
    }
  }
  const pick = (it, announce) => pickItems(it ? groupOf(it) : [], announce);
  function update() {
    for (const it of sel) { const g = itemsG.querySelector(`[data-k="${it.k}"]`); if (g) place(g, it); }
    drawSel();
  }

  /* ---------- A verse on the board ---------- */
  // board.cap = { text, ref, ver, pos: "bottom" | "top", size }: the words of a passage, brought
  // from the reader, on a felt strip along the bottom (or top) of the scene, with its reference.
  const measure = document.createElement("canvas").getContext("2d");
  const CJK = /[㐀-鿿　-〿＀-￯]/;
  function wrap(text, font, max) {
    measure.font = font;
    const parts = CJK.test(text) ? [...text] : text.split(/(\s+)/);
    const lines = []; let line = "";
    for (const w of parts) {
      const next = line + w;
      if (measure.measureText(next).width > max && line.trim()) { lines.push(line.trim()); line = w.trimStart(); }
      else line = next;
    }
    if (line.trim()) lines.push(line.trim());
    return lines;
  }
  const SERIF = '"Frank Ruhl Libre", "Noto Serif TC", "Noto Serif", Georgia, serif';
  function capLayout(cap) {
    const maxW = W - 200;
    let size = Math.round(42 * (cap.size || 1)), lines;
    for (;;) { lines = wrap(cap.text, `500 ${size}px ${SERIF}`, maxW); if (lines.length <= 5 || size <= 20) break; size -= 2; }
    const lh = Math.round(size * 1.32), refSize = Math.max(18, Math.round(size * 0.62));
    const h = 48 + lines.length * lh + refSize + 20;
    const y = cap.pos === "top" ? 40 : H - 40 - h;
    return { size, lines, lh, refSize, h, y };
  }
  function capBox(cap) { const l = capLayout(cap); return { x: 60, y: l.y, w: W - 120, h: l.h }; }
  function capSVG(cap) {
    if (!cap || !cap.text) return "";
    const l = capLayout(cap), b = capBox(cap);
    const tx = l.lines.map((ln, i) => `<text x="${W / 2}" y="${l.y + 34 + l.size * 0.9 + i * l.lh}" text-anchor="middle" font-family='${SERIF}' font-size="${l.size}" font-weight="500" fill="#2b2420">${esc(ln)}</text>`).join("");
    const ref = `<text x="${W / 2}" y="${l.y + 34 + (l.lines.length - 1) * l.lh + l.size * 0.9 + l.refSize + 22}" text-anchor="middle" font-family='"Libre Franklin", system-ui, sans-serif' font-size="${l.refSize}" font-weight="600" letter-spacing="1" fill="#7a5a2e">${esc(cap.ref + (cap.ver ? " · " + cap.ver : ""))}</text>`;
    return `<g class="cap" role="button" tabindex="0" aria-label="${esc(t("The verse: ") + cap.ref)}"><rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="22" fill="#f6eedb" filter="url(#felt)"/><g class="own">${tx}${ref}</g></g>`;
  }
  function capTool(what) {
    const cap = board.cap; if (!cap) return;
    remember();
    if (what === "move") cap.pos = cap.pos === "top" ? "bottom" : "top";
    else if (what === "smaller") cap.size = Math.max(0.6, (cap.size || 1) / 1.12);
    else if (what === "bigger") cap.size = Math.min(1.6, (cap.size || 1) * 1.12);
    else if (what === "delete") { delete board.cap; capSel = false; say(t("The verse is off the board")); }
    render(); save();
  }

  /* ---------- Changing the pieces picked up ---------- */
  const clampS = s => Math.max(0.15, Math.min(6, s));
  const norm = r => { r = ((r % 360) + 540) % 360 - 180; return Math.round(r * 10) / 10; };
  // Turn and size the pieces round the middle of their box, from where they started (snap).
  function snapshot(items) { return items.map(it => ({ it, x: it.x, y: it.y, s: it.s, r: it.r || 0 })); }
  function transformFrom(snap, cx, cy, k, d) {
    if (snap.some(o => o.s * k < 0.15 || o.s * k > 6)) k = Math.min(...snap.map(o => 6 / o.s), Math.max(...snap.map(o => 0.15 / o.s), k));
    const a = d * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
    for (const o of snap) {
      const dx = (o.x - cx) * k, dy = (o.y - cy) * k;
      o.it.x = Math.round(cx + dx * c - dy * s); o.it.y = Math.round(cy + dx * s + dy * c);
      o.it.s = o.s * k; o.it.r = norm(o.r + d);
    }
  }
  let gid = 0;
  const newClip = () => "c" + Date.now().toString(36) + (gid++);
  function tool(what) {
    if (capSel) { capTool(what); return; }
    if (!sel.length) return;
    if (what === "done") { pickItems([]); return; }
    if (what === "choose") { choosing = true; drawSel(); say(t("Tap the pieces to clip to this one, then Done")); return; }
    if (what === "cancel-choose") { choosing = false; pickItems(groupOf(sel[0]), false); return; }
    remember();
    const b = boxOf(sel), snap = snapshot(sel);
    if (what === "smaller") transformFrom(snap, b.cx, b.cy, 1 / 1.15, 0);
    else if (what === "bigger") transformFrom(snap, b.cx, b.cy, 1.15, 0);
    else if (what === "left") transformFrom(snap, b.cx, b.cy, 1, -15);
    else if (what === "right") transformFrom(snap, b.cx, b.cy, 1, 15);
    else if (what === "flip") for (const it of sel) { it.x = Math.round(2 * b.cx - it.x); it.f = -(it.f || 1); it.r = norm(-(it.r || 0)); }
    else if (what === "flipv") for (const it of sel) { it.y = Math.round(2 * b.cy - it.y); it.f = -(it.f || 1); it.r = norm(180 - (it.r || 0)); }
    else if (what === "front" || what === "back") {
      const moving = board.items.filter(i => sel.includes(i)), rest = board.items.filter(i => !sel.includes(i));
      board.items = what === "front" ? [...rest, ...moving] : [...moving, ...rest];
    } else if (what === "copy") {
      const map = {};
      const copies = board.items.filter(i => sel.includes(i)).map(it => ({ ...it, k: ++uid, x: Math.min(W, it.x + 40), y: Math.min(H, it.y + 30), ...(it.g ? { g: map[it.g] || (map[it.g] = newClip()) } : {}) }));
      board.items.push(...copies); render(); pickItems(copies, false); save(); say(t("Copied: ") + copies.map(nameOf).join(", ")); return;
    } else if (what === "clip") {
      const g = newClip();
      for (const it of sel) it.g = g;
      choosing = false; say(t("Clipped together: ") + sel.map(nameOf).join(", "));
    } else if (what === "unclip") {
      for (const it of sel) delete it.g;
      say(t("Unclipped"));
    } else if (what === "delete") {
      const names = sel.map(nameOf).join(", ");
      board.items = board.items.filter(i => !sel.includes(i)); sel = []; render(); save(); say(t("Taken off the board: ") + names); return;
    }
    render(); save();
    const g = sel[0] && itemsG.querySelector(`[data-k="${sel[0].k}"]`);
    if (kbd && g && document.activeElement !== g && (what === "front" || what === "back")) g.focus();
  }

  /* ---------- The menu over what is picked up ---------- */
  // A small balloon over the pieces, as the reader's balloon over chosen words: the ways to change
  // them, then what to do with them.
  const IC = {
    smaller: '<circle cx="11" cy="11" r="7"/><path d="M8 11h6M20 20l-4-4"/>',
    bigger: '<circle cx="11" cy="11" r="7"/><path d="M8 11h6M11 8v6M20 20l-4-4"/>',
    left: '<path d="M4 12a8 8 0 1 0 2.3-5.6"/><path d="M4 4v5h5"/>',
    right: '<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 4v5h-5"/>',
    flip: '<path d="M12 3v18" stroke-dasharray="2 3"/><path d="M9 7 4 17h5ZM15 7l5 10h-5Z"/>',
    flipv: '<path d="M3 12h18" stroke-dasharray="2 3"/><path d="M7 9 17 4v5ZM7 15l10 5v-5Z"/>',
    front: '<rect x="8" y="8" width="12" height="12" rx="2" fill="currentColor" fill-opacity=".25"/><path d="M4 16V5a1 1 0 0 1 1-1h11"/>',
    back: '<rect x="4" y="4" width="12" height="12" rx="2"/><path d="M20 8v11a1 1 0 0 1-1 1H8"/>',
    copy: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V5a1 1 0 0 1 1-1h11"/>',
    clip: '<path d="M15.5 7.5 9 14a2 2 0 0 0 2.8 2.8l7-7a4 4 0 0 0-5.6-5.6l-7.1 7.1a6 6 0 0 0 8.5 8.5L20 14"/>',
    choose: '<path d="M15.5 7.5 9 14a2 2 0 0 0 2.8 2.8l7-7a4 4 0 0 0-5.6-5.6l-7.1 7.1a6 6 0 0 0 8.5 8.5L20 14"/>',
    unclip: '<path d="M15.5 7.5 9 14a2 2 0 0 0 2.8 2.8l7-7a4 4 0 0 0-5.6-5.6l-7.1 7.1a6 6 0 0 0 8.5 8.5L20 14"/><path d="M3 3l18 18"/>',
    delete: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    done: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    move: '<path d="M12 3v18M7 8l5-5 5 5M7 16l5 5 5-5"/>',
  };
  const icon = k => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${IC[k]}</svg>`;
  const Pop = (() => {
    const pop = $("pop");
    const btn = (k, label, text, cls) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "pb" + (text ? " wide" : "") + (cls ? " " + cls : "");
      b.title = t(label); b.setAttribute("aria-label", t(label));
      b.innerHTML = icon(k) + (text ? `<span>${esc(t(text))}</span>` : "");
      b.onclick = e => { e.stopPropagation(); tool(k); };
      return b;
    };
    const row = (...kids) => { const d = document.createElement("div"); d.className = "prow"; d.append(...kids); return d; };
    function build() {
      if (capSel) {
        return [row(btn("smaller", "Smaller words"), btn("bigger", "Bigger words"), btn("move", board.cap.pos === "top" ? "Move to the bottom" : "Move to the top")),
          row(btn("delete", "Take the verse off the board", "Remove", "del"), btn("done", "Done", "Done"))];
      }
      if (choosing) {
        const n = document.createElement("p"); n.className = "pnote";
        n.textContent = t("Tap the pieces to clip to this one.");
        return [n, row(btn("clip", "Clip them together", "Clip", sel.length > 1 ? "on" : ""), btn("cancel-choose", "Cancel", "Cancel"))];
      }
      const clipped = sel.length > 1 && sel.every(i => i.g && i.g === sel[0].g);
      const clipBtn = clipped ? btn("unclip", "Unclip these pieces", "Unclip") : sel.length > 1 ? btn("clip", "Clip them together", "Clip") : btn("choose", "Clip other pieces to this one", "Clip");
      return [row(btn("smaller", "Smaller"), btn("bigger", "Bigger"), btn("left", "Turn left"), btn("right", "Turn right"), btn("flip", "Flip side to side"), btn("flipv", "Flip upside down")),
        row(btn("front", "Bring to front", "Front"), btn("back", "Send to back", "Back"), btn("copy", "Copy", "Copy"), clipBtn, btn("delete", "Take off the board", "", "del"))];
    }
    let shown = false;
    function show() {
      const opening = !shown;
      pop.replaceChildren(...build());
      pop.hidden = false; shown = true;
      place();
      if (opening) { pop.classList.remove("in"); void pop.offsetWidth; pop.classList.add("in"); }
    }
    function hide() { pop.hidden = true; shown = false; }
    // Above the pieces; below them where there is no room.
    function place() {
      if (pop.hidden) return;
      const m = stage.getScreenCTM();
      let b;
      if (capSel && board.cap) { const c = capBox(board.cap); b = { x0: c.x, y0: c.y, x1: c.x + c.w, y1: c.y + c.h }; }
      else if (sel.length) b = boxOf(sel);
      else return;
      const tl = new DOMPoint(b.x0, b.y0 - (sel.length && knob() ? 95 : 50)).matrixTransform(m), br = new DOMPoint(b.x1, b.y1 + 20).matrixTransform(m);
      const wrapR = $("wrap").getBoundingClientRect();
      const ph = pop.offsetHeight, pw = pop.offsetWidth;
      let top = tl.y - ph - 8, below = false;
      if (top < wrapR.top + 6) { top = br.y + 8; below = true; }
      if (top + ph > innerHeight - 8) { top = Math.max(wrapR.top + 6, innerHeight - ph - 8); }
      const left = Math.max(8, Math.min(innerWidth - pw - 8, (tl.x + br.x) / 2 - pw / 2));
      pop.style.top = top + "px"; pop.style.left = left + "px";
      pop.classList.toggle("below", below);
    }
    addEventListener("resize", place);
    return { show, hide, place };
  })();

  /* ---------- Adding pieces ---------- */
  let added = 0;
  function add(id, x, y) {
    const p = byId[id];
    remember();
    if (x == null) { const k = added++ % 6; x = W / 2 - 150 + k * 60; y = H / 2 - 60 + k * 24; }
    const it = { k: ++uid, a: id, x: Math.round(x), y: Math.round(y), s: p.s, r: 0, f: 1 };
    board.items.push(it);
    render(); pick(it, false); save(); used(id);
    say(t("Added: ") + t(p.name));
    const g = itemsG.querySelector(`[data-k="${it.k}"]`);
    if (g && document.activeElement && document.activeElement.closest(".piece") && kbd) g.focus();
  }
  function setScene(id) {
    if (board.bg === id) return;
    remember(); board.bg = id; render(); save(); used("scene:" + id);
    say(t("Scene: ") + t(sceneById[id].name));
  }

  /* ---------- Moving pieces: pointer ---------- */
  const pts = new Map();
  let drag = null;
  function toBoard(e) {
    const m = stage.getScreenCTM().inverse(), q = new DOMPoint(e.clientX, e.clientY).matrixTransform(m);
    return { x: q.x, y: q.y };
  }
  stage.addEventListener("pointerdown", e => {
    kbd = false;
    mouse = e.pointerType === "mouse";
    const q = toBoard(e);
    pts.set(e.pointerId, q);
    stage.setPointerCapture(e.pointerId);
    if (pts.size === 2 && sel.length) { startPinch(); return; }
    if (pts.size > 2) return;
    const h = e.target.closest && e.target.closest(".handle");
    if (h && sel.length) {
      remember();
      const b = boxOf(sel);
      drag = { mode: h.dataset.h, snap: snapshot(sel), cx: b.cx, cy: b.cy, d0: Math.hypot(q.x - b.cx, q.y - b.cy), a0: Math.atan2(q.y - b.cy, q.x - b.cx) };
      return;
    }
    if (e.target.closest && e.target.closest(".cap")) { pickItems([]); capSel = true; drawSel(); drag = null; return; }
    const g = e.target.closest && e.target.closest(".item");
    if (g) {
      const it = board.items.find(i => i.k === +g.dataset.k), grp = groupOf(it);
      // Choosing pieces to clip, or Shift held: the piece joins (or leaves) those picked up.
      if (choosing || e.shiftKey || e.metaKey || e.ctrlKey) {
        const inSel = sel.includes(it);
        if (choosing && inSel && grp.includes(sel[0])) { drag = null; return; }
        sel = inSel ? sel.filter(i => !grp.includes(i)) : [...sel, ...grp];
        capSel = false; drawSel(); drag = null; return;
      }
      if (!sel.includes(it)) pickItems(grp, false);
      remember();
      drag = { mode: "move", start: q, snap: snapshot(sel), moved: false };
      stage.classList.add("dragging");
      Pop.hide();
      e.preventDefault();
    } else if (e.pointerType === "touch" && sel.length && !choosing) {
      // A finger on the board beside what is picked up: if a second finger joins it, the two
      // pinch the piece; if it lifts alone, the piece is let go.
      drag = { mode: "letgo" };
    } else { if (!choosing) pickItems([]); drag = null; }
  });
  stage.addEventListener("pointermove", e => {
    if (!pts.has(e.pointerId)) return;
    const q = toBoard(e);
    pts.set(e.pointerId, q);
    if (drag && drag.mode === "pinch") { doPinch(); return; }
    if (!drag || drag.mode === "letgo") return;
    if (drag.mode === "move") {
      let dx = q.x - drag.start.x, dy = q.y - drag.start.y;
      if (!drag.moved && Math.hypot(dx, dy) < 3) return;
      drag.moved = true;
      // The pieces stay on the board: the whole group stops at its edges.
      const xs = drag.snap.map(o => o.x), ys = drag.snap.map(o => o.y);
      dx = Math.max(-Math.min(...xs), Math.min(W - Math.max(...xs), dx));
      dy = Math.max(-Math.min(...ys), Math.min(H - Math.max(...ys), dy));
      for (const o of drag.snap) { o.it.x = Math.round(o.x + dx); o.it.y = Math.round(o.y + dy); }
      for (const o of drag.snap) { const g = itemsG.querySelector(`[data-k="${o.it.k}"]`); if (g) place(g, o.it); }
      selG.innerHTML = "";
      return;
    }
    if (drag.mode === "size") transformFrom(drag.snap, drag.cx, drag.cy, Math.hypot(q.x - drag.cx, q.y - drag.cy) / Math.max(1, drag.d0), 0);
    else if (drag.mode === "rot") {
      let d = (Math.atan2(q.y - drag.cy, q.x - drag.cx) - drag.a0) * 180 / Math.PI;
      const r0 = drag.snap[0].r, r = norm(r0 + d);
      if (Math.abs(r) < 4 && drag.snap.length === 1) d = -r0;
      transformFrom(drag.snap, drag.cx, drag.cy, 1, d);
    }
    update();
  });
  const end = e => {
    pts.delete(e.pointerId);
    stage.classList.remove("dragging");
    if (drag && drag.mode === "pinch") { if (pts.size < 2) { drag = null; save(); drawSel(); } return; }
    if (drag && drag.mode === "letgo") { drag = null; if (!pts.size) pickItems([]); return; }
    if (!drag) return;
    if (drag.mode === "move" && !drag.moved) past.pop();     // a tap: nothing to undo
    $("undo").disabled = !past.length;
    drag = null; save(); drawSel();
  };
  stage.addEventListener("pointerup", end);
  stage.addEventListener("pointercancel", end);
  function startPinch() {
    const [a, b] = [...pts.values()];
    if (!drag || drag.mode !== "move") remember();
    if (drag && drag.mode === "move") for (const o of drag.snap) { o.x = o.it.x; o.y = o.it.y; }
    const bx = boxOf(sel);
    drag = { mode: "pinch", snap: snapshot(sel), cx: bx.cx, cy: bx.cy, d0: Math.hypot(b.x - a.x, b.y - a.y), a0: Math.atan2(b.y - a.y, b.x - a.x), mx: (a.x + b.x) / 2, my: (a.y + b.y) / 2 };
    Pop.hide();
  }
  function doPinch() {
    const [a, b] = [...pts.values()];
    transformFrom(drag.snap, drag.cx, drag.cy, Math.hypot(b.x - a.x, b.y - a.y) / Math.max(1, drag.d0), (Math.atan2(b.y - a.y, b.x - a.x) - drag.a0) * 180 / Math.PI);
    // And it goes where the fingers go.
    const dx = (a.x + b.x) / 2 - drag.mx, dy = (a.y + b.y) / 2 - drag.my;
    for (const o of drag.snap) { o.it.x = Math.round(Math.max(0, Math.min(W, o.it.x + dx))); o.it.y = Math.round(Math.max(0, Math.min(H, o.it.y + dy))); }
    for (const o of drag.snap) { const g = itemsG.querySelector(`[data-k="${o.it.k}"]`); if (g) place(g, o.it); }
    selG.innerHTML = "";
  }
  // A mouse wheel or trackpad over the board resizes what is picked up.
  stage.addEventListener("wheel", e => {
    if (!sel.length) return;
    e.preventDefault();
    const b = boxOf(sel);
    // Shift and the wheel turn it (some systems send Shift and the wheel sideways); the wheel alone,
    // or a trackpad's pinch, makes it bigger or smaller.
    if (e.shiftKey) transformFrom(snapshot(sel), b.cx, b.cy, 1, Math.max(-15, Math.min(15, (e.deltaY || e.deltaX) * 0.2)));
    else transformFrom(snapshot(sel), b.cx, b.cy, Math.exp(-e.deltaY * 0.0015), 0);
    update(); clearTimeout(stage._w); stage._w = setTimeout(save, 300);
  }, { passive: false });
  addEventListener("scroll", () => Pop.place(), { passive: true });

  /* ---------- Moving pieces: keyboard ---------- */
  let kbd = false;
  document.addEventListener("keydown", e => { if (e.key === "Tab") kbd = true; });
  function onKey(e) {
    if (!sel.length) return;
    const step = e.shiftKey ? 50 : 10;
    const move = (dx, dy) => () => { for (const it of sel) { it.x = Math.max(0, Math.min(W, it.x + dx)); it.y = Math.max(0, Math.min(H, it.y + dy)); } };
    const act = {
      ArrowLeft: move(-step, 0), ArrowRight: move(step, 0), ArrowUp: move(0, -step), ArrowDown: move(0, step),
      "+": () => tool("bigger"), "=": () => tool("bigger"), "-": () => tool("smaller"),
      f: () => tool("flip"), v: () => tool("flipv"), r: () => tool("right"), R: () => tool("left"), "]": () => tool("front"), "[": () => tool("back"),
      Delete: () => tool("delete"), Backspace: () => tool("delete"), Escape: () => { pickItems([]); stage.focus?.(); },
    }[e.key];
    if (!act) return;
    e.preventDefault();
    if (e.key.startsWith("Arrow")) { if (!e.repeat) remember(); act(); update(); save(); }
    else act();
  }

  /* ---------- The drawers: finding a piece among hundreds ---------- */
  // Tabs for the drawers (with Recent, and Stories, which gather a story's people, things and
  // scenes), groups within each drawer, and a search over names, other words for them, and stories.
  const TAB_COLORS = { recent: "#5b6475", stories: "#c23a7c", people: "#2459c4", animals: "#a8790a", things: "#bf5a1f", nature: "#2f8a3c", scenes: "#6d43c9" };
  const TAB_ICONS = {
    recent: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    stories: '<path d="M12 6.5C10 5 7 4.5 3.5 5v14c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v14"/>',
    people: '<circle cx="12" cy="7" r="4"/><path d="M5 21c0-4 3-7 7-7s7 3 7 7"/>',
    animals: '<circle cx="7" cy="9" r="2"/><circle cx="17" cy="9" r="2"/><circle cx="10" cy="5" r="2"/><circle cx="14" cy="5" r="2"/><path d="M8 17c0-3 2-5 4-5s4 2 4 5-2 3-4 3-4 0-4-3Z"/>',
    things: '<path d="M4 10h16l-2 10H6Z"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    nature: '<path d="M12 21V11"/><path d="M12 13c-5 0-7-4-7-8 5 0 7 3 7 8Zm0 0c5 0 7-4 7-8-5 0-7 3-7 8Z"/>',
    scenes: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 16 5-5 4 4 3-3 6 6"/>',
  };
  const storyById = Object.fromEntries(ART.stories.map(s => [s.id, s]));
  const storeGet = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } };
  const storeSet = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage */ } };
  let tab = storeGet("sb.tab2", "people"), sub = "", story = null, query = "";
  if (!ART.cats.some(c => c[0] === tab)) tab = "people";
  function used(id) { const r = storeGet("sb.recent", []).filter(x => x !== id); r.unshift(id); storeSet("sb.recent", r.slice(0, 40)); }
  function renderTabs() {
    $("tabs").replaceChildren(...ART.cats.map(([id, name]) => {
      const b = document.createElement("button");
      b.type = "button"; b.setAttribute("role", "tab"); b.id = "tab-" + id;
      const on = id === tab && !query;
      b.setAttribute("aria-selected", String(on)); b.setAttribute("aria-controls", "tray");
      b.tabIndex = on ? 0 : -1;
      b.style.setProperty("--tc", TAB_COLORS[id]);
      b.innerHTML = `<i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${TAB_ICONS[id]}</svg></i><b></b>`;
      b.querySelector("b").textContent = t(name);
      b.title = t(name);
      b.onclick = () => { tab = id; sub = ""; story = null; storeSet("sb.tab2", id); if (query) { query = ""; $("find").value = ""; } openDrawer(true); renderTabs(); renderTray(); };
      b.onkeydown = e => {
        const i = ART.cats.findIndex(c => c[0] === tab), n = ART.cats.length;
        const j = e.key === "ArrowRight" || e.key === "ArrowDown" ? (i + 1) % n : e.key === "ArrowLeft" || e.key === "ArrowUp" ? (i + n - 1) % n : -1;
        if (j < 0) return;
        e.preventDefault(); tab = ART.cats[j][0]; sub = ""; story = null; renderTabs(); renderTray(); $("tab-" + tab).focus();
      };
      return b;
    }));
    $("tray").setAttribute("aria-labelledby", "tab-" + tab);
  }
  function thumb(p) { return `<svg viewBox="${-6} ${-6} ${p.w + 12} ${p.h + 12}" aria-hidden="true"><use href="#a-${p.id}" width="${p.w}" height="${p.h}"/></svg>`; }
  const li = node => { const l = document.createElement("li"); l.append(node); return l; };
  function pieceBtn(p) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "piece"; b.style.setProperty("--tc", TAB_COLORS[p.cat]);
    b.dataset.id = p.id;
    b.setAttribute("aria-label", t("Add to the board: ") + t(p.name));
    b.innerHTML = thumb(p) + "<span></span>";
    b.querySelector("span").textContent = t(p.name);
    grab(b, p);
    return li(b);
  }
  function sceneBtn(s) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "piece scene"; b.style.setProperty("--tc", TAB_COLORS.scenes);
    b.dataset.scene = s.id;
    b.setAttribute("aria-pressed", String(board.bg === s.id));
    b.setAttribute("aria-label", t("Scene: ") + t(s.name));
    b.innerHTML = `<svg viewBox="0 0 1600 1000" aria-hidden="true">${s.svg}</svg><span></span>`;
    b.querySelector("span").textContent = t(s.name);
    b.onclick = () => setScene(s.id);
    return li(b);
  }
  // The groups within a drawer, as chips to narrow it down.
  function chips(list, current, onPick, color) {
    const box = $("chips");
    box.hidden = !list.length;
    box.replaceChildren(...list.map(([id, label]) => {
      const b = document.createElement("button");
      b.type = "button"; b.textContent = label; b.style.setProperty("--tc", color);
      b.setAttribute("aria-pressed", String(id === current));
      b.onclick = () => onPick(id);
      return b;
    }));
  }
  // Search: every word asked for must be found in a piece's name (in either language), its other
  // words, its group or its stories; names that begin with the words come first.
  const hay = new Map();
  function haystack(p) {
    if (!hay.has(p.id)) {
      const subName = ((ART.subs[p.cat] || []).find(s => s[0] === p.sub) || [])[1] || "";
      hay.set(p.id, [p.id, p.id.replace(/-/g, " "), p.name, t(p.name), p.tags, subName, t(subName), p.cat, ...(p.stories || []).map(id => storyById[id].name + " " + t(storyById[id].name))].join(" ").toLowerCase());
    }
    return hay.get(p.id);
  }
  function search(q) {
    const words = q.toLowerCase().split(/\s+/).filter(Boolean);
    const score = (name, h) => words.every(w => h.includes(w)) ? (name.startsWith(words[0]) ? 3 : name.includes(words[0]) ? 2 : 1) : 0;
    const pieces = ART.pieces.map(p => [p, score(t(p.name).toLowerCase() + " " + p.name.toLowerCase(), haystack(p))]).filter(x => x[1]).sort((a, b) => b[1] - a[1] || t(a[0].name).localeCompare(t(b[0].name))).map(x => x[0]);
    const scenes = ART.scenes.filter(s => words.every(w => (s.name + " " + t(s.name) + " " + s.id).toLowerCase().includes(w)));
    const stories = ART.stories.filter(s => words.every(w => (s.name + " " + t(s.name) + " " + s.ref).toLowerCase().includes(w)));
    return { pieces, scenes, stories };
  }
  function storyTile(s) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "piece story"; b.style.setProperty("--tc", TAB_COLORS.stories);
    const sc = sceneById[s.scenes[0]] || ART.scenes[0];
    const faces = s.pieces.slice(0, 3).map(id => byId[id]).filter(Boolean);
    b.innerHTML = `<svg viewBox="0 0 1600 1000" aria-hidden="true">${sc.svg}${faces.map((p, i) => { const h = 560, k = h / p.h; return `<use href="#a-${p.id}" x="${420 + i * 380 - p.w * k / 2}" y="${960 - h}" width="${p.w * k}" height="${h}"/>`; }).join("")}</svg><span><b></b><small></small></span>`;
    b.querySelector("b").textContent = t(s.name);
    b.querySelector("small").textContent = s.ref;
    b.onclick = () => { story = s.id; renderTray(); };
    return li(b);
  }
  function renderTray() {
    const tray = $("tray"); tray.scrollLeft = 0; tray.scrollTop = 0;
    const col = TAB_COLORS[tab];
    $("drawer").style.setProperty("--tc", col);
    const items = [];
    let empty = "";
    if (query) {
      chips([], "", null, col);
      const r = search(query);
      items.push(...r.stories.map(storyTile), ...r.pieces.map(pieceBtn), ...r.scenes.map(sceneBtn));
      $("found").textContent = r.pieces.length + r.scenes.length + r.stories.length ? t("{n} found").replace("{n}", r.pieces.length + r.scenes.length + r.stories.length) : "";
      if (!items.length) empty = t("Nothing matches. Try another word, like a name, an animal or a story.");
    } else {
      $("found").textContent = "";
      if (tab === "recent") {
        chips([], "", null, col);
        for (const id of storeGet("sb.recent", [])) {
          if (id.startsWith("scene:")) { const s = sceneById[id.slice(6)]; if (s) items.push(sceneBtn(s)); }
          else if (byId[id]) items.push(pieceBtn(byId[id]));
        }
        if (!items.length) empty = t("The pieces you use show up here.");
      } else if (tab === "stories") {
        if (story && storyById[story]) {
          const s = storyById[story];
          chips([["", "← " + t("All stories")], [s.id, t(s.name)]], s.id, id => { if (!id) { story = null; renderTray(); } }, col);
          items.push(...s.scenes.map(id => sceneById[id]).filter(Boolean).map(sceneBtn), ...s.pieces.map(id => byId[id]).filter(Boolean).map(pieceBtn));
        } else { chips([], "", null, col); items.push(...ART.stories.map(storyTile)); }
      } else if (tab === "scenes") {
        chips([], "", null, col);
        items.push(...ART.scenes.map(sceneBtn));
      } else {
        const subs = (ART.subs[tab] || []).filter(([id]) => ART.pieces.some(p => p.cat === tab && p.sub === id));
        chips(subs.length > 1 ? [["", t("All")], ...subs.map(([id, n]) => [id, t(n)])] : [], sub, id => { sub = id; renderTray(); }, col);
        items.push(...ART.pieces.filter(p => p.cat === tab && (!sub || p.sub === sub)).map(pieceBtn));
      }
    }
    if (empty) { const e = document.createElement("li"); e.className = "tray-empty"; e.textContent = empty; items.push(e); }
    tray.replaceChildren(...items);
  }
  function syncScenes() { for (const b of $("tray").querySelectorAll(".piece.scene")) b.setAttribute("aria-pressed", String(b.dataset.scene === board.bg)); }
  (() => {
    const f = $("find");
    let timer = 0;
    f.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(() => { query = f.value.trim(); renderTabs(); renderTray(); }, 120); });
    f.addEventListener("focus", () => openDrawer(true));
    f.addEventListener("keydown", e => { if (e.key === "Escape" && f.value) { e.stopPropagation(); f.value = ""; query = ""; renderTabs(); renderTray(); } });
  })();

  // A piece: a tap adds it near the middle; pulling it out of the drawer and onto the board puts
  // it where it is dropped.
  const side = () => matchMedia("(min-width: 640px) and (min-aspect-ratio: 1/1)").matches;
  function grab(btn, p) {
    let start = null, ghost = null, id = null;
    btn.addEventListener("pointerdown", e => { if (e.button > 0) return; start = { x: e.clientX, y: e.clientY }; id = e.pointerId; if (e.pointerType === "mouse") e.preventDefault(); });
    btn.addEventListener("pointermove", e => {
      if (!start || e.pointerId !== id) return;
      const dx = e.clientX - start.x, dy = e.clientY - start.y;
      if (!ghost) {
        const out = side() ? dx > 14 && Math.abs(dx) > Math.abs(dy) : dy < -14 && Math.abs(dy) > Math.abs(dx);
        const along = side() ? Math.abs(dy) > 10 : Math.abs(dx) > 10;
        if (along && !out) { start = null; return; }          // scrolling the drawer
        if (!out) return;
        ghost = document.createElement("div"); ghost.className = "ghost"; ghost.innerHTML = thumb(p);
        document.body.append(ghost);
        try { btn.setPointerCapture(id); } catch (err) { /* already released */ }
      }
      ghost.style.left = e.clientX + "px"; ghost.style.top = e.clientY + "px";
    });
    const up = e => {
      if (!start || e.pointerId !== id) return;
      if (ghost) {
        ghost.remove(); ghost = null;
        const r = stage.getBoundingClientRect();
        if (e.type === "pointerup" && e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom) {
          const q = toBoard(e);
          if (q.x >= 0 && q.x <= W && q.y >= 0 && q.y <= H) add(p.id, q.x, q.y);
        }
        btn.dataset.dragged = "1";
      }
      start = null;
    };
    btn.addEventListener("pointerup", up);
    btn.addEventListener("pointercancel", up);
    btn.addEventListener("click", () => { if (btn.dataset.dragged) { delete btn.dataset.dragged; return; } add(p.id); });
  }

  // Pulling the drawer open and shut: a tap on its handle, or a drag along it.
  function openDrawer(open) {
    $("drawer").classList.toggle("closed", !open);
    $("pull").setAttribute("aria-expanded", String(open));
    $("pull").setAttribute("aria-label", t(open ? "Close the drawers" : "Open the drawers"));
  }
  (() => {
    const pull = $("pull"); let y0 = null, x0 = null, moved = false;
    pull.addEventListener("pointerdown", e => { y0 = e.clientY; x0 = e.clientX; moved = false; pull.setPointerCapture(e.pointerId); });
    pull.addEventListener("pointermove", e => {
      if (y0 == null) return;
      const d = side() ? e.clientX - x0 : y0 - e.clientY;
      if (Math.abs(d) > 24) { moved = true; openDrawer(d > 0); y0 = null; }
    });
    pull.addEventListener("pointerup", () => { y0 = null; });
    pull.addEventListener("click", () => { if (moved) { moved = false; return; } openDrawer($("drawer").classList.contains("closed")); });
  })();

  /* ---------- The bar's buttons ---------- */
  $("undo").onclick = undo;
  function clearBoard() {
    if (!board.items.length) return;
    if (!confirm(t("Take every piece off the board?"))) return;
    remember(); board.items = []; delete board.cap; sel = []; render(); save(); say(t("The board is clear"));
  }
  $("present").onclick = () => {
    const sb = $("sb");
    if (document.fullscreenElement) document.exitFullscreen?.();
    else if (sb.requestFullscreen) sb.requestFullscreen().catch(() => {});
    else if (sb.webkitRequestFullscreen) sb.webkitRequestFullscreen();
  };
  if (!document.fullscreenEnabled && !document.webkitFullscreenEnabled) $("present").hidden = true;
  document.addEventListener("keydown", e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "z" && !e.target.closest("input, dialog")) { e.preventDefault(); undo(); }
  });

  /* ---------- The board as a picture: to share, and to print ---------- */
  // The whole board as SVG, with each piece drawn in full (no <use>), so it can become a PNG or
  // be printed. "line": black outlines on white, for colouring; a piece may bring its own line
  // art (p.line), otherwise every shape is outlined.
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function boardSVG(mode) {
    const line = mode === "line";
    const sc = sceneById[board.bg] || ART.scenes[0];
    const pieces = board.items.map(it => {
      const p = byId[it.a];
      return `<g transform="${xf(it)}"${line ? "" : ' filter="url(#felt)"'}><g transform="translate(${-p.w / 2} ${-p.h / 2})">${line && p.line ? `<g class="own">${p.line}</g>` : p.svg}</g></g>`;
    }).join("");
    const style = line ? `<style>:not(.own, .own *){fill:#fff!important;stroke:#1d1d1d!important;stroke-width:2.4px!important;stroke-linejoin:round;stroke-linecap:round;opacity:1!important;fill-opacity:1!important;stroke-opacity:1!important;stroke-dasharray:none!important;vector-effect:non-scaling-stroke}:not(.own *)[fill="none"]{fill:none!important}</style>` : "";
    const filters = line ? "" : $("felt").outerHTML + $("feltbg").outerHTML;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">${style}<defs>${filters}</defs>` +
      `<g${line ? "" : ' filter="url(#feltbg)"'}>${line && sc.line ? `<g class="own">${sc.line}</g>` : sc.svg}</g>${pieces}${capSVG(board.cap).replace(/ role="button" tabindex="0"/, "")}</svg>`;
  }
  function boardPNG(mode = "color") {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const c = document.createElement("canvas"); c.width = W; c.height = H;
        const g = c.getContext("2d"); g.fillStyle = "#fff"; g.fillRect(0, 0, W, H); g.drawImage(img, 0, 0, W, H);
        c.toBlob(b => (b ? resolve(b) : reject(new Error("no picture"))), "image/png");
      };
      img.onerror = reject;
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(boardSVG(mode));
    });
  }
  const fileName = () => (doc.name || "felt-stories").replace(/[\\/:*?"<>|]+/g, "").trim().slice(0, 60) || "felt-stories";
  // Share: the device's own share sheet where it can take a picture (phones, tablets, some
  // desktops); otherwise the picture is saved.
  $("share").onclick = async () => {
    let blob;
    try { blob = await boardPNG(); } catch (e) { say(t("The picture couldn't be made")); return; }
    const file = new File([blob], fileName() + ".png", { type: "image/png" });
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      try { await navigator.share({ files: [file], title: doc.name || t("Felt Stories") }); return; }
      catch (e) { if (e.name === "AbortError") return; }
    }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = file.name;
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    say(t("Picture saved"));
  };
  // Print: in full colour, or as line art to colour in. The page is laid out sideways, with the
  // board's name above it.
  function printBoard(mode) {
    closeMenus();
    const box = $("print");
    box.innerHTML = `<h1>${esc(doc.name || "")}</h1>` + boardSVG(mode);
    box.className = mode === "line" ? "line" : "color";
    const done = () => { box.innerHTML = ""; window.removeEventListener("afterprint", done); };
    window.addEventListener("afterprint", done);
    setTimeout(() => window.print(), 60);
  }
  function closeMenus() { $("print-menu").hidden = true; $("print-btn").setAttribute("aria-expanded", "false"); }
  $("print-btn").onclick = e => {
    e.stopPropagation();
    const m = $("print-menu"), open = m.hidden;
    m.hidden = !open; $("print-btn").setAttribute("aria-expanded", String(open));
    if (open) m.querySelector("button").focus();
  };
  $("print-color").onclick = () => printBoard("color");
  $("print-line").onclick = () => printBoard("line");
  document.addEventListener("click", e => { if (!e.target.closest("#print-menu")) closeMenus(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("print-menu").hidden) { closeMenus(); $("print-btn").focus(); } });

  /* ---------- Syncing with the account ---------- */
  // The same sign-in as the reader's (account.js keeps it in "pe.account"). Boards are sent a few
  // seconds after a change and fetched when the page opens or comes back into view; the newer
  // copy of each board wins. Without an account, or before the account service has the boards
  // table, everything stays on this device.
  const Sync = (() => {
    const C = (window.SITE_CONFIG || {}).supabase || {}, BASE = (C.url || "").replace(/\/+$/, "");
    const acct = () => { try { return JSON.parse(localStorage.getItem("pe.account")) || {}; } catch (e) { return {}; } };
    let state = "off", timer = null, running = false, again = false;
    async function token() {
      const s = acct().session;
      if (!s) return null;
      if (s.expires_at - 60 > Date.now() / 1000) return s.access_token;
      const res = await fetch(BASE + "/auth/v1/token?grant_type=refresh_token", { method: "POST", headers: { apikey: C.key, "Content-Type": "application/json" }, body: JSON.stringify({ refresh_token: s.refresh_token }) });
      if (!res.ok) return null;
      const j = await res.json(), a = acct();
      a.session = { access_token: j.access_token, refresh_token: j.refresh_token, expires_at: j.expires_at || Math.floor(Date.now() / 1000) + (+j.expires_in || 3600), user: s.user };
      try { localStorage.setItem("pe.account", JSON.stringify(a)); } catch (e) { /* storage */ }
      return j.access_token;
    }
    async function call(path, method = "GET", body, extra = {}) {
      const tk = await token();
      if (!tk) throw Object.assign(new Error("signed out"), { out: true });
      const res = await fetch(BASE + path, { method, headers: { apikey: C.key, Authorization: "Bearer " + tk, ...(body ? { "Content-Type": "application/json" } : {}), ...extra }, body: body ? JSON.stringify(body) : undefined });
      if (!res.ok) throw Object.assign(new Error("HTTP " + res.status), { status: res.status });
      const txt = await res.text();
      return txt ? JSON.parse(txt) : null;
    }
    function soon() { clearTimeout(timer); timer = setTimeout(run, 2500); }
    async function run() {
      const who = acct().session;
      if (!BASE || !who) { state = "off"; changed(); return; }
      if (running) { again = true; return; }
      running = true; state = "busy"; changed();
      // Another account than last time: start over, and add this device's boards to it.
      if (lib.user !== who.user.id) { lib.user = who.user.id; lib.pulled = null; for (const d of Object.values(lib.docs)) lib.dirty[d.id] = true; lib.foldersDirty = true; }
      try {
        let cur = false, any = false;
        const since = lib.pulled ? "&synced_at=gt." + encodeURIComponent(lib.pulled) : "";
        const rows = await call("/rest/v1/boards?select=id,name,folder,data,updated_at,deleted,synced_at&order=synced_at.asc" + since);
        for (const r of rows || []) {
          const mine = lib.docs[r.id];
          if (!mine || r.updated_at > mine.t) {
            lib.docs[r.id] = { id: r.id, name: r.name, folder: r.folder, data: r.data || blank(), t: r.updated_at, ...(r.deleted ? { del: true } : {}) };
            delete lib.dirty[r.id]; any = true; if (r.id === doc.id) cur = true;
          } else if (r.updated_at === mine.t) delete lib.dirty[r.id];
          lib.pulled = r.synced_at;
        }
        for (const id of Object.keys(lib.dirty)) {
          const d = lib.docs[id];
          if (!d) { delete lib.dirty[id]; continue; }
          const sent = d.t;
          await call("/rest/v1/rpc/push_board", "POST", { id: d.id, name: d.name || "", folder: d.folder || "", data: d.del ? null : d.data, updated_at: d.t, deleted: !!d.del });
          if (lib.docs[id] && lib.docs[id].t === sent) delete lib.dirty[id];
        }
        const fr = await call("/rest/v1/prefs?select=value,updated_at&key=eq.board_folders");
        const theirs = fr && fr[0];
        if (theirs && theirs.updated_at > (lib.foldersT || 0)) { lib.folders = Array.isArray(theirs.value) ? theirs.value : []; lib.foldersT = theirs.updated_at; lib.foldersDirty = false; any = true; }
        else if (lib.foldersDirty || (!theirs && lib.folders.length)) {
          await call("/rest/v1/rpc/push_pref", "POST", { key: "board_folders", value: lib.folders, updated_at: lib.foldersT || Date.now() });
          lib.foldersDirty = false;
        }
        state = "on"; lib.last = Date.now(); persist();
        if (cur) openDoc(doc.id, true);
        else if (any && doc.del) openDoc(null, true);
        if (any) Library.refresh();
      } catch (e) {
        state = e.out ? "off" : e.status === 404 ? "waiting" : "error";
      }
      running = false; persist(); changed();
      if (again) { again = false; soon(); }
    }
    const listeners = [];
    function changed() { listeners.forEach(f => f(state)); }
    document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") run(); });
    window.addEventListener("online", run);
    // Signing in here, with the same account as the reader. The session is kept where the reader
    // keeps it, marked fresh so the reader also sends what it has saved on this device.
    async function auth(path, body) {
      if (navigator.onLine === false) throw new Error(t("You're offline. Try again when you're connected."));
      const res = await fetch(BASE + path, { method: "POST", headers: { apikey: C.key, "Content-Type": "application/json" }, body: JSON.stringify(body) });
      let j = {};
      try { j = await res.json(); } catch (e) { /* empty */ }
      if (!res.ok) throw new Error(j.msg || j.message || j.error_description || j.error || "HTTP " + res.status);
      return j;
    }
    function keep(s) {
      const a = acct();
      a.session = { access_token: s.access_token, refresh_token: s.refresh_token, expires_at: s.expires_at || Math.floor(Date.now() / 1000) + (+s.expires_in || 3600), user: { id: s.user.id, email: s.user.email } };
      a.fresh = true; a.dirty = a.dirty || {};
      try { localStorage.setItem("pe.account", JSON.stringify(a)); } catch (e) { /* storage */ }
      run();
    }
    const back = () => encodeURIComponent(new URL("index.html", location.href).href);
    async function signIn(email, password) { keep(await auth("/auth/v1/token?grant_type=password", { email, password })); }
    async function signUp(email, password) {
      const s = await auth("/auth/v1/signup?redirect_to=" + back(), { email, password });
      if (s && s.access_token) { keep(s); return "in"; }
      const u = (s && (s.user || s)) || {};
      return Array.isArray(u.identities) && !u.identities.length ? "exists" : "confirm";
    }
    async function recover(email) { await auth("/auth/v1/recover?redirect_to=" + back(), { email }); }
    async function signOut() {
      const s = acct().session;
      if (s) { try { await fetch(BASE + "/auth/v1/logout", { method: "POST", headers: { apikey: C.key, Authorization: "Bearer " + s.access_token } }); } catch (e) { /* offline */ } }
      try { localStorage.setItem("pe.account", JSON.stringify({ dirty: {} })); } catch (e) { /* storage */ }
      state = "off"; changed();
    }
    // Another tab signing in or out.
    window.addEventListener("storage", e => { if (e.key === "pe.account") run(); });
    return { call, soon, run, get state() { return state; }, email: () => (acct().session || {}).user?.email || "", on: f => listeners.push(f), signIn, signUp, recover, signOut, ready: !!BASE };
  })();

  /* ---------- My boards: the library ---------- */
  const DEFAULT = "";
  const folderName = f => f || t("My boards");
  function setFolders(list) { lib.folders = [...new Set(list.filter(Boolean))]; lib.foldersT = Date.now(); lib.foldersDirty = true; persist(); Sync.soon(); }
  function allFolders() { return [DEFAULT, ...new Set([...lib.folders, ...live().map(d => d.folder).filter(Boolean)])]; }
  // A small form: a name, and (for moving or a new board) a folder.
  function ask({ title, value = "", label = t("Name"), folder = null, ok = t("Save") }) {
    return new Promise(resolve => {
      const dlg = $("ask");
      $("ask-title").textContent = title;
      $("ask-label").textContent = label;
      const inp = $("ask-name"); inp.value = value;
      $("ask-name-row").hidden = value === null;
      const selRow = $("ask-folder-row"), selEl = $("ask-folder");
      selRow.hidden = folder === null;
      if (folder !== null) {
        selEl.replaceChildren(...allFolders().map(f => Object.assign(document.createElement("option"), { value: f, textContent: folderName(f), selected: f === folder })));
        selEl.append(Object.assign(document.createElement("option"), { value: "\u0000new", textContent: t("New folder…") }));
      }
      $("ask-ok").textContent = ok;
      const done = v => { dlg.close(); dlg.onclose = null; resolve(v); };
      $("ask-form").onsubmit = async e => {
        e.preventDefault();
        let f = folder === null ? null : selEl.value;
        if (f === "\u0000new") {
          dlg.close();
          const nf = await ask({ title: t("New folder"), label: t("Folder name"), ok: t("Make folder") });
          if (!nf || !nf.name) { resolve(null); return; }
          setFolders([...lib.folders, nf.name]); f = nf.name;
        }
        done({ name: value === null ? null : inp.value.trim().slice(0, 120), folder: f });
      };
      $("ask-cancel").onclick = () => done(null);
      dlg.onclose = () => resolve(null);
      dlg.showModal();
      if (value !== null) { inp.focus(); inp.select(); }
    });
  }
  const Library = (() => {
    const dlg = $("lib");
    let openMore = null;
    function preview(d) {
      const data = cleanData(d.data), sc = sceneById[data.bg] || ART.scenes[0];
      return `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">${sc.svg}${data.items.map(it => { const p = byId[it.a]; return `<use href="#a-${p.id}" x="${-p.w / 2}" y="${-p.h / 2}" width="${p.w}" height="${p.h}" transform="${xf(it)}"/>`; }).join("")}</svg>`;
    }
    const when = ms => { try { return new Date(ms).toLocaleDateString(document.documentElement.lang || undefined, { month: "short", day: "numeric", year: "numeric" }); } catch (e) { return ""; } };
    function status() {
      const s = Sync.state, el = $("lib-status");
      el.textContent = "";
      const link = (label, fn) => { const b = document.createElement("button"); b.type = "button"; b.className = "linkish"; b.textContent = label; b.onclick = fn; return b; };
      if (s === "on" || s === "busy") el.append(s === "busy" ? t("Syncing…") : t("Synced with your account") + (Sync.email() ? " (" + Sync.email() + ")" : "") + ". ", link(t("Sign out"), async () => { await Sync.signOut(); status(); }));
      else if (s === "waiting") el.append(t("Saved on this device. Syncing with your account starts soon."));
      else if (s === "error") el.append(t("Saved on this device. Your account couldn't be reached just now; it will sync later."));
      else {
        el.append(t("Saved on this device. "), link(t("Sign in to keep your boards on every device."), () => SignIn.open()));
      }
      el.dataset.s = s;
    }
    function refresh() {
      if (!dlg.open) return;
      status();
      const box = $("lib-list"); box.textContent = "";
      box.append(shelf());
      for (const f of allFolders()) {
        const docs = live().filter(d => (d.folder || "") === f).sort((a, b) => b.t - a.t);
        const sec = document.createElement("section"); sec.className = "lib-folder";
        const h = document.createElement("h3");
        h.innerHTML = `<i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/></svg></i><span></span><small></small>`;
        h.querySelector("span").textContent = folderName(f);
        h.querySelector("small").textContent = String(docs.length);
        if (f) {
          const more = document.createElement("span"); more.className = "lib-factions";
          more.append(btn(t("Rename"), async () => {
            const r = await ask({ title: t("Rename folder"), value: f, label: t("Folder name") });
            if (!r || !r.name || r.name === f) return;
            for (const d of live().filter(d => d.folder === f)) { d.folder = r.name; touch(d); }
            setFolders(lib.folders.map(x => (x === f ? r.name : x))); refresh();
          }), btn(t("Delete folder"), () => {
            if (docs.length && !confirm(t("Delete this folder? Its boards move to My boards."))) return;
            for (const d of docs) { d.folder = ""; touch(d); }
            setFolders(lib.folders.filter(x => x !== f)); refresh();
          }));
          h.append(more);
        }
        sec.append(h);
        const ul = document.createElement("ul"); ul.className = "lib-grid";
        if (!docs.length) { const li = document.createElement("li"); li.className = "lib-empty"; li.textContent = t("No boards in this folder yet."); ul.append(li); }
        for (const d of docs) {
          const li = document.createElement("li"); li.className = "lib-card" + (d.id === doc.id ? " cur" : "");
          const open = document.createElement("button");
          open.type = "button"; open.className = "lib-open";
          open.innerHTML = preview(d) + "<b></b><small></small>";
          open.querySelector("b").textContent = d.name || untitled();
          open.querySelector("small").textContent = (d.id === doc.id ? t("Open now") + " · " : "") + when(d.t);
          open.onclick = () => { openDoc(d.id); dlg.close(); };
          const more = document.createElement("button");
          more.type = "button"; more.className = "lib-more"; more.setAttribute("aria-label", t("More for ") + (d.name || untitled()));
          more.setAttribute("aria-expanded", String(openMore === d.id));
          more.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>';
          more.onclick = () => { openMore = openMore === d.id ? null : d.id; refresh(); };
          li.append(open, more);
          if (openMore === d.id) {
            const acts = document.createElement("div"); acts.className = "lib-actions";
            acts.append(
              btn(t("Rename"), async () => { const r = await ask({ title: t("Rename board"), value: d.name }); if (r && r.name) { d.name = r.name; touch(d); if (d === doc) showName(); refresh(); } }),
              btn(t("Move"), async () => { const r = await ask({ title: t("Move to a folder"), value: null, folder: d.folder || "", ok: t("Move") }); if (r && r.folder !== null && r.folder !== d.folder) { d.folder = r.folder; touch(d); refresh(); } }),
              btn(t("Duplicate"), () => { const c = newDoc((d.name || untitled()) + " " + t("(copy)"), d.folder, JSON.parse(JSON.stringify(cleanData(d.data)))); lib.docs[c.id] = c; touch(c); openMore = null; refresh(); }),
              btn(t("Delete"), () => {
                if (!confirm(t("Delete this board? This can't be undone."))) return;
                d.del = true; d.data = null; touch(d); openMore = null;
                if (d === doc) openDoc(null, true);
                refresh();
              }, "danger"));
            li.append(acts);
          }
          ul.append(li);
        }
        sec.append(ul);
        box.append(sec);
      }
    }
    // The Felt Stories that come with the app: always here, never deleted. Tapping one opens your
    // own board of it (made the first time), so the story itself stays as it is; Start fresh
    // makes another.
    function shelf() {
      const sec = document.createElement("section"); sec.className = "lib-folder lib-shelf";
      const h = document.createElement("h3");
      h.innerHTML = `<i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.5C10 5 7 4.5 3.5 5v14c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v14"/></svg></i><span></span><small></small>`;
      h.querySelector("span").textContent = t("Felt Stories");
      h.querySelector("small").textContent = String(ART.stories.length);
      const ul = document.createElement("ul"); ul.className = "lib-grid";
      for (const s of ART.stories) {
        const mine = live().filter(d => d.data && d.data.from === s.id).sort((a, b) => b.t - a.t)[0];
        const li = document.createElement("li"); li.className = "lib-card story" + (mine && mine.id === doc.id ? " cur" : "");
        const open = document.createElement("button");
        open.type = "button"; open.className = "lib-open";
        open.innerHTML = preview({ data: s.board || storyData(s.id, null, 5) }) + "<b></b><small></small>";
        open.querySelector("b").textContent = t(s.name);
        open.querySelector("small").textContent = s.ref + (mine ? " · " + t("Yours") : "");
        open.onclick = () => { if (mine) openDoc(mine.id); else start(s); dlg.close(); };
        const more = document.createElement("button");
        more.type = "button"; more.className = "lib-more"; more.setAttribute("aria-label", t("More for ") + t(s.name));
        const key = "story:" + s.id;
        more.setAttribute("aria-expanded", String(openMore === key));
        more.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>';
        more.onclick = () => { openMore = openMore === key ? null : key; refresh(); };
        li.append(open, more);
        if (openMore === key) {
          const acts = document.createElement("div"); acts.className = "lib-actions";
          if (mine) acts.append(btn(t("Open yours"), () => { openDoc(mine.id); dlg.close(); }));
          acts.append(btn(t("Start fresh"), () => { start(s); dlg.close(); }));
          li.append(acts);
        }
        ul.append(li);
      }
      sec.append(h, ul);
      return sec;
    }
    function start(s) {
      const d = newDoc(t(s.name), "", { ...JSON.parse(JSON.stringify(s.board || storyData(s.id, null, 5))), from: s.id });
      lib.docs[d.id] = d; touch(d); openDoc(d.id);
    }
    function btn(label, fn, cls) { const b = document.createElement("button"); b.type = "button"; b.textContent = label; if (cls) b.className = cls; b.onclick = fn; return b; }
    $("boards").onclick = () => { openMore = null; dlg.showModal(); refresh(); Sync.run(); };
    $("lib-close").onclick = () => dlg.close();
    dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
    $("lib-new").onclick = async () => {
      const r = await ask({ title: t("New board"), value: untitled(), folder: doc.folder || "", ok: t("Make board") });
      if (!r) return;
      const d = newDoc(r.name || untitled(), r.folder || "");
      lib.docs[d.id] = d; touch(d); openDoc(d.id); dlg.close();
    };
    $("lib-folder").onclick = async () => {
      const r = await ask({ title: t("New folder"), label: t("Folder name"), ok: t("Make folder") });
      if (r && r.name) { setFolders([...lib.folders, r.name]); refresh(); }
    };
    $("lib-clear").onclick = () => { dlg.close(); clearBoard(); };
    Sync.on(() => { if (dlg.open) status(); });
    return { refresh };
  })();
  /* ---------- Signing in, here ---------- */
  const SignIn = (() => {
    const dlg = $("signin");
    let mode = "in";
    function show(msg, ok) { const m = $("si-msg"); m.textContent = msg || ""; m.hidden = !msg; m.className = "si-msg" + (ok ? " ok" : ""); }
    function said(e) {
      const m = (e && e.message) || "";
      if (/invalid login credentials/i.test(m)) return t("That email and password don't match. Try again, or choose “Forgot your password?”.");
      if (/email not confirmed/i.test(m)) return t("Confirm your email first: open the link we sent you, then sign in.");
      if (/password.*(at least|short|characters)/i.test(m)) return t("Choose a longer password: at least 8 characters.");
      if (/rate limit|too many|security purposes/i.test(m)) return t("Too many tries for now. Wait a minute and try again.");
      return m;
    }
    function setMode(m) {
      mode = m;
      $("si-title").textContent = t(m === "new" ? "Create an account" : m === "reset" ? "Reset your password" : "Sign in");
      $("si-pass-row").hidden = m === "reset";
      $("si-pass").required = m !== "reset";
      $("si-pass").autocomplete = m === "new" ? "new-password" : "current-password";
      $("si-go").textContent = t(m === "new" ? "Create account" : m === "reset" ? "Email me a reset link" : "Sign in");
      $("si-switch").textContent = t(m === "in" ? "New here? Create an account" : "I have an account: sign in");
      $("si-forgot").hidden = m !== "in";
      show("");
    }
    $("si-switch").onclick = () => setMode(mode === "in" ? "new" : "in");
    $("si-forgot").onclick = () => setMode("reset");
    $("si-cancel").onclick = () => dlg.close();
    $("si-form").onsubmit = async e => {
      e.preventDefault();
      const email = $("si-email").value.trim(), pass = $("si-pass").value, go = $("si-go");
      go.disabled = true; show("");
      try {
        if (mode === "in") { await Sync.signIn(email, pass); dlg.close(); say(t("Signed in")); Library.refresh(); }
        else if (mode === "new") {
          const r = await Sync.signUp(email, pass);
          if (r === "in") { dlg.close(); Library.refresh(); }
          else if (r === "exists") { setMode("in"); show(t("There is already an account with this email. Sign in instead.")); }
          else show(t("Check your email: open the link we sent to confirm your account, then sign in here."), true);
        } else { await Sync.recover(email); show(t("We sent a link to reset your password. Open it on this device to choose a new one."), true); }
      } catch (err) { show(said(err)); }
      go.disabled = false;
    };
    return { open: () => { setMode("in"); dlg.showModal(); $("si-email").focus(); } };
  })();
  if (!Sync.ready) $("lib-status").hidden = true;

  $("doc-name").onclick = async () => {
    const r = await ask({ title: t("Rename board"), value: doc.name });
    if (r && r.name) { doc.name = r.name; touch(doc); showName(); }
  };

  /* ---------- A passage from the reader ---------- */
  // The reader's "Felt Stories" leaves the passage in sb.incoming and comes here: it goes on the
  // board open (or a new one), on a strip along the bottom.
  function incoming() {
    const v = storeGet("sb.incoming", null);
    try { localStorage.removeItem("sb.incoming"); } catch (e) { /* storage */ }
    if (location.hash === "#verse") history.replaceState(null, "", location.pathname);
    if (!v || !v.text || Date.now() - (v.t || 0) > 30 * 60e3) return;
    const cap = { text: v.text, ref: v.ref, ver: v.ver || "", pos: "bottom", size: 1 };
    const put = () => { remember(); board.cap = cap; render(); save(); pickItems([]); capSel = true; drawSel(); say(t("Added the verse: ") + v.ref); };
    if (!board.items.length && !board.cap) { put(); return; }
    const dlg = $("verse-in");
    $("vi-ref").textContent = v.ref + (v.ver ? " · " + v.ver : "");
    $("vi-text").textContent = v.text;
    $("vi-this").querySelector("small").textContent = (doc.name || untitled()) + (board.cap ? " — " + t("in place of its verse") : "");
    $("vi-this").onclick = () => { dlg.close(); put(); };
    $("vi-new").onclick = () => { dlg.close(); const d = newDoc(v.ref, doc.folder || ""); lib.docs[d.id] = d; touch(d); openDoc(d.id, true); put(); };
    $("vi-cancel").onclick = () => dlg.close();
    dlg.showModal();
  }
  // Tapping beside the menu lets go of what is picked up.
  document.addEventListener("pointerdown", e => {
    if (choosing || (!sel.length && !capSel)) return;
    if (e.target.closest("#pop, #stage, dialog, .tbtn, .pmenu")) return;
    pickItems([]);
  }, true);

  // A link from a lesson: #story=noah (that story) or #find=word (a search), with &l=q3-7 (the
  // lesson) and &t=its title. The scene being worked on is kept (in Drafts, if it has no folder),
  // and the lesson's own board opens: made the first time, with the story's scene and people,
  // and opened again after that.
  function fromHash() {
    const h = new URLSearchParams(location.hash.slice(1));
    const st = h.get("story") && storyById[h.get("story")] ? h.get("story") : null, find = h.get("find");
    if (!st && !find) return;
    history.replaceState(null, "", location.pathname);
    if (st) { tab = "stories"; story = st; query = ""; $("find").value = ""; }
    else { query = find; $("find").value = query; }
    const key = h.get("l");
    if (key) toLesson(key, h.get("t") || (st ? t(storyById[st].name) : find), st, find);
    openDrawer(true); renderTabs(); renderTray();
  }
  // A story's starting scene: its backdrop, and some of its pieces standing on the ground.
  function storyData(st, find, n = 4) {
    const s = st && storyById[st];
    const ids = s ? s.pieces.filter(id => byId[id]) : search(find || "").pieces.map(p => p.id);
    const items = ids.slice(0, n).map((id, i, all) => {
      const p = byId[id], gap = W / (all.length + 1);
      return { k: i + 1, a: id, x: Math.round(gap * (i + 1)), y: Math.round(H * 0.68 - (p.h * p.s * 0.85) / 2 + 60), s: Math.round(p.s * 0.85 * 100) / 100, r: 0, f: 1 };
    });
    return { bg: (s && sceneById[s.scenes[0]]) ? s.scenes[0] : "hills", items };
  }
  function toLesson(key, title, st, find) {
    let d = live().find(x => x.data && x.data.lesson === key);
    if (d && d === doc) return;
    const busy = board.items.length || board.cap;
    if (busy && !doc.folder) {
      doc.folder = t("Drafts"); touch(doc);
      if (!lib.folders.includes(doc.folder)) setFolders([...lib.folders, doc.folder]);
      notice(t("Your scene “{name}” is kept in Drafts").replace("{name}", doc.name || untitled()));
    } else if (!busy && !(doc.data && doc.data.lesson)) { doc.del = true; doc.data = null; touch(doc); }
    if (!d) {
      d = newDoc(title, t("Lessons"), { ...storyData(st, find), lesson: key });
      lib.docs[d.id] = d; touch(d);
      if (!lib.folders.includes(t("Lessons"))) setFolders([...lib.folders, t("Lessons")]);
    }
    openDoc(d.id, true);
    say(t("Opened: ") + d.name);
  }
  // A short note on the screen, for a moment.
  let noticeTimer = 0;
  function notice(msg) {
    const n = $("notice"); n.textContent = msg; n.hidden = false;
    clearTimeout(noticeTimer); noticeTimer = setTimeout(() => { n.hidden = true; }, 4200);
  }
  addEventListener("hashchange", fromHash);

  // New artwork arriving: into the drawers, the search and the boards that use it.
  function artChanged(rows) {
    installArt(rows); hay.clear();
    renderTabs(); renderTray(); render();
    if ($("lib").open) Library.refresh();
  }
  // The artist's studio: only for the artist's account (the server lets no other account save
  // artwork), and loaded only then.
  function studioButton() {
    const b = $("studio");
    if (!b) return;
    b.hidden = Sync.email().toLowerCase() !== ARTIST;
    b.onclick = () => {
      if (window.Studio) { window.Studio.open(); return; }
      const sc = document.createElement("script"); sc.src = "art-studio.js?v=4"; sc.onload = () => window.Studio && window.Studio.open(); document.head.append(sc);
    };
  }
  window.SB = { ART, W, H, t, byId, sceneById, artMarkup, Sync, notice, installed: rows => { artChanged(rows); try { localStorage.setItem(ART_KEY, JSON.stringify(rows)); } catch (e) { /* storage */ } }, ABASE, ACFG };
  Sync.on(studioButton); studioButton();

  renderTabs(); renderTray(); openDrawer(true); render(); showName(); persist();
  incoming(); fromHash();
  Sync.run(); fetchArt();
})();
