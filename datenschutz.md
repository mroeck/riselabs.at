---
layout: default
title: Datenschutzerklärung
permalink: /datenschutz/
description: >-
  Information on the processing of personal data on riselabs.at under the
  GDPR - hosting, newsletter, contact, and your rights.
---

{%- assign im = site.data.impressum -%}

{%- comment -%}
  Written as explicit HTML, like the other static pages: these sections sit
  inside <main> and <section>, and kramdown does not parse markdown inside
  block-level HTML.

  This describes what the site actually does as built - no cookies,
  cookieless audience measurement with Plausible, self-hosted fonts, one
  external processor for the newsletter, and one stored preference (the
  theme). If that changes, this page has to change with it. In particular,
  adding any embed (a video, a map, a social widget) means a new section
  here, and usually a consent banner too.

  The Reichweitenmessung section below went live with the Plausible snippet
  on 4 November 2026 (R10, H25). The two belong together: the script must
  never be on the site while this page says there is no analytics.
{%- endcomment -%}

<div class="page-head wrap narrow">
  <h1>Datenschutzerklärung</h1>
  <p class="lede">Information über die Verarbeitung personenbezogener Daten
  nach Art. 13 und 14 DSGVO.</p>
</div>

<main id="content">
<section class="band">
<div class="wrap narrow legal">

<p class="muted small">Legal text under Austrian and EU law; the German
wording is the operative one, with an English rendering of each heading in
brackets. Stand: {{ site.data.privacy_updated | default: "4. November 2026" }}.</p>

<h2>Verantwortlicher <span class="gloss">[controller]</span></h2>

<p>
{{ im.name }}<br>
{%- for line in im.address_lines %}{{ line }}{% unless forloop.last %}<br>{% endunless %}{% endfor %}<br>
E-Mail: <a href="mailto:{{ im.email }}">{{ im.email }}</a>
</p>

<p class="muted small">Ein Datenschutzbeauftragter ist nicht bestellt, da die
Voraussetzungen des Art. 37 DSGVO nicht vorliegen.</p>

<h2>Grundsatz <span class="gloss">[in short]</span></h2>

<p>Diese Website setzt keine Cookies und bindet keine Werbe- oder
Social-Media-Dienste ein. Schriftarten werden lokal von diesem Server
ausgeliefert und nicht von Dritten nachgeladen. Zur Reichweitenmessung wird
ein cookiefreies Verfahren eingesetzt, das unten beschrieben ist.
Personenbezogene Daten werden nur in den unten beschriebenen Fällen
verarbeitet.</p>

<h2>Gespeicherte Einstellung <span class="gloss">[stored preference]</span></h2>

<p>Wenn Sie über die Schaltfläche am unteren Bildschirmrand zwischen dem
dunklen und dem hellen Erscheinungsbild wechseln, wird diese Auswahl in der
lokalen Browser-Speicherung (<em>localStorage</em>) Ihres Geräts unter dem
Schlüssel <code>rise-theme</code> abgelegt. Gespeichert wird ausschließlich
das Wort <code>dark</code> oder <code>light</code>.</p>

<p>Diese Speicherung erfolgt ausschließlich auf Ihre ausdrückliche Handlung
hin und dient allein dazu, Ihre Auswahl beim nächsten Seitenaufruf
beizubehalten. Es findet keine Übertragung an uns oder an Dritte statt, es
werden keine Kennungen vergeben und es erfolgt keinerlei Wiedererkennung oder
Analyse Ihres Nutzungsverhaltens. Da es sich um eine von Ihnen selbst
veranlasste Einstellung handelt, ist hierfür keine gesonderte Einwilligung
erforderlich (§ 165 Abs. 3 TKG 2021).</p>

<p>Sie können den Eintrag jederzeit löschen, indem Sie die Websitedaten in
Ihrem Browser entfernen. Wird die Speicherung durch Ihre Browser-Einstellungen
unterbunden, funktioniert die Umschaltung weiterhin - die Auswahl gilt dann
nur für die aktuelle Seite.</p>

<h2>Reichweitenmessung <span class="gloss">[audience measurement]</span></h2>

