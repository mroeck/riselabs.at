---
layout: default
title: Publications
permalink: /publications/
---

<div class="page-head wrap narrow">
  <h1>Publications</h1>
  <p class="lede">Peer-reviewed research, reports and open datasets from the
  RISE team and our collaborations.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow">

<!-- Nothing here is edited by hand. Each publication is a file in
     _publications/ and gets its own page. -->

<p class="muted">Full lists via
<a href="{{ site.scholar }}">Google Scholar</a> and
<a href="https://orcid.org/0000-0003-2940-1230">ORCID</a>.
Open access or available on request.</p>

{%- comment -%}
  The "With RISE or GBDI" chips. About half of this list is work the team did
  before joining - Galway, BPIE, Politecnico di Milano - which belongs here,
  because it is theirs, but a visitor asking what RISE has published should be
  able to say so.

  The bar renders only when at least one person has a `rise_since` year, so
  until those years exist the page is exactly as it was rather than offering a
  filter that would quietly mislabel people's work. The script shows the bar;
  without JavaScript the full list stands, which is the honest default.
{%- endcomment -%}
{%- assign dated = site.people | where_exp: "x", "x.rise_since" -%}
{%- if dated.size > 0 %}
<div class="themebar" data-pubfilter hidden>
  <button type="button" data-pub-filter="" class="on">All</button>
  <button type="button" data-pub-filter="rise">With RISE or GBDI</button>
</div>
{%- endif %}

{% include filter.html target="#publist" placeholder="Filter by author, title, journal or year…" %}

<div class="entrylist" id="publist">
{% include publist.html pubs=site.publications sections="true" %}
</div>

</div>
</section>
</main>
