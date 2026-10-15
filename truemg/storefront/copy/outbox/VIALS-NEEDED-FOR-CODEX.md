# Vial renders still needed — 19 of 20

Checked against the live store and the Drive on 15 Oct 2026.

## Labels: nothing needed

All 40 label print files already exist in Drive — a `SIDE-` and a `TOP-` PDF for every one of
the 20 size-slots below, plus SVGs for several. Verified by listing them. Do not regenerate
labels and **do not rewrite any label text**: the compliance block is fixed and must not be
AI-generated.

## Vials: 19 needed

Sam has delivered **TMG-3RT 10MG** only. Every other photo on the store is a placeholder that
has to come out.

| # | Product (as the store shows it) | Strength on the label | SKU | Status |
|---|---|---|---|---|
| 1 | BPC-157 + TB-500 | 20MG (10+10) | TMG-BPC157TB500-20MG | needed |
| 2 | CJC-1295 (No DAC) + IPAMORELIN | 10MG (5+5) | TMG-CJC1295IPA-10MG | needed |
| 3 | EPITHALON | 10MG | TMG-EPI-10MG | needed |
| 4 | GHK-CU | 50MG | TMG-GHKCU-50MG | needed |
| 5 | IPAMORELIN | 10MG | TMG-IPA-10MG | needed |
| 6 | KLOW | 80MG blend (TB10+BPC10+GHK50+KPV10) | TMG-KLOW-80MG | needed |
| 7 | MOTS-C | 20MG | TMG-MOTSC-20MG | needed |
| 8 | NAD+ | 1000MG | TMG-NAD-1000MG | needed |
| 9 | SELANK | 10MG | TMG-SELANK-10MG | needed |
| 10 | SEMAX | 10MG | TMG-SEMAX-10MG | needed |
| 11 | SS-31 | 10MG | TMG-SS31-10MG | **needed — empty slot on the site** |
| 12 | SS-31 | 50MG | TMG-SS31-50MG | needed |
| 13 | TESAMORELIN | 20MG | TMG-TESA-20MG | needed |
| 14 | THYMOSIN ALPHA-1 | 10MG | TMG-TA1-10MG | needed |
| 15 | TMG-2TZ | 10MG | TMG-2TZ-10MG | **needed — empty slot on the site** |
| 16 | TMG-2TZ | 20MG | TMG-2TZ-20MG | needed |
| 17 | TMG-3RT | 10MG | TMG-3RT-10MG | **DONE — this is the standard** |
| 18 | TMG-3RT | 20MG | TMG-3RT-20MG | **needed — empty slot on the site** |
| 19 | TMG-BAC | 10ML | TMG-BAC-10ML | needed |
| 20 | VITAMIN B12 | 10ML | TMG-B12-10ML | needed |

**Do these three first** — they are the only size-slots on the live store with no photo at all,
so until they land, picking that strength shows a mismatched image:
SS-31 10MG · TMG-2TZ 10MG · TMG-3RT 20MG

## Format

Match Sam's TMG-3RT 10MG exactly. Two things matter:

- **The cutout, transparent background, square.** His is 1254x1254 RGBA. This is the one the
  storefront needs — product cards sit it on a tinted background, so any baked-in backdrop
  shows as a box.
- The marble lifestyle shot is a separate, optional deliverable. Nice for marketing, wrong for
  a product card.

## What the label on the render has to show

Observed on Sam's TMG-3RT 10MG, which is the reference:

- Compound name in blue, strength beneath it in black
- `TRUE MG LABS` set vertically up the right side of the label
- A large pale ghosted lizard filling the label behind the mark
- The solid blue lizard mark lower left
- `NOT FOR HUMAN CONSUMPTION` / `RESEARCH USE ONLY`, two lines
- A DNA-helix motif down the right edge
- White flip-top cap over a blue crimp
- On the lifestyle shot only, BATCH and LOT numbers set vertically

**Naming:** TMG-BAC must never be called bacteriostatic water, anywhere. Use the store names in
the table above, not the underlying compound names, for TMG-2TZ, TMG-3RT and TMG-BAC.

## Where finished files go

Sam's shared folder, `LOGOS/vial/Labels`:
drive.google.com/drive/folders/1RnTchA_5Tiz3tk0KEAhYu85-R3QKdlxq

That folder is currently shared "anyone with the link — Viewer", so only Sam can add to it.
Per Mila, this is the **only** source for vial artwork — nothing is pulled from the repo renders
or the Desktop folder.
