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
  T1, "Where we work", below the team. Everything shown here comes from
  _data/place.yml, so a move is a change to that file and not to this page;
  the work order prepares the dieHauswirtschaft text for early 2027, and it
  is deliberately not on the page until Martin says so.

  Text left, pictures right from 56rem, pictures under the text on a phone.
  One wide picture at 16:9 and two at 3:2 beneath it. Each is cropped with
  `object-fit: cover` and the `focus` value from the data as its
  `object-position`, because the three files are 3:2, 4:3 and 3:2 and the
  interesting part of each is not in the middle.

  Every caption ends with its credit. The two Climate Lab photographs are
  published on Martin's decision of 2 Nov (H34); the team photograph is by
  Rue Munemo and everyone in it has consented (H35).

  With no images in the data the text runs full width, so the band never
  shows an empty box.
{%- endcomment -%}
{%- assign place = site.data.place -%}
<section class="band alt" id="where-we-work">
<div class="wrap">
  <h2>Where we work</h2>
  <p class="band-lede">We work mostly remotely, with colleagues in Austria,
  Switzerland and South Africa, and come together for team retreats and
  regular in-person meetings.</p>

  <div class="place{% if place.images.size == 0 %} place-notext{% endif %}">
    <div class="place-body">
      <h3>{{ place.name }}</h3>
      {%- for para in place.text %}
      <p>{{ para }}</p>
      {%- endfor %}
      <p class="place-address">
        {%- for line in place.address -%}
        {{ line }}{% unless forloop.last %}<br>{% endunless %}
        {%- endfor -%}
      </p>
      {%- if place.link %}
      <p class="more"><a href="{{ place.link.url }}">{{ place.link.label }} &rarr;</a></p>
      {%- endif %}
    </div>

    {%- if place.images.size > 0 %}
    <div class="place-shots">
      {%- for im in place.images -%}
      <figure class="place-shot place-{{ im.slot }}">
        <span class="tone"><img src="{{ im.src | relative_url }}" alt="{{ im.alt }}"
          loading="lazy"{% if im.focus %} style="object-position: {{ im.focus }}"{% endif %}></span>
        <figcaption class="muted small">{{ im.caption }}{% if im.credit %} Photo: {{ im.credit | strip }}.{% endif %}</figcaption>
      </figure>
      {%- endfor -%}
    </div>
    {%- endif %}
  </div>
</div>
</section>
</main>
