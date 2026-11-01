// The Story Board: a felt board for telling Bible stories. Pieces come out of the drawers (tap
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

  /* ---------- The board's state ---------- */
  let board = load() || { bg: "hills", items: [] };
  let sel = null, uid = board.items.reduce((m, i) => Math.max(m, i.k), 0);
  const past = [];
  function load() { try { const b = JSON.parse(localStorage.getItem(KEY)); return b && Array.isArray(b.items) ? { bg: b.bg, items: b.items.filter(i => byId[i.a]) } : null; } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(board)); } catch (e) { /* storage full or blocked */ } }
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
  $("clear").onclick = () => {
    if (!board.items.length) return;
    if (!confirm(t("Take every piece off the board?"))) return;
    remember(); board.items = []; sel = null; render(); save(); say(t("The board is clear"));
  };
  $("present").onclick = () => {
    const sb = $("sb");
    if (document.fullscreenElement) document.exitFullscreen?.();
    else if (sb.requestFullscreen) sb.requestFullscreen().catch(() => {});
    else if (sb.webkitRequestFullscreen) sb.webkitRequestFullscreen();
  };
  if (!document.fullscreenEnabled && !document.webkitFullscreenEnabled) $("present").hidden = true;
  // A picture of the board, as it is, without the selection.
  $("picture").onclick = () => {
    const s = sel; pick(null);
    const clone = stage.cloneNode(true);
    clone.setAttribute("width", W); clone.setAttribute("height", H);
    clone.querySelector("#sel")?.remove();
    const src = new XMLSerializer().serializeToString(clone);
    const img = new Image();
    img.onload = () => {
      const c = document.createElement("canvas"); c.width = W; c.height = H;
      c.getContext("2d").drawImage(img, 0, 0, W, H);
      c.toBlob(blob => {
        if (!blob) return;
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob); a.download = "story-board.png";
        document.body.append(a); a.click(); a.remove();
        setTimeout(() => URL.revokeObjectURL(a.href), 4000);
        say(t("Picture saved"));
      }, "image/png");
      if (s) pick(s, false);
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(src);
  };
  document.addEventListener("keydown", e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "z") { e.preventDefault(); undo(); }
  });

  renderTabs(); renderTray(); openDrawer(true); render();
})();
