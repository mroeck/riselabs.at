# Fonts

## Circular (Lineto) - headings and labels

`CircularXXWeb-Medium.woff2` and `.woff`, the CI typeface, self-hosted. No
font service and no third-party request: the files are served from this site
like any other asset.

### Licence

    © 2019, Copyright by Lineto. All rights reserved.
    Circular is a trademark of Lineto.
    https://lineto.com/licensing

From the licence note Lineto supplies with the web package:

> Licence to use self-hosted webfonts for displaying dynamic text on specified
> website domains. Our package includes WOFF and WOFF2 font formats.
>
> Should the license page views limit be exceeded the license holder will be
> required to contact Lineto.com for an upgrade.
>
> It is strictly prohibited to rename the font and to download or use these
> fonts in any other media.
>
> These Web fonts are licensed exclusively for the use on the following
> domain(s) and their subdomains:
>
> www.riseregenerate.com (monthly pageviews: <50K)

Two things follow from that, and both are deliberate.

**The family keeps Lineto's name.** The `@font-face` rule in `style.css`
declares `font-family: "CircularXXWeb-Medium"`, the name of the file as
supplied, because the licence forbids renaming the font. It is not aliased to
"Circular" or to anything else.

**The licensed domain is www.riseregenerate.com.** This site is served from
riselabs.at today, which that licence does not cover. Martin's decision of
29 October 2026 is to make riseregenerate.com the site's primary domain and
redirect riselabs.at to it, which brings the site inside the licence; the move
is on the roadmap. Until it happens, the fonts are being served from a domain
the licence does not name. Whoever maintains this site should either finish
the move or ask Lineto to add riselabs.at to the licence. The page-view
ceiling is 50k a month on this licence; above it Lineto wants an upgrade.

Only the web formats are here. Do not commit the desktop OTF or TTF files to
this repository, which is public.

### Only one cut, for now

The package supplied on 29 October 2026 holds a single face: Medium, weight
500, upright. There is no Book (400) and no italic, which `fontTools` confirms
from the files themselves (`OS/2.usWeightClass` 500, the italic bit in
`head.macStyle` clear). A second file, `CircularXXSub-Medium`, is a 470-glyph
subset of the same 755-glyph face, not another weight, and is not used here.

So Circular is set on headings and labels only, which is the CI's own heading
weight, and body text stays on Figtree until the Book cut arrives. The site
sets `font-synthesis: none`, so nothing is ever faked into a bold or an
italic Lineto did not draw. When Book and the italics arrive, add their
`@font-face` rules and point `--font` at Circular; nothing else needs to
change.

## Figtree - body text

Figtree is licensed under the SIL Open Font License 1.1; see `LICENSE.txt`.
It stood in for Circular throughout the site and now carries the body text.
