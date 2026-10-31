# Site map and structure

What lives where, which file produces which page, and how the pages link to
each other. Read this before making structural changes; for day-to-day
content editing, `03-editing-the-site.md` is the one you want.

---

## 1. Every page the site produces

### Fixed pages - one file each, in the repository root

| URL | File | What it is |
|---|---|---|
| `/` | `index.md` | Home. Hero, three pillars, latest news, recent publications, current projects, partners, three testimonials, contact, newsletter |
| `/approach/` | `approach.md` | The long argument: three strands of scaling, post-growth, methods |
| `/expertise/` | `expertise.html` | Six fields of expertise, each with an image and worked examples |
| `/projects/` | `projects.html` | Filterable list of all projects |
| `/publications/` | `publications.md` | Filterable list of all publications |
| `/team/` | `team.md` | **Hidden for now.** The team, then core collaborators - see §7 |
| `/partners/` | `partners.md` | Equal Earth world map, then a filterable alphabetical list with a count of projects, publications and news per partner |
| `/join/` | `join.html` | Open positions, filtered by deadline. See §8 of docs/03 |
| `/news/` | `news.md` | All news and events |
| `/impressum/` | `impressum.md` | Legal disclosure (ECG, UGB, MedienG) |
| `/datenschutz/` | `datenschutz.md` | Privacy policy (GDPR) |
| `/404.html` | `404.html` | Shown for an address that does not exist |

### Generated pages - one per content file

| URL pattern | Source folder | Count today |
|---|---|---|
| `/projects/<filename>/` | `_projects/` | 15 |
| `/publications/<filename>/` | `_publications/` | 38 |
| `/team/<filename>/` | `_people/` | 1 published, 4 held back |
| `/partners/<filename>/` | `_partners/` | 44 |
| `/news/<year>/<title>/` | `_posts/` | 11 |

**The filename is the URL.** `_projects/indicate-life.md` becomes
`/projects/indicate-life/`. Renaming a file breaks every link to it,
including ones outside this site. Treat filenames as permanent once
published.

### Produced automatically, no file needed

| URL | By | What for |
|---|---|---|
| `/sitemap.xml` | `jekyll-sitemap` | Search engines |
| `/feed.xml` | `jekyll-feed` | RSS of the news posts |
| `robots.txt` | GitHub Pages | Default crawl rules |

---

## 2. The repository

```
riselabs.at/
├── _config.yml           site settings, navigation, collections  ← see §5
├── CNAME                 the custom domain. Do not delete.
├── .gitignore            what git ignores
├── Gemfile               tells GitHub Pages which Jekyll to run
│
├── index.md              ─┐
├── approach.md            │
├── services.md            │  the fixed pages
├── projects.md            │  (list pages are generated from the
├── publications.md        │   collections below, not written by hand)
├── team.md                │
├── partners.md            │
├── news.md                │
├── impressum.md           │
├── datenschutz.md         │
├── 404.html              ─┘
│
├── _projects/            one file per project      → /projects/<name>/
├── _publications/        one file per publication  → /publications/<name>/
├── _people/              one file per person       → /team/<name>/
├── _partners/            one file per partner      → /partners/<name>/
├── _posts/               one file per news item    → /news/<year>/<title>/
│
├── _data/                structured content that is not a page
│   ├── hero.yml          the three rotating home images
│   ├── services.yml      the six service blocks
│   ├── testimonials.yml  the five quotes
│   └── impressum.yml     the legal details
│
├── _layouts/             page shells (default, project, person, …)
├── _includes/            reusable fragments (lists, tabs, filters, …)
│
├── assets/
│   ├── css/style.css     the entire stylesheet, themes included
│   ├── js/ui.js          tabs, filters, hero crossfade
│   ├── fonts/            Figtree, self-hosted
│   └── img/              photos, logos, figures
│
└── docs/                 these guides. Excluded from the built site.
```

Folders beginning with an underscore are Jekyll's. Everything else is copied
to the site as-is.

---

## 3. How things link to each other

This is the part that makes the site feel joined-up, and the part most worth
understanding before you add content.

**Every content file refers to others by filename**, without the `.md`. So in
`_projects/indicate-life.md`:

```yaml
people:
  - martin-roeck          # → _people/martin-roeck.md
clients:
  - eu-life               # → _partners/eu-life.md
partners:
  - bpie
  - tu-graz
```

Those are not just labels. They produce links, **and the link works in both
directions**, because each page asks the question from its own side:

```
                    ┌─────────────┐
                    │   PROJECT   │
                    └──────┬──────┘
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    people:           clients:          partners:
         │             partners:             │
         ▼                 ▼                 ▼
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │  PERSON  │      │ PARTNER  │      │ PARTNER  │
   └──────────┘      └──────────┘      └──────────┘

   ┌──────────────┐                   ┌──────────┐
   │ PUBLICATION  │ ── projects: ───▶ │ PROJECT  │
   │              │ ── people:   ───▶ │  PERSON  │
   │              │ ── partners: ───▶ │ PARTNER  │
   └──────────────┘                   └──────────┘

   ┌──────────┐
   │   POST   │ ── projects: ───▶ a project
   │  (news)  │ ── people:   ───▶ a person
   └──────────┘
```

