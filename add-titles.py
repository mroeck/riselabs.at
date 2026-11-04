#!/usr/bin/env python3
"""Give every partner and person file a `title:` equal to its `name:`.

Q1.6, 4 Nov 2026. A collection document with no `title` gets one from Jekyll,
made out of its file name: /partners/bpie/ was "Bpie - RISE" in the tab and in
og:title, and /team/martin-roeck/ was "Martin Roeck", with the umlaut lost.
Neither name is written anywhere; both are guessed from a slug.

The page itself never showed this. It reads `name`, as it always did. Only
the title, the Open Graph title and anything quoting them were wrong, which
is why it survived: a browser tab and a link preview are the two places
nobody looks while building a page.

Run again safely: a file that already has a `title` is left alone.
"""
import pathlib, re, sys

changed, already = [], 0
for coll in ("partners", "people"):
    for f in sorted(pathlib.Path(f"_{coll}").glob("*.md")):
        text = f.read_text()
        m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
        if not m:
            print(f"  no front matter: {f}", file=sys.stderr)
            continue
        fm = m.group(1)
        if re.search(r"^title:", fm, re.M):
            already += 1
            continue
        nm = re.search(r'^name:[ \t]*(.+)$', fm, re.M)
        if not nm:
            print(f"  no name: {f}", file=sys.stderr)
            continue
        # The same value, quoted the same way, on the line above `name`, so
        # the two sit together and a later edit to one is next to the other.
        new_fm = fm.replace(nm.group(0), f"title: {nm.group(1)}\n{nm.group(0)}", 1)
        f.write_text(text[:m.start(1)] + new_fm + text[m.end(1):])
        changed.append(str(f))

print(f"{len(changed)} file(s) given a title, {already} already had one")
for c in changed[:4]:
    print(f"  {c}")
if len(changed) > 4:
    print(f"  ... and {len(changed) - 4} more")
