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
one. Mila picked the second. `../vials/mark-2365CD.png` is the master.

| File | Fill | Use |
|---|---|---|
| `truemg-mark-brand.svg` | `#2365CD` | The default |
| `truemg-mark-ink.svg` | `#0A0A0B` | On paper, and for foil, emboss or one-colour print |
| `truemg-mark-paper.svg` | `#FCFBF8` | Knocked out of a dark photograph |
| `truemg-mark-current.svg` | `currentColor` | For CSS — inherits from its container |

`trace_mark.py` rebuilds all four from the master. Three paths, 10KB, 99.66%
silhouette match. **The favicon is still the other drawing** — it is an upload
in the Lapis admin, which this integration cannot reach, so it needs replacing
by hand with `truemg-mark-brand.svg`.

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

`build_lockup.py` builds four, and they split on one rule: **the Gila mark
appears on the browser tab and on the vial, and nowhere on the site itself.**

| File | Use |
|---|---|
| `truemg-lockup-web.svg` | **The site header.** Wordmark and LABS, no mark |
| `truemg-lockup-web-onink.svg` | The site footer |
| `truemg-lockup-header.svg` | Mark + wordmark, light ground. Print, Canva, decks |
| `truemg-lockup-onink.svg` | The same on a dark ground |

Each has a `.min.svg` beside it, produced by svgo at `--precision=0`. A
hand-rolled regex that tried to do the same thing produced a file that rendered
nothing at all, so the optimizer does this, not a script.

`truemg-lockup-light-1200.png` and `-dark-1200.png` are transparent PNGs of the
**web** lockup at 1200px wide, roughly 3x the header's rendered size. **These
are the ones to upload in the Lapis admin.** `render_png.mjs` makes them, and
`lockup-preview.jpg`, from the SVGs — they used to be exported by hand, which is
exactly how they came to be carrying the old drawing and the stretched LABS
after the SVGs had already been fixed.

### Why the header cannot be done from the storefront integration

There is no copy key for the logo on any template — only `logoScale`. The image
is an admin upload. Two routes were tested against the CSS sanitizer:

- `content: url(...)` and `background-image: url(...)` — **every** external URL
  is rewritten to `url(#)`, in every property. No image can be pulled in from
  outside, from jsDelivr or anywhere else.
- A base64 `data:` URI **does** survive the sanitizer, so the lockup can be
  inlined into `customCss`.

A raw (non-base64) `data:image/svg+xml;utf8,<svg…>` URI loses its angle brackets
to the sanitizer. Base64 is the only form that survives.

`customCss` is capped at 10,000 characters. That cap is the other reason the
site header carries the markless lockup: with the mark it minifies to 9,464
characters of base64 and the rest of the CSS no longer fits. Without it, 4,148,
which leaves room. Both go away the moment the PNGs are uploaded in the admin.
