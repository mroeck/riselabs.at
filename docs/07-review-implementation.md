# Review implementation spec

Source: website review of 29 October 2026, comparing riselabs.at with Smith
Innovation, Bauhaus Earth, Eunomia and Carlson Lab. Full review:
https://claude.ai/artifact/9uJmDgQqD4YnrDgB7nsGX4

This file is the work order for whoever implements the review, human or AI.
Put it in `docs/` next to `04-roadmap.md`. Work through the phases in order.
Each task names the files, the change, the human input it needs, and how to
tell it is done.

---

## 0. Rules for the implementer

These override anything below that seems to conflict with them.

1. **Keep the existing contracts.** `docs/03-editing-the-site.md`,
   `docs/05-design-basis.md` and `docs/06-core-collaborators.md` still apply.
   In particular: colours only through semantic tokens, no third-party scripts
   or fonts, no hex values inside component rules. One exception, decided
   29 October 2026: the Plausible analytics snippet (R10), loaded only in
   production and only together with the approved Datenschutz text.
2. **Invent nothing that carries a name, a number or a DOI.** No bios, no
   abstracts, no quotes, no figures, no event dates, no licences. Where content
   is missing, leave the field empty or keep `published: false`, and add the
   item to the "Human input" list at the end of this file.
3. **Run `python3 docs-check.py` before every commit.** Extend the checker
   whenever a task adds a field (see each task). "no problems found" is the
   bar.
4. **One branch and pull request per phase.** Title it `Review P<n>: <topic>`.
   Describe in the PR which acceptance criteria were checked and how.
5. **Check rendering.** Before merging, look at every changed page at 375 px
   and at 1280 px wide, in dark and in light theme, and tab through it with the
   keyboard.
6. **Consent before people.** No person page or portrait is published until the
   person has approved the exact text, as described in `docs/06`.
7. **Update the docs you change.** A new field goes into `docs/03` (the table
   for that content type) and `docs/02` if it changes what links to what. Tick
   off roadmap items in `docs/04` when done.

---

## Phase P1: fixes (small, no new design)

### P1.0 Make https://riselabs.at work (do this first)

- **Problem:** on 29 October 2026, https://riselabs.at/ and
  https://www.riselabs.at/ showed a browser certificate error ("Privacy
  error") in Chrome, while http://riselabs.at/ loaded and other https sites
  loaded normally. The site's own `canonical` and `og:url` point to
  `https://riselabs.at/`, so search engines and every shared link lead to
  the warning.
- **Change (needs repository admin rights, H0):**
  1. GitHub → repository Settings → Pages → Custom domain: confirm it reads
     `riselabs.at` (matching `CNAME` in the repo) and that the DNS check
     passes.
  2. At the DNS provider: the apex `riselabs.at` needs exactly the four
     GitHub Pages A records (185.199.108.153, 185.199.109.153,
     185.199.110.153, 185.199.111.153), optionally the matching AAAA
     records, and no other A/AAAA/CNAME records on the apex. `www` needs a
     CNAME to `mroeck.github.io`. Remove anything else on those names,
     including leftovers from a previous host.
  3. If the DNS was already right, remove and re-save the custom domain in
     the Pages settings; GitHub then requests a new certificate.
  4. When the certificate is issued, tick "Enforce HTTPS".
- **Done when:** https://riselabs.at/ and https://www.riselabs.at/ load
  without a warning, and http:// redirects to https://. Record the date in
  `docs/01-publishing-on-github.md`.

### P1.1 Merge the duplicate green paper

- **Files:** `_publications/toth-2026-housing-need-future.md`,
  `_publications/toth-2026-housing-we-need.md`
- **Problem:** the same publication appears twice. One entry has DOI
  `10.5281/zenodo.21030392`; the other has `note: "Published 3 July 2026. No
  DOI assigned."` Both show on the homepage.
- **Decision (Martin, 29 Oct 2026):** same document; list it once, with the
  Zenodo DOI.
- **Change:** keep `toth-2026-housing-we-need.md` (it carries the summary
  text, the project link and the partners). Set
  `doi: "10.5281/zenodo.21030392"`, delete the `note` line, keep the VELUX
  PDF as `url_external`, and use the title in sentence case like the other
  entries: "The housing we need for the future we want". Delete
  `toth-2026-housing-need-future.md` and add a redirect from its URL (P4.2
  mechanism; until then a plain delete is acceptable).
- **Author list:** the two files spell one author differently
  ("Reimer Bjørkskov KB" and "Bjørkskov KBR"). Use the form on the Zenodo
  record; if it cannot be checked, ask (H1).
- **Done when:** one entry on `/publications/`, on the homepage and on
  `/projects/reliving-scaling-renovation/`; the `note` no longer contradicts
  the DOI.

### P1.2 Remove "Page in progress" from the homepage

- **File:** `index.md` – delete `wip: true`.
- **Done when:** the live homepage shows no WIP label. The mechanism stays for
  pages that really are unfinished.

### P1.3 Unpin the past event

- **File:** `_posts/2026-10-12-wlc-network-closing-event-brussels.md` – set
  `featured: false` (the event was on 21 October 2026).
- **Done when:** homepage "Latest" shows the three newest posts. P3.2 makes
  this automatic.

### P1.4 Social preview image

- **Files:** `_config.yml`, `_layouts/default.html`, `assets/img/social/`
- **Problem:** no `og:image`, so links shared on LinkedIn and Bluesky show no
  picture; `twitter:card` is `summary`.
- **Change:**
  - Add a 1200 × 630 px default image (navy background, white RISE logo,
    tagline) at `assets/img/social/rise-default.png`. Build it from the
    existing logo files; no new artwork.
  - Set `image: /assets/img/social/rise-default.png` in `_config.yml`
    (jekyll-seo-tag reads it).
  - For project pages and posts, use the page's `hero` as the social image.
    jekyll-seo-tag only reads `image`, so either set `image` alongside `hero`
    in each file and make `docs-check.py` warn when `hero` is set without
    `image`, or emit the meta tags yourself in `default.html` and make sure they
    are not duplicated. Pick one, and document it in `docs/03`.
  - Use `summary_large_image` wherever an image is present.
- **Done when:** the page source of `/`, one project and one post each carry
  exactly one `og:image` and one `twitter:image`, with absolute https URLs.

### P1.5 Source the floor-area figure

- **File:** `approach.md`, section "Growth, and what follows it"
- **Problem:** "global floor area is projected to rise by up to 150% by 2050,
  which is roughly five billion square metres of new building every year"
  has no source, on a site that argues for reproducibility.
- **Change:** link the source Martin names (H2). If none is confirmed, reword
  so the sentence carries no number.
- **Done when:** the figure has a link, or no figure remains.

### P1.6 Make the INDICATE LIFE facts agree

- **Files:** `_projects/indicate-life.md`, `approach.md`,
  `assets/img/projects/indicate-life-map.png`
- **Problem:** the hero image reads "2024 – 2026" while `years` says
  "2024–2027" (also on the homepage). `hero_caption` lists Croatia; the
  `partners_note`, the body and `approach.md` list only Austria, Hungary,
  Italy and Luxembourg.
- **Decision (Martin, 29 Oct 2026):** INDICATE LIFE ends in 2026; Croatia
  is part of it. The hero image is therefore correct.
- **Change:**
  - `_projects/indicate-life.md`: `years: "2024–2026"`; add Croatia to
    `partners_note` and to the country list in the body, in alphabetical
    order: "Austria, Croatia, Hungary, Italy and Luxembourg".
  - `approach.md` ("Scaling wide"): the same five countries.
  - In January 2027, set `status: "concluded"`, so it leaves "Current
    projects".
- **Done when:** "2024–2026" and the five countries appear identically on
  the project page, the homepage and `/approach/`.

### P1.7 Ready for the job posts (deadline: before the posts go out, week of 2 Nov 2026)

RISE issues job posts in the first week of November 2026. Applicants will
look at the site, so these must be live first: P1.0 (https), P1.1, P1.2,
P1.6, this task, and P2.1 with at least Martin and Barbara on the team page.

- **Files:** new `join.md`, `_config.yml` (nav), `_layouts/post.html`,
  `_posts/2026-10-05-example-open-position.md` (template), `docs/03` § 8,
  `docs-check.py`
- **Join page:** `/join/`, in the nav under About, directly after Team.
  It lists every published post with `type: opening` whose `deadline` has not
  passed (build-time filter plus the `data-end` script described in P3.1),
  newest first. Below the list, a short standing paragraph (H9); until it
  exists, only this line: "Write to office@riselabs.at if you want to hear
  about future openings."
- **Opening fields** (all required for `type: opening`; `docs-check.py`
  fails a published opening that lacks any of them):

  | Field | Example | Notes |
  | --- | --- | --- |
  | `deadline` | `2026-11-30` | Applications close at the end of this day |
  | `start` | `2027-02-01` or "by agreement" | |
  | `duration` | "2 years" | |
  | `hours` | "40 h/week (100%)" | |
  | `location` | "Vienna, Austria" | |
  | `pay_min` | "EUR x,xxx" | Gross minimum pay; the real figure comes from Martin |
  | `pay_unit` | `month` / `week` / `hour` | |
  | `pay_basis` | "14 payments per year" | Optional |
  | `apply` | `office@riselabs.at` | Where applications go |

