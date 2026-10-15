# The three size photos — why they still need a human hand (15 Oct 2026)

Mila asked me to do them. I got into the admin, found exactly what was missing, and could
not complete the upload. This records how far it goes and where it stops, so nobody burns
another hour on it.

## What is actually missing — verified on all three

These are the only multi-size products. In every one it is the **10MG** row whose photo slot
is empty; the larger size already has a photo.

| Product | Sizes | 10MG photo | Larger size | Stock |
|---|---|---|---|---|
| SS-31 | 10MG / 50MG | **empty** | present | 0 / 0 |
| TMG-2TZ | 10MG / 20MG | **empty** | present | 0 / 0 |
| TMG-3RT | 10MG / 20MG | **empty** | present | 0 / 0 |

Lapis states the rule under that section: *"Give each size its own photo — the storefront
swaps the product image when a shopper picks that size. Sizes without a photo use the main
product picture."* So the defect is not a wrong card image; it is that picking 10MG does not
swap to the 10MG vial.

## SUPERSEDED 15 Oct 2026 — do NOT use the renders in this repo

Mila: **"Sam created the vials. Use the files in the Drive Sam gave us. Do not use any other
location to pull or upload from. We are not using the ones you created."**

So `truemg/assets/vials/tmg-*.png` are **not** the artwork for these slots, and neither is the
Desktop `TRUEMG UPLOAD` folder — all 17 PNGs in it are byte-identical to those renders.
The only source for vial artwork is Sam's shared folder:
`drive.google.com/drive/folders/1RnTchA_5Tiz3tk0KEAhYu85-R3QKdlxq` -> `vial/Labels`.

Sam's label is a different design: wordmark reads TRUE MG **LABS**, a large ghosted lizard
watermark fills the label behind the mark, a DNA-helix motif runs down the right edge, the
newer cleaner lizard, a deeper blue cap, and the lifestyle shot carries BATCH 60392 / LOT 60393.
None of that is in the repo renders.

As of 15 Oct his folder holds **one** product in two formats — TMG-3RT 10MG as a transparent
cutout (the format the storefront needs) and as a marble lifestyle shot — plus a one-page
labels PDF. The remaining nineteen size-slots have no Sam artwork visible to us; the folder is
view-only, so he may have more that is simply not shared.

**Every one of the 17 product photos currently live on the store came from the repo renders.**
If his set replaces them, that is 17 products / 20 size-slots, not three.

## Why it cannot be automated

The product page carries three file inputs: the Pictures "Add" (inside a label), **one shared
input for the whole Sizes section**, and the COA upload. The sizes input is not bound to a row.
Each row has its own button — `aria-label="Add photo for 10MG"` — and clicking it is what tells
the component which size the next file belongs to. That click opens a **native macOS file
dialog**, which cannot be driven from here and would block the browser if opened.

Setting the file on the shared input directly does not work either. `file_upload` reported
success, then the input's `files.length` read back as **0** and the 10MG slot was still empty —
the component discards a file it was not expecting.

Two separate obstacles, worth not confusing:
1. The Desktop folder is outside this session's readable paths (`/add-dir` would fix that).
2. The size-photo input rejects a programmatic file. **This is the real blocker, and where the
   files live makes no difference to it.**

Nothing was saved. The input I had temporarily unhidden to test was restored by reloading the
page; descriptions and every other field were verified intact afterwards.

## The human version — about thirty seconds per product

Products -> Catalog -> the product -> scroll to **Sizes, pricing & stock** -> click the dashed
square next to **10MG** -> pick the matching file -> **Save**. Repeat for TMG-2TZ and TMG-3RT.

Worth checking while in there: the larger size's existing photo. The thumbnails are too small
to read the printed strength, and we only hold one render per product, printed 10MG — so if a
50MG/20MG slot is showing 10MG artwork, that is a second thing to fix and would need new renders.
