// Sharing: a square picture (1080 × 1080, for social media) of a verse, a connection or a moment in
// history, with a link back to the same place on the site. Phones share the picture and the link
// through the system's share sheet; elsewhere a small window shows the picture with "Save image"
// and "Copy link". Used by the reader (index.html), the web (graph.html) and the timeline
// (history.html), each of which calls Share.verse, Share.web or Share.history, and the web in 3D
// (web3d.html), which calls Share.snapshot.
(() => {
  const SIZE = 1080;
  const SITE = "bibledata.org";
  const READ = '"Frank Ruhl Libre", "Noto Serif", Georgia, serif';
  const SANS = '"Libre Franklin", system-ui, -apple-system, "Segoe UI", sans-serif';
  const INK = "#161b26", MUTED = "#5b6475", PAPER = "#fbfaf7", LAPIS = "#2646a1", GOLD = "#8a640b";

  // The site's address for a page and its fragment, wherever this copy of the site is served.
  const here = (page, hash) => new URL(page + (hash || ""), location.href).href;
  // The link as printed on the picture: in full when short, else the site and page alone.
  const shortUrl = url => {
    const u = url.replace(/^https?:\/\//, "").replace(/\/index\.html/, "/").replace(/\/$/, "");
    return u.length <= 36 ? u : u.replace(/#.*$/, "").replace(/\/$/, "");
  };

  function canvas() {
    const c = document.createElement("canvas");
    c.width = c.height = SIZE;
    return [c, c.getContext("2d")];
  }
  // Words into lines no wider than w; returns the lines.
  function wrap(g, text, w) {
    const out = [];
    for (const para of String(text).split("\n")) {
      let line = "";
      for (const word of para.split(/\s+/).filter(Boolean)) {
        const t = line ? line + " " + word : word;
        if (g.measureText(t).width > w && line) { out.push(line); line = word; } else line = t;
      }
      out.push(line);
    }
    return out;
  }
  // The largest font size (from max down) at which the text fits in w × h.
  function fit(g, text, font, max, min, w, h, lead = 1.32) {
    for (let s = max; s >= min; s -= 2) {
      g.font = font(s);
      const lines = wrap(g, text, w);
      if (lines.length * s * lead <= h) return { size: s, lines, lead };
    }
    g.font = font(min);
    const lines = wrap(g, text, w);
    const keep = Math.max(1, Math.floor(h / (min * lead)));
    if (lines.length > keep) { lines.length = keep; lines[keep - 1] = lines[keep - 1].replace(/\s*\S*$/, "") + "…"; }
    return { size: min, lines, lead };
  }
  let icon = null;
  function loadIcon() {
    if (!icon) icon = new Promise(res => {
      const im = new Image();
      im.onload = () => res(im); im.onerror = () => res(null);
      im.src = new URL("icons/icon.svg", location.href).href;
    });
    return icon;
  }
  // The foot of every picture: the icon, the site's name and the link.
  async function footer(g, url, dark) {
    const im = await loadIcon();
    const y = SIZE - 96;
    g.globalAlpha = 1;
    if (im) g.drawImage(im, 72, y - 22, 52, 52);
    g.fillStyle = dark ? "#e9ecf3" : INK;
    g.font = `500 30px ${READ}`;
    g.textBaseline = "middle";
    g.fillText("BibleData.org", 140, y + 4);
    g.font = `600 24px ${SANS}`;
    g.fillStyle = dark ? "#9db3ff" : LAPIS;
    g.textAlign = "right";
    g.fillText(shortUrl(url), SIZE - 72, y + 4);
    g.textAlign = "left";
  }
  const ready = () => (document.fonts ? document.fonts.ready : Promise.resolve());

  /* ---------- A verse ---------- */
  async function verse({ ref, text, url, note }) {
    await ready();
    const [c, g] = canvas();
    const grad = g.createLinearGradient(0, 0, SIZE, SIZE);
    grad.addColorStop(0, "#fdfcf9"); grad.addColorStop(1, "#efe8d6");
    g.fillStyle = grad; g.fillRect(0, 0, SIZE, SIZE);
    // A quiet frame, as on the maps.
    g.strokeStyle = "rgba(138,100,11,0.35)"; g.lineWidth = 3; g.strokeRect(40, 40, SIZE - 80, SIZE - 80);
    const box = fit(g, text, s => `400 ${s}px ${READ}`, 64, 30, SIZE - 220, 600);
    // The verse, its mark and its reference, as one block in the middle of the page.
    const blockH = 110 + box.lines.length * box.size * box.lead + 110;
    let y = Math.max(140, (SIZE - 120 - blockH) / 2 + 40);
    g.fillStyle = GOLD; g.font = `400 150px ${READ}`; g.textBaseline = "alphabetic";
    g.fillText("“", 96, y + 100);
    y += 110 + box.size;
    g.fillStyle = INK; g.font = `400 ${box.size}px ${READ}`;
    for (const line of box.lines) { g.fillText(line, 110, y); y += box.size * box.lead; }
    g.fillStyle = LAPIS; g.font = `600 36px ${SANS}`;
    g.fillText(ref, 110, Math.min(y + 40, 880));
    if (note) { g.fillStyle = MUTED; g.font = `500 22px ${SANS}`; g.fillText(note, 110, Math.min(y + 82, 922)); }
    await footer(g, url, false);
    return open(c, { title: ref, text: `${ref}: “${text}”`, url, filename: ref.replace(/[^\w]+/g, "-") });
  }

  /* ---------- A sketch, on its paper ---------- */
  // paths: [{d, color}] in the sketch's own units (unit across); ref and quote: the words it was
  // drawn for.
  async function sketch({ paths, unit = 288, paper = "#fbfdff", grid = null, ref, quote, url }) {
    await ready();
    const [c, g] = canvas();
    // The sketch alone, a square of paper on a warm background, slightly turned.
    const desk = g.createLinearGradient(0, 0, SIZE, SIZE);
    desk.addColorStop(0, "#e6dcc6"); desk.addColorStop(1, "#d3c4a4");
    g.fillStyle = desk; g.fillRect(0, 0, SIZE, SIZE);
    const sq = 640, sx = SIZE / 2, sy = 90 + sq / 2;
    g.save();
    g.translate(sx, sy); g.rotate(-0.012);
    g.shadowColor = "rgba(60,45,10,0.30)"; g.shadowBlur = 30; g.shadowOffsetY = 10;
    g.fillStyle = paper; g.fillRect(-sq / 2, -sq / 2, sq, sq);
    g.shadowColor = "transparent";
    g.scale(sq / unit, sq / unit); g.translate(-unit / 2, -unit / 2);
    // Graph paper: a line every grid step, a stronger one every fourth.
    if (grid) for (let v = grid.step, i = 1; v < unit; v += grid.step, i++) {
      g.strokeStyle = i % 4 ? grid.minor : grid.major; g.lineWidth = i % 4 ? 0.8 : 1;
      g.beginPath(); g.moveTo(v, 0); g.lineTo(v, unit); g.moveTo(0, v); g.lineTo(unit, v); g.stroke();
    }
    for (const p of paths) { g.fillStyle = p.color; g.fill(new Path2D(p.d)); }
    g.restore();
    const px = sx - sq / 2 - 20, pw = sq + 40;
    // What it was drawn for.
    let y = sy + sq / 2 + 70;
    g.textBaseline = "alphabetic";
    g.fillStyle = LAPIS; g.font = `600 34px ${SANS}`;
    g.fillText(ref, px + 20, y);
    if (quote) {
      const box = fit(g, `“${quote}”`, s => `italic 400 ${s}px ${READ}`, 28, 22, pw - 40, 76, 1.3);
      g.fillStyle = MUTED; g.font = `italic 400 ${box.size}px ${READ}`;
      y += 14;
      for (const line of box.lines) { y += box.size * box.lead; g.fillText(line, px + 20, y); }
    }
    await footer(g, url, false);
    return open(c, { title: ref, text: ref, url, filename: "sketch-" + ref.replace(/[^\w]+/g, "-") });
  }

  /* ---------- A connection: the chosen point and its threads ---------- */
  // center: {label, sub, color}; nodes: [{label, color, ring}] (the strongest first, up to 14).
  /* ---------- The icons of the web's points ---------- */
  // Drawn on a 24-unit square as strokes, one SVG path each, so the same shapes serve the page
  // (as SVG), its canvas and these pictures (as Path2D).
  const ICONS = {
    torah: "M4 20V8a3 3 0 0 1 6 0v12ZM14 20V8a3 3 0 0 1 6 0v12ZM6 11h2M6 14h2M16 11h2M16 14h2",
    history: "M3 8l4.2 4L12 6l4.8 6L21 8l-2 11H5Z",
    wisdom: "M3.5 13.5h12.5a3.5 3.5 0 0 0 3.5-3.5h-2.5l-2.5 3.5M3.5 13.5c0 3 3 5 7 5s6.5-2 6.5-5M10.5 18.5V21M7 21h7M9.5 10c1.6-1.4 1.6-3 0-5-1 1.5-2.4 2-2.4 3.4S8.5 10 9.5 10Z",
    prophets: "M3 10v4h3l7 4V6l-7 4ZM16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11",
    gospels: "M12 3v18M7 8.5h10",
    acts: "M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.5 1.5-4 2.5-5.5.3 1.8 1.2 2.8 2.5 3 .2-2.8-1-5 0-7.5Z",
    letters: "M3 6h18v12H3ZM3.5 6.5 12 13l8.5-6.5",
    revelation: "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9Z",
    person: "M12 4a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7ZM5 21c0-4 3-7 7-7s7 3 7 7",
    place: "M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11ZM12 7.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5Z",
    event: "M12 2.5v5.5M12 16v5.5M2.5 12H8M16 12h5.5M5.3 5.3l3.6 3.6M15.1 15.1l3.6 3.6M5.3 18.7l3.6-3.6M15.1 8.9l3.6-3.6",
  };
  const paths = {};
  // An icon centred at (x, y), `size` across, drawn in `color`.
  function drawIcon(g, name, x, y, size, color, weight = 2) {
    if (!ICONS[name]) return;
    const p = paths[name] || (paths[name] = new Path2D(ICONS[name]));
    g.save();
    g.translate(x - size / 2, y - size / 2); g.scale(size / 24, size / 24);
    g.strokeStyle = color; g.lineWidth = weight; g.lineCap = "round"; g.lineJoin = "round"; g.shadowBlur = 0;
    g.stroke(p);
    g.restore();
  }


  async function web({ center, nodes, url, caption }) {
    await ready();
    const [c, g] = canvas();
    const grad = g.createRadialGradient(SIZE / 2, SIZE / 2 - 40, 60, SIZE / 2, SIZE / 2, SIZE * 0.75);
    grad.addColorStop(0, "#1b2442"); grad.addColorStop(1, "#05070d");
    g.fillStyle = grad; g.fillRect(0, 0, SIZE, SIZE);
    // A faint field of stars, always the same for the same point.
    let seed = [...center.label].reduce((a, ch) => a * 31 + ch.charCodeAt(0), 7) >>> 0;
    const rnd = () => ((seed = (seed * 1103515245 + 12345) >>> 0) / 4294967296);
    for (let k = 0; k < 260; k++) { g.fillStyle = `rgba(200,210,255,${0.08 + rnd() * 0.25})`; g.beginPath(); g.arc(rnd() * SIZE, rnd() * SIZE, rnd() * 2.2, 0, 7); g.fill(); }
    // The title at the top, and the web in the space below it, clear of the words.
    const cx = SIZE / 2, cy = 628, R = 256;
    const ns = nodes.slice(0, 14);
    const at = ns.map((n, k) => { const a = -Math.PI / 2 + (2 * Math.PI * k) / ns.length; const r = R * (k % 2 ? 0.86 : 1); return [cx + r * Math.cos(a), cy + r * Math.sin(a), a]; });
    // Threads, glowing.
    g.lineCap = "round";
    ns.forEach((n, k) => {
      const [x, y] = at[k];
      const lg = g.createLinearGradient(cx, cy, x, y); lg.addColorStop(0, center.color); lg.addColorStop(1, n.color);
      g.strokeStyle = lg; g.globalAlpha = 0.85; g.lineWidth = 4; g.shadowColor = n.color; g.shadowBlur = 18;
      g.beginPath(); g.moveTo(cx, cy); g.lineTo(x, y); g.stroke();
    });
    g.globalAlpha = 1;
    // The points.
    ns.forEach((n, k) => {
      const [x, y] = at[k];
      g.shadowColor = n.color; g.shadowBlur = 26; g.fillStyle = n.color;
      g.beginPath(); g.arc(x, y, n.ring ? 19 : 21, 0, 7);
      if (n.ring) { g.lineWidth = 5; g.strokeStyle = n.color; g.stroke(); } else g.fill();
    });
    g.shadowBlur = 50; g.shadowColor = center.color; g.fillStyle = center.color;
    g.beginPath(); g.arc(cx, cy, 56, 0, 7); g.fill();
    g.shadowBlur = 0;
    // Each point's icon: dark on a filled point, in its own color inside a ring.
    ns.forEach((n, k) => { const [x, y] = at[k]; drawIcon(g, n.icon, x, y, n.ring ? 17 : 21, n.ring ? n.color : "#0b1020", n.ring ? 2.4 : 2.6); });
    drawIcon(g, center.icon, cx, cy, 60, "#0b1020", 2);
    // Labels, outside each point.
    g.textBaseline = "middle";
    ns.forEach((n, k) => {
      const [x, y, a] = at[k];
      const right = Math.cos(a) >= -0.05;
      g.font = `600 26px ${SANS}`; g.textAlign = Math.abs(Math.cos(a)) < 0.3 ? "center" : right ? "left" : "right";
      const lx = x + (Math.abs(Math.cos(a)) < 0.3 ? 0 : right ? 34 : -34), ly = y + (Math.abs(Math.cos(a)) < 0.3 ? (Math.sin(a) < 0 ? -42 : 42) : 0);
      g.lineWidth = 6; g.strokeStyle = "rgba(5,7,13,0.85)"; g.strokeText(n.label, lx, ly);
      g.fillStyle = "#e9ecf3"; g.fillText(n.label, lx, ly);
    });
    g.textAlign = "center"; g.textBaseline = "alphabetic";
    // Above the web: where it is from, the point's name, what it is and how many threads.
    g.font = `600 22px ${SANS}`; g.fillStyle = "#e2bd5c";
    g.fillText("THE WEB OF SCRIPTURE", cx, 78);
    const t = fit(g, center.label, s => `500 ${s}px ${READ}`, 58, 36, SIZE - 160, 130, 1.1);
    g.font = `500 ${t.size}px ${READ}`; g.fillStyle = "#ffffff";
    let ty = 92 + t.size;
    for (const line of t.lines) { g.fillText(line, cx, ty); ty += t.size * 1.1; }
    const sub = [(center.sub || "").toUpperCase(), caption].filter(Boolean).join("  ·  ");
    if (sub) { g.font = `600 20px ${SANS}`; g.fillStyle = "#a3acbd"; g.fillText(sub, cx, ty + 10); }
    g.textAlign = "left";
    await footer(g, url, true);
    return open(c, { title: `${center.label}: the web of Scripture`, text: `${center.label} and the threads that connect it, on the web of Scripture.`, url, filename: center.label.replace(/[^\w]+/g, "-") + "-connections" });
  }

  /* ---------- A moment in history: the item chosen and what else was happening ---------- */
  // item: {n, when, kind, stream, color, a, z}; kin: [{n, s, color, a, z, event}]; range [a, z].
  async function history({ item, kin, url }) {
    await ready();
    const [c, g] = canvas();
    g.fillStyle = PAPER; g.fillRect(0, 0, SIZE, SIZE);
    g.fillStyle = item.color; g.fillRect(0, 0, SIZE, 14);
    g.textBaseline = "alphabetic";
    g.fillStyle = MUTED; g.font = `600 22px ${SANS}`;
    g.fillText(`${item.kind} · ${item.stream}`.toUpperCase(), 72, 96);
    const t = fit(g, item.n, s => `500 ${s}px ${READ}`, 76, 40, SIZE - 144, 170, 1.12);
    g.fillStyle = INK; g.font = `500 ${t.size}px ${READ}`;
    let y = 100 + t.size;
    for (const line of t.lines) { g.fillText(line, 72, y); y += t.size * 1.12; }
    g.fillStyle = item.color; g.font = `600 34px ${SANS}`;
    g.fillText(item.when, 72, y + 8);
    // A small timeline: the item's span and, below it, what overlapped it.
    const rows = kin.slice(0, 8);
    let a = Math.min(item.a, ...rows.map(r => r.a)), z = Math.max(item.z, ...rows.map(r => r.z));
    const pad = Math.max(5, (z - a) * 0.08); a -= pad; z += pad;
    g.fillStyle = MUTED; g.font = `600 18px ${SANS}`;
    g.fillText("AT THE SAME TIME", 72, y + 64);
    const X0 = 72, X1 = SIZE - 72, top = y + 130;
    const x = v => X0 + ((v - a) / (z - a)) * (X1 - X0);
    const yl = v => (v <= 0 ? `${1 - v} BC` : `AD ${v}`);
    g.strokeStyle = "#e4e2db"; g.lineWidth = 2;
    const step = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000].find(s => (z - a) / s <= 6) || 1000;
    g.font = `500 19px ${SANS}`; g.fillStyle = MUTED; g.textAlign = "center";
    for (let v = Math.ceil(a / step) * step; v <= z; v += step) {
      g.beginPath(); g.moveTo(x(v), top - 12); g.lineTo(x(v), SIZE - 150); g.stroke();
      g.fillText(yl(v === 0 ? 1 : v), x(v), top - 22);
    }
    g.textAlign = "left";
    const bar = (r, yy, h, strong) => {
      g.fillStyle = r.color; g.globalAlpha = strong ? 1 : 0.85;
      if (r.event || r.a === r.z) { g.beginPath(); g.moveTo(x(r.a), yy); g.lineTo(x(r.a) + h / 2, yy + h / 2); g.lineTo(x(r.a), yy + h); g.lineTo(x(r.a) - h / 2, yy + h / 2); g.fill(); }
      else { g.beginPath(); g.roundRect(x(r.a), yy, Math.max(8, x(r.z) - x(r.a)), h, h / 3); g.fill(); }
      g.globalAlpha = 1;
    };
    bar({ ...item, event: item.a === item.z }, top, 40, true);
    const room = SIZE - 170 - (top + 64);
    const rh = Math.min(64, room / Math.max(1, rows.length));
    rows.forEach((r, k) => {
      const yy = top + 64 + k * rh;
      bar(r, yy + 4, Math.min(22, rh - 30), false);
      g.fillStyle = INK; g.font = `600 22px ${SANS}`;
      const lx = Math.min(Math.max(x(r.a), X0), X1 - 360);
      g.fillText(r.n, lx, yy + rh - 8);
      g.fillStyle = MUTED; g.font = `500 18px ${SANS}`;
      g.fillText(r.s, lx + g.measureText(r.n).width * (22 / 18) + 14, yy + rh - 8);
    });
    await footer(g, url, false);
    return open(c, { title: `${item.n}: streams of time`, text: `${item.n} (${item.when}), and what else was happening at the time.`, url, filename: item.n.replace(/[^\w]+/g, "-") + "-timeline" });
  }

  /* ---------- The world in a year: each part of the world, and what it was doing ---------- */
  // groups: [{name, color, items: [names]}]
  async function moment({ year, age, groups, url }) {
    await ready();
    const [c, g] = canvas();
    g.fillStyle = PAPER; g.fillRect(0, 0, SIZE, SIZE);
    g.textBaseline = "alphabetic";
    g.fillStyle = GOLD; g.font = `600 24px ${SANS}`;
    g.fillText("THE WORLD IN", 72, 108);
    g.fillStyle = INK; g.font = `400 120px ${READ}`;
    g.fillText(year, 66, 222);
    g.fillStyle = MUTED; g.font = `600 24px ${SANS}`;
    g.fillText(age.toUpperCase(), 72, 266);
    const gs = groups.slice(0, 7);
    const top = 320, room = SIZE - 170 - top, rh = Math.min(118, room / Math.max(1, gs.length));
    gs.forEach((grp, k) => {
      const y = top + k * rh;
      g.fillStyle = grp.color; g.beginPath(); g.roundRect(72, y + 6, 10, rh - 18, 5); g.fill();
      g.fillStyle = grp.color; g.font = `700 19px ${SANS}`;
      g.fillText(grp.name.toUpperCase(), 100, y + 26);
      const t = fit(g, grp.items.join(" · "), s => `500 ${s}px ${READ}`, 30, 20, SIZE - 172, rh - 40, 1.2);
      g.fillStyle = INK; g.font = `500 ${t.size}px ${READ}`;
      t.lines.forEach((line, j) => g.fillText(line, 100, y + 26 + 10 + t.size * (j + 1) * 1.15));
    });
    await footer(g, url, false);
    return open(c, { title: `The world in ${year}`, text: `The world in ${year}: ${age}.`, url, filename: "the-world-in-" + year.replace(/\s+/g, "-") });
  }

  /* ---------- A view of the web in 3D, as the reader sees it ---------- */
  // image: a canvas of the view; the chosen point's kicker, title and line beneath, its color
  // and icon. The view is cropped to fill the space under the title, centred on the point.
  async function snapshot({ image, kicker, title, sub, color, icon: mark, url }) {
    await ready();
    const [c, g] = canvas();
    g.fillStyle = "#05070d"; g.fillRect(0, 0, SIZE, SIZE);
    const top = 250, bottom = SIZE - 150, bw = SIZE, bh = bottom - top;
    const k = Math.max(bw / image.width, bh / image.height);
    const sw = bw / k, sh = bh / k;
    g.save(); g.beginPath(); g.rect(0, top, bw, bh); g.clip();
    g.drawImage(image, (image.width - sw) / 2, (image.height - sh) / 2, sw, sh, 0, top, bw, bh);
    g.restore();
    // Soft edges, so the view melts into the card.
    for (const [y0, y1, a, b] of [[top, top + 70, 1, 0], [bottom - 70, bottom, 0, 1]]) {
      const fade = g.createLinearGradient(0, y0, 0, y1);
      fade.addColorStop(0, `rgba(5,7,13,${a})`); fade.addColorStop(1, `rgba(5,7,13,${b})`);
      g.fillStyle = fade; g.fillRect(0, y0, SIZE, y1 - y0);
    }
    g.textBaseline = "alphabetic";
    g.fillStyle = color; g.beginPath(); g.arc(94, 100, 22, 0, 2 * Math.PI); g.fill();
    drawIcon(g, mark, 94, 100, 28, "#0b1020", 2.4);
    g.fillStyle = color; g.font = `700 24px ${SANS}`;
    g.fillText(kicker.toUpperCase(), 132, 109);
    const t = fit(g, title, s => `400 ${s}px ${READ}`, 76, 44, SIZE - 144, 92, 1.1);
    g.fillStyle = "#ffffff"; g.font = `400 ${t.size}px ${READ}`;
    g.fillText(t.lines[0], 70, 140 + t.size * 0.9);
    if (sub) {
      g.fillStyle = "#a3acbd"; g.font = `500 26px ${SANS}`;
      g.fillText(wrap(g, sub, SIZE - 144)[0], 72, 140 + t.size * 0.9 + 46);
    }
    await footer(g, url, true);
    return open(c, { title: `${title} in the web of Scripture`, text: `${title}, in the web of Scripture.`, url, filename: title.replace(/[^\w]+/g, "-") + "-web-3d" });
  }

  /* ---------- Sharing the picture ---------- */
  const STYLE = `
    .share-scrim { position: fixed; inset: 0; z-index: 50; background: rgb(10 14 24 / 55%); display: grid; place-items: center; padding: 16px; }
    .share-box { background: var(--surface, #fff); color: var(--ink, #161b26); border-radius: 16px; padding: 16px; width: min(440px, 100%); max-height: 100%; overflow: auto; box-shadow: 0 12px 40px rgb(0 0 0 / 35%); display: grid; gap: 12px; font: 400 15px/1.4 ${SANS}; }
    .share-box img { width: 100%; height: auto; border-radius: 10px; display: block; border: 1px solid var(--line, #e4e2db); }
    .share-box h2 { margin: 0; font: 500 21px/1.2 ${READ}; }
    .share-box .row { display: flex; flex-wrap: wrap; gap: 8px; }
    .share-box button { border: 1px solid var(--line, #e4e2db); background: var(--surface, #fff); color: inherit; border-radius: 10px; padding: 9px 14px; font: 600 14px/1.2 ${SANS}; cursor: pointer; }
    .share-box button.solid { background: var(--lapis, #2646a1); border-color: var(--lapis, #2646a1); color: var(--surface, #fff); }
    .share-box .url { font: 500 13px/1.3 ${SANS}; color: var(--muted, #5b6475); word-break: break-all; }`;
  function dialog(c, blob, { title, url, filename }) {
    if (!document.getElementById("share-style")) {
      const st = document.createElement("style"); st.id = "share-style"; st.textContent = STYLE; document.head.append(st);
    }
    const src = URL.createObjectURL(blob);
    const scrim = document.createElement("div");
    scrim.className = "share-scrim";
    scrim.innerHTML = `<div class="share-box" role="dialog" aria-modal="true" aria-label="Share">
      <h2></h2><img alt=""><p class="url"></p>
      <div class="row"><button class="solid" data-a="save">Save image</button><button data-a="copy">Copy link</button><button data-a="close">Close</button></div></div>`;
    scrim.querySelector("h2").textContent = "Share";
    scrim.querySelector("img").src = src;
    scrim.querySelector("img").alt = title;
    scrim.querySelector(".url").textContent = url;
    const close = () => { scrim.remove(); URL.revokeObjectURL(src); removeEventListener("keydown", esc); };
    const esc = e => { if (e.key === "Escape") close(); };
    addEventListener("keydown", esc);
    scrim.addEventListener("click", async e => {
      const a = e.target.dataset.a;
      if (e.target === scrim || a === "close") close();
      else if (a === "save") { const l = document.createElement("a"); l.href = src; l.download = filename + ".png"; l.click(); }
      else if (a === "copy") {
        try { await navigator.clipboard.writeText(url); e.target.textContent = "Link copied"; }
        catch (err) { e.target.textContent = "Copy failed"; }
      }
    });
    document.body.append(scrim);
    scrim.querySelector("[data-a=save]").focus();
  }
  async function open(c, info) {
    const blob = await new Promise(res => c.toBlob(res, "image/png"));
    const file = new File([blob], info.filename + ".png", { type: "image/png" });
    // Phones and tablets: the system share sheet, with the picture and the link.
    if (matchMedia("(pointer: coarse)").matches && navigator.canShare && navigator.canShare({ files: [file] })) {
      try { await navigator.share({ files: [file], title: info.title, text: `${info.text} ${info.url}`, url: info.url }); return; }
      catch (e) { if (e.name === "AbortError") return; }
    }
    dialog(c, blob, info);
  }

  window.Share = { verse, web, history, moment, snapshot, sketch, here, icons: ICONS, drawIcon };
})();