<p>Wir messen die Nutzung dieser Website mit <strong>Plausible
Analytics</strong>, einem Dienst der Plausible Insights OÜ, Estland. Die
Verarbeitung findet auf Servern innerhalb der Europäischen Union statt. Eine
Übermittlung in Drittstaaten erfolgt nicht.</p>

<p>Das Verfahren arbeitet ohne Cookies und ohne Speicherung oder Auslesen von
Informationen auf Ihrem Endgerät. Es werden keine gerätebezogenen Kennungen
vergeben und keine Profile gebildet. Ihre IP-Adresse wird nicht gespeichert:
sie fließt zusammen mit einem täglich wechselnden Zufallswert, der Domain
dieser Website und Ihrer Browser-Kennung in einen Hashwert ein, aus dem sich
die IP-Adresse nicht zurückrechnen lässt. Der Zufallswert wird alle 24 Stunden
gelöscht, sodass eine Wiedererkennung über den Tag hinaus oder über andere
Websites hinweg nicht möglich ist.</p>

<p>Erhoben werden dabei:</p>

<ul>
  <li>die aufgerufene Seite sowie Datum und Uhrzeit des Aufrufs;</li>
  <li>die verweisende Website, sofern Sie über einen Link gekommen sind;</li>
  <li>das Herkunftsland, abgeleitet aus der IP-Adresse, die dabei nicht
      gespeichert wird;</li>
  <li>Gerätetyp, Browser und Betriebssystem in gröberer Form;</li>
  <!-- This last bullet is only true while "Outbound links" and "File
       downloads" are enabled in the Plausible dashboard for riselabs.at.
       With the current snippet the features are set there, not in the
       script's file name, so nothing in this repository can check it. If
       either is turned off, shorten this bullet to match; if both are, delete
       it. Declaring more than is collected is not a breach, but it is wrong,
       and a privacy page that is wrong in one place is not trusted in the
       others. -->
  <li>Klicks auf Links zu anderen Websites sowie Downloads von Dateien, etwa
      der Stellenausschreibungen als PDF.</li>
</ul>

<p>Diese Angaben lassen für sich genommen und in Verbindung miteinander keinen
Rückschluss auf Ihre Person zu. Wir verwenden sie ausschließlich in
zusammengefasster Form, um zu verstehen, welche Inhalte gelesen werden und
über welche Wege Besucherinnen und Besucher zu uns finden.</p>

<p>Rechtsgrundlage ist unser berechtigtes Interesse an einer datensparsamen
Reichweitenmessung gemäß Art. 6 Abs. 1 lit. f DSGVO. Unser Interesse besteht
darin, die Website auf Grundlage tatsächlicher Nutzung zu verbessern. Da keine
Cookies gesetzt, keine Kennungen vergeben und keine personenbezogenen Daten
gespeichert werden, überwiegen Ihre schutzwürdigen Interessen nach unserer
Einschätzung nicht.</p>

<p>Plausible Insights OÜ ist für uns als Auftragsverarbeiterin tätig. Die
Vereinbarung zur Auftragsverarbeitung nach Art. 28 DSGVO ist Bestandteil der
Nutzungsbedingungen des Dienstes.</p>

<p>Wenn Sie nicht gezählt werden möchten, können Sie in Ihrem Browser unter
<em>localStorage</em> für diese Website den Schlüssel
<code>plausible_ignore</code> auf <code>true</code> setzen; Besuche von diesem
Browser werden dann nicht mehr erfasst. Da keine personenbezogenen Daten
verarbeitet werden, ist darüber hinaus kein Widerspruch erforderlich.</p>

<p class="muted small">Weitere Angaben des Anbieters zum Datenschutz:
<a href="https://plausible.io/data-policy">plausible.io/data-policy</a>.</p>

<h2>Hosting und Server-Logs <span class="gloss">[hosting and server logs]</span></h2>

<p>Die Website wird auf GitHub Pages gehostet, einem Dienst der GitHub, Inc.,
88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der
Website wird nach Angaben von GitHub die IP-Adresse der Besucherinnen und
Besucher zu Sicherheitszwecken protokolliert und gespeichert - unabhängig
davon, ob eine Anmeldung bei GitHub besteht.</p>

