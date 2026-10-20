#!/usr/bin/env python3
"""Download partner logos, normalise them, and wire them into the front matter.

Seventeen partners have no logo. They cannot be fetched from the session this
script was written in — its network allowlist reaches package registries and
GitHub and nothing else — so this exists to make the job one command once you
have the URLs.

Fill in `logo-sources.txt` (one `slug <space> url` per line, `#` for
comments), then:

    python3 add-logos.py            # check the list, download nothing
    python3 add-logos.py --write    # download, convert, save, set `logo:`

Needs Pillow:  pip install --break-system-packages pillow

What it does to each file, and why — these are all mistakes this site has
already made once:

  * converts CMYK to RGB. A CMYK JPEG renders with inverted-looking colour in
    most browsers; the BPIE logo arrived that way.
  * trims surrounding transparency or uniform background, but only if the
    trim looks sane. An aggressive auto-trim once cut a 640x250 wordmark down
    to 128x131 by latching onto an internal element.
  * caps the long edge at 600px and keeps the aspect ratio. Tiles are small;
    a 4000px logo is just bytes.
  * saves PNG with transparency preserved, because the tiles are white in
    both themes and a baked-in white box shows its edges.

Prefer an SVG or a large transparent PNG from the organisation's own press or
brand page. A screenshot of a logo is not a logo.
"""

import argparse
import pathlib
import re
import sys
import urllib.error
import urllib.request

SITE = pathlib.Path(__file__).parent
PARTNERS = SITE / "_partners"
LOGOS = SITE / "assets/img/partners"
LIST = SITE / "logo-sources.txt"
MAXEDGE = 600
UA = "riselabs.at logo fetcher (martin.roeck@riselabs.at)"


def read_list():
    if not LIST.exists():
        sys.exit(f"no {LIST.name} — create it with lines of: slug  https://…/logo.png")
    out = []
    for n, raw in enumerate(LIST.read_text().splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2:
            print(f"  !! line {n}: expected 'slug url', got {raw.strip()!r}")
            continue
        out.append((parts[0], parts[1]))
    return out


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get("Content-Type", "")


def normalise(raw, slug):
    """Return PNG bytes, or None with a reason printed."""
    from io import BytesIO
    from PIL import Image, ImageChops

    try:
        im = Image.open(BytesIO(raw))
        im.load()
    except Exception as e:                       # noqa: BLE001 - report, don't crash
        print(f"  !! {slug}: not an image Pillow can read ({e}). "
              f"If it is an SVG, convert it by hand or export a PNG.")
        return None

    if im.mode == "CMYK":
        im = im.convert("RGB")
    if im.mode not in ("RGBA", "RGB"):
        im = im.convert("RGBA")

    before = im.size

    # trim, but only accept the result if it still looks like the same artwork
    if im.mode == "RGBA":
        bbox = im.getchannel("A").getbbox()
    else:
        bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
        bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if w >= before[0] * 0.25 and h >= before[1] * 0.25:
            im = im.crop(bbox)
        else:
            print(f"  .. {slug}: trim would cut {before} to ({w}, {h}) — skipped, "
                  f"that is the over-trim this script exists to avoid")

    if max(im.size) > MAXEDGE:
        scale = MAXEDGE / max(im.size)
        im = im.resize((max(1, round(im.width * scale)),
                        max(1, round(im.height * scale))), Image.LANCZOS)

    buf = BytesIO()
    im.save(buf, "PNG", optimize=True)
    print(f"  ok {slug}: {before[0]}x{before[1]} -> {im.width}x{im.height}, "
          f"{len(buf.getvalue()) // 1024} KB")
    return buf.getvalue()


def set_front_matter(slug, filename):
    f = PARTNERS / f"{slug}.md"
    text = f.read_text()
    if re.search(r"^logo:", text, re.M):
        return "already set"
    # replace the commented placeholder if there is one, else add after website
    new, n = re.subn(r'^#\s*logo:.*$', f'logo: "{filename}"', text, count=1, flags=re.M)
    if not n:
        new, n = re.subn(r'^(website:.*)$', rf'\1\nlogo: "{filename}"',
                         text, count=1, flags=re.M)
    if not n:
        new, n = re.subn(r'^(name:.*)$', rf'\1\nlogo: "{filename}"',
                         text, count=1, flags=re.M)
    if not n:
        return "could not find a place to put it"
    f.write_text(new)
    return "set"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="actually download and save")
    args = ap.parse_args()

    pairs = read_list()
    if not pairs:
        sys.exit("nothing to do — logo-sources.txt has no slug/url lines")

    missing = [s for s, _ in pairs if not (PARTNERS / f"{s}.md").exists()]
    if missing:
        sys.exit(f"no partner file for: {', '.join(missing)}")

    if not args.write:
        print(f"{len(pairs)} logo(s) listed. Re-run with --write to fetch them.")
        for s, u in pairs:
            print(f"  {s:26} {u}")
        return

    LOGOS.mkdir(parents=True, exist_ok=True)
    done = 0
    for slug, url in pairs:
        try:
            raw, ctype = fetch(url)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"  !! {slug}: {e}")
            continue
        if "svg" in ctype.lower() or url.lower().endswith(".svg"):
            print(f"  !! {slug}: SVG — Pillow cannot rasterise it. Export a PNG, "
                  f"or save the SVG to {LOGOS}/ and set `logo:` by hand.")
            continue
        png = normalise(raw, slug)
        if not png:
            continue
        (LOGOS / f"{slug}.png").write_bytes(png)
        print(f"     front matter: {set_front_matter(slug, f'{slug}.png')}")
        done += 1

    print(f"\n{done} of {len(pairs)} logo(s) saved to {LOGOS.relative_to(SITE)}/")
    print("Now run: python3 docs-check.py")


if __name__ == "__main__":
    main()
