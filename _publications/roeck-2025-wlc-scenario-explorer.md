---
title: "wlc-scenario-explorer: an open source tool for exploring building stock whole life cycle emission scenarios"
kind: data
authors: "Röck M, Lesné B, Eissa S, Alaux N, Ramon D, Passer A, Allacker K"
year: 2025
journal: "Zenodo"
doi: "10.5281/zenodo.13315280"
# The three fields below are the ones `toollist.html` has always read and
# nothing had ever set: they are what the Data & tools cards show. `link`
# points at our own tool page rather than at KU Leuven, because that page
# carries the explanation, the provenance and the citation alongside the
# running app.
state: available
repo: "https://github.com/mroeck/wlc-scenario-explorer"
link: /tools/wlc-scenario-explorer/
summary: "Explore whole life carbon scenarios for the EU building stock to 2050: predefined policy pathways or custom Avoid, Shift and Improve strategies, broken down by country, building type, material and life cycle stage."
people:
  - martin-roeck
partners:
  - ku-leuven
  - tu-graz
projects:
  - analysis-of-life-cycle-greenhouse
thumbnail: /assets/img/pubs/roeck-2025-wlc-scenario-explorer.webp
rise_tier: core
---

<!-- Built out on 11 November 2026, from the tool's own repository: the
     README and paper.md at github.com/mroeck/wlc-scenario-explorer, which
     Martin wrote. Nothing here is inferred from the running app.

     This page is the record. The working tool lives at
     /tools/wlc-scenario-explorer/ (Martin, 11 Nov 2026), which is also
     where wlc-scenario-explorer.com now points. The two link to each
     other; neither repeats the other.

     The DOI is the concept DOI, 10.5281/zenodo.13315280 (Martin,
     11 Nov 2026), replacing the version DOI ...281 this file used to
     carry. Zenodo mints both: the concept DOI always resolves to the
     newest version of the software, the version DOI pins one deposit. For
     a tool that will be released again, the concept DOI is the one to
     publish and to cite, so that a citation does not quietly come to mean
     an old release. Use the version DOI only where a specific release has
     to be identified, such as reproducing a particular result. -->

The **WLC Scenario Explorer** is an open source web tool for exploring whole
life cycle greenhouse gas emission scenarios for buildings across Europe. It
is aimed at policy professionals, industry and researchers who need to see
what a combination of carbon reduction and removal strategies does to a
national or EU building stock, without running the model themselves.

{% include figure.html
   file="/assets/img/tools/wlc-scenario-explorer-app.webp"
   caption="The explorer showing total global warming potential of the EU
            building stock to 2050, split between residential and
            non-residential buildings, under the optimistic current policy
            scenario. The panel on the left selects a predefined scenario or
            builds one from Avoid, Shift and Improve settings."
   source="Screenshot of the running tool, 11 November 2026" %}

<p class="doc-line"><a href="/tools/wlc-scenario-explorer/">Use the explorer
→</a></p>

<h2>What it does</h2>

Users select one of six predefined policy scenarios, or define their own by
setting how far each package of strategies spreads across the Member States.
The strategies are grouped the way the underlying study groups them:
**Avoid** reduces material and energy demand, **Improve** makes conventional
materials and processes better, and **Shift** moves to low-carbon
alternatives. Results can be compared two scenarios at a time, broken down
by country, building type, element, material, stock activity or life cycle
stage, and read as total emissions, per square metre or per head.

<h2>Where the results come from</h2>

The scenario results are not produced by the tool. They come from a
modelling pipeline combining building archetype data from the SLiCE model
with upscaling and scenario analysis from the PULSE model, covering 4096
scenarios across the twenty-seven EU Member States. The software paper is
explicit that the methodology and the results dataset are published
separately, and that publication is
[Context-specific life cycle emissions pathways for EU buildings and
construction](/publications/alaux-2026-context-specific-life/), in *Nature
Communications*, by the same group.

Read together: the Alaux paper is the evidence and the argument, this
software paper is the instrument, and the
[tool page](/tools/wlc-scenario-explorer/) is where the two meet.

<h2>Reuse</h2>

The source is Apache-2.0 licensed at
[github.com/mroeck/wlc-scenario-explorer](https://github.com/mroeck/wlc-scenario-explorer).
The tool reads any scenario results following the SLiCE tabular data format,
and works with incomplete datasets by limiting itself to the attributes the
data actually provides, so it is reusable for analyses other than this one.

The app is hosted on KU Leuven infrastructure. The work links to the EU
study *Analysis of Life-cycle Greenhouse Gas Emissions and Removals of EU
Buildings and Construction* (GROW/2022/OP/0005), contracted by the European
Commission, DG GROW. The authors' opinions do not represent the Commission's
official position.
