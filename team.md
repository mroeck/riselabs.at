---
layout: default
title: Team
permalink: /team/
---

<div class="page-head wrap narrow">
  <h1>Team</h1>
  <p class="lede">RISE is a growing team in Vienna. We work every day with
  researchers at partner institutions, and with a global network across
  policy, industry, and research.</p>
</div>

<main id="content">
<section class="band">
<!-- The full band width, not `narrow`. `narrow` is the reading measure,
     which is right for the lede above and wrong for a grid of cards.

     The cards are the stood-up kind since 1 Nov 2026: portrait on top as a
     1:1 crop, text beneath, three across. It is the shape the home page reel
     uses and the shape the project and publication grids use, so the three
     card grids on this site now read as one set. The flat card put a small
     portrait beside the text, which was dense but gave the photographs
     almost no room. -->
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

<p class="banner">We are growing. New colleagues join in 2027 and more
profiles are on their way. <a href="{{ '/join/' | relative_url }}">See open
positions &rarr;</a></p>

{% include filter.html target="#teamlist" placeholder="Filter the team…" %}

<div id="teamlist">

{%- assign rise = site.people | where: "group", "rise" | sort: "order" -%}
{%- assign collab = site.people | where: "group", "collaborator" | sort: "order" -%}
{%- assign everyone = rise | concat: collab -%}

{%- if everyone.size > 0 %}
{% include peoplelist.html people=everyone stacked="true" %}
<p class="muted small">Team members employed elsewhere are shown with their institution.</p>
{%- endif %}

</div>

<p class="more"><a href="{{ '/partners/' | relative_url }}">All partners →</a></p>

</div>
</section>

{%- comment -%}
  Where we work (Martin, 1 Nov 2026). The team is distributed and the page
  said nothing about that, which left a reader to guess whether "a growing
  team in Vienna" meant a room in Vienna.

  Every fact here is one the site already holds or Martin stated: the
  registered address in _data/impressum.yml is Climate Lab, Spittelauer
  Lände 45, 1090 Wien, and what Climate Lab is comes from climatelab.at.
  Nothing is said about how many people work there or how often the team
  meets beyond "regularly", because neither is known here.

  NOT mentioned, on purpose: the possible move to dieHauswirtschaft. Martin
  put it at early 2027 and called it an update to make then. A page that
  announces a move that has not happened is wrong twice if it does not.

  The photograph is the R11 placeholder. Climate Lab's own photographs are
  theirs, not ours to publish, and a stock picture of some other coworking
  space standing in for our office would be the same error docs/06 forbids
  for portraits. Replace `image` below once there is a photograph RISE took
  or has permission to use, and add `image_credit` if it is someone else's.
{%- endcomment -%}
<section class="band alt" id="where-we-work">
<div class="wrap">
  <h2>Where we work</h2>
  <div class="xfield">
    <figure class="xfield-img">
      <span class="tone"><img src="{{ '/assets/img/placeholders/placeholder-project.webp' | relative_url }}" alt="" loading="lazy"></span>
      <figcaption class="muted small">A photograph of the office is still to
      come.</figcaption>
    </figure>
    <div class="xfield-body">
      <p class="xlede">We work mostly remotely, and meet in person regularly:
      at team retreats, at partner workshops, and around the projects
      themselves.</p>
      <p>Our on-site team is based at <a href="https://climatelab.at/">Climate
      Lab</a> in Vienna, an innovation centre for the climate transition run
      by Impact Hub Vienna. It brings together organisations working on the
      energy transition, sustainable building and the circular economy, which
      is to say the people our work is for are in the building.</p>
      <p class="muted small">Climate Lab, Spittelauer Lände 45, 1090 Vienna,
      Austria. It is also our registered address; see the
      <a href="{{ '/impressum/' | relative_url }}">Impressum</a>.</p>
    </div>
  </div>
</div>
</section>
</main>
