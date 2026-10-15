# Image specs — hand this to whoever makes the art

Every one of these is **Mila-side**. The Lapis design endpoint cannot upload or
replace a product photo; it can only point at a URL that already exists.

## The rule that governs all of it
**A white backdrop is a bug.** Every vial currently sits in a hard white square
inside a grey card. That single detail is most of why the store reads as a parts
catalogue instead of a brand. Transparent PNG, always.

## Product vials — the main job
| Spec | Value |
|---|---|
| Format | PNG with real alpha. Not JPG, not PNG-on-white |
| Size | 1600 × 1600, vial occupying ~70% of frame height |
| Angle | 8–15° off vertical. Never dead-straight, never dead-centre |
| Shadow | Baked soft contact shadow under the vial, on transparency |
| Label | Legible at 300px wide — that is the real catalogue card size |
| Lighting | One key from upper left, soft fill right, visible highlight down the glass |
| File name | `tmg-<compound>-<size>.png`, lowercase, e.g. `tmg-bpc157-tb500-20mg.png` |

Shoot or render **17 products / 20 variants**. Priority six first, so the Friday
order test has something real to click:
BPC-157 + TB-500 · GHK-CU · TESAMORELIN · TMG-3RT · IPAMORELIN · NAD+

## Colour field per compound
The reference site gives every vial its own soft gradient field keyed to that
vial's label colour — lilac, blue, red, mint. The background *is* the brand.

Two ways to get there, and they stack:
1. **In the render** — bake the gradient behind the vial. Best result, most work.
2. **In CSS** — transparent vial over a per-product gradient drawn by `customCss`.
   Agent-side, no new art needed, and it is how Day 1 ships.

Set `productImageBg` to empty, never to `#ffffff`. The white well is the thing
we are removing.

## Hero
| | |
|---|---|
| Desktop `heroBackgroundUrl` | 2560 × 1400, under 400KB, WebP |
| Mobile `heroBackgroundMobileUrl` | 1200 × 1600 portrait crop |
| Composition | Subject right of centre — `heroAlign` is `left`, so the headline holds the left column |
| Weight | It is the LCP element. Over 400KB and it costs ranking as well as patience |

## Logo
SVG preferred. Failing that, transparent PNG at 1000px+ on the long edge. Light
and dark variants if they exist. `logoScale` (0.5–2) tunes size on the site, so
supply it large and let the platform scale down.

## Social share
`seoImageUrl` — 1200 × 630. Currently pointed at the raw brand logo PNG, which
renders as a small mark on a wide white field in every share preview. Needs a
real composed card.

---

# UPDATE — the white background is baked into the files

Verified 2026-10-06 against the live source files, not assumed.

The product images are PNGs at 2000 × 2000 in **RGB mode — no alpha channel at
all** — with pure `#FFFFFF` in every corner. The white is inside the file.

This was tested properly: setting `productImageBg` to the brand's near-black
turned the card dark and **the white rectangles stayed**. No palette, no CSS, no
platform setting can remove them. New files are the only fix.

**This is why the brand palette cannot go live yet.** On the ink ground, white
rectangles behind every vial look markedly worse than the current light theme.
The order is: transparent images first, palette second.

## The good news: these cut out cleanly

2000 × 2000 on pure white is close to ideal input. A background removal on
`TMG-3RT 10MG` produced a real alpha channel (range 0–255) with the glass body,
the crimped cap and the label all intact and no halo. Composited on `#0A0A0B`
the vial floats correctly.

So this is **a background-removal pass over existing art, not a reshoot.** All
17 products already exist at full resolution in the Canva library — the test
file came back already named "TrueMGLabs Branding - 7", so the set is there.

## What transparency does and does not buy

Removing the white delivers *"clean images without white backdrops."* It does
**not** deliver *"make the vials look dynamic."* These are shot dead-straight,
centred and flat. Dynamism comes from one of two places:

1. **CSS** — a cast shadow, a few degrees of rotation, a hover lift, a gold rim
   light. Agent-reachable, ships this week, works on the existing art once it is
   transparent.
2. **New renders** — angled, floating, lit. Better, slower, not a Friday job.

Do 1 now. Schedule 2 after launch.

---

# VIAL RENDERS — supersedes the spec above (15 Oct 2026)

