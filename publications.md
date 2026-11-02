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

{%- comment -%}
  The wide wrap since 1 Nov 2026. This band was `narrow` when the entries
  were rows of text and a reading measure was the right constraint. They are
  cards now, and three of them across 40rem is 182px each, which is narrower
  than the same card on a phone.
{%- endcomment -%}
<main id="content">
<section class="band">
<div class="wrap">

<!-- Nothing here is edited by hand. Each publication is a file in
     _publications/ and gets its own page. -->

<p class="muted">Full lists via
<a href="{{ site.scholar }}">Google Scholar</a> and
<a href="https://orcid.org/0000-0003-2940-1230">ORCID</a>.
Open access or available on request.</p>

{%- comment -%}
  M1: one control row. The filter box takes the width that is left and the
  sort select sits beside it; under about 30rem they wrap onto two lines.

  The "With RISE or GBDI" chips are gone (Martin, 31 Oct). About half this
  list is work the team did before joining, and the filter was the wrong way
  to say so: it made a visitor do the sorting. The list still puts RISE and
  GBDI work first inside each year, which says the same thing without asking
  anything of the reader.

  Both controls are added by the script, so without JavaScript the page is
  the full list in its built order, which is a complete page.

  "Most cited" only appears once counts exist in the files. They come from
  OpenAlex, not Google Scholar, which has no API and does not permit
  scraping; each entry records where its number came from and when.
{%- endcomment -%}
{%- assign cited = site.publications | where_exp: "x", "x.citations" -%}
<div class="pubcontrols" data-pubcontrols hidden>
  {% include filter.html target="#publist" placeholder="Filter by author, title, journal or year…" %}
  <p class="sortwrap">
    <label for="pub-sort">Sort</label>
    <select id="pub-sort" data-pub-sort>
      <option value="newest">Newest first</option>
      <option value="oldest">Oldest first</option>
      {%- if cited.size > 0 %}
      <option value="cited">Most cited</option>
      {%- endif %}
    </select>
  </p>
</div>


{%- comment -%}
  The kind tabs (Martin, 1 Nov 2026). One button per section, built from the
  same list publist.html uses, so a kind with nothing in it never gets a tab
  and a new kind gets one without anyone editing this page.

  Hidden until the script runs, like the theme bar on /projects/: a filter
  that cannot filter should not be on the page, and without JavaScript every
  section is shown, which is the whole list and a complete page.

  These hide whole sections rather than individual entries, because the
  sections are the kinds. The filter box and the sort control below act on
  the entries inside whatever is shown, so the three compose: filter by
  author within reports, sorted by citations.
{%- endcomment -%}
{%- assign kinds = "article,conference,report,book,data" | split: "," -%}
{%- assign names = "Journal articles,Conference papers,Reports,Books and chapters,Data and tools" | split: "," -%}
<div class="themebar kindbar" data-kindbar hidden>
  <button type="button" class="on" data-kind-filter="">All</button>
  {%- for k in kinds -%}
  {%- assign group = site.publications | where: "kind", k -%}
  {%- if group.size > 0 -%}
  <button type="button" data-kind-filter="{{ k }}">{{ names[forloop.index0] }}</button>
  {%- endif -%}
  {%- endfor -%}
</div>

<div class="entrylist" id="publist">
{% include publist.html pubs=site.publications sections="true" %}
</div>

</div>
</section>
</main>
