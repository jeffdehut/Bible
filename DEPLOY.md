# Deploying the website

The website is the repository itself. `index.html`, the reader, is at the root, and everything
it links to sits beside it:

```
index.html               the reader (home page)
genealogy.html           The Generations
history.html             Streams of Time
maps/index.html          the Bible maps, and the eight sheets beside it
maps/data/               the maps' data
data/bible/              the reader's books, word data, lexicon, search index and places
icons/, manifest.webmanifest, sw.js   the app icon, install details and offline support
404.html, robots.txt     the not-found page, and the test site's instructions to crawlers
```

Everything is already built and committed, so any static host can serve the folder as it is.
There is no build step and no server code. Every page links back to the reader, and the
reader's menu links to every page.

## A test site on Netlify

`netlify.toml` holds the settings: publish the repository root, no build. It also marks every
page `noindex` and ships a `robots.txt` that turns crawlers away, so the drafts stay out of
search engines while the site is a test.

### From GitHub (recommended)

Netlify then redeploys on every push.

1. Sign in at [app.netlify.com](https://app.netlify.com) and choose **Add new site → Import an
   existing project → GitHub**.
2. Allow Netlify to read the `jeffdehut/Bible` repository, then pick it.
3. Choose the branch to publish: `main` once this work is merged, or
   `claude/ecstatic-faraday-0wu2gv` to test it now. Leave the build command and publish
   directory as Netlify fills them in from `netlify.toml` (publish directory: the root, `.`).
4. Choose **Deploy**. The site appears at a `*.netlify.app` address within a few minutes. The
   first deploy uploads the whole repository, about 110 MB; later deploys send only what
   changed.
5. Optional: under **Site configuration → Build & deploy → Branches and deploy contexts**, turn
   on deploy previews. Each pull request then gets its own test address.

If you created the site before this layout, open **Site configuration → Build & deploy →
Build settings** and clear the publish directory (or set it to `.`), so `netlify.toml` decides.

### Without GitHub

From the repository folder, with Node.js installed:

```
npx netlify-cli deploy --dir=.            # a draft address to try
npx netlify-cli deploy --dir=. --prod     # the site's main address
```

The first run asks you to sign in and to create or pick a site. Dragging the repository folder
onto [app.netlify.com/drop](https://app.netlify.com/drop) also works.

## Trying it on your own computer

The reader loads its books as separate files, so it needs a web server rather than a double
click. From the repository folder:

```
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Updating the content

After changing the translation or the data, rebuild what changed and commit it:

```
python3 scripts/translation.py   # the compiled translation in text/english/
python3 scripts/connections.py   # genealogy.html and history.html
python3 scripts/reader.py        # the reader's data in data/bible/
python3 scripts/maps.py          # the maps in maps/
```

The pages are built from templates in `scripts/templates/`; edit those, not the built pages.
When the service worker or the app shell changes, raise `VERSION` in `sw.js` so installed
copies of the reader pick up the new version.

## Going live

1. Add the domain under **Domain management**. Netlify provides HTTPS automatically.
2. Remove the `X-Robots-Tag` header from `netlify.toml` and delete `robots.txt`, or replace it
   with one that allows crawling.
3. Consider rebuilding the reader data once more and bumping `VERSION` in `sw.js`.

The same folder deploys unchanged to Cloudflare Pages or GitHub Pages: set the output
directory to the repository root and leave the build command empty.
