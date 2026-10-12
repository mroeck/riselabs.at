---
layout: default
title: Home
permalink: /
---

{% include hero.html %}

<main id="content">

<section class="band">
  <div class="wrap">
    <p class="eyebrow">What we stand for</p>
    <div class="cols pillars">
      <div>
        <h3>System change</h3>
        <p class="muted">Reducing and removing the emissions and resource use
        locked into how we build — and redistributing what the built
        environment takes and gives.</p>
      </div>
      <div>
        <h3>We are nature</h3>
        <p class="muted">Reconnecting with the systems we are part of, rather
        than managing them from outside.</p>
      </div>
      <div>
        <h3>Stronger together</h3>
        <p class="muted">Collective action, solidarity and systems of care —
        because effective climate action is never done alone.</p>
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
    licensing allows. A benchmark nobody can reproduce is an opinion.</p>
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
    {%- assign shown = "epfl,ku-leuven,ramboll,bpie,iiasa,ucl,worldgbc,tu-delft" | split: "," -%}
    {% include partners.html keys=shown %}
    <p class="more"><a href="{{ '/partners/' | relative_url }}">All partners →</a></p>
  </div>
</section>

{% include testimonials.html only="brigitte-jacquemont,xavier-le-den,simone-kongsbak" %}

<section class="band cta-band">
  <div class="wrap narrow">
    <h2>Work with us</h2>
    <p>We collaborate with policy makers, industry and research partners, and
    with networks pioneering what the sector has not normalised yet. If your
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
