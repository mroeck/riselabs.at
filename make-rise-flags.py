#!/usr/bin/env python3
"""Write `rise_tier` into every publication.

Three tiers, and they decide the order inside one year on /publications/:

  core      someone with `group: rise` in `_people/` is on it, and the
            publication is from their `rise_since` year or later. This is
            RISE's own output.
  extended  the same, but the person is a collaborator rather than core
            team: work by someone in the wider team, usually with their
            other institution, which RISE is part of but did not lead.
  prior     nobody on it was with RISE yet. Work the authors did before
            joining, which belongs on the list and belongs below the rest.

This replaced the `rise_work` boolean on 31 October 2026. The boolean put
"core" and "extended" in one bucket, so a year could open with a wider-team
paper while RISE's own most recent work sat under it, which is what Martin
reported that day. Nothing about the data changed, only how finely it is
read: both tiers come from the same `people` list and the same `rise_since`
years as before.

The tier has to be a field rather than something the template works out,
because the publications list sorts on it, and Liquid cannot sort on a value
computed while rendering.

Run this after changing anyone's `rise_since` or `group`, after adding a
person to a paper, or after adding a publication. docs-check.py recomputes
the same thing and fails on a mismatch, so a stale tier cannot reach the site
quietly.
"""
import pathlib
import re
import sys

import yaml

SITE = pathlib.Path(__file__).parent

ORDER = ("core", "extended", "prior")


def front_matter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def people_index(site=SITE):
    """slug -> (rise_since, group), for everyone in _people/."""
    out = {}
    for f in (site / "_people").glob("*.md"):
        fm = front_matter(f)
        out[f.stem] = (fm.get("rise_since"), fm.get("group"))
    return out


def tier_for(pb, people):
    """The tier a publication's front matter earns. Highest tier wins: one
    core author is enough, whoever else is on the paper."""
    year = pb.get("year") or 0
    found = set()
    for slug in (pb.get("people") or []):
        since, group = people.get(slug, (None, None))
        if since and year >= since:
            found.add("core" if group == "rise" else "extended")
    for t in ORDER:
        if t in found:
            return t
    return "prior"


def main():
    people = people_index()

    changed = []
    for f in sorted((SITE / "_publications").glob("*.md")):
        text = f.read_text()
        fm = front_matter(f)
        want = tier_for(fm, people)
        have = fm.get("rise_tier")
        if have == want and "rise_work" not in fm:
            continue
        line = f"rise_tier: {want}"
        if re.search(r"^rise_tier:.*$", text, re.M):
            text = re.sub(r"^rise_tier:.*$", line, text, count=1, flags=re.M)
            # the old boolean, where this file still carries one
            text = re.sub(r"^rise_work:.*\n", "", text, count=1, flags=re.M)
        elif re.search(r"^rise_work:.*$", text, re.M):
            text = re.sub(r"^rise_work:.*$", line, text, count=1, flags=re.M)
        else:
            end = text.index("\n---\n", 3)
            text = text[:end] + "\n" + line + text[end:]
        f.write_text(text)
        changed.append((f.stem, have if have else fm.get("rise_work"), want))

    for slug, have, want in changed:
        print(f"  {slug}: {have} -> {want}")
    print(f"{len(changed)} changed" if changed else "nothing to change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
