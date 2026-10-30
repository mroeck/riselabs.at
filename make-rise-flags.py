#!/usr/bin/env python3
"""Write `rise_work` into every publication.

A publication counts as RISE or GBDI work when someone on it has a
`rise_since` year in `_people/` and the publication is from that year or
later. That is the same rule the "With RISE or GBDI" filter uses.

The flag has to be a field rather than something the template works out,
because the publications list sorts on it: within a year, RISE work comes
first, and Liquid cannot sort on a value computed while rendering.

Run this after changing anyone's `rise_since`, or after adding a publication.
docs-check.py recomputes the same thing and fails on a mismatch, so a stale
flag cannot reach the site quietly.
"""
import pathlib
import re
import sys

import yaml

SITE = pathlib.Path(__file__).parent


def front_matter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def main():
    since = {}
    for f in (SITE / "_people").glob("*.md"):
        since[f.stem] = front_matter(f).get("rise_since")

    changed = []
    for f in sorted((SITE / "_publications").glob("*.md")):
        text = f.read_text()
        fm = front_matter(f)
        year = fm.get("year") or 0
        want = any(since.get(s) and year >= since[s] for s in (fm.get("people") or []))
        have = fm.get("rise_work")
        if have is want:
            continue
        line = f"rise_work: {'true' if want else 'false'}"
        if re.search(r"^rise_work:.*$", text, re.M):
            text = re.sub(r"^rise_work:.*$", line, text, count=1, flags=re.M)
        else:
            end = text.index("\n---\n", 3)
            text = text[:end] + "\n" + line + text[end:]
        f.write_text(text)
        changed.append((f.stem, have, want))

    for slug, have, want in changed:
        print(f"  {slug}: {have} -> {want}")
    print(f"{len(changed)} changed" if changed else "nothing to change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
