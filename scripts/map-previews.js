// Small preview pictures of the Bible maps, for the cards in maps/index.html.
//
//     node scripts/map-previews.js            (after scripts/maps.py; needs Playwright)
//     python3 scripts/maps.py index           then rebuild the index with the pictures
//
// Opens each built sheet, maps/NAME.html, in a headless browser with its controls hidden,
// photographs the whole sheet and writes maps/previews/NAME.png; scripts/maps.py turns each
// into a small JPEG beside it (maps/previews/NAME.jpg) and shows it on the sheet's card.
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), http = require("http");
const ROOT = path.join(__dirname, "..");
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png" };
const server = http.createServer((req, res) => {
  const file = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(0, r));
  const port = server.address().port;
  const names = fs.readdirSync(path.join(ROOT, "maps", "data")).filter(f => f.endsWith(".json")).map(f => f.slice(0, -5));
  const only = process.argv.slice(2);
  const browser = await chromium.launch();
  for (const name of names.filter(n => !only.length || only.includes(n))) {
    // A window the shape of the sheet, so the whole sheet fits it.
    const sheet = JSON.parse(fs.readFileSync(path.join(ROOT, "maps", "data", name + ".json"), "utf8")).sheet;
    const ratio = (sheet.height || sheet.h) / (sheet.width || sheet.w) || 1.33;
    const page = await browser.newPage({ viewport: { width: 1000, height: Math.round(1000 * ratio) + 40 }, deviceScaleFactor: 1, colorScheme: "light" });
    await page.goto(`http://localhost:${port}/maps/${name}.html`);
    await page.waitForTimeout(2500);
    // The sheet alone: no buttons, panels or title over it.
    await page.addStyleTag({ content: ".bar, .ui, nav, .zoom, .panel, .toast { display: none !important; }" });
    await page.click("#zfit", { force: true }).catch(() => {});
    await page.waitForTimeout(900);
    const box = await page.evaluate(() => {
      const svg = document.getElementById("map");
      const g = svg.querySelector("g");
      const r = (g || svg).getBoundingClientRect();
      return { x: Math.max(0, r.left), y: Math.max(0, r.top), width: Math.min(r.width, innerWidth), height: Math.min(r.height, innerHeight) };
    });
    await page.screenshot({ path: path.join(ROOT, "maps", "previews", name + ".png"), clip: box });
    console.log(name, Math.round(box.width), "x", Math.round(box.height));
    await page.close();
  }
  await browser.close();
  server.close();
})();
