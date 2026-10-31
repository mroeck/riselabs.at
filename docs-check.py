#!/usr/bin/env python3
"""Check the RISE site before publishing.

Run it from the repository root:   python3 docs-check.py

It reads every content file and reports what Jekyll will not: references
to files that do not exist, missing images, missing required fields,
navigation pointing at pages that are not there, and front matter using a
field name Jekyll reserves for itself. Needs Python 3 and PyYAML.
"""
import pathlib, re, sys, yaml

SITE = pathlib.Path(__file__).resolve().parent
problems = []
notes = []


def P(kind, where, msg):
    problems.append((kind, where, msg))


def N(where, msg):
    notes.append((where, msg))


def split_fm(path):
    t = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    if not m:
        return None, t
    try:
        return yaml.safe_load(m.group(1)) or {}, m.group(2)
    except yaml.YAMLError as e:
        P("yaml", path.name, f"front matter will not parse: {e}")
        return None, m.group(2)


cfg, _ = split_fm(SITE / "_config.yml") if False else (yaml.safe_load((SITE / "_config.yml").read_text()), "")

# ---------------------------------------------------------------- collections
coll = {}
# Every slug with a file, including the unpublished ones. A reference to a
# person who exists but has not approved their text yet is not a broken
# reference, and saying "has no file" about a file that is sitting right
# there sends whoever reads it looking for the wrong problem.
on_disk = {}
for name in ("projects", "people", "publications", "partners"):
    coll[name] = {}
    on_disk[name] = set()
    for f in sorted((SITE / f"_{name}").glob("*.md")):
        fm, body = split_fm(f)
        if fm is None:
            continue
        on_disk[name].add(f.stem)
        if fm.get("published") is False:      # templates and drafts
            continue
        coll[name][f.stem] = (fm, body, f)

posts = {}
for f in sorted((SITE / "_posts").glob("*.md")):
    fm, body = split_fm(f)
    if fm is None:
        continue
    posts[f.stem] = (fm, body, f)

print(f"projects {len(coll['projects'])}  people {len(coll['people'])}  "
      f"publications {len(coll['publications'])}  partners {len(coll['partners'])}  "
      f"posts {len(posts)}")

# -------------------------------------------------------- required front matter
REQUIRED = {
    "projects": ["title", "summary"],
    "people": ["name", "role"],
    "publications": ["title", "year"],
    "partners": ["name"],
}
for cname, items in coll.items():
    for slug, (fm, body, f) in items.items():
        for key in REQUIRED[cname]:
            if not fm.get(key):
                P("frontmatter", f"_{cname}/{slug}.md", f"missing `{key}`")

for slug, (fm, body, f) in posts.items():
    if not fm.get("title"):
        P("frontmatter", f"_posts/{slug}.md", "missing `title`")

# ------------------------------------------------------------ cross-references
# which key in which collection points at which other collection
XREF = [
    ("projects",     "people",    "people"),
    ("projects",     "clients",   "partners"),
    ("projects",     "partners",  "partners"),
    ("publications", "people",    "people"),
    ("publications", "projects",  "projects"),
    ("publications", "partners",  "partners"),
    ("people",       "projects",  "projects"),
]
for src, key, target in XREF:
    for slug, (fm, body, f) in coll[src].items():
        vals = fm.get(key) or []
        if isinstance(vals, str):
            P("xref", f"_{src}/{slug}.md", f"`{key}` is a string, should be a list")
            vals = [vals]
        for v in vals:
            if v in coll[target]:
                continue
            # `rise` is a partner key with no file behind it on purpose:
            # _includes/partners.html writes that tile itself and points it at
            # the home page, because a file would give RISE a partner page of
            # its own and list it on /partners/ among the organisations we
            # work with. The rule just above this loop's block checks where it
            # is allowed to appear.
            if target == "partners" and v == "rise":
                continue
            if v in on_disk[target]:
                N(f"_{src}/{slug}.md",
                  f"`{key}` names {v}, whose file is still unpublished, so the "
                  "link will appear on its own once that file goes live")
            else:
                P("xref", f"_{src}/{slug}.md",
                  f"`{key}` points at '{v}', which has no file in _{target}/")

for slug, (fm, body, f) in posts.items():
    for key, target in (("projects", "projects"), ("people", "people"),
                        ("publications", "publications"), ("partners", "partners")):
        vals = fm.get(key) or []
        if isinstance(vals, str):
            vals = [vals]
        for v in vals:
            if v not in coll[target]:
                P("xref", f"_posts/{slug}.md",
                  f"`{key}` points at '{v}', which has no file in _{target}/")

# ------------------------------------------------- data files referencing slugs
svc = yaml.safe_load((SITE / "_data/expertise.yml").read_text()) or []
for s in svc:
    # The question is what heads the field on the page; the title is the
    # method, and it reads as a label under it. A field that loses its
    # question silently falls back to the method name, which is the old page
    # and gives no sign that anything is missing.
    if not (s.get("question") or "").strip():
        P("data", "_data/expertise.yml",
          f"the field '{s.get('title')}' has no `question`. The page heads "
          "each field with the question a client arrives with.")
    elif not s["question"].rstrip().endswith("?"):
        P("data", "_data/expertise.yml",
          f"`question` for '{s.get('title')}' does not end in a question "
          "mark. It is meant to be the question, not a restatement.")
    ex = s.get("example")
    if ex and ex not in coll["projects"]:
        P("xref", "_data/services.yml", f"example '{ex}' has no file in _projects/")

