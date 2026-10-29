---
layout: default
title: Home
permalink: /
---

{%- comment -%}
  Seven bands (L2), in this order and for these reasons:

    1  hero
    2  current projects   what we actually do, in pictures, before any claim
    3  what we stand for  the claim, with the two ways into the argument
    4  team               who does it. Gated; see home_team_band in _config.yml
    5  latest + publications, side by side on a wide screen
    6  partners and quotes, on one surface band
    7  work with us, with the newsletter as its last row

  Alternate bands carry `.band.alt`, so the page has a rhythm instead of
  running as one column. Every band has a real heading.

  THE RULE, FROM R2: two adjacent bands never share a background. Reading
  down, the backgrounds must go bg / surface / bg / surface and so on, with
  the hero and the closing band as the two exceptions, which carry a photo and
  the CI gradient. It is not decoration: when the review was written the page
  ran blush, white, white, blush, blush, so two pairs of neighbours merged and
  the bands stopped being bands.

  So: adding, removing or reordering a band means re-checking every `.band`
  below it and flipping `.alt` where it now clashes. There is nothing
  automatic about it, because the bands are written out here rather than
  generated. The order is:

    1  hero            photo
    2  current projects   --bg
    3  what we stand for  --surface   (.alt)
    4  team               --bg
    5  latest + pubs      --surface   (.alt)
    6  partners + quotes  --bg
    7  work with us       --gradient  (.cta-band)
{%- endcomment -%}

{% include hero.html %}

<main id="content">

<section class="band">
  <div class="wrap">
    <h2>Current projects</h2>
    <p class="band-note">Research and advisory work for the European
    Commission, national governments, international organisations and
    philanthropic funders.</p>
    {%- assign current = site.projects | where: "status", "current" | sort: "years" | reverse | slice: 0, 3 -%}
    {% include projectgrid.html projects=current %}
    <p class="more"><a href="{{ '/projects/' | relative_url }}">All projects →</a></p>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    <h2>What we stand for</h2>
    <div class="cols pillars">
      <div>
        <h3>Systemic decarbonisation</h3>
        <p class="muted">Reducing and removing the emissions and resource use
        locked into how we build - and redistributing what the built
        environment takes and gives.</p>
      </div>
      <div>
        <h3>Planetary boundaries</h3>
        <p class="muted">Healthy ecosystems are the foundation for sustainable
        development and resilient societies. We help understand where the
        balance is.</p>
      </div>
      <div>
        <h3>Stronger together</h3>
        <p class="muted">Collective action, solidarity and systems of care -
        because effective climate action is never done alone.</p>
      </div>
    </div>

    {%- comment -%}
      The old "onward" band, folded in here: it was two links sitting alone
      between the quotes and the offer, which is a band's worth of page for
      two links.
    {%- endcomment -%}
    <div class="onward">
      <a href="{{ '/approach/' | relative_url }}">
        <span class="onward-t">How we work</span>
        <span class="onward-d muted">The three strands, the post-growth
        question, and the methods behind the numbers.</span>
      </a>
      <a href="{{ '/expertise/' | relative_url }}">
        <span class="onward-t">What we do</span>
        <span class="onward-d muted">Six fields of work - assessment,
        stock modelling, policy evidence, data, methods and teaching.</span>
      </a>
    </div>
  </div>
</section>

{%- comment -%}
  The team band. Built and ready, deliberately off: `home_team_band` in
  _config.yml is false until the team page itself is complete, because a
  "Team" band showing one person says the wrong thing. Flip that one flag to
  turn it on; nothing else needs changing.

  L3 (large portraits, black and white, a quote beside the row) is a separate
  piece of work and waits on the collaborators' profiles being confirmed.
{%- endcomment -%}
{%- if site.home_team_band %}
{%- assign rise = site.people | where: "group", "rise" | sort: "order" -%}
{%- assign collab = site.people | where: "group", "collaborator" | sort: "order" -%}
{%- assign team = rise | concat: collab -%}
{%- if team.size > 1 %}
<section class="band">
  <div class="wrap">
    <h2>The team</h2>
    <p class="band-note">A small institute in Vienna, working with a wider
    network across policy, industry and research.</p>
    {% include peoplelist.html people=team %}
    <p class="more"><a href="{{ '/team/' | relative_url }}">The whole team →</a></p>
  </div>
</section>
{%- endif %}
{%- endif %}

{%- comment -%}
  Latest and Recent publications side by side from 64rem, stacked below it.
  They were two full-width bands of text one after the other, which is most
  of why the page read as a single column of prose.
{%- endcomment -%}
<section class="band alt">
  <div class="wrap">
    <div class="home-split">
      <div>
        <h2>Latest</h2>
        {%- assign featured = site.posts | where: "featured", true -%}
        {%- assign others = site.posts | where_exp: "p", "p.featured != true" -%}
        {%- assign latest = featured | concat: others | slice: 0, 3 -%}
        {% include newslist.html posts=latest %}
        <p class="more"><a href="{{ '/news/' | relative_url }}">All news →</a></p>
      </div>
      <div>
        <h2>Recent publications</h2>
        <p class="band-note">We publish our methods, data and code openly
        wherever licensing allows. A benchmark nobody can reproduce is an
        opinion.</p>
        {%- assign recent = site.publications | sort: "year" | reverse | slice: 0, 3 -%}
        {% include publist.html pubs=recent %}
        <p class="more"><a href="{{ '/publications/' | relative_url }}">All publications →</a></p>
      </div>
    </div>
  </div>
</section>

{%- comment -%}
  Partners and the quotes on one surface band: both are other people vouching
  for the work, and they were two separate full-width bands doing the same job.
{%- endcomment -%}
<section class="band">
  <div class="wrap">
    <h2>We work with</h2>
    {%- comment -%} hand-picked, in this order; the full list is on /partners/ {%- endcomment -%}
    {%- assign shown = "worldgbc,smith-innovation,bpie,iiasa,ec-dg-grow,unep,laudes,global-industry-hub,epfl,ku-leuven" | split: "," -%}
    {% include partners.html keys=shown %}
    <p class="more"><a href="{{ '/partners/' | relative_url }}">All partners →</a></p>

    {% include testimonials.html only="brigitte-jacquemont,xavier-le-den,simone-kongsbak" short="true" bare="true" %}
  </div>
</section>

{%- comment -%}
  The four ways work starts, from _data/engagement.yml, the same source
  /expertise/ reads. Each card's link prefills the subject line, so an
  enquiry arrives already sorted by what it is about, and each card names two
  projects that began that way, so none of it is an unbacked claim. The
  newsletter is the last row of this band rather than a band of its own: it is
  the smaller ask for a reader not ready for the larger one.

  The lede names who, not what. The projects band near the top of this page
  already shows what.
{%- endcomment -%}
<section class="band cta-band" id="work-with-us">
  <div class="wrap">
    <h2>Work with us</h2>
    <p class="band-lede">We work with public authorities, international
    organisations, funders, research partners and the pioneers changing how we
    build. Most collaborations start in one of four ways.</p>
    {% include engagement.html style="cards" %}
    <p class="muted small">Or write to
    <a href="mailto:{{ site.email }}">{{ site.email }}</a> if none of those
    quite fits.</p>

    <div class="home-news">
      {% include newsletter.html %}
    </div>
  </div>
</section>

</main>
