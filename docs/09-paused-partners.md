# Partners temporarily off the site

Martin, 22 November 2026: take **ClimateWorks Foundation** and the **Global
Industry Hub** off the website as clients and funders, everywhere, and keep a
record so they can go back.

This is that record. It is the restore instructions, not a history note, so
keep it accurate if anything here moves.

## What to do to put them back

1. Delete the `published: false` line (and the comment above it) from
   `_partners/climateworks.md` and `_partners/global-industry-hub.md`.
2. Put back each line in the table below, exactly as written.
3. Run `python3 docs-check.py`. It fails while a reference points at a
   partner that is still unpublished, so it will tell you if you restore a
   reference and forget step 1, or the reverse.

Restoring one of the two without the other is fine. The table says which is
which.

## Exactly what was removed

| File | Field | Line removed |
|---|---|---|
| `_projects/global-building-data-initiative.md` | `funder` | `funder: "ClimateWorks Foundation"` |
| `_projects/global-building-data-initiative.md` | `clients` | the whole block: `clients:` and `  - climateworks` |
| `_projects/gbdi-china-and-india-cooperation.md` | `funder` | `funder: "Global Industry Hub"` |
| `_projects/gbdi-china-and-india-cooperation.md` | `clients` | the whole block: `clients:` and `  - global-industry-hub` |
| `_posts/2025-11-20-global-buildings-database.md` | `partners` | `  - climateworks`, which sat after `  - epfl` |
| `index.md` | partner band | `global-industry-hub`, which sat between `laudes` and `epfl` in the `assign shown` list |

`clients` was removed as a whole block in both projects because each listed
only the one organisation. Leaving `clients:` behind with nothing under it
would be a different thing from no clients at all.

The `funder` lines were removed rather than emptied. `_layouts/project.html`
compares `funder` against the `clients` names to decide whether the funder
says anything the client links do not; an empty string is not the same input
as a missing key, and the guard is `if page.funder and page.clients.size > 0`.

## What was deliberately left alone

- **Both partner files**, including their logos at
  `assets/img/partners/climateworks.svg` and
  `assets/img/partners/global-industry-hub.png`. Only `published: false` was
  added. The checker now notes both logos as unreferenced files; that is
  correct and expected while this is in force. Do not delete them in a
  clean-up: Q3 lists unreferenced assets for removal, and these two are the
  exception.
- **The project pages themselves.** Both GBDI projects still describe the
  work, the people and the outputs. Only who paid for it came off.
- **The partner map coordinates**, so the pins come back in the right places.

## What this changed on the live site

- `/partners/` lists two fewer organisations, and the two partner pages at
  `/partners/climateworks/` and `/partners/global-industry-hub/` stop
  existing. Anyone holding those links gets a 404.
- Both GBDI project pages lose their funder line entirely. Neither had any
  other client, so the row disappears rather than shortening.
- The home page partner band shows nine tiles instead of ten. It is a
  flex-wrap row of fixed-width tiles, so it simply reflows; there is no grid
  gap to fill, and no substitute tile was added.

## The check that guards this

`docs-check.py` treats a reference to an unpublished **partner** as a
problem, not a note, which is the opposite of how it treats an unpublished
person. The reason is in `_unpub_partner_msg`: `_includes/partners.html` has
no "skip it" branch, so it falls through to
`<span class="unknown">{{ key }}</span>` and prints the raw slug on the live
page. An unpublished person is skipped quietly by the people templates; an
unpublished partner is not.

That distinction was added on 22 November 2026, with this change, because
until then nothing had ever unpublished a partner. The same rule guards the
restore.