- **Legal note for the template text (Austria; not legal advice):** a job
  advertisement must state the minimum pay for the position, with a time unit
  (hour, week or month). Employers without a collective agreement state the
  pay they intend as the minimum basis for negotiation. "Gehalt ab EUR …
  brutto" with the minimum is sufficient; a willingness to pay more is
  optional. A first breach draws a warning, later breaches a fine of up to
  EUR 360 ([WKO](https://www.wko.at/oe/einstellen/angabe-mindestentgelts-stelleninserat)).
  The Equal Treatment Act also requires gender-neutral wording; confirm the
  current text with the Gleichbehandlungsanwaltschaft guidance before
  publishing. The post layout renders `pay_min` and `pay_unit` in a facts
  box at the top of every opening, so the statement can never be left out.
- **Template:** rewrite the example opening so its "Terms" placeholder
  becomes the front-matter fields above, and keep `published: false` on the
  template itself.
- **Human input:** the real openings (title, text, fields) (H15).
- **Done when:** `/join/` shows an opening built from the template in a
  local build, with a pay line at the top; and `docs-check.py` fails when
  `pay_min` is removed from a published opening.

---

## Phase P2: people and publications

### P2.1 Publish the team page

The people: Martin Röck, Barbara Droste-Luckmann, Nicole Di Santo, Zuhaib
Batra. Martin is ready. The other three are not (H3–H5).

- **Files:** `_config.yml`, `team.md`, `_people/*.md`,
  `_includes/peoplelist.html`, `assets/css/style.css`, `docs/06`
- **Change:**
  1. Follow the "To bring it back" note in `_config.yml`: set
     `team_page: true`, remove `published: false` from `team.md`, and put
     `Team` back in the nav as the **first** item under About.
  2. Replace the two-section layout in `team.md` with **one grid headed
     "Team"**, ordered: `group: rise` first, then `group: collaborator`, each
     by `order`. Under the grid, one plain sentence: "Team members employed
     elsewhere are shown with their employer."
  3. Every card shows the affiliation: "RISE" for `group: rise` (Martin,
     Barbara; Barbara's employment confirmed 29 Oct 2026), and
     "Core collaborator · <org>" for `group: collaborator` (Nicole and Zuhaib,
     "Core collaborator · GBDI · EPFL"). Keep `group` and `org` as they are.
     Do **not** relabel Nicole or Zuhaib as RISE; that changes only when their
     contracts do (H6). Their profile drafts are being prepared by Martin and
     stay `published: false` until each has approved the text.
  4. Update `docs/06-core-collaborators.md`: the combined grid with a visible
     employer line replaces the separate "Core collaborators" heading. The
     reasoning in that file stands.
  5. A person whose file still has `published: false` does not appear. Do not
     remove that line for anyone until H3–H5 are answered.
- **Done when:** `/team/` is in the nav, shows Martin now and the others as
  they are approved, every card shows an employer, and `docs-check.py` passes.

### P2.2 Card and profile content (Smith and Carlson patterns)

- **New person fields** (add to `docs/03` § 6 and the template
  `_people/example-colleague.md`):

  | Field | Type | Shown | Notes |
  | --- | --- | --- | --- |
  | `tagline` | string, max 120 characters | Card and profile | One line on why they do this work, in their own words |
  | `works_on` | list of theme slugs from `_data/themes.yml` | Profile, as chips; plain text until the theme pages of P5.1 exist, then linked to them | Closed vocabulary; `docs-check.py` must reject unknown slugs |

- **Card** (`_includes/peoplelist.html`): square portrait (1:1, `object-fit:
  cover`), name, role, employer line, tagline, then a row of small links
  (email, ORCID, Google Scholar, LinkedIn, Bluesky) taken from `email` and
  `links`. Without a portrait, show the person's initials on a token-coloured
  square. Never use a stock photo for a person.
- **Profile** (`_layouts/person.html`): the tagline as the lede (it replaces
  `summary` there; keep `summary` for lists elsewhere), then the body, then
  "Works on" chips, then the existing related projects, publications and news.
- **Portrait alt text:** the person's name on the profile; empty on cards,
  where the name is printed next to it.
- **Done when:** Martin's card and profile render with all elements at
  375 px and 1280 px, in both themes.

### P2.3 People on the homepage

- **File:** `index.md`
- **Change:** a band "The team" after "Current projects": the published
  people's cards in compact form (portrait, name, role), linking to `/team/`.
  Hide the band when fewer than two people are published.
- **Done when:** the band appears once two people are published and links to
  `/team/`.

### P2.4 A named contact on every project

- **Files:** `_layouts/project.html`, `_projects/*.md`, `docs/03` § 4
- **Change:** optional field `contact:` (a person slug). If absent, use the
  first entry in `people:` that has an `email`. Render a "Contact" row at the
  end of the facts box: name (linked to the profile), role, email. Show nothing
  when no person qualifies.
- **Done when:** every project with Martin in `people:` shows a contact row;
  `docs-check.py` rejects a `contact:` slug that does not exist.

### P2.5 Publication entries with image and download (Carlson pattern)

- **New publication fields** (add to `docs/03` § 5 and `docs-check.py`):

  | Field | Type | Meaning |
  | --- | --- | --- |
  | `date` | YYYY-MM-DD | Publication date; used for sorting. Keep `year` |
  | `thumbnail` | path | `assets/img/pubs/<file>.webp`, 4:3, 480 × 360 px |
  | `thumbnail_credit` | string | Required when the image is not RISE's own |
  | `open_access` | true / false | Shows an "Open access" badge |
  | `licence` | string, e.g. `CC BY 4.0` | Required before a PDF is hosted here |
  | `pdf` | path or URL | Local file in `assets/pdf/` or a repository URL |
  | `data` | URL | Dataset (Zenodo, etc.) |
  | `code` | URL | Code repository |
  | `preprint` | URL | Preprint or accepted manuscript |

- **Hosting rule:** host a PDF in the repo only when `licence` permits it
  (a CC licence, or the publisher allows the accepted manuscript). Otherwise
  link to the publisher, Zenodo or the institutional repository. Keep any
  single PDF under 20 MB; larger files go to Zenodo.
- **Thumbnail rule:** in order of preference, (a) a figure RISE made, (b) page 1
  of an openly licensed PDF, rendered by a script, (c) a plain tile with
  the publication kind in text. Never a journal cover or a publisher's graphical
  abstract unless the licence allows it.
- **What to take from Carlson Lab, and what not:** their publications page
  (checked 29 Oct 2026) is a card grid: page 1 of the paper as the image,
  then title, journal and date; topic chips filter it; a preprint table
  (title, server, date) with a lab-member filter sits above it. Take the card
  grid, the topic chips (use RISE's themes) and a "filter by person" select
  built from `people:`. Do not copy two things: the cards open publisher
  PDFs of closed-access papers (for example *Science*) hosted on Google
  Drive, which the hosting rule above forbids; and the list is an embedded
  third-party app (Softr) in an iframe, which `docs/05` rules out. Build it
  natively in Liquid.
- **Script:** add `make-thumbnails.py` (excluded in `_config.yml` like the
  other scripts). It renders page 1 of every local PDF whose publication has no
  `thumbnail` to a 480 × 360 webp, and prints what it did. Use `pdftoppm` or
  PyMuPDF; nothing is fetched at page load.
- **Entry layout** (`_includes/pubitem.html`): thumbnail on the left
  (120 px wide on desktop, above the text on phones), the citation on the
  right as now, and below it a row of buttons: `PDF ↓` (with the `download`
  attribute for local files), `DOI`, `Data`, `Code`, `Preprint`, `Cite`
  (copies the citation, reusing the `data-citeas` script). Show only the
  buttons whose fields are filled. "Open access" as a small badge after the
  venue.
- **Listing** (`publications.md`, `_includes/publist.html`): sort by `date`
  (fall back to `year`) within each kind section. Add kind buttons (All,
  Articles, Books, Reports, Data) next to the existing text filter, using the
  same no-JS fallback pattern as the project theme filter.
- **Publication page** (`_layouts/publication.html`): thumbnail at the top
  when present; the abstract under the facts; the same action buttons.
- **Done when:** a publication with every field filled, and one with none of
  the new fields, both render correctly in the list, on the homepage and on
  their own page.

### P2.6 Abstracts

- **Change:** run `python3 fetch-abstracts.py` (report), then
  `python3 fetch-abstracts.py --write` on a machine with network access.
  Review the diff. Do not write or condense abstracts by model; roadmap item 2
  says why.
- **Human input:** a person runs the script and reads the diff (H7).
- **Done when:** every publication with a DOI that Crossref or OpenAlex
  knows has its abstract; the script's "not found" list goes into the PR.

### P2.7 Homepage publications

- **File:** `index.md`
- **Change:** "Recent publications" sorts by `date` and shows the new entry
  layout with thumbnails, three entries instead of four.
- **Done when:** the three most recent by date show, with no duplicates.

### P2.8 Less text, more pictures on the homepage

Checked in the browser on 29 October 2026: below the hero, the homepage is
text from top to bottom (Latest, publications, projects, three long
testimonial cards); the only pictures are partner logos.

- **File:** `index.md`
- **Change:**
  - "Current projects": use `_includes/projectgrid.html` (the image cards
    already on `/projects/`) for the three most recent current projects,
    instead of the text list.
  - In every citation list, show the DOI as a short `DOI` link, not the full
    `https://doi.org/...` URL as link text (P2.5 does this in
    `pubitem.html`).
  - Latest: show the post's `hero` as a small image when it has one.
- **Done when:** each homepage band after the hero, except "What we stand
  for" and the closing calls to action, carries at least one image.

---

## Phase P3: action and co-creation

### P3.1 Event fields and the events page (Bauhaus Earth pattern)

- **New post fields for `type: event`** (add to `docs/03` § 8 and the
  checker):

  | Field | Type | Notes |
  | --- | --- | --- |
  | `event_start` | YYYY-MM-DD, optional time | Required for events |
  | `event_end` | YYYY-MM-DD | Defaults to `event_start` |
  | `location` | string | "Brussels, Belgium" or "Online" |
  | `format` | `in person` / `online` / `hybrid` | |
  | `register_url` | URL | Shown until `event_end` |
  | `materials` | list of `{title, url}` | Slides, recording, report; shown after the event |

- **Events page** (`events.md`): "Upcoming" (soonest first) above "Past"
  (newest first, grouped by year). Each item shows the date and the place in
  bold before the title, a "Register" button while upcoming, and the
  materials links once past.
- **Staleness:** GitHub Pages rebuilds only on push, so a build-time split
  goes stale. Render every event with `data-end="<event_end>"` and let a
  few lines in `assets/js/ui.js` move items whose end date has passed into
  "Past" on load. Without JavaScript the build-time split stands. No external
  requests.
- **Backfill:** add the fields to the six existing event posts using the
  dates and places already written in their bodies. Where a body gives no
  date, leave the field empty and list it under H8.
- **Done when:** the Brussels event shows under Past and the COP31 session
  under Upcoming (if its date is known), with and without JavaScript.

### P3.2 "Coming up" on the homepage

- **File:** `index.md`
- **Change:** a "Coming up" band above "Latest" with the next two upcoming
  events (date, place, title, Register). Hide it when nothing is upcoming.
  For `type: event`, `featured: true` only counts while `event_end` is in the
  future, which makes P1.3 automatic.
- **Done when:** a past featured event no longer leads "Latest".

### P3.3 "Work with us" on the homepage

- **Files:** new `_data/engagement.yml`, `index.md`, `expertise.html`
- **Change:** move the four ways of working (commissioned work, research
  partnership, independent review, teaching and facilitation) out of
  `expertise.html` into `_data/engagement.yml`, unchanged in wording, and
  render them in both places from that file. On the homepage they replace the
  current "Work with us" band: four cards, each ending in a mail link with a
  prefilled subject, e.g. `mailto:office@riselabs.at?subject=Independent%20review`.
  Put a "Get in touch" link in the hero next to "Our approach".
- **Done when:** the four modes show on the homepage and on `/expertise/`
  from one data file, and each card's link opens a mail with the right subject.

### P3.4 Join page: moved

Now P1.7, because job posts go out in the first week of November 2026.
Here, only the follow-up: once the standing text (H9) exists, add a
"Join us" link to the homepage "Work with us" band.

### P3.5 Testimonials tied to work

- **Files:** `_data/testimonials.yml`, `_includes/testimonials.html`,
  `index.md`, `_layouts/person.html`
- **Change:** add `about: person | work` and an optional `project:` slug to
  each entry. The five LinkedIn recommendations become `about: person` and
  render on Martin's profile, with their `context` line unchanged. The homepage
  shows only `about: work` quotes, linking to the project; if there are none,
  the band does not render. Do not publish the Rodríguez Droguett quote until
  her consent is confirmed (H10).
- **Done when:** the homepage carries no personal recommendations, and
  Martin's profile carries all five.

---

## Phase P4: imagery and polish

### P4.1 Own imagery instead of stock

- **Files:** `_data/expertise.yml`, `_data/stock.yml`, `assets/img/`
- **Change:** replace each `/assets/img/stock/*` image on `/expertise/` with
  a RISE photograph or a RISE figure. Candidates already in the repo:
  `assets/img/projects/eu-stock-by-country.png` (stock modelling),
  `eu-ecb-boxplot.png` (benchmarking), `gbdi-platform.png` (open data),
  `hero/indicate-community.jpg` (teaching). Add `image_credit` where the
  photographer is not RISE. Figures sit on white cards, as `docs/05`
  prescribes.
- **Human input:** event and workshop photos with permission to publish
  (H11).
- **Done when:** no `/assets/img/stock/` path is referenced by
  `expertise.yml`.

### P4.2 Clean project URLs

- **Files:** `_projects/supporting-the-development-of-a.md`,
  `analysis-of-life-cycle-greenhouse.md`,
  `towards-embodied-carbon-benchmarks-for.md`, `_config.yml`
- **Change:** rename to short, readable slugs (H12 confirms names). Add
  `jekyll-redirect-from` to `plugins` (check that the pinned `github-pages`
  gem includes it) and a `redirect_from:` entry with the old URL in each
  renamed file. Update every reference to the old slugs (`related`,
  `projects`, `examples` in `_data/expertise.yml`).
- **Done when:** old URLs redirect, new URLs work, `docs-check.py` passes.

### P4.3 Remaining roadmap items

Finish the open items in `docs/04-roadmap.md` § 3: Politecnico di Milano and
the ten missing partner logos, the light-mode check of photographs, and the
two unconfirmed partner websites.

---

## Phase P5: optional

- **P5.1 Theme pages** (Smith): `/themes/<slug>/` for each entry in
  `_data/themes.yml`, collecting its projects, publications and posts. Link
  the theme tags on project pages to them.
- **P5.2 One German page** at `/de/`: who RISE is and the four ways of
  working, in German, linked from the footer. Not a full translation.
  Text from Martin (H13).
- **P5.3 Evidence strip** (Eunomia): a row of counts on the homepage,
  computed in Liquid from the collections (projects, publications, partner
  countries). Never typed by hand.

---

## Phase L: layout and visual appeal

Source: layout and appeal review of 29 October 2026, comparing the live
site with the same four references in the browser:
https://claude.ai/artifact/SUKCW8k7e8Vth1tPWxTqg9

Section 0 applies in full. In particular: colours only through the semantic
tokens in `docs/05`, the hero stays dark in both themes, figures and logos
sit on white cards unless a task below says otherwise, no third-party fonts
or scripts. Measure before and after every change (page height at 1,280 px
and 390 px, screenshots in both themes) and put the numbers in the PR.

Order: L1 now (one line, before next week's job posts). L2–L5 together as one
PR, because they share the homepage. The rest in any order. L3 depends on
photos (H16).

### L1 Fix the missing page-head gutter (do this first)

- **File:** `assets/css/style.css`, line 453.
- **Problem:** `.page-head { padding: 2.5rem 0 1rem; }` sets the left and
  right padding to 0, overriding `.wrap { padding: 0 1.5rem; }` on the same
  element. On phones every inner page's title and lede touch the screen
  edge (measured: title at 0 px, body text at 24 px). On desktop the title
  sits 24 px left of the body text (313 px vs 337 px at 1,280 px).
- **Change:** `.page-head { padding-top: 2.5rem; padding-bottom: 1rem; }`.
- **Done when:** at 390 px the `h1`, `.lede` and first body paragraph of
  `/projects/`, `/publications/` and `/team/martin-roeck/` share one left
  edge at 24 px; at 1,280 px they share one left edge too.

### L2 Homepage order and bands

- **File:** `index.md`, `assets/css/style.css`
- **Change:** reorder to seven bands:
  1. Hero (L8)
  2. Current projects: the three most recent `status: "current"` projects
     as image cards via `_includes/projectgrid.html` (replaces P2.8's first
     bullet), "All projects →"
  3. What we stand for, with "How we work →" and "What we do →" as its two
     links (this absorbs the old "onward" band)
  4. Team (L3)
  5. Latest and Recent publications side by side from 1,024 px (two
     columns, three items each, posts with a small image or date tile per
     L13, publications in the P2.5 entry layout); stacked on phones
  6. Partners and quotes (L7, L9) on one `--surface` band
  7. Work with us (the four modes from P3.3) with the newsletter form as its
     last row
- **Done when:** the homepage has seven bands; page height at 1,280 px and
  390 px is reported before and after in the PR; no band is a plain text
  list.

### L3 Portraits and the team band (Smith, Eunomia, Bauhaus Earth)

- **Files:** `index.md`, `_includes/peoplelist.html`, `team.md`,
  `_layouts/project.html`, `assets/img/people/`, `docs/03` § 9 (images)
- **Decision (Martin, 29 Oct 2026):** black and white, until harmonised
  headshots of all team members exist.
- **Photo rule (write it into `docs/03`):** every portrait renders in black
  and white through CSS, not by converting the files: add
  `filter: grayscale(1)` to `.portrait` and the portrait images in
  `_includes/peoplelist.html`, behind one class (for example
  `.people-bw` on `<body>`, set from `_config.yml` as
  `portraits: bw`), so it can be switched off in one place once the
  harmonised headshots arrive. Keep the original files in colour. Square
  1:1 crop, at least 800 × 800 px, head and shoulders. A person with no
  photo yet gets an initials tile; a person with any approved photo uses it,
  cropped square and shown in black and white.
- **Homepage team band:** the published people as a row of large portraits
  (about 240 px wide on desktop), name, role, affiliation line (P2.1). One
  short quote from one person in display size beside the row is optional
  (Smith).
- **Team page:** a group photo as the page header when one exists (Bauhaus
  Earth, Carlson Lab); otherwise the portrait grid starts directly under the
  title. 4 columns on desktop, 2 on phones.
- **Project pages:** "Our experts" cards with a 96 px portrait instead of
  the 40 px circle.
- **Human input:** the portrait shoot (H16) and, if wanted, a group photo.
- **Done when:** every published person has a portrait in the chosen style,
  and the homepage, team page and project pages use them at the sizes above.

### L4 Section hierarchy and accent use

- **File:** `assets/css/style.css`, `index.md`, `_layouts/*.html`
- **Change:**
  - Each homepage band gets a real heading (`h2`, about 2rem, weight 600)
    with the existing eyebrow above it as a small label, or drop the eyebrow.
  - Introduce one band variant `.band.alt` with `background: var(--surface)`
    and use it on alternate bands (2 and 6 in L2), so the page has a rhythm.
  - Magenta (`--accent`) only for buttons, links in running text, and one
    highlight per band. Years, eyebrows and meta lines move to
    `--ink-soft`. DOIs become buttons (P2.5).
- **Done when:** a screenshot of the homepage at 1,280 px shows a visible
  heading per band and alternating band backgrounds, and contrast still meets
  WCAG AA in both themes.

### L5 Two-column inner pages (Smith, Bauhaus Earth)

- **Files:** `_layouts/project.html`, `_layouts/person.html`,
  `_layouts/publication.html`, `_layouts/post.html`, `assets/css/style.css`
- **Change:** from 1,024 px, a two-column body inside `--wide`:
  - project: facts box (duration, funder, role, client, collaborators,
    website, contact) as a sticky left column of about 18rem; text right in
    `--measure`. Move the facts box from after the text to this column.
  - person: portrait, links and "Works on" chips left; bio right.
  - publication: thumbnail, action buttons and facts left; abstract right.
  - post: date, place and register button (events) left; text right.
  Below 1,024 px, the left column stacks above the text as today.
- **Done when:** the four page types render in two columns at 1,280 px and
  in one column at 390 px, with no horizontal scroll.

### L6 Long lists as tabs

- **Files:** `_layouts/person.html`, `_includes/related.html`
- **Problem:** Martin's profile is 13,540 px at 1,280 px and 22,083 px at
  390 px; after the bio come 10 posts, 15 projects and all publications.
- **Change:** render the related lists with the tab component project pages
  already use (`data-tabs`): News, Projects, Publications, each showing the
  three newest and a "Show all" link to the filtered index. Without
  JavaScript the full lists show, as today.
- **Done when:** the profile height drops and is reported in the PR; the
  no-JS fallback still shows every item.

### L7 Partner logos

- **Files:** `_includes/partners.html`, `index.md`, `assets/css/style.css`
- **Change:** on the homepage only, show the ten partners as one compact
  strip: logos about 40 px high, in a single tone (CSS
  `filter: grayscale(1)` plus an opacity of about 0.8 on the white card, full
  colour on hover/focus), on the `.band.alt` surface. The partner pages and
  `/partners/` keep the full-colour white cards.
- **Done when:** the homepage logo band is under half its current height
  (434 px) and no longer the brightest element on the page.

### L8 Hero

- **Files:** `_includes/hero.html`, `assets/css/style.css`
- **Change:**
  - Lighten the image bed on the right: keep the gradient strong behind the
    text (left), and let the right half show the photo (raise `.hero-media
    img` opacity from 0.44 to about 0.6 and make the `::after` gradient run
    left to right). Check text contrast stays at WCAG AA.
  - Add a primary button ("Work with us", to the P3.3 band anchor) before
    the existing "Our approach →" link.
  - Add a "Coming up" panel at the hero's lower right on desktop (next
    upcoming event from P3.1: date, place, title, link), as Bauhaus Earth
    does with its news panel. On phones it sits under the hero text. Hidden
    when nothing is upcoming.
  - Add a small "Get in touch" button to the header on desktop (Eunomia),
    linking to the same anchor.
- **Done when:** the hero shows two actions and, when an event is upcoming,
  the panel; contrast passes in both themes.

### L9 Short quotes

- **Files:** `_data/testimonials.yml`, `_includes/testimonials.html`
- **Decision (Martin, 29 Oct 2026):** short versions approved. Until at
  least two `about: work` quotes exist (P3.5), the homepage keeps showing
  the three personal recommendations it shows today, in their short form,
  with their `context` line ("LinkedIn recommendation, …") unchanged so
  they stay honest. The full quotes move to Martin's profile.
- **Change:** add a `short` field to each entry in
  `_data/testimonials.yml` with exactly these sentences, each checked as a
  verbatim substring of its `quote`:

  | `id` | `short` |
  | --- | --- |
  | `brigitte-jacquemont` | Martin consistently demonstrated a deep understanding of the subject matter, contributing valuable insights to every study. His work was always of the highest quality and delivered with exceptional clarity. |
  | `xavier-le-den` | Martin is a fantastic partner at work: he combines bottomless scientific knowledge of carbon in buildings with the ability to organise and steer complex studies with strategic implications. |
  | `simone-kongsbak` | Martin is an inspiring data scientist who has a unique ability to understand how building LCAs can create climate policy and industry action and is a skilled communicator. |
  | `rutger-broer` | Martin in short: highly qualified, responsible and reliable, an intuitive team player with a healthy sense of humour. |
  | `andreas-sorensen` | His leadership and deep understanding of the field was instrumental to the success of our work, and he has an exceptional ability to make complex concepts tangible. |
  | `barbara-rodriguez-droguett` | Ensuring that the data architecture for the Chilean WLC tool is compatible with global standards from day one prevents future technical problems and ensures data integration. |

  The homepage renders `short` with name, role, organisation (logo where
  the organisation is a partner) and `context`. The Rodríguez Droguett
  quote stays unpublished until H10 is answered. Extend `docs-check.py` so
  it fails when a `short` is not a substring of its `quote` (compare with
  whitespace collapsed).
- **Done when:** the homepage quotes take one row of cards, and the
  checker passes.

### L10 Project image rules

- **Files:** `docs/03` § 9 (images), `_projects/*.md`
- **Change:** write the rule: in order of preference, (1) an own photograph
  from the project, (2) an own figure on a white card, (3) a stock photo
  only with a credit. Never a screenshot of a website. Replace the two GBDI
  card images that are website screenshots (`gbdi-objectives.png`,
  `gbdi-platform.png`) with a figure or photo (H11).
- **Done when:** no project `hero` is a screenshot of a web page.

### L11 to L17 (smaller)

- **L11 Expertise images:** covered by P4.1.
- **L12 DOI buttons:** covered by P2.5.
- **L13 Post images:** posts with `type: event` and no `hero` get a
  generated date tile (day and month in display type on `--surface`) in
  lists; news posts without an image use their first project's `hero`.
- **L14 Vertical rhythm:** one spacing rule for every `h2` in `.post-body`
  (for example `margin-top: 2.5rem`), so "Collaborators" and "Client" no
  longer sit directly under the block above.
- **L15 Approach diagram:** a simple inline SVG of the three strands (up,
  wide, deep) under the lede, drawn with tokens, no script. Wording from the
  page's own headings.
- **L16 Image placeholders:** give card images `background: var(--surface)`
  so lazy-loading images do not flash white.
- **L17 Footer:** three columns: address, the nav groups, follow and
  newsletter link.

### L18 Shorter profile for Martin

- **File:** `_people/martin-roeck.md` (body only; front matter unchanged)
- **Problem:** the body is 1,123 words, with nine lessons from the air;
  with the related lists the page runs to 13,540 px (L6).
- **Decision (Martin, 29 Oct 2026):** draft approved unchanged.
- **Change:** replace everything after the front matter with the contents
  of `martin-roeck-body-draft.md`, exactly as supplied (H18). The draft is 561 words. It keeps the five `<h2>`
  sections, every role, board, link and degree, and turns the nine lessons
  into four. Keep the lessons in the existing `<dl class="lessons">`
  markup, four `<dt>`/`<dd>` pairs. Do not edit the wording yourself. If
  Martin approves the draft unchanged, it is supplied ready to paste as
  `martin-roeck-body-draft.md` (already in this markup); otherwise use the
  text he sends.
- **Done when:** the body matches the approved text exactly, and the
  page height after L6 and L18 is reported in the PR.

---

## Phase R: visual refinement against the RISE CI (round 3)

Source: third review of 29 October 2026, of the live site after PR #19
(HEAD 6b5b7d2), checked against the RISE CI Manual v1.2 (hla.studio,
12 Dec 2024) and the reference sites:
https://claude.ai/artifact/4pDbvLmqiKqPeiLDvt33vR

Assets: `riselabs-asset-pack-2026-10-29.zip`, supplied with this spec.
Unzip at the repo root. It holds `assets/img/pubs/` (38 thumbnails),
`assets/img/photos/` (10 photos), `manifest.yml` (target path, front-matter
line, source, licence and credit for every file),
`assets/img/placeholders/` (R11), `drafts/datenschutz-plausible-draft.html`
(R10, publish only after approval), `preview/` (reference images, do not
publish), `make_tiles.py` and `crop_pages.py` (move both to
`scripts/`).

Decision (Martin): **light is the default theme; light and dark must both
work.** This replaces "Dark is primary" in `docs/05`.

Phase R supersedes older tasks where they overlap: R4 replaces L5, R5
replaces L17, R2, R3 and R9 replace L4. R6 and R7 cover the image parts of
P2.5 and P4.1 / L11; direct downloads (P2.5) and the team's own photos
(P4.1) remain.

Order: R1–R3 as one PR (theme, tokens, type; every page changes). R4 and
R5 next. R6–R9 and R11 in any order. R10 needs Martin's Plausible setup
and H25. Screenshots of the homepage,
`/projects/`, `/publications/`, one project, one post and `/team/` at 1,280
and 390 px, light and dark, go in each PR.

### R1 Light by default

- **Files:** `_layouts/default.html` (line 4), the theme script,
  `docs/05`.
- **Problem:** line 4 hard-codes `data-theme="dark"`, so every first visit
  and every visitor without JavaScript sees dark.
- **Change:** `data-theme="light"` in the markup. The script keeps a stored
  choice (`localStorage`, wrapped in try/catch) and otherwise follows
  `prefers-color-scheme`. Without JavaScript: light. The toggle stays.
  In `docs/05`, replace "Dark is primary" with "Light is the default; dark
  must work equally well".
- **Done when:** a fresh private window with the OS set to light, and one
  with JavaScript off, both show light; the toggle still switches and
  remembers.

### R2 Palette and bands

- **File:** `assets/css/style.css` (tokens), `index.md`
- **Problem:** light-theme bands run hero / blush / white / white / blush /
  blush. The last two blush bands merge into about 1,600 px of pink, and the
  two white ones into one, so the bands do not read as bands. In dark, the
  alternate band #0a2347 is only 1.15:1 against the navy page. The bright
  magenta is used as a large fill, which the CI does not ask for (it is an
  accent and the end of the gradient).
- **Change:** these tokens, and nothing else for colour:

  | Token | Light | Dark |
  | --- | --- | --- |
  | `--bg` | #ffffff | #001730 |
  | `--surface` (alternate band, card) | #f1f3f6 | #16325a |
  | `--tint` (small highlights only) | #ffe1ee | #2a1745 |
  | `--text` | #001730 | #ffffff |
  | `--accent` (links, labels, rules) | #be208b | #f92d84 |
  | `--btn-bg` / `--btn-fg` | #001730 / #ffffff | #f92d84 / #001730 |
  | `--gradient` | `linear-gradient(120deg, #001730, #751094, #f92d84)` | same |

  Blush (#ffe1ee) is no longer a band colour. Use it only for small
  highlights (a tag, the team banner in R8). Homepage bands, in order:
  hero (photo) → projects (`--bg`) → what we stand for (`--surface`) →
  team (`--bg`) → latest (`--surface`) → partners and quotes (`--bg`) →
  work with us (`--gradient`, white text) → footer (navy in both themes).
  Remove the 1 px border between bands.
- **Rule:** two adjacent bands never share a background. Add a check to
  `docs-check.py` if the bands are data-driven; otherwise a comment in
  `index.md`.
- **Done when:** contrast is measured and reported in the PR: body text on
  every band at least 4.5:1, `--surface` visibly different from `--bg`
  (light #f1f3f6 on white; dark #16325a is 1.41:1 off navy, white text on it
  12.8:1), `--accent` #be208b on white at least 4.5:1.

### R3 Type scale and band rhythm

- **File:** `assets/css/style.css`
- **Problem:** `h2` is 20.8 px on a 17 px body, so section heads barely
  stand out; band padding is 57.6 px. The CI scale steps H1 24 → H2 18 →
  body 10 pt, a ratio of 1.8 between H2 and body; the site has 1.2.
- **Change:** `h1 { font-size: clamp(2.25rem, 5vw, 3rem); }`,
  `h2 { font-size: clamp(1.75rem, 3vw, 2.125rem); font-weight: 500;
  line-height: 1.1; }`. Band padding `6rem` from 48rem up, `4rem` below.
  Text measure 60–80 characters (CI), so text columns are at most 40rem.
- **Typeface (decided, H22):** RISE holds a web and desktop licence for
  Circular, the CI typeface. Switch to it:
  - Self-host the WOFF2 files Martin supplies (H24) in `assets/fonts/`,
    with `@font-face` rules and `font-display: swap`. No font service, no
    third-party request.
  - Cuts: Book (400) for body text, Medium (500) for headings and labels
    (the CI's heading weight), and the matching italics. Use only the cuts
    the licence covers; do not synthesise bold or italic
    (`font-synthesis: none`).
  - Font stack: `"Circular", "Figtree", system-ui, sans-serif`. Keep the
    Figtree files until Circular is live, then remove them.
  - Put the licence notice or EULA reference in `assets/fonts/README.md`
    if the licence asks for it. Do not commit the desktop (OTF/TTF) files
    to the public repo.
  - Re-render the designed publication tiles (R6) with Circular:
    `make_tiles.py` takes the font path as a setting (Martin or the
    implementer runs it locally with the desktop files; only the WebP
    output is committed).
  - `docs/05`: replace Figtree with Circular.
- **Done when:** the homepage at 1,280 px shows each band's heading as the
  largest text in that band, and band edges are visible in both themes;
  the network panel shows the Circular WOFF2 files loading from
  riselabs.at and no other font requests.

### R4 Inner pages: two templates

- **Files:** `_layouts/page.html`, `_layouts/project.html`,
  `_layouts/post.html`, `_layouts/publication.html` (or the include they
  share), the index pages `/projects/`, `/publications/`, `/posts/`.
- **Problem:** inner pages sit in a single 640 px column on a 1,280 px
  screen, so they look narrow and empty next to the full-width homepage.
- **Change:** two templates, both in a 64rem `.wrap`:
  - **Article** (one project, one post, one publication, one profile): a
    full-width page head (title, lede, meta, optional hero image), then a
    grid `minmax(0, 40rem) 18rem` with a 4rem gap. Text in the first column.
    The sidebar holds facts (dates, funder, partners, contact person,
    downloads, tags) and is `position: sticky; top: 6rem` from 64rem up.
    Below 64rem the sidebar moves above the text as a compact fact box.
    Related items go in a full-width `--surface` band below.
  - **Index** (projects, publications, posts): page head, then a filter or
    tab row, then a card grid `repeat(auto-fill, minmax(16rem, 1fr))` that
    uses the full 64rem.
- **Mapping:** projects index, publications index, posts index → Index;
  project, post, publication, person → Article.
- **Done when:** at 1,280 px no inner page has an empty area wider than
  320 px either side of the content; at 390 px text runs edge to edge
  inside the 24 px gutter (L1).

### R5 Footer in one row

- **File:** `_includes/footer.html`, `assets/css/style.css` (line 1312 and
  the `.foot-*` rules)
- **Problem:** `.foot-grid` is 456 / 228 / 228 px and the whole nav sits in
  one 228 px column, so it wraps (About and Work above Media). Line 1312
  sets `align-items: end`, which pushes columns down unevenly. "We work with
  GBDI / INDICATE" is squeezed into the same strip.
- **Change:**
  ```css
  .foot-grid { display: grid; grid-template-columns: 1.6fr repeat(4, 1fr);
               gap: 2rem; align-items: start; }
  .foot-nav  { display: contents; }   /* each nav group becomes a column */
  @media (max-width: 48rem) {
    .foot-grid { grid-template-columns: 1fr 1fr; }
    .foot-grid > :first-child { grid-column: 1 / -1; }
  }
  ```
  Delete line 1312. Columns: address and newsletter (wide), then About,
  Work, Media, Follow. Bottom bar on its own row: left
  "© 2026 RISE · Impressum · Datenschutz", right "Initiatives: GBDI ·
  INDICATE" (links).
- **Done when:** at 1,280 px every nav group sits on one line, and the
  bottom bar is one line; at 390 px two columns.

### R6 Publication grid with title pages

- **Files:** `_publications/*.md` (front matter), the publications index
  and card include, `assets/css/style.css`, `scripts/`
- **Change:**
  - Copy `assets/img/pubs/*.webp` (38 files, 600 × 800) from the pack. For
    each entry in `manifest.yml`, add its `field` line (`thumbnail: …`) and
    its `thumbnail_credit` to the publication's front matter. 20 are title
    pages from open-access PDFs; 18 are designed tiles in the CI (closed
    access, or no PDF that could be opened). Do not swap one kind for the
    other without a licence.
  - Card: 3:4 thumbnail with a 1 px `--surface` border, kind label, title
    (3 lines max), first authors, year and venue, then pills for PDF, DOI,
    Data and Cite, each shown only when the field exists. Grid as R4 Index
    (four columns at 1,280 px, two at 390 px). Year headings stay.
  - Credit: `thumbnail_credit` in small text on the publication page, not
    on the card.
  - Title pages and tiles are never duotoned (R7).
  - `scripts/make_tiles.py` makes a tile from front matter for a new
    entry; `scripts/crop_pages.py` crops a page from a screenshot. Add a
    `make-thumbnails.py` that renders page 1 of a PDF in `assets/pdf/` to
    600 × 800 WebP when the entry's licence allows it. Note both in
    `docs/04`.
- **Licence check (H20):** three title pages are CC-BY-NC-ND
  (`alaux-2024-whole-life-greenhouse`, `roeck-2020-embodied-ghg-emissions`,
  `soustverdaguer-2025-data-infrastructure-whole`). Install them only
  after H20 is answered; until then use a tile made with `make_tiles.py`.
- **Done when:** every publication shows a thumbnail; `docs-check.py`
  fails a publication without `thumbnail`, and a title page without
  `thumbnail_credit`.

### R7 Photos for Expertise, Approach and two projects, in duotone

- **Files:** `_data/expertise.yml`, the Approach page, `_projects/` (the two
  GBDI entries), `assets/css/style.css`
- **Change:**
  - Copy `assets/img/photos/*.jpg` (10 files, 906 × 678). Use them as
    listed in `manifest.yml` (`use`), each with its `image_credit`
    ("Photo: <name> / Unsplash") in small text under or over the image.
    This replaces the current Expertise stock images.
  - Approach: three image and text bands (scaling up, scaling wide, scaling
    deep), image left and text right, alternating sides, on alternating
    `--bg` / `--surface` (R2). Scaling deep uses the existing
    `assets/img/projects/collaborative-housing.jpg`.
  - The GBDI China and India and GBDI Pilot projects get the two
    `project-gbdi-*` photos as hero images.
  - **Duotone, in CSS:** a `.duotone` wrapper. The image is
    `filter: grayscale(1) contrast(1.1)`; two layers sit over it: one
    `mix-blend-mode: lighten` with the dark colour, one
    `mix-blend-mode: multiply` with the light colour. Tokens:
    `--duo-dark` / `--duo-light`. Light theme: #f92d84 / #ffe1ee (ramp A,
    the CI's light duotone, magenta to blush; decided by Martin, H19).
    The photos turn strongly pink on purpose, as accents; keep text off
    them (captions and credits sit below the image, not over it). Dark theme: #001730 / #f92d84 with #751094 in between (ramp D,
    the CI's dark duotone). `preview/*-light.jpg` and `*-dark.jpg` show the
    intended result for each photo.
  - Duotone only for photos. Never for figures, title pages, tiles, logos
    or portraits (portraits stay black and white, H16).
- **Done when:** the Expertise page, the Approach page and the two GBDI
  projects match the previews in both themes, and every photo shows its
  credit.

### R8 Team page wording and layout

- **File:** `team.md` (or `_pages/team.md`), the person card include,
  `_people/*.md` (`group` field)
- **Change:** use this text exactly.
  - Lede: "RISE is a growing team in Vienna. We work every day with
    researchers at partner institutions, and with a wider network across
    policy, industry and research."
  - Banner under the lede (`--tint` background, small text): "We are
    growing. New colleagues join in 2027 and more profiles are on their
    way. [See open positions →](/join/)"
  - First group heading: "At RISE".
  - Second group heading: "Extended team", with the note "Researchers we
    work with closely on shared projects, employed by our partner
    institutions." This replaces "core collaborators" everywhere on the
    site, including front matter values and labels.
  - Card affiliation line: "RISE" for `group: rise`; for
    `group: collaborator`, "Extended team · " followed by the person's
    `org` (for example "Extended team · Global Building Data Initiative,
    EPFL"). Built from front matter, never typed. The `group` value
    `collaborator` can stay as an internal key; only the visible label
    changes.
  - Layout: four columns of 1:1 portraits about 240 px wide, black and
    white in CSS (`filter: grayscale(1)`), name, role, affiliation line.
    Two columns at 390 px.
  - As of 235b9a8 the page shows five people as drafts (Martin, Barbara,
    Nicole, Zuhaib, Norman). The draft marking stays until each person
    has approved their text (H3–H5).
- **Done when:** the words "core collaborator" appear nowhere in the built
  site, and the banner links to `/join/`.

### R9 Hero and accents

- **File:** `assets/css/style.css`
- **Change:** the hero overlay uses `--gradient` at 85% opacity over the
  photo, in both themes (the CI's gradient; the opacity is a proposal,
  tune by eye). Buttons use
  `--btn-bg` / `--btn-fg` (navy in light, magenta in dark). Magenta as a
  fill only on the hero, the "work with us" band (via the gradient) and
  small elements; everywhere else it is text, rule or icon colour.
- **Done when:** in light theme no area larger than a button is filled
  with flat #f92d84.

### R10 Visitor analytics with Plausible (decided, H21)

- **Files:** new `_includes/analytics.html`, `_layouts/default.html`
  (`<head>`), `404.html`, `datenschutz.md`, `_data/` (privacy date),
  `docs/04`, `docs/05`
- **Decision (Martin, 29 Oct 2026):** Plausible Analytics. EU-hosted, no
  cookies, no local storage, raw IP addresses never stored. Visitors are
  counted with a hash of a daily salt, the site domain, IP address and
  browser, and the salt is deleted every 24 hours, so a visitor cannot be
  followed across days or sites.
- **Plan:** the answer to "from and to where" across several pages (user
  journeys, funnels) is only in **Business** ($19 a month at 10k
  pageviews, as of 29 Oct 2026). Starter ($9) has visitors, sources,
  pages, entry and exit pages, countries, devices, time on page, outbound
  links and downloads, but one user only; Growth ($14) adds team members
  (Barbara) and shared links. Start with the free 30-day trial, which has
  all Business features, and decide on the plan after a month of data.
- **Martin does (account owner, H21):**
  1. Create the account at plausible.io and add the site `riselabs.at`.
     Plausible's terms include its data processing agreement (DPA); no
     separate signature is needed. Save a PDF of the DPA for the records.
  2. In the site settings under General → Tracking, turn on outbound
     links, file downloads and form submissions.
  3. Under Goals, add a custom event goal named `404`.
  4. Under Shields → IP addresses, add the office IPv4 and IPv6 address.
     On each own browser and device, open riselabs.at, open the developer
     console and run `localStorage.plausible_ignore=true` to stop counting
     own visits.
  5. Copy the site's snippet from Settings → General → Tracking → Site
     installation and give it to the implementer.
  6. Optional: weekly email report; invite Barbara (needs Growth or
     Business).
- **Implementer does:**
  - Paste the snippet exactly as Plausible gives it into
    `_includes/analytics.html`. Do not rewrite or self-host it. Include it
    in `<head>` of `_layouts/default.html`, only in production:
    ```liquid
    {%- if jekyll.environment == "production" -%}
      {%- include analytics.html -%}
    {%- endif -%}
    ```
    GitHub Pages builds with `JEKYLL_ENV=production`, so local builds and
    previews send nothing. Plausible also ignores `localhost` by default.
  - `404.html`: after the snippet has loaded, send the 404 event (from
    Plausible's docs):
    ```html
    <script>document.addEventListener('DOMContentLoaded', function () { plausible('404'); });</script>
    ```
  - This is the one third-party script the site allows. Note the
    exception in `docs/05`, line 77 ("An embedded third-party script…"),
    and in section 0 of this spec.
  - `datenschutz.md`:
    - Replace "verwendet keine Webanalyse" in the "Grundsatz" paragraph with
      a sentence that says the site uses cookieless audience measurement,
      described below.
    - Add the section in `drafts/datenschutz-plausible-draft.html`. Do this
      only after Martin or a lawyer has approved it (H25).
    - Update the comment at the top of the file and the "Stand" date.
  - No cookie banner is added. Whether § 165 Abs. 3 TKG 2021 requires
    consent for cookieless measurement is not settled (EDPB Guidelines
    2/2023 read the rule broadly). That is part of the H25 review. If the
    reviewer wants consent, stop and ask; do not build a banner on your
    own.
- **Done when:**
  - The snippet is in the HTML on riselabs.at and absent from a local
    build.
  - A test visit, an outbound click, a PDF download and a 404 each show
    in the realtime view.
  - Own visits are excluded.
  - The Datenschutz section is live with the approved wording.

### R11 One placeholder per kind of item

- **Files:** `_includes/stockimg.html`, `_data/stock.yml`,
  `_includes/projectgrid.html`, `_layouts/project.html`,
  `_layouts/person.html`, `_includes/peoplelist.html`,
  `_includes/pubitem.html`, `assets/img/placeholders/`
- **Now (235b9a8):**
  - Projects and Expertise fall back to one of eight stock texture photos
    (`_data/stock.yml`), chosen by the length of the slug modulo 8. Items
    whose slugs have the same length get the same picture, and a texture
    does not tell a visitor that a picture is still to come. All 15
    projects have a `hero` today, so this fallback is only visible on
    Expertise, which R7 replaces.
  - People cards show initials when there is no portrait. The profile page
    shows nothing.
  - Publications have no image at all.
- **Change:** one dedicated placeholder per kind, all in the CI, so a
  missing image looks intentional. Previews are in
  `preview/placeholders.jpg`; the files are in `assets/img/placeholders/`
  in the pack.
  - **Project** (card and page head): `placeholder-project.webp`, the CI
    gradient with the white signet. Use it wherever a project, post or
    event has no `hero` or `image`. Retire the stock-texture picker for
    projects. Keep `_data/stock.yml` only if Martin wants the textures
    elsewhere.
  - **Publication**: no image file. When `thumbnail` is missing, render the
    designed tile in HTML and CSS from front matter: the gradient bar, kind
    label, venue, title, the first three authors, year and DOI, on a 3:4
    white card, matching the R6 tiles. A new publication therefore never
    shows an empty box. `docs-check.py` warns (not fails) when `thumbnail`
    is missing, so a proper tile or title page gets made later.
  - **Person**: initials from `cite`, centred in Circular Medium, on
    `--surface` (light #f1f3f6 with navy text; dark #16325a with white
    text), 1:1. Use the same markup on the card and on the profile page.
- **H23 items:** the EU, IEA EBC, TU Graz and MDPI publications keep
  their designed tiles from the pack until Martin supplies the PDFs.
  Their tiles are their placeholders.
- **Done when:** removing `hero`, `thumbnail` or `portrait` from a test
  copy of one project, one publication and one person shows the matching
  placeholder on the card and on the page, in both themes.

## Phase W: "Work with us" and Expertise, revised content

Source: review of 29 October 2026 of the homepage "Work with us" band and
`/expertise/` against the projects and publications on the site (repo at
2158c73): https://claude.ai/artifact/Nr5v6wntREMDGKGCCF7cBh

Both still carried the old services wording. Expertise had no field for the
"scaling deep" strand of `/approach/`, no Global South, and linked only
projects. "Work with us" missed the two ways most current work starts
(funders backing programmes, countries joining data programmes).

Content files, supplied ready to use (Martin approves the wording, H29):
`drafts/engagement.yml` and `drafts/expertise.yml`. Every slug in them has
been checked against `_projects/`, `_publications/` and `_posts/` at 2158c73.

Do W1–W4 in one PR, after R7 (photos) or together with it.

### W1 Four ways in, with examples

- **Files:** `_data/engagement.yml`, `_includes/engagement.html`,
  `index.md`, `docs-check.py`
- **Change:**
  - Replace `_data/engagement.yml` with `drafts/engagement.yml`.
  - Each entry has a new `examples` list of project slugs. In the cards
    include, render under the body: "For example:" and the project
    titles, linked, joined with " · ". Use the project's `short_title` if it
    has one, otherwise `title`. Then the mail link as now.
  - Add `short_title` to the front matter of these projects (new field;
    document it in `docs/03`). Values, exactly:
    | project | short_title |
    | --- | --- |
    | supporting-the-development-of-a | EU whole life carbon roadmap |
    | analysis-of-life-cycle-greenhouse | EU buildings emissions analysis |
    | towards-embodied-carbon-benchmarks-for | European embodied carbon benchmarks |
    | agora-leitmaerkte-embodied-carbon | Agora lead markets |
    | global-status-report-for-buildings | Global Status Report |
    | global-whole-life-carbon-tracker | Global Whole Life Carbon Tracker |
    | global-building-data-initiative | GBDI |
    | gbdi-china-and-india-cooperation | GBDI China and India |
    | chile-wlc-data-harmonisation | Chile data harmonisation |
    | indicate | INDICATE |
    | indicate-life | INDICATE LIFE |
    | iea-ebc-annex-72 | IEA EBC Annex 72 |
    | reliving-scaling-renovation | Re:Living |
    | collaborative-carbon | CollaborativeCarbon |
    | pef4buildings | PEF4Buildings |
    W2 uses `short_title` in the same way.
  - Drop the `style="list"` branch of the include, which nothing uses after
    W2.
  - Homepage lede (`index.md`, `#work-with-us`), exactly: "We work with
    public authorities, international organisations, funders, research
    partners and the pioneers changing how we build. Most collaborations
    start in one of four ways."
  - Keep the fallback email line and the newsletter row.
  - `docs-check.py`: fail an unknown slug in `engagement.yml` `examples`.
- **Done when:** four cards, each with two linked examples, the new lede,
  and mail links whose subject is the card title.

### W2 Expertise page by strand

> **Update 31 Oct 2026.** `drafts/expertise.yml` is now rebased on the
> positioning-led copy of PR #38: the six existing fields keep their
> `question`, lede and bullet points exactly as merged; the draft only adds
> `publications`, `posts`, extra `examples`, moves Methods to `strand: wide`,
> and appends the two deep-strand fields (each with a `question`). It passes
> `docs-check.py` against 9993724. Where the text below conflicts with PR
> #38, PR #38 wins: keep the question-led headings and the page title
> pattern, so the `h1` becomes "Eight questions we answer", and keep the
> current page lede (adjusting "six" if it says so). Images stay on the stock
> paths until R7 installs the photos. Wording approved by Martin on 31 Oct
> (H29); review work dropped from Methods (H27).

- **Files:** `_data/expertise.yml`, `expertise.html`, `assets/css/style.css`
- **Change:**
  - Replace `_data/expertise.yml` with `drafts/expertise.yml` (eight fields;
    new keys `publications` and `posts`).
  - Page head: `h1` "Expertise". Lede, exactly: "What we do, grouped by the
    three strands of our approach. Under each field are the projects and
    publications where you can check it."
  - Index row: the three strands, each followed by its fields as jump
    links.
  - Three bands, in order up, wide, deep, alternating `--bg` and
    `--surface` (R2). Each opens with an `h2`, a one-line intro, and a
    link "More on this strand →" to the matching Approach section (W3).
    Exactly:
    | strand | h2 | intro |
    | --- | --- | --- |
    | up | Scaling up: changing the rules | Evidence for the people writing the rules, and the methods that make it hold up. |
    | wide | Scaling wide: reaching greater numbers | Shared infrastructure that lets many actors act at once. |
    | deep | Scaling deep: working with pioneers | Testing what is possible with the networks that build differently, and keeping carbon from crowding out everything else. |
  - Fields render as now (image and text, alternating sides), with field
    titles as `h3`. Evidence becomes two lines: "Projects" (from
    `examples`) and "Publications" (from `publications`, then `posts`), each
    linking the item's title. Publication titles longer than 80 characters
    are cut at a word boundary with "…"; the link carries the full title in
    `title`.
  - A field without `image` shows the R11 project placeholder.
  - After the deep band, a "Global South and emerging markets" band, text
    exactly: "Most of the floor area of the coming decades will be built in
    the Global South. Across all three strands, a growing share of our work
    is with partners in China, India, Chile and South Africa: shared data,
    local capacity, and methods built with local teams rather than
    imported." Then the same two evidence lines, from these slugs:
    projects `gbdi-china-and-india-cooperation`,
    `chile-wlc-data-harmonisation`, `global-building-data-initiative`;
    publications `dunant-2025-timely-deployment-best`,
    `satola-2021-life-cycle-ghg`; posts `cbpm-cape-town-keynote`,
    `cbmf-beijing-low-carbon-concrete`, `gbdi-india-webinar`. Put the slugs
    in the page's front matter (`global_south:`), not in the markup.
  - Replace both end blocks ("How we work with you" and the "Work with us"
    box) with the homepage band: `h2` "Work with us", the line "We would
    rather hear the problem than the brief.", the four cards
    (`engagement.html style="cards"`), and the fallback email line. No
    newsletter here.
- **Done when:** eight fields under three strand headings, every field
  with at least two project links and at least one publication link, the
  Global South band, one "Work with us" block at the end; no broken links
  (`docs-check.py`).

### W3 Anchors on the Approach page

- **File:** `approach.md`
- **Change:** give the three strand headings stable ids: `scaling-up`,
  `scaling-wide`, `scaling-deep` (`<h2 id="scaling-up">`). Text unchanged.
- **Done when:** `/approach/#scaling-deep` jumps to that heading.

### W4 Checker and docs

- **Files:** `docs-check.py`, `docs/03-editing-the-site.md`
- **Change:** `docs-check.py` fails an unknown slug in `expertise.yml`
  (`examples`, `publications`, `posts`), in `engagement.yml` `examples`,
  and in `expertise.html` `global_south`; it fails a `strand` other than
  up, wide, deep. Document the new keys in `docs/03` (expertise and
  engagement tables).
- **Done when:** a misspelt slug in either data file makes the checker
  fail with the file and the slug named.

### W5 Approach: drop the review line

- **File:** `approach.md`, the list under "How we hold ourselves to account"
- **Decision (Martin, 31 Oct 2026, H27):** RISE does not offer review work.
- **Change:** delete the list item "We review only where we have no stake in
  the outcome, and say so in writing." The other three items stay as they
  are. Check `docs/10-boilerplate.md` for the same line and remove it there
  too.
- **Done when:** no page on the built site mentions review work or "no
  stake".

### W6 "Work with us": six ways in, scope, and next steps

- **Files:** `_data/engagement.yml`, `_includes/engagement.html`, `index.md`
  (`#work-with-us`), `expertise.html` (closing band), `assets/css/style.css`,
  `docs/03`, new `_publications/dejaco-2020-combining-lca-lcc.md`
- **Source:** Martin's decisions of 1 Nov 2026. Supplied in
  `riselabs-w6-2026-11-01.zip`: `_data/engagement.yml` (replace the file),
  the new publication and its tile. Both pass `docs-check.py` at 368a636.
- **Problem:** the hero button "Work with us" lands on a band called "Start
  with the problem"; the band uses a third framing beside Expertise's
  questions and the cards' situations; it has no way in for the deep strand
  or for research consortia, and it closes on the newsletter only while job
  posts are going out.
- **Change:**
  - Heading: "Work with us" (keep `id="work-with-us"`).
  - Lede, exactly: "We would rather hear the problem than the brief. We
    cover the whole life cycle, from cost and carbon to environmental and,
    increasingly, social impacts, and every scale from a single building to
    national and global building stocks. Tell us the decision in front of
    you, and we will tell you what evidence would hold up."
  - Six cards from `engagement.yml`, in file order, in a 3 x 2 grid from
    64rem, 2 columns from 40rem, 1 below. Each card: `label` as a small
    uppercase line in the accent colour (linked to `label_url` where given),
    `title`, `body`, "For example:" with the two projects, then the mail
    link with `action` and the `subject` prefilled. Same height per row.
  - Under the grid, two lines:
    - "Looking for training, a workshop or a speaker, or something else
      entirely? Write to office@riselabs.at." (mail link)
    - "Not sure where you fit? See the eight questions we answer →" linking
      to `/expertise/`.
  - Last row, two blocks side by side from 40rem: the newsletter as now, and
    "Join us". While a post with `type: opening` is published: "We are
    growing, and hiring in Vienna." with "Open positions →" to `/join/`.
    Otherwise: "Other ways in: theses, visiting researchers →" to `/join/`.
  - `expertise.html`: the closing band uses the same six cards and the two
    lines; no newsletter or Join row there.
  - Add `dejaco-2020-combining-lca-lcc` (backs "cost" in the lede), then run
    the citation and abstract scripts for it. Its title page is CC BY and can
    replace the tile.
  - `docs-check.py`: fail a card without `label`, `title`, `action` and two
    `examples`, and a project used on two cards. Document `label` and
    `label_url` in `docs/03`.
- **Wording notes (decided):** "social impacts" is qualified with
  "increasingly" because the Approach page still calls the social and
  economic dimensions "the next step"; cities are not named until a
  city-scale project is on the site.
- **Done when:** the band reads "Work with us" with the lede above; six cards,
  3 x 2 on a desktop; every card shows a label, two linked examples and a
  working mail link; the Join block switches with the opening post.

## Phase E: publications of the extended team

Source: search of 30 October 2026 (ORCID, Crossref, DataCite, OpenAlex,
EPFL and UCT records) for Nicole Di Santo, Zuhaib Batra and Darmarajan
(Norman) Chinasamy, the RISE x GBDI extended team. Partners at other
organisations are out of scope.

Supplied: `riselabs-extended-team-pubs-2026-10-30.zip` with 26 files for
`_publications/`, their 26 designed tiles for `assets/img/pubs/`, and
`manifest-newpubs.yml` (sources, licences, PDF links). The test copy passed
`docs-check.py` ("no problems found") with the files added at 45f6980.

### E1 Add the entries

- **Files:** `_publications/` (26 new), `assets/img/pubs/` (26 new)
- **Change:** copy them in unchanged. 25 are the extended team's: 1 shared
  GBDI paper (Di Santo, Batra, Röck and others, fib Congress 2026), 4 more
  by Nicole, 14 more by Zuhaib, 6 by Norman. The 26th is Martin's own and
  was missing: the Global Status Report 2025-2026 (UNEP, GlobalABC), linked
  to that project.
- Each entry carries `people:` for the person, so it shows on their profile;
  `partners:` only where OpenAlex lists that institution for a co-author,
  and only for partners that already have a file; `projects:` only for the
  GBDI paper and the Status Report.
- Conference papers use `kind: article` (the site has no conference kind);
  their tiles say "Conference paper".
- Thumbnails are designed tiles for now. Where `manifest-newpubs.yml` says
  `title_page_possible_later: true`, a CC BY title page can replace the tile
  later (R6 rule).
- **Done when:** the three profiles list their publications; the
  publications page shows 64 entries.

### E2 Earlier name forms

- **Files:** `_people/zuhaib-batra.md`, `_includes/pubitem.html`,
  `docs/03`
- **Problem:** Zuhaib published as "Zuhaib S" (Sheikh Zuhaib) until 2022 and
  as "Batra Z" from 2024 (same ORCID, 0000-0002-3402-0048). Author strings
  keep the published form, so his older papers would not be underlined.
- **Change:** a new optional list `cite_also:` on people
  (`cite_also: ["Zuhaib S"]` for Zuhaib); `pubitem.html` underlines each
  form like `cite`. Document it in `docs/03`.
- **Done when:** "Zuhaib S" is underlined in his 2016-2022 entries.

### E3 Optional: tell RISE work from earlier work

- **Problem:** with E1, about half of the list predates RISE and GBDI
  (Galway, BPIE, Politecnico di Milano). A filter may help visitors.
- **Change, if Martin wants it (H31):** a filter chip on `/publications/`
  "With RISE or GBDI". The rule that decides it is agreed with Martin
  first (H31); derive it from existing fields rather than tagging by hand.

## Phase F: homepage facts, six perspectives

Source: facts review of 31 October 2026:
https://claude.ai/artifact/UrPGudha3ecLT2MUgxcWMw

Decisions (Martin, 31 Oct 2026):
- The VELUX green paper (`toth-2026-housing-we-need`) may be used, labelled
  as a green paper in the source line ("Toth et al., 2026, green paper").
  Update the comment in `index.md` that says every figure must come from a
  peer-reviewed paper: "published, with a DOI, on this site; non-peer-reviewed
  sources labelled as such".
- Numbers for Mouton et al. 2022 (2/2) may come from its open preprint
  (10.21203/rs.3.rs-2199079/v1); the source line links the published entry.
- Publication titles follow the published versions (F2).

### F1 Six facts in a 3 x 2 grid

- **Files:** new `_data/facts.yml`, `index.md` (`#evidence`),
  `assets/css/style.css`, `docs-check.py`, `docs/03`
- **Change:** the six picked facts move into `_data/facts.yml`, one entry
  each: `perspective`, `value`, `say`, `source_label`, `publication` (slug).
  The band renders them as a grid: 3 columns from 64rem, 2 below, 1 under
  30rem; each cell shows the perspective label (small caps, accent colour),
  the value, the sentence and the linked source line(s). `docs-check.py`
  fails a fact whose `publication` slug does not exist.
- **Content (decided 31 Oct 2026):** use `_data/facts.yml` from
  `riselabs-w2-f2-2026-10-31.zip` exactly. Each entry has `perspective`,
  `value`, `say` and a `sources` list (`label`, `publication`); Scaling has
  two sources, joined with "; " in the source line. Order as in the file:
  Europe, Existing buildings, Global, Global South, Single building,
  Scaling. Sentences that start lower-case ("could be created…", "of the
  world's…") continue the value and are rendered directly after it.
- **Band lede (decided 31 Oct 2026):** replace "Efficiency alone will not
  get Europe's buildings within their limits. Our research shows why, and
  what does." with, exactly: "From single buildings to the regenerative
  evolution of the world's building stock: our research shows what works at
  scale." 
- **Done when:** six cards, 3 x 2 at 1,280 px and 2 x 3 at 390 px; every
  source line links to its publication page; the four old figures are gone
  from `index.md`.

### F2 Published titles for the two Mouton papers

- **Files:** `_publications/mouton-2022-low-tech-passive.md`,
  `_publications/mouton-2022-environmental-potentials-bio.md`
- **Change:** set `title:` to the published titles, exactly (slugs and URLs
  unchanged):
  - 2/2: "Low-tech passive solar design concepts and bio-based material
    solutions for reducing life cycle GHG emissions of buildings – Life cycle
    assessment of regenerative design strategies (2/2)"
  - 1/2: "Bio-based building material solutions for environmental benefits
    over conventional construction products – Life cycle assessment of
    regenerative design strategies (1/2)"
  Re-render both tiles with `make_tiles.py` if the publication has a designed
  tile rather than a title page.
- **Done when:** both titles match the DOI landing pages.

## Phase M: phone fixes for publications and the team band

Source: Martin's phone screenshots of 31 October 2026 (publications page and
homepage, dark theme) and the prototype
https://claude.ai/artifact/ULwzsM5THXyzE2LH53v1Ph, which is the reference for
both tasks (open it on a phone and on a desktop).

### M1 Publications: one control row, title first, readable on a phone

- **Files:** `publications.md`, `_includes/pubitem.html`,
  `_includes/filter.html` (if needed), `assets/js/ui.js`,
  `assets/css/style.css`, `docs/03`
- **Problem:**
  - On Martin's phone the list shows only the covers: no titles, authors or
    venues, on `/publications/` and in "Recent publications" on the
    homepage. In desktop Chrome at 390 px the text renders (in a 207 px
    column, with up to 32 authors running six lines and more), so the cause
    is device-specific and not yet found.
  - The controls break up on a phone: two rows of pill buttons with labels
    on their own lines, and the filter box sits directly against the sort
    buttons.
- **Decision (Martin, 31 Oct 2026):** remove the "With RISE or GBDI" filter
  (H31) and simplify sorting.
- **Change:**
  - Delete the `data-pubfilter` bar and `setupPubFilter` in `ui.js`. Keep
    `rise_work` and the RISE-first order within a year; it costs nothing
    on the page. *(`rise_work` became the three-valued `rise_tier` on
    31 Oct 2026; see the implementer's note above.)*
  - Replace the sort buttons with one `<select id="pub-sort">` labelled
    "Sort" (Newest first, Oldest first, Most cited; the last only when
    counts exist), on one row with the filter box: the input takes the
    remaining width, the select sits to its right, and both wrap onto two
    lines under about 30rem with a gap of .6rem. Space above the list:
    2rem. Without JavaScript the select is hidden, as the buttons are now.
  - Each entry leads with its title (bold, linked), then the full author
    list in a smaller, muted size with team names underlined, then venue,
    year and DOI. On a phone (below 40rem): a 64 px cover beside the title,
    and authors and venue full width underneath (`grid-template-areas:
    "thumb title" "authors authors" "meta meta"`). From 40rem: a 96 px
    cover, with title, authors and venue stacked beside it. Same markup and
    CSS for the homepage "Recent publications".
  - Find the cause of the missing text before closing this task: test on a
    real Android phone in Chrome and in Samsung Internet, light and dark
    theme, with and without a content blocker, and with a cleared cache.
    Note what it was in the PR. If it was a content blocker hiding
    class names that start with `pub`, rename the classes (for example
    `cite-`).
- **Done when:** on a real phone, every entry on `/publications/` and on the
  homepage shows its title, authors and venue; the controls are one row on a
  desktop and at most two on a phone; there is no filter by RISE or GBDI.

### M2 Team band: a one-row swipe carousel

- **Files:** `index.md` (team band), `_includes/peoplelist.html` (if the
  card needs a class), `assets/js/ui.js` (`setupCarousel`),
  `assets/css/style.css` (the carousel section)
- **Problem:** the carousel shows two people per page with dots, a counter,
  arrows and a play button, and the page jumps when the last page holds one
  person (five people, two per page).
- **Change:** follow the prototype exactly:
  - One row of cards that scrolls sideways with native scrolling and
    `scroll-snap-type: x mandatory`; each card snaps to its start.
  - Card width: 78% below 40rem (one card and a slice of the next), 42% from
    40rem (two and a bit), 29% from 64rem (three and a bit). On a phone the
    row bleeds to the screen edge, so the next card visibly continues.
  - The card is the existing person card: 1:1 portrait in black and white,
    name, role, affiliation line. Every card has the same height.
  - No dots, no counter, no play button, no autoplay, no hidden items. Remove
    that code from `setupCarousel` and its CSS.
  - Two subtle round arrow buttons (prev, next), shown only when
    `(hover: hover) and (pointer: fine)`, vertically centred on the
    portraits. Each scrolls by one card width; each is disabled and faded
    out at its end of the row. Smooth scrolling unless
    `prefers-reduced-motion`.
  - Without JavaScript: the same swipeable row, without arrows.
  - Hide the scrollbar; keep keyboard focus visible on each card link.
- **Done when:** at 390 px one card and part of the next show and swiping
  moves card by card; at 1,280 px three and part of a fourth show, with
  arrows; the band never changes height while scrolling.

## Phase T: team page

### T1 "Where we work", below the team

- **Files:** `team.md` (or the team page template), `assets/css/style.css`,
  `assets/img/place/`, `docs/03`
- **Source:** Martin, 1 Nov 2026. Draft and layout:
  https://claude.ai/artifact/DPf6Aoekbi8ZC16iQeF5sY (prototype). Facts from
  climatelab.at, its press page, ORF Wien (2 Oct 2022) and EIT Climate-KIC
  (13 Mar 2022).
- **Change:** a new band below the team groups (and above any Join block),
  on `--surface`, with this text exactly:
  - `h2` "Where we work"
  - Lede: "We work mostly remotely, with colleagues in Austria, Switzerland
    and South Africa, and come together for team retreats and regular
    in-person meetings."
  - `h3` "Climate Lab Vienna", then: "Our on-site team is based at Climate
    Lab, an innovation centre for the climate transition at Spittelau on the
    Donaukanal. It is run by Impact Hub Vienna in premises provided by Wien
    Energie, beside the waste-to-energy plant designed by Friedensreich
    Hundertwasser." and "We share it with start-ups, companies and
    researchers working on the energy transition, sustainable building and
    the circular economy."
  - Address block: "Climate Lab / Spittelauer Lände 45, 1090 Vienna / U4 and
    U6 Spittelau", then a link "climatelab.at" to https://climatelab.at/.
  - Images, right of the text from 56rem, below it on a phone: one wide
    (16:9) and two smaller (3:2) underneath. Inside the workspace only; no
    picture of the building exterior (Martin, 1 Nov 2026). Supplied by Martin
    on 2 Nov 2026, in `riselabs-t1-photos-2026-11-02.zip`
    (`assets/img/place/`, with `_data/place.yml` ready to use):
    1. Wide: `climate-lab-event.jpg`, the Climate Lab floor during an event,
       caption "Climate Lab, Spittelau."
    2. Small: `rise-desks.jpg`, caption "Our desks at Climate Lab."
    3. Small: `team-sbc-summit-2026.jpg`, caption "The team at the
       Sustainable Buildings and Construction Summit, Lausanne, April 2026."
    Crop with `object-fit: cover` and the `focus` value from `place.yml` as
    `object-position`. Each caption ends with "Photo: <credit>": 1 "Climate
    Lab / Fetz", 2 "Climate Lab", 3 "Rue Munemo". All three go live now
    (Martin, 2 Nov 2026).
    With none shown, the text runs full width. No empty boxes on the live
    site.
  - Photos follow R7 (duotone in both themes); captions sit below, never on
    the image.
  - Put the place in `_data/place.yml` (name, text, address, link, images
    with credit), so a move is a data change, not a template change. T2
    turned that into a list of places on 2 Nov 2026.
- **Done when:** the band shows below the team on /team/ in both themes,
  every photo carries its credit, and no placeholder boxes are visible.

### T2 The 2027 move, on the page now

Martin, 2 Nov 2026: add dieHausWirtschaft and keep Climate Lab. The move is
not a swap. RISE keeps its Climate Lab membership and stays in that
community and its events, and the new house is on the page a year early so
that anyone considering applying can weigh up where they would live while
they are still deciding.

- **Files:** `_data/place.yml`, `team.md`, `_includes/placeblock.html` (new),
  `assets/css/style.css`, `docs-check.py`, `docs/03`
- **Change:** `_data/place.yml` becomes a `places` list rather than one
  place, with `when` as the label above each name ("Today", "From 2027").
  `images` stays outside the list: the photographs are of the team and of
  the desks it works at now. The page loops the list, so the move itself is
  a reordering of two entries and two labels.
- **Layout:** the first place keeps the text column beside the photographs.
  Every place after it spans the full width underneath, with a rule above
  and its paragraphs in two columns from 56rem. Stacked in the text column
  instead, the second place left about 550 px of empty surface beside it,
  because all three photographs belong to the first.
- **Text:** the wording prepared in T1 is used as drafted, plus the
  cooperative's own two halves of the house and the housing line. Checked
  against diehauswirtschaft.at on 2 Nov 2026: the cooperative, the
  Nordbahnviertel, "Arbeiten und Wohnen nehmen jeweils 50 Prozent der Fläche
  ein", the low-energy building with its own photovoltaics (the coworking
  page), tram O stopping at the door, and the members designing the house
  with einszueins architektur, who are RISE's partners in
  CollaborativeCarbon. No count of people or flats is quoted: that site
  gives 200 and 250 people in different places, and 46 and 48 homes, and
  rule 2 is not satisfied by picking one.
- **Housing:** the flats are let by the cooperative. The page says so and
  sends the question there, because RISE has nothing to do with letting them
  and must not read as though it had.
- **Still needed:** pictures of the new house, which are H39. Until they
  exist the band shows the Climate Lab photographs only, which is honest:
  RISE does not work there yet.
- **Done when:** /team/ shows both places in both themes, no sideways scroll
  at 390 px, and `docs-check` passes.

---

## Phase N: one page for news and events

Martin, 1 Nov 2026: /news/ and /events/ show almost the same list, so they
become one page with tabs by type of post. More types will follow (news,
events, project updates, insights and so on); Martin will bring the
categories used on social media so the two can line up later (H36). Build
with the types in use now. Prototype:
https://claude.ai/artifact/BBuRw4RbqB7dD6PizjM72t (file
`news-and-events.html`).

This phase replaces the events page in P3.1. The event fields from P3.1
(`event_start`, `event_end`, `location`, `format`, `register_url`,
`materials`) stay exactly as specified there, and the backfill in P3.1 is
part of this phase. P3.2 ("Coming up" on the homepage) reuses the include
from N3.

### N1 Post types in one data file

- **New file:** `_data/post_types.yml`, one entry per type, in tab order:

  ```yaml
  - slug: event        # value of `type:` in the post
    label: Event       # shown on a card
    plural: Events     # shown on the tab
    hash: events       # /news/#events
  - slug: project
    label: Project update
    plural: Project updates
    hash: project-updates
  - slug: output
    label: Publication
    plural: Publications
    hash: publications
  - slug: opening
    label: Open position
    plural: Open positions
    hash: open-positions
  ```

- Adding a type later is one entry here; no template changes. Do not add
  types that no post uses yet (no "Insights" until there is one).
- `docs-check.py`: every post's `type` must be a `slug` in this file; a post
  with `type: event` and `published` not false must have `event_start`, or be
  listed in H8 (warn, do not fail, so the six existing posts can be
  backfilled step by step).
- `newslist.html` and the homepage "Latest" show `label` instead of the raw
  `type` value ("Project update", not "project").
- `docs/03` § 8: document the file and the rule.

### N2 The page

- **File:** `news.md`, title and h1 "News and events", lede "What we
  published, where we spoke, and what changed in our projects."
- **Order on the page:** page head, "Coming up" (N3), tab row with the
  filter field on the right (below the tabs on a phone), card grid.
- **Tabs:** "All" plus one tab per type in `post_types.yml` order, each with
  its count in a small muted number ("Events 6"). A type with no published
  post has no tab. Built at build time from `site.posts`; the script only
  switches. Tabs are buttons with `role="tab"` and `aria-selected`, in a row
  that scrolls sideways on a phone without a visible scrollbar. Reuse
  `setupTabs` in `ui.js` if it fits; otherwise extend it rather than adding a
  second tab script.
- **Links:** each tab has its own hash (`/news/#events`); opening the page
  with a hash selects that tab, and choosing a tab updates the hash with
  `history.replaceState` (no new history entries).
- **Filter:** the existing `filter.html` field, applied within the chosen
  tab. "Nothing matches" line when the result is empty.
- **Without JavaScript:** all posts show in one grid, newest first, and the
  tab row is hidden.
- **Years:** no year breaks in the grid; the date on each card is enough.

### N3 "Coming up"

- **New include:** `_includes/comingup.html`, used here and by P3.2 on the
  homepage.
- Lists events whose `event_end` (or `event_start`) is today or later,
  soonest first, at most three, as cards side by side (stacked on a phone).
  Each shows a date block (day and month; month and year only when the day
  is not known), the title without "Upcoming:", the place and one short line,
  and "Register" when `register_url` is set.
- Staleness as in P3.1: render with `data-end` and let `ui.js` hide items
  whose end has passed. Hide the whole strip when it is empty.
- Shown on the "All" and "Events" tabs only.
- On a `--surface` band, like the prototype.

### N4 Cards

- **New include** (or a rework of `newslist.html`): a grid of cards, three
  columns on desktop, two on a tablet, one on a phone.
- Each card: image (16:9; 21:9 on a phone), then type label and post date in
  one line (`.eyebrow` style for the label), title, summary clamped to three
  lines. The whole card is the link.
- **Image:** the post's `hero` when set. Otherwise a tile in the CI
  gradient with the type label in white capitals at the bottom left, the same
  tile style as L13. Each type has its own direction or stop on the gradient
  so the grid does not look uniform (prototype: project updates navy, events
  navy to purple, publications purple to magenta). Event tiles also carry
  the event date (large day, small month and year) at the bottom right.
- **Featured:** a post with `featured: true` leads the "All" tab at full
  width, image left and text right on desktop. In the other tabs and while
  filtering it is an ordinary card. For events, `featured` only counts while
  the event is upcoming (P3.2).
- Light and dark themes from the tokens; no new colours.

### N5 Old URL, navigation and homepage

- **/events/:** `events.md` becomes a redirect to `/news/#events`: a page
  with `layout: null`, `<meta http-equiv="refresh" content="0;
  url=/news/#events">`, `<link rel="canonical" href="/news/">`, `<meta
  name="robots" content="noindex">` and a plain link for anyone without
  refresh. No new plugin (keep the GitHub Pages plugin list as it is).
  Leave `sitemap: false` on it.
- **Navigation** (`_config.yml`): under Media, one item "News and events"
  to `/news/`. Search the site for other links to `/events/` and point them
  to `/news/#events`.
- **Homepage "Latest":** same card style as N4 (three cards, featured
  first), with "All news and events →" to `/news/`.
- **Feed:** `jekyll-feed` stays as it is.

### N6 Backfill

- Add the P3.1 fields to the six event posts from their bodies: IGBC
  (26 Nov 2026, Mumbai), Brussels (21 Oct 2026, Brussels), Beijing
  (22 Sep 2026, Beijing), India webinar (1 Jul 2026, online), Cape Town
  (25 Jun 2026, Cape Town). COP31: the body gives the conference (9 to
  20 Nov 2026, Antalya, Türkiye) but not the session's day; set
  `location: Antalya, Türkiye`, leave `event_start` empty until H8, and
  show it in "Coming up" as "Nov 2026" with "session date to be confirmed".
- Drop "Upcoming:" from the IGBC title; "Coming up" already says it.
- Set `hero` for posts whose commented-out image already exists in
  `assets/img/posts/`; leave the rest to the type tile.

- **Done when:** /news/ shows the tabs that have posts, `/news/#events`
  opens on Events, /events/ lands there, "Coming up" lists only future
  events (and disappears when there are none), the page works on a phone at
  390 px without sideways scroll in both themes, and `docs-check` passes.

---

## Phase Q: fix the faults, then refactor without visible change

Martin, 3 Nov 2026: fix the faults found in the review of 2 November, then
refactor the code so that the site looks and reads exactly as it does now.
The design concept from that review (new grid, type scale, navigation, home
order) is **not** part of this phase; it waits for Martin's decisions. Source:
fresh-eyes review and concept, https://claude.ai/artifact/6YxdEuMy4bJ8WX496WxY3j
(sections 2, 7 and 8). Line numbers below are from commit 94b2457 and will
drift; search for the quoted code.

### Rules for this phase

These add to §0 and override rule 4 where they differ.

1. **Q1 is the only step that may change what a visitor sees.** Every other
   step must leave the site pixel for pixel and word for word as it was.
2. **Prove it with the visual check.** `visual-check/visual-check.mjs` (supplied
   with this phase, see Q0) takes full-page screenshots of 19 pages at 1440
   and 390 px in dark and light (76 shots) and records each page's title,
   description, Open Graph tags, canonical link and visible text. Shoot
   `main` before the step and the branch after it, run `compare`, and attach
   `report.md` to the pull request. A step passes when the report lists no
   differences, or for Q1 only the intended ones.
3. **One pull request per step** (Q1, Q2, … Q9), titled `Review Q<n>: <topic>`,
   merged in order. Q1 may be split into one pull request per fault.
4. **Where two variants look different, do not choose.** If merging two
   templates, classes or scripts would change how either looks, keep both,
   and add the pair to the list under "Differences left for the design phase"
   at the end of this phase. Choosing between them is a design decision.
5. **Same URLs, same feed, same sitemap.** No permalink, anchor id, RSS
   entry or sitemap entry may change. Check `/feed.xml` and `/sitemap.xml`
   by diffing the built files before and after.
6. **GitHub Pages must still build.** The repository keeps the
   `github-pages` gem and its plugin set. After each merge, confirm the Pages
   build succeeded before starting the next step.
7. **Out of scope:** Phase C content work, Circular licensing (H24), and
   anything in the design concept. If a step tempts you into a visual
   improvement, write it down instead.

### Q0 Baseline and the visual check

- **Files:** new folder `visual-check/` with `visual-check.mjs`,
  `visual-pages.txt`, `package.json` and `README.md` (supplied in
  `riselabs-q-visual-check-2026-11-03.zip`); `_config.yml`; `.gitignore`.
- Add `visual-check` to `exclude:` in `_config.yml`, like the other tools,
  so it is never published, and add `.visual/` and
  `visual-check/node_modules/` to `.gitignore`. (`.visual/` starts with a dot,
  so Jekyll skips it anyway.)
- Run `npm install` in `visual-check/` (Playwright, pixelmatch and pngjs,
  versions pinned), then `npx playwright install chromium` if no browser is
  present. Serve `main` locally with `bundle exec jekyll serve` and run
  `node visual-check/visual-check.mjs shoot http://localhost:4000 .visual/main`.
  Keep this baseline until Q1 is merged, then shoot a new one: Q1 changes
  the baseline on purpose.
- Before Q4 and Q7, also save `_site/feed.xml`, `_site/sitemap.xml` and the
  `<head>` of every page in the list, for rule 5.
- **Done when:** the tool runs, the baseline exists, and a compare of
  `main` against itself reports no differences.

### Q1 Fix the live faults (visible, intended)

Each fix is small. After it, the visual check should show changes on the
named pages only.

1. **Partner facts box.** Two different components share the class
   `.facts`: the `<dl class="facts">` label and value list
   (`_layouts/partner.html`, `_layouts/publication.html`, CSS at
   `style.css:879`) and the home page evidence list `<ul class="facts">`
   (`index.md:72`, CSS at `style.css:2875`). The later rule wins, so every
   partner page lays its labels and values across three columns ("Type, think
   tank, City / Brussels, Country, Belgium"). Rename the home list to
   `.evidence` in `index.md` and in its CSS block, and leave `.facts` to the
   `<dl>`. Expected change: the 44 partner pages show one label and value
   per row; publication pages and the home page unchanged.
2. **Card class collision.** Project cards (`_includes/projectgrid.html`,
   CSS `style.css:2228–2238`) and post cards (`_includes/postcards.html`,
   CSS `style.css:3033–3045`) both use `.pcard-meta`, `.pcard-title` and
   `.pcard-sum`; the post-card rules come later and silently restyle project
   cards. Give post cards their own names (for example `.post-card-meta`,
   `-title`, `-sum`) in the include and the CSS. Then make the project-card
   rules say explicitly what project cards inherit from the post-card rules
   today, so the project grid does not change. Expected change: none (check
   `/projects/` and the home page).
3. **News search count.** On `/news/` the search box sits inside the
   `[data-newsbar]` (`news.md:60`), so `init` attaches both `setupFilter` and
   `setupNews` to it (`ui.js:817` and `:821`). On the Events tab, typing
   "carbon" shows 5 posts while the count says "9 of 11". Let one script own
   the input: the count must count what is visible in the active tab
   ("5 of 6"). Expected change: the count on `/news/` only.
4. **Partner table search.** `setupFilter` selects `li, tr` (`ui.js:54`
   and `:75`), which includes the header row: the count reads "of 45" for 44
   partners, and the header disappears when a search does not match it.
   Select `li, tbody tr`. Expected change: `/partners/` count and header.
5. **Hero button in the light theme.** The hero always sits on a dark photo,
   but in the light theme `--btn-bg` is navy (`style.css:291`), so "Work with
   us" is navy on a navy-tinted picture and reads as plain text. Inside
   `.hero-full`, set the button tokens to the dark-theme values in both
   themes (magenta `#f92d84`, navy text `#001730`, 4.9:1; hover `#ff6ba6`),
   as tokens, not as hex values in the component rule. Expected change: the
   home hero in the light theme only.
6. **Page titles from `name`.** Partner files have `name:` but no `title:`,
   so Jekyll makes one from the file name: the tab title of `/partners/bpie/`
   is "Bpie · RISE", and `og:title` is the same. Add `title:` with the exact
   `name` value to every partner file (a script, not by hand), check whether
   people and any other collection have the same gap, and make
   `docs-check.py` require `title` to equal `name` where both exist.
   Expected change: `<title>` and `og:title` on partner pages; nothing on the
   page itself.

- **Done when:** the visual check lists changes only on the pages named
  above, each matches the expected change, and `docs-check` passes.

### Q2 Make the checker trustworthy and run it on every pull request

- **File:** `docs-check.py`, new `.github/workflows/check.yml`.
- **Fix:**
  - The partner-logo check never runs. It sits after a `continue` at the end
    of the `_want_pics` loop and uses stale `slug` and `logo` variables, so
    no logo is ever marked as referenced and 43 of the 52 "not referenced"
    notes are false. Move it into the partner loop above it (the one that
    notes "has no logo").
  - Scan `_config.yml` for asset paths too (`rise-default.png` is reported
    as unused although `_config.yml` uses it).
  - The message that names `_data/services.yml` (a file that no longer
    exists) should name the file it actually reads.
  - Remove the slug check that cannot fire (audit note: around line 244).
- **Add** (problems unless marked as notes):
  - An allowed-fields list per collection; an unknown or misspelled
    front-matter field is a problem.
  - Closed vocabularies: publication `kind`, post `type` (from
    `_data/post_types.yml`), project `status`, and partner `type` (move the
    14 values in use today into a new `_data/partner_types.yml`; the values
    and how they print stay as they are).
  - Images over 300 KB, and `<img>` without `width` and `height`, as notes.
  - CSS classes that nothing uses, and classes in markup that no CSS or
    script uses, as notes (they feed Q3).
- **Workflow:** on every pull request, check out, set up Python 3, `pip
  install pyyaml`, run `python3 docs-check.py`. The checker already exits
  with 1 on problems, so a problem fails the check. Make it a required check
  on `main` (repository settings, Martin or Mel).
- **Done when:** the workflow runs on a test pull request, the false logo
  notes are gone, a misspelled field in a test file fails the check, and the
  visual check shows no differences.

### Q3 Delete dead code and files

Delete only what the Q2 checker and a search of every template, markdown
file, data file and script prove unused. Expected visual change: none.

- **CSS:** the `.svc-*` and `.service` block (about 85 lines), `.lessons`,
  `.cols .num`, `.projects .role`, `.facts-cite`, `.person-also`,
  `.themebar-label`, `.tile`, `.pcard-img-empty`, `.xfield-img-empty`,
  `#teamlist h2` and `#teamlist h2 + .muted`, and the `.findings .engage-*`
  rules. Confirm each with a search first.
- **Templates:** the unused "list" branch of `_includes/engagement.html`
  (both callers pass `style="cards"`), the empty
  `{% if page.type == "opening" %}{% endif %}` in `_layouts/post.html`, the
  unused `all_projects` assign in `_layouts/partner.html`, and the double
  count in `_includes/partnerstats.html`.
- **Markup classes with no CSS and no script:** remove them, after checking
  `ui.js` for each.
- **Config and data:** `site.author_cite` if nothing reads it; `layout:` in
  the 11 posts (the defaults in `_config.yml` already set it).
- **Images:** the unreferenced files the checker lists, for example
  `assets/img/indicate-life-hero.jpg`, `assets/img/photos/project-gbdi-pilot.jpg`,
  `assets/img/projects/building-greenery.webp`,
  `assets/img/projects/embodied-carbon-world.png`. **Keep** the three files
  in `assets/img/hero/` named after the pillars: C1 deletes them when the
  new hero pictures arrive.
- **Keep** the post field `format` (P3.1 defines it, even though nothing
  prints it yet) and `hero_tone` (the checker notes it as unused, but it is a
  deliberate opt-out).
- **Done when:** the visual check shows no differences, `docs-check` passes,
  and the pull request lists what was removed and the bytes saved.

### Q4 Split the stylesheet into Sass layers

- **Files:** `assets/css/style.css` → `assets/css/style.scss` (front matter
  `---` / `---`, then `@import` lines) and partials in `_sass/`; `_config.yml`.
- **Layers, in this order:** `_tokens` (custom properties, both themes),
  `_fonts`, `_base` (reset, type, focus, skip link), `_layout` (wrap, band,
  grid, article), `_components/*` (one partial per component: card, people,
  partners, facts, figure, filter, tabs, reel, hero, footer, nav, cite, map
  …), `_pages/*` (home, expertise, approach, team, partners, news), `_utilities`,
  `_print`.
- **Keep the cascade.** Move rules without reordering them across files
  where the order matters: when two rules of equal specificity set the same
  property, the one that wins today must still come later. Fix nothing while
  moving; Q1 has already fixed the known collisions.
- **Tokens only.** Replace the 27 hex values and 26 `rgba()` values written
  outside `:root` with existing tokens where the value is identical, or a new
  token where it is not. The value on screen must not change.
- **Output:** set `sass: { style: compressed }` in `_config.yml`. The
  comments stay in the partials, where they are useful, and drop out of what
  visitors download (114 KB to about 60 KB). Keep the `?v=` cache-busting
  query in `_layouts/default.html` pointing at `/assets/css/style.css`.
- **Watch the Sass version.** GitHub Pages compiles with an old Sass
  (LibSass through `jekyll-sass-converter` 1.x), which can misread CSS's own
  `max()`, `min()` and `clamp()` (used 18 times, for example
  `max(16px, env(safe-area-inset-left, 0px))`) as Sass functions. Wrap any it
  rejects in `unquote("…")`, and compare the compiled CSS with the old file.
- **Done when:** the visual check shows no differences, the compiled CSS is
  smaller, the Pages build succeeds, and `docs-check`'s CSS checks (brace
  balance, duplicated runs) read the partials.

### Q5 Shared includes where the output is the same

Replace copies with one include wherever the HTML they produce is the same,
or differs only in ways no visitor can see. Expected visual change: none.

- `_includes/more-link.html` for the 28 "more" links (the arrow written once,
  in CSS or in the include, instead of "→" ×19 and `&rarr;` ×9 in the
  sources; the arrow a visitor sees must stay the same character).
- `_includes/back-link.html` for the five back links; move their inline
  `style="margin-top:2.5rem"` into a class.
- `_includes/date.html` with the formats in use today (long, short, tile),
  each producing exactly today's text. Note that `%d` and `%-d` both occur
  today; keep each where it is used, or list the difference under the
  design phase.
- `_includes/page-head.html` for the 13 narrow and 2 wide page heads,
  producing the same markup. Move the page head inside `<main id="content">`
  so the "skip to content" link lands on the page title; check that the
  move changes nothing on screen.
- Vocabularies read from `_data/` instead of being typed into templates:
  publication kinds (`publications.md` and `publist.html`), strand names
  (`expertise.html`, `approach.md`, `engagement.yml`), theme and post-type
  lookups (three copies each), city and country formatting (three copies).
- Project pages compute publications, posts and related projects once
  (today twice, in `_layouts/project.html`). The hand-built related tabs on
  project pages and `_includes/related.html` differ in panel names, heading
  level and labels: keep both and list the pair (rule 4).
- **Done when:** the visual check shows no differences, and the pull request
  lists every include added and every copy it replaced.

### Q6 One script for filters and tabs

- **Files:** `assets/js/ui.js` → `_includes/js/*.js`, joined by a new
  `assets/js/ui.js` with front matter that includes them in today's order.
- Split by job: `core`, `nav`, `theme`, `filter`, `tabs`, `collapse`,
  `staleness` (coming up and openings), `reel`, `hero`, `map`, `cite`,
  `external-links`.
- Replace the four controllers that each show one value and hide the rest
  (`setupTabs`, `setupKinds`, `setupNews`, `setupThemes`) and the text filter
  with one controller that each page configures through data attributes. It
  must reproduce today's behaviour on each page exactly: which buttons
  exist, which is active on load, hash in the address bar, counts, the empty
  message, and the ARIA states each page has now. Where the four differ
  today (full tab roles on one, `class="on"` on others, hash on some), keep
  each page's current behaviour and list the difference (rule 4).
- The two date-based hiders (`setupComingUp`, `setupOpenings`) become one.
- The team reel: one resize handler instead of two plus a ResizeObserver;
  same movement.
- Without JavaScript every page must look as it does today with JavaScript
  off.
- **Done when:** the visual check shows no differences with JavaScript on,
  a second run with JavaScript off (Playwright `javaScriptEnabled: false`)
  matches a baseline taken the same way, and every filter, tab and search is
  tried by hand on `/news/`, `/publications/`, `/projects/`, `/partners/`,
  `/team/` and a project page.

### Q7 One data schema

- **Files:** a one-time `migrate-fields.py` at the root (excluded in
  `_config.yml` like the other scripts, deleted after the merge); every collection; the
  templates that read the renamed fields; `docs-check.py`; `docs/03`.
- **Renames** (same meaning, new name; the script does all files at once):

  | Collection | Today | After |
  | --- | --- | --- |
  | people | `portrait` | `image` |
  | publications | `thumbnail`, `thumbnail_credit` | `image`, `image_credit` |
  | partners | `logo` (file name only) | `logo` as the full path |
  | projects | `hero` where it equals `image` (14 of 15) | removed; `image` is used. Where they differ, `hero` stays as an override |
  | projects | `years` ("2024–2026", sorted as text) | `start_year`, `end_year` (numbers); the page prints exactly today's text |
  | all | `hero_caption`, `image_credit`, `thumbnail_credit`, `credit` | one `image_credit` and one `image_caption` per item |

- Where two fields may not mean the same thing (people `summary` and
  `tagline`; people `affil` and `org`), do not merge them: list them for
  Martin.
- **One change that is not visible on the page but is visible elsewhere:**
  jekyll-seo-tag reads `image`. Renaming publication `thumbnail` to `image`
  gives every publication page an `og:image` (its title page) where today
  link previews show the site default. Ask Martin before merging (H40); if
  he says no, set the publication pages' Open Graph image explicitly so it
  stays as it is.
- Sorting must not change: compare the order of `/projects/`,
  `/publications/` and the home page bands before and after.
- After the migration, `docs-check` refuses the old field names.
- **Done when:** the visual check shows no differences, the text check shows
  only the approved `og:image` change (or none), and `docs/03` documents the
  new names.

### Q8 Lighter images

- Re-encode the 11 images over 300 KB (largest:
  `assets/img/projects/eu-stock-by-country.png`, 2.4 MB) as WebP at 200 KB or
  less, at the same pixel size. Keep the originals out of the repository
  only after Martin confirms he holds them elsewhere.
- Add `width` and `height` to every `<img>` in the templates, from the file's
  real size, so pages stop shifting while they load.
- Re-encoding moves pixels slightly. For this step only, the visual check
  may show small differences inside pictures; look at each diff image and
  confirm that only picture areas changed, never text or layout.
- `srcset` for large pictures is left for the design phase.
- **Done when:** no image is over 300 KB, the checker's image notes are
  gone, and the diff images show changes inside pictures only.

### Q9 Docs that match the code

- Rewrite `docs/02-site-map-and-structure.md`, `docs/03-editing-the-site.md`
  and `docs/05-design-basis.md` from the code as it now is. Known drift: the
  team page described as hidden, counts of 38 publications and one person,
  `services.md` and `_data/services.yml` (gone), `tags` instead of `themes`,
  "only `current` projects reach the home page", fonts listed as Figtree
  only, "nothing is stored on the device" (the theme choice is), and
  `.tile`, which no longer exists.
- Let `docs-check.py` write the counts (projects, publications, people,
  partners, posts) and the repository tree into a marked block of `docs/02`,
  so they cannot drift again.
- Move the long design reasoning out of the CSS comments into `docs/05`
  where it explains a rule, and keep a one-line pointer in the partial.
- **Done when:** a new implementer could follow `docs/03` to add a project,
  a publication, a person and a post without reading the templates.

### Differences left for the design phase

Fill this list during Q4 to Q7 (rule 4): each pair of variants that look or
behave differently, where they are used, and how they differ. It becomes the
input for the design phase. Known so far:

- Project-page related tabs vs `_includes/related.html` (panel names,
  heading level, labels).
- The four filter and tab controllers (ARIA roles, active-state class, hash).
- Date formats `%d` and `%-d`.
- Eight card types, seven image fallbacks, five button styles (review,
  section 7).
- The project card's three-line summary clamp (Q1.2, 4 Nov 2026). Project
  cards are clamped to three lines and set a size larger than their own
  rules said, because the post-card block shared their class names and won.
  The values are now written in the project rules, so the grid looks exactly
  as it did; whether a project card wants a clamp at all is a design
  question.
- The home page evidence band's hairlines and type size (Q1.1, 4 Nov 2026).
  That band has a 1px rule above and below it and is set at `.93rem`, and
  neither was ever written for it: it took all three from the key-facts
  `<dl>` while it shared that class. The rename would have dropped them, so
  `.evidence` now sets them itself and the band looks exactly as it did.
  Whether it should keep them is a design question, not a refactoring one.

---

## Human input

Items the implementer cannot resolve. Ask, and do not guess.

| ID | Needed from | Question | Blocks |
| --- | --- | --- | --- |
| H0 | Martin (repo and DNS admin) | Fix the custom-domain DNS and certificate in GitHub Pages | P1.0 |
| H1 | Martin | ~~Same document, and the author name form~~ Answered 29 Oct: one entry with the Zenodo DOI; the name is "Bjørkskov KBR" | P1.1 |
| H2 | Martin | ~~Source for "up to 150% by 2050 … five billion square metres per year"~~ Answered 29 Oct: the Global Status Report for Buildings and Construction 2025-2026, UNEP and GlobalABC. Figures restored with the link | P1.5 |
| H3 | Barbara | Employer answered 29 Oct: RISE. Still needed: tagline, bio, portrait, links, approval | P2.1, P1.7 |
| H4 | Nicole | Draft by Martin in progress. Needed: approval of the text, portrait, links; EPFL clearance if required | P2.1 |
| H5 | Zuhaib | Draft by Martin in progress. Needed: approval of the text, portrait, links; EPFL clearance if required | P2.1 |
| H6 | Martin | Date from which Nicole and Zuhaib are RISE employees, if and when that happens | P2.1 label |
| H7 | Martin or Barbara | Run `fetch-abstracts.py --write` and review the diff | P2.6 |
| H8 | Martin | ~~Dates, places and registration links for event posts that lack them, starting with the COP31 session~~ Answered 3 Nov for COP31: two sessions, both 16 Nov, 10:00-11:00 at the Finland Pavilion (GlobalABC and RICS) and 14:00-15:00 (RICS, WBCSD, GBDI, GlobalABC, presenting CLEAR). Still open for other posts, and no registration links yet | P3.1, N6 |
| H9 | Martin | ~~Standing text for `/join/`~~ Drafted 29 Oct and live on the page as "Other ways in": theses, visiting researchers, fellowships. Reword freely | P1.7, P3.4 |
| H10 | Martin | Consent from Bárbara Rodríguez Droguett to publish her quote | P3.5 |
| H11 | Martin | Own photos with permission to publish | P4.1 |
| H12 | Martin | New slugs for the three projects with truncated names | P4.2 |
| H13 | Martin | German text for `/de/` | P5.2 |
| H14 | Martin | ~~End year and Croatia~~ Answered 29 Oct: ends 2026; Croatia takes part | P1.6 |
| H15 | Martin | The job posts for November 2026: title, text, and the opening fields in P1.7 | P1.7 |
| H16 | Martin | ~~Colour or black and white~~ Answered 29 Oct: black and white until harmonised headshots of all team members exist. Still open: the shoot itself, and a group photo if wanted | L3 |
| H17 | Martin | ~~Short testimonial versions~~ Answered 29 Oct: approved; texts in L9 | L9 |
| H18 | Martin | ~~Approve the shortened profile text~~ Answered 29 Oct: approved unchanged; use `martin-roeck-body-draft.md` as supplied | L18 |
| H19 | Martin | ~~Light-theme duotone~~ Answered 29 Oct: ramp A, the CI's magenta → blush (first answered B, then changed to A the same evening) | R7 |
| H20 | Martin | ~~Three title pages are CC-BY-NC-ND~~ Answered 30 Oct: RISE can use them. All three are installed with their CC-BY-NC-ND credit | R6 |
| H21 | Martin | ~~Analytics tool~~ Answered 29 Oct: Plausible. Still needed: the account and setup steps in R10, the snippet, and the plan after the 30-day trial (Business for user journeys) | R10 |
| H22 | Martin | ~~Circular licence~~ Answered 29 Oct: licensed for web and desktop use; switch to Circular | R3 |
| H23 | Martin | To do, later: PDFs for the EU roadmap and DG GROW reports, IEA EBC Annex 72, TU Graz and the MDPI papers, so their tiles can become title pages. Designed tiles stay as placeholders until then | R6, R11 |
| H24 | Martin | The Circular WOFF2 web files (Book, Medium and italics) and any notice the licence requires. **Partly answered 29-30 Oct**: files supplied, but Medium only and licensed for another domain. Still needed: the Book cut, and riselabs.at on the licence (or the move to riseregenerate.com). See the implementer's note below | R3 |
| H25 | Martin or a lawyer | Approve the Datenschutz section for Plausible (`drafts/datenschutz-plausible-draft.html`), including whether consent is needed | R10 |
| H26 | Norman Chinasamy | Approval of his profile text and portrait (live as a draft since 235b9a8); UCT clearance if required | R8 |
| H27 | Martin | ~~Independent review work~~ Answered 31 Oct: dropped, not an offer RISE sells. The Methods field in `drafts/expertise.yml` no longer mentions review (lede, bullets and note rewritten); W5 removes the line from Approach | W2, W5 |
| H28 | Martin | ~~A photograph for "Bio-based and regenerative materials"~~ **Answered 31 Oct 2026**: straw-bale infill in a timber frame, supplied by Martin. Filed as `expertise-biobased-materials.jpg`, credited "Hyllie. Image: Ecococon" | W2 |
| H29 | Martin | ~~Approve the wording~~ Answered 31 Oct: approved, including Methods moving to the wide strand | W1, W2 |
| H30 | Nicole, Zuhaib, Norman | Confirm their list is complete and correct, and name anything to leave out. Norman's public ORCID record is empty; his six entries come from Crossref and OpenAlex. Zuhaib: two items were left out on purpose (an amphibian-biology paper misattributed to "Sheikh Zuhaib" in OpenAlex, and a correction notice); is he an author of the 2022 Global Status Report or the BPIE EU Buildings Climate Tracker (2022)? Neither names him publicly | E1 |
| H31 | Martin | ~~"With RISE or GBDI" filter~~ Answered 31 Oct: no; removed in M1 | E3, M1 |
| H32 | Martin | ~~Pick one fact per perspective~~ Answered 31 Oct: combined picks, texts in `_data/facts.yml` | F1 |
| H33 | Martin | ~~New lede for the facts band~~ Answered 31 Oct: text in F1 | F1 |
| H34 | Martin | ~~Climate Lab permission~~ Answered 2 Nov: Martin decided to publish both Climate Lab photos with credits "Climate Lab / Fetz" and "Climate Lab", at his own risk | T1 |
| H35 | Martin | ~~Own photos, consent, credit~~ Answered 2 Nov: supplied; all six in the team photo consented; team photo by Rue Munemo | T1 |
| H36 | Martin | The post categories used on social media, so the types in `_data/post_types.yml` can match them | N1 |
| H37 | Martin | More imagery from RISE projects and activities for the home hero carousel. It runs on three pictures today, one per brand pillar, and the same three on every visit. Wanted: photographs of the work and the people doing it, roughly 2.2:1 or croppable to it, each with the pillar it belongs to, who took it, and whether it may be published | C1 |
| H38 | Martin | A pass over the 15 projects one by one: the description, the visual assets, and the reports and other outputs to link. Gaps found so far are listed in C2. Needed per project: whether the summary and body still read correctly, a photograph where the picture is currently a diagram, and the URL of every public report, dataset or tool that belongs to it | C2 |
| H39 | Martin | Photographs of Die HausWirtschaft, once RISE is there or has permission to publish the cooperative's own. One 16:9 and two 3:2, with the credit for each, as in T1. ~~Also: which spelling?~~ Answered 4 Nov: Martin does not mind; the site uses "Die HausWirtschaft" throughout, which is the form in the job adverts and on the house's own English page | T2 |
| H40 | Martin | Publication pages get an Open Graph image (their title page) when `thumbnail` becomes `image` in Q7; today link previews show the site default. Yes, or keep the default? | Q7 |

---

## Phase C: imagery and project content

Martin, 2 Nov 2026: two content jobs rather than build jobs. Both are
blocked on material only Martin can supply, so neither is a thing the
implementer can start alone. The gaps are counted here so the asking is
specific.

### C1 More pictures in the home hero

`_data/hero.yml` holds three entries, one per brand pillar (System change,
We are nature, Stronger together), and the hero crossfades between them.
Three is the minimum that makes a carousel rather than a still, and all
three are the same on every visit.

- Martin supplies photographs from projects and activities (H37). Each needs
  the pillar it illustrates, the credit line, and clearance to publish.
- **Then:** add them to `_data/hero.yml` in pillar order, cropped to roughly
  2.2:1 as the file's own comment requires, and check the hero at 390 px and
  on desktop in both themes.
- No change to `_includes/hero.html` is expected: it already loops the file.
  If the list grows past about six, revisit whether every image should load
  on first paint.
- `assets/img/hero/` still holds three unused files named after the pillars
  (`system-change.jpg`, `we-are-nature.jpg`, `stronger-together.jpg`), the
  earlier set, all 16:9 rather than the 2.2:1 the hero wants. They are not
  RISE's own pictures. Delete them once the real ones arrive, so the folder
  does not read as if the carousel had six.

### C2 Project-by-project content pass

Fifteen projects in `_projects/`. What the files look like today, counted on
2 Nov 2026:

- **Outputs:** 5 of 15 carry an `outputs:` list (Agora Leitmärkte, the EU
  life-cycle GHG analysis, CollaborativeCarbon, PEF4Buildings, RELIVING).
  The other 10 link nothing: GBDI, GBDI China and India, the Global Status
  Report, the Global WLC Tracker, Annex 72, INDICATE, INDICATE-LIFE, the
  Chile harmonisation, the modelling framework, and the EU embodied-carbon
  benchmarks.
- **Hero pictures:** all 15 have one, but 9 are diagrams or charts rather
  than photographs (the `.png` heroes, plus the GBDI platform screenshot).
  That is honest, and for some projects a figure is the right picture, but it
  means the project grid reads as a wall of charts.
- **Captions:** 13 of 15 have `hero_caption:`. CollaborativeCarbon and
  PEF4Buildings do not.
- **Descriptions:** body length runs from 29 lines to 161. The short ones
  are the older entries.

Work, once Martin has been through them (H38): correct the summary and body
where he marks them, swap in photographs where he supplies them, fill the
two missing captions, and add `outputs:` entries with real titles and URLs.
Rule 2 of §0 still holds: no invented titles, numbers or DOIs, so a project
gets an outputs list only when Martin gives the links.

- **Done when:** every project Martin has signed off reads as he left it,
  `docs-check` passes, and no project links an output that does not resolve.

---

## Implementer's notes

Added by whoever is doing the work, as things are found. Facts only, each
with the date and where it came from.

### The expertise pictures: H28 closed, and the band that stayed plain

Two things on /expertise/, both on 31 October.

**H28 is answered.** Martin supplied the bio-based photograph - straw-bale
infill in a timber frame under a CLT deck, before the linings go on. It is
cropped to the 3:2 the page frames every field picture at, from the top, so
the browser is not asked to throw away half a portrait on every load. That
was the last field falling through to the R11 placeholder, so no field uses
it now.

The building is Hyllie and the image came from Ecococon (ecococon.eu), which
Martin confirmed later the same day. The credit reads "Hyllie. Image:
Ecococon" and nothing beyond that is claimed here: who took the photograph is
not known at this end, and `Image:` rather than `Photo:` is the honest form
for a picture that was supplied rather than shot by the named party. It is
not RISE's own work, so the credit is required rather than optional.

**The whole "scaling deep" band was rendering plain**, which is what Martin
noticed. The `.tone` wrapper that carries the picture treatment was written
as `{% if x.image_credit %}`, so it only reached pictures that happened to
have a credit line. The six fields under "scaling up" and "scaling wide" are
Unsplash photographs and all carry one; the two under "scaling deep" are the
only ones that do not, so exactly that band missed the treatment. The credit
says who took the photograph and the wrapper carries the treatment, and the
two have nothing to do with each other; the wrapper is now unconditional.

Worth saying plainly: this was not a rule that did the wrong thing, it was
two unrelated things tied to one condition, and it held for weeks because the
fields that proved it were the ones nobody looked at twice.

### The picture treatment, and where it stops (Martin, 29-31 October)

Black and white plus a navy tint (`--photo-tint: #16325a`, option B of four
that Martin compared on 31 October). It reaches figures wrapped in `.tone`,
project cards and portraits. Three things it deliberately does not reach:

- **Heroes.** Measured, not guessed: tinting the hero bed takes the
  standfirst from 8.45:1 to 4.23:1, below the 4.5 AA needs, and the h1 from
  2.82:1 to 1.12:1. The hero keeps its own treatment.
- ~~**Eight project heroes** that are maps, charts or screenshots.~~
  **Reversed 31 Oct 2026.** Those eight carried `hero_tone: false`, and
  Martin dropped all of them: one consistent surface, every card toned. It
  surfaced because the home page selection changed the same evening and
  INDICATE LIFE's map appeared in colour among five toned cards. The cost is
  real and was accepted: the EU stock map's country colours and the INDICATE
  pilot regions are now shades of grey. The `hero_tone` lever still exists
  and nothing uses it, which `docs-check.py` notes.
- **Charts and logo tiles**, which were never in it.

Two borderline images were put to Martin on 31 October and he chose to treat
both: the UNEP Global Status Report cover, which is another organisation's
branded artwork, and the ISS aurora photograph, whose whole subject is
coloured light. Neither carries `hero_tone`.

Portraits needed a wrapper to carry the overlay at all. A pseudo-element
never renders on a replaced element, so `img::after` draws nothing; the
portrait is now inside `<span class="pc-shot">` in `peoplelist.html` and
`_layouts/person.html`.

### RISE is listed among a project's organisations (Martin, 31 October)

Project pages named every organisation on a piece of work except the one
whose site this is, which read as though the work had nobody behind it. RISE
now leads the tile block and the sidebar row.

Three decisions, all Martin's on 31 October:

- **The tile points at the home page.** RISE has no file in `_partners/` and
  gets none: that would give it a partner page duplicating the home page, and
  list RISE on /partners/ among the organisations we work *with*. The key
  `rise` is special-cased in `_includes/partners.html` and
  `_includes/partnernames.html`, and the cross-reference check in
  `docs-check.py` skips it for the same reason.
- **Only where RISE existed.** A project lists RISE when it ran to 2023 or
  later with a core RISE person on it, which is the test `rise_tier` uses on
  publications. Thirteen of fifteen qualify. PEF4Buildings (2017-2018) and
  Towards embodied carbon benchmarks (2021-2022) ran entirely before RISE was
  founded and keep the lists they had. `docs-check.py` fails a project that
  gets this wrong in either direction, or that lists `rise` anywhere but
  first; all three failures are tested.
- **"Partners", not "Collaborators".** The heading and the sidebar label
  changed, because RISE is not a collaborator on its own work and the word
  had to cover both. It is also already the site's word for these
  organisations: the page is /partners/ and the link under the block reads
  "All partners".

One exemption, decided the same day. IEA EBC Annex 72 qualifies on its last
year alone, and with no other partner files its block read "Partners: RISE".
Martin's call: that project should list no partners at all, RISE included,
because the consortium is 27 countries and any list short enough to show
would be a selection nobody made on purpose. `partners_omitted: true` in its
front matter is the deliberate exemption; `docs-check.py` honours it, and
fails it if the project still lists partners or drops the `partners_note`
that has to say why the names are missing. The sidebar row shows that note
where the names would have gone.

Publications were left alone. They carry their own `partners` lists and the
same question applies to them, but adding RISE to twenty-four files is a
separate decision and nobody has made it.

### R1 is reversed: dark is the default again (Martin, 31 October)

R1 made light the default on 29 October. Martin reversed it on 31 October:
dark is what the markup ships and what a visitor without a stored choice and
without a light system setting gets. Both themes still have to work equally
well, which is the half of R1 that stands.

Three things moved, and nothing else: `data-theme="dark"` on `<html>`, the
inline `<head>` script now testing `prefers-color-scheme: light` instead of
`dark`, and `docs/02` and `docs/05` rewritten to match. The stylesheet needed
no reordering: `:root` already carried the dark values with
`[data-theme="light"]` overriding them, which is how R1 was built.

Two things that were wrong under the light default and are now right:

- The toggle's markup in `_layouts/default.html` still shipped
  `aria-pressed="false"`, `title="Switch to the light theme"` and the label
  "Light". Under a light default a visitor with JavaScript off saw a button
  offering the theme they were already on. R1 changed the attribute but not
  the button, and this reversal fixes it by accident rather than by design.
- The `matchMedia` test was negated rather than written for the theme it
  selects. A browser with no `prefers-color-scheme` support answers false to
  every such query, so under the old code it fell through to the markup's
  light, which was also the default and so looked correct. Written the new
  way it has to be explicit, and it is: the query asks for `light`.

Added since: each theme block carries `color-scheme`, so the sort select on
/publications/, text inputs, scrollbars and the focus ring follow the theme.
Without it the browser draws its own furniture in the system's scheme, which
on a dark default is a light-grey select on a navy page. This was missing
before the reversal too; the dark default is what made it visible.

### The system setting is no longer read (Martin, 3 November)

The 31 October reversal left one step in front of the default: a visitor
with no stored choice got their operating system's `prefers-color-scheme`,
and only fell through to dark if that said dark or said nothing. Most people
run their machines light, so most first visits were light. The site had a
dark default that almost nobody met.

Martin, 3 November: dark by default, full stop. The `matchMedia` branch is
gone from the inline `<head>` script, which now reads the stored choice and
nothing else, and the script is six lines shorter for it. Everything else
stands: `data-theme="dark"` in the markup, the toggle, the `rise-theme` key,
the before-paint read that stops the flash, and the Datenschutz section that
discloses the one word stored.

What this costs is worth writing down rather than discovering later. A
system set to light is a statement about how someone reads, sometimes a
medical one, and this site now ignores it on the first visit and asks them
to find a button in the bottom-right corner instead. The toggle has to stay
visible and reachable for that reason; it is no longer a convenience but the
only way to light. Both themes still get checked on every change.

### The home page cut its publications before they were ordered (3 November)

Martin asked for six publications on the home page instead of three, 3x2 on
a desktop and 2x3 on a phone. The count was the ask; the order was the bug
found on the way.

The band read `site.publications | sort: "year" | reverse | slice: 0, 3`.
That sorts on year and nothing else, so inside the newest year it took
whichever three the build emitted first. On 3 November that was
`alaux-2026`, then `batra-2026`, which is a wider-team paper, and only then
`disanto-2026`: a wider-team paper above six of RISE's own, which is exactly
what E3's tier order exists to prevent. The tier order lives in
`publist.html` and was never reached, because the list had already been cut
before it got there. The publications page was always right; only the home
page was cutting first.

`publist.html` takes `limit` now, applied after the year-and-tier rebuild,
and the home page passes the whole collection with `limit=6`. The six that
render are all 2026 and all `core`.

Two things worth knowing about that selection. Seven 2026 papers are
`core`, so one of them is not on the page, and which one is decided by the
build's order inside the year, not by anything meaningful: these files carry
a year and no month, as `publist.html` has said all along, so there is no
recency to sort on and nothing invents one. If a particular paper has to be
on the home page, that needs a `featured` flag or real dates, and both are
Martin's call rather than something to assume.

`docs-check` now fails any page that slices `site.publications` outside
`publist.html`, because this is a silent failure: it renders six perfectly
good cards in the wrong order, and nothing looks broken.

### The home page band: Martin's own work, and a featured flag (3 November)

Two changes to the six publications on the home page, both from Martin the
evening the six went live.

**Only publications he co-authored, for now.** The filter reads `people`,
which is safe to use for this: on the day it was written, all 41 entries
listing `martin-roeck` carried "Röck M" in `authors` and all 41 carrying
"Röck M" listed him. `docs-check` notes any entry where the two stop
agreeing, as a note rather than a failure, because an entry where he
contributed without being a named author is legitimate and only means the
band's description no longer matches what it shows. "For now" is Martin's
word: removing the filter is removing one `where_exp`.

**The filter does not do what it was expected to do.** Martin asked for it
expecting it would bring the Alaux pathways paper back into the six. It does
not, and it cannot: all seven of the 2026 `core` papers are his, so the
filter removes nothing from the newest year and the same six render either
way. What kept that paper off the page was never authorship. Seven papers
fit six slots, and the one that fell off was decided by the build's order
inside the year, which the live site confirmed on 3 Nov to be the reverse of
the alphabet, putting `alaux-` last of seven.

So the paper is on the page by `featured: true`, which is how `featured`
already works for projects and posts on this same page. It applies only
where a list is cut, which today is the home page and nowhere else: on
/publications/ a paper jumping its year would read as a sorting bug rather
than a choice, and that page is unchanged, with Alaux still fourth among the
2026 articles. Verified in both places.

A featured publication leads the band rather than keeping its date position,
which follows the projects precedent. The alternative, where featuring only
guarantees survival, is a few lines away if Martin prefers it.

`docs-check` notes when more than three publications are featured: past
that, a band of six stops being recent work and becomes a fixed list.

### Light is the default again (Martin, 4 November)

The fourth setting of this switch, and the second in two days. The order,
because four commits are worse than one paragraph: light until 29 October,
dark from 31 October, dark without reading the system from 3 November, and
now light with the system read again.

What it does now: a stored choice wins, then `prefers-color-scheme: dark`,
then the markup's light. `data-theme="light"` ships in the markup, so that is
what a visitor without JavaScript sees, and the toggle button ships the state
that goes with it rather than the one it replaced.

Checked in Chromium across every system setting (light, dark, none) against
every stored value (none, light, dark, junk), and with `localStorage`
throwing outright under both system settings: fourteen cases, all landing
where they should, no page errors.

One thing to know before moving it a fifth time: the stylesheet is not what
sets the default. `:root` carries the dark values and `[data-theme="light"]`
overrides them, so the default lives in the markup and the inline script, and
the token blocks stay as they are either way.

Q1.5, the hero button in the light theme, matters more now than when it was
written: the fault it describes is on the home page every visitor meets by
default rather than only the ones who chose light.

### Q1.2 to Q1.6, and what the measuring found (4 November)

Five faults in one pull request. Three of them were worse or wider than the
order described, and the measuring is what showed it.

**Q1.2, the card classes, collided in both directions.** The order says the
post-card rules silently restyle project cards, which they did: project
cards rendered at 700 weight, 1.05rem titles and a three-line clamp that
their own rules never asked for. But the project block is written first, so
it kept every property the post block did not set, and post cards were
taking `margin: .75rem 0 .25rem`, `text-transform: uppercase` and
`letter-spacing: .05em` from it. The uppercase is the visible one: a post
card's date reads "3 NOVEMBER 2026" because of a rule written for project
years. Renaming alone would have changed both card types. Both blocks now
state what they actually render, and all 434 computed properties of all six
spans match before and after.

**Q1.3 broke the search box on the way to fixing the count.** Taking
setupFilter off the news input left nothing to reveal it: the box ships
`hidden` so it never appears as a control that does nothing, and setupFilter
was what cleared that. Caught by driving the page in a browser rather than
reading the diff. setupNews reveals it now.

**Q1.6 was not only the partners.** `_people` has the same gap, six files
with `name` and no `title`, and there it costs more than a capital letter:
/team/martin-roeck/ was "Martin Roeck" in the tab and in og:title, with the
umlaut gone, because Jekyll was building the title out of the file name.
`add-titles.py` writes `title` next to `name` in all fifty files and
docs-check keeps the two equal.

**Q1.5 is worth a figure.** The fault is not the label on the button, which
was always fine; it is the button against the photograph. In the light theme
the navy button on the hero's navy-tinted picture measured **1.30:1** at its
own edge. It is 4.11:1 now, which clears the 3:1 that a UI component's
boundary needs. The hero redefines the `--btn-*` tokens for its own scope
rather than writing a hex in the rule, and `#ff6ba6` became
`--magenta-light` so the third place that needs it does not copy it again.

### H24, Circular: the files supplied on 29 October do not cover this site

Four files arrived with the pack: `CircularXXWeb-Medium` and
`CircularXXSub-Medium`, each as WOFF and WOFF2, plus Lineto's
`stylesheet.css`. Two things block R3's typeface switch.

**The licence names another domain.** The disclaimer in Lineto's own
`stylesheet.css` reads: "These Web fonts are licensed exclusively for the use
on the following domain(s) and their subdomains: www.riseregenerate.com
(monthly pageviews: <50K)". This site is riselabs.at, which is neither that
domain nor a subdomain of it, so serving these files from riselabs.at would
fall outside the licence. Needed: riselabs.at added to the licensed domains.

**Only one cut, and no italics.** Both files report weight 500, upright, in
their own metadata (`OS/2.usWeightClass` 500, `head.macStyle` bit 1 clear).
R3 asks for Book (400) for body text and Medium (500) for headings, with
`font-synthesis: none`, so with these files alone the body text has no face
to render in. The "Sub" file is a 470-glyph subset of the 755-glyph "Web"
file, not a second weight. Needed: the Book cut, and the italics if they are
wanted.

Until both are resolved the site stays on Figtree, which is what the order
above says to do while the files are missing. `assets/css/style.css` keeps
the `@font-face` block and the `--font` token together at the top of the
file, so the swap is those two edits and nothing else.

### W1 was already built, from the PDF, before v4 of this order arrived

Shipped in PR #26 on 29 October against the proposal document. v4 then put
the same task in writing here. The two agree except in three places, all
resolved in favour of this order on 30 October:

- `short_title` for `towards-embodied-carbon-benchmarks-for` was "Towards
  Embodied Carbon Benchmarks"; now "European embodied carbon benchmarks".
- `short_title` for `global-building-data-initiative` was "GBDI pilot"; now
  "GBDI".
- The checker's cap on `short_title` was 34 characters, which rejected the
  first of those at 35. It is 38 now. The cap was a number picked by eye, not
  a measured limit, so the supplied value won.

Two things W1 asks for are deliberately not done yet, because W2 is what
needs them:

- The `style="list"` branch of `_includes/engagement.html` is still there.
  v4 says to drop it "which nothing uses after W2", and /expertise/ still
  uses it today.
- `docs-check.py` already fails an unknown slug in `engagement.yml`
  `examples`, which W1 and W4 both ask for.

### W2 was blocked and is not any more (31 Oct 2026)

`drafts/expertise.yml` was missing from both earlier packs. W2 needs the
eight fields' own contents, which the order quotes only the headings of, and
writing them would have meant inventing claims about what RISE does, which
rule 2 forbids. The packs of 31 October carry it, identically in both. W2,
R7 and R11 are built. `drafts/engagement.yml` arrived too and was not needed:
W1 shipped from the proposal document, which quotes all four cards in full.

### Four places where the built site differs from this order, and why

**F1, the single-column breakpoint.** The order says "3 columns from 64rem, 2
below, 1 under 30rem", and also "2 x 3 at 390 px". 390px is under 30rem, so
the two cannot both hold. The acceptance test won: the single column starts
at 22rem, so two columns hold down to 360px.

**R7, where the photo credits sit on the two GBDI projects.** The order says
each photograph carries its `image_credit` in small text. The project layout
has no such field; it prints `hero_caption`. Both projects already had one,
describing the diagrams these photographs replaced, so those captions had to
change anyway. The credit went there rather than into a new field nothing
renders.

**R7, the treatment is black and white with navy in the shadows, and it is
on.** The order describes a magenta-to-blush duotone kept off. Martin asked
on 31 October for a simple black and white with a subtle navy tone instead,
and picked it from a sheet of four rendered on five real photographs: a
`lighten` layer with #16325a. The CI's own #001730 was tried first and moved
almost nothing, because it is darker than the shadows in most of these
pictures. One tint in both themes. `photo_treatment: plain` turns it off.

**M2, the card in the row.** The order says "the existing person card". The
prototype shows that card stood up: portrait full width as a 1:1 crop, text
under it, no card chrome. The prototype won, since the order names it as the
reference. The grid on /team/ is untouched.

### M1: the missing text on Martin's phone is almost certainly a content blocker

Not confirmed on a device, and it cannot be from here. But the symptom is
exact: the covers rendered and the text did not. The classes were `pub-text`,
`pub-title`, `pub-thumb`. `pub` is the French word for advertisement, and the
widely used filter lists hide elements whose class contains it. A rule
catching `pub-text` and not `pub-thumb` produces precisely what the
screenshots show.

The classes are `cite-` now. If the text is still missing after this, the
next thing to rule out is the browser itself, not the markup.

### What the title-page and abstract work actually found (31 Oct 2026)

Counts and abstracts came from the sources through a browser tab, since this
environment cannot reach api.openalex.org, api.crossref.org or
api.zotero.org.

- **Counts: 54 of 64**, from OpenAlex. Not Google Scholar, which has no API,
  does not permit scraping, and whose counts are not RISE's to republish.
  Four Zenodo records answer with the concept DOI rather than the version DOI
  the site holds; each was confirmed separately rather than inferred.
- **Abstracts: 50 of 64.** OpenAlex 42, Crossref 0 - it holds none for any of
  the 21 OpenAlex missed, which is normal for Elsevier and Springer deposits
  - and the RISE Zotero group library 8. Finding those eight meant paging all
  6,996 items: Zotero's free-text search does not cover the DOI field, so a
  DOI query answers "not found" for items that are plainly there.
- **Only 20 of the 64 thumbnails are real title pages**; the other 44 are
  designed tiles. Reading abstracts off the images could never have covered
  the list, whatever H23 adds later.
