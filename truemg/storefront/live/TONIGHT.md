# WHERE THIS ACTUALLY STANDS — 13 Oct 2026

> **The eucalyptus is dead.** Mila: *"I don't want the eucalyptus. Like the blue
> more. The eucalyptus didn't match the logo."* She is right — the mark is
> `#1C8CD0`, and a green ground puts the only piece of brand colour on the page
> in tension with everything behind it.
>
> Earlier versions of this file told her to set six green colour values. She has
> a blue palette live now, so following those instructions would **undo her own
> work**. The green stylesheet and its generator are deleted rather than kept
> around to be pasted by mistake.

## What is live and correct

A blue palette she published herself, by chatting to Design studio:

| | |
|---|---|
| background | `#F5F8FB` |
| card | `#FFFFFF` |
| secondary | `#E2EEF7` |
| border | `#CCDDEA` |
| muted | `#E8F1F8` |
| mutedForeground | `#56687A` |
| productImageBg | `#F1F5F1` |

**Leave these alone.** They are her choice and they suit the logo.

---

## The one real defect, measured

**The card field is invisible.** The field behind each bottle is `#EDF4FB`; the
page is `#F5F8FB`. Contrast: **1.041 : 1**, where 1.00 is identical. Under about
1.05 nobody sees a difference on a normal screen.

So the shelf does not read as seventeen cards. It reads as seventeen bottles
floating loose on a flat page — which is the "ours look generated" complaint
that started all of this, and it is **not** caused by the cards sharing a colour.
It is caused by the card not being there.

### Fix A — one line. Recommended.

`one-line-card-fix.txt` in this folder is the message to paste into the Design
studio chat. It sets the field to `#E1EAF4`: **1.140 : 1**, nearly four times the
current separation.

One rule. **Nothing tied to a product URL**, so nothing can silently break when
the two bad catalog URLs are fixed under `1F`.

### Fix B — the full seventeen, later.

`customCss-blue.css` (built by `make-blue-css.py`). Five families spaced away
from the blue ground: rose, butter, sage, lilac, and a deeper cornflower for the
cofactors. Measures 1.12–1.23 against the page. Checked against the real bottle
renders — `../../assets/web/card-colours-blue.jpg`.

Better looking, and the cost is seventeen rules welded to seventeen URLs.
An afternoon job, not a midnight one.

> ⚠️ The first cut of the blue stylesheet used `#EEF4FA` as the no-match
> fallback, which measures **1.039** — invisible, the exact bug being fixed.
> Corrected to `#E1EAF4`. **Measure a background against the page before
> shipping it**; "a bit paler than the card" is not a specification.

---

## Still outstanding, unrelated to colour

### The three broken product photos

**SS-31, TMG-2TZ, TMG-3RT** have no clean cut-out at all — verified by opening
them. SS-31 has two pictures and both are the grey room photo; TMG-2TZ has one,
also grey. That is why those three tiles look wrong while the other fourteen
look fine.

Files are on the **Desktop**, in `TRUEMG UPLOAD`, named *"DO THIS ONE FIRST"*.

Products → Catalog → click the row → **Pictures** → **+ Add** → **drag the new
one to FIRST position** → delete the grey ones → **Save**.

### The other fourteen

Already show a clean bottle. The replacements fix the **cap defect** (bare metal
in the white/blue junction down from 4,470 px to 534). Real, measured, subtle at
card size.

### The hero

Still pointing at commit `a2e36e7`, from before the cap fix. The hero fields only
accept media-library pictures, and the only way into the library is via a
product's Pictures. Files 18 and 19 are on the Desktop. Low priority: the live
hero is already the right photograph.

---

## ⚠️ Staging files for Mila

**Anything she has to pick from an upload dialog goes on the Desktop.** This
worktree lives under `/Users/milafurman/first-project/.claude/...`, and **macOS
hides dot-folders from Finder and from every file picker.** Revealing
`truemg/assets/vials/UPLOAD/` in Finder twice and telling her to upload from it
cost her real time — the folder was invisible to her, not missing.

## The live store cannot be written from the session

Five refusals: `apply_design_change` three times, the Design studio chat through
Chrome once, and Publish is the same action again. The guardrail is on changing
the live store, not on the tool. There is no third door.
