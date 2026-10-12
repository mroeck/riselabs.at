# riselabs.at

Interim RISE site. Static Jekyll, built and served by GitHub Pages. Designed to
be replaced when the CI revamp lands — nothing here is precious.

## Documentation

Three guides in `docs/` (excluded from the built site):

| | |
| --- | --- |
| `01-publishing-on-github.md` | Getting it online, the custom domain, failed builds |
| `02-site-map-and-structure.md` | What file produces what page, and how pages link |
| `03-editing-the-site.md` | Handbook for whoever updates the site. Start here |
| `04-roadmap.md` | What is not done, including the collaboration network graph |
| `newsletter-page-copy.md` | Text for the Buttondown subscribe page |

Before publishing a change, run `python3 docs-check.py` from this folder. It
catches broken cross-references, missing images and reserved field names —
things Jekyll builds happily and silently gets wrong.

## Design basis

Follows the RISE CI Manual v1.2:

| | |
| --- | --- |
| Navy | `#001730` — page background |
| Magenta | `#f92d84` — the only accent |
| Purple | `#751094` — gradient only, per the manual |
| Blush | `#ffe1ee` — reserved for light-theme use, currently unused |
| Type | Circular is licensed; **Figtree** stands in as the closest open match |

### Themes

Dark is the primary theme and what every page loads with. A toggle in the
bottom corner switches to light for that page view; nothing is stored on the
visitor's device, so the choice does not follow them from page to page.

Colour is defined in two layers in `assets/css/style.css`: the **brand
constants** (`--navy`, `--magenta`, `--purple`, `--blush`), which never change,
and the **semantic tokens** (`--bg`, `--surface`, `--ink`, `--ink-soft`,
`--accent`, `--rule`, `--field-bg`, `--btn-*`), which the theme swaps. A new
palette means repointing the semantic layer — no rule in the file needs
touching.

The light accent `#be208b` is the CI magenta blended 45% toward the CI purple,
because `#f92d84` reaches only 3.7:1 on white and fails WCAG AA for text. Pure
magenta is still used for fills and rules, where the text rules do not apply.

If you buy a Circular web licence, swap the font files in and change `--font`
in `assets/css/style.css`. That is the only change needed.

Logos were derived from the supplied PNG: `rise-logo-navy.png`,
`rise-logo-white.png` (used on the dark site) and two signets for the favicon.
Replace with the official SVGs from the brand package when convenient — they
will be sharper.

## Adding news

Create a file in `_posts/` named `YYYY-MM-DD-short-slug.md`:

```
---
layout: post
type: output
featured: true
title: "A global buildings database, openly published"
summary: "One line shown in the news list and on the home page."
---

Body text in markdown.
```

The date comes from the filename — rename the file to change it.

| Field | Required | What it does |
| --- | --- | --- |
| `title` | yes | shown everywhere |
| `type` | no | small label: `opening`, `project`, `output`, `event`, or anything you like |
| `summary` | no | one line under the title in lists |
| `featured` | no | `true` pins it to the top of the home page |
| `published` | no | `false` keeps it out of the site entirely |

**Home** shows three items: anything featured first, then the most recent.
**News** is the full archive, newest first, broken by year.

So an older item can be kept visible by featuring it, and an announcement
drops off the front page by itself once three newer things exist. Nothing
needs maintaining by hand.

`_posts/2026-10-05-example-open-position.md` is a job-advert template with
`published: false`. Copy it, rename with the date, edit, remove that line.

## The content model

Four folders hold everything. Each file becomes its own page with its own URL,
and the links between them are made by writing a filename.

```
_projects/      → /projects/<filename>/
_people/        → /team/<filename>/
_publications/  → /publications/<filename>/
_partners/      → /partners/<filename>/
_posts/         → /news/<year>/<slug>/
```

Naming conventions that keep URLs readable:

| Folder | Filename pattern | Example URL |
| --- | --- | --- |
| `_publications/` | `author-year-keywords` | `/publications/roeck-2020-embodied-ghg-emissions/` |
| `_posts/` | `YYYY-MM-DD-keywords` | `/news/2026/gbdi-association/` |
| others | a short name | `/partners/ku-leuven/` |

A post's filename still needs the full date (Jekyll requires it), but only the
year and the keywords appear in the URL.

Cross-references use the other file's name, without `.md`:

```yaml
# in a project, publication or post
people:
  - martin-roeck

# in a publication or post — one or several
projects:
  - analysis-of-life-cycle-greenhouse
  - indicate-life

# in a project: who it is for, and who we do it with
clients:
  - ec-dg-grow
partners:
  - ku-leuven
  - ramboll

# in a publication: the affiliations behind the co-authors
partners:
  - ku-leuven
  - tu-graz
```

