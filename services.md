---
layout: default
title: Services
permalink: /services/
description: >-
  Commissioned research, data infrastructure, independent review, strategy,
  training and research partnerships on the decarbonisation of the built
  environment.
---

<div class="page-head wrap narrow">
  <h1>Services</h1>
  <p class="lede">We help governments, public authorities, international
  organisations, cities and industry turn climate targets into evidence,
  methods and measurable strategies for the built environment.</p>
</div>

<main id="content">

<section class="band">
<div class="wrap narrow">

<p>Commissioned work is how a good deal of our research gets funded, and it is
also how the research reaches the places where decisions are made. The
<a href="{{ '/approach/' | relative_url }}">three strands of our approach</a> —
changing the rules, reaching greater numbers, working with pioneers — are not a
separate activity from the work clients pay for. They are the same work,
described from the other side.</p>

<p>What that means in practice: we take on assignments where the answer is
allowed to be inconvenient. We publish our methods. And we say no to work where
the conclusion is specified in advance.</p>

</div>
</section>

{%- for s in site.data.services %}
<section class="band service">
<div class="wrap">

  <div class="svc-grid">
    <div class="svc-main">
      {%- if s.strand and s.strand != "" -%}
      {%- case s.strand -%}
        {%- when "up" -%}{% assign strand_label = "Scaling up — changing the rules" %}
        {%- when "wide" -%}{% assign strand_label = "Scaling wide — reaching greater numbers" %}
        {%- when "deep" -%}{% assign strand_label = "Scaling deep — working with pioneers" %}
        {%- else -%}{% assign strand_label = nil %}
      {%- endcase -%}
      {%- if strand_label %}
      <p class="eyebrow"><a href="{{ '/approach/' | relative_url }}">{{ strand_label }}</a></p>
      {%- endif -%}
      {%- endif %}

      <h2>{{ s.title }}</h2>
      <p class="svc-lede">{{ s.lede }}</p>

      {%- if s.includes %}
      <ul class="svc-list">
        {%- for item in s.includes %}
        <li>{{ item }}</li>
        {%- endfor %}
      </ul>
      {%- endif %}

      {%- if s.note and s.note != "" %}
      <p class="muted small svc-note">{{ s.note }}</p>
      {%- endif %}
    </div>

    <aside class="svc-side">
      {%- if s.example and s.example != "" -%}
      {%- assign ex = site.projects | where: "slug", s.example | first -%}
      {%- if ex %}
      <p class="svc-label">For example</p>
      <p class="svc-example"><a href="{{ ex.url | relative_url }}">{{ ex.title }}</a></p>
      {%- if ex.summary and ex.summary != "" %}
      <p class="muted small">{{ ex.summary }}</p>
      {%- endif %}
      {%- endif -%}
      {%- endif %}

      {%- if s.audience and s.audience != "" %}
      <p class="svc-label">Typically for</p>
      <p class="muted small">{{ s.audience }}</p>
      {%- endif %}
    </aside>
  </div>

</div>
</section>
{%- endfor %}

{% include testimonials.html heading="What people say" %}

<section class="band">
<div class="wrap narrow">

<h2>How an engagement starts</h2>

<p>A first conversation, usually half an hour, about what decision the work has
to support and by when. If we are the right people for it, you get a short
proposal: scope, method, what we will and will not be able to conclude,
timeline and fee. If we are not, we will say so and point you to someone better
placed.</p>

<p>We are a small team and deliberately so, which means we are selective and we
plan some months ahead. For work tied to a procurement deadline or a
legislative timetable, earlier is better.</p>

</div>
</section>

<section class="band cta-band">
<div class="wrap narrow">
  <h2>Enquiries</h2>
  <p>Tell us what you are deciding and what evidence is missing. That is
  usually enough to work out whether we can help.</p>
  <a class="cta" href="mailto:{{ site.email }}">{{ site.email }}</a>
</div>
</section>

</main>
