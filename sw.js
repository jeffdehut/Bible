// Offline support for the reader: the app itself is cached when installed, and each book,
// lexicon page and font is cached the first time it is read, then served from the cache
// while a fresh copy is fetched in the background. Pages themselves come from the network
// first, so a new version of the site shows on the first visit after it is published; the
// saved copy is used offline, or when the network is slow.
//
// The page registers this file as sw.js?v=N with N the number in VERSION (index.html), so each
// release has a new address that no cache along the way can hold an old copy of: change both.
const VERSION = "reader-43";
const SHELL = ["./", "index.html", "config.js?v=31", "account.js?v=32", "i18n.js?v=3", "nav.js?v=33", "manifest.webmanifest", "icons/icon.svg", "icons/icon-192.png", "data/bible/books.json"];

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
  if (req.mode === "navigate") {
    event.respondWith(page(req));
    return;
  }
  event.respondWith(caches.open(VERSION).then(async cache => {
    const hit = await cache.match(req);
    const fresh = fetch(req).then(res => {
      if (res.ok) cache.put(req, res.clone());
      return res;
    }).catch(() => hit);
    return hit || fresh;
  }));
});

// A page: from the network (asking any cache on the way to check it is current), kept for
// offline; the saved copy if the network fails or takes longer than four seconds.
async function page(req) {
  const cache = await caches.open(VERSION);
  const saved = () => cache.match(req, { ignoreSearch: true }).then(hit => hit || cache.match("index.html"));
  const net = fetch(req.url, { cache: "no-cache", credentials: "same-origin" }).then(res => {
    if (res.ok) cache.put(req, res.clone());
    return res;
  });
  const slow = new Promise(resolve => setTimeout(resolve, 4000)).then(saved);
  try {
    return (await Promise.race([net, slow])) || await net;
  } catch (e) {
    return (await saved()) || Response.error();
  }
}
