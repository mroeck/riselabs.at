---
layout: default
title: Impressum
permalink: /impressum/
description: >-
  Legal disclosure for riselabs.at under §5 ECG, §14 UGB and §25 Mediengesetz.
---

{%- assign im = site.data.impressum -%}

<main id="content">
<section class="band">
<div class="wrap narrow legal">

<h1>Impressum</h1>

<p class="muted">Offenlegung und Informationspflicht gemäß §&nbsp;5 E-Commerce-Gesetz,
§&nbsp;14 Unternehmensgesetzbuch und §&nbsp;25 Mediengesetz.
<span class="small">(Legal disclosure under Austrian law. The German wording is
the operative one; an English rendering of each heading follows in
brackets.)</span></p>

{%- if im.legal_form == "" or im.legal_form == nil %}
<p class="legal-warn"><strong>Diese Offenlegung ist noch unvollständig.</strong>
Die Rechtsform und weitere Pflichtangaben fehlen. Vor Veröffentlichung in
<code>_data/impressum.yml</code> ergänzen.</p>
{%- elsif im.trade_law_checked != true %}
<p class="legal-warn"><strong>Noch zu prüfen:</strong> ob die Tätigkeit der
Gewerbeordnung unterliegt. Falls ja, fehlen hier Gewerbe, Gewerbebehörde und
Kammerzugehörigkeit. Siehe Hinweise in <code>_data/impressum.yml</code>.
Dieser Hinweis erscheint nur im Entwurf.</p>
{%- endif %}

<h2>Medieninhaber und Diensteanbieter <span class="gloss">[media owner and service provider]</span></h2>

<p>
{{ im.name }}{% if im.legal_form != "" %}<br>{{ im.legal_form }}{% endif %}
{%- if im.trading_as != "" %}<br>{{ im.trading_as }}{% endif %}
</p>

{%- if im.owner and im.owner != "" %}
<p>Inhaber und Vertretung <span class="gloss">[owner and representation]</span>: {{ im.owner }}{% if im.owner_role and im.owner_role != "" %}<br>{{ im.owner_role }}{% endif %}</p>
{%- endif %}

<p>
{%- for line in im.address_lines %}{{ line }}{% unless forloop.last %}<br>{% endunless %}{% endfor %}
</p>

{%- if im.seat != "" %}
<p class="muted small">Sitz <span class="gloss">[registered seat]</span>: {{ im.seat }}</p>
{%- endif %}

<h2>Kontakt <span class="gloss">[contact]</span></h2>

<p>
E-Mail: <a href="mailto:{{ im.email }}">{{ im.email }}</a>
{%- if im.phone != "" %}<br>Telefon: <a href="tel:{{ im.phone | remove: ' ' }}">{{ im.phone }}</a>{% endif %}
{%- if im.linkedin_url and im.linkedin_url != "" %}<br>LinkedIn: <a href="{% include url.html u=im.linkedin_url %}">{{ im.linkedin_url | remove: "https://www." }}</a>{% endif %}
{%- if im.contact_form_url != "" %}<br>Kontaktformular: <a href="{% include url.html u=im.contact_form_url %}">{{ im.contact_form_url }}</a>{% endif %}
<br>Web: <a href="{{ site.url }}">{{ site.url | remove: "https://" }}</a>
</p>

{%- if im.firmenbuch_no != "" or im.uid != "" or im.zvr != "" %}
<h2>Register und Steuer <span class="gloss">[registration and tax]</span></h2>
<p>
{%- if im.firmenbuch_no != "" %}Firmenbuchnummer: {{ im.firmenbuch_no }}{% if im.firmenbuch_court != "" %}<br>Firmenbuchgericht: {{ im.firmenbuch_court }}{% endif %}{% endif %}
{%- if im.zvr != "" %}{% if im.firmenbuch_no != "" %}<br>{% endif %}ZVR-Zahl: {{ im.zvr }}{% endif %}
{%- if im.uid != "" %}{% if im.firmenbuch_no != "" or im.zvr != "" %}<br>{% endif %}UID-Nummer: {{ im.uid }}{% endif %}
</p>
{%- endif %}

{%- if im.gewerbe != "" or im.gewerbebehoerde != "" or im.wko != "" %}
<h2>Gewerberecht <span class="gloss">[trade law]</span></h2>
<p>
{%- if im.gewerbe != "" %}Gewerbe: {{ im.gewerbe }}{% endif %}
{%- if im.gewerbebehoerde != "" %}{% if im.gewerbe != "" %}<br>{% endif %}Aufsichtsbehörde: {{ im.gewerbebehoerde }}{% endif %}
{%- if im.wko != "" %}<br>Kammerzugehörigkeit: {{ im.wko }}{% endif %}
{%- if im.berufsrecht_url != "" %}<br>Anwendbare Rechtsvorschrift:
<a href="{{ im.berufsrecht_url }}">Gewerbeordnung (GewO) im RIS</a>{% endif %}
</p>
{%- endif %}

<h2>Unternehmensgegenstand <span class="gloss">[business purpose]</span></h2>
<p>{{ im.purpose }}</p>

{%- if im.blattlinie != "" %}
<h2>Grundlegende Richtung <span class="gloss">[editorial direction]</span></h2>
<p>{{ im.blattlinie }}</p>
{%- endif %}

{%- if im.ownership != "" %}
<h2>Beteiligungsverhältnisse <span class="gloss">[ownership]</span></h2>
<p>{{ im.ownership }}</p>
{%- endif %}

<h2>Haftung für Inhalte und Links <span class="gloss">[liability]</span></h2>

<p>Die Inhalte dieser Website werden mit Sorgfalt erstellt. Forschungsergebnisse
und Analysen geben den Stand zum Zeitpunkt der Veröffentlichung wieder.
Für Inhalte externer Websites, auf die verlinkt wird, sind ausschließlich
deren Betreiber verantwortlich.</p>

<h2>Urheberrecht <span class="gloss">[copyright]</span></h2>

<p>Texte und Grafiken auf dieser Website stehen, soweit nicht anders
angegeben, im Urheberrecht des Medieninhabers. Publikationen
und Daten sind bei der jeweiligen Veröffentlichung mit ihrer Lizenz
ausgewiesen; dort gilt die dort genannte Lizenz.</p>

{%- if site.privacy_url and site.privacy_url != "" %}
<h2>Datenschutz <span class="gloss">[data protection]</span></h2>
<p>Informationen zur Verarbeitung personenbezogener Daten finden sich in der
<a href="{% include url.html u=site.privacy_url %}">Datenschutzerklärung</a>.</p>
{%- endif %}

</div>
</section>
</main>
