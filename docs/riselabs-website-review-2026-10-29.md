# riselabs.at website review – record, 29 Oct 2026

- Content and structure review (Claude Doc): https://claude.ai/artifact/9uJmDgQqD4YnrDgB7nsGX4
- Layout and appeal review (Claude Doc, with screenshots): https://claude.ai/artifact/SUKCW8k7e8Vth1tPWxTqg9
- Shortened profile for Martin (Claude Doc, approved): https://claude.ai/artifact/Javw8atPF34f3X66b3RLZM
- Round 3: visual refinement against the RISE CI (Claude Doc): https://claude.ai/artifact/4pDbvLmqiKqPeiLDvt33vR
- Handover brief for Mel and the comms team (Claude Doc): https://claude.ai/artifact/AmeymPj6f8iko4hJ83R2ep
- Implementation spec for the website AI: `docs/07-review-implementation.md` (phases P1–P5, Phase L for layout L1–L18, Phase R for CI refinement R1–R11; human inputs H0–H26). The repo copy predates Phase R; the new version was delivered to Martin on 29 Oct. Plus `riselabs-asset-pack-2026-10-29.zip` for R6/R7/R10/R11 (thumbnails, photos, per-photo duotone previews, placeholders, German Datenschutz draft). P1 merged as PR #12; PR #19 (6b5b7d2); PR #21/#22 (235b9a8): five team pages live as drafts (Martin, Barbara, Nicole, Zuhaib, Norman Chinasamy).
- References viewed in Chrome: Smith Innovation (portraits, profile layout, project facts sidebar), Bauhaus Earth (documentary photos, news/events panel at hero, group photo, project team portraits), Eunomia (header "Get in touch", portrait mosaic, short quotes; avoid stock nature imagery), Carlson Lab (warm team page, research themes with own figures, publication cards; do not copy closed-access PDFs on Google Drive or the Softr iframe).

## Verdict (content)
Ready after minor revisions, plus two substantive upgrades (team page, publications). 21 issues: 3 critical, 9 major, 6 minor, 3 suggestions.

## Verdict (layout)
Strong brand (navy, magenta); the homepage below the hero was a single column of text lists: 10 bands, 5,656 px desktop / 9,994 px phone, no images except partner logos. 17 layout issues (L1–L17); L18 added for the profile.

## Verdict (round 3, after PR #19)
Structure much improved; the look now needs the CI applied consistently.
- Default theme was still dark (`_layouts/default.html` line 4) → R1 light default, both must work.
- Bands invisible because neighbours share a colour (blush + blush, white + white); dark alt band #0a2347 is 1.15:1 off navy → R2 tokens: `--surface` #f1f3f6 / #16325a, blush only for small highlights, never two same bands in a row; magenta as accent, not fill.
- h2 20.8 px on 17 px body → R3 larger scale and band padding; switch to Circular.
- Inner pages 640 px column → R4 Article (40rem text + 18rem sticky sidebar) and Index (full-width card grid).
- Footer nav wraps in one 228 px column → R5 one-row grid, bottom bar "Initiatives: GBDI · INDICATE".
- Imagery: 38 publication thumbnails (20 open-access title pages, 18 CI tiles), 10 Unsplash photos for Expertise, Approach and two GBDI projects, CSS duotone for photos only → R6, R7.
- Team: "Extended team" replaces "core collaborators"; "We are growing" banner → R8.
- Analytics: Plausible → R10 (spec rule 1 now names it as the one allowed third-party script).
- Placeholders: one per kind (project: gradient + white signet; publication: designed tile rendered from front matter; person: initials on surface colour) → R11. Current fallback is 8 stock textures chosen by slug length mod 8.
- Phase R supersedes L5 (R4), L17 (R5), L4 (R2/R3/R9); covers the image parts of P2.5 and P4.1/L11.

## Decisions (Martin, 29 Oct)
- Team page: Martin, Barbara Droste-Luckmann (employed by RISE), Nicole Di Santo, Zuhaib Batra, Norman Chinasamy (extended team; drafts pending their approval).
- Green paper: one entry with Zenodo DOI 10.5281/zenodo.21030392; author form "Bjørkskov KBR".
- INDICATE LIFE: ends 2026; Croatia takes part (AT, HR, HU, IT, LU).
- Floor-area figure sourced to the Global Status Report 2025-2026 (UNEP, GlobalABC).
- Job posts week of 2 Nov 2026 → /join/ with mandatory minimum-pay line (Austrian rule, WKO).
- H16: portraits in black and white until harmonised headshots of all team members exist.
- H17: short verbatim testimonial versions approved (spec L9).
- H18: shortened profile approved unchanged.
- Round 3: light theme is the default; light and dark must both work.
- H19: duotone ramp A, the CI's magenta → blush, for light theme ("B is boring, A adds accents"; first chose B, reverted the same evening). CI dark duotone for dark. Text kept off tinted photos.
- H22: Circular licensed for web and desktop → self-host WOFF2, Figtree retired.
- H21: Plausible; 30-day trial (Business features), Business needed for user journeys ($19/mo at 10k pageviews, Oct 2026); setup steps in R10.
- H23: PDFs later; designed tiles remain as placeholders.
- 29 Oct: work handed over to Mel and the comms team.

## Open items
HTTPS/DNS fix (admin); Barbara's profile content; job post texts and pay; headshot shoot; consent for Rodríguez Droguett quote (H10); H20 three CC-BY-NC-ND title pages (alaux-2024, roeck-2020, soustverdaguer-2025) – tiles until answered; H23 PDFs; H24 Circular WOFF2 files; H25 approval of the Plausible Datenschutz section (incl. § 165 TKG consent question and retention wording); Plausible account setup by Martin; H26 Norman Chinasamy's approval.
