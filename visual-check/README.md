# Visual check (Phase Q)

Proves that a refactoring step changed nothing a visitor can see or a search
engine can read, or shows exactly what it did change.

```sh
cd visual-check
npm install                      # once; uses the Chromium that Playwright installs
npx playwright install chromium  # once, if no Chromium is present

# 1. on main, with the site served locally (bundle exec jekyll serve)
node visual-check.mjs shoot http://localhost:4000 ../.visual/before

# 2. on the branch, same command, other folder
node visual-check.mjs shoot http://localhost:4000 ../.visual/after

# 3. compare: report.md plus a diff image for every page that moved
node visual-check.mjs compare ../.visual/before ../.visual/after ../.visual/report
```

For Q6, repeat steps 1 to 3 with `NOJS=1` in front of each `shoot` command:
that shows the pages as a visitor without JavaScript sees them.

Attach `report.md` to the pull request. A step passes when the report lists
no differences, or only the ones the step was meant to make (Q1). Exit code 0
means no difference at all.

`visual-check/` is excluded from the Jekyll build in `_config.yml`;
`.visual/` and `visual-check/node_modules/` are in `.gitignore`.

## How it actually runs (3 Nov 2026)

The steps above need Jekyll, and the implementer cannot install it:
rubygems.org answers 403 through the proxy that environment uses, so there is
no `bundle install` and no `jekyll serve` there. Nothing above is wrong; it
just cannot be run from that machine.

So the same two shoots run in GitHub Actions instead, where the
`github-pages` gem installs normally:
`.github/workflows/visual-check.yml` builds the base commit and the head
commit with one Jekyll, serves each with `python3 -m http.server`, shoots
both, and compares. It writes `report.md` into the job summary, posts it as a
single comment on the pull request that it rewrites on each push, and uploads
every screenshot and diff image as an artifact. It also diffs `feed.xml`,
`sitemap.xml` and the list of built pages, which rule 5 asks for and
screenshots cannot show.

The check reports and does not block: Q1 changes pages on purpose, so a red
tick there would be noise.

Anyone with Ruby can still run the commands above by hand. The workflow uses
the same script with the same arguments.
