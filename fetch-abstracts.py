#!/usr/bin/env python3
"""Fill in publication abstracts, from the RISE Zotero library first.

Why this is a script and not something already done: abstracts have to come
from the record, not from a summary. Writing them by hand - or having a model
write them - produces plausible text that is not the paper's abstract, on a
page that carries a DOI. So this fetches the real thing.

Three sources, tried in order:

  1. The RISE group library on Zotero. Preferred, because it is ours: the
     abstracts in it have been through a human, and it covers reports and
     datasets that publishers never deposited anywhere.
  2. Crossref, by DOI.
  3. OpenAlex, by DOI, reconstructed from its inverted index.

Run it from the site root, with a network connection:

    python3 fetch-abstracts.py            # report what is found, change nothing
    python3 fetch-abstracts.py --write    # fetch and insert
    python3 fetch-abstracts.py --no-zotero   # skip the library

It only touches files whose body is empty or still holds the placeholder
comment. A publication you have already written about by hand is left alone
and reported as "skipped".

Nothing is sent anywhere except the DOI and a contact address, which Crossref
asks for so it can reach you if a script misbehaves. The Zotero group is read
anonymously; that works while the group is public. If it is private, set
ZOTERO_API_KEY in the environment and the script will use it.
"""

import argparse
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

MAILTO = "martin.roeck@riselabs.at"
ZOTERO_GROUP = "6485191"          # RISE Open - zotero.org/groups/6485191/rise_open
PUBS = pathlib.Path(__file__).parent / "_publications"
UA = f"riselabs.at abstract fetcher (mailto:{MAILTO})"

FRONT = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
JATS = re.compile(r"<[^>]+>")


def get(url, headers=None):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm_doi(doi):
    doi = (doi or "").strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    return doi


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def load_zotero():
    """Pull the whole group library once, indexed by DOI and by title.

    Public groups read without a key. A private one needs ZOTERO_API_KEY.
    Returns ({doi: abstract}, {title: abstract}), either possibly empty.
    """
    by_doi, by_title = {}, {}
    headers = {"Zotero-API-Version": "3"}
    key = os.environ.get("ZOTERO_API_KEY")
    if key:
        headers["Zotero-API-Key"] = key

    start, total = 0, None
    while True:
        url = (f"https://api.zotero.org/groups/{ZOTERO_GROUP}/items/top"
               f"?format=json&limit=100&start={start}")
        try:
            batch = get(url, headers)
        except urllib.error.HTTPError as e:
            print(f"  !! Zotero returned HTTP {e.code}"
                  + (" - the group may be private; set ZOTERO_API_KEY"
                     if e.code in (403, 404) else ""))
            return {}, {}
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            print(f"  !! could not read the Zotero library: {e}")
            return {}, {}

        if not batch:
            break
        for item in batch:
            d = item.get("data") or {}
            abstract = (d.get("abstractNote") or "").strip()
            if not abstract:
                continue
            doi = norm_doi(d.get("DOI"))
            if doi:
                by_doi.setdefault(doi, abstract)
            title = norm_title(d.get("title"))
            if title:
                by_title.setdefault(title, abstract)
        start += len(batch)
        if total is not None and start >= total:
            break
        if len(batch) < 100:
            break
        time.sleep(0.2)

    print(f"  Zotero: {len(by_doi)} item(s) with a DOI and an abstract, "
          f"{len(by_title)} by title")
    return by_doi, by_title


def clean(text):
    """Crossref abstracts arrive as JATS XML; strip the tags, keep the words."""
    text = re.sub(r"<jats:title>.*?</jats:title>", "", text, flags=re.S | re.I)
    text = JATS.sub("", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = re.sub(r"\s+", " ", text).strip()
    # some publishers prefix the word "Abstract"
    return re.sub(r"^abstract[:\s]+", "", text, flags=re.I).strip()


def from_crossref(doi):
    try:
        d = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
                f"?mailto={urllib.parse.quote(MAILTO)}")
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None
    a = (d.get("message") or {}).get("abstract")
    return clean(a) if a else None


def from_openalex(doi):
    """OpenAlex stores abstracts as a word -> positions index, for licensing
    reasons. Reconstructing it gives back the original text."""
    try:
        d = get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}"
                f"?mailto={urllib.parse.quote(MAILTO)}")
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None
    idx = d.get("abstract_inverted_index")
    if not idx:
        return None
    positions = {}
    for word, places in idx.items():
        for p in places:
            positions[p] = word
    if not positions:
        return None
    return " ".join(positions[i] for i in sorted(positions)).strip()


def wrap(text, width=78):
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        out.append(line)
    return "\n".join(out)


def body_is_empty(body):
    stripped = re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()
    return stripped == ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="actually edit the files")
    ap.add_argument("--force", action="store_true",
                    help="also replace bodies that already have text")
    ap.add_argument("--no-zotero", action="store_true",
                    help="skip the RISE group library and go straight to Crossref")
    args = ap.parse_args()

    if not PUBS.is_dir():
        sys.exit(f"no {PUBS} - run this from the site root")

    zot_doi, zot_title = ({}, {}) if args.no_zotero else load_zotero()

    found = missing = skipped = nodoi = 0
    by_source = {}

    for f in sorted(PUBS.glob("*.md")):
        m = FRONT.match(f.read_text())
        if not m:
            print(f"  ?? {f.name}: no front matter")
            continue
        front, body = m.group(1), m.group(2)

        doi_m = re.search(r'^doi:\s*"?([^"\n]+)"?', front, re.M)
        title_m = re.search(r'^title:\s*"(.*)"', front, re.M)
        doi = norm_doi(doi_m.group(1)) if doi_m else ""
        title = norm_title(title_m.group(1)) if title_m else ""

        if not body_is_empty(body) and not args.force:
            skipped += 1
            continue

        # 1. our own library, by DOI then by title - a title match covers the
        #    reports and datasets that have no DOI at all
        abstract, source = None, None
        if doi and doi in zot_doi:
            abstract, source = zot_doi[doi], "Zotero"
        elif title and title in zot_title:
            abstract, source = zot_title[title], "Zotero (title match)"

        # 2. and 3. the public metadata services, which need a DOI
        if not abstract and doi:
            abstract = from_crossref(doi)
            source = "Crossref"
            if not abstract:
                abstract = from_openalex(doi)
                source = "OpenAlex"
            time.sleep(0.4)   # be polite to a free service

        if not abstract:
            if not doi:
                nodoi += 1
                print(f"  -- {f.name}: no DOI and not matched in Zotero")
            else:
                missing += 1
                print(f"  -- {f.name}: no abstract anywhere for {doi}")
            continue

        by_source[source] = by_source.get(source, 0) + 1

        found += 1
        print(f"  ok {f.name}: {len(abstract)} chars from {source}")

        if args.write:
            where = f"{source} for DOI {doi}" if doi else f"{source}"
            note = (f"<!-- Abstract as held by {where},\n"
                    f"     retrieved {time.strftime('%Y-%m-%d')}. Reproduced as\n"
                    f"     recorded; edit only to fix encoding. -->\n\n")
            f.write_text(f"---\n{front}\n---\n\n{note}{wrap(abstract)}\n")

    detail = ", ".join(f"{n} from {s}" for s, n in sorted(by_source.items()))
    print(f"\n{found} abstract(s) found" + (f" ({detail})" if detail else "")
          + f", {missing} not deposited anywhere, {skipped} already written, "
            f"{nodoi} with neither a DOI nor a Zotero match")
    if not args.write and found:
        print("Nothing was changed. Re-run with --write to insert them.")


if __name__ == "__main__":
    main()
