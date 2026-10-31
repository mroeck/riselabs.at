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


<div class="entrylist" id="publist">
{% include publist.html pubs=site.publications sections="true" %}
</div>

</div>
</section>
</main>
