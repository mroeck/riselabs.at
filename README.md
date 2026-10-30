# riselabs.at

Interim RISE site. Static [Jekyll](https://jekyllrb.com), built and served by
GitHub Pages. Designed to be replaced when the CI revamp lands - nothing here
is precious.

## Before you publish anything

```sh
python3 docs-check.py
```

It catches broken cross-references, missing images, reserved field names and
unresolved layouts - the kinds of mistake Jekyll builds happily and silently
gets wrong. Run it from this folder. "no problems found" means go.

## Where the documentation is

Everything about how to use and edit this site lives in `docs/`, which is
excluded from the built site. **Start with `03`.**

| File | What it covers |
| --- | --- |
| `docs/01-publishing-on-github.md` | Getting it online, the custom domain, failed builds |
| `docs/02-site-map-and-structure.md` | What file produces what page, and how pages link |
| `docs/03-editing-the-site.md` | **Handbook for whoever updates the site. Start here** |
| `docs/04-roadmap.md` | What is not done yet |
| `docs/05-design-basis.md` | The CI colours, type and layout rules the CSS implements |
| `docs/06-core-collaborators.md` | Inviting and publishing core collaborator profiles |
| `docs/07-review-implementation.md` | The review work order: phases P, L, R and W |
| `docs/08-deploy-previews.md` | Preview builds for pull requests, and how to set them up |
| `docs/09-publications-without-a-project.md` | Which publications belong to which project, and the projects still missing |
| `docs/10-boilerplate.md` | The short texts for search results, profiles, proposals and press |
| `docs/newsletter-page-copy.md` | Text for the Buttondown subscribe page |

## The two scripts

| Script | What it does |
| --- | --- |
| `docs-check.py` | The checker described above. Run it before every publish |
| `fetch-abstracts.py` | Pulls publication abstracts from Crossref/OpenAlex by DOI |
| `make-figures.py` | Redraws the CollaborativeCarbon charts from their source values |

Neither is published - both are in the `exclude` list in `_config.yml`.

## Running it locally

```sh
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. Ruby 3.2 is the safe version; the
`github-pages` gem pins Jekyll 3, which does not get on with Ruby 3.4.
