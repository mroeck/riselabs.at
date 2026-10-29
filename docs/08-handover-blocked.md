# Handover: what is blocked, and on what

Written 29 October 2026, at the end of the session that implemented phases P1
and the unblocked half of L. Attach this file, `07-review-implementation.md`
and `03-editing-the-site.md` to a new session and it should be able to start
without rediscovering any of the below.

The next pieces of work are **engagement (P3.3) and the team (P2.1 to P2.4)**.
Those are covered in detail in section 4.

---

## 1. Where the site stands

`main` is at the merge of pull request #14. `python3 docs-check.py` reports
**no problems found**, and that is the bar before every commit.

Merged this week, in order: #7 project image attribution, #8 the kramdown and
cache bugs, #9 the project page restructure, #10 stock imagery, #11 the footer
links, #12 phase P1, #13 L1, #14 the unblocked phase L items.

What that leaves live: project pages in their new order with the image behind
the title; `/join/` with the opening fields and the "Other ways in" section;
the social preview card; stock imagery on `/expertise/`; Martin's shortened
profile with collapsed related lists; the three-column footer.

**Phase P1 is complete except P1.0.** Phase L is complete except the items in
section 3. Phases P2, P3, P4 and P5 are untouched.

---

## 2. The environment, and what it cannot do

This cost real time to discover. It will cost it again if the next session has
to find out the same way.

- **Jekyll cannot be run here.** RubyGems is blocked, so there is no way to
  build the site or to run kramdown. Everything is verified by reading the
  templates, balancing Liquid blocks, parsing the YAML, running
  `docs-check.py`, and rendering hand-built markup against the real
  `assets/css/style.css` in headless Chromium. **The first real build is
  always on merge.** Say so in the pull request rather than implying the build
  was checked.
- **The shell reaches GitHub and the package registries, nothing else.** Not
  the live site, not Zenodo, not UNEP, not `mroeck.github.io`, not the Pages
  build artifact (it is on Azure blob storage).
- **`WebFetch` reaches most public sites but not all.** `agora-industrie.de`
  and `zenodo.org` were both refused. When a source cannot be reached, say so
  and leave the fact unverified rather than inventing a citation.
- **Claude in Chrome works** and is the only way to see the live site. It
  reaches `riselabs.at` over **http**, not https, until P1.0 is fixed. Zenodo
  is blocked there too.
- Looking at the live site caught two things a static mock could not: a
  publication really is linked to the Agora project, and the Agora client and
  collaborator tiles duplicate. **Check the live site before claiming a
  section is empty.**

---

## 3. Blocked work, grouped by what unblocks it

### Waiting on Martin, repository and DNS admin

| | |
| --- | --- |
| **H0 / P1.0** | The HTTPS certificate. `https://riselabs.at` shows a certificate error; the site's own canonical and `og:url` point at https, so every shared link and every search result leads to the warning. The steps are in `07` § P1.0. **This is the most urgent open item**: job posts go out in the first week of November and applicants will follow shared links. Record the date in `docs/01` when it is done. |

### Waiting on photographs

| | |
| --- | --- |
| **H16 / L3** | The portrait shoot. Black and white was decided on 29 Oct; the rule is to apply `filter: grayscale(1)` in CSS behind one switch, never to convert the files. Square 1:1, at least 800 × 800. **L3 blocks L2**, so the homepage rework waits on this unless it ships with initials tiles. A group photo for the team page header is optional. |
| **H11 / P4.1, L10** | Own photographs with permission to publish, to replace the stock imagery on `/expertise/` and the two GBDI card images that are website screenshots. |

### Waiting on people

| | |
| --- | --- |
| **H3 / Barbara** | Employer confirmed as RISE on 29 Oct. Still needed: tagline, bio, portrait, links, and her approval of the exact text. |
| **H4 / Nicole, H5 / Zuhaib** | Drafts being prepared by Martin. Needed: each person's approval, portrait, links, and EPFL clearance if required. Both stay `published: false` until then. |
| **H6** | The date from which Nicole and Zuhaib become RISE employees, if that happens. Until then they stay `group: collaborator`; do not relabel them. |
| **H10** | Consent from Bárbara Rodríguez Droguett to publish her quote. Her `short` is already in `_data/testimonials.yml` and must not be rendered until consent exists. |

`docs/06-core-collaborators.md` is the contract for all of this. **No person
page or portrait is published until that person has approved the exact text.**

### Waiting on content from Martin

| | |
| --- | --- |
| **H15** | The real job posts: title, text, and the opening fields. A draft was sent as a Word file on 29 Oct. The template is `_posts/2026-10-05-example-open-position.md`, `published: false`, and `docs-check.py` refuses to publish it while `pay_min` is the placeholder. |
| **H7** | Run `python3 fetch-abstracts.py --write` on a machine with network access and review the diff. Abstracts must not be written or condensed by a model; `docs/04` § 2 says why. |
| **H8** | Dates, places and registration links for event posts that lack them, starting with the COP31 session. |
| **H12** | New slugs for the three projects with truncated names. |
| **H13** | German text for `/de/`, if P5.2 is wanted. |

