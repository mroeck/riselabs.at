---
layout: default
title: Data & tools
permalink: /tools/
---

<div class="page-head wrap narrow">
  <h1>Data &amp; tools</h1>
  <p class="lede">The datasets, models and software behind the studies -
  published so the results can be reproduced, not just read.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow">

<p class="band-note">A benchmark nobody can reproduce is an opinion. Where
licensing allows, the data and the code are released with the study rather
than on request. Each one below has its own DOI and is citable in its own
right.</p>

{%- comment -%}
  These are the publications with `kind: data`. They are not duplicated here
  - this page is a different way into the same files, because a dataset
  listed fourth on a publications page is effectively buried.
{%- endcomment -%}
{%- assign datasets = site.publications | where: "kind", "data" -%}

{% include filter.html target="#toollist" placeholder="Filter data &amp; tools…" %}

<div id="toollist">
{% if datasets.size > 0 %}
  {% include toollist.html pubs=datasets %}
{% else %}
  <p class="muted">Nothing here yet.</p>
{% endif %}
</div>

<p class="more"><a href="{{ '/publications/' | relative_url }}">All publications →</a></p>

</div>
</section>
</main>
