# Design basis

What the stylesheet implements, and why. Moved out of the README so that file
stays short — this is the reference for anyone changing colours, type or
layout, and for whoever picks the site up at the CI revamp.

## Colour

Follows the RISE CI Manual v1.2.

| | |
| --- | --- |
| Navy | `#001730` — page background in the dark theme |
| Magenta | `#f92d84` — the only accent |
| Purple | `#751094` — gradient only, per the manual |
| Blush | `#ffe1ee` — pale tint |

These four are **brand constants**. They are declared once at the top of
`assets/css/style.css` and never used directly by a component.

Everything else reads a **semantic token**: `--bg`, `--surface`, `--ink`,
`--ink-soft`, `--accent`, `--rule`, `--field-bg`, `--tile-edge` and the
`--btn-*` set. The light theme redefines those eleven tokens and nothing
else. That is what makes two themes possible without two stylesheets — and it
means a new component gets both themes for free, as long as it never writes a
hex value of its own.

### Contrast

Checked, not eyeballed. Body text meets WCAG AA at 4.5:1; large text and
non-text graphics meet 3:1.

Two consequences worth knowing, because they look like mistakes otherwise:

- **Buttons are navy on magenta, not white on magenta.** White on `#f92d84`
  is 3.7:1, which fails AA for normal text. Navy on magenta is 4.9:1.
- **The light theme's accent is darker** (`#be208b`, not `#f92d84`). Brand
  magenta on white does not clear 4.5:1.

## Type

Figtree, self-hosted from `assets/fonts` and declared in the stylesheet.

There is deliberately **no Google Fonts link**. Loading it would make every
visitor's browser call Google and hand over their IP address, which needs a
legal basis and a disclosure. The body weight is preloaded because it is on
the critical path for every page.

## Layout

- `--measure: 40rem` — the reading column. Body text never exceeds it.
- `--wide: 64rem` — the wide container, for grids and figures that break out.

`.wrap` gives the wide container, `.wrap.narrow` the reading column.

## Images on white

Partner logos and figures sit on white cards (`.fig img`, `.tile`) in both
themes. That is intentional: artwork and charts are drawn for white, and
recolouring them per theme would drag the magenta signet off-brand. A white
card on navy is a deliberate surface, not an oversight.

## Themes

Dark is primary and is what every visitor gets first. The toggle sits in the
bottom-right corner and flips `data-theme` on `<html>`.

The choice is remembered in `localStorage` under `rise-theme` — one word, set
only when the visitor presses the button, never transmitted. An inline script
in `<head>` applies it before first paint, so there is no flash of dark on a
light-theme reload. This is disclosed on the Datenschutz page; if you remove
the toggle, remove that section too.

## What would break the design

- A hex value written inside a component rule. Use a token.
- An embedded third-party script or font. It re-opens the privacy question the
  self-hosting exists to close, and needs a Datenschutz section and probably a
  consent banner.
- Text over a photograph without a scrim. The hero has one; anything new needs
  its own.
