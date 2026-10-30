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

{%- comment -%}
  The evidence, before anything else. The page used to open on what RISE
  works on; it now opens on what the work found, with the figure, its unit
  and its source in the first line of each.

  Every figure is from a published, peer-reviewed paper that is on this site,
  so each links to its own entry rather than to a claim nobody can check.
  Nothing unpublished goes in this band. If a number here cannot be followed
  to a paper, it does not belong.
{%- endcomment -%}
<section class="band" id="evidence">
  <div class="wrap">
    <h2>What the evidence says</h2>
    <p class="band-lede">Efficiency alone will not get Europe's buildings
    within their limits. Our research shows why, and what does.</p>

    <ul class="figures">
      <li>
        <p class="fig-val">8.5 billion tonnes CO<sub>2</sub>e</p>
        <p class="fig-say">what EU buildings and construction must avoid
        between 2020 and 2050 to meet EU climate targets. That is about ten
        years of 2020 emissions.</p>
        <p class="fig-src"><a href="{{ '/publications/alaux-2026-context-specific-life/' | relative_url }}">Alaux et al., 2026, Nature Communications</a></p>
      </li>
      <li>
        <p class="fig-val">32%</p>
        <p class="fig-say">the share of that reduction which efficiency and
        cleaner materials alone could not deliver within national capacities,
        2.72 billion tonnes short.</p>
        <p class="fig-src"><a href="{{ '/publications/alaux-2026-context-specific-life/' | relative_url }}">Alaux et al., 2026</a></p>
      </li>
      <li>
        <p class="fig-val">2.2 billion tonnes CO<sub>2</sub>e</p>
        <p class="fig-say">the additional reduction within national capacities
        from using less floor space per person, circular construction and
        bio-based materials.</p>
        <p class="fig-src"><a href="{{ '/publications/alaux-2026-context-specific-life/' | relative_url }}">Alaux et al., 2026</a></p>
      </li>
      <li>
        <p class="fig-val">45&ndash;50%</p>
        <p class="fig-say">the share of life cycle emissions that are embodied
        in highly energy-efficient buildings, from more than 650 building life
        cycle assessments.</p>
        <p class="fig-src"><a href="{{ '/publications/roeck-2020-embodied-ghg-emissions/' | relative_url }}">Röck et al., 2020, Applied Energy</a></p>
      </li>
    </ul>

    <p class="more"><a href="{{ '/publications/' | relative_url }}">Read the research →</a></p>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    {%- comment -%}
      Four pillars, replacing three values. The old three described a stance;
      these describe an order of work, and each one is something a reader can
      hold RISE to. "Stronger together" is folded into the fourth as shared
      infrastructure many actors can use at once, which says the same thing in
      a way the work can show.
    {%- endcomment -%}
    <h2>What we stand for</h2>
    <div class="cols pillars">
      <div>
        <h3>Within limits</h3>
        <p class="muted">We start from what the planet can bear: carbon
        budgets and planetary boundaries. Not from what is convenient to
        reduce.</p>
      </div>
      <div>
        <h3>Enough, then efficient</h3>
        <p class="muted">The lowest-carbon building is the one we do not build
        new. Renovating, sharing and using space better come before building
        cleaner.</p>
      </div>
      <div>
        <h3>Whole-system gains</h3>
        <p class="muted">A carbon cut that costs nature, affordability or
        material justice is not a gain. We count what others leave out.</p>
      </div>
      <div>
        <h3>Open by default</h3>
        <p class="muted">We publish our methods, data and code wherever
        licences allow, and build shared infrastructure that many can use at
        once.</p>
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

<section class="band">
  <div class="wrap">
    <h2>What we are working on</h2>
    <p class="band-note">Research and advisory work for the European
    Commission, national governments, international organisations and
    philanthropic funders.</p>
    {%- assign current = site.projects | where: "status", "current" | sort: "years" | reverse | slice: 0, 3 -%}
    {% include projectgrid.html projects=current %}
    <p class="more"><a href="{{ '/projects/' | relative_url }}">All projects →</a></p>
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
{%- comment -%}
  NOTE ON THE BAND RHYTHM: this band is conditional, and the bands either
  side of it are `--bg`. Turning `home_team_band` off therefore puts two
  `--bg` bands next to each other, which is the one thing the rule at the top
  of this file forbids. If it is ever turned off, flip the "Latest" band to
  `.alt` at the same time.
{%- endcomment -%}
{%- if site.home_team_band %}
{%- assign rise = site.people | where: "group", "rise" | sort: "order" -%}
{%- assign collab = site.people | where: "group", "collaborator" | sort: "order" -%}
{%- assign team = rise | concat: collab -%}
{%- if team.size > 1 %}
<section class="band alt">
  <div class="wrap">
    <h2>The team</h2>
    <p class="band-note">Based in Vienna, working with a global network across
    policy, industry, and research.</p>
    {%- comment -%}
      Two at a time, rotating through everyone. The band stays compact and
      the whole team is still reachable, both through the rotation and
      through the link below it, which shows the full grid.

      Every card is in the markup; the script hides all but the current pair
      and adds the controls. Without JavaScript this is the ordinary grid
      with everybody in it, which is a complete band on its own.
    {%- endcomment -%}
    <div class="carousel" data-carousel="2">
      {% include peoplelist.html people=team %}
    </div>
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
<section class="band">
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
        wherever licensing allows. <a href="#work-with-us">Get in touch</a> to
        learn more.</p>
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
<section class="band alt">
  <div class="wrap">
    <h2>Who relies on our evidence</h2>
    <p class="band-note">The European Commission, UN agencies, national
    governments, research institutes and philanthropic funders use our work to
    set targets, write rules and fund change.</p>
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
    <h2>Start with the problem</h2>
    <p class="band-lede">We would rather hear the problem than the brief. Tell
    us what you need to decide, and we will tell you what evidence would
    help.</p>
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
