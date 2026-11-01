// The site's icons, drawn from their SVG markup: the shapes inside an icon's <svg> (paths,
// circles, rectangles, lines, ellipses, polylines), as the icon files in icons/library/ have
// them. The same markup serves the page (as SVG) and every canvas (the web, the 3D web, the
// timeline, shared pictures), so an icon looks the same wherever it is drawn.
//
// The icons are drawn on a 24-unit square (some on 20) in strokes of currentColor, 1.5 units by
// default (1.75 for small controls), with finer inner lines (their own stroke-width) and a faint
// tone inside some shapes (fill="currentColor" with a low fill-opacity).
//
//   IconKit.svg(markup, { size, sw, cls, label, vb })  -> an <svg> string
//   IconKit.el(markup, opts)                           -> an <svg> element
//   IconKit.draw(g, markup, x, y, size, color, sw)     -> draws it on a canvas, centred at (x, y)
(() => {
  const SW = 1.5;
  function svg(markup, { size = null, sw = SW, cls = "", label = "", vb = 24, attrs = "" } = {}) {
    const dim = size ? ` width="${size}" height="${size}"` : "";
    const a11y = label ? ` role="img" aria-label="${label.replace(/"/g, "&quot;")}"` : ` aria-hidden="true"`;
    return `<svg${cls ? ` class="${cls}"` : ""} viewBox="0 0 ${vb} ${vb}"${dim} fill="none" stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round"${a11y}${attrs ? " " + attrs : ""}>${markup}</svg>`;
  }
  function el(markup, opts) { const t = document.createElement("template"); t.innerHTML = svg(markup, opts); return t.content.firstChild; }

  // Canvas: each shape as a Path2D with its own stroke width, fill and opacity.
  const num = (n, k, d = 0) => { const v = parseFloat(n.getAttribute(k)); return Number.isFinite(v) ? v : d; };
  function shapeD(n) {
    switch (n.tagName.toLowerCase()) {
      case "path": return n.getAttribute("d") || "";
      case "circle": { const cx = num(n, "cx"), cy = num(n, "cy"), r = num(n, "r"); return `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0Z`; }
      case "ellipse": { const cx = num(n, "cx"), cy = num(n, "cy"), rx = num(n, "rx"), ry = num(n, "ry"); return `M${cx - rx} ${cy}a${rx} ${ry} 0 1 0 ${2 * rx} 0a${rx} ${ry} 0 1 0 ${-2 * rx} 0Z`; }
      case "line": return `M${num(n, "x1")} ${num(n, "y1")}L${num(n, "x2")} ${num(n, "y2")}`;
      case "rect": {
        const x = num(n, "x"), y = num(n, "y"), w = num(n, "width"), h = num(n, "height");
        let rx = num(n, "rx", NaN), ry = num(n, "ry", NaN);
        if (!Number.isFinite(rx)) rx = Number.isFinite(ry) ? ry : 0;
        if (!Number.isFinite(ry)) ry = rx;
        rx = Math.min(rx, w / 2); ry = Math.min(ry, h / 2);
        if (!rx) return `M${x} ${y}h${w}v${h}h${-w}Z`;
        return `M${x + rx} ${y}h${w - 2 * rx}a${rx} ${ry} 0 0 1 ${rx} ${ry}v${h - 2 * ry}a${rx} ${ry} 0 0 1 ${-rx} ${ry}h${-(w - 2 * rx)}a${rx} ${ry} 0 0 1 ${-rx} ${-ry}v${-(h - 2 * ry)}a${rx} ${ry} 0 0 1 ${rx} ${-ry}Z`;
      }
      case "polyline": case "polygon": {
        const pts = (n.getAttribute("points") || "").trim().split(/[\s,]+/).map(Number);
        let d = "";
        for (let i = 0; i + 1 < pts.length; i += 2) d += (i ? "L" : "M") + pts[i] + " " + pts[i + 1];
        return d + (n.tagName.toLowerCase() === "polygon" ? "Z" : "");
      }
      default: return "";
    }
  }
  const cache = new Map();
  function parts(markup) {
    if (cache.has(markup)) return cache.get(markup);
    const doc = new DOMParser().parseFromString(`<svg xmlns="http://www.w3.org/2000/svg">${markup}</svg>`, "image/svg+xml");
    const out = [];
    const walk = (node, inh) => {
      for (const n of node.children) {
        const tag = n.tagName.toLowerCase();
        const own = { ...inh };
        for (const k of ["stroke", "stroke-width", "fill", "fill-opacity", "opacity", "stroke-opacity"]) if (n.hasAttribute(k)) own[k] = n.getAttribute(k);
        if (tag === "g") { walk(n, own); continue; }
        if (tag === "title" || tag === "desc" || tag === "style") continue;
        const d = shapeD(n);
        if (d) out.push({ p: new Path2D(d), ...own });
      }
    };
    walk(doc.documentElement, {});
    cache.set(markup, out);
    return out;
  }
  // Drawn centred at (x, y), `size` across, in `color`; sw is the icon's base stroke width (in
  // its own units: its finer lines keep their proportion to it).
  function draw(g, markup, x, y, size, color, sw = SW, vb = 24) {
    if (!markup) return;
    const ps = parts(markup);
    g.save();
    g.translate(x - size / 2, y - size / 2); g.scale(size / vb, size / vb);
    g.lineCap = "round"; g.lineJoin = "round"; g.shadowBlur = 0;
    for (const s of ps) {
      const op = parseFloat(s.opacity ?? 1);
      const fill = s.fill && s.fill !== "none" ? (s.fill === "currentColor" ? color : s.fill) : null;
      if (fill) {
        g.globalAlpha = op * parseFloat(s["fill-opacity"] ?? 1);
        g.fillStyle = fill; g.fill(s.p);
      }
      if (s.stroke !== "none") {
        g.globalAlpha = op * parseFloat(s["stroke-opacity"] ?? 1);
        g.strokeStyle = !s.stroke || s.stroke === "currentColor" ? color : s.stroke;
        g.lineWidth = s["stroke-width"] != null ? parseFloat(s["stroke-width"]) * (sw / SW) : sw;
        g.stroke(s.p);
      }
    }
    g.restore();
  }
  window.IconKit = { SW, svg, el, draw, parts };
})();
