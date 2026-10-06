# Vial images — transparent, all 17

Every product image with the baked-in white background removed. **These are the
files that unblock the brand palette.** Upload them in Lapis to replace the
current ones; no agent can do that step.

| | |
|---|---|
| Count | 17 products |
| Size | 2000 × 2000 PNG, RGBA with a real alpha channel |
| Weight | ~1 MB each, 17 MB total |
| Framing | Vial occupies 79% of frame height — unchanged from the originals, so this is a drop-in replacement with no layout risk |

`contact-sheet.jpg` shows all 17 composited on the brand ink ground.

## Why this was done here rather than through a background-removal service
The obvious route returns a 200 × 200 preview, which is useless for a product
photo. These were cut at the original full resolution instead, from the source
files on the store's own CDN.

## How the cut works — `cutout.py`
The naive approach to a white background is to make every near-white pixel
transparent. That destroys this particular subject: the vial is clear glass with
a **white label**, and a brightness threshold alone punches holes straight
through both.

So the script does not threshold on brightness. It thresholds, then keeps only
the regions **connected to the image border**:

1. Mark every pixel at or above `#F4F4F4` on all three channels as candidate background.
2. Label the connected components of that mask.
3. Keep only components that touch an outer edge. Enclosed white — the label, the
   highlights inside the glass, the gap under the crimped cap — is never reached
   and stays fully opaque.
4. Soften the last 3px inward, ramped on how white each pixel is, which removes
   the white fringe that otherwise haloes a cutout on a dark ground.
5. A 0.6px blur to anti-alias.

Verified: 75.8% of each frame became transparent, 24.1% stayed fully opaque,
~9,900 pixels landed in the soft edge. All 17 produced identical silhouettes,
which is expected — they are one vial mockup re-labelled per product.

Re-run with `python3 -I cutout.py <filename…>` against `cut/src`.

## What this does and does not deliver
It delivers **"clean images without white backdrops"**. It does not deliver
**"dynamic"** — these are still shot dead-straight, centred and flat. Dynamism
is the next step and it is CSS: a cast shadow, a few degrees of rotation, a
hover lift, a gold rim light. That works on these files now that they are
transparent. Genuinely new renders — angled, floating, lit — are a later job.

---

# UPDATE — the labels still carried the old blue brand

Removing the white background did nothing about what is **printed on the label**.
The blue product name, the blue MG, and the old blue dragon mark were all inside
the artwork, and the first pass shipped all three. Caught on review, fixed here.

`rebrand.py` runs after `cutout.py` and does three things:

1. **Recolours the blue type** — product name and the MG — to `#9C7C34`, the
   brand's gold for a paper ground. Each pixel keeps its own lightness so
   anti-aliased letter edges stay smooth instead of going chunky.
2. **Erases the old dragon.** Its pixels are reconstructed row by row from the
   label stock either side, because the label carries a soft vertical gradient
   and a flat median fill leaves a visible rectangle. The seam is then feathered.
3. **Drops the new Gila mark in**, rendered from `truemg/assets/logo/truemg-mark-ink.svg`,
   centred in the space the old one occupied.

Verified: **zero** pixels matching the brand blue survive in any of the 17.

## The limit of this, stated plainly

This fixes **the images on the website**. It does not change **the labels on the
bottles**. These are product mockups, so retouching them is legitimate for a
storefront — but if physical vials have already been printed with the blue
label, the site would then show a product that does not match what ships, and
that is a worse problem than an off-brand photo.

Two things follow, and neither is an agent job:

- **Confirm whether any labels are printed.** If they are, either the site keeps
  the old artwork until stock turns over, or the labels get reprinted.
- **The real deliverable is a label design file**, not a retouched mockup —
  flat artwork in the brand, set for the actual die line, which a printer can
  run. That is a separate piece of work and it should happen before any
  significant print run.
