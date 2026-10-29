# Deploying the website

The website is the repository itself. `index.html`, the reader, is at the root, and everything
it links to sits beside it:

```
index.html               the reader (home page)
config.js, account.js    site settings, and the optional accounts (off until set up)
privacy.html             what the site keeps about its readers
genealogy.html           The Generations
history.html             Streams of Time
graph.html               The Web of Scripture
maps/index.html          the Bible maps, and the eight sheets beside it
maps/data/               the maps' data
data/bible/              the reader's books, word data, lexicon, search index, places and people
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

## Accounts

Accounts let readers sign in, with a code sent by email, to keep their highlights and notes the
same on every device. They are optional for readers and off until you turn them on: with
`config.js` left empty, the reader shows no sign-in at all. They use
[Supabase](https://supabase.com) for the database and the sign-in emails; the free plan suits
a test site (it pauses a project left unused for a week), and Supabase's pricing page gives the
cost of a live one.

1. **Create a project** at [supabase.com](https://supabase.com/dashboard). Choose a region near
   most readers, and keep the database password somewhere safe.
2. **Create the table.** In the project's **SQL Editor**, paste all of `supabase/schema.sql` and
   run it. It creates one table, `annotations`, with rules that let each person read and write
   only their own rows, and two functions: `push_annotations`, which keeps whichever version of
   a verse's highlight and note is newer, and `delete_account`.
3. **Sign-in emails.** Under **Authentication → Sign In / Providers**, leave **Email** on. Under
   **Authentication → Emails**, edit both the **Confirm signup** and **Magic Link** templates so
   they include the code, for example:

   ```html
   <h2>Your Plain English Bible sign-in code</h2>
   <p>Enter this code in the reader: <strong>{{ .Token }}</strong></p>
   <p>Or open this link on the device you are signing in on: <a href="{{ .ConfirmationURL }}">sign in</a>.</p>
   ```

   Supabase's own mail service sends only a few emails an hour and is meant for testing. Before
   going live, set up a mail service under **Authentication → Emails → SMTP Settings** (Resend,
   Postmark, Amazon SES and others work), sending from an address on your domain.
4. **Addresses.** Under **Authentication → URL Configuration**, set the **Site URL** to the
   site's address (for example `https://your-site.netlify.app/`), and add the same address
   to **Redirect URLs**. Sign-in links bring readers back there.
5. **Turn them on.** Under **Project Settings → API Keys**, copy the project URL and the
   publishable key (or the legacy anon key) into `config.js`, and put a contact address for
   privacy questions in `contact`. Commit and push. Both values are public by design: the
   table's rules keep each person's notes to themselves. Never put the secret (service role)
   key in the site.
6. **Try it.** Sign in on two browsers, add a highlight in one and choose **Sync now** in the
   other.

What readers see: **Sync across devices** in the reader's menu. Signing in adds what the device
has saved to the account and brings in what the account holds, verse by verse, the newest
change winning; after that each change is sent a few seconds after it is made. Signing out
leaves the notes on the device. **Delete my account** removes the account and everything in it
at once. `privacy.html` says all this for readers; read it over before going live.

## Going live

1. Add the domain under **Domain management**. Netlify provides HTTPS automatically.
2. Remove the `X-Robots-Tag` header from `netlify.toml` and delete `robots.txt`, or replace it
   with one that allows crawling.
3. Consider rebuilding the reader data once more and bumping `VERSION` in `sw.js`.
4. If accounts are on, set up a mail service for the sign-in emails (step 3 under *Accounts*)
   and update the Site URL in Supabase to the new domain.

The same folder deploys unchanged to Cloudflare Pages or GitHub Pages: set the output
directory to the repository root and leave the build command empty.
