#!/usr/bin/env python3
"""Fetch citation counts for publications that have a DOI, from OpenAlex.

Why OpenAlex and not Google Scholar: Scholar has no API, its terms do not
allow scraping, and its counts cannot be redistributed. OpenAlex is open
data with a public API, its `cited_by_count` is free to reuse, and it names
its source. The number will be lower than Scholar's, because Scholar counts
more grey literature. That is a difference worth stating on the page rather
than hiding.

This needs network access, which the environment the site is usually edited
in does not have. Run it anywhere with a connection:

    python3 fetch-citations.py            # report what would change
    python3 fetch-citations.py --write    # write it

It writes three fields, and all three matter: a bare number with no source
and no date is not evidence of anything.

    citations:        the count
    citations_source: "OpenAlex"
    citations_date:   the day it was fetched

Re-run it now and then. A count with an old date is not wrong, it is just
old, and the page says when it was taken.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

import yaml

SITE = pathlib.Path(__file__).parent
API = "https://api.openalex.org/works/doi:"
# OpenAlex asks for a contact address so they can reach you about heavy use.
MAILTO = "office@riselabs.at"


def front_matter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def fetch(doi):
    url = API + urllib.parse.quote(doi) + "?mailto=" + urllib.parse.quote(MAILTO)
    req = urllib.request.Request(url, headers={"User-Agent": f"riselabs.at ({MAILTO})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write the counts into the files")
    args = ap.parse_args()

    today = datetime.date.today().isoformat()
    changed, missing, failed = [], [], []

    for f in sorted((SITE / "_publications").glob("*.md")):
        fm = front_matter(f)
        doi = fm.get("doi")
        if not doi:
            missing.append(f.stem)
            continue
        try:
            data = fetch(doi)
        except Exception as e:                      # noqa: BLE001 - reported, not raised
            failed.append((f.stem, str(e)[:60]))
            continue
        count = data.get("cited_by_count")
        if count is None:
            failed.append((f.stem, "no cited_by_count in the response"))
            continue
        if fm.get("citations") == count:
            continue
        changed.append((f.stem, fm.get("citations"), count))
        if not args.write:
            continue
        text = f.read_text()
        for key, value in (("citations", count),
                           ("citations_source", '"OpenAlex"'),
                           ("citations_date", f'"{today}"')):
            line = f"{key}: {value}"
            if re.search(rf"^{key}:.*$", text, re.M):
                text = re.sub(rf"^{key}:.*$", line, text, count=1, flags=re.M)
            else:
                end = text.index("\n---\n", 3)
                text = text[:end] + "\n" + line + text[end:]
        f.write_text(text)

    for slug, old, new in changed:
        print(f"  {slug}: {old} -> {new}")
    print(f"\n{len(changed)} would change" if not args.write else f"\n{len(changed)} written")
    if missing:
        print(f"{len(missing)} have no DOI, so there is nothing to look up:")
        for s in missing:
            print(f"   {s}")
    if failed:
        print(f"{len(failed)} could not be fetched:")
        for s, why in failed:
            print(f"   {s}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
