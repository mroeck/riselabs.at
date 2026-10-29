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
for name in ("projects", "people", "publications", "partners"):
    coll[name] = {}
    for f in sorted((SITE / f"_{name}").glob("*.md")):
        fm, body = split_fm(f)
        if fm is None:
            continue
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
            if v not in coll[target]:
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
    ex = s.get("example")
    if ex and ex not in coll["projects"]:
        P("xref", "_data/services.yml", f"example '{ex}' has no file in _projects/")

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

# ---------------------------------------------------------------- stock images
stock = (yaml.safe_load((SITE / "_data/stock.yml").read_text()) or [])
if not stock:
    P("stock", "_data/stock.yml", "no stock images listed; the fallback has nothing to pick")
for i, s in enumerate(stock):
    if not s.get("file"):
        P("stock", "_data/stock.yml", f"entry {i} has no `file`")
        continue
    if not (SITE / s["file"].lstrip("/")).exists():
        P("stock", "_data/stock.yml", f"missing file {s['file']}")
    if not s.get("alt"):
        N("_data/stock.yml", f"{s['file']} has no `alt`")

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