Write the link **once**, on the file where it is most natural, and both pages
show it:

| You write this… | …on this file | …and it also appears on |
|---|---|---|
| `people: [martin-roeck]` | a project | Martin's page, under his projects |
| `projects: [indicate-life]` | a publication | the INDICATE LIFE page, under publications |
| `clients: [ec-dg-env]` | a project | the DG ENV partner page, under "as client" |
| `projects: [gbdi]` | a news post | the GBDI project page, under updates |
| `partners: [uct]` | a news post | UCT's partner page, under News & events |

Person and partner pages each end with a tabbed panel - **All · News &
events · Projects · Publications · People** - assembled entirely from these
references. Project pages show the same material as stacked sections with
headings rather than tabs, because each section carries more detail there.
Either way, nothing in them is maintained by hand.

**A reference to a file that does not exist is silently ignored.** Nothing
breaks, nothing appears, and no error is shown. This is the single most
common way for content to go missing. `docs-check.py` in the repository root
catches it - see §6.

---

## 4. Which page shows what

Useful when you add something and want to know where it will surface.

| Add this | Appears on |
|---|---|
| A project with `status: current` | `/projects/`, its own page, the home page's current projects |
| A project with `status: concluded` | `/projects/`, its own page |
| A publication | `/publications/`, its own page, and - if among the four newest by year - the home page |
| A person with `group: rise` | their own page; the team list too, once it is unhidden |
| A person with `group: collaborator` | the same, under "Core collaborators" |
| A partner | `/partners/`, its own page. **Only appears on the home page if added by hand** to the list in `index.md` |
| A news post | `/news/`, its own page, and the home page's latest three |
| A news post with `featured: true` | the same, but jumps to the front of the home page's three |
| Anything with `published: false` | nowhere at all |

---

## 5. `_config.yml`, the settings file

Worth knowing about, rarely worth changing:

| Setting | Does what |
|---|---|
| `title`, `tagline`, `description` | Browser tab, search results, social previews |
| `url`, `baseurl` | The live address. Leave alone |
| `email`, `linkedin`, `scholar` | Used in the footer and contact blocks |
| `author_cite` | `"Röck M"` - underlined automatically in every author list |
| `privacy_url` | Setting it adds the Datenschutz link to the footer |
| `newsletter_action` | The Buttondown form endpoint |
| `nav` | The main menu. Order here is order on screen |
| `collections` | Declares the five content folders. Changing a `permalink` here changes every URL under it |
| `plugins` | seo-tag, feed, sitemap |
| `exclude` | Files kept out of the built site, including `docs/` |

### Themes

Dark is the default; a toggle in the bottom corner switches a page to
light, and a visitor whose system is set to light gets light without asking.
Colour lives in two layers at the top of `assets/css/style.css`: brand
constants that never change, and semantic tokens the theme swaps. Changing
the palette means editing those tokens, nothing else.

The hero keeps its dark image bed in both themes - a pale wash over the same
photographs would leave dark text fighting the imagery - so its text colours
are pinned rather than inherited.

Nothing is stored on the visitor's device, by choice. The consequence is that
the theme resets on navigation. To make it persist, the value would have to be
kept in `localStorage` and read back by a small inline script in `<head>`
before first paint; the comment in `assets/js/ui.js` says where.

---

## 6. Checking the site before you publish

`docs-check.py` in the repository root reads every content file and reports
problems that Jekyll will not:

```
python3 docs-check.py
```

It catches: references to files that do not exist, missing images and logos,
missing required fields, duplicate testimonial ids, navigation pointing at
pages that are not there, and front matter using a field name Jekyll reserves
for itself.

That last one is worth knowing about. Jekyll gives every page its own `url`,
`path`, `id`, `date`, `content` and a few others. A front matter field with
one of those names is **silently ignored** - which is how every partner page
once came to link to itself instead of to the partner's website. The field is
now called `website`, and the checker refuses the reserved names outright.

A clean run prints `no problems found`. Run it before any sizeable change
goes live.


---

## 7. The hidden team page

`/team/` is deliberately not built at the moment. The team is still forming
and the page was thin. Nothing has been deleted.

Three things keep it hidden, and all three have to be undone together:

1. `team_page: false` in `_config.yml` - this also hides the "← The team" and
   "The whole team →" links on person and partner pages, so they do not point
   at a page that is not there.
2. `published: false` in `team.md`.
3. The Team entry in `nav` is commented out.

Three people - Barbara Droste-Luckmann, Nicole Di Santo and Zuhaib Batra -
also carry `published: false`, because their pages still contain `[ADD]`
placeholders. Remove that line once their text is written, whether or not the
team page is back.

Martin's page stays live throughout: it is linked from projects and
publications, and it is finished.

`docs-check.py` knows the difference between a link to a *hidden* page and a
link to a *missing* one, and reports the first as a note rather than an error.
