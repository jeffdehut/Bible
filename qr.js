// QR codes, made here (ISO/IEC 18004, Model 2): text in byte mode (UTF-8), error correction M
// (or L when the text is long), versions 1 to 25, with the mask that scores best by the
// standard's penalty rules. QR.make(text) gives { size, dark(x, y) }, or null if the text is too
// long; QR.draw(ctx, code, x, y, px) paints it, with its quiet zone, onto a canvas.
(() => {
  /* ---------- Error correction: Reed–Solomon over GF(256), polynomial 0x11D ---------- */
  const EXP = new Uint8Array(512), LOG = new Uint8Array(256);
  for (let i = 0, x = 1; i < 255; i++) { EXP[i] = x; LOG[x] = i; x <<= 1; if (x & 0x100) x ^= 0x11d; }
  for (let i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
  const mul = (a, b) => (a && b ? EXP[LOG[a] + LOG[b]] : 0);
  function generator(n) {
    let g = [1];
    for (let i = 0; i < n; i++) {
      const next = new Array(g.length + 1).fill(0);
      for (let j = 0; j < g.length; j++) { next[j] ^= g[j]; next[j + 1] ^= mul(g[j], EXP[i]); }
      g = next;
    }
    return g;
  }
  function ecc(data, n) {
    const g = generator(n), r = new Array(n).fill(0);
    for (const d of data) {
      const f = d ^ r.shift(); r.push(0);
      for (let j = 0; j < n; j++) r[j] ^= mul(g[j + 1], f);
    }
    return r;
  }

  /* ---------- Capacity: per version, [EC codewords per block, blocks, data codewords, blocks, data codewords] ---------- */
  const BLOCKS = {
    L: [null, [7, 1, 19], [10, 1, 34], [15, 1, 55], [20, 1, 80], [26, 1, 108], [18, 2, 68], [20, 2, 78], [24, 2, 97], [30, 2, 116], [18, 2, 68, 2, 69],
      [20, 4, 81], [24, 2, 92, 2, 93], [26, 4, 107], [30, 3, 115, 1, 116], [22, 5, 87, 1, 88], [24, 5, 98, 1, 99], [28, 1, 107, 5, 108], [30, 5, 120, 1, 121],
      [28, 3, 113, 4, 114], [28, 3, 107, 5, 108], [28, 4, 116, 4, 117], [28, 2, 111, 7, 112], [30, 4, 121, 5, 122], [30, 6, 117, 4, 118], [26, 8, 106, 4, 107]],
    M: [null, [10, 1, 16], [16, 1, 28], [26, 1, 44], [18, 2, 32], [24, 2, 43], [16, 4, 27], [18, 4, 31], [22, 2, 38, 2, 39], [22, 3, 36, 2, 37], [26, 4, 43, 1, 44],
      [30, 1, 50, 4, 51], [22, 6, 36, 2, 37], [22, 8, 37, 1, 38], [24, 4, 40, 5, 41], [24, 5, 41, 5, 42], [28, 7, 45, 3, 46], [28, 10, 46, 1, 47], [26, 9, 43, 4, 44],
      [26, 3, 44, 11, 45], [26, 3, 41, 13, 42], [26, 17, 42], [28, 17, 46], [28, 4, 47, 14, 48], [28, 6, 45, 14, 46], [28, 8, 47, 13, 48]],
  };
  const FORMAT = { L: 1, M: 0 };
  const ALIGN = [null, [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50], [6, 30, 54], [6, 32, 58], [6, 34, 62],
    [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74], [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90], [6, 28, 50, 72, 94], [6, 26, 50, 74, 98],
    [6, 30, 54, 78, 102], [6, 28, 54, 80, 106], [6, 32, 58, 84, 110]];
  const dataBytes = (ver, lvl) => { const b = BLOCKS[lvl][ver]; return b[1] * b[2] + (b[3] || 0) * (b[4] || 0); };
  const countBits = ver => (ver < 10 ? 8 : 16);

  /* ---------- The modules ---------- */
  function build(bytes, ver, lvl) {
    const size = ver * 4 + 17;
    const mod = Array.from({ length: size }, () => new Array(size).fill(false));
    const fn = Array.from({ length: size }, () => new Array(size).fill(false));
    const set = (x, y, d) => { mod[y][x] = d; fn[y][x] = true; };
    for (let i = 0; i < size; i++) { set(6, i, i % 2 === 0); set(i, 6, i % 2 === 0); }
    const finder = (cx, cy) => {
      for (let dy = -4; dy <= 4; dy++) for (let dx = -4; dx <= 4; dx++) {
        const x = cx + dx, y = cy + dy;
        if (x < 0 || y < 0 || x >= size || y >= size) continue;
        const d = Math.max(Math.abs(dx), Math.abs(dy));
        set(x, y, d !== 2 && d !== 4);
      }
    };
    finder(3, 3); finder(size - 4, 3); finder(3, size - 4);
    const al = ALIGN[ver], last = al.length - 1;
    for (let i = 0; i <= last; i++) for (let j = 0; j <= last; j++) {
      if ((i === 0 && j === 0) || (i === 0 && j === last) || (i === last && j === 0)) continue;
      for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) set(al[i] + dx, al[j] + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1);
    }
    const format = mask => {
      const data = (FORMAT[lvl] << 3) | mask;
      let rem = data;
      for (let i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
      const bits = ((data << 10) | rem) ^ 0x5412, bit = i => ((bits >>> i) & 1) === 1;
      for (let i = 0; i <= 5; i++) set(8, i, bit(i));
      set(8, 7, bit(6)); set(8, 8, bit(7)); set(7, 8, bit(8));
      for (let i = 9; i < 15; i++) set(14 - i, 8, bit(i));
      for (let i = 0; i < 8; i++) set(size - 1 - i, 8, bit(i));
      for (let i = 8; i < 15; i++) set(8, size - 15 + i, bit(i));
      set(8, size - 8, true);
    };
    format(0);
    if (ver >= 7) {
      let rem = ver;
      for (let i = 0; i < 12; i++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1f25);
      const bits = (ver << 12) | rem;
      for (let i = 0; i < 18; i++) {
        const d = ((bits >>> i) & 1) === 1, a = size - 11 + (i % 3), b = Math.floor(i / 3);
        set(a, b, d); set(b, a, d);
      }
    }
    // The codewords: data, then error correction, each interleaved across the blocks.
    const spec = BLOCKS[lvl][ver], n = spec[0], blocks = [];
    let k = 0;
    for (const [count, len] of [[spec[1], spec[2]], [spec[3] || 0, spec[4] || 0]]) for (let b = 0; b < count; b++) { const d = bytes.slice(k, k + len); k += len; blocks.push({ d, e: ecc(d, n) }); }
    const words = [], maxD = Math.max(...blocks.map(b => b.d.length));
    for (let i = 0; i < maxD; i++) for (const b of blocks) if (i < b.d.length) words.push(b.d[i]);
    for (let i = 0; i < n; i++) for (const b of blocks) words.push(b.e[i]);
    let i = 0;
    for (let right = size - 1; right >= 1; right -= 2) {
      if (right === 6) right = 5;
      for (let v = 0; v < size; v++) for (let j = 0; j < 2; j++) {
        const x = right - j, y = ((right + 1) & 2) === 0 ? size - 1 - v : v;
        if (!fn[y][x] && i < words.length * 8) { mod[y][x] = ((words[i >>> 3] >>> (7 - (i & 7))) & 1) === 1; i++; }
      }
    }
    // The mask that leaves the fewest confusing patterns.
    const MASKS = [(x, y) => (x + y) % 2 === 0, (x, y) => y % 2 === 0, x => x % 3 === 0, (x, y) => (x + y) % 3 === 0, (x, y) => (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0,
      (x, y) => ((x * y) % 2) + ((x * y) % 3) === 0, (x, y) => (((x * y) % 2) + ((x * y) % 3)) % 2 === 0, (x, y) => (((x + y) % 2) + ((x * y) % 3)) % 2 === 0];
    const apply = m => { for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) if (!fn[y][x] && MASKS[m](x, y)) mod[y][x] = !mod[y][x]; };
    let best = 0, bestScore = Infinity;
    for (let m = 0; m < 8; m++) {
      apply(m); format(m);
      const s = penalty(mod, size);
      if (s < bestScore) { bestScore = s; best = m; }
      apply(m);
    }
    apply(best); format(best);
    return { size, dark: (x, y) => mod[y][x], version: ver, level: lvl };
  }
  function penalty(m, size) {
    let s = 0;
    for (let pass = 0; pass < 2; pass++) for (let a = 0; a < size; a++) {
      let run = 1, line = "";
      for (let b = 0; b < size; b++) {
        const v = pass ? m[b][a] : m[a][b];
        line += v ? "1" : "0";
        if (b && v === (pass ? m[b - 1][a] : m[a][b - 1])) { run++; if (run === 5) s += 3; else if (run > 5) s++; } else run = 1;
      }
      for (const pat of ["10111010000", "00001011101"]) for (let p = line.indexOf(pat); p >= 0; p = line.indexOf(pat, p + 1)) s += 40;
    }
    let dark = 0;
    for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
      if (m[y][x]) dark++;
      if (x < size - 1 && y < size - 1) { const c = m[y][x]; if (c === m[y][x + 1] && c === m[y + 1][x] && c === m[y + 1][x + 1]) s += 3; }
    }
    s += Math.floor(Math.abs((dark * 20) / (size * size) - 10)) * 10;
    return s;
  }

  function make(text) {
    const utf8 = Array.from(new TextEncoder().encode(text));
    for (const lvl of ["M", "L"]) for (let ver = 1; ver <= 25; ver++) {
      const cap = dataBytes(ver, lvl), bits = [];
      const push = (v, n) => { for (let i = n - 1; i >= 0; i--) bits.push((v >>> i) & 1); };
      if (4 + countBits(ver) + utf8.length * 8 > cap * 8) continue;
      push(4, 4); push(utf8.length, countBits(ver));
      for (const b of utf8) push(b, 8);
      push(0, Math.min(4, cap * 8 - bits.length));
      while (bits.length % 8) bits.push(0);
      const bytes = [];
      for (let i = 0; i < bits.length; i += 8) bytes.push(bits.slice(i, i + 8).reduce((a, b) => (a << 1) | b, 0));
      for (let pad = 0xec; bytes.length < cap; pad ^= 0xec ^ 0x11) bytes.push(pad);
      return build(bytes, ver, lvl);
    }
    return null;
  }
  // Painted with a quiet zone of four modules round it, in black on white.
  function draw(g, code, x, y, px) {
    const q = 4, n = code.size + 2 * q;
    g.fillStyle = "#fff"; g.fillRect(x, y, n * px, n * px);
    g.fillStyle = "#000";
    for (let r = 0; r < code.size; r++) for (let c = 0; c < code.size; c++) if (code.dark(c, r)) g.fillRect(x + (c + q) * px, y + (r + q) * px, px, px);
    return n * px;
  }
  window.QR = { make, draw };
})();