Each page then gathers what points at it, with no list to maintain:

| Page | Shows |
| --- | --- |
| Person | their projects, publications and news |
| Project | who works on it, its publications, its client, its collaborators, its news |
| Publication | its RISE authors, the projects it came from, the affiliations behind it |
| Partner | projects we do for them, projects we do together, publications |
| Team, Projects, Publications, Partners, News | everything in the folder |

A section is skipped entirely when nothing points at it, so a stub page stays
clean.

## Adding a person

Copy `_people/example-colleague.md`, rename it to the person's name in
lowercase with hyphens, remove the `published: false` line, and let them write
whatever they want in the body.

```
---
name: "Full Name"
role: "Researcher"
cite: "Surname F"        # how the name appears in author lists
order: 2                 # position in the team list
portrait: /assets/img/people/filename.jpg
email: "name@riselabs.at"
summary: "One line, shown in the team list."
links:
  - title: LinkedIn
    url: "https://..."
---
```

`cite` is what gets underlined in publication author lists. Portraits are
square, around 700px.

## Adding a publication

One file in `_publications/`. The filename becomes the URL, so
`2026-context-specific-pathways.md` publishes at
`/publications/2026-context-specific-pathways/`.

```
---
title: "Context-specific life cycle emissions pathways for EU buildings"
kind: article            # article | book | report | data — picks the section
authors: "Alaux N, Allacker K, Passer A, Röck M"
year: 2026
journal: "Nature Communications"
doi: "10.1038/s41467-026-73433-1"
people:
  - martin-roeck
project: analysis-of-life-cycle-greenhouse
---
```

Only `title`, `kind`, `authors` and `year` are required. A publication can
also carry `outputs:` to embed or offer a PDF, exactly as a project does.

## The home page

Built from `index.md` plus two small pieces:

- `_data/hero.yml` — the three hero images, crossfading slowly behind the
  headline. Replace the files; one per brand pillar.
- `_includes/newsletter.html` — the signup block.

Everything else on the home page pulls itself from the collections: latest
news, four most recent publications, current projects, a selected row of
partners. The partner row is the one hand-picked list, set by the `shown`
line in `index.md`.

**The newsletter has two possible wirings**, and they are not
interchangeable:

```yaml
# a button that opens your Buttondown page — currently set
newsletter_url: "https://buttondown.com/riseregenerate"

# a form on the page itself, posting to Buttondown's API
newsletter_action: "https://buttondown.com/api/emails/embed-subscribe/riseregenerate"
```

`newsletter_url` is the public page where people subscribe and read past
issues. `newsletter_action` is the API endpoint a form posts to. Posting a
form at the page URL subscribes nobody, which is why they are separate
settings.

Set both and the form shows with a link to the archive beneath it. Comment
both out and the block falls back to an email link, so the page never shows a
control that cannot work.

A form on the page converts better; a link keeps people on Buttondown where
the archive lives. Either is a reasonable choice.

## Highlighting key points on a project page

Objectives, findings and lessons read better as a list with a coloured lead
sentence. Wrap a plain markdown list in a `findings` div:

```
<h2>What we found</h2>

<div class="findings" markdown="1">

- **The lead sentence, which carries the point.** Then the explanation,
  as long as it needs to be.
- **The next point.** And its explanation.

</div>
```

The `markdown="1"` attribute matters — without it kramdown leaves the list as
literal text. The bolded lead renders in magenta on its own line.

## Tabs and filtering

Person, project and partner pages group their related content into tabs — All,
Projects, Publications, News. List pages have a filter box above them.

Both are progressive enhancement: without JavaScript every panel is visible
and every list is complete. That is also what search engines and printing see.
The filter box stays hidden until the script enables it, so it never appears
as a control that does nothing.

Neither needs configuring. A tab appears when there is something to put in it,
and the filter matches against all the text in each row.

## Partner logos

Every partner currently has a **placeholder wordmark** — the name set in type,
generated as an SVG in `assets/img/partners/`. They are there so the layout is
right; they are not the real logos.

To replace one: download the organisation's logo, save it as
`assets/img/partners/<partner-filename>.svg` (or `.png`), and it is picked up
automatically. Logos sit on a white tile, so a dark logo on a transparent
background works best. The `logo:` line in each partner file points at the
filename.

## Adding a partner

One file in `_partners/`, named for the organisation. Referenced from a
project's `clients:` or `partners:` list, and from a publication's
`partners:` list.

