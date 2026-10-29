# Publishing riselabs.at on GitHub Pages

What this covers: getting the site online the first time, pointing
riselabs.at at it, and what happens on every later change. Nothing here needs
a developer, but it does need someone with admin access to the GitHub account
and to the DNS records at the domain registrar.

---

## 1. What this site is, in one paragraph

It is a **Jekyll** site. Jekyll takes plain text files - Markdown for content,
YAML for structured data - and builds them into an ordinary website. GitHub
Pages runs Jekyll for free on every push, so there is no server to maintain
and no database to back up. The whole site, content included, is the files in
this repository. If you can edit a text file, you can edit the site.

There is nothing to install to make a change. Edits can be made in the browser
on github.com.

---

## 2. First-time setup

### 2.1 Create the repository

1. Sign in to GitHub as the account that should own the site. An organisation
   account is better than a personal one: people leave, organisations don't.
2. **New repository**. Name it `riselabs.at` (any name works; this one is
   self-explanatory).
3. **Public** or **Private** both work. Private repositories need a paid plan
   for Pages. Public is fine - everything here is published anyway.
4. Do **not** add a README, .gitignore or licence. The repository must start
   empty.

### 2.2 Upload the site

Easiest route, no command line:

1. Unzip `rise-site.zip` on your computer.
2. On the empty repository page, click **uploading an existing file**.
3. Open the unzipped folder and drag **everything inside it** into the
   browser - the files, not the folder itself. The root of the repository must
   contain `_config.yml`, `index.md` and the `_projects`, `_people` and other
   folders directly.
4. Scroll down, write a commit message such as "Initial site", and
   **Commit changes**.

Two things to check after uploading, because both are easy to lose:

- **`.gitignore` and `CNAME`.** Files starting with a dot are hidden in macOS
  Finder (press `Cmd + Shift + .` to show them) and are sometimes skipped by
  drag-and-drop. Confirm both are listed in the repository.
- **Folder structure.** If the repository shows a single folder named
  `rise-site`, you dragged the folder rather than its contents. Delete and
  redo, or the build will produce nothing.

### 2.3 Turn Pages on

1. Repository → **Settings** → **Pages**.
2. **Source**: *Deploy from a branch*.
3. **Branch**: `main`, folder `/ (root)`. **Save**.

GitHub starts a build. Watch it under the **Actions** tab: a yellow dot means
building, green tick means published, red cross means the build failed (see
§5). The first build takes a minute or two.

The site is now live at `https://<account>.github.io/<repository>/`. Open it
and check it works before touching DNS.

---

## 3. Pointing riselabs.at at it

This has two halves that must both be done. They can be done in either order,
but the GitHub side will show an error until DNS has propagated, which is
normal.

### 3.1 At the domain registrar

In the DNS settings for `riselabs.at`, create these records:

| Type  | Name / Host | Value                     |
|-------|-------------|---------------------------|
| A     | `@`         | `185.199.108.153`         |
| A     | `@`         | `185.199.109.153`         |
| A     | `@`         | `185.199.110.153`         |
| A     | `@`         | `185.199.111.153`         |
| CNAME | `www`       | `<account>.github.io.`    |

All four A records are needed - they are GitHub's four servers, and using only
one makes the site fragile. `@` means the bare domain; some registrars want it
left blank instead. The trailing dot on the CNAME value is correct, and some
registrars add it for you.

Delete any existing A, AAAA or CNAME records for `@` and `www` that point
somewhere else, or they will conflict.

DNS changes take anywhere from a few minutes to a few hours to propagate.

### 3.2 At GitHub

1. Settings → **Pages** → **Custom domain**: enter `riselabs.at` and **Save**.
2. GitHub runs a DNS check. If DNS has not propagated yet it will show a
   warning - wait and reload rather than changing anything.
3. Once the check passes, tick **Enforce HTTPS**. The certificate is issued
   automatically and is free. The tickbox stays greyed out until the
   certificate exists, which can take up to an hour.

