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
