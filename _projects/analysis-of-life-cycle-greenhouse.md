---
title: "Analysis of Life Cycle Greenhouse Gas Emissions and Removals of EU Buildings and Construction"
short_title: "EU buildings emissions analysis"
status: "concluded"
years: "2022–2025"
funder: "European Commission DG GROW"
role: "Team lead and task lead, baseline analysis and scenario modelling"
summary: "Quantified the baseline and the plausible futures for emissions and removals across the EU building stock to 2050"
hero: "/assets/img/projects/eu-stock-by-country.png"
image: "/assets/img/projects/eu-stock-by-country.png"   # the social preview; see docs/03
hero_caption: "Building stock composition by country across the EU."
themes:
  - building-stock
  - whole-life-carbon
  - policy-regulation
link: "https://c.ramboll.com/life-cycle-emissions-of-eu-building-and-construction"
project_title: "Analysis of life-cycle greenhouse gas emissions and removals of EU buildings and construction"
# Only outputs Martin co-authored (Martin, 16 Nov 2026). The study produced
# more than this - the full set is on the project's own page, which `link`
# above already points to - but this page speaks for RISE, and listing a
# consortium partner's deliverable here would imply a hand in writing it.
#
# Three qualify, each checked against the document's own title page rather
# than against the project page's description of it:
#
#   D4.1          Röck first author
#   the explorer  Röck first author of the software paper
#   final report  Röck in the author list, last of nine
#
# Deliberately not here, and why, so nobody adds them back by mistake:
#
#   D5.2, future availability and generation of data - written by Xerome
#     Fernández Álvarez and Judit Kockat of BPIE. Not his.
#   The four 2023-2024 EC deliverables (docsroom 58194, 58195, 58196,
#     58197) - authorship unestablished. Those links now forward to
#     CIRCABC, unreachable from here by shell, fetch or browser, and the EC
#     document page names the author only as GROW.H.1, the Commission unit.
#     He led the analytical work, so he may well be on them, but "may well
#     be" is not a byline. They go in once the PDFs or the author lists
#     arrive.
outputs:
- title: "Quantitative figures for future scenarios"
  note: "Deliverable D4.1 · European Commission, 2025"
  url: "https://c.ramboll.com/hubfs/RMC/Content/D4-1_Future-Scenarios.pdf"
- title: "WLC Scenario Explorer"
  note: "The open tool built from this study's stock model"
  url: /tools/wlc-scenario-explorer/
- title: "Analysis of results and implications"
  note: "Final report · European Commission, 2025"
  url: "https://data.europa.eu/doi/10.2873/2247112"
  # thumb: /assets/img/outputs/dg-grow-report.jpg
# Add further published deliverables as blocks above: title, optional note,
# and a url. Only outputs anyone may read, and that Martin co-authored,
# belong here.
figures:
- file: /assets/img/projects/wlc-scenario-explorer.png
  number: Figure 1
  caption: The WLC Scenario Explorer, the open tool built from this
    study's stock model.
clients:
  - ec-dg-grow
people:
  - martin-roeck
partners:
  - rise
  - ku-leuven
  - tu-graz
  - ramboll
  - bpie
  - iiasa
  - aau-build
  - polimi
# Related projects, by slug. The link is written on both sides for
# readability, but the layout also resolves it in reverse, so naming a
# project on one side alone is enough to make it appear on both.
related:
  - collaborative-carbon
  - global-status-report-for-buildings
  - global-whole-life-carbon-tracker
  - reliving-scaling-renovation
  - supporting-the-development-of-a
---

<!-- Concluded project, so the text runs Context then Insights, with a third
     section for where the results actually landed.

     ON THE DELIVERABLES, 16 Nov 2026. Martin first asked for every document
     the project's own page links, then narrowed it the same day: only
     outputs he co-authored. One test now decides both `outputs` above and
     whether a deliverable gets a publication record, which is why the lists
     match. What that test produced:

     - D4.1, quantitative figures for future scenarios. Title page read
       directly: Martin is first author, with Ramon, Pristerà and Allacker
       (KU Leuven), Alaux and Steinberger-Maierhofer (TU Graz), Mastrucci
       and Zhong (IIASA). Recorded at
       _publications/roeck-2025-future-scenarios-quantitative.md
     - D5.2, future availability and generation of data. Title page read
       directly: authored by Xerome Fernández Álvarez and Judit Kockat of
       BPIE, reviewed by Ramboll and BPIE. Not his, so it appears nowhere on
       this page.
     - The four 2023-2024 deliverables on ec.europa.eu. Authorship could not
       be established: the links now forward to CIRCABC, which this
       environment cannot reach by any route, and the EC document page gives
       the author only as GROW.H.1, the Commission unit. He led the
       analytical work, so he may well be on them, but that is an inference
       and not a byline. Send the four PDFs, or confirm the author lists,
       and they go into `outputs` and get records in the same change.

     Anyone wanting the study's full output set has `link` in the front
     matter, which goes to the project's own page where all of it is
     published. This page lists what RISE had a hand in writing.

     Eight further publications already carry `projects:
     analysis-of-life-cycle-greenhouse` and appear on this page
     automatically, so the journal papers are not repeated in `outputs`. -->


<h2>Context</h2>

Buildings and construction account for roughly 40% of greenhouse gas emissions
in the EU, but until recently there was no agreed quantification of how those
emissions are distributed across the life cycle of the stock, nor of how
different policy choices would change them by 2050. Without that, the revision
of the Energy Performance of Buildings Directive would have been argued on
assertion rather than evidence.

DG GROW commissioned the analysis to close that gap. We led the analytical
work: a bottom-up model of the EU27 building stock, built from archetype
buildings and harmonised material and energy flow data, run forward to 2050
under a set of policy scenarios, and assembled from open archetypes so that
national teams could repeat it rather than start over.

<h2>Insights</h2>

<div class="findings" markdown="1">

- **Embodied emissions are already about half the problem, and rising as a
  share.** As operational performance improves under existing directives, the
  emissions locked into materials and construction become the dominant term.
  Any policy that targets only operational energy is aiming at a shrinking
  fraction.
- **No single lever is sufficient.** Reaching a trajectory consistent with EU
  climate targets requires radical reduction of operational emissions, a
  three- to fourfold increase in renovation rates, and material efficiency and
  decarbonisation of materials, together. Scenarios that pull only one of
  these levers fall well short.
- **Removals are real but modest, and contested.** Biogenic carbon storage in
  timber and mineral carbonation can contribute, but the magnitude depends
  heavily on accounting choices and on assumptions about forest carbon
  opportunity costs.

</div>

<h2>Impact</h2>

The results informed the evidence base for the revised Energy Performance of
Buildings Directive, which now requires whole life carbon disclosure for all
new buildings by 2030, and fed into the Commission's wider work on the EU
Taxonomy and construction products.
