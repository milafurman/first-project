# Nurish Labs, taken apart — and what Lapis must change to match it

Measured on **trynurishlabs.com**, 14 Oct 2026, by reading its live stylesheets
and DOM. Every number below is counted, not estimated.

## The headline finding

**Nurish's quality is not built with fancy JavaScript.** No GSAP, no Swiper, no
AOS, no Lenis, no scroll-observer reveals. Just jQuery and **1,360 CSS rules**
with **12 named keyframe animations**.

That is good news and bad news. Good: everything they do is reproducible with
CSS alone — no exotic runtime needed. Bad: **TrueMG's entire CSS budget is
10,000 characters.** Their 1,360 rules are roughly ten times that. So the
binding constraint is not permission, it is **room**.

## What they are, and what we are

| | Nurish Labs | TrueMG |
|---|---|---|
| Platform | **WordPress** — full theme and template control | hosted Lapis theme (`revive`) |
| Styling | unlimited stylesheets, 41 of them | **one 10,000-character box** |
| Markup | can add any element or wrapper | cannot add elements at all |
| Fonts | Inter Tight, self-hosted | Google Fonts link only |
| Images | 56, WebP | product/hero slots only |
| Scripts | 29 | none possible |

**This asymmetry is the real story.** They can add a `<div>` whenever an effect
needs one. We cannot add a single element, so any technique that needs a wrapper
is impossible regardless of which properties are allowed.

## Technique-by-technique, against Lapis's current limits

| Technique | Nurish | Lapis allows now | Verdict |
|---|---|---|---|
| `position` | fixed, absolute, relative, sticky | relative, absolute, sticky — **not `fixed`** | **BLOCKED** |
| `z-index` | 40, 1000, 1001, 99998, 999999, up to 2,147,482,000 | **≤ 9** | **BLOCKED — the worst one** |
| offsets | max **100px** | ≤ 400px | fine |
| `transition` | 0.13s – 0.275s | ≤ 3s | fine |
| `@keyframes` / `animation` | **12 animations**, 0.5s – 9s | **not mentioned in the re-allow** | **UNKNOWN — must ask** |
| `backdrop-filter` | blur(8px), blur(2px) | ≤ 40px blur | fine |
| `filter` | `drop-shadow(…)`, `brightness(1.45)` | was refused; **not in the re-allow list** | **BLOCKED** |
| `mix-blend-mode` | `multiply` | was refused; not re-allowed | **BLOCKED** |
| `mask-image` | **4 uses**, radial + linear gradients | never mentioned | **UNKNOWN** |
| `clip-path` | 2 uses | allowed | fine |
| `will-change`, `backface-visibility` | 2 each | not mentioned | **UNKNOWN** |
| `@media` | **101 queries** | works | fine |
| per-page styling | every page has its own template | **no page hook at all** | **BLOCKED** |

## The ask, ordered by how much it unlocks

### 1. Raise the customCss limit — this matters more than everything else combined

10,000 characters cannot hold a designed site. TrueMG's current stylesheet is
3,679 and that is one colour change away from cramped. Nurish runs ten times
that. **Ask: 50,000, or an uploadable stylesheet file.** Without this the rest is
rearranging deck chairs.

### 2. `z-index` above 9

9 cannot layer a sticky header over a dropdown over a modal. Nurish's own header
sits at 40 and its overlays at 1000+. **Ask: up to 9,999**, which is plenty and
still far below anything that could escape the store's own stacking context.

### 3. `position: fixed`

Needed for a sticky cart drawer, a back-to-top, an age gate, any overlay that
must survive scrolling. Nurish uses it. **Ask: allow `fixed` scoped inside the
store root**, if the concern is a rule escaping onto the admin chrome.

### 4. Confirm `@keyframes` and `animation`

Austin re-allowed `transition` but never said whether `@keyframes` blocks survive
the sanitizer. **Nurish's entire sense of life comes from 12 of them.** If they
are stripped, no amount of `transition` substitutes. **Ask: a direct yes or no,
and if no, please allow them with the same 3-second cap as transitions.**

### 5. `filter`, `mix-blend-mode`, `mask-image`

- `filter: drop-shadow()` is how a cut-out vial gets a shadow that follows its
  silhouette instead of its bounding box. We hit exactly this and had to bake
  shadows into the PNGs instead.
- `mix-blend-mode: multiply` is how a white-ground product photo drops onto a
  tinted panel without a halo.
- `mask-image` with a gradient is how a section fades out instead of ending in a
  hard line — four of Nurish's softest edges are this.

**Ask: all three re-allowed, with the same stated caps approach used for the
others.**

### 6. A per-page hook, and section classes on every page

Already raised separately — see `ASK-AUSTIN-PAGE-HOOKS.md`. Nothing identifies a
route, and `/about`, `/contact` and `/lab-results` have **zero** `lf-section-*`
hooks while `/store` and `/catalog` have 35 and 27.

### 7. The honest long-shot: a way to add markup

Every remaining gap after the above is "we cannot add an element". A per-section
HTML block, or theme-level template overrides, would close it. Worth asking even
if the answer is no, so we stop designing around a wall we think might move.

## What we can do today, with none of this granted

- Typography, spacing, colour, borders, radii, shadows via `box-shadow`
- `transition` on hover, within 3s
- `clip-path` for full-bleed bands (**re-expressed**: the old
  `inset(0 -100vmax)` exceeds the new 400px offset cap)
- `backdrop-filter` blur up to 40px
- CSS grid and flex, 101 media queries' worth of responsive behaviour
- `object-fit`, `aspect-ratio`

That is a genuinely good static site. It is not Nurish, and the single reason is
room plus the ability to layer and animate.