# The four ways work starts. Each card claims a way of working and then names
# projects that began that way, which is the only thing that keeps the card
# from being a brochure line. So the slugs are checked hard: a card pointing at
# a project that is not there would render as a card with one example, or
# none, and nobody would notice.
eng = yaml.safe_load((SITE / "_data/engagement.yml").read_text()) or []
_eng_ids = set()
for e in eng:
    where = f"entry '{e.get('title', '?')}'"
    for key in ("id", "title", "action", "subject", "body"):
        if not e.get(key):
            P("data", "_data/engagement.yml", f"{where} has no `{key}`")
    if e.get("id") in _eng_ids:
        P("data", "_data/engagement.yml", f"duplicate id '{e['id']}'")
    _eng_ids.add(e.get("id"))

    exs = e.get("examples") or []
    for ex in exs:
        if ex not in coll["projects"]:
            P("xref", "_data/engagement.yml",
              f"{where} gives the example '{ex}', which has no file in _projects/")
    if len(exs) < 2:
        N("_data/engagement.yml",
          f"{where} has {len(exs)} worked example(s). The card is meant to "
          "name two projects that started this way; if there are not two, the "
          "card may be describing something RISE does not actually do.")

# The six homepage facts (F1). Each figure on that band is a claim about the
# world with a paper behind it, and the whole point of the band is that a
# visitor can follow any number to the work it came from. A `publication` slug
# with no file behind it would render as a dead link under a headline figure,
# which is worse than no figure at all - so it fails rather than warns.
facts = yaml.safe_load((SITE / "_data/facts.yml").read_text()) or []
_f_seen = set()
for f in facts:
    where = f"fact '{f.get('perspective', '?')}'"
    for key in ("perspective", "value", "say", "sources"):
        if not f.get(key):
            P("data", "_data/facts.yml", f"{where} has no `{key}`")
    if f.get("perspective") in _f_seen:
        P("data", "_data/facts.yml", f"duplicate perspective '{f['perspective']}'")
    _f_seen.add(f.get("perspective"))
    for s in f.get("sources") or []:
        if not s.get("label"):
            P("data", "_data/facts.yml", f"{where} has a source with no `label`")
        slug = s.get("publication")
        if not slug:
            P("data", "_data/facts.yml", f"{where} has a source with no `publication`")
        elif slug not in coll["publications"]:
            P("xref", "_data/facts.yml",
              f"{where} cites '{slug}', which has no file in _publications/")

tst = yaml.safe_load((SITE / "_data/testimonials.yml").read_text()) or []
seen_ids = set()
for t in tst:
    if not t.get("id"):
        P("data", "_data/testimonials.yml", f"entry for {t.get('name')} has no `id`")
    elif t["id"] in seen_ids:
        P("data", "_data/testimonials.yml", f"duplicate id '{t['id']}'")
    else:
        seen_ids.add(t["id"])

# index.md picks testimonials by id
idx = (SITE / "index.md").read_text()
m = re.search(r'testimonials\.html only="([^"]+)"', idx)
if m:
    for k in m.group(1).split(","):
        if k.strip() not in seen_ids:
            P("data", "index.md", f"testimonial id '{k.strip()}' does not exist")

# home page partner tiles
m = re.search(r'assign shown = "([^"]+)" \| split', idx)
if m:
    for k in m.group(1).split(","):
        if k.strip() not in coll["partners"]:
            P("xref", "index.md", f"partner tile '{k.strip()}' has no file in _partners/")

# partner files need a slug field, since templates filter on it
for slug, (fm, body, f) in coll["partners"].items():
    if fm.get("slug") and fm["slug"] != slug:
        P("data", f"_partners/{slug}.md", f"`slug` says '{fm['slug']}' but the filename says '{slug}'")

# --------------------------------------------------- every page has a layout
# A collection document with no layout is rendered by Jekyll as raw text: no
# stylesheet, no navigation, no header. It looks fine locally and broken live.
rules = {(r.get("scope") or {}).get("type"): (r.get("values") or {}).get("layout")
         for r in (cfg.get("defaults") or [])}
for cname, items in coll.items():
    for slug, (fm, body, f) in items.items():
        if not fm.get("layout") and not rules.get(cname):
            P("layout", f"_{cname}/{slug}.md",
              "no layout, and _config.yml has no defaults rule for "
              f"`{cname}` - Jekyll will render this as unstyled raw text")
            break
for slug, (fm, body, f) in posts.items():
    if not fm.get("layout") and not rules.get("posts"):
        P("layout", f"_posts/{slug}.md", "no layout and no defaults rule for posts")
        break
for cname in coll:
    lay = rules.get(cname)
    if lay and not (SITE / "_layouts" / f"{lay}.html").exists():
        P("layout", "_config.yml", f"`{cname}` defaults to layout `{lay}`, which does not exist")

