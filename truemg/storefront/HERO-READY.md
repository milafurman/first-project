# Hero: ready to apply, not applied

Mila's standing rule: nothing goes live without her direct word. This records
exactly what to apply when it comes, so the decision does not have to be
reconstructed from a conversation.

## Copy keys

| key | value |
|---|---|
| `heroBackgroundUrl` | `…@a2e36e7/truemg/assets/web/hero-hand.jpg` |
| `heroBackgroundMobileUrl` | `…@a2e36e7/truemg/assets/web/hero-spa-mobile.jpg` |
| `heroMediaUrl` | `…@a2e36e7/truemg/assets/web/pixel.png` |
| `heroBackgroundPosition` | `center center` |

Base: `https://cdn.jsdelivr.net/gh/milafurman/first-project`

`heroMediaUrl` points at a 1×1 transparent pixel on purpose. The key cannot be
left empty — empty falls back to the first featured product's image — and the
hero's own photograph already carries the product.

## Custom styling

Apply `storefront.css` in full (9,542 of the 10,000 character cap). It is the
live stylesheet plus the two hero-scrim rules. The scrim rules alone are what
the preview link carries; the rest of the file is the logo and the hover
polish, which the link has no room for.

## Why the phone gets a different picture

The mobile hero is about 390×690 and the headline, subheading, two buttons and
three trust lines fill all of it. Three attempts at fitting product in ended
with vials sliced down the middle and text sitting on them. The phone gets the
room without product; the product is a thumb-flick below in the grid.

## Still blocked

A band above the footer, like the Nurish one Mila asked for. The section is
there — `lf-section-ctaBanner`, right above the footer — but it takes no image,
and the CSS sanitizer rewrites every external `url()` to `url(#)`, so custom
styling cannot supply one either. Needs Lapis. Goes in the same mail as the
uploads not saving and the intermittent blank render.
