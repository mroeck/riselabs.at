---
layout: default
title: Events
permalink: /events/
---

<div class="page-head wrap narrow">
  <h1>Events</h1>
  <p class="lede">Talks, panels, workshops and seminars — where the work gets
  argued about in public.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow">

{%- comment -%}
  Everything here comes from _posts. A post appears on this page when its
  front matter says `type: event`; it also stays in the full News list, which
  is the one place everything appears together.
{%- endcomment -%}
{%- assign events = site.posts | where: "type", "event" -%}

{% include filter.html target="#eventlist" placeholder="Filter events…" %}

<div id="eventlist">
{% if events.size > 0 %}
  {% include newslist.html posts=events years="true" %}
{% else %}
  <p class="muted">Nothing here yet.</p>
{% endif %}
</div>

<p class="more"><a href="{{ '/news/' | relative_url }}">All news →</a></p>

</div>
</section>
</main>
