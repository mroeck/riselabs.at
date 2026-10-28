---
layout: default
title: Team
permalink: /team/
published: false   # hidden for now - see `team_page` in _config.yml
---

<div class="page-head wrap narrow">
  <h1>Team</h1>
  <p class="lede">RISE is a small research institute in Vienna, working with a
  wider network of partners across policy, industry and research.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow">

<!-- Nothing here is edited by hand. Each person is a file in _people/, and
     the `group` field in that file decides which list they appear in:
     `rise` for the institute, `collaborator` for the people we work with
     closely who are employed elsewhere. A collaborator should also carry an
     `org` line naming where they actually sit. -->

{% include filter.html target="#teamlist" placeholder="Filter the team…" %}

<div id="teamlist">

{%- assign rise = site.people | where: "group", "rise" | sort: "order" -%}
{%- if rise.size > 0 %}
{% include peoplelist.html people=rise %}
{%- endif %}

{%- assign collab = site.people | where: "group", "collaborator" | sort: "order" -%}
{%- if collab.size > 0 %}
<h2>Core collaborators</h2>
<p class="muted">People we work with closely who are employed elsewhere. They
are not part of RISE, and much of what we do would not happen without
them.</p>
{% include peoplelist.html people=collab %}
{%- endif %}

</div>

<p class="more"><a href="{{ '/partners/' | relative_url }}">All partners →</a></p>

</div>
</section>
</main>
