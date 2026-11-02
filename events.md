---
layout: null
permalink: /events/
sitemap: false
---
<!doctype html>
<!-- /events/ became part of /news/ on 2 Nov 2026 (N5). The two pages showed
     almost the same list, so they are one page with tabs, and this stays
     behind so nothing already linked to /events/ breaks.

     A meta refresh rather than a plugin: GitHub Pages runs a fixed plugin
     list and jekyll-redirect-from is not in this site's, so adding it would
     mean changing the build for one page. `canonical` points at /news/ and
     `noindex` keeps this page out of search results, which is what a
     redirect page is for. The link below is for anyone whose browser does
     not follow the refresh. -->
<html lang="{{ site.lang | default: "en" }}">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={{ '/news/#events' | relative_url }}">
<link rel="canonical" href="{{ '/news/' | absolute_url }}">
<meta name="robots" content="noindex">
<title>Events have moved to News and events</title>
</head>
<body>
<p>Events are now part of
<a href="{{ '/news/#events' | relative_url }}">News and events</a>.</p>
</body>
</html>
