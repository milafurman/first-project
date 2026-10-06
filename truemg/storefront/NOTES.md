# Storefront — what is live

Applied through the Lapis design endpoint on the `arcane` template. The endpoint
reaches the palette, ~281 copy keys and one scoped `customCss` string. It cannot
reach products, stock, prices, images, checkout or settings.

## Palette

| key | value | why |
|---|---|---|
| `accent`, `themeAccent` | `#2866CD` | the brand blue, sampled off the original wordmark |
| `themeAccentDeep` | `#16397C` | the dark end of the button and band gradient |
| `background` | `#FBFCFE` | a cool near-white, so pure-white cards still read as cards |
| `card` | `#FFFFFF` | |
| `border` | `#E3E8F0` | cool enough to sit under the blue without going grey |
| `foreground` | `#10131A` | |
| `primary` | `#0A0A0B` | the footer and the promo band |

It was `#2563eb` (stock Tailwind blue) running into `#0c03b5` (a purple-navy),
which is why every button read as somebody else's brand.

## The white boxes

Every product photograph has white baked into the file, and the theme sat it on
the muted band `#ecebee`, so the white read as a rectangle floating in a grey
tile. Two fixes together: `productImageBg: "#ffffff"` and
`.lf-card .arcane-lozenge{background:#fff}`.

**A drop-shadow on those images makes it worse, not better.** `drop-shadow`
follows the alpha channel, and these files have none, so it casts a shadow of
the bounding box and draws the exact rectangle the rest of the work removes. It
goes in only once the transparent cut-outs in `truemg/assets/vials/` are
uploaded.

## Keys that save but do not render on `arcane`

These validate, save and read back correctly, and the live page ignores them.
Same class of problem as the `entryGate*` keys. Worth raising with Lapis.

| key | what happens |
|---|---|
| `faq` | Ten questions are stored; `/faq` renders the theme's own seven. |
| `homeSectionOrder` | Accepted; the section order on the page does not change. |
| `heroHeadlineAccent` | Accepted; the phrase does not pick up the accent colour. |
| `comparisonTable` | Renders, but inside a second `main.lf-store` that is injected *after* the footer, in a different layout wrapper from the rest of the page. Nothing in `homeSectionOrder` moves it. It is hidden in CSS and the same argument now runs in the discovery section, which does render mid-page. |

`aboutBody` does not parse markdown either — `**bold**` prints as literal
asterisks, so the sub-heads are set as plain capitalised lines.

## The compliance screen

Server-side, on every string, and it is blunt rather than contextual. It
rejected an About draft for the words **"patient"** (used as an adjective
meaning unhurried) and **"testimonials"** (in a sentence promising there would
be none), and it objects to second-person "you" in long-form body copy while
allowing it in the FAQ. Write long-form in the third person and pick synonyms
that have no clinical reading.

## Custom CSS

Selectors come from the live DOM, not from guessing: `.lf-card`,
`.arcane-lozenge` (the theme uses the same class for the product image frame
*and* for buttons), `.arcane-fill-grad`, `.lf-section-*`, `.bg-arcane-band`.

The sanitizer strips the child combinator `>`, so `.lf-promo-banner>*` became
`.lf-promo-banner *` and painted the gradient onto every text node inside the
banner. Write descendant selectors that are safe when widened.

`storefront.css` is the applied string.
