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

## Owner-side, still blocking

Stock on six products. Every card reads *Out of stock*, so nothing can be bought
no matter how the page looks. Anchor pricing (a struck-through compare-at price)
and volume tiers are admin-side too — the reference site never shows a bare
number, and that is the single biggest selling mechanic still missing.
