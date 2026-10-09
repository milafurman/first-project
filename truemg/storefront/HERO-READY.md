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

## There is no staging store

Worth writing down, because it was assumed otherwise for a while. Lapis has one
store. `truemglabs.com` is live on the internet right now; the public sees a
coming-soon page because `comingSoonEnabled` is `"1"`, not because the site is
somewhere else.

So "go live" means two separate things and they must not be confused:

- **Applying a design change** saves to the real store, but the curtain is
  still down, so the public still sees the coming-soon page. Reversible in one
  call.
- **Clearing `comingSoonEnabled`** opens the store to the world. That is the
  launch, and it is gated on the attorney review, stock on all 20 variants and
  the rest of the open list.

`?peek=1` is Lapis's own door past the curtain — the schema says so: "The
Design preview and ?peek=1 links still show the real store." It works, and it
combines with `?ov=`, so a preview link can be opened without signing in.
Treat it as owner-only: anyone holding the link sees the store early.

## Correction: the logo preview caveat was wrong

Previews were described as showing a stock logo because the real one is too
large to ride inside a `?ov=` link. That is wrong. The logo is an UPLOAD in
Design studio -> Manual -> Logo, not a `customCss` rule, so it renders
correctly in previews whatever the stylesheet carries. (The live `customCss`
still holds a leftover `img[src*="brand-logos"]` rule that the logo README
already describes as retired — redundant, worth removing next time the
stylesheet is touched, which would also free about 8,000 characters.)

## The blank render, measured

Previously noted as roughly 1 in 10. Measured properly on 2026-10-09 against
the hero preview: five cold loads in a real browser, **three rendered, two
came back blank** — a blank page with the chrome but no content. A sixth and
seventh bare `?peek=1` load returned "upstream request failed" outright.

So it is nearer 40% than 10%, it is server-side, and it is not caused by the
length of the `?ov=` payload: the same URL alternates between rendering and
blanking with nothing changed. Reloading clears it.

This belongs in the Lapis mail with hard numbers rather than "it sometimes
goes blank".

## Still blocked

A band above the footer, like the Nurish one Mila asked for. The section is
there — `lf-section-ctaBanner`, right above the footer — but it takes no image,
and the CSS sanitizer rewrites every external `url()` to `url(#)`, so custom
styling cannot supply one either. Needs Lapis. Goes in the same mail as the
uploads not saving and the intermittent blank render.
