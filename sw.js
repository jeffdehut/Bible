// Offline support for the reader: the app itself is cached when installed, and each book,
// lexicon page and font is cached the first time it is read, then served from the cache
// while a fresh copy is fetched in the background.
const VERSION = "reader-8";
const SHELL = ["./", "index.html", "config.js", "account.js", "manifest.webmanifest", "icons/icon.svg", "icons/icon-192.png", "data/bible/books.json"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(VERSION).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const ours = url.origin === location.origin;
  const fonts = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!ours && !fonts) return;
  event.respondWith(caches.open(VERSION).then(async cache => {
    const hit = await cache.match(req);
    const fresh = fetch(req).then(res => {
      if (res.ok) cache.put(req, res.clone());
      return res;
    }).catch(() => hit);
    return hit || fresh;
  }));
});
