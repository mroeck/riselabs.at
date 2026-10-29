---
title: "Chile: whole life carbon tool and data harmonisation with OpenBDF"
short_title: "Chile data harmonisation"
status: "current"
years: "2025–2026"
funder: "CORFO Chile Public Goods Call"
role: "International technical partner - data architecture and OpenBDF alignment"
summary: "Aligns Chile's national whole life carbon tool and building database with the open global data format from the start, so the data stays comparable"
hero: "/assets/img/projects/santiago.jpg"
image: "/assets/img/projects/santiago.jpg"   # the social preview; see docs/03
hero_caption: "Santiago de Chile."
link: "https://www.gbdi.io"
partners:
  - ebp-chile
  - universidad-de-chile
  - epfl
people:
  - martin-roeck
  - nicole-di-santo
  - barbara-droste-luckmann
# Nicole Di Santo is Technical Lead on this. Add `- nicole-di-santo` above once
# her person page is finished and `published: false` is removed from it.
themes:
  - data-benchmarks
  - global-south
  - whole-life-carbon
# Related projects, by slug. The link is written on both sides for
# readability, but the layout also resolves it in reverse, so naming a
# project on one side alone is enough to make it appear on both.
related:
  - gbdi-china-and-india-cooperation
  - global-building-data-initiative
---

<!-- DRAFT - written from the project information sheet supplied in October
     2026. The framing and the facts come from that document; check the dates
     and the description of the partners' roles before relying on it. -->

<h2>Context</h2>

Chile's construction sector is expanding, and the country has set ambitious
decarbonisation goals. What was missing was the machinery in between: a
standardised method and an open tool for measuring emissions across the whole
life cycle, and credible benchmarks to measure against. The project was
launched under the CORFO Chile Public Goods Call to build exactly that.

<h2>Objectives</h2>

- **Align the data architecture from day one.** The Chilean tool is built on
  the Open Building Data Format, so its data is structured the way the global
  database expects rather than translated afterwards.
- **Harmonise the classifications.** Building element classes, material classes
  and quantity take-offs, mapped between Chilean practice and the international
  schema.
- **Open up public procurement data.** Quantity take-offs from Mercado Público,
  Chile's public procurement system, extended into a non-residential building
  database.

<h2>Why the sequencing matters</h2>

Most national datasets are built first and harmonised later, which is how data
silos form: by the time anyone tries to compare two countries, the differences
are baked into the structure and the work has to be redone. Adopting the shared
framework at the proposal stage avoids that, and means Chilean buildings can be
compared with buildings anywhere else without a translation layer.

<h2>What it should produce</h2>

- An output data file aligned with OpenBDF, so Chilean building cases import
  directly into the global platform
- A database mapping real carbon values in Chile
- A framework underpinning the national whole life carbon tool

The harder parts are known: there is no standardised material classification
at the local level, and extracting quantity take-offs from public project data
is still largely manual.

<h2>Where it sits</h2>

Part of the [Global Building Data
Initiative](/projects/global-building-data-initiative/), with partners at EBP
Chile and the Facultad de Arquitectura y Urbanismo of the Universidad de Chile.