# ----------------------------------------- front matter that Jekyll shadows
# Jekyll gives every document its own url, path, id, collection, date,
# excerpt, content and output. A front matter key of the same name is
# silently ignored, which is how every partner page came to link to itself.
SHADOWED = {"url", "path", "id", "collection", "excerpt", "content", "output", "next", "previous"}
for cname, items in coll.items():
    for slug, (fm, body, f) in items.items():
        for key in fm:
            if key in SHADOWED:
                P("shadowed", f"_{cname}/{slug}.md",
                  f"`{key}` is a built-in Jekyll field and will be ignored - rename it")

# ------------------------------------------------------------------- assets
asset_re = re.compile(r'(?:^|[\s"\'(:])(/assets/[A-Za-z0-9._/\-]+)')
all_text = []
for p in [f for f in SITE.glob("*.md") if f.name != "README.md"] + list(SITE.glob("_data/*.yml")) + \
         list(SITE.glob("_includes/*.html")) + list(SITE.glob("_layouts/*.html")) + \
         [f for c in coll.values() for (_, _, f) in c.values()] + \
         [f for (_, _, f) in posts.values()]:
    all_text.append((p, p.read_text()))

referenced = set()
def strip_comments(t):
    """A commented-out asset path is not a reference."""
    out = []
    for line in t.splitlines():
        ls = line.lstrip()
        if ls.startswith("#") or ls.startswith("<!--"):
            continue
        out.append(line)
    return "\n".join(out)

for p, t in all_text:
    for m in asset_re.finditer(strip_comments(t)):
        path = m.group(1)
        referenced.add(path)
        f = SITE / path.lstrip("/")
        if not f.exists():
            P("asset", str(p.relative_to(SITE)), f"missing file {path}")

# logo filenames are assembled in the template, not written out in full
for slug, (fm, body, f) in coll["partners"].items():
    logo = fm.get("logo")
    if not logo:
        N("partners", f"{slug} has no logo")

# Every project, publication and post should carry at least one image: a
# figure from the work for a project or paper, a photograph for an event.
# This is a note rather than an error - a page without one still builds, it
# just reads as a wall of text, which is what this is here to prevent.
def _has_picture(fm, body):
    if fm.get("hero") or (fm.get("figures") or []):
        return True
    # a figure written straight into the body counts too
    return "<figure" in body or "![" in body

# Themes are a closed vocabulary. An unknown slug is an error, not a note:
# it silently drops the item out of every filter, which is exactly how the
# fifteen single-use tags this replaced became useless.
_theme_slugs = {t["slug"] for t in (yaml.safe_load((SITE / "_data/themes.yml").read_text()) or [])}
_theme_use = {s: 0 for s in _theme_slugs}
for kind in ("projects", "publications"):
    for slug, (fm, body, f) in coll.get(kind, {}).items():
        for t in (fm.get("themes") or []):
            if t not in _theme_slugs:
                P("themes", f"_{kind}/{slug}.md",
                  f"theme '{t}' is not in _data/themes.yml")
            else:
                _theme_use[t] += 1
_unused = [s for s, n in _theme_use.items() if n == 0]
if _unused:
    N("themes", f"declared but never used: {', '.join(sorted(_unused))}")
_thin = [f"{s} ({n})" for s, n in sorted(_theme_use.items()) if 0 < n < 3]
if _thin:
    N("themes", "used fewer than three times - a label rather than a theme: "
                + ", ".join(_thin))

# Reported as one line per kind rather than one per page: sixty separate
# notes would bury everything else, and the useful number here is the gap.
_want_pics = {
    "projects":     ("project", "a figure from the work - intervention logic, key results"),
    "publications": ("publication", "a selection of figures from the paper"),
    "posts":        ("post", "a figure from the project or paper, or a photograph for an event"),
}
for kind, (singular, wanted) in _want_pics.items():
    if kind == "posts":
        items = {p.stem: split_fm(p) for p in sorted((SITE / "_posts").glob("*.md"))}
        bare = [s for s, (fm, body) in items.items() if not _has_picture(fm or {}, body)]
        total = len(items)
    else:
        items = coll.get(kind, {})
        bare = [s for s, (fm, body, f) in items.items() if not _has_picture(fm, body)]
        total = len(items)
    if bare:
        shown = ", ".join(sorted(bare)[:6])
        more = f", +{len(bare) - 6} more" if len(bare) > 6 else ""
        N("figures", f"{len(bare)} of {total} {kind} have no image - wanted: "
                     f"{wanted}\n      {shown}{more}")
        continue
    path = "/assets/img/partners/" + logo
    referenced.add(path)
    if not (SITE / path.lstrip("/")).exists():
        P("asset", f"_partners/{slug}.md", f"logo file missing: {path}")

for slug, (fm, body, f) in coll["people"].items():
    por = fm.get("portrait")
    if por:
        referenced.add(por)
        if not (SITE / por.lstrip("/")).exists():
            P("asset", f"_people/{slug}.md", f"portrait missing: {por}")

# unused images (informational only)
on_disk = {("/" + str(f.relative_to(SITE))) for f in (SITE / "assets").rglob("*")
           if f.is_file() and f.suffix.lower() in
           (".jpg", ".jpeg", ".png", ".svg", ".webp", ".gif", ".pdf")}
