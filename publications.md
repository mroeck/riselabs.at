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
  Two control rows. Both are added by the script, so without JavaScript the
  page is the full list in its built order, which is a complete page.

  FILTER. About half this list is work the team did before joining RISE or
  GBDI - Galway, BPIE, Politecnico di Milano - which belongs here because it
  is theirs, but a visitor asking what RISE has published should be able to
  ask that. The row renders only when at least one person has a `rise_since`
  year, so it can never quietly mislabel anyone's earlier work.

  SORT. Newest first is how the page is built, so that button starts on.
  "Most cited" appears only once counts exist in the files: run
  `python3 fetch-citations.py --write` somewhere with a connection. Until
  then the button is absent rather than present and useless. Counts come from
  OpenAlex, not Google Scholar, which has no API and does not permit
  scraping; OpenAlex's number is lower, and each entry says where it came
  from and when.
{%- endcomment -%}
{%- assign dated = site.people | where_exp: "x", "x.rise_since" -%}
{%- if dated.size > 0 %}
<div class="themebar" data-pubfilter role="group" aria-labelledby="pubfilter-label" hidden>
  <span class="themebar-label" id="pubfilter-label">Show</span>
  <button type="button" data-pub-filter="" class="on" aria-pressed="true">All</button>
  <button type="button" data-pub-filter="rise" aria-pressed="false">With RISE or GBDI</button>
</div>
{%- endif %}

{%- assign cited = site.publications | where_exp: "x", "x.citations" -%}
<div class="themebar" data-pubsort role="group" aria-labelledby="pubsort-label" hidden>
  <span class="themebar-label" id="pubsort-label">Sort</span>
  <button type="button" data-pub-sort="newest" class="on" aria-pressed="true">Newest first</button>
  <button type="button" data-pub-sort="oldest" aria-pressed="false">Oldest first</button>
  {%- if cited.size > 0 %}
  <button type="button" data-pub-sort="cited" aria-pressed="false">Most cited</button>
  {%- endif %}
</div>

{% include filter.html target="#publist" placeholder="Filter by author, title, journal or year…" %}

<div class="entrylist" id="publist">
{% include publist.html pubs=site.publications sections="true" %}
</div>

</div>
</section>
</main>