### Blocked only by other work, not by a person

| Item | Needs |
| --- | --- |
| **L2** homepage order | P3.3 engagement modes, and L3 for the team band |
| **L5** two-column inner pages | P2.4 contact row, P2.5 thumbnails and buttons |
| **L7** partner logo strip | the homepage bands from L2 |
| **L8** hero | P3.1 events for the "Coming up" panel, P3.3 for the button target |
| **L13** post images | P3.1 event fields |
| **P2.7, P2.8** homepage | P2.5 |
| **P3.2** "Coming up" | P3.1 |

**L15**, the approach diagram, is unblocked and was left out of #14 only to
keep that pull request reviewable. It is the easiest remaining win.

---

## 4. The engagement and team work, in order

This is the thread to pull next. Nothing here needs a photograph except the
last step.

1. **P3.3 engagement.** Move the four ways of working out of `expertise.html`
   into a new `_data/engagement.yml`, **unchanged in wording**, and render
   both `/expertise/` and the homepage from it. Each homepage card ends in a
   `mailto:` with a prefilled subject. This is self-contained and unblocks L2
   and L8.
2. **P2.1 team page.** `team_page: true`, remove `published: false` from
   `team.md`, `Team` back as the first nav item under About, one grid headed
   "Team" ordered `rise` then `collaborator`. Every card shows the employer.
   Martin appears immediately; the others appear as H3 to H5 are answered.
   Update `docs/06` to match.
3. **P2.2 cards and profiles.** New `tagline` and `works_on` fields.
   `works_on` is a closed vocabulary from `_data/themes.yml` and the checker
   must reject an unknown slug, exactly as the `related` rule does.
4. **P2.4 contact on every project.** Optional `contact:` field, falling back
   to the first person in `people:` with an email. The checker must reject a
   slug that does not exist.
5. **P2.3 and L3 homepage team band**, once portraits exist.

Steps 1 to 4 can all be done now. Only step 5 waits on H16.

---

## 5. Conventions that must hold

From `docs/03`, `docs/05`, `docs/06` and `07` § 0, plus what this session
learned by getting it wrong:

- **Invent nothing that carries a name, a number, a date or a DOI.** Leave the
  field empty, keep `published: false`, and add the item to the human-input
  table in `07`.
- **Colours only through semantic tokens.** No hex inside a component rule. No
  third-party scripts or fonts, no analytics.
- **No em-dashes anywhere.** Four unpublished person drafts still contain
  them: `barbara-droste-luckmann`, `nicole-di-santo`, `zuhaib-batra`,
  `example-colleague`. They were left alone because Martin is drafting those
  files; clean them when he is done.
- **`markdown="1"` must start at column 0.** An indented one is not parsed by
  kramdown and its tags leak onto the page as text. That was the `/expertise/`
  bug. `docs-check.py` now fails on it. A page that is pure layout belongs in
  `.html`, where Liquid still runs and kramdown cannot touch it.
- **Progressive enhancement is not optional here.** The opening deadlines, the
  collapsed lists and the tabs all render completely without JavaScript, and
  no control that needs a script is present in the markup. Keep that.
- **Extend `docs-check.py` whenever a task adds a field**, and prove the new
  rule fires by breaking something on purpose before committing.
- **One branch and pull request per phase**, titled `Review P<n>: <topic>`,
  and **always branch off current `main`**. Stacked pull requests only
  auto-retarget when the base branch is deleted; that cost a cleanup once
  already.
- Do not push without clearance. Martin reviews and merges on the GitHub web
  app, not in a terminal.

---

## 6. Housekeeping

Eleven merged branches are still on the remote and can be deleted from the
repository's Branches page: `develop`, `posts-china-india`,
`project-reliving`, `fix-project-images`, `fix-expertise-markup-and-grid`,
`project-page-restructure`, `stock-imagery`, `footer-social-links`,
`review-p1-fixes`, `review-l1-page-head`, `review-l-unblocked`.

Two things noticed on the live site and not yet fixed, neither of which has a
task in `07`:

- **Agora Industrie is listed as both client and collaborator** in
  `_projects/agora-leitmaerkte-embodied-carbon.md`, so it appears twice in the
  facts box and as two tiles. Probably wants to be client only. Confirmed on
  the live page.
- **The GWLCT hero is 547 × 365**, which is soft at full width. A larger
  original would help.

`docs/04-roadmap.md` § 3 still lists the ten missing partner logos, the
unverified publication affiliations, the light-mode check of photographs and
two unconfirmed partner websites.
