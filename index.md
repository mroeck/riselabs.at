---
layout: default
title: Home
permalink: /
wip: true   # shows the "Page in progress" note by the theme toggle
---

{% include hero.html %}

<main id="content">

<section class="band">
  <div class="wrap">
    <p class="eyebrow">What we stand for</p>
    <div class="cols pillars">
      <div>
        <h3>System evolution</h3>
        <p class="muted">Reducing and removing the emissions and resource use
        locked into how we build — and redistributing what the built
        environment takes and gives.</p>
      </div>
      <div>
        <h3>We are nature</h3>
        <p class="muted">Healthy ecosystems are the foundation for sustainable
        development and resilient societies. We help understand where the
        balance is.</p>
      </div>
      <div>
        <h3>Stronger together</h3>
        <p class="muted">Capacity-building, collective action, and solidarity —
        because effective climate action is never done alone. Committed to open science.</p>
      </div>
    </div>
    <p class="more"><a href="{{ '/approach/' | relative_url }}">How we work →</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p class="eyebrow">Latest</p>
    {%- assign featured = site.posts | where: "featured", true -%}
    {%- assign others = site.posts | where_exp: "p", "p.featured != true" -%}
    {%- assign latest = featured | concat: others | slice: 0, 3 -%}
    {% include newslist.html posts=latest %}
    <p class="more"><a href="{{ '/news/' | relative_url }}">All news →</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p class="eyebrow">Recent publications</p>
    <p class="band-note">We publish our methods, data and code openly wherever
    licensing allows. A benchmark nobody can reproduce is just an opinion.</p>
    {%- assign recent = site.publications | sort: "year" | reverse | slice: 0, 4 -%}
    {% include publist.html pubs=recent %}
    <p class="more"><a href="{{ '/publications/' | relative_url }}">All publications →</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p class="eyebrow">Current projects</p>
    <p class="band-note">Research and advisory work for the European
    Commission, national governments, international organisations and
    philanthropic funders.</p>
    {%- assign current = site.projects | where: "status", "current" | sort: "years" | reverse -%}
    {% include projectlist.html projects=current %}
    <p class="more"><a href="{{ '/projects/' | relative_url }}">All projects →</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p class="eyebrow">We work with</p>
    {%- comment -%} hand-picked, in this order; the full list is on /partners/ {%- endcomment -%}
    {%- assign shown = "worldgbc,smith-innovation,bpie,iiasa,ec-dg-grow,unep,laudes,global-industry-hub,epfl,ku-leuven" | split: "," -%}
    {% include partners.html keys=shown %}
    <p class="more"><a href="{{ '/partners/' | relative_url }}">All partners →</a></p>
  </div>
</section>

{% include testimonials.html only="brigitte-jacquemont,xavier-le-den,simone-kongsbak" %}

{%- comment -%}
  Somewhere to go after the quotes. A reader convinced by them should be able
  to reach the argument or the offer without scrolling back to the nav.
{%- endcomment -%}
<section class="band">
  <div class="wrap narrow">
    <div class="onward">
      <a href="{{ '/approach/' | relative_url }}">
        <span class="onward-t">How we work</span>
        <span class="onward-d muted">The three strands, the post-growth
        question, and the methods behind the numbers.</span>
      </a>
      <a href="{{ '/services/' | relative_url }}">
        <span class="onward-t">What we offer</span>
        <span class="onward-d muted">Commissioned research, data
        infrastructure, independent review, strategy and training.</span>
      </a>
    </div>
  </div>
</section>

<section class="band cta-band">
  <div class="wrap narrow">
    <h2>Work with us</h2>
    <p>We collaborate with policy makers, industry and research partners, and
    with networks and players pioneering what the sector has not yet normalized. If your
    work touches any of that, write to us.</p>
    <a class="cta" href="mailto:{{ site.email }}">{{ site.email }}</a>
  </div>
</section>

<section class="band">
  <div class="wrap narrow">
    {% include newsletter.html %}
  </div>
</section>

</main>
