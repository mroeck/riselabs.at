---
layout: default
title: News and events
permalink: /news/
---

{%- comment -%}
  One page for news and events (Phase N, 2 Nov 2026). /news/ and /events/
  showed almost the same list, so they are one page with tabs by type of
  post; /events/ is now a redirect to /news/#events.

  Order: page head, "Coming up", the tab row with the filter beside it, then
  the card grid. The tabs and their counts are built here, at build time,
  from the posts that exist; the script only switches between them.
{%- endcomment -%}

<div class="page-head wrap narrow">
  <h1>News and events</h1>
  <p class="lede">What we published, where we spoke, and what changed in our
  projects.</p>
</div>

<main id="content">

{% include comingup.html %}

<section class="band">
<div class="wrap">

{%- comment -%}
  Featured first, then everything else by date. The featured card is full
  width, so it has to lead: left in date order it sits in the middle of the
  grid and tears a hole in the row it is in. The script moves it back to an
  ordinary card inside a tab or under a filter, where a wider card would
  mean nothing.
{%- endcomment -%}
{%- assign pinned = site.posts | where: "featured", true -%}
{%- assign rest = site.posts | where_exp: "p", "p.featured != true" -%}
{%- assign ordered = pinned | concat: rest -%}

{%- comment -%}
  A tab per type that has at least one published post, in the order of
  _data/post_types.yml, each with its count. A type with nothing behind it
  gets no tab rather than an empty one.

  Hidden until the script runs: without JavaScript every post shows in one
  grid, newest first, which is the whole page and a complete one.
{%- endcomment -%}
{%- assign types = site.data.post_types -%}
<div class="newsbar" data-newsbar hidden>
  <div class="themebar kindbar" role="tablist" aria-label="Show">
    <button type="button" class="on" role="tab" aria-selected="true" data-news-filter="">All<small>{{ site.posts.size }}</small></button>
    {%- for t in types -%}
    {%- assign of_type = site.posts | where: "type", t.slug -%}
    {%- if of_type.size > 0 -%}
    <button type="button" role="tab" aria-selected="false" data-news-filter="{{ t.slug }}" data-hash="{{ t.hash }}">{{ t.plural }}<small>{{ of_type.size }}</small></button>
    {%- endif -%}
    {%- endfor -%}
  </div>
  {% include filter.html target="#newslist" placeholder="Filter by title or topic…" %}
</div>

<div id="newslist">
{% if site.posts.size > 0 %}
  {% include postcards.html posts=ordered featured="true" %}
{% else %}
  <p class="muted">Nothing here yet.</p>
{% endif %}
</div>
<p class="muted" data-news-empty hidden>Nothing matches. Try another tab or
clear the filter.</p>

</div>
</section>
</main>
