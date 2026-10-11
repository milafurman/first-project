# What the Lapis CSS sanitizer actually allows

Measured on 2026-10-11 by dry-running probe rules through
`preview_design_change` and reading the rejection list, after a stylesheet
that applied cleanly in the morning came back with 33 rules dropped in the
evening. The allowlist had tightened in between. Do not trust a rule because
it worked before; dry-run it.

## Rejected outright

| Property | Reason given |
|---|---|
| `position`, `inset`, `z-index` | not in the allowed property list |
| `clip-path`, `overflow` | not in the allowed property list |
| `filter`, `mix-blend-mode` | not in the allowed property list |
| `transition` | not in the allowed property list |
| `backdrop-filter` | not in the allowed property list |
| `transform` | one scale (0.5–2) and one translate only |
| `margin-left/right` | must stay between -200px and 400px |
| `color` with alpha | must be a plain, opaque colour |

## Allowed

`width` (including `100vw`), `max-width`, `padding-*`, `border-radius`,
`box-shadow`, `background-color`, `background-image` (gradients),
`border-*`, `color` (opaque only), `font-size`, `font-weight`,
`letter-spacing`, `text-transform`, `display`, `gap`, `opacity`, `content`,
`animation`. `!important` is fine and is often required.

## Two traps worth the scar tissue

**There is no full-bleed.** A section is a `max-w-7xl` centred container.
Bleeding it needs `clip-path`, `overflow`, or a `-50vw` margin, and all three
are blocked. `box-shadow: 0 0 0 100vmax <colour>` LOOKS like a way around it
and is allowed — but with `clip-path` stripped the shadow paints over the
neighbouring sections, which is exactly how the navy "Anyone can fill a vial"
band got wiped out and left white text on pale blue. Use tinted rounded
panels instead.

**The footer is a protected region**, because it carries the research-use
disclaimer. Its text cannot be resized, faded, hidden or moved — `font-size`,
`letter-spacing`, `display` and `margin` on anything inside it are refused,
and so is any `color` with alpha. Footer colours must be set as a PAIR
(`color` and `background-color` together, plain hex or rgb) so contrast can be
checked. This is a good rule. Do not look for a way around it; the small-caps
column headings are simply not available here.

A footer rule also needs `!important`: the theme puts its own class on the
`footer` element, and a bare element selector loses to it. The rule will be
ACCEPTED without it and then silently lose the cascade — which is worse than
being rejected, because nothing tells you.

## Design studio wipes customCss

Saving anything in Lapis Design studio (logo, favicon) resets the custom CSS
to its previous value. Do all Design studio work first, then re-apply the
stylesheet. Product image uploads do NOT wipe it — different screen.
