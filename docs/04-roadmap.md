# Roadmap

Things worth doing to this site that are not done. Kept here so they are not
lost between conversations. Nothing here is urgent.

---

## 1. The collaboration network graph

**The idea.** The partner map shows *where* organisations are. It does not show
*who works with whom*. A network graph would - RISE and GBDI at the centre,
projects and publications as the edges, partner organisations and co-authors as
the nodes. Something closer to the co-authorship maps that plot an institution's
real collaboration structure rather than a list of names.

**What already exists.** More than you would think. The cross-reference model
is already a graph, it is just never drawn as one:

```
PROJECT ──people──▶ PERSON          PUBLICATION ──projects──▶ PROJECT
   │  └─clients────▶ PARTNER             │  └─people────────▶ PERSON
   └─partners──────▶ PARTNER             └─partners────────▶ PARTNER
POST ──projects──▶ PROJECT / ──people──▶ PERSON
```

Every partner has `coords`, so a geographic layout is available today. The
partner "Together" counts are already computed from these edges - that logic is
in `_includes/partnerstats.html` and would become the edge weights.

**What is missing, and this is the real work.** Co-authors. Publications record
`authors` as one string - `"Röck M, Sørensen A, Habert G"` - which is right for
a citation and useless as data. A network needs each author as a node, which
means either:

- *One file per co-author* in `_people/`, which would put dozens of people on
  the team page who are not on the team. Workable only if `group:` gets a third
  value, something like `external`, filtered out of the team list but available
  to the graph. This is the honest route and the slow one.
- *A separate `_data/coauthors.yml`*, mapping name → affiliation → coordinates,
  with publications referencing entries by key. Lighter, no page per person, no
  risk of implying someone is part of RISE. Probably the right first step.
- *Pull from ORCID or OpenAlex.* Both expose co-authorship for a given ORCID,
  which would populate this automatically rather than by hand. A build-time
  script writing `_data/coauthors.yml` would be a day's work and would keep
  itself current. The catch is that it puts a live dependency in the build, so
  it should write a committed file rather than fetch at page load.

**Suggested sequence**, each step useful on its own:

1. Draw the graph with what exists now - projects, partners, posts. No new
   data needed.
2. Add co-authors from a `_data/coauthors.yml` populated by hand for the
   twenty or so most frequent names.
3. Replace that with an ORCID or OpenAlex script once the shape has proved
   itself.

**One caution.** A network diagram flatters. Every node looks like a
partnership whether it was a decade of work or one shared paper, and anyone
depicted can see themselves on it. Edge weights and a legend that says what an
edge means are what keep it honest.

---

## 2. Publication abstracts

All 38 publication pages carry the full citation - title, authors, journal,
year, linked DOI, related projects and RISE authors - and no prose. That is a
complete citation page and most research sites stop there, but the plan is to
paste each paper's **abstract** in and condense it.

The body of a publication file is ordinary Markdown: everything after the
second `---`. Paste the abstract there and it appears under the citation. Doing
them in batches by project is less tedious than working alphabetically.

Not invented in the meantime, deliberately: writing a plausible-sounding
summary of a paper nobody has re-read, on a page that carries a DOI, is where a
confident invention does the most damage.

---

## 3. Smaller things, roughly in order of how much they matter

- ~~**Politecnico di Milano has no logo.**~~ Done, October 2026: the real
  logo replaced the placeholder wordmark.
- **Ten new partners have no logo** - the South African universities, the
  Chinese and Indian organisations added with the 2026 events. The name shows
  on its own, which is tidy but inconsistent.
- **Publication affiliations are unverified.** The `partners:` field on
  publications was seeded from each project's partner list, not from the
  papers' actual author affiliations. The partner "Together" counts lean on it,
  so the publication column is directionally right rather than exact.
- **The GBDI association post** still needs its date and wording confirmed.
- **Three people are held back** with `published: false` - their pages have
  `[ADD]` placeholders. Team page is hidden until the team settles.
- **Photographs were chosen against the dark theme.** Worth ten minutes in
  light mode to see which ones flatten.
- **Three superseded hero images** are still in the repo, unused, kept because
  no other copy exists.
- **Two websites unconfirmed** - China Building Materials Federation and
  Greentech Knowledge Solutions have `website: ""` rather than a guessed URL.

---

## 3a. From the October 2026 review

The work order is `docs/07-review-implementation.md`. Phase P1 is done except
P1.0 (the HTTPS certificate, which needs DNS and repository admin):

- ~~P1.1 duplicate green paper~~ merged into one entry with the Zenodo DOI
- ~~P1.2 "Page in progress" on the homepage~~ removed
- ~~P1.3 past event pinned to the homepage~~ unpinned
- ~~P1.4 no social preview image~~ default card added, `image` alongside `hero`
- ~~P1.5 unsourced floor-area figure~~ sourced to the UNEP/GlobalABC Global
  Status Report 2025-2026
- ~~P1.6 INDICATE LIFE facts disagreed~~ 2024-2026 and five countries everywhere
- ~~P1.7 nothing for the November job posts~~ `/join/`, opening fields, template

Still open and waiting on a person: H0 (the HTTPS certificate) and H15 (the
real job posts). H1, H2 and H9 were answered on 29 October. See the table at
the end of `docs/07`.

---

## 4. Things deliberately not done

Recorded so they are not re-litigated by accident.

- **No analytics.** Adding any would mean a consent banner and a new section in
  `/datenschutz/`. A cookieless, EU-hosted tool would avoid the banner if
  visitor numbers ever become worth having.
- **The theme choice is not remembered.** Storing nothing on the visitor's
  device was a deliberate instruction; the cost is that the theme resets on
  every page. One `localStorage` line plus an inline script in `<head>` would
  change that - the comment in `assets/js/ui.js` marks the spot.
- **The hero stays dark in both themes.** A pale wash over the same
  photographs leaves dark text fighting the imagery.
- **Individual partner pages stay on.** Switching them off was tried and
  reverted - a partner's name would have linked to the organisation's own site
  instead, with `/partners/` as the fallback. If it comes up again: set
  `output: false` on the partners collection and repoint `partners.html`,
  `partnernames.html` and the table in `partners.md`, since `pa.url` goes empty
  when a collection stops producing pages.
