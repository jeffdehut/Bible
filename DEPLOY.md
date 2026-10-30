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

## Porkbun Static Hosting

Porkbun hosts the site at `bibledata.org`, beside the domain, its DNS and its email
forwarding. Its **GitHub Connect** publishes the `main` branch of `jeffdehut/Bible`, and each
change to `main` refreshes the site. Other branches are not published: try a change on your own
computer (below), then merge its branch into `main` (on GitHub, open a pull request from the
branch into `main` and choose **Merge**).

To set it up (once): at porkbun.com open **Domain Management**, then the house icon in the
**Website** column beside `bibledata.org`, which opens the Static Hosting page. Under **GitHub
Connect**, connect GitHub, allow Porkbun to read the `jeffdehut/Bible` repository, pick it and
pick the branch `main`. Porkbun serves the files as they are: there is no build step, and
`index.html` is at the root, where Porkbun expects it. Its plan allows files up to 40 MB; the
largest here, `data/bible/search.json`, is under 5 MB. `robots.txt` turns crawlers away while
the site is a test. (`netlify.toml` holds the Netlify settings below; Porkbun ignores it.)

## The bibledata.org domain

`bibledata.org` is registered at Porkbun, and Porkbun keeps its DNS. Its records:

| Name | Type | Value | For |
|---|---|---|---|
| `bibledata.org` | ALIAS | `ss1-sixie.porkbun.com` | Porkbun Static Hosting (set by Porkbun) |
| `*` | CNAME | `ss1-sixie.porkbun.com` | the same, for `www` and other names (set by Porkbun) |
| `ftp` | CNAME | `pixie-ss1-ftp.porkbun.com` | the hosting's FTP access (set by Porkbun) |
| `bibledata.org` | MX, TXT | added by Porkbun's email forwarding | `privacy@bibledata.org` |
| `send` | MX, TXT | as Resend's domain page gives them | sign-in emails sent through Resend |
| `resend._domainkey` | TXT | as Resend's domain page gives it | the same (DKIM) |

`info@bibledata.org` (the reader's **Send feedback** buttons, set as `feedback` in `config.js`)
needs its own forward, made the same way. To show **Support this project** in the reader's
**About this project** page, put the address of a donation page (Ko-fi, GitHub Sponsors, a
PayPal or Stripe payment link) in `support` in `config.js`; left empty, the section stays hidden.

`privacy@bibledata.org` forwards, through Porkbun (**Domain Management → Email → Email
Forwarding**), to the owner's inbox. Supabase sends its sign-in emails through Resend (see
step 3 under *Accounts*), from `signin@bibledata.org`.

## Netlify (being retired)

The site was first tested on Netlify (`biblemadeplain.netlify.app`), set up by `netlify.toml`,
which publishes `main` too. Each Netlify publish uses 15 of its free plan's 300 monthly credits,
so stop its builds (**Project configuration → Build & deploy → Continuous deployment → Stop
builds**) before the next merge into `main`, and delete the project once Porkbun is serving the
site.

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
python3 scripts/connections.py   # the notes in connections/, and the genealogy, timeline and web pages
python3 scripts/reader.py        # the reader's data in data/bible/
python3 scripts/maps.py          # the maps in maps/
node scripts/map-previews.js     # pictures of the maps for their cards (then: python3 scripts/maps.py index)
python3 scripts/study.py         # the topics and dictionary in data/bible/study/
python3 scripts/parallels.py     # parallel passages and reading plans (after study.py)
python3 scripts/lexicons.py      # the full lexicon entries (BDB, LSJ) in data/bible/lexicon/
python3 scripts/markings.py      # the study markings in data/bible/markings/ (after reader.py)
```

Then push the branch, and merging it into `main` puts it live. The pages are built from templates in `scripts/templates/`; edit those, not the built pages.
When the service worker or the app shell changes, raise `VERSION` in `sw.js` so installed
copies of the reader pick up the new version, and raise the `?v=` number after `sw.js`, `config.js`
and `account.js` in `index.html` (and `config.js` in `scripts/templates/privacy.html`) to match:
Porkbun's servers keep JavaScript files for 30 days, so a changed script needs a new address.

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
3. **Sign-in emails.** Under **Authentication → Sign In / Providers**, leave **Email** on.
   Supabase's own emails carry only a link, which signs the reader in on the device where it is
   opened; that works once step 4 is done. To add a code, which suits the installed app better,
   edit both the **Confirm signup** and **Magic Link** templates under **Authentication →
   Emails**. A new free project can edit them only after a mail service is set up (below). For
   example:

   ```html
   <h2>Your Plain English Bible sign-in code</h2>
   <p>Enter this code in the reader: <strong>{{ .Token }}</strong></p>
   <p>Or open this link on the device you are signing in on: <a href="{{ .ConfirmationURL }}">sign in</a>.</p>
   ```

   Supabase's own mail service sends only a few emails an hour, and only to the members of your
   Supabase team, so it suits testing alone. Before anyone else can sign in, set up a mail service
   under **Authentication → Emails → SMTP Settings**, sending from an address on a domain you own.
   Resend's free plan (3,000 emails a month, 100 a day) is enough for a small site; Brevo,
   Postmark and Amazon SES also work.
4. **Addresses.** Under **Authentication → URL Configuration**, set the **Site URL** to the
   site's address (`https://bibledata.org/`), and add the same address
   to **Redirect URLs**. Sign-in links bring readers back there. (A link that opens
   `localhost:3000` means the Site URL is still Supabase's default. An email with a link but
   no code means that template, **Confirm signup** for a new reader, hasn't been edited.)
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

1. Check that `https://bibledata.org` serves the site with a valid certificate (Porkbun
   provides it).
2. Delete `robots.txt`, or replace it with one that allows crawling.
3. Consider rebuilding the reader data once more and bumping `VERSION` in `sw.js`.
4. If accounts are on, check that the sign-in emails come from `bibledata.org` (step 3 under
   *Accounts*) and that Supabase's Site URL is `https://bibledata.org/`.

The same folder deploys unchanged to Netlify, Cloudflare Pages or GitHub Pages: set the output
directory to the repository root and leave the build command empty.
