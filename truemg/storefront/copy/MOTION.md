# Motion — newly possible as of 13 Oct 2026

**Until today the stylesheet could not move.** `transition`, `transform`,
`clip-path`, `overflow` and `backdrop-filter` were all refused by the Lapis
allowlist, which is why the site is completely static. Austin re-opened them:

| | Limit |
|---|---|
| `transition` | up to 3 s |
| `transform` | allowed (was capped) |
| `position` | relative / absolute / sticky |
| offsets | within 400px |
| `z-index` | up to 9 |
| `clip-path` | shapes |
| backdrop blur | up to 40px |

So "as dynamic as possible" is now a real option rather than a wish. **Every rule
below must still be dry-run before it ships** — the allowlist moved twice
already.

## The principle: it moves like the animal

Nothing snaps. Nothing bounces. Nothing attention-seeks. The voice is
*unhurried* (see `VOICE.md`), so the motion is slow, weighted and gets out of
the way. 240–400ms, ease-out, never a spring.

**If an animation makes someone look at the animation, it is wrong.**

## Worth doing, in order of payoff

**1. Card lift on hover.** The grid is seventeen static tiles. A 2–3px rise plus
a deepened shadow over ~300ms makes it feel like an interface rather than a
printout. This existed before the allowlist ate it — the rule is in
`customCss-pre-allowlist-10-oct.css`.

**2. The nav underline.** Austin's own note: animate `width` from 0 to 100%,
**not** `scaleX(0)`. The old rule used scaleX and must be rebuilt, not restored.

**3. The vial, on the product page.** A slow 1.02 scale on hover. The renders
are 2000px so there is resolution to spare. This is the one place a little
flourish is earned, because the bottle is the product.

**4. Full-bleed section bands — the real win.** These were lost when `clip-path`
was refused, and the current rounded panels are a fallback, not a choice. See
`RESEND-THE-33-RULES.md`. Note the old `inset(0 -100vmax)` exceeds the new 400px
offset cap and needs re-expressing.

**5. Reveal on scroll.** Sections fading up 12px as they enter. Tempting, and
**deliberately last** — it is the easiest thing to overdo and the fastest way to
make a calm site feel like a pitch deck. If it ships, 1 section at a time, never
staggered children.

## Never

- Anything that loops forever in the corner of the eye.
- Carousels that advance on their own.
- Countdown timers (banned on brand grounds as well — see `VOICE.md`).
- Parallax on the hero. The hero carries the compliance line; it does not move.
- `prefers-reduced-motion` must be honoured on everything here.
