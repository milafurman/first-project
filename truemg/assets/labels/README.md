
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

| Key | Ground | Accent | Reads as |
|---|---|---|---|
| `ink-gold` | `#0A0A0B` | `#D8B46A` | Premium, differentiated. Almost no peptide vial is black |
| `paper-blue` | `#FCFBF8` | `#2866CD` | The original direction. Clinical, conventional pharma |
| `paper-teal` | `#FCFBF8` | `#0E7A8C` | Softer and warmer than the cobalt, still clearly clinical |
| `ink-blue` | `#0A0A0B` | `#4C8BE8` | The blue on black. Striking, but reads tech rather than lab |

`palette-comparison.jpg` shows all four on two products. Generate any of them with
`label(..., palette="paper-teal")`; the default set stays `ink-gold` until a
decision is made.

**One thing to weigh on the white grounds:** the compliance block is set in a
muted grey at 1.9 mm. It clears contrast, but it is small type on a bright field
and will look lighter in print than on screen. If white wins, that block should
go a step darker.
