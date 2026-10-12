---
layout: default
title: Partners
permalink: /partners/
---

<div class="page-head wrap narrow">
  <h1>Partners</h1>
  <p class="lede">The organisations we work with, and work for, across policy,
  industry and research.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap">

<!-- Nothing here is edited by hand. Each partner is a file in _partners/. -->

{% include filter.html target="#partnertable" placeholder="Filter partners by name, city or country…" %}

<p class="muted small tally-key">The <strong>Together</strong> column counts
what each partnership has produced: <span class="k">projects</span> ·
<span class="k">publications</span> · <span class="k">news and events</span>.
A dash means none yet.</p>

<div class="tablewrap">
<table class="listing" id="partnertable">
  <thead><tr>
    <th>Partner</th><th>Type</th><th>Where</th>
    <th class="t-tally" title="Projects · Publications · News">Together</th>
  </tr></thead>
  <tbody>
  {%- assign sorted = site.partners | sort: "name" -%}
  {%- for pa in sorted %}
    <tr>
      <td class="t-partner">
        <a href="{{ pa.url | relative_url }}">
          {%- if pa.logo -%}
          <span class="t-logo"><img src="{{ '/assets/img/partners/' | append: pa.logo | relative_url }}" alt="" loading="lazy"></span>
          {%- endif -%}
          <span class="t-name">{{ pa.name }}</span>
        </a>
      </td>
      <td>{{ pa.type }}</td>
      <td>{{ pa.city }}{% if pa.city and pa.country %}, {% endif %}{{ pa.country }}</td>
      <td class="t-tally">{% include partnerstats.html pa=pa %}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

</div>
</section>
</main>
