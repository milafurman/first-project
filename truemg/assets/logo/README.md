# TrueMG logo — production files

Real vector. Every file here is SVG with live paths, not a traced-looking raster
in an SVG wrapper. Scales to any size, recolours by editing one attribute, and
foil-stamps, embosses and screen-prints because it is flat and single-colour.

## The mark

| File | Fill | Use |
|---|---|---|
| `truemg-mark-gold.svg` | `#D8B46A` | On the ink ground. The default |
| `truemg-mark-ink.svg` | `#0A0A0B` | On paper, and for foil, emboss or one-colour print |
| `truemg-mark-paper.svg` | `#FCFBF8` | Knocked out of a dark photograph |
| `truemg-mark-current.svg` | `currentColor` | For CSS — inherits the colour of its container |

Three paths, 10KB. Verified legible at 120, 76 and 44px; tight but readable at
28; at 16px it is a dense shape rather than a lizard, so a favicon may want the
ring alone or the head without the crest. That is the one open refinement.

## The wordmark

Traced from the alpha channel of the original PNG, so these are the **real
letterforms**, not a substitute typeface. The stencil cuts on the T, R, U and E
are preserved exactly.

| File | Use |
|---|---|
| `truemg-wordmark-onink.svg` | TRUE in `#EDEBE6`, MG in `#D8B46A`. The default |
| `truemg-wordmark-onpaper.svg` | TRUE in `#0A0A0B`, MG in `#9C7C34` (the deeper gold holds contrast on paper) |
| `truemg-wordmark-ink.svg` / `-paper.svg` / `-current.svg` | Single colour, for stamping and CSS |

The blue is gone. MG now carries the gold, which keeps the brand rule intact:
one accent, once per view.

`_source-wordmark.png` is the original, kept for reference.

## Lockup
Mark then wordmark, baselines aligned, mark height roughly 1.6x the cap height,
gap roughly one mark-width. `lockup-preview.jpg` shows it on both grounds and at
header scale.

## How it was made
The chosen direction was generated as a raster, then vectorised with potrace at
8x upsample with a corner threshold of 0.9 — low enough to keep the stencil's
sharp tapered points rather than rounding them off. The wordmark was traced from
its alpha channel, which is exact. Both are reproducible from
`truemg/assets/marks/` and the scripts used.

## What still needs a human
The paths are clean but they were traced, not drawn. Before this goes on a
printed label, an illustrator should open it once and true up the curves by
hand — particularly where the crest tapers meet the jaw. It is production-ready
for screen today.
