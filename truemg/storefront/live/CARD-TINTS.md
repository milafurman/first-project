# Keying each catalog card to its own colour — how, and the one trap

Measured against the live store, 12 Oct 2026.

## The problem

`1B.6` has said since the start that Amino Club's grid looks designed rather
than stocked because **each card's photo field is keyed to that vial's own
colour**, and ours is one pale blue seventeen times
(`.lf-card .aspect-square{background:#EDF4FB}`).

Doing it needs a per-product hook in the markup. **There isn't one.** Every card
on the live catalog carries byte-identical classes:

```
lf-card hover-lift group flex flex-col overflow-hidden rounded-2xl border border-border bg-card
```

No `data-` attribute, no product id, no slug class. The grid parent is just
`lf-catalog-grid`. Nothing distinguishes one card from another.

## What does work

The card sits **inside** an anchor, and the anchor's `href` is the product slug.
So the hook is the URL:

```css
a[href="/catalog/ghk-cu-hxoc"] .aspect-square{background:#F5E6E5!important}
```

Verified both halves:

- **The sanitizer accepts it.** `preview_design_change` returned `ok: true`,
  `wouldApply: ["custom styling updated"]`, no refused rules. Attribute
  selectors and descendant combinators are inside the allowlist — only nesting,
  `&`, `*` and `:has()` are out, and this needs none of them.
- **The selector is surgical.** Injected into the live page in the exact nested
  form Lapis wraps customCss in — `:where(.lf-store) a[href="…"] .aspect-square`
  — it matched **1** element, turned GHK-CU's field rose, and left all sixteen
  others on `#EDF4FB`. Nothing was saved; the test style tag was removed.

Budget is fine: the live stylesheet is **2,316 of 10,000 characters**, and
seventeen rules is about 1,250 more.

## ⚠️ The trap: these rules are welded to the URLs

A rule keyed to `href` breaks silently the moment a product's URL changes — the
card quietly falls back to the house blue and nothing errors.

**Two of the seventeen URLs are already slated to change.** `1F` flags them as
copy-rule breaches:

| Shows as | URL today |
|---|---|
| TMG-2TZ | `/catalog/tirzepatide-k8ms` |
| TMG-BAC | `/catalog/bacteriostatic-water-tzbc` |

So **do `1F` first, or do the tints knowing those two will need re-pointing.**
Doing the tints first and the URLs later is the order that produces a bug nobody
notices for a week.

## The seventeen slugs, as live on 12 Oct 2026

| Product | href |
|---|---|
| TESAMORELIN | `/catalog/tesamorelin-9ruh` |
| IPAMORELIN | `/catalog/ipamorelin-5pwi` |
| CJC-1295 (No DAC) + IPAMORELIN | `/catalog/cjc-1295-no-dac-ipamorelin-8jay` |
| BPC-157 + TB-500 | `/catalog/bpc-157-tb-500-r20n` |
| KLOW | `/catalog/klow-snoj` |
| GHK-CU | `/catalog/ghk-cu-hxoc` |
| EPITHALON | `/catalog/epithalon-f9mh` |
| SS-31 | `/catalog/ss-31-c73t` |
| MOTS-C | `/catalog/mots-c-atky` |
| NAD+ | `/catalog/nad-pjb7` |
| SELANK | `/catalog/selank-nsn7` |
| SEMAX | `/catalog/semax-m7yh` |
| THYMOSIN ALPHA-1 | `/catalog/thymosin-alpha-1-jvna` |
| VITAMIN B12 | `/catalog/vitamin-b12-vx6i` |
| TMG-2TZ | `/catalog/tirzepatide-k8ms` ⚠️ |
| TMG-3RT | `/catalog/tmg-3rt-2k6j` |
| TMG-BAC | `/catalog/bacteriostatic-water-tzbc` ⚠️ |

## Why this answers "eucalyptus on the site but not the label"

Three separate layers, and only the third one reaches a printer:

| Layer | Where it lives | Reaches a printer? |
|---|---|---|
| The page ground | the store's `background` + the `lf-section-*` bands in customCss | no |
| The field behind each bottle | `.aspect-square`, keyed per product as above | no |
| The label artwork | the Canva design, 20 pages | **yes** |

The colour Mila liked is layers 1 and 2. Layer 3 is **on hold** by her
instruction and is not needed for any of it. The bottles photographed on white
paper labels stay truthful to what ships, which is the whole reason the vial
README warns against retouching a mockup into something the customer will not
receive.

## Backup

`customCss-2026-10-12.css` in this folder is the live stylesheet as of today.
**Saving in Design studio wipes customCss** — re-apply from that file if it ever
comes back empty.
