# Deploying the website

The website is the `site/` folder: the reader (`index.html`) and the pages and maps beside it.
Everything in it is already built and committed, so any static host can serve it as it is.
There is no build step and no server code.

## A test site on Netlify

`netlify.toml` holds the settings: publish `site/`, no build. It also marks every page
`noindex` and ships a `robots.txt` that turns crawlers away, so the drafts stay out of search
engines while the site is a test.

### From GitHub (recommended)

Netlify then redeploys on every push.

1. Sign in at [app.netlify.com](https://app.netlify.com) and choose **Add new site → Import an
   existing project → GitHub**.
2. Allow Netlify to read the `jeffdehut/Bible` repository, then pick it.
3. Choose the branch to publish: `main` once this work is merged, or
   `claude/ecstatic-faraday-0wu2gv` to test it now. Leave the build command and publish
   directory as Netlify fills them in from `netlify.toml`.
4. Choose **Deploy**. The site appears at a `*.netlify.app` address within a minute or two.
5. Optional: under **Site configuration → Build & deploy → Branches and deploy contexts**, turn
   on deploy previews. Each pull request then gets its own test address.

### Without GitHub

From the repository folder, with Node.js installed:

```
npx netlify-cli deploy --dir=site            # a draft address to try
npx netlify-cli deploy --dir=site --prod     # the site's main address
```

The first run asks you to sign in and to create or pick a site.

## Trying it on your own computer

The reader loads its books as separate files, so it needs a web server rather than a double
click:

```
python3 -m http.server 8000 -d site
```

Then open http://localhost:8000.

## Updating the content

After changing the translation or the data, rebuild what changed and commit it:

```
python3 scripts/translation.py   # the compiled translation in text/english/
python3 scripts/connections.py   # site/genealogy.html and site/history.html
python3 scripts/reader.py        # the reader's data in site/data/bible/
python3 scripts/maps.py          # the maps in site/maps/
```

When the service worker or the app shell changes, raise `VERSION` in `site/sw.js` so
installed copies of the reader pick up the new version.

## Going live

1. Add the domain under **Domain management**. Netlify provides HTTPS automatically.
2. Remove the `X-Robots-Tag` header from `netlify.toml` and delete `site/robots.txt`, or
   replace it with one that allows crawling.
3. Consider rebuilding the reader data once more and bumping `VERSION` in `site/sw.js`.

The same `site/` folder deploys unchanged to Cloudflare Pages or GitHub Pages: set the output
directory to `site` and leave the build command empty.
