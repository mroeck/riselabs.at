# Design basis

What the stylesheet implements, and why. Moved out of the README so that file
stays short - this is the reference for anyone changing colours, type or
layout, and for whoever picks the site up at the CI revamp.

## Colour

Follows the RISE CI Manual v1.2.

| | |
| --- | --- |
| Navy | `#001730` - page background in the dark theme |
| Magenta | `#f92d84` - the only accent |
| Purple | `#751094` - gradient only, per the manual |
| Blush | `#ffe1ee` - pale tint |

These four are **brand constants**. They are declared once at the top of
`assets/css/style.css` and never used directly by a component.

Everything else reads a **semantic token**: `--bg`, `--surface`, `--tint`,
`--ink`, `--ink-soft`, `--accent`, `--rule`, `--field-bg`, `--tile-edge` and
the `--btn-*` set. The light theme redefines those tokens and nothing else.
That is what makes two themes possible without two stylesheets - and it means
a new component gets both themes for free, as long as it never writes a hex
value of its own.

Two of them have a job that is easy to get wrong:

- **`--surface` is the alternate band and the card.** Light `#f1f3f6`, dark
  `#16325a`. It is the only alternate band colour.
- **`--tint` is blush, and only for small things.** A tag, a banner, a
  highlight inside a band. Blush used to be `--surface`, which made two blush
  bands in a row merge into one long pink stretch; R2 took it off bands for
  good. If a tint is covering more than a paragraph, it is the wrong token.

### Bands

Two adjacent bands never share a background. The home page is written out by
hand, so this is checked by eye and recorded in the comment at the top of
`index.md`; moving a band means re-checking every band below it.

The closing band is the exception: it carries the CI gradient
(`--gradient-text-bed`) and redefines the tokens on itself so everything
inside inherits white. The gradient under text is darkened by a quarter-
opacity navy, because white on the bare magenta end is 3.66:1.

### Contrast

Checked, not eyeballed. Body text meets WCAG AA at 4.5:1; large text and
non-text graphics meet 3:1.

Two consequences worth knowing, because they look like mistakes otherwise:

- **Dark-theme buttons are navy on magenta, not white on magenta.** White on
  `#f92d84` is 3.7:1, which fails AA for normal text. Navy on magenta is
  4.9:1. The light theme's buttons are white on navy, 17.2:1.
- **Neither theme's accent is the brand magenta.** Light uses `#be208b`,
  because `#f92d84` on white does not clear 4.5:1. Dark uses `#ff6ba6`,
  because `#f92d84` on the `#16325a` band is 3.50:1. The brand magenta is
  still itself wherever it is a fill rather than text: the gradient, the hero
  and the dark theme's buttons.

## Type

Two faces, for two jobs.

**Headings and labels: Circular**, the CI typeface, self-hosted from
`assets/fonts`. One cut is licensed and present, Medium 500, so headings are
set at 500 and the stylesheet carries `font-synthesis: none`; nothing is ever
faked into a bold or an italic. The `@font-face` family is Lineto's own file
name, `CircularXXWeb-Medium`, because the licence forbids renaming the font.

**Body text: Figtree**, self-hosted, SIL Open Font License. It stood in for
Circular across the whole site and keeps the body text until Circular's Book
(400) cut arrives. `assets/fonts/README.md` has the licence, what is missing
and what the domain question is.

The scale follows the CI's step from heading to body: `h1`
`clamp(2.25rem, 5vw, 3rem)`, `h2` `clamp(1.75rem, 3vw, 2.125rem)`, body
`17px`. That is about 2:1 between h2 and body, where the site used to have
1.2:1 and section heads barely registered.

There is deliberately **no Google Fonts link** and no font service of any
kind. Loading one would make every visitor's browser call a third party and
hand over their IP address, which needs a legal basis and a disclosure. Every
font file is served from this site.

## Layout

- `--measure: 40rem` - the reading column. Body text never exceeds it.
- `--wide: 64rem` - the wide container, for grids and figures that break out.

`.wrap` gives the wide container, `.wrap.narrow` the reading column.

## Images on white

Partner logos and figures sit on white cards (`.fig img`, `.tile`) in both
themes. That is intentional: artwork and charts are drawn for white, and
recolouring them per theme would drag the magenta signet off-brand. A white
card on navy is a deliberate surface, not an oversight.

## Themes

**Light is the default; dark must work equally well.** (Decided 29 October
2026, replacing "dark is primary".) Neither is a second-class rendering:
every change is checked in both, and the contrast figures above are met in
both.

What a visitor actually gets, in order: a theme they chose here before, else
their operating system's `prefers-color-scheme`, else light. The markup ships
`data-theme="light"`, so that is also what anyone with JavaScript off sees.
The toggle sits in the bottom-right corner and flips `data-theme` on `<html>`.

The choice is remembered in `localStorage` under `rise-theme` - one word, set
only when the visitor presses the button, never transmitted. An inline script
in `<head>` applies it before first paint, so neither theme flashes into the
other on reload. This is disclosed on the Datenschutz page; if you remove
the toggle, remove that section too.

## What would break the design

- A hex value written inside a component rule. Use a token.
- An embedded third-party script or font. It re-opens the privacy question the
  self-hosting exists to close, and needs a Datenschutz section and probably a
  consent banner.
- Text over a photograph without a scrim. The hero has one; anything new needs
  its own.