Saving the custom domain writes a `CNAME` file into the repository. One is
already included, containing `riselabs.at`, so this should be a no-op - but
if GitHub ever appears to "forget" the domain, check that file still exists.
Deleting it unsets the custom domain.

### 3.3 What success looks like

- `https://riselabs.at` loads the site, with a padlock.
- `https://www.riselabs.at` redirects to it.
- `http://riselabs.at` redirects to `https://`.

**Done on 29 October 2026.** All three verified in a browser that evening:
`http://riselabs.at/projects/` redirected to `https://`,
`https://www.riselabs.at/` redirected to `https://riselabs.at/`, and the site
loaded with no certificate warning.

Before that the certificate was missing, so `https://riselabs.at` showed a
privacy error while `http://` worked. Everything the site says about itself
points at `https://` - the canonical tag, `og:url`, the sitemap - so every
shared link and every search result led to the warning. Ticking **Enforce
HTTPS** became possible once GitHub had issued the certificate, which is the
signal that the DNS was right; the checkbox stays greyed out until then.

If this ever recurs, the usual causes in order: a stray A, AAAA or CNAME
record left on the apex from a previous host; a CAA record that does not
permit `letsencrypt.org`; or a custom domain that needs removing and
re-saving in the Pages settings to trigger a fresh certificate request.

---

## 4. Making changes after launch

Every push to `main` rebuilds and republishes the site, usually within a
minute. There is no separate "publish" step and no staging site.

For small edits, use the browser: open the file on github.com, click the
pencil icon, edit, and **Commit changes** at the bottom. Committing straight
to `main` publishes immediately.

For anything larger - a new project with images, several files at once -
commit to a branch and open a pull request instead. Nothing goes live until
the pull request is merged, which gives a second pair of eyes.

**A draft that is not ready to be seen** should carry `published: false` in
its front matter. Jekyll skips those files entirely. That is safer than
leaving a half-finished page live, and safer than keeping it only on your
laptop where nobody else can pick it up.

---

## 5. When the build fails

A red cross under **Actions** means Jekyll could not build the site. The
previous version stays live, so a failed build never takes the site down.

Click the failed run and read the error. In practice it is almost always one
of these:

| Message | Cause | Fix |
|---|---|---|
| `could not find expected ':'` | A colon inside an unquoted value, e.g. `title: Carbon: a study` | Wrap the value in double quotes |
| `found character that cannot start any token` | A tab character in the front matter | Use spaces; YAML forbids tabs |
| `Liquid Exception … Unknown tag` | A typo in `{% ... %}` | Compare with a working file |
| `mapping values are not allowed here` | Missing `---` line, or text before it | The file must begin with `---` on line 1 |
| Build succeeds but a page is blank | Front matter missing entirely | Every content file needs the `---` block |

The single most common cause is a stray colon in a title. When in doubt, put
double quotes around the value.

---

## 6. Access and succession

Worth settling before launch rather than after:

- The repository should be owned by an **organisation account**, with at least
  two people holding admin rights. A site owned by one person's account is a
  problem the day that person is unavailable.
- The **domain registrar** login needs the same treatment. The DNS records are
  the one part of this that GitHub cannot restore.
- Whoever holds the **Buttondown** account controls the newsletter list.
  Export the subscriber list periodically; it is the only asset here that
  cannot be rebuilt from the repository.

---

## 7. Reference

- Repository root must contain: `_config.yml`, `index.md`, `CNAME`
- Build source: branch `main`, folder `/ (root)`
- Plugins in use: `jekyll-seo-tag`, `jekyll-feed`, `jekyll-sitemap` - all three
  are on GitHub Pages' supported list, so they need no extra setup
- Generated automatically once live: `/sitemap.xml`, `/feed.xml`, `/404.html`
- Checked before every upload: `python3 docs-check.py` from the repository
  root - it should print `no problems found`
- Never edit: `_site/` (build output, not in the repository) and `_preview/`
  (local previews, excluded from the build)
