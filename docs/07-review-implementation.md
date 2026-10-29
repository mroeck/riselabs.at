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
   or fonts, no analytics, no hex values inside component rules.
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

## Human input

Items the implementer cannot resolve. Ask, and do not guess.

| ID | Needed from | Question | Blocks |
| --- | --- | --- | --- |
| H0 | Martin (repo and DNS admin) | Fix the custom-domain DNS and certificate in GitHub Pages | P1.0 |
| H1 | Martin | ~~Same document?~~ Answered 29 Oct: yes, list once with the Zenodo DOI. Still open: author name form "Reimer Bjørkskov KB" or "Bjørkskov KBR" | P1.1 |
| H2 | Martin | Source for "up to 150% by 2050 … five billion square metres per year" | P1.5 |
| H3 | Barbara | Employer answered 29 Oct: RISE. Still needed: tagline, bio, portrait, links, approval | P2.1, P1.7 |
| H4 | Nicole | Draft by Martin in progress. Needed: approval of the text, portrait, links; EPFL clearance if required | P2.1 |
| H5 | Zuhaib | Draft by Martin in progress. Needed: approval of the text, portrait, links; EPFL clearance if required | P2.1 |
| H6 | Martin | Date from which Nicole and Zuhaib are RISE employees, if and when that happens | P2.1 label |
| H7 | Martin or Barbara | Run `fetch-abstracts.py --write` and review the diff | P2.6 |
| H8 | Martin | Dates, places and registration links for event posts that lack them, starting with the COP31 session | P3.1 |
| H9 | Martin | Standing text for `/join/`: theses, visiting researchers, fellowships | P1.7, P3.4 |
| H10 | Martin | Consent from Bárbara Rodríguez Droguett to publish her quote | P3.5 |
| H11 | Martin | Own photos with permission to publish | P4.1 |
| H12 | Martin | New slugs for the three projects with truncated names | P4.2 |
| H13 | Martin | German text for `/de/` | P5.2 |
| H14 | Martin | ~~End year and Croatia~~ Answered 29 Oct: ends 2026; Croatia takes part | P1.6 |
| H15 | Martin | The job posts for November 2026: title, text, and the opening fields in P1.7 | P1.7 |