**Read this section first. Where it disagrees with the table above, this wins.**
The spec above was written before any vial was delivered. Sam has now delivered one, and that
file — not the table above — is the reference.

## Source of truth

Mila, 15 Oct: *"Sam created the vials. Use the files in the Drive Sam gave us. Do not use any
other location to pull or upload from. We are not using the ones you created."*

- **Only source:** `drive.google.com/drive/folders/1RnTchA_5Tiz3tk0KEAhYu85-R3QKdlxq` → `vial/Labels`
- **Do not use** `truemg/assets/vials/tmg-*.png` or `~/Desktop/TRUEMG UPLOAD`. Both are earlier
  renders and are off-brand. All 17 photos currently live on the store came from them and are
  placeholders to be replaced.
- Finished files go back into Sam's folder. It is shared "anyone with the link — Viewer", so
  only Sam can add to it.

## Reference file

`exec-3e56feb1-fab7-426e-a414-f3e85bea3cef.png` — **TMG-3RT 10MG**, 1254x1254, RGBA,
transparent. Match it.

Note the size: **1254x1254**, not the 1600x1600 in the older table. Match the delivered file.

There is also a marble-worktop lifestyle shot, 1145x1374 RGB, with BATCH 60392 / LOT 60393 on
the label. **That is a separate, optional deliverable.** It is wrong for a product card — the
storefront sits the image on a tinted background, so any baked-in backdrop renders as a visible
box. The transparent cutout is the one the site needs.

## Label elements, observed on the reference

- Compound name in blue; strength beneath it in black
- `TRUE MG LABS` set vertically up the right side of the label
- A large pale ghosted lizard filling the label behind the mark
- The solid blue lizard mark, lower left
- `NOT FOR HUMAN CONSUMPTION` / `RESEARCH USE ONLY`, on two lines
- A DNA-helix motif down the right edge
- White flip-top cap over a blue crimp
- BATCH / LOT vertical — on the lifestyle shot only

**Do not rewrite any label text.** The compliance block is fixed and must not be AI-generated.

## Labels: nothing needed

All 40 label print files already exist in Drive — a `SIDE-` and a `TOP-` PDF for every one of
the 20 size-slots, reconciled slot by slot on 15 Oct, none missing, no extras. Do not
regenerate them.

## The 19 still needed

Delivered: TMG-3RT 10MG. Everything below is outstanding.

| Product (store name) | Strength | SKU |
|---|---|---|
| BPC-157 + TB-500 | 20MG (10+10) | TMG-BPC157TB500-20MG |
| CJC-1295 (No DAC) + IPAMORELIN | 10MG (5+5) | TMG-CJC1295IPA-10MG |
| EPITHALON | 10MG | TMG-EPI-10MG |
| GHK-CU | 50MG | TMG-GHKCU-50MG |
| IPAMORELIN | 10MG | TMG-IPA-10MG |
| KLOW | 80MG blend (TB10+BPC10+GHK50+KPV10) | TMG-KLOW-80MG |
| MOTS-C | 20MG | TMG-MOTSC-20MG |
| NAD+ | 1000MG | TMG-NAD-1000MG |
| SELANK | 10MG | TMG-SELANK-10MG |
| SEMAX | 10MG | TMG-SEMAX-10MG |
| SS-31 | 10MG | TMG-SS31-10MG |
| SS-31 | 50MG | TMG-SS31-50MG |
| TESAMORELIN | 20MG | TMG-TESA-20MG |
| THYMOSIN ALPHA-1 | 10MG | TMG-TA1-10MG |
| TMG-2TZ | 10MG | TMG-2TZ-10MG |
| TMG-2TZ | 20MG | TMG-2TZ-20MG |
| TMG-3RT | 20MG | TMG-3RT-20MG |
| TMG-BAC | 10ML | TMG-BAC-10ML |
| VITAMIN B12 | 10ML | TMG-B12-10ML |

**These three first.** They are the only size-slots on the live store with no photo at all, so
until they land, choosing that strength shows a mismatched image:

1. SS-31 10MG
2. TMG-2TZ 10MG
3. TMG-3RT 20MG

## Naming

TMG-BAC is **never** called bacteriostatic water, in any field or file name. Use the store
names — TMG-2TZ, TMG-3RT, TMG-BAC — not the underlying compound names.
