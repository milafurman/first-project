# The 33 dropped rules — recoverable, and worth resending

Austin re-opened the allowlist and asked us to resend what was dropped:
*"We didn't touch your saved CSS, so please have your agent resend the dropped
rules; anything still refused will say exactly why."*

## They were nearly lost

The rules themselves were **not** written into `LAPIS-CSS-LIMITS.md` — only the
*property names* were. The stylesheet was rewritten against the allowlist rather
than archived, and `storefront.css` was then deleted in the 13 Oct cleanup.

They survive in history only, at the commit **before** the rewrite:

```
git show 0b34c29^:truemg/storefront/storefront.css
```

Extracted to **`customCss-pre-allowlist-10-oct.css`** in this folder so it stops
depending on anyone remembering that commit hash.

## What is in there worth having back

**The full-bleed section bands — this one broke the live page, not just degraded
it.** From the rewrite's own commit message: the trick was
`box-shadow: 0 0 0 100vmax <colour>` clipped back by `clip-path`. `box-shadow`
survived the tightening and `clip-path` did not, so the shadow painted over its
neighbours and **wiped out the navy "Anyone can fill a vial" band — white text on
pale blue, unreadable.** It was replaced with tinted rounded panels because
nothing else was available: the sections are `max-w-7xl` centred containers, and
bleeding one needs `clip-path`, `overflow`, or a `-50vw` margin, and margins were
capped at -200px.

**`clip-path` is allowed again.** So full-bleed bands can come back, and the
rounded-panel workaround can go.

Also recoverable: card and button `transition`s, the header's `backdrop-filter`
reset, and `position: relative/absolute` on the nav links.

## One rule must be REWRITTEN, not resent

The nav underline used `transform: scaleX(0)` with a transform transition.
Austin, specifically: *"For a nav underline that grows on hover, animate width
from 0 to 100% instead of using scaleX(0)."* So that rule needs rebuilding, not
restoring.

## The new limits to build against

| Property | Limit |
|---|---|
| `position` | `relative`, `absolute`, `sticky` — **not** `fixed` |
| offsets | within 400px |
| `z-index` | up to 9 |
| `clip-path` | shapes allowed |
| `overflow` | allowed |
| backdrop blur | up to 40px |
| `transition` | up to 3 s |

The old `clip-path: inset(0 -100vmax)` exceeds the 400px offset limit and will
need re-expressing.

## Method — do not guess

Dry-run every rule through `preview_design_change` and read the refusal list
before handing Mila anything. Refusals now carry reasons and also appear under
**Settings → Connected agents**. Help guide 72 keeps a dated changelog.

⚠️ And carry `!important` through on anything replacing an existing rule — that
is what killed the card-colour change.

**Status: not started.** This is agent work, not Mila's.
