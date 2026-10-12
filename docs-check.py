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
svc = yaml.safe_load((SITE / "_data/services.yml").read_text()) or []
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
              f"`{cname}` — Jekyll will render this as unstyled raw text")
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
                  f"`{key}` is a built-in Jekyll field and will be ignored — rename it")

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
for p in SITE.glob("*.md"):
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

# posts, whose permalink is /news/:year/:title/ — the filename carries both
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
                       "currently unpublished — fine if the link is behind a flag")
        elif target not in pages:
            P("link", str(p.relative_to(SITE)), f"links to {target}, which no page produces")

# nav entries
for item in cfg.get("nav", []):
    if item["url"] not in pages:
        P("config", "_config.yml", f"nav item '{item['title']}' points at {item['url']}, no such page")

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
