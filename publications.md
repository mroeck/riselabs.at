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

{% include filter.html target="#publist" placeholder="Filter by author, title, journal or year…" %}

<div class="entrylist" id="publist">
{% include publist.html pubs=site.publications sections="true" %}
</div>

</div>
</section>
</main>
