---
layout: default
title: Projects
permalink: /projects/
---

<div class="page-head wrap narrow">
  <h1>Projects</h1>
  <p class="lede">Research and advisory work for the European Commission,
  national governments, international organisations and philanthropic funders.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow">

{% include filter.html target="#projlist" placeholder="Filter projects…" %}

<div id="projlist">

<!-- Nothing on this page is edited by hand.
     Each project is a file in _projects/ — add one there. -->

{%- assign groups = "current,concluded" | split: "," -%}
{%- assign headings = "Current,Concluded" | split: "," -%}

{%- for state in groups -%}
  {%- assign items = site.projects | where: "status", state | sort: "years" | reverse -%}
  {%- if items.size > 0 %}

<h2>{{ headings[forloop.index0] }}</h2>

<ul class="projects">
  {%- for project in items %}
  <li>
    <p class="meta"><span class="date">{{ project.years }}</span>
      {%- if project.funder %}<span class="funder">{{ project.funder }}</span>{% endif -%}
    </p>
    <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
    {%- if project.summary %}<p class="sum">{{ project.summary }}.</p>{% endif -%}
    {%- if project.role %}<p class="role">{{ project.role }}</p>{% endif -%}
  </li>
  {%- endfor %}
</ul>
  {%- endif -%}
{%- endfor %}

</div>

</div>
</section>
</main>