for f in sorted(on_disk - referenced):
    N("assets", f"not referenced anywhere: {f}")

# ------------------------------------------------------------- internal links
pages = {"/"}
hidden_pages = set()
# Both extensions: Jekyll builds a top-level page from either, and the pages
# that are pure layout deliberately live in .html so kramdown never sees them.
for p in sorted(list(SITE.glob("*.md")) + list(SITE.glob("*.html"))):
    fm, _ = split_fm(p)
    if not fm or not fm.get("permalink"):
        continue
    if fm.get("published") is False:
        hidden_pages.add(fm["permalink"])   # exists, deliberately not built
    else:
        pages.add(fm["permalink"])
for slug in coll["projects"]:
    pages.add(f"/projects/{slug}/")
for slug in coll["people"]:
    pages.add(f"/team/{slug}/")
for slug in coll["publications"]:
    pages.add(f"/publications/{slug}/")
for slug in coll["partners"]:
    pages.add(f"/partners/{slug}/")

# posts, whose permalink is /news/:year/:title/ - the filename carries both
for slug in posts:
    m = re.match(r"(\d{4})-\d{2}-\d{2}-(.+)", slug)
    if m:
        pages.add(f"/news/{m.group(1)}/{m.group(2)}/")

link_re = re.compile(r"""['"](/[A-Za-z0-9._/\-]*)['"]\s*\|\s*relative_url""")
for p, t in all_text:
    for m in link_re.finditer(t):
        target = m.group(1)
        if target.startswith("/assets/"):
            continue
        if target in hidden_pages:
            N("links", f"{p.relative_to(SITE)} links to {target}, a page that is "
                       "currently unpublished - fine if the link is behind a flag")
        elif target not in pages:
            P("link", str(p.relative_to(SITE)), f"links to {target}, which no page produces")

# nav entries. An entry is either a link (`url`) or a group (`items`); a
# group's children are links. Both shapes are checked, and a group with no
# children is flagged, because the header silently skips it.
def _check_nav(entry, parent=None):
    where = f"nav item '{entry.get('title', '?')}'"
    if parent:
        where = f"nav item '{parent}' > '{entry.get('title', '?')}'"
    if "items" in entry:
        kids = entry.get("items") or []
        if not kids:
            N("config", f"nav group '{entry.get('title','?')}' has no visible items "
                        "and is skipped by the header - fine if its pages are hidden")
        for kid in kids:
            _check_nav(kid, entry.get("title"))
    elif "url" in entry:
        if entry["url"] not in pages:
            P("config", "_config.yml", f"{where} points at {entry['url']}, no such page")
    else:
        P("config", "_config.yml", f"{where} has neither a url nor items")

for item in cfg.get("nav", []):
    _check_nav(item)

# ------------------------------------------------------------- jekyll/config
if "{%- seo" in (SITE / "_layouts/default.html").read_text() or "{% seo" in (SITE / "_layouts/default.html").read_text():
    if "jekyll-seo-tag" not in (cfg.get("plugins") or []):
        P("config", "_config.yml", "layout uses {% seo %} but jekyll-seo-tag is not in `plugins`")

for coll_name in ("projects", "people", "publications", "partners"):
    c = (cfg.get("collections") or {}).get(coll_name)
    if not c:
        P("config", "_config.yml", f"collection `{coll_name}` is not declared")
    elif not c.get("output"):
        P("config", "_config.yml", f"collection `{coll_name}` has output: false, pages will not be built")

for f in ("CNAME", ".gitignore", "404.html", "README.md", "Gemfile"):
    if not (SITE / f).exists():
        N("repo", f"no {f}")