<p>Auf Umfang und Dauer dieser Protokollierung haben wir keinen Einfluss und
keinen Zugriff auf die Protokolldaten. Rechtsgrundlage ist Art. 6 Abs. 1
lit. f DSGVO; das berechtigte Interesse liegt in der sicheren und
zuverlässigen Bereitstellung der Website. Die Verarbeitung erfolgt in den
USA. Näheres in der
<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">Datenschutzerklärung
von GitHub</a>.</p>

<h2>Newsletter <span class="gloss">[newsletter]</span></h2>

<p>Für den Versand unseres Newsletters nutzen wir Buttondown, LLC,
406 W Franklin St. #201, Richmond, VA 23221, USA. Bei der Anmeldung wird die
eingegebene E-Mail-Adresse an Buttondown übermittelt und dort gespeichert.
Buttondown verarbeitet außerdem technische Daten des Anmeldevorgangs sowie
Daten zur Zustellung der Newsletter.</p>

<p>Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO.
Sie können diese Einwilligung jederzeit mit Wirkung für die Zukunft
widerrufen - über den Abmeldelink in jedem Newsletter oder formlos per
E-Mail an <a href="mailto:{{ im.email }}">{{ im.email }}</a>. Nach dem
Widerruf wird die E-Mail-Adresse aus dem Verteiler gelöscht.</p>

<p>Mit Buttondown besteht ein Auftragsverarbeitungsvertrag. Die Verarbeitung
erfolgt in den USA; für die Übermittlung gelten die Standardvertragsklauseln
des Durchführungsbeschlusses (EU) 2021/914, Modul 2. Siehe den
<a href="https://buttondown.com/legal/data-processing-agreement">Data
Processing Agreement</a> und die
<a href="https://buttondown.com/legal/subprocessors">Liste der
Unterauftragsverarbeiter</a> von Buttondown.</p>

<h2>Kontaktaufnahme <span class="gloss">[contact]</span></h2>

<p>Wenn Sie uns per E-Mail kontaktieren, verarbeiten wir die übermittelten
Daten zur Bearbeitung Ihrer Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b
DSGVO bei vertragsbezogenen Anfragen, sonst Art. 6 Abs. 1 lit. f DSGVO
aufgrund unseres berechtigten Interesses an der Beantwortung. Die Daten
werden gelöscht, sobald sie nicht mehr erforderlich sind und keine
gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>

<h2>Externe Links <span class="gloss">[external links]</span></h2>

<p>Diese Website verlinkt auf externe Websites, unter anderem auf unser
LinkedIn-Profil, auf Projektwebsites und auf Publikationen bei Verlagen und
Repositorien. Beim Anklicken eines solchen Links verlassen Sie diese Website;
für die Datenverarbeitung auf der Zielseite ist deren Betreiber
verantwortlich. Es werden keine Inhalte Dritter eingebettet, die bereits beim
Laden einer Seite eine Verbindung herstellen würden.</p>

<h2>Ihre Rechte <span class="gloss">[your rights]</span></h2>

<p>Ihnen stehen gegenüber dem Verantwortlichen die folgenden Rechte zu:
Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17),
Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20)
sowie Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen
(Art. 21). Eine erteilte Einwilligung können Sie jederzeit nach Art. 7 Abs. 3
DSGVO widerrufen; die Rechtmäßigkeit der bis dahin erfolgten Verarbeitung
bleibt davon unberührt.</p>

<p>Zur Ausübung dieser Rechte genügt eine E-Mail an
<a href="mailto:{{ im.email }}">{{ im.email }}</a>.</p>

<h2>Beschwerderecht <span class="gloss">[right to complain]</span></h2>

<p>Wenn Sie der Ansicht sind, dass die Verarbeitung Ihrer Daten gegen die
DSGVO verstößt, können Sie sich bei einer Aufsichtsbehörde beschweren. In
Österreich ist das die<br>
Österreichische Datenschutzbehörde<br>
Barichgasse 40–42, 1030 Wien<br>
<a href="mailto:dsb@dsb.gv.at">dsb@dsb.gv.at</a> ·
<a href="https://www.dsb.gv.at/">dsb.gv.at</a></p>

<h2>Änderungen <span class="gloss">[changes]</span></h2>

<p>Wir passen diese Erklärung an, wenn sich die Website oder die
Rechtsgrundlagen ändern. Es gilt jeweils die hier veröffentlichte Fassung.</p>

</div>
</section>
</main>
