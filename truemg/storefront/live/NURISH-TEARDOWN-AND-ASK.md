# Nurish Labs, taken apart — and what Lapis must change to match it

Measured on **trynurishlabs.com**, 14 Oct 2026, by reading its live stylesheets
and DOM. Every number below is counted, not estimated.

## The headline finding

**Nurish's quality is not built with fancy JavaScript.** No GSAP, no Swiper, no
AOS, no Lenis, no scroll-observer reveals. Just jQuery and **1,360 CSS rules**
with **12 named keyframe animations**.

That is good news and bad news. Good: everything they do is reproducible with
CSS alone — no exotic runtime needed. Bad: **TrueMG's entire CSS budget is
10,000 characters**, and theirs is **311,053** — measured, not estimated:
187,416 characters across 1,184 readable rules plus 123,637 in inline blocks,
with **three cross-origin stylesheets unreadable on top**. So that figure is a
floor.

**31× the budget.** The binding constraint is not permission, it is **room**.

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

## Technique-by-technique — every line below was DRY-RUN against Lapis

Not inferred from Austin's email. Each property was sent through
`preview_design_change` and the refusal text below is **Lapis's own wording**.

| Technique | Nurish | Lapis verdict (measured) |
|---|---|---|
| `@keyframes` | **12 animations** | ⛔ *"@keyframes is not allowed"* |
| `animation` | 0.5s – 9s | ⛔ *"not in the allowed property list"* |
| `filter` | `drop-shadow()`, `brightness(1.45)` | ⛔ *"not in the allowed property list"* |
| `mix-blend-mode` | `multiply` | ⛔ *"not in the allowed property list"* |
| `mask-image` (+`-webkit-`) | 4 uses | ⛔ *"not in the allowed property list"* |
| `will-change` / `backface-visibility` | 2 each | ⛔ both refused |
| `position: fixed` | used | ⛔ *"can cover the whole page, its disclaimer included; use sticky, or absolute inside a section"* |
| `z-index` | 40, 1000, 1001, 999999 | ⛔ *"must be auto or a whole number from −1 to 9 (the header, menus and the disclaimer sit above that)"* |
| `html` / `body` / `main` | styled freely | ⛔ *"html, body, main and form fields cannot be targeted"* |
| offsets | max **100px** | ✅ ≤ 400px — fine |
| `transition` | 0.13 – 0.275s | ✅ ≤ 3s — fine |
| `backdrop-filter` | blur(8px) | ✅ ≤ 40px — fine |
| `clip-path` | 2 uses | ✅ allowed |
| `@media` | **101 queries** | ✅ works |

**11 of our probe rules were refused in one pass.**

### Two of those refusals have a stated reason, and it is a good one

`position: fixed` and high `z-index` are refused **to protect the research-use
disclaimer** — so a stylesheet cannot cover the compliance line. That is a
legitimate constraint on a site like this and should not be argued with. It
changes the shape of the ask: not *"let us use fixed"* but *"give us a layer
below the disclaimer"*.

### The library claim, verified properly

Checked for globals, not just script URLs: `gsap`, `ScrollTrigger`, `Swiper`,
`AOS`, `Lenis`, `ScrollMagic`, `anime`, `Motion` — **all absent**. Only jQuery.
No `IntersectionObserver`, no `requestAnimationFrame`. **8 CSS animations were
running live on the page** when measured. Their motion is pure CSS.

## The ask, ordered by how much it unlocks

### 1. Raise the customCss limit — this matters more than everything else combined

10,000 characters cannot hold a designed site. TrueMG's current stylesheet is
3,679 and that is one colour change away from cramped. **Nurish runs 311,053 —
31× the entire budget, and that is a floor** because three of its stylesheets
could not be read.

**Ask, in order of preference: an uploadable stylesheet file** (removes the
ceiling as a design constraint entirely), **or 50,000 characters.** Without one
of these the rest is rearranging deck chairs.

### 2. `z-index` above 9

9 cannot layer a sticky header over a dropdown over a modal. Nurish's own header
sits at 40 and its overlays at 1000+. **Ask: up to 9,999**, which is plenty and
still far below anything that could escape the store's own stacking context.

### 3. A stacking band below the disclaimer — not `fixed` itself

Lapis refuses `fixed` and z-index above 9 **to keep the research-use disclaimer
coverable by nothing.** Right call. So the ask is not to lift the rule, it is:

> Reserve a range — say z-index 1–900 for store styling, with the header,
> menus and disclaimer pinned above it — and allow `position: fixed` **only
> within the store root**, never over the disclaimer element. Then an owner can
> build a cart drawer or a back-to-top without any route to hiding compliance
> text.

Framing it their way is far more likely to get a yes than asking them to drop a
safety rule.

### 4. `@keyframes` and `animation` — confirmed refused, and this is the big one

No longer a question. Lapis says flatly: *"@keyframes is not allowed"*, and
`animation` is *"not in the allowed property list"*.

**Nurish had 8 CSS animations running on screen at the moment of measurement.**
That is where the sense of life comes from, and `transition` cannot substitute —
a transition needs a state change to fire; an animation runs on its own.

**Ask: allow `@keyframes` and `animation` with the same 3-second cap already
applied to transitions**, and the same honouring of `prefers-reduced-motion`.

### 5. `filter`, `mix-blend-mode`, `mask-image` — all three confirmed refused

- `filter: drop-shadow()` is how a cut-out vial gets a shadow that follows its
  silhouette instead of its bounding box. We hit exactly this and had to bake
  shadows into the PNGs instead.
- `mix-blend-mode: multiply` is how a white-ground product photo drops onto a
  tinted panel without a halo.
- `mask-image` with a gradient is how a section fades out instead of ending in a
  hard line — four of Nurish's softest edges are this.

**Ask: all three re-allowed, with the same stated caps approach used for the
others.** Also `will-change` and `backface-visibility`, which are refused and are
only ever performance hints.

### 6. Let `html`, `body` and `main` be targeted — or give us an equivalent

Measured: *"html, body, main and form fields cannot be targeted."* So the page's
own background cannot be set from customCss at all, which is why a site-wide dark
treatment is not simply a matter of one rule either.

### 7. A per-page hook, and section classes on every page

Already raised separately — see `ASK-AUSTIN-PAGE-HOOKS.md`. Nothing identifies a
route, and `/about`, `/contact` and `/lab-results` have **zero** `lf-section-*`
hooks while `/store` and `/catalog` have 35 and 27.

### 8. The honest long-shot: a way to add markup

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
