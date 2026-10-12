---
layout: default
title: News
permalink: /news/
---

<div class="page-head wrap narrow">
  <h1>News</h1>
  <p class="lede">Openings, project updates, publications and events.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow">

{% include filter.html target="#newslist" placeholder="Filter news…" %}

<div id="newslist">
{% if site.posts.size > 0 %}
  {% include newslist.html posts=site.posts years="true" %}
{% else %}
  <p class="muted">Nothing here yet.</p>
{% endif %}
</div>

</div>
</section>
</main>
