> **Parked, 31 October 2026.** Martin asked for this to be archived until he
> asks for it again; it may not happen at all. Nothing is set up: no Netlify
> site was ever connected to this repository, and no preview build has ever
> run on a pull request.
>
> The file is kept rather than deleted because the research in it still
> holds - why Netlify over Cloudflare Pages, and the one thing Cloudflare
> does better - and redoing that work would cost more than storing it. If
> this is revived, read the dated note at the end first: the advice here was
> wrong once and was corrected.
>
> Nothing in the repository depends on this. `netlify.toml` sits at the root
> doing nothing, because a build file only does something once a Netlify site
> points at the repository.

# Deploy previews

Every pull request gets its own built copy of the site at its own URL, so a
visual change can be looked at before it is merged instead of after.

The live site does not move. riselabs.at is still built and served by GitHub
Pages from `main`, exactly as before. Netlify builds pull requests and
nothing else.

## Why Netlify rather than Cloudflare Pages

Both do this. Netlify fits this repository better for three reasons:

1. **The Gemfile is `github-pages`.** That gem pins Jekyll and its plugins to
   the exact set GitHub Pages runs. Netlify's build image ships Ruby and
   Bundler and runs `bundle exec` as a matter of course, so the preview is
   built by the same gems as production. On Cloudflare the Ruby version has
   to be pinned by hand and kept in step with whatever `github-pages`
   currently wants.
2. **The preview shows up in the pull request.** Netlify adds a Deploy
   Preview check to the PR with the link in it, which is where the review
   already happens.
3. **Previews are not indexed.** Netlify sends `X-Robots-Tag: noindex` on
   deploy previews by default, and `netlify.toml` repeats it for every path.
   A second public copy of the site in search results is a real hazard and
   worth belt and braces.

The one place Cloudflare would win: **gating previews behind a login.**
Cloudflare Access can put previews behind a sign-in on the free tier;
Netlify's password protection and private projects are paid features. That
matters if a preview would ever carry something that must not be public -
an unapproved person page, a job post before it is announced. Today it does
not, because everything in the repository is already published. If that
changes, this decision is worth revisiting rather than worked around.

## Setting it up (once, needs the Netlify account)

1. Sign in at netlify.com with GitHub.
2. **Add new project → Import an existing project → GitHub**, and pick
   `mroeck/riselabs.at`. Authorise Netlify for that one repository, not for
   everything.
3. The build settings come from `netlify.toml`, so leave the build command
   and publish directory as they appear. Deploy.
4. **Project configuration → Build & deploy → Branches and deploy contexts:**
   - Leave the **production branch** as `main`.
   - Leave **Deploy Previews** enabled.
   - Set **branch deploys** to none.
5. Open any pull request. Within a minute or two the PR shows a
   `netlify/<project>/deploy-preview` check with a link to the built site.

### Why `main` stays the production branch

A first draft of this file said to point the production branch at a branch
that does not exist, so that Netlify would never publish a production copy.
That would have switched the previews off along with it. Netlify only builds
a Deploy Preview when the pull request's **base branch** is either the
production branch or a branch with branch deploys enabled; with the
production branch pointing nowhere, every pull request against `main` would
have had no preview, which is the whole point of this.

So `main` stays the production branch, and Netlify does publish its own copy
of the site at `<project>.netlify.app`. That copy is harmless: it is not
linked from anywhere, `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`
on every path so it stays out of search results, and every canonical tag on
it points at riselabs.at. riselabs.at remains the live site, served by GitHub
Pages, and nothing about this changes that.

Optional: **Site configuration → Notifications → Deploy notifications → add a
GitHub pull request comment**, if a comment in the thread is easier to find
than the checks list.

## What a preview is and is not

- It is the **real Jekyll build**, with the real plugins. If Liquid is wrong,
  the preview fails the way production would.
- It is **not production**. `JEKYLL_ENV` is `preview`, not `production`, so
  anything wrapped in `jekyll.environment == "production"` stays off. That
  matters for the analytics snippet of R10: without this, every preview of
  every pull request would count itself as traffic on the real statistics.
- **Absolute URLs still point at riselabs.at.** `url:` in `_config.yml` is
  the live domain, so canonical tags, the feed and the sitemap on a preview
  name production. Navigation inside the preview works, because the templates
  use `relative_url`. Do not read a preview's `<head>` as if it were the
  deployed one.

## If the first build fails

Almost always Ruby. The `github-pages` gem is particular about which version
it runs on, and the error says which it wants. Change `RUBY_VERSION` in
`netlify.toml` to that version and push; nothing else needs touching.

There is no `Gemfile.lock` in this repository, which is deliberate: GitHub
Pages resolves the gems itself. Netlify does the same. If builds ever start
differing between the two, committing a lockfile is the fix, and then both
build from it.
