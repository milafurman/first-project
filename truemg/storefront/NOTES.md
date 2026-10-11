# Storefront — what is live

**Template: `revive`.** Switched from `arcane`, which was a catalogue page with a
colour scheme. `revive` is a shop: hero with artwork and proof chips, product
cards that carry a description, size chips and a price, a numbered how-it-works,
a dark quality band, an FAQ accordion on the home page and a closing CTA.

## The unlock: images by URL

The repository is public, so `cdn.jsdelivr.net/gh/...` serves it. Several copy
keys take an image URL, which means real artwork went on the site without
anything being uploaded into the Lapis product catalogue:

| key | file |
|---|---|
| `heroMediaUrl` | `hero-media.webp` — the transparent vial cluster; replaces the theme's product carousel |
| `heroBackgroundUrl` | `hero-field.jpg` — a plain blue field, 21KB |
| `heroBackgroundMobileUrl` | `hero-field-mobile.jpg` |
| `seoImageUrl` | `hero-desktop.jpg` — the share card |

**Pin the URL to a commit SHA, not a branch.** jsDelivr caches a branch's file
listing for about twelve hours, so a file added to an already-cached branch
returns 404 until that expires. `@<sha>` is immutable, resolves immediately and
never serves a stale copy. `raw.githubusercontent.com` is correct at once but is
not a CDN and should not carry storefront traffic.

The art is built by `truemg/assets/web/compose.py` from the transparent cut-outs.
These are the one place a drop shadow is right: the cut-outs have a real alpha
channel, so the shadow follows the glass. On the product cards, where the
uploaded catalogue photographs are still white-backed, the same effect draws a
rectangle.

A phone-sized trap: `heroMediaUrl` also renders on phones, so a mobile
background that contains vials paints a second set behind the first. The mobile
background is a plain field.

## Copy keys are per template

`arcane` and `revive` share maybe half their keys and the overlap is not
guessable — `browse1Href` exists on one and is rejected by the other. There is
no way to read a template's keys before switching to it, so: apply the template,
then `get_store_design` for the real list.

Three keys that were dead on `arcane` work on `revive`: `heroHeadlineAccent`
(the second line in brand blue), the FAQ, and the hero media. The FAQ moved from
one JSON blob to five `faqNQ`/`faqNA` pairs that render on the home page, which
is the better surface anyway.

Limits are tighter than they look and over-long values are silently truncated
rather than rejected — `productTrust1` is 30 characters, `faqNA` is 400,
`quality1Body` is 140. Check `schema.copyKeys[key].max` before writing.

## Still unresolved

`comparisonTable` renders into a wrapper injected after the footer on both
templates, and nothing moves it; it is hidden in CSS. `homeSectionOrder` is
inert. `aboutBody` does not parse markdown.

## The compliance screen

Server-side on every string, blunt rather than contextual. It rejected an About
draft for **"patient"** (used as an adjective meaning unhurried) and
**"testimonials"** (in a sentence promising there would be none), and objects to
second-person "you" in long-form body copy while allowing it in FAQ answers.

## Custom CSS

The sanitizer strips the child combinator `>`, so write descendant selectors
that stay correct when widened. `storefront.css` is the applied string.

**It also strips `@keyframes` blocks while keeping the `animation:` property.**
A custom animation therefore validates, saves, and shows the right
`animationName` in the browser, pointing at a rule that does not exist. Nothing
moves, and a screenshot looks identical to a working version. The only way to
catch it is to sample an element's position over several seconds.

Use the keyframes the theme already ships instead. Available on `revive`:
`float` (translateY 0 to -4px), `pulse`, `bounce`, `spin`, `rev-fade-up`,
`fade-up`, and the per-theme marquees. The hero cluster rides `float`.

Do not override `animation` on `.lf-section-hero .justify-center`. That wrapper
uses `rev-fade-up` to go from `opacity: 0` to `1`, so replacing the animation
leaves it at zero and the entire hero visual becomes invisible.

## Voice

Copy runs through the TELLS SCRUB in the `viral-formula` skill before it ships.
The first pass failed it badly: em dashes throughout, not one contraction on the
whole site, every body paragraph the same two sentences, threes everywhere.

The angle that makes this category work under a research-use-only constraint is
that **the fear is commercial, not medical**. Nothing may imply an outcome in a
person or an animal, but "most vendors post one certificate and sell a dozen
batches behind it" is specific, checkable and entirely compliant. The named
mechanic is **the lot match**.

## Owner-side, still blocking

Stock on six products. Every card reads *Out of stock*, so nothing can be bought
no matter how the page looks. Anchor pricing (a struck-through compare-at price)
and volume tiers are admin-side too — the reference site never shows a bare
number, and that is the single biggest selling mechanic still missing.

## Two hard limits, found the hard way

**`customCss` is capped at 10,000 characters.** Over that the endpoint refuses
the whole request with the count and the limit, and saves nothing. The header
lockup as a base64 data URI is 7.2KB, so it fits alongside the motion rules
with room to spare. The header *and* footer lockups together are 14.4KB of
base64 before a single other rule, so **both logos cannot coexist in CSS.** Only
an upload in the Lapis admin gets the mark into both places.

**A preview URL dies well before that.** Roughly 8,000 characters is the
practical ceiling; past it the server returns `URI_TOO_LONG` or simply hangs. So
any `customCss` big enough to carry an image can be applied but never previewed.

## The storefront renders empty on roughly one cold load in four

Not caused by anything here. Measured on the live coming-soon page over eight
cold loads with a fresh context and a cache-buster each time: 6 rendered, 2 came
back as an empty shell (HTTP 200, no images, `Skip to content` and nothing
else, no JavaScript error on the page). **The same 6/2 split appears with
`customCss` cleared entirely**, which is what rules out the custom styling.

It is worth raising with Lapis. It also means a single page load is not evidence
of anything: verify through several, or a pass that reports "no logo" is really
just a load that never rendered.
