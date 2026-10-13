# Vial images — transparent, all 17

> **2026-10-12 — the cap is fixed.** All 17 re-rendered. Mila: *"Look at the
> actual bottle and the cap. The blue doesn't go all the way to the white, and
> the white looks crooked."* Both of those were one bug.
>
> The cap is a cylinder photographed slightly from above, so **both edges of
> the aluminium band are ellipse arcs.** `recolour_crimp` was painting the blue
> between two flat fractions of the vial's height (`CRIMP = (0.085, 0.170)`). A
> straight line can only agree with an arc at one point, so what was left over
> was a **wedge** of bare metal — 16px under the middle of the white disc,
> about 10px at the sides. A parallel strip would have read as a design choice.
> A wedge reads as crooked, which is exactly what she saw.
>
> `find_crimp()` now measures both edges **per column** out of the photograph
> itself — steepest darkening for the top (the shadow seam where the plastic
> overhangs the metal), last metal row for the bottom (the cap overhangs the
> glass, so at the outer columns there is background below the band and not
> glass, and looking for "the first dark row" never finds one). Both edges are
> median-filtered and fitted low-order, because they are shallow arcs and a
> wild column is noise. A degree-4 fit to the BOTTOM edge chased its own noise
> and scalloped the band; it is degree 2.
>
> Measured result: top edge 306 under the middle rising to 314 at the sides
> (a 9px arch), bottom 460 to 466 (6px). Bare aluminium across all 17 fell from
> 341,904 pixels to 211,055 — and everything remaining is the white plastic
> disc and the glass neck, which are not the cap band. In the seam itself,
> rows 312–322 went from ~724 grey pixels to 77, and those 77 are the
> anti-aliased boundary, which has to be there.
>
> Before and after: `../web/cap-before-after.jpg`.
>
> **Everything downstream was re-rendered in the same pass** — `float/`,
> `foil/`, `tinted/`, `ledge/`, both contact sheets, `blue-crimp-detail.jpg`,
> and in `../web/` the hand composites, the spa composites, the scene plates,
> the tiles, the cluster hero and all three video pairs with their posters.
>
> ⚠️ **This needs numpy, scipy and pillow, and none of them are installed
> system-wide on this machine.** `render.py` could not run at all until a
> virtualenv was made for it. If a future session finds `ModuleNotFoundError:
> scipy`, that is why — make a venv, do not rewrite the script around it.
>
> `caps/` was deliberately NOT rebuilt. Those sheets are the exploration that
> chose the cap colour in the first place; rebuilding them would change what the
> exploration showed. They are history, not product images.

> **2026-10-09 — the mark on the label changed.** Mila went back to the
> ORIGINAL Gila, the spiky crest with the feathered mane. No vials had been
> printed yet, so the label artwork moved with the brand instead of diverging
> from it. `render.py` now stamps `mark-og.png`, which `logo/render_png.mjs`
> rasterises from `truemg-mark-brand.svg` so it cannot drift; `_archive/smooth-mark/mark-2365CD.png` (the
> smooth drawing) stays as the record of what the labels used to carry. All 17
> have been re-rendered, and so has everything downstream that contains a vial.
>
> `swap_mark` was also fixed while doing it: it resized the mark to the label
> box as an output SIZE, which stretched it about 4%. Invisible while one mark
> was in use and its proportions were baked into the master; not invisible the
> moment the mark changes shape. It fits inside the box now.

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

## cut/src/ — the master photography

Seventeen 2000x2000 photographs: one vial shot once and re-labelled seventeen
times, confirmed pixel-identical apart from the label. **Everything in this
project that shows a vial is built from these** — the renders in this folder,
the ledge product tiles, the floating set, the hand shot, the spa composites,
the cluster hero.

They are committed. They used to be gitignored and fetched from the store's
CDN on first run, which made the whole visual system depend on files that are
simultaneously the live product images in the Lapis admin. Replacing those
images could have taken the masters with them, and no vial could have been
re-rendered again — for a colour change, a mark change, a new composite —
without reshooting. 22MB is cheap against that.

## float/ — the catalog set, with a shadow

Mila pointed at a competitor's product page: the bottles there look 3D and
floating, and ours did not. `float.py` renders the difference.

What it is NOT: a size change. The uploaded sprites are 652x1589 of ink in a
2000x2000 canvas, which looks like wasted room — but the product card is
square, `object-contain` fits the square, and the vial is already at 79% of the
binding dimension. Measuring that before writing the code saved shipping a
"bigger" that delivered nothing.

What it IS: a cast shadow, in two parts. A contact pool carrying the vial's own
squashed silhouette, and a much wider, fainter ambient pool further out. Both
start a little BELOW the glass rather than at it, which is the whole trick —
touching reads as standing, a gap reads as hovering. Both lean right, because
the photographs are lit from the upper left.

The shadow has to be baked in. The uploaded product images come back from the
store CDN as RGB with the alpha flattened, so a CSS `drop-shadow` on one
outlines the white SQUARE, not the bottle. Measured, not assumed.

`float.py` also builds the marketing cluster (`web/hero-float*.jpg`): four
vials, mixed tilts, staged in depth. Tilt is where a photograph shows its
limits — the cap's ellipse and the label's wrap were fixed when the shutter
fired and cannot open to match a new angle — so the cluster stays inside about
22 degrees, where nobody reads the discrepancy.

These are upload candidates. Products are owner-only; nothing here reaches the
store without Mila uploading it.

## ledge/ — the product tiles

Mila, on the reference storefront: colour-code only the photo BACKGROUND, and
stand the vial on the spa ledge. Those are one note. Their product panel is a
tinted wash with the bottle floating on it and the tint is always the panel,
never the label — look at their related-products row, six tiles, six different
pale grounds, six identical cream labels.

`web/ledge.py` builds it. The crop is deliberately tight: counter, the lit
niche behind it, nothing else. The orchids and the monstera are the best part
of that plate and have no business in a 240px tile, where they fight the vial
and neither wins. They stay in the hero.

Order of operations is the part that is not obvious. The plate is graded FIRST
and the vial placed into it afterwards, so the colour lands on the room and
never on the white label — the thing Mila explicitly ruled out. It also means
`spa.relight` still runs against the room it was tuned against.

Two things the first pass got wrong, both fixed:

  * mixing a sage tint into a warm cream room gives OLIVE, because the cream
    is still in there fighting it. Every family came out a variant of the same
    khaki. The plate is pulled to its own luminance first, which throws the
    cream away and keeps the light, and only then colourised.
  * `spa.relight` kills 22% of the studio key, which is right for a bottle
    200px tall in a warm hero and wrong for a tile where the bottle IS the
    subject — it left the white label reading grey. `relight` and `place` now
    take a `key`, defaulting to the hero's 0.78 so the hero cannot drift.

Soft background, sharp subject: a 330px crop of the plate blown to 1200 is a
3.6x upscale, but that region is defocused stone and a glow with no detail to
lose, while the vial composites at full resolution. That is what a real
product photograph looks like anyway.

Upload candidates. Products are owner-only; nothing here reaches the store
without Mila uploading it.