# --------------------------------------------------------------------- people
# `works_on` is a closed vocabulary, the same theme slugs projects use. A typo
# would simply render the raw slug as a chip, which looks like a label nobody
# chose. `tagline` is capped because it has to fit on a card.
# _theme_slugs is already built further up, where project themes are checked.
for _slug, (_fm, _body, _f) in coll["people"].items():
    for _w in (_fm.get("works_on") or []):
        if _w not in _theme_slugs:
            P("people", f"_people/{_slug}.md",
              f"`works_on` names {_w}, which is not a theme in _data/themes.yml")
    # This cap has been raised twice, which is the sign that a character count
    # was never the thing worth checking. What matters is how it wraps, and
    # that is visual. So: a note once it is long enough to be worth a second
    # look on a card, and a failure only once it has clearly stopped being a
    # tagline and become a paragraph.
    _tag = _fm.get("tagline")
    if _tag and len(_tag) > 220:
        P("people", f"_people/{_slug}.md",
          f"`tagline` is {len(_tag)} characters. That is a paragraph; the body "
          "text is the place for it.")
    elif _tag and len(_tag) > 140:
        N(f"_people/{_slug}.md",
          f"`tagline` is {len(_tag)} characters, so it runs to several lines on "
          "a card. Fine on the profile; look at the team page before shipping it.")

    # `affil` is the one-line affiliation a team card shows, in acronyms:
    # "GBDI, EPFL" where `org` has "Global Building Data Initiative, EPFL".
    # Spelt out, it wraps and the whole grid grows to the height of the
    # longest one, which is the thing the short field exists to avoid. The
    # card falls back to `org` where `affil` is absent, so a missing one is a
    # note rather than a failure.
    # `rise_since` decides which of a person's publications the "With RISE or
    # GBDI" filter counts. A wrong year quietly moves work from one side of
    # that line to the other, and nothing on the page looks wrong, so the
    # value is checked for being a plausible year rather than a string, a
    # date, or a typo with a digit too many.
    _rs = _fm.get("rise_since")
    if _rs is not None:
        if not isinstance(_rs, int) or _rs < 1990 or _rs > 2100:
            P("people", f"_people/{_slug}.md",
              f"`rise_since` is {_rs!r}. It should be a bare year, like 2024: "
              "it is compared against each publication's `year`.")

    # An ORCID is an identifier, not a link: a wrong digit still resolves, to
    # somebody else's research record. The checksum is cheap to verify, so it
    # is, rather than trusting a number typed from an email.
    for _l in (_fm.get("links") or []):
        if _l.get("title") != "ORCID":
            continue
        _m = re.match(r"^https://orcid\.org/(\d{4})-(\d{4})-(\d{4})-(\d{3}[\dX])$",
                      (_l.get("url") or "").strip())
        if not _m:
            P("people", f"_people/{_slug}.md",
              f"ORCID link is `{_l.get('url')}`. It should read "
              "https://orcid.org/0000-0000-0000-0000, with the final "
              "character a digit or X.")
            continue
        _digits = "".join(_m.groups())
        _total = 0
        for _c in _digits[:15]:
            _total = (_total + int(_c)) * 2
        _check = (12 - _total % 11) % 11
        _expect = "X" if _check == 10 else str(_check)
        if _digits[15] != _expect:
            P("people", f"_people/{_slug}.md",
              f"ORCID {_l['url']} fails its own checksum: the last character "
              f"should be {_expect}. One digit is wrong somewhere, and a wrong "
              "ORCID points at a real stranger's publication record.")

    _af = _fm.get("affil")
    if _af and len(_af) > 40:
        P("people", f"_people/{_slug}.md",
          f"`affil` is {len(_af)} characters, which wraps on a team card. It is "
          "the short form, in acronyms; `org` is where the names are spelt out.")
    elif not _af and _fm.get("org"):
        N(f"_people/{_slug}.md",
          "no `affil`, so the team card falls back to the full `org`. Add the "
          "acronym form if that wraps.")

# `rise_tier` is derived, not decided. A publication is `core` when someone
# with `group: rise` is on it from their `rise_since` year, `extended` when
# that person is a collaborator instead, and `prior` when nobody on it was
# with RISE yet. It lives in the file because the list sorts on it and a
# template cannot sort on something it computes while rendering - which means
# it can drift the moment a `rise_since` or a `group` changes, or a person is
# added to a paper. So it is recomputed here and compared, every run.
#
# A tier outside the three is failed as well as a missing one: publist.html
# builds each year by selecting the three in turn, so a fourth value would
# drop the entry to the end of its year, which is a silent demotion rather
# than a visible error.
_TIERS = ("core", "extended", "prior")
_who = {s: (fm.get("rise_since"), fm.get("group"))
        for s, (fm, _b, _f) in coll["people"].items()}
for _slug, (_pb, _body, _f) in coll["publications"].items():
    _found = set()
    for _s in (_pb.get("people") or []):
        _y, _g = _who.get(_s, (None, None))
        if _y and (_pb.get("year") or 0) >= _y:
            _found.add("core" if _g == "rise" else "extended")
    _want = next((_t for _t in _TIERS if _t in _found), "prior")
    _have = _pb.get("rise_tier")
    if _have is None:
        P("publications", f"_publications/{_slug}.md",
          "no `rise_tier`. Run `python3 make-rise-flags.py` to write it.")
    elif _have not in _TIERS:
        P("publications", f"_publications/{_slug}.md",
          f"`rise_tier` is {_have!r}, which is not one of "
          f"{', '.join(_TIERS)}. Run `python3 make-rise-flags.py`.")
    elif _have != _want:
        P("publications", f"_publications/{_slug}.md",
          f"`rise_tier` says {_have}, but the people on it, their "
          f"`rise_since` years and their `group` say {_want}. "
          f"Run `python3 make-rise-flags.py`.")
    if "rise_work" in _pb:
        P("publications", f"_publications/{_slug}.md",
          "still carries `rise_work`, which `rise_tier` replaced on 31 Oct "
          "2026. Run `python3 make-rise-flags.py` to drop it.")

# `rise` at the head of a project's `partners`. RISE belongs in the list of
# organisations on its own project pages (Martin, 31 Oct 2026) - leaving it
# out read as though the work had nobody behind it - but only where RISE
# existed to do the work. Two projects ran entirely before it was founded and
# must not claim it. The rule is the one `rise_tier` uses on publications:
# the project runs to a core person's `rise_since` year or later.
#
# `rise` is not a file in _partners/; _includes/partners.html writes that tile
# itself and points it at the home page, so the unknown-key check below has to
# skip it as well.
_rise_people = {s for s, (fm, _b, _f) in coll["people"].items()
                if fm.get("group") == "rise" and fm.get("rise_since")}
