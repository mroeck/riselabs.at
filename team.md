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
  Open positions, 4 Nov 2026. The team page is where someone looks when they
  are wondering whether there is room for them, so the live openings are
  named here rather than only on /join/.

  The band hides itself when nothing is open, so the page never carries an
  empty "we are hiring" heading.

  The deadline test is the same one join.html runs, written out a second time
  rather than shared: the two lists look different enough that one include
  with a style switch would be a worse trade than two short loops. Listed
  under differences for the design phase, which is where Q5 will decide.
{%- endcomment -%}
{%- assign today = 'now' | date: "%Y%m%d" | plus: 0 -%}
{%- assign all_openings = site.posts | where: "type", "opening" | sort: "position_id" -%}
{%- assign open_count = 0 -%}
{%- for post in all_openings -%}
  {%- assign close = post.deadline | date: "%Y%m%d" | plus: 0 -%}
  {%- if close >= today %}{% assign open_count = open_count | plus: 1 %}{% endif -%}
{%- endfor -%}
{%- if open_count > 0 %}
<section class="band" id="open-positions">
<div class="wrap narrow">
  <h2>Open positions</h2>
  <p class="band-lede">We are hiring. The full advert for each position,
  including what we offer and how we work, is on its own page and as a PDF.</p>

  <ul class="openings">
    {%- for post in all_openings -%}
    {%- assign close = post.deadline | date: "%Y%m%d" | plus: 0 -%}
    {%- if close >= today %}
    <li>
      <p class="meta">
        <span class="date">Apply by {{ post.deadline | date: "%d %B %Y" }}</span>
        {%- if post.location %}<span class="funder">{{ post.location }}</span>{% endif -%}
      </p>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      {%- if post.summary %}<p class="sum">{{ post.summary }}</p>{% endif -%}
    </li>
    {%- endif -%}
    {%- endfor -%}
  </ul>

  <p class="more"><a href="{{ '/join/' | relative_url }}">How to apply, and other ways in →</a></p>
</div>
</section>
{%- endif %}

{%- comment -%}
  T1, "Where we work", below the team. Everything shown here comes from
  _data/place.yml, so a move is a change to that file and not to this page.

  Two places since 2 Nov 2026: Climate Lab today, and dieHausWirtschaft from
  2027. Both are in the data file's `places` list and the page loops it, so
  when the move happens it is a reordering of that list and the labels above
  the names, with nothing to change here. Climate Lab stays on the page after
  the move: the membership and the events continue.

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
    {%- comment -%}
      The first place takes the text column beside the photographs. The
      photographs are of the team and of the desks it works at now, so they
      belong to that one; anything after it spans the full width underneath,
      where there is no picture column to leave half empty.
    {%- endcomment -%}
    {%- for p in place.places limit:1 -%}
    {% include placeblock.html p=p wrap="place-body" %}
    {%- endfor %}

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

    {%- for p in place.places offset:1 -%}
    {% include placeblock.html p=p wrap="place-next" %}
    {%- endfor %}
  </div>
</div>
</section>
</main>
