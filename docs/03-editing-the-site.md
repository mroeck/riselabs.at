# Editing the site

A handbook for whoever keeps riselabs.at up to date. No coding knowledge
assumed. Everything here can be done in a browser on github.com.

**The one idea to take away:** every piece of content is a plain text file,
and the filename becomes the web address. Add a file, the page appears. There
is no admin panel, no "publish" button, and nothing to break that a second
pair of eyes cannot catch.

---

## Contents

1. [How to add or edit anything](#1-how-to-add-or-edit-anything)
2. [The shape of every file](#2-the-shape-of-every-file)
3. [Rules that prevent most mistakes](#3-rules-that-prevent-most-mistakes)
4. [Add a project](#4-add-a-project)
5. [Add a publication](#5-add-a-publication)
6. [Add a person](#6-add-a-person)
7. [Add a partner](#7-add-a-partner)
8. [Add a news post or event](#8-add-a-news-post-or-event)
9. [Images](#9-images)
10. [Edit the fixed pages](#10-edit-the-fixed-pages)
11. [Services and testimonials](#11-services-and-testimonials)
12. [Writing text: formatting that works](#12-writing-text-formatting-that-works)
13. [Checklist before publishing](#13-checklist-before-publishing)
14. [When something goes wrong](#14-when-something-goes-wrong)

---

## 1. How to add or edit anything

**To change existing text:** find the file on github.com, click the pencil
icon, edit, then **Commit changes** at the bottom. The site rebuilds within
about a minute.

**To add something new:** open the right folder (`_projects`, `_people`, and
so on), click **Add file → Create new file**, type the filename, paste one of
the templates below, fill it in, commit.

**For anything substantial**, choose *Create a new branch for this commit* on
the commit screen and open a pull request. Nothing goes live until it is
merged.

**For anything not finished**, add `published: false` as the first line under
the opening `---`. Jekyll skips the file entirely. Remove that line when
you're ready.

---

## 2. The shape of every file

Each content file has two parts:

```markdown
---
title: "The bit between the dashed lines is the front matter"
year: 2026
---

Everything after the second set of dashes is the body text, written
in ordinary prose.
```

The **front matter** is structured information - title, year, who it links
to - in YAML. The **body** is free text.

Some files need only front matter. A publication, for example, works
perfectly well with an empty body.

---

## 3. Rules that prevent most mistakes

**Filenames become web addresses.** `_projects/indicate-life.md` is
`/projects/indicate-life/`. Use lowercase, hyphens instead of spaces, no
accents or special characters, ending `.md`.

**Never rename a published file.** It breaks every link to that page,
including links on other people's sites. Change the title inside instead -
the title and the filename are allowed to differ.

**Put double quotes around any title containing a colon.** This is the single
most common cause of a failed build:

```yaml
title: "Carbon budgets: a European view"     ✓
title: Carbon budgets: a European view       ✗  build fails
```

Quotes are always safe. Use them by default.

**Indent with spaces, never tabs.** YAML forbids tab characters. The GitHub
editor inserts spaces, so this only bites if you paste from elsewhere.

**Links between files use the filename without `.md`:**

```yaml
people:
  - martin-roeck          ✓
  - Martin Röck           ✗  silently ignored
  - martin-roeck.md       ✗  silently ignored
```

A reference that doesn't match a file is **silently dropped**. No error, no
warning - the connection just doesn't appear. When something you expected
doesn't show up, this is almost always why. Run `python3 docs-check.py` to
catch it.

---

## 4. Add a project

Create `_projects/short-name.md`:

```markdown
---
title: "The full project title"
status: current
years: "2025–2028"
funder: "Who is paying for it"
role: "What RISE does on it, e.g. Work package lead"
summary: "One sentence, no full stop. Shown in lists and on the home page."
link: "https://project-website.example"
clients:
  - partner-filename
partners:
  - another-partner-filename
people:
  - martin-roeck
---

A paragraph or several about the project. What it is for, what it
produces, why it matters.
```

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Quote it if it contains a colon |
| `short_title` | yes | The project's name in a sentence, up to 34 characters: "Re:Living", "GBDI pilot", "EU whole life carbon roadmap". Used wherever a project is named mid-sentence instead of as a headline, such as the engagement cards. The full `title` is still what the project's own page and the card grids show |
| `status` | yes | `current` or `concluded`. Only `current` reaches the home page |
| `years` | yes | `"2025–2028"`. An en dash (–) not a hyphen |
| `funder` | yes | Who funds the work. Shown in one **Funder / client** row together with `clients`, because on every project so far they are the same organisation. Where `clients` names a partner, that partner's linked name is what shows; `funder` is the fallback where there is no partner file, and is shown in brackets alongside only when it says something the partner name does not |
| `role` | yes | What RISE's role is |
| `summary` | yes | One sentence. No full stop - it sits in lists |
| `link` | no | The project's own website |
| `clients` | no | Partner filenames. Shown in the **Funder / client** row as links to their partner pages |
| `partners` | no | Partner filenames, shown as tiles under **Partners**. The first is `rise` on every project that ran while RISE existed: it is not a file in `_partners/` but a tile written by the include, pointing at the home page. `docs-check.py` adds it to the rule below and fails a project that claims RISE for work it predates |
| `people` | no | Person filenames |
| `hero` | no | A wide photo at the top: `/assets/img/name.jpg` |
| `hero_caption` | no | What the photo shows |
| `hero_tone` | no | `false` turns the picture treatment off for this project's card. **No project uses it.** Eight did, the map and screenshot heroes, until Martin dropped the exceptions on 31 Oct 2026 for one consistent surface. Kept for the next diagram hero that wants it; `docs-check.py` notes that nothing does |
| `featured` | no | `true` puts this project at the front of the home page grid, ahead of anything newer. Nothing carries it today. Seven featured projects would fill the grid and push every recent one off it |
| `tags` | no | Free-text labels |
| `partners_note` | no | A line explaining the partner list. Shown in the sidebar row, on its own where there are no names |
| `partners_omitted` | no | `true` means this project shows no partner tiles at all, RISE included, because any list short enough to show would be an arbitrary selection. Requires `partners_note` to say why, and the project must list no partners. One project uses it: IEA EBC Annex 72, 27 countries |

**`rise` in `partners` is written by the rule, not by hand.** A project
lists RISE when it ran to 2023 or later with a core RISE person on it, which
is the same test the publications list uses for `rise_tier`. Two projects ran
entirely before RISE was founded - PEF4Buildings and Towards embodied carbon
benchmarks - and must not claim it. `docs-check.py` fails a project that has
it wrong in either direction, or that lists `rise` anywhere but first.

**The hero photo must actually be of this project.** Nothing in the system
checks that. A photo from a different project on a project page is the kind
of error that is embarrassing precisely because it looks deliberate.

### Optional: outputs and figures

```yaml
outputs:
- title: "Final report"
  note: "European Commission, 2025"
  url: "https://data.europa.eu/doi/10.2873/2247112"

figures:
- file: /assets/img/figures/name.jpg
  number: Figure 1
  caption: What the figure shows.
  source: Where it came from.
```

`outputs` are **published deliverables** - reports, datasets, tools that
anyone may read. Internal notes, drafts and briefing documents do not belong
here.

---

## 5. Add a publication

Create `_publications/firstauthor-year-keywords.md` - for example
`roeck-2026-embodied-carbon-benchmarks.md`. Lowercase surname, no accents
(`roeck`, not `röck`).

```markdown
---
title: "The full title of the paper"
kind: article
authors: "Röck M, Surname F, Another A"
year: 2026
journal: "Journal name, or the publisher"
doi: "10.1016/j.example.2026.123456"
people:
  - martin-roeck
projects:
  - project-filename
partners:
  - partner-filename
---
```

| Field | Required | Notes |
|---|---|---|
| `title` | yes | |
| `kind` | yes | `article`, `report`, `data` or `book` |
| `authors` | yes | One string, `Surname I` format, comma-separated, **in the published order**. `Röck M` is underlined automatically |
| `year` | yes | A number, unquoted. Sorting depends on it |
| `journal` | no | Journal, publisher or repository |
| `doi` | no | The bare DOI, no `https://doi.org/` prefix |
| `url_external` | no | Only when there is no DOI |
| `people`, `projects`, `partners` | no | Filenames |
| `rise_tier` | written for you | `core`, `extended` or `prior`. Decides the order inside a year on /publications/. Never edit it by hand: run `python3 make-rise-flags.py`, which derives it from `people` and each person's `group` and `rise_since` |

The body can be left empty. Add a paragraph only when there is something
worth saying beyond the citation.

**On the order of the list.** /publications/ runs newest year first, and
inside a year `core` (someone with `group: rise` was on it, from their
`rise_since`), then `extended` (the wider team), then `prior` (what an author
published before joining). Inside one tier the order is the order the files
build in: the entries carry a year and no month, so there is no recency to
sort on and nothing invents one.

**On `partners`:** this should reflect the real affiliations of the
co-authors. Some entries were seeded from the relevant project's partner list
rather than checked against the paper, so treat existing values as
provisional and verify when you touch a file.

---

## 6. Add a person

Create `_people/firstname-surname.md`. Use plain letters in the filename
(`martin-roeck`), the real spelling in the `name` field.

```markdown
---
name: "Dr. Firstname Surname"
role: "Their role"
cite: "Surname F"
group: rise
order: 3
portrait: /assets/img/people/firstname-surname.jpg
email: "firstname.surname@riselabs.at"
summary: "One line on what they work on, shown in the team list."
links:
  - title: LinkedIn
    url: "https://www.linkedin.com/in/..."
  - title: ORCID
    url: "https://orcid.org/..."
---

A paragraph or two, ideally in their own words.
```

| Field | Required | Notes |
|---|---|---|
| `name` | yes | As it should appear, titles included |
| `role` | yes | |
| `group` | yes | `rise` for the institute, `collaborator` for close collaborators employed elsewhere |
| `org` | if collaborator | Where they actually sit, e.g. `"Global Building Data Initiative, EPFL"` |
| `cite` | no | How they appear in author lists, e.g. `Surname F` |
| `order` | no | Position within their group. Lower first |
| `portrait` | no | See §9 |
| `email`, `links` | no | |
| `summary` | no | One line for the team list |

`_people/example-colleague.md` is a filled-in template carrying
`published: false`. Copy it rather than starting from scratch, and remember
to remove that line.

**The team page is currently hidden** - see §7 of
`02-site-map-and-structure.md` for what to switch back on. Three people are
held back with `published: false` because their pages still have `[ADD]`
placeholders in them. A person page goes live the moment that line is
removed, whether or not the team list is back, so write the text first.

**When someone leaves**, don't delete the file - their name is attached to
projects and publications. Either set `published: false`, or keep the page and
change the role to past tense.


### Fields added October 2026

| Field | Type | Shown | Notes |
|---|---|---|---|
| `tagline` | string; a note above 140 characters, a failure above 220 | Card and profile | One line in their own words on why they do this work. On the profile it replaces `summary` as the lede; `summary` is still what lists elsewhere use |
| `works_on` | list of theme slugs | Profile, as chips | From `_data/themes.yml` only. `docs-check.py` rejects an unknown slug, exactly as it does for a project's `themes` |

**Portraits.** Square, at least 600 × 600 px, head and shoulders. A person
without one gets their initials on a token-coloured square, taken from `cite`
("Röck M" gives RM). **Never a stock photograph of a face** - see `docs/06`.

**Every card shows an affiliation**, the person's own institutions for RISE
staff or "Extended team · <institutions>" for everyone else, from `affil`
(short, in acronyms) falling back to `org`. That is what lets the team page be
one grid instead of two sections.

**A card shows three links at most**: email, LinkedIn and ORCID, in that
order, whatever order they sit in the front matter. Those are what a reader
wants from a card - how to write to someone, who they are professionally, and
what they have published. Everything else a person links to appears on their
own page. A person missing one of the three simply shows fewer.

`docs-check.py` checks an ORCID against its own checksum, because a single
wrong digit still resolves - to a stranger's publication record.

**`rise_since`** is the year a person started with RISE or GBDI, as a bare
number. It is what the "With RISE or GBDI" filter on `/publications/` uses: a
publication counts as RISE or GBDI work when someone on it has a
`rise_since` and the publication is from that year or later.

It is the one fact in all of this that no file can work out for itself. An
author string says who wrote a paper, not who they worked for at the time,
and about half the publication list is work the team did before joining -
Galway, BPIE, Politecnico di Milano - which belongs on the site because it is
theirs. **Being attached to a project is deliberately not enough to count:**
some projects here ran before RISE existed, so that test would have called
2022 work RISE work.

Until at least one person has a `rise_since`, the filter does not render at
all. It never guesses.

**`cite_also`** is an optional list of earlier forms of a person's name, for
anyone who has published under more than one. Zuhaib carries
`cite_also: ["Zuhaib S"]`, because he published as Sheikh Zuhaib until 2022
and as Batra from 2024, under one ORCID. Author strings keep the form the
paper was published under, so without this half of someone's own work would
appear in the lists as a stranger's. Every form listed is underlined in the
publication lists exactly as `cite` is.

---
## 7. Add a partner

Create `_partners/short-name.md`:

```markdown
---
name: "Organisation name"
city: "City"
country: "Country"
type: "university"
website: "https://example.org"
logo: "short-name.svg"
---

Optional: a paragraph about the collaboration.
```

| Field | Required | Notes |
|---|---|---|
| `name` | yes | |
| `type` | yes | In use: `university`, `public authority`, `consultancy`, `foundation`, `network`, `international organisation`, `research institute`, `think tank`, `architecture practice`, `industry association`. Reuse an existing one where it fits |
| `city`, `country` | no | Shown under the name |
| `coords` | no | `[latitude, longitude]` - puts the partner on the world map. Leave it out and they appear in the table only |
| `website` | no | Their site. **Must be `website`, not `url`** - see the warning below |
| `logo` | no | A filename inside `assets/img/partners/` |

> **Never name this field `url`.** Jekyll reserves `url` for the page's own
> address and silently ignores a front matter field of that name. Every
> partner page once linked to itself for exactly this reason. The same applies
> to `path`, `id`, `date`, `content` and `collection`. `docs-check.py` now
> refuses them.

**22 of the 23 logos are the real thing.** Politecnico di Milano is still on
a placeholder - its name set in type - because no logo file was supplied.

To add or replace one: save the file as `<slug>.png` (or `.svg`) in
`assets/img/partners/`, matching the partner's filename, and set `logo:` in
the partner file to match. Three things worth knowing, all learned from the
first batch:

- **Convert CMYK JPEGs to RGB.** Browsers render them with wrong colours or
  not at all. BPIE's logo arrived this way.
- **Trim the built-in padding.** Many logo files ship with generous white
  space baked in, which makes them look shrunken beside marks that have none.
- **Resize to about 640px wide.** One file in the first batch was 5119px -
  far more than a 3rem-tall tile will ever use.

A partner appears on `/partners/` automatically. The home page shows a
**hand-picked** subset, listed in `index.md` - search for `assign shown`.

The **Together** column on `/partners/` counts what each partnership has
produced - projects, publications, news - and is calculated from the
cross-references, never typed in. A dash means none yet. If a number looks
wrong, the cause is a missing or misspelled reference on the project,
publication or post, not on the partner file.

**A post counts for a partner only when the post names them**, in its
`partners:` list. So when you write a news item, list the organisations it is
about - otherwise the partner's page will not show it and the column will read
as a dash. That is the whole mechanism; there is no inference from projects.

---

## 8. Add a news post or event

Create `_posts/YYYY-MM-DD-short-title.md`. **The date in the filename is the
publication date** - there is no date field. To change the date, rename the
file (which also changes its URL, so do it before publishing).

```markdown
---
layout: post
type: output
featured: false
title: "The headline"
summary: "One or two sentences. Shown in lists and on the home page."
projects:
  - project-filename
people:
  - martin-roeck
---

The body of the post.
```

| Field | Required | Notes |
|---|---|---|
| `layout` | yes | Always `post` |
| `type` | yes | `output`, `event`, `project` or `opening`. Shown as a small label |
| `title` | yes | |
| `summary` | yes | What appears in lists |
| `featured` | no | `true` pushes it to the front of the home page's three. Use sparingly - one at a time |
| `projects`, `people` | no | Filenames. The post then also appears on those pages |
| `partners` | no | Filenames. Use when a post is about a partner but not tied to one of their projects |

The home page shows three posts: any featured ones first, then the newest.
`/news/` shows all of them.

### Openings (`type: opening`)

A job advertisement needs more than a post. `/join/` lists every published
opening whose `deadline` has not passed, and the post layout prints the terms
in a box above the text. All of these are **required** once the post is
published; `docs-check.py` fails a published opening that is missing any of
them, and fails one that still carries the template's placeholder pay.

| Field | Example | Notes |
|---|---|---|
| `deadline` | `2026-11-30` | Applications close at the end of this day |
| `start` | `2027-02-01` or `"by agreement"` | |
| `duration` | `"2 years"` | |
| `hours` | `"40 h/week (100%)"` | |
| `location` | `"Vienna, Austria"` | |
| `pay_min` | `"EUR 3,500"` | Gross minimum pay |
| `pay_unit` | `month` / `week` / `hour` | |
| `pay_basis` | `"14 payments per year"` | Optional |
| `apply` | `office@riselabs.at` | Where applications go |

**Why the pay field is required.** An Austrian job advertisement must state
the minimum pay for the position with a time unit. Stating it is enough; a
willingness to pay more is optional. The layout renders it at the top of every
opening so it cannot be forgotten in the prose. Wording must also be
gender-neutral under the Equal Treatment Act. None of this is legal advice:
check the current guidance before publishing.

Start from `_posts/2026-10-05-example-open-position.md`, which is a template
and stays `published: false`.

**Deadlines go stale.** GitHub Pages rebuilds only on a push, so `/join/`
filters at build time *and* again in the browser from each item's `data-end`
attribute. Without JavaScript the build-time filter stands, so the page can be
a few days out of date but never badly wrong.

---

## 9. Images

Put them in the right folder:

| What | Where |
|---|---|
| Portraits | `assets/img/people/` |
| Partner logos | `assets/img/partners/` |
| Project heroes | `assets/img/` |
| Figures from a project | `assets/img/figures/` |
| Home page hero images | `assets/img/hero/` |

**Before uploading:**

- Resize. A hero wants about 2000px wide; a portrait about 800px square.
  A 6MB photo straight from a phone makes the page slow for everyone.
- Save as JPEG for photographs, PNG for screenshots, SVG for logos.
- Name it after what it shows, lowercase with hyphens.

Reference images with a path from the site root, starting with a slash:

```yaml
portrait: /assets/img/people/martin-roeck.jpg
```

### The picture shown when a link is shared

`_config.yml` sets a site-wide card at `/assets/img/social/rise-default.png`,
so every shared link has a picture. A page with its own picture sets **both**
`hero:` and `image:`, with the same path:

```yaml
hero: "/assets/img/projects/indicate-life-map.png"
image: "/assets/img/projects/indicate-life-map.png"
```

The duplication is deliberate. `jekyll-seo-tag` reads `image` and knows
nothing about `hero`, and writing the Open Graph tags by hand in
`default.html` would duplicate the ones the plugin already emits. A second
field is the cheaper of the two, and `docs-check.py` notes any page that sets
`hero` without `image`.

**The three home page hero images** are listed in `_data/hero.yml`, one per
pillar. To swap one, upload the new image and change the filename there.

Two rules for hero images, both learned by getting them wrong:

- **Crop to roughly 2.2:1 before uploading.** The hero is a wide band. A
  portrait photo gets cut to a thin horizontal strip by the browser, and it
  will not be the strip you wanted.
- **Put the subject in the middle third, vertically.** The hero darkens
  sharply toward the bottom so the text stays readable, which means anything
  in the lower part of the frame disappears.

A pale photograph under the navy wash can also read as an empty gradient;
lifting its contrast before uploading helps.

---

## 10. Edit the fixed pages

Home, Approach and Services are in the repository root: `index.md`,
`approach.md`, `services.md`.

These pages are written in **HTML paragraphs**, not Markdown - the text sits
inside `<p>` tags:

```html
<p>A paragraph of text on the Approach page.</p>
```

This is deliberate and necessary. Jekyll does not convert Markdown inside
HTML blocks, and these pages are built from HTML sections - so Markdown
written here appears on screen as raw syntax. When editing, keep text inside
its `<p>` tags, and for a link write:

```html
<a href="https://example.org">the link text</a>
```

Project, publication, person, partner and news bodies are **ordinary
Markdown** - §12 applies there, not this.

Legal pages: `impressum.md` and `datenschutz.md`. The Impressum's details come
from `_data/impressum.yml`. Edit that file, not the page. **Check with Martin
before changing either** - both carry legal obligations, and the privacy
policy in particular describes exactly what the site does. Adding anything
third-party (an embedded video, a map, analytics, a social widget) makes it
inaccurate and requires a new section, usually a cookie banner too.

---

## 11. Services, engagement and testimonials

All three are in `_data/`, not pages.

**`_data/engagement.yml`** - the four ways work with RISE actually starts.
Each entry has an `id` (used only for the anchor; keep it stable), a `title`,
a `body`, a `subject` that prefills the mail link on the home page card, and
`examples`: two project slugs.

`examples` is the part that matters. Each card names two projects that began
that way, linked to their pages under their `short_title`, so a visitor can
check the claim in one click. `docs-check.py` fails a slug with no project
behind it, and notes a card with fewer than two. **If a card has no examples
to give, question the card, not the line** - the four here replaced an older
set in which two modes had nothing on the site behind them.

One file, two places: the "Work with us" band on the home page renders them
as cards, `/expertise/` renders the same four as a findings list, both through
`_includes/engagement.html` with `style="cards"` or `style="list"`. The
wording used to live on the expertise page alone, which let the home page say
something vaguer and let the two drift. **Edit the data file, never the
pages.**

**`_data/services.yml`** - each block has `title`, `strand` (`up`, `wide` or
`deep`, which links back to the Approach page), `lede`, a list of `includes`,
an `example` (a project filename, whose title and summary are pulled in
automatically), `audience`, and an optional `note`.

**`_data/testimonials.yml`** - each quote needs a unique `id`, the `quote`
verbatim, `name`, `role`, `org` and a `context` line giving the source and
date.

The home page shows three, chosen by id in `index.md`:

```liquid
{% include testimonials.html only="brigitte-jacquemont,xavier-le-den,simone-kongsbak" %}
```

The order in that list is the order on screen. Remove the `only=` part to show
all of them.

**Before publishing a new testimonial**, get the person's agreement in
writing. It names an identifiable person and their employer in a commercial
context. Attribute them with the role they held **when they said it**, not
their current job - implying a present employer endorses RISE when they
haven't is both misleading and the kind of thing people object to.

---

## 11c. The six facts on the home page

The "What the evidence says" band reads `_data/facts.yml`. Nothing on that
band is written into `index.md`, so the page and `docs-check.py` read the same
source and cannot disagree.

```yaml
- perspective: "Europe"            # the small label above the figure
  value: "8.5 billion tonnes CO₂e" # the large figure
  say: >-                          # what it means, one or two sentences
    What EU buildings and construction must avoid from 2020 to 2050 …
  sources:                         # one or more
    - label: "Alaux et al., 2026, Nature Communications"
      publication: alaux-2026-context-specific-life
```

Three rules, and the checker enforces the third:

1. **Every figure is published, has a DOI, and is on this site.** The
   `publication` slug is a file in `_publications/`, and the band builds the
   link from it. A number nobody can follow to a paper does not belong here.
2. **A source that is not peer-reviewed says so in its label**, as the VELUX
   green paper does: "Toth et al., 2026, green paper (not peer-reviewed)".
3. **A slug with no file behind it fails the check.** It would otherwise
   render as a dead link under a headline figure, which is worse than showing
   no figure at all.

Several of the sentences continue the figure rather than starting after it -
"50-107 million homes *could be created within Europe's existing buildings*" -
which is why the figure and the sentence are one paragraph in the markup and
not two boxes. Write `say` to follow on from `value` or to stand alone, and it
will read correctly either way.

A fact with two sources lists both, joined with a semicolon. Six is what the
grid is built for: three columns on a laptop, two on a phone.

---

## 11a. The "Page in progress" note

The magenta pill in the bottom corner, next to the theme toggle, is switched
on per page: `wip: true` in that page's front matter. It is on the home page
only at the moment.

Remove the line when the page is finished. There is no site-wide switch, on
purpose - a disclaimer that nobody can remember how to turn off tends to stay
up for a year.

---

## 11b. Light and dark

Dark is the primary theme and what every page loads with. The toggle in the
bottom corner switches that page to light. Nothing is stored on the visitor's
device, so the choice resets when they move to another page - a deliberate
trade for storing nothing.

Colour is set in two layers at the top of `assets/css/style.css`: the brand
constants from the CI manual, which never change, and the semantic tokens the
theme swaps. **If you change a colour, change a token - never a value inside
a rule**, or it will be right in one theme and wrong in the other.

The hero is dark in both themes, which is why its text colours are pinned
rather than inherited.

---

## 12. Writing text: formatting that works

In project, publication, person, partner and news **bodies** (not the fixed
pages - see §10):

```markdown
## A heading

Ordinary text. Blank line between paragraphs.

**Bold** and *italic*.

- A bullet
- Another bullet

[Link text](https://example.org)
```

A bare URL on its own becomes a link automatically.

House style, from the existing pages: sentence case in headings, en dashes
(–) in year ranges, British spelling, and no full stop at the end of a
`summary` line.

---

## 13. Checklist before publishing

- [ ] Filename is lowercase with hyphens and ends `.md`
- [ ] The file starts with `---` on line 1
- [ ] Every title containing a colon is in double quotes
- [ ] Every cross-reference matches a real filename, exactly
- [ ] Images uploaded, resized, and paths start with `/assets/`
- [ ] A hero photo actually shows this project
- [ ] `published: false` removed when ready
- [ ] `python3 docs-check.py` prints `no problems found`
- [ ] After the build goes green, open the live page and read it

---

## 14. When something goes wrong

**A page didn't appear.** Check for `published: false`. Check the file is in
the right folder and ends `.md`. Check the build under **Actions**.

**A connection didn't appear** - a publication missing from a project page,
say. The reference doesn't match a filename. Compare them character by
character; run `docs-check.py`.

**The build failed** (red cross under Actions). Click it and read the error.
Nine times out of ten it is an unquoted colon in a title. The previous version
stays live, so the site is never down because of this.

**Markdown is showing as raw syntax.** You are editing one of the fixed pages
- see §10.

**Something broke and you want it back.** Every change is reversible. Open the
file on github.com, click **History**, find the version before the change, and
restore it. Nothing is ever lost.

**Still stuck.** Note what you changed and what you expected, and ask. A
broken page in a branch costs nothing; a wrong claim on a live page costs
more.

---

## 15. Images are not optional

**Every project, publication and post should carry at least one image.** The
checker reports how many do not, grouped by kind, so the gap stays visible.

What each kind wants:

| Kind | What to show |
| --- | --- |
| Project | The intervention logic, or the key result. A diagram of what the project actually did beats a stock photograph |
| Publication | A selection of figures from the paper itself |
| Post | For a project or paper, reuse one of its figures. For an event, a photograph of the room or the people |

Three fields do this, and they work the same on projects, publications and
posts:

```yaml
hero: /assets/img/figures/my-figure.png
hero_caption: "What it shows. Source, licence if someone else's."
figures:
  - file: /assets/img/figures/another.png
    number: Figure 2
    caption: What this one shows.
    source: Where it came from.
```

`hero` is the one at the top. `figures` is the list further down. You can also
write a `<figure class="fig">` straight into the body if it needs to sit at a
particular point in the argument - the CollaborativeCarbon project does this.

**When asking a partner or a project for material, ask for the figures at the
same time**, and ask what licence they come under. Agora's figures are CC BY
4.0 and can be reused with attribution; most publishers' are not. A caption
naming the source is the minimum.

## 16. Cite this

Publication pages build a citation block automatically from their front
matter.

**Project pages do not, and should not.** A project is not a citable work.
Most of them were done with partners, so a citation line on the page invites
a reader to cite RISE for work RISE contributed to rather than authored. A
citation needs authors, a venue and ideally a DOI, which is what a
publication has and a project does not.

If a project produced something citable - a report, a dataset, a paper - then
that output is the citable thing, and it belongs in `_publications/` with its
own citation. It will then appear on the project page by itself, under
"Publications on this project", because publications name the projects they
came from.

`docs-check.py` fails any `cite_*` field left in a project file, so this
cannot quietly come back.

## 17. Data & tools

`/tools/` is not a new kind of content. It shows the publications whose
`kind` is `data`, because a dataset listed as the fourth section of a
publications page is effectively buried. Two optional fields in those files
appear on the cards:

```yaml
state: "available"              # or "in development"
repo: "https://github.com/..."  # where the source lives
```

To add a dataset or a tool, add a publication with `kind: data`. It appears in
both places automatically.

## 18. Navigation

The menu is built from the `nav` block in `_config.yml`. An entry with a `url`
is a plain link; an entry with `items` is a group that opens a panel. Groups
exist so the bar stays on one line on a phone.

A group whose items are all hidden is skipped rather than rendered as a dead
button - which is what happens to About while the team page is hidden.