```
---
name: "KU Leuven"
city: "Leuven"
country: "Belgium"
type: "university"       # or consultancy, foundation, public authority, …
url: "https://www.kuleuven.be"
logo: ku-leuven.svg      # optional; without it the name shows as text
# coords: [50.88, 4.70]  # for the future map
---
```

Only `name` is required. Logos go in `assets/img/partners/`; they sit on a
white tile, so dark logos work best. The partners page groups by country.

`type` is there for stakeholder categories — nothing filters on it yet, but
recording it now means the data is ready when something does.

**On the future map and network diagram.** The references already form a
graph with typed edges. Uncomment `coords:` on each partner and the same data
can be drawn as a map; nothing else needs recording.

## Adding a project

Each project is one file in `_projects/`. The filename becomes the URL, so
`_projects/collaborative-carbon.md` is published at
`riselabs.at/projects/collaborative-carbon/`.

```
---
title: "Collaborative Carbon — Whole Life Carbon Assessments"
status: current
years: "2024–2026"
funder: "Laudes Foundation"
role: "Principal Investigator"
partners: "RISE with einszueins and TU Delft"
link: "http://www.collaborative-carbon.com"
summary: "One line, shown in the project list."
---

Body text. As long or short as you like — this is the project's own page.
```

Only `title`, `status` and `years` are required. `status` is `current` or
`concluded`; changing that word moves the project between sections. The list
sorts by start year, newest first, so the order of files does not matter.

### Giving a project a full page

All of these are optional and are skipped when absent, so a stub and a full
study use one template.

```
project_title: "The full official title, if it differs from the heading"
grant: "LIFE 101167585"
tags:
  - whole life carbon
hero: /assets/img/project-hero.jpg
hero_caption: "Shown under the image."
outputs:
  - title: "Analysis of results and implications"
    note: "Final report · European Commission, 2025"
    url: "https://data.europa.eu/doi/10.2873/2247112"
    thumb: /assets/img/outputs/dg-grow-report.jpg
figures:
  - file: /assets/img/figures/fig-01.png
    number: "Figure 1"
    caption: "What the figure shows."
    source: "Where it came from."
```

**Outputs point outward.** Each card opens the deliverable in a new tab at
wherever the publisher hosts it, so the PDFs are not in this repository. Only
the thumbnail is — a cover image around 400px wide in
`assets/img/outputs/`. Without one the card shows a plain "PDF" tile. Add one
block per deliverable; five reports is five blocks.

**On hero photos.** Nothing checks that the photo matches the project — it is
whatever `hero:` points at. Keep project photos named after their project
(`indicate-life-hero.jpg`) so the mismatch is visible in the file name.

### Linking news to a project

Add `project: <filename>` to a news post and it appears automatically under
**Updates** on that project's page:

```
---
layout: post
type: output
project: global-building-data-initiative
title: "A global buildings database, openly published"
---
```

The value is the project's filename without `.md`. Nothing else needs doing —
the project page picks it up, and the post still appears in the news feed as
normal.

## Adding a publication

One line per entry in `publications.md`, inside the `{% capture entries %}`
block:

```
- Authors. **Title.** *Journal*, 2026. https://doi.org/...
```

Names listed in `author_cite` (`_config.yml`) underline automatically, bare
`https://` links become clickable, `**bold**` marks the title and `*italic*`
the journal.

## A note on headings

Markdown headings (`## Like this`) do **not** work inside `<div>` blocks —
kramdown leaves them as literal text. Inside the page wrappers, write
`<h2>Like this</h2>` instead. The existing pages already do.

## Publishing

1. New **public** repository on GitHub.
2. Upload the *contents* of this folder (not the folder).
3. Settings → Pages → Deploy from a branch → `main` → `/ (root)`.
4. Check it at `https://<username>.github.io/<repo>/` first.
5. Remove the Linktree forwarding on riselabs.at at the registrar.
6. Add DNS: four A records on `@` to `185.199.108.153`, `.109.153`,
   `.110.153`, `.111.153`, and a CNAME on `www` to `<username>.github.io`.
7. Settings → Pages → Custom domain → `riselabs.at`. Then Enforce HTTPS.

`CNAME` already contains `riselabs.at`. If the DNS check fails, delete that
file until the records resolve, as with martinroeck.com.

## Structure

```
_config.yml              title, nav, contact, author_cite, collections
index.md                 Home — positioning, scaling logic, latest news
approach.md              Approach — the long argument
projects.md              lists _projects/ automatically; nothing to edit
publications.md          one line per publication
news.md                  the news archive
_projects/               one file per project → its own page and URL
_posts/                  one file per news item → its own page and URL
_includes/newslist.html  shared news list markup
_layouts/                default, post, project
assets/css/style.css     all styling
assets/img/              logos
CNAME                    riselabs.at
```