for _slug, (_pr, _body, _f) in coll["projects"].items():
    _years = re.findall(r"\d{4}", str(_pr.get("years") or ""))
    _end = int(_years[-1]) if _years else 0
    _want = any(
        _s in _rise_people
        and _end >= coll["people"][_s][0]["rise_since"]
        for _s in (_pr.get("people") or [])
    )
    _parts = _pr.get("partners") or []
    _has = "rise" in _parts
    # `partners_omitted: true` is the deliberate exemption: a project whose
    # consortium is too large for any honest short list shows no tiles at all,
    # RISE included, and says so in `partners_note` instead. IEA EBC Annex 72
    # is the one case (27 countries).
    if _pr.get("partners_omitted"):
        if _parts:
            P("projects", f"_projects/{_slug}.md",
              "sets `partners_omitted` but still lists partners. It means no "
              "tiles at all; drop the list or drop the flag.")
        elif not _pr.get("partners_note"):
            P("projects", f"_projects/{_slug}.md",
              "sets `partners_omitted` with no `partners_note`. The page then "
              "says nothing at all about who else was on it. Say why the "
              "names are missing.")
    elif _want and not _has:
        P("projects", f"_projects/{_slug}.md",
          f"ran to {_end or 'an unreadable year'} with a RISE person on it, "
          "but `partners` does not open with `rise`. The project pages list "
          "RISE among the organisations from 31 Oct 2026.")
    elif _has and not _want:
        P("projects", f"_projects/{_slug}.md",
          f"lists `rise` in `partners`, but it ran to {_end or 'an unreadable year'} "
          "and no core RISE person was with RISE by then. Saying RISE did "
          "work it predates is the one error this rule exists to catch.")
    elif _has and _parts[0] != "rise":
        P("projects", f"_projects/{_slug}.md",
          "lists `rise` in `partners` but not first. The tile block reads as "
          "the organisations behind the project, and RISE leads it.")

# Publication thumbnails. Every entry should have one: the list draws a tile
# from front matter where a file is missing, so nothing looks broken, but a
# designed tile or a title page says more than a year and a kind label.
# A credit is required wherever the image is not RISE's own; that cannot be
# told from the front matter, so what is checked is that a credit, where
# given, is not empty.
for _slug, (_pb, _body, _f) in coll["publications"].items():
    _th = _pb.get("thumbnail")
    if not _th:
        N(f"_publications/{_slug}.md",
          "no `thumbnail`, so the list draws a tile from the front matter. "
          "A title page or a designed tile says more.")
    elif not (SITE / _th.lstrip("/")).exists():
        P("asset", f"_publications/{_slug}.md", f"thumbnail missing: {_th}")
    if "thumbnail_credit" in _pb and not (_pb.get("thumbnail_credit") or "").strip():
        P("publications", f"_publications/{_slug}.md",
          "`thumbnail_credit` is empty. Either name whose image it is, or "
          "remove the line.")

# ---------------------------------------------------------------- testimonials
# `short` is what the homepage shows where a full quote will not fit. It must
# be a verbatim substring of `quote`, never a paraphrase: a shortened quote
# that says something the person did not write is the one failure mode here
# that matters, and it is invisible once published. Whitespace is collapsed
# before comparing, because YAML folding rewraps both.
_tst = yaml.safe_load((SITE / "_data/testimonials.yml").read_text()) or []
for _e in _tst:
    _id = _e.get("id", "?")
    if not _e.get("short"):
        N("_data/testimonials.yml", f"{_id} has no `short`; the full quote is used everywhere")
        continue
    _s = re.sub(r"\s+", " ", _e["short"]).strip()
    _q = re.sub(r"\s+", " ", _e.get("quote", "")).strip()
    if _s not in _q:
        P("testimonial", "_data/testimonials.yml",
          f"{_id}: `short` is not a verbatim substring of `quote`. A shortened "
          "quote must never say something the person did not write.")

# -------------------------------------------------------------------- openings
# A job advertisement in Austria must state the minimum pay for the position
# with a time unit, so a published opening missing pay_min or pay_unit is a
# legal problem, not a cosmetic one. The rest of the fields are what the
# facts box at the top of the post renders. The template itself is
# published: false and so is not checked.
OPENING_FIELDS = ("deadline", "start", "duration", "hours",
                  "location", "pay_min", "pay_unit", "apply")
for _slug, (_fm, _body, _f) in posts.items():
    if _fm.get("type") != "opening":
        continue
    if _fm.get("published") is False:
        continue
    missing = [k for k in OPENING_FIELDS if not _fm.get(k)]
    if missing:
        P("opening", f"_posts/{_slug}.md",
          "published opening is missing " + ", ".join(f"`{k}`" for k in missing)
          + ". Austrian law requires the minimum pay and its time unit to be "
            "stated in a job advertisement; the other fields fill the facts box.")
    if _fm.get("pay_unit") and _fm["pay_unit"] not in ("month", "week", "hour"):
        P("opening", f"_posts/{_slug}.md",
          f"`pay_unit` is {_fm['pay_unit']}; it must be month, week or hour")
    if "x,xxx" in str(_fm.get("pay_min", "")):
        P("opening", f"_posts/{_slug}.md",
          "`pay_min` is still the placeholder from the template (H15)")

