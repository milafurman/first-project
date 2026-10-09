# TrueMG logo — production files

Real vector. Every file here is SVG with live paths, not a traced-looking raster
in an SVG wrapper. Scales to any size, recolours by editing one attribute, and
foil-stamps, embosses and screen-prints because it is flat and single-colour.

**The brand colour is `#2365CD`.** It is sampled from the TRUEMG Labels artwork
in Canva, where it is the literal fill on the product-name text, so the printed
label and everything here are the same blue by construction. On a dark ground
the accent lightens to `#65A0F5`, because `#2365CD` on near-black does not hold.

> An earlier version of this file described a **gold** palette (`#D8B46A` /
> `#9C7C34`) as the brand and said "the blue is gone". That was true for about
> a day and then stopped being true. Every file here is blue now. If you find a
> gold TrueMG asset anywhere, it predates this and should not be used.

## The mark

There were two different Gila drawings loose in this project, and for a while
the logo files and the product disagreed about which one was the logo:

- a head with a **spiky crest** and a fine feathered mane — still on the
  storefront's favicon, kept at `../marks/mark-original.png`
- a **smoother head** with bolder strokes and a heavier ring — on all seventeen
  vials and in the Canva label pages

As silhouettes they overlap 53%, so they are two drawings, not two exports of
one.

**Mila picked the FIRST — the spiky one — on 2026-10-09**, and because no vials
had been printed yet the label artwork moved with it rather than diverging from
it. `../marks/mark-original.png` is the master. The smooth drawing is kept at
`../vials/mark-2365CD.png` as the record of what the labels used to carry.

> An earlier version of this file said the second drawing was the master and
> the storefront favicon had been changed to match. That was true for two days.
> If you find a smooth-crested TrueMG mark anywhere outside
> `truemg-mark-smooth-*.svg`, it predates this and should not be used.

| File | Fill | Use |
|---|---|---|
| `truemg-mark-brand.svg` | `#2365CD` | The default |
| `truemg-mark-ink.svg` | `#0A0A0B` | On paper, and for foil, emboss or one-colour print |
| `truemg-mark-paper.svg` | `#FCFBF8` | Knocked out of a dark photograph |
| `truemg-mark-current.svg` | `currentColor` | For CSS — inherits from its container |

`trace_original.py` rebuilds all four from the master and writes the CANONICAL
filenames, so `build_lockup.py` and `render_png.mjs` follow the mark without an
edit and cannot quietly disagree with it. Five paths, 15KB, 98.06% silhouette
match against the master.

That master is a 900px screenshot — soft edges, JPEG mush, paper texture in the
ground — which is why it is traced rather than filtered. Filtering adds no
detail that is not there; unsharp masking a blurry edge only haloes it. The
trace takes the inked area from 22.0% fuzzy-edge pixels to 1.9%, and that 1.9%
is real anti-aliasing at render time rather than blur baked into a file.

`trace_mark.py` still builds the smooth drawing, under `-smooth-` names, so the
two can sit side by side without one overwriting the other.

### Separating ink from ground

The two masters need different methods and this is the whole difference between
the scripts. The vial master is a PNG with a real alpha channel, so its
silhouette is simply the alpha. This one is flat RGB on a mottled off-white with
no alpha, so the ink is separated by COLOUR — blue minus the stronger of red and
green. Brightness would not do: it would eat the white shapes INSIDE the mark —
the eye, the gap under the jaw, the splits between the mane strokes — because
those are the same white as the background.

### Tracing notes

Upsample the master's **anti-aliased alpha** and threshold after, never the
other way round. Enlarging an already-hard-edged mask magnifies its staircase
and potrace then spends hundreds of segments tracing the steps: that route
produced a 128KB file at *worse* fidelity than the current 10KB one. 2x
upsample, `-a 0.9`, `-u 1`. 4x buys 0.14% more fidelity for 2.5x the bytes,
which the header's CSS budget cannot afford.

## The wordmark

Traced from the alpha channel of the original PNG, so these are the **real
letterforms**, not a substitute typeface. The stencil cuts on the T, R, U and E
are preserved exactly.

| File | Use |
|---|---|
| `truemg-wordmark-onink.svg` | TRUE in `#EDEBE6`, MG in `#65A0F5` |
| `truemg-wordmark-onpaper.svg` | TRUE in `#0A0A0B`, MG in `#2365CD` |
| `truemg-wordmark-ink.svg` / `-paper.svg` / `-current.svg` | Single colour, for stamping and CSS |

`_source-wordmark.png` is the original, kept for reference.

## What still needs a human

The paths are clean but they were traced, not drawn. Before this goes on a
printed label, an illustrator should open it once and true up the curves by
hand — particularly where the mane strokes meet the jaw. It is production-ready
for screen today.

---

# TrueMG **Labs** — the full lockup

