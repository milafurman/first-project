# Archive — superseded logo work

Nothing in here is live. Nothing in here is referenced by any script that
still runs. It is kept because a brand's rejected directions are evidence of
why the chosen one is right, and because throwing them away means re-arguing
the same decisions in six months.

Archived 11 Oct 2026, when Mila asked for every other logo to be put away so
only the current mark is loose in the tree.

## What IS current, for contrast

| File | What |
|---|---|
| `../marks/mark-original.png` | **The master.** The spiky-crest Gila, as drawn. Everything downstream traces from this one file |
| `../logo/trace_original.py` | Traces it to vector |
| `../logo/truemg-mark-*.svg` | The mark, four colourways |
| `../logo/truemg-lockup-*.svg` | Wordmark + mark lockups |
| `../vials/mark-og.png` | The raster stamped on all 17 labels |

## `rejected-marks/` — the directions not taken

Eight Gila concepts, all gold on ink, from the round that chose the mark.
`marks/README.md` has the original reads on each; the short version:

| File | Why it lost |
|---|---|
| `profile.jpg` | Handsome, but the long snout reads monitor lizard, not Gila |
| `blunt.jpg` | Was the recommendation. Short snout, deep jaw. Lost to the stencil line |
| `dorsal.jpg` | Top-down. Symmetrical and striking, but reads as a mask and the eyes vanish |
| `regal-head.jpg` | Heraldic bust, jewelled goldwork. Too much for a 32px favicon |
| `regal-coin.jpg` | The bust struck on a coin. Beautiful, same problem |
| `sten-direct.jpg` | The stencil line — the ANCESTOR of the current mark. Earlier, looser |
| `sten-heraldic.jpg` | Closest of the three to what shipped. The current mark is this idea, redrawn |
| `sten-reduced.jpg` | The one-colour reduction of it |
| `marks-sheet.jpg`, `regal-sheet.jpg`, `stencil-sheet.jpg` | The comparison sheets, with size ladders |

Worth knowing: the current mark is not a rejection of this set, it is the end
of the stencil branch. `sten-heraldic.jpg` and the live mark are the same
animal in the same pose.

## `smooth-mark/` — the mark the labels used to carry

`mark-2365CD.png` is the SMOOTH-crest drawing, in the old brand blue
`#2365CD`. It was on all 17 vial labels until 9 Oct 2026, when Mila went back
to the original spiky drawing. The two overlap only 52% as silhouettes, so it
is a genuinely different drawing rather than a re-export.

`trace_mark.py` traced it. Its master path is rewritten to point beside it, so
it is readable, but it is not wired into anything and should not be run.

It was also still on the **Canva label artwork** — all 20 pages — until
12 Oct 2026, three days after the mark was chosen, because nothing syncs this
repo to Canva. Replaced there now; see `../logo/README.md`.

It may still be on **product images already uploaded to the store**, which were
exported before the change. Anything re-rendered from `../vials/mark-og.png`
carries the correct spiky mark.

## `superseded/`

| File | Why |
|---|---|
| `trace_labs.py` | Superseded by `../../logo/relabs.py`, which fixed its LABS letter-spacing (it forced LABS to span the full wordmark, giving roughly 8em of tracking). It also reads a `vec/` directory that no longer exists, so it has not been runnable for some time |
| `gila-mark.html` | A dark specimen page for the GOLD mark directions. The brand went blue; `../logo/lockup-preview.jpg` is the current specimen |