# ------------------------------------------------------------- social preview
# jekyll-seo-tag reads `image`, not `hero`. A page that sets a hero without an
# image still shares correctly, but with the generic site card instead of its
# own picture, which is almost never what was wanted. P1.4 chose the explicit
# second field over hand-writing meta tags, so this is the rule that keeps the
# two in step.
for _name in ("projects", "people", "publications", "partners"):
    for _slug, (_fm, _body, _f) in coll[_name].items():
        if _fm.get("hero") and not _fm.get("image"):
            N(f"_{_name}/{_slug}.md",
              "has `hero` but no `image`, so a shared link shows the generic "
              "RISE card rather than this page's own picture. Add "
              "`image:` with the same path.")
for _slug, (_fm, _body, _f) in posts.items():
    if _fm.get("hero") and not _fm.get("image"):
        N(f"_posts/{_slug}.md",
          "has `hero` but no `image`; a shared link shows the generic card")

_social = cfg.get("image")
if not _social:
    P("config", "_config.yml", "no site-wide `image`, so shared links have no picture")
elif not (SITE / _social.lstrip("/")).exists():
    P("config", "_config.yml", f"`image` points at {_social}, which does not exist")

# ----------------------------------------------------------------- placeholder
# R11: one placeholder for anything without a picture of its own, resolved by
# _includes/stockimg.html. It is one file, so this is one check - but a hard
# one, because every project card, project page and expertise field without an
# image falls through to it, and a missing file would break all of them at
# once rather than one page quietly.
_ph = "assets/img/placeholders/placeholder-project.webp"
if not (SITE / _ph).exists():
    P("placeholder", _ph,
      "missing. Every project, post or event without a `hero` falls back to "
      "this one file, so it cannot be absent.")

# _data/stock.yml held the eight texture photographs the fallback used to pick
# from by slug length. Nothing reads it since R11. The file is left in place in
# case the textures are wanted elsewhere, and said so here rather than being
# deleted quietly.
_stock_file = SITE / "_data/stock.yml"
if _stock_file.exists():
    _used = any("data.stock" in p.read_text()
                for p in SITE.glob("_includes/*.html"))
    if not _used:
        N("_data/stock.yml",
          "nothing reads this any more: the picture fallback is one "
          f"placeholder ({_ph}) since R11. Keep it only if the textures are "
          "wanted somewhere else.")

# ------------------------------------------------------------ related projects
# `related` names other projects by slug. A typo would simply render nothing,
# so it is checked here. Self-references are flagged too: the layout drops
# them, but they are always a mistake.
for slug, (pr, _body, _f) in coll["projects"].items():
    for other in (pr.get("related") or []):
        if other == slug:
            P("related", f"_projects/{slug}.md", "lists itself in `related`")
        elif other not in coll["projects"]:
            P("related", f"_projects/{slug}.md",
              f"`related` names {other}, which is not a project")

    # `short_title` is the link text wherever a project is named inside a
    # sentence: the engagement cards today, and anywhere else that needs a
    # name rather than a headline. The real titles run to a line and a half
    # ("Supporting the Development of a Roadmap for the Reduction of Whole
    # Life Carbon..."), which swamps a card. The cap is what fits on one line
    # of a card at the smallest column width; above it the point is lost.
    #
    # Raised from 34 to 38 on 30 October: the work order supplies "European
    # embodied carbon benchmarks", 35 characters, so 34 turned out to be a
    # number picked by eye rather than a limit anything actually hits. 38
    # still rejects a full project title, which is what the field exists to
    # prevent.

    # A project is not a citable work. Most of these were done with partners,
    # and a citation line on a project page invites someone to cite RISE for
    # work RISE contributed to rather than authored. Citations belong to
    # publications, which have authors, a venue and a DOI. These fields used
    # to render a "Cite as" row; the row is gone, so a file carrying them
    # again means someone is expecting one.
    for _k in [k for k in pr if k.startswith("cite_")]:
        P("projects", f"_projects/{slug}.md",
          f"`{_k}` is a citation field, and project pages do not carry a "
          "citation. If this project produced something citable, give it a "
          "file in _publications/ and cite it there.")

    _st = pr.get("short_title")
    if _st is None:
        N(f"_projects/{slug}.md",
          "no `short_title`, so anything naming this project inside a "
          "sentence falls back to the full title")
    elif len(_st) > 38:
        P("projects", f"_projects/{slug}.md",
          f"`short_title` is {len(_st)} characters, which is no longer short: "
          "it wraps in an engagement card. Keep it to a name.")