| File | Use |
|---|---|
| `truemg-labs-onink.svg` | TRUE paper, MG `#65A0F5`, hairline, LABS tracked to the full wordmark width |
| `truemg-labs-onpaper.svg` | The same on a light ground, MG `#2365CD` |
| `truemg-labs-compact-onink.svg` / `-onpaper.svg` | Tighter tracking, no rule. **Use below ~200px** and on the vial label |
| `truemg-labs-ink.svg` / `-paper.svg` | One colour, for foil, embossing and single-colour print |

`relabs.py` re-spaces LABS in all six. (`trace_labs.py` is the superseded
original, kept for provenance; it cannot run and it is what produced the
stretched LABS.)

## Why LABS is not in the wordmark's typeface

It cannot be. The original wordmark uses a very wide chamfered face that is not
Helvetica, Archivo, Saira, Chakra Petch or Oxanium — all were set beside it and
compared, and none match. It is not in the Canva account either, so the source
file could not be recovered.

So LABS is deliberately **not** trying to match. It is set in Archivo Black,
small and letterspaced, which is how a descriptor is normally handled: the
difference in face reads as hierarchy rather than as a mistake. The hairline
between them makes that reading explicit.

**If the original typeface is ever identified, this is a ten-minute change** —
set LABS in it, trace, and re-run. Worth asking whoever made the original
wordmark.

## Tracking is set twice, on purpose

At full width the letterspacing is extreme, which is correct at hero size and
unreadable at header size. The compact cut tracks about half as far. Both are
traced from rendered type, so neither depends on a font being installed.

## The lockups

`build_lockup.py` builds four: with the Gila mark and without, each on a light
and a dark ground.

| File | Use |
|---|---|
| `truemg-lockup-header.svg` | **The site logo.** Mark + wordmark + LABS, light ground |
| `truemg-lockup-onink.svg` | The same on a dark ground |
| `truemg-lockup-web.svg` | Wordmark and LABS, no mark |
| `truemg-lockup-web-onink.svg` | The same on a dark ground |

The markless pair exists because of a constraint that no longer applies — see
the customCss note below. It is kept for anywhere the mark would be redundant
or too small to read, not because the mark is barred from the site.

Each has a `.min.svg` beside it, produced by svgo at `--precision=0`. A
hand-rolled regex that tried to do the same thing produced a file that rendered
nothing at all, so the optimizer does this, not a script.

`render_png.mjs` renders four transparent PNGs at 1200px wide, roughly 3x the
header's rendered size, plus `lockup-preview.jpg`:

| File | |
|---|---|
| `truemg-lockup-mark-light-1200.png` | **The one in the Lapis admin's Logo slot** |
| `truemg-lockup-mark-dark-1200.png` | the same on a dark ground |
| `truemg-lockup-light-1200.png` / `-dark-1200.png` | the markless pair |

They used to be exported by hand, which is exactly how they came to be carrying
the old drawing and the stretched LABS after the SVGs had already been fixed.

The Lapis admin takes one logo file and uses it in both the header and the
footer. The footer is near-black and the logo is dark ink, so the theme lays a
white rounded plate behind it rather than inverting it.

### The customCss route, and why it is retired

The logo lives in **Design studio -> Manual -> Logo**, as an upload. Before that
was found, the header was driven from `customCss` instead, and the notes below
are kept because the sanitizer findings still hold for anything else inlined
there.

There is no copy key for the logo on any template — only `logoScale`. Two
routes were tested against the CSS sanitizer:

- `content: url(...)` and `background-image: url(...)` — **every** external URL
  is rewritten to `url(#)`, in every property. No image can be pulled in from
  outside, from jsDelivr or anywhere else.
- A base64 `data:` URI **does** survive the sanitizer, so the lockup can be
  inlined into `customCss`.

A raw (non-base64) `data:image/svg+xml;utf8,<svg…>` URI loses its angle brackets
to the sanitizer. Base64 is the only form that survives.

`customCss` is capped at 10,000 characters, and that cap is why the markless
lockup exists at all: with the Gila the file minifies to 9,464 characters of
base64 and the rest of the stylesheet no longer fits; without it, 4,148. Since
the logo is an upload the cap no longer applies to it, and whether the mark
sits beside the wordmark is a design choice rather than a platform limit. The
logo rule has been removed from `customCss` accordingly.

## favicon/

There was no favicon in this repo, which is why the one on the store is
whichever drawing was last uploaded by hand. `favicon.py` makes a real one
from the spiky mark.

A favicon is 32 logical pixels wide, and the mark's mane is fine separated
strokes. Shrunk straight down they collapse into a blue smear — not an ugly
smear, an unidentifiable one. So there are two cuts and the choice is real:

  * KNOCKED OUT — mark in white on a solid brand-blue rounded square. One
    shape, maximum contrast, still legible at 16px, and it holds its own in a
    row of twenty tabs. This is the default, because being FOUND is the job.
  * PLAIN — blue mark on white. Prettier large, invisible small against a
    light browser chrome.

The 180px cut is opaque and square-cornered on purpose: iOS strips alpha,
composites what is left onto black, and applies its own corner radius.
