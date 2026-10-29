---
layout: default
title: Team
permalink: /team/
---

<div class="page-head wrap narrow">
  <h1>Team</h1>
  <p class="lede">RISE is a small research institute in Vienna, working with a
  wider network of partners across policy, industry and research.</p>
</div>

<main id="content">
<section class="band">
<!-- The full band width, not `narrow`. `narrow` is the reading measure, which
     is right for the lede above and wrong for a grid of cards: at 40rem the
     cards are too tight for a job title to fit beside a portrait. -->
<div class="wrap">

<!-- Nothing here is edited by hand. Each person is a file in _people/.

     One grid, not two. The `group` field still decides the order - `rise`
     first, then `collaborator`, each by `order` - but everyone appears in the
     same list, and every card carries its employer line instead. Separating
     the two into different sections made the collaborators read as a lesser
     tier; the employer line keeps the distinction honest without implying a
     hierarchy. See docs/06.

     A person with `published: false` does not appear at all. Do not remove
     that line until the person has approved the exact text. -->

{% include filter.html target="#teamlist" placeholder="Filter the team…" %}

<div id="teamlist">

{%- assign rise = site.people | where: "group", "rise" | sort: "order" -%}
{%- assign collab = site.people | where: "group", "collaborator" | sort: "order" -%}
{%- assign everyone = rise | concat: collab -%}

{%- if everyone.size > 0 %}
{% include peoplelist.html people=everyone %}
<p class="muted small">Team members employed elsewhere are shown with their employer.</p>
{%- endif %}

</div>

<p class="more"><a href="{{ '/partners/' | relative_url }}">All partners →</a></p>

</div>
</section>
</main>