# -------------------------------------------------------- markdown vs. html
#
# Two bugs that reached the live site, and the rules that catch them.
#
# 1. kramdown only treats an HTML tag as a block-level element when it starts
#    at the beginning of the line. `<div markdown="1">` indented inside a
#    parent div is not recognised, so neither the markdown inside it nor the
#    tags themselves are processed, and the raw <div> and <li> end up visible
#    as text. That is exactly what happened to /expertise/. Every other
#    markdown="1" block on the site sits at column 0 and renders correctly.
#
# 2. A page that is pure layout - all HTML and Liquid, no markdown prose - has
#    nothing to gain from being a .md file and everything to lose, because it
#    is still run through kramdown. Such pages belong in .html, where Liquid
#    still runs but markdown does not.
for f in sorted(SITE.rglob("*.md")):
    rel = f.relative_to(SITE)
    if rel.parts[0] in ("_preview", "docs", "_site") or rel.name == "README.md":
        continue
    fm, body = split_fm(f)
    if fm is None:
        continue

    for i, line in enumerate(body.split("\n"), 1):
        if 'markdown="1"' in line and line[:1].isspace():
            P("markdown", str(rel),
              f"line {i}: <div markdown=\"1\"> is indented. kramdown only parses "
              "block HTML that starts at column 0, so this block and its tags "
              "will render as visible text. Move it to column 0, or write the "
              "content as HTML and drop the markdown=\"1\".")

    # Pure-layout page living as markdown.
    stripped = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    stripped = re.sub(r"\{%.*?%\}", "", stripped, flags=re.S)
    prose = re.findall(r"^(?:#{1,6} |[-*] |\d+\. |> )", stripped, re.M)
    has_html = re.search(r"^\s*<(div|section|main|ul|table|figure)\b", stripped, re.M)
    if has_html and not prose and rel.parent == pathlib.Path("."):
        N(str(rel), "is all HTML and Liquid with no markdown prose. It would be "
                    "safer as .html, where Liquid still runs but kramdown cannot "
                    "mangle the markup. (Keep the permalink when renaming.)")

# ------------------------------------------------------ compound `where_exp`
# GitHub Pages runs Jekyll 3.10 on Liquid 4.0.4, whose `where_exp` takes one
# comparison and nothing more. Joining two with `and` raises
#
#   Liquid syntax error: Expected end_of_string but found id
#
# which is a parse error, so the whole site fails to build and the last good
# version stays live. That happened on 31 Oct 2026 and went unnoticed for six
# hours, because a failed Pages build is silent unless someone looks: the site
# does not break, it simply stops changing, and every merge after it looked
# fine and shipped nothing.
#
# Write it as chained filters instead, which is the same thing and parses:
#   | where_exp: "x", "x.a != 'one'" | where_exp: "x", "x.a != 'two'"
#
# This check exists because the local renderer is python-liquid, which accepts
# the compound form happily. Anything the two engines disagree about has to be
# caught here or it is caught by the deploy.
_WHERE_EXP = re.compile(r"where_exp\s*:\s*(\"[^\"]*\"|'[^']*')\s*,\s*(\"[^\"]*\"|'[^']*')")
for _f in sorted(SITE.glob("**/*.html")) + sorted(SITE.glob("*.md")):
    if any(p in _f.parts for p in ("_site", "docs", ".git")):
        continue
    for _m in _WHERE_EXP.finditer(_f.read_text()):
        _exp = _m.group(2)[1:-1]
        if re.search(r"\b(and|or)\b", _exp):
            P("liquid", str(_f.relative_to(SITE)),
              f"`where_exp` joins comparisons with and/or: {_exp}. Liquid 4 "
              "cannot parse that and the whole Pages build fails. Chain one "
              "`where_exp` per comparison instead.")

# --------------------------------------------------- duplicated stylesheet runs
# Two whole blocks of style.css have been pasted in twice now: the picture
# treatment on 31 Oct, and the expertise block the same day, 98 lines of it.
# A duplicate is invisible when the copies agree - the second simply wins - and
# becomes a bug the moment someone edits one of them, because the other goes on
# overriding it from further down the file and the edit appears to do nothing.
#
# Eight identical lines is well past coincidence: the longest honest repeat in
# this file is a four-line media query. Overlapping windows are collapsed to
# one report so a 98-line duplicate is one problem rather than ninety.
_css = SITE / "assets/css/style.css"
if _css.exists():
    _lines = _css.read_text().splitlines()
    _RUN = 8
    _first, _dupes = {}, []
    for _i in range(len(_lines) - _RUN):
        _win = tuple(l.strip() for l in _lines[_i:_i + _RUN])
        if sum(1 for _w in _win if _w) < _RUN - 1:
            continue                      # mostly blank, not a real block
        if _win in _first:
            if _dupes and _i == _dupes[-1][1] + 1:
                _dupes[-1] = (_dupes[-1][0], _i)      # same run, extend it
            else:
                _dupes.append((_first[_win], _i))
        else:
            _first[_win] = _i
    for _a, _b in _dupes:
        P("css", "assets/css/style.css",
          f"the block starting at line {_a + 1} is repeated at line {_b + 1}. "
          "Delete the second copy: while they agree it is dead weight, and "
          "once they differ the later one silently wins.")

# ---------------------------------------------------------------- report
print()
if problems:
    print(f"{len(problems)} PROBLEM(S)")
    for kind, where, msg in problems:
        print(f"  [{kind}] {where}: {msg}")
else:
    print("no problems found")

if notes:
    print(f"\n{len(notes)} note(s)")
    for where, msg in notes:
        print(f"  [{where}] {msg}")

sys.exit(1 if problems else 0)
