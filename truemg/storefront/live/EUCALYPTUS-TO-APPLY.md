# The eucalyptus site change — built, previewed, NOT saved

> **See `DO-THIS-IN-LAPIS.md` for the keystroke version**, which also covers the
> hero URLs. The save was refused twice; this file is the background.

Mila said "go ahead" on 12 Oct 2026. Everything is ready. The save itself was
**refused by this session's safety rule** (it classes a live-store write as a
production deploy), so the last step needs either Mila's permission or Mila's
hands.

**Nothing on the live store has changed.** The old look is still up, and
`customCss-2026-10-12.css` in this folder is the backup of it.

## It was validated first

`preview_design_change` returned `ok: true`, with **no refused rules** — all 42
lines survive the sanitizer, including the seventeen URL-keyed card rules. It
reported one automatic readability adjustment, on `mutedForeground`, which Lapis
nudges for contrast. 3,679 characters of the 10,000 budget.

## The two halves

**1. The palette** — set these in Design studio → Colors:

| Key | Value | What it is |
|---|---|---|
| `background` | `#EEF2EE` | the eucalyptus page |
| `card` | `#FCFDFB` | near-white cards, so they lift off the green |
| `secondary` | `#E9EDE9` | was a cool grey; now green-neutral |
| `border` | `#DCE5DC` | |
| `muted` | `#E4EBE4` | |
| `mutedForeground` | `#6E7A6E` | Lapis will adjust this for contrast |
| `accent` / `themeAccent` | `#1c8cd0` | **unchanged** — the brand blue stays |
| `themeAccentDeep` | `#0f547e` | **unchanged** |
| `primary` | `#0a0a0b` | **unchanged** |

**2. The stylesheet** — `customCss-eucalyptus.css` in this folder, pasted whole
into Design studio → Custom CSS. Rebuild it any time with
`make-eucalyptus-css.py`, which derives it from the backup plus the approved
tints rather than being hand-maintained.

⚠️ **Saving in Design studio wipes customCss.** Do the colours and the CSS in
the same save, or do the colours first and paste the CSS second.

## What changes, and what does not

Changed: the page ground, the section bands (the blue-white and cream blocks go
green), the header's hairline, the two dark blocks from navy `#0A192F` to the
mock's green-black `#202A22`, and **the field behind each bottle, now one colour
per compound instead of one pale blue for all seventeen.**

Not changed: the brand blue, the logo, the type, the layout, every word of copy,
and the coming-soon curtain — which stays up, so nobody sees any of this until
Mila drops it.

## The tint strength was corrected before previewing

The first build washed each field 45% toward white, carried over from the
approved sheet where the colour mostly came from a drawn label chip. On the real
cards the labels are **white photographs**, so a 45% wash nearly vanished.
Checked against the actual renders — `../../assets/web/card-field-test.jpg`
shows full tint against 15% and 45% — and the full tint is what shipped into the
preview.

## The trap, restated

Each card rule hangs off that product's URL. **TMG-2TZ** (`/catalog/tirzepatide-k8ms`)
and **TMG-BAC** (`/catalog/bacteriostatic-water-tzbc`) are both slated to change
under `1F`. When they do, re-point those two lines or those two cards silently
fall back to `#F1F5F1`. The fallback was deliberately changed from the old blue
to a green-white so that a miss degrades quietly instead of looking broken.
See `CARD-TINTS.md`.
