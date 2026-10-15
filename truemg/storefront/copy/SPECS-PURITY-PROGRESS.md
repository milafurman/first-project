# Purity line replacement — COMPLETE, all 17 verified (15 Oct 2026)

Mila: *"Replace the purity line and do the citations."* The purity half is done. Citations are
still waiting on a scope decision — see the bottom.

**Replacement:** `≥99% (validated by HPLC/COA)` → **"Reported on the certificate issued for your
lot"**. Where a Solubility field said "bacteriostatic water" it became **TMG-BAC** in the same
pass.

## Verified by reloading each product page and reading the field back

Not by the save banner — that banner appears on no-op saves on this platform and cannot be
trusted. Every row below was confirmed on a fresh page load.

| # | Product | Purity now | Solubility now |
|---|---|---|---|
| 1 | EPITHALON | certificate line | Soluble in water and in TMG-BAC |
| 2 | GHK-CU | certificate line | Soluble in water |
| 3 | BPC-157 + TB-500 | certificate line | Soluble in water / TMG-BAC |
| 4 | CJC-1295 (No DAC) + IPAMORELIN | certificate line | Soluble in water / TMG-BAC |
| 5 | IPAMORELIN | certificate line | Soluble in water / TMG-BAC |
| 6 | KLOW | certificate line | Soluble in water / TMG-BAC |
| 7 | MOTS-C | certificate line | Soluble in water / TMG-BAC |
| 8 | NAD+ | certificate line | Soluble in water |
| 9 | SELANK | certificate line | Soluble in water |
| 10 | SEMAX | certificate line | Soluble in water |
| 11 | SS-31 | certificate line | Soluble in water |
| 12 | TESAMORELIN | certificate line | Soluble in water / TMG-BAC |
| 13 | THYMOSIN ALPHA-1 | certificate line | Soluble in water / TMG-BAC |
| 14 | TMG-2TZ | certificate line | Soluble in water / TMG-BAC |
| 15 | VITAMIN B12 | certificate line | Soluble in water |
| 16 | TMG-3RT | **never had the claim** | (empty) |
| 17 | TMG-BAC | **never had the claim** | Miscible with aqueous solutions |

**On every one of the 17:** the string `validated by HPLC` is gone and the phrase
`bacteriostatic water` is gone. Checked against the whole page markup, not just the field.

**Correction to an earlier assumption:** not all 17 carried the claim. 15 did. TMG-3RT and
TMG-BAC never did, so there was nothing to replace on those two — `changed: []` was the correct
result there, not a failure.

## New finding: TMG-3RT's specs are nearly empty

Its CAS number, molecular formula, molecular weight, amino-acid sequence, purity, endotoxin,
appearance and solubility are **all blank**. Only Storage is filled. Every other product is
substantially populated. This is a genuine content gap, not a rendering problem — though it is
masked today because the storefront does not render the specs block at all.

## Two platform behaviours worth not relearning

1. **A timeout does not mean the write failed.** TMG-2TZ's edit appeared to freeze — the call
   had already written and saved and only the response never returned. Always read the value
   back before re-running, or you will double-apply.
2. **Check your own selector before blaming the page.** TMG-3RT looked unpopulated because
   `document.querySelectorAll('input')[0]` is the admin search box, not the product title.

## Still open: the citations

Real papers were pulled from PubMed for Epitalon. Of three, only one is safe for a product page —
an in-vitro enzyme assay. The others carry effect claims in their titles, and a title sitting
under a product you sell reads as intended use.

Needs Mila's decision: cite only identity, characterisation and analytical-method work — which
for several compounds means one citation or none — or take the broader literature knowingly.
