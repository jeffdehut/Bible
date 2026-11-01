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
  for (const p of ART.pieces) {
    const s = document.createElementNS(NS, "symbol");
    s.id = "a-" + p.id; s.setAttribute("viewBox", `0 0 ${p.w} ${p.h}`); s.setAttribute("overflow", "visible");
    s.innerHTML = p.svg;
    defs.append(s);
  }

  /* ---------- The boards: each a saved document, in folders ---------- */
  // lib: { docs: {id: {id, name, folder, data: {bg, items}, t, del?}}, cur: the board open,
  //        folders: [names], foldersT, foldersDirty, dirty: {id: true} not yet sent to the
  //        account, pulled: the server time of the newest change fetched, user: whose account }
  const DOCS = "sb.docs.v1";
  const rid = () => (crypto.randomUUID ? crypto.randomUUID().replace(/-/g, "").slice(0, 20) : Math.random().toString(36).slice(2, 12) + Date.now().toString(36));
  const blank = () => ({ bg: "hills", items: [] });
  const newDoc = (name, folder = "", data = null) => ({ id: rid(), name, folder, data: data || blank(), t: Date.now() });
  const cleanData = d => ({ bg: sceneById[d && d.bg] ? d.bg : "hills", items: ((d && d.items) || []).filter(i => byId[i.a]) });
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
  let sel = null, uid = board.items.reduce((m, i) => Math.max(m, i.k), 0);
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
    past.length = 0; $("undo").disabled = true; sel = null;
    itemsG.textContent = "";
    render(); showName();
    if (!quiet) say(t("Opened: ") + doc.name);
  }
  function showName() { $("doc-name").textContent = doc.name || untitled(); document.title = (doc.name || untitled()) + " · " + t("Felt Stories"); }
  function remember() { past.push(JSON.stringify(board)); if (past.length > 60) past.shift(); $("undo").disabled = false; }
  function undo() {
    if (!past.length) return;
    board = JSON.parse(past.pop()); sel = null;
    $("undo").disabled = !past.length;
    render(); save(); say(t("Undone"));
  }
  const say = msg => { $("live").textContent = ""; requestAnimationFrame(() => { $("live").textContent = msg; }); };
  const nameOf = it => t(byId[it.a].name);

  /* ---------- Drawing ---------- */
  function render() {
    bgG.innerHTML = (sceneById[board.bg] || ART.scenes[0]).svg;
    const keep = new Map([...itemsG.children].map(g => [+g.dataset.k, g]));
    const order = [];
    for (const it of board.items) {
      let g = keep.get(it.k);
      if (!g) g = make(it);
      keep.delete(it.k);
      place(g, it);
      order.push(g);
    }
    for (const g of keep.values()) g.remove();
    order.forEach(g => itemsG.append(g));
    drawSel();
    $("empty").hidden = board.items.length > 0;
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
    g.addEventListener("focus", () => { if (!sel || sel.k !== it.k) pick(board.items.find(i => i.k === +g.dataset.k), false); });
    g.addEventListener("keydown", onKey);
    return g;
  }
  const xf = it => `translate(${it.x} ${it.y}) rotate(${it.r || 0}) scale(${it.s * (it.f || 1)} ${it.s})`;
  function place(g, it) { g.setAttribute("transform", xf(it)); }
  function drawSel() {
    selG.innerHTML = "";
    $("tools").hidden = !sel;
    if (!sel) return;
    const it = sel, p = byId[it.a], pad = 10 / it.s;
    const g = document.createElementNS(NS, "g");
    g.setAttribute("transform", `translate(${it.x} ${it.y}) rotate(${it.r || 0}) scale(${it.s})`);
    const r = 15 / it.s, x0 = -p.w / 2 - pad, y0 = -p.h / 2 - pad, w = p.w + 2 * pad, h = p.h + 2 * pad;
    g.innerHTML = `<rect class="sel-box" x="${x0}" y="${y0}" width="${w}" height="${h}" rx="${8 / it.s}"/><rect class="sel-box2" x="${x0}" y="${y0}" width="${w}" height="${h}" rx="${8 / it.s}"/>` +
      `<line x1="0" y1="${y0}" x2="0" y2="${y0 - 34 / it.s}" stroke="#2646a1" stroke-width="3" vector-effect="non-scaling-stroke"/>` +
      `<circle class="handle rot" data-h="rot" cx="0" cy="${y0 - 34 / it.s}" r="${r}"/>` +
      `<circle class="handle" data-h="size" cx="${x0 + w}" cy="${y0 + h}" r="${r}"/>`;
    selG.append(g);
  }
  function pick(it, announce = true) {
    sel = it || null;
    drawSel();
    if (sel && announce) say(t("Picked up: ") + nameOf(sel));
  }
  function update(it) {
    const g = itemsG.querySelector(`[data-k="${it.k}"]`);
    if (g) place(g, it);
    if (sel === it) drawSel();
  }

  /* ---------- Adding pieces ---------- */
  let added = 0;
  function add(id, x, y) {
    const p = byId[id];
    remember();
    if (x == null) { const k = added++ % 6; x = W / 2 - 150 + k * 60; y = H / 2 - 60 + k * 24; }
    const it = { k: ++uid, a: id, x: Math.round(x), y: Math.round(y), s: p.s, r: 0, f: 1 };
    board.items.push(it);
    render(); pick(it, false); save();
    say(t("Added: ") + t(p.name));
    const g = itemsG.querySelector(`[data-k="${it.k}"]`);
    if (g && document.activeElement && document.activeElement.closest(".piece") && kbd) g.focus();
  }
  function setScene(id) {
    if (board.bg === id) return;
    remember(); board.bg = id; render(); save();
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
    const q = toBoard(e);
    pts.set(e.pointerId, q);
    stage.setPointerCapture(e.pointerId);
    if (pts.size === 2 && sel) { startPinch(); return; }
    if (pts.size > 2) return;
    const h = e.target.closest && e.target.closest(".handle");
    if (h && sel) {
      remember();
      drag = { mode: h.dataset.h, it: sel, s0: sel.s, r0: sel.r || 0, d0: Math.hypot(q.x - sel.x, q.y - sel.y), a0: Math.atan2(q.y - sel.y, q.x - sel.x) };
      return;
    }
    const g = e.target.closest && e.target.closest(".item");
    if (g) {
      const it = board.items.find(i => i.k === +g.dataset.k);
      pick(it, false);
      remember();
      drag = { mode: "move", it, dx: q.x - it.x, dy: q.y - it.y, moved: false };
      stage.classList.add("dragging");
      e.preventDefault();
    } else { pick(null); drag = null; }
  });
  stage.addEventListener("pointermove", e => {
    if (!pts.has(e.pointerId)) return;
    const q = toBoard(e);
    pts.set(e.pointerId, q);
    if (drag && drag.mode === "pinch") { doPinch(); return; }
    if (!drag) return;
    const it = drag.it;
    if (drag.mode === "move") {
      it.x = Math.round(Math.max(0, Math.min(W, q.x - drag.dx)));
      it.y = Math.round(Math.max(0, Math.min(H, q.y - drag.dy)));
      drag.moved = true;
    } else if (drag.mode === "size") {
      const d = Math.hypot(q.x - it.x, q.y - it.y);
      it.s = clampS(drag.s0 * d / Math.max(1, drag.d0));
    } else if (drag.mode === "rot") {
      let r = drag.r0 + (Math.atan2(q.y - it.y, q.x - it.x) - drag.a0) * 180 / Math.PI;
      r = ((r + 540) % 360) - 180;
      if (Math.abs(r) < 4) r = 0;
      it.r = Math.round(r);
    }
    update(it);
  });
  const end = e => {
    pts.delete(e.pointerId);
    if (drag && drag.mode === "pinch") { if (pts.size < 2) { drag = null; save(); } return; }
    if (!drag) return;
    if (drag.mode === "move" && !drag.moved) past.pop();     // a tap: nothing to undo
    $("undo").disabled = !past.length;
    drag = null; stage.classList.remove("dragging"); save();
  };
  stage.addEventListener("pointerup", end);
  stage.addEventListener("pointercancel", end);
  const clampS = s => Math.max(0.2, Math.min(5, s));
  function startPinch() {
    const [a, b] = [...pts.values()];
    if (!drag || drag.mode !== "move") remember();
    drag = { mode: "pinch", it: sel, s0: sel.s, r0: sel.r || 0, d0: Math.hypot(b.x - a.x, b.y - a.y), a0: Math.atan2(b.y - a.y, b.x - a.x) };
  }
  function doPinch() {
    const [a, b] = [...pts.values()], it = drag.it;
    it.s = clampS(drag.s0 * Math.hypot(b.x - a.x, b.y - a.y) / Math.max(1, drag.d0));
    it.r = Math.round(drag.r0 + (Math.atan2(b.y - a.y, b.x - a.x) - drag.a0) * 180 / Math.PI);
    update(it);
  }
  // A mouse wheel or trackpad over a picked-up piece resizes it.
  stage.addEventListener("wheel", e => {
    if (!sel) return;
    e.preventDefault();
    sel.s = clampS(sel.s * Math.exp(-e.deltaY * 0.0015));
    update(sel); clearTimeout(stage._w); stage._w = setTimeout(save, 300);
  }, { passive: false });

  /* ---------- Moving pieces: keyboard ---------- */
  let kbd = false;
  document.addEventListener("keydown", e => { if (e.key === "Tab") kbd = true; });
  function onKey(e) {
    const it = sel; if (!it) return;
    const step = e.shiftKey ? 50 : 10;
    const act = {
      ArrowLeft: () => { it.x = Math.max(0, it.x - step); }, ArrowRight: () => { it.x = Math.min(W, it.x + step); },
      ArrowUp: () => { it.y = Math.max(0, it.y - step); }, ArrowDown: () => { it.y = Math.min(H, it.y + step); },
      "+": () => tool("bigger"), "=": () => tool("bigger"), "-": () => tool("smaller"),
      f: () => tool("flip"), r: () => tool("turn"), "]": () => tool("front"), "[": () => tool("back"),
      Delete: () => tool("delete"), Backspace: () => tool("delete"), Escape: () => { pick(null); stage.focus?.(); },
    }[e.key];
    if (!act) return;
    e.preventDefault();
    if (e.key.startsWith("Arrow")) { if (!e.repeat) remember(); act(); update(it); save(); }
    else act();
  }

  /* ---------- The tools for the piece picked up ---------- */
  const IC = {
    smaller: '<circle cx="11" cy="11" r="7"/><path d="M8 11h6M20 20l-4-4"/>',
    bigger: '<circle cx="11" cy="11" r="7"/><path d="M8 11h6M11 8v6M20 20l-4-4"/>',
    turn: '<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 4v5h-5"/>',
    flip: '<path d="M12 3v18" stroke-dasharray="2 3"/><path d="M9 7 4 17h5ZM15 7l5 10h-5Z"/>',
    front: '<rect x="8" y="8" width="12" height="12" rx="2" fill="currentColor" fill-opacity=".25"/><path d="M4 16V5a1 1 0 0 1 1-1h11"/>',
    back: '<rect x="4" y="4" width="12" height="12" rx="2"/><path d="M20 8v11a1 1 0 0 1-1 1H8"/>',
    copy: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V5a1 1 0 0 1 1-1h11"/>',
    delete: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    done: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
  };
  const TOOLS = [["smaller", "Smaller"], ["bigger", "Bigger"], ["turn", "Turn"], ["flip", "Flip"], "|", ["front", "Bring to front"], ["back", "Send to back"], ["copy", "Copy"], "|", ["delete", "Take off the board"], ["done", "Done"]];
  $("tools").replaceChildren(...TOOLS.map(x => {
    if (x === "|") return Object.assign(document.createElement("span"), { className: "sep" });
    const b = document.createElement("button");
    b.type = "button"; b.title = t(x[1]); b.setAttribute("aria-label", t(x[1]));
    if (x[0] === "delete") b.className = "del";
    b.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${IC[x[0]]}</svg>`;
    b.onclick = () => tool(x[0]);
    return b;
  }));
  function tool(what) {
    const it = sel; if (!it) return;
    const i = board.items.indexOf(it);
    if (what === "done") { pick(null); return; }
    remember();
    if (what === "smaller") it.s = clampS(it.s / 1.15);
    else if (what === "bigger") it.s = clampS(it.s * 1.15);
    else if (what === "turn") it.r = (((it.r || 0) + 15 + 180) % 360) - 180;
    else if (what === "flip") it.f = -(it.f || 1);
    else if (what === "front") { board.items.splice(i, 1); board.items.push(it); }
    else if (what === "back") { board.items.splice(i, 1); board.items.unshift(it); }
    else if (what === "copy") {
      const c = { ...it, k: ++uid, x: Math.min(W, it.x + 40), y: Math.min(H, it.y + 30) };
      board.items.push(c); render(); pick(c, false); save(); say(t("Copied: ") + nameOf(c)); return;
    } else if (what === "delete") {
      board.items.splice(i, 1); const n = nameOf(it); sel = null; render(); save(); say(t("Taken off the board: ") + n); return;
    }
    render(); save();
    const g = itemsG.querySelector(`[data-k="${it.k}"]`);
    if (kbd && g && document.activeElement !== g && (what === "front" || what === "back")) g.focus();
  }

  /* ---------- The drawers ---------- */
  const TAB_COLORS = { people: "#2459c4", animals: "#a8790a", things: "#bf5a1f", nature: "#2f8a3c", scenes: "#6d43c9" };
  const TAB_ICONS = {
    people: '<circle cx="12" cy="7" r="4"/><path d="M5 21c0-4 3-7 7-7s7 3 7 7"/>',
    animals: '<circle cx="7" cy="9" r="2"/><circle cx="17" cy="9" r="2"/><circle cx="10" cy="5" r="2"/><circle cx="14" cy="5" r="2"/><path d="M8 17c0-3 2-5 4-5s4 2 4 5-2 3-4 3-4 0-4-3Z"/>',
    things: '<path d="M4 10h16l-2 10H6Z"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    nature: '<path d="M12 21V11"/><path d="M12 13c-5 0-7-4-7-8 5 0 7 3 7 8Zm0 0c5 0 7-4 7-8-5 0-7 3-7 8Z"/>',
    scenes: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 16 5-5 4 4 3-3 6 6"/>',
  };
  let tab = (() => { try { return localStorage.getItem("sb.tab") || "people"; } catch (e) { return "people"; } })();
  if (!ART.cats.some(c => c[0] === tab)) tab = "people";
  function renderTabs() {
    $("tabs").replaceChildren(...ART.cats.map(([id, name]) => {
      const b = document.createElement("button");
      b.type = "button"; b.setAttribute("role", "tab"); b.id = "tab-" + id;
      b.setAttribute("aria-selected", String(id === tab)); b.setAttribute("aria-controls", "tray");
      b.tabIndex = id === tab ? 0 : -1;
      b.style.setProperty("--tc", TAB_COLORS[id]);
      b.innerHTML = `<i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${TAB_ICONS[id]}</svg></i><b></b>`;
      b.querySelector("b").textContent = t(name);
      b.title = t(name);
      b.onclick = () => { tab = id; try { localStorage.setItem("sb.tab", id); } catch (e) { /* no storage */ } openDrawer(true); renderTabs(); renderTray(); };
      b.onkeydown = e => {
        const i = ART.cats.findIndex(c => c[0] === tab), n = ART.cats.length;
        const j = e.key === "ArrowRight" || e.key === "ArrowDown" ? (i + 1) % n : e.key === "ArrowLeft" || e.key === "ArrowUp" ? (i + n - 1) % n : -1;
        if (j < 0) return;
        e.preventDefault(); tab = ART.cats[j][0]; renderTabs(); renderTray(); $("tab-" + tab).focus();
      };
      return b;
    }));
    $("tray").setAttribute("aria-labelledby", "tab-" + tab);
  }
  function thumb(p) { return `<svg viewBox="${-6} ${-6} ${p.w + 12} ${p.h + 12}" aria-hidden="true"><use href="#a-${p.id}" width="${p.w}" height="${p.h}"/></svg>`; }
  function renderTray() {
    const tray = $("tray"); tray.scrollLeft = 0; tray.scrollTop = 0;
    const col = TAB_COLORS[tab];
    if (tab === "scenes") {
      tray.replaceChildren(...ART.scenes.map(s => {
        const li = document.createElement("li"), b = document.createElement("button");
        b.type = "button"; b.className = "piece scene"; b.style.setProperty("--tc", col);
        b.setAttribute("aria-pressed", String(board.bg === s.id));
        b.innerHTML = `<svg viewBox="0 0 1600 1000" aria-hidden="true">${s.svg}</svg><span></span>`;
        b.querySelector("span").textContent = t(s.name);
        b.onclick = () => setScene(s.id);
        li.append(b); return li;
      }));
      return;
    }
    tray.replaceChildren(...ART.pieces.filter(p => p.cat === tab).map(p => {
      const li = document.createElement("li"), b = document.createElement("button");
      b.type = "button"; b.className = "piece"; b.style.setProperty("--tc", col);
      b.dataset.id = p.id;
      b.setAttribute("aria-label", t("Add to the board: ") + t(p.name));
      b.innerHTML = thumb(p) + "<span></span>";
      b.querySelector("span").textContent = t(p.name);
      grab(b, p);
      li.append(b); return li;
    }));
  }
  function syncScenes() { if (tab === "scenes") for (const b of $("tray").querySelectorAll(".piece.scene")) b.setAttribute("aria-pressed", String(b.querySelector("span").textContent === t(sceneById[board.bg].name))); }

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
    remember(); board.items = []; sel = null; render(); save(); say(t("The board is clear"));
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
      `<g${line ? "" : ' filter="url(#feltbg)"'}>${sc.svg}</g>${pieces}</svg>`;
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
    async function call(path, method = "GET", body) {
      const tk = await token();
      if (!tk) throw Object.assign(new Error("signed out"), { out: true });
      const res = await fetch(BASE + path, { method, headers: { apikey: C.key, Authorization: "Bearer " + tk, ...(body ? { "Content-Type": "application/json" } : {}) }, body: body ? JSON.stringify(body) : undefined });
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
    return { soon, run, get state() { return state; }, email: () => (acct().session || {}).user?.email || "", on: f => listeners.push(f), signIn, signUp, recover, signOut, ready: !!BASE };
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

  renderTabs(); renderTray(); openDrawer(true); render(); showName(); persist();
  Sync.run();
})();
