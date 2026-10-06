
---

# Two fixes

## LABS was sitting left — the cause was dead canvas, not alignment

CSS `letter-spacing` applies after the final letter too, so the rendered LABS
bitmap carried roughly **20% empty canvas on its right edge**. Scaling that whole
canvas to the wordmark's width therefore pushed the visible letters left and left
a gap under MG. `trace_labs.py` now crops each bitmap to its ink bounding box
before tracing, so LABS spans the wordmark exactly, edge to edge. Both the full
and compact cuts are rebuilt.

## Four palettes, and the real original blue

The original wordmark's blue was sampled from the source file rather than
guessed: the MG gradient runs **#2866BE → #3B7EE8**, median **#3374D7**, and the
vial label used **#2866CD**. It is a cobalt, not a teal — worth knowing before
committing, since the brief described it as teal.

| Key | Ground | Accent | Contrast | Note |
|---|---|---|---|---|
| `ink-gold` | `#0A0A0B` | `#D8B46A` | 10.04:1 | Premium, differentiated |
| `ink-teal` | `#0A0A0B` | `#45C9DB` | 10.02:1 | Teal matched to the gold's exact weight |
| `paper-gold` | `#FCFBF8` | `#9C7C34` | **3.80:1** | The brand book's paper gold. Under AA for small text |
| `paper-gold-aa` | `#FCFBF8` | `#866A2C` | 4.94:1 | Same hue one step down. Clears AA |
| `paper-teal` | `#FCFBF8` | `#0E7A8C` | 5.04:1 | Softer than the cobalt |
| `paper-blue` | `#FCFBF8` | `#2866CD` | 5.49:1 | The original direction |
| `ink-blue` | `#0A0A0B` | `#4C8BE8` | 7.09:1 | Reads tech rather than lab |

## Two things the contrast maths turned up

**The teal on ink is not a guess.** Gold measures 10.04:1 against the ink ground.
Candidate teals were measured against the same ground and `#45C9DB` lands at
**10.02:1** — so the teal carries the identical optical weight to the gold rather
than merely being a teal that looked about right. Swapping between those two
palettes changes the hue and nothing else.

**The brand book's paper gold does not clear AA.** `#9C7C34` is specified as the
"accent on paper", and against `#FCFBF8` it measures **3.80:1** — below the 4.5:1
that normal-size text needs. On this label the accent carries the strength line
and the hairline, both small. `paper-gold` is included exactly as the brand book
specifies it; `paper-gold-aa` is the same hue stepped down to `#866A2C` at
4.94:1. On screen they are nearly indistinguishable; in print the darker one
holds. **Use `paper-gold-aa` unless there is a reason not to.**

`palette-comparison.jpg` shows all four on two products. Generate any of them with
`label(..., palette="paper-teal")`; the default set stays `ink-gold` until a
decision is made.

**One thing to weigh on the white grounds:** the compliance block is set in a
muted grey at 1.9 mm. It clears contrast, but it is small type on a bright field
and will look lighter in print than on screen. If white wins, that block should
go a step darker.
