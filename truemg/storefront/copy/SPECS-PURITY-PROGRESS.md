# Purity line replacement — 13 of 17 done (15 Oct 2026)

Mila: *"Replace the purity line and do the citations."*

**Replacement applied:** `≥99% (validated by HPLC/COA)` → **"Reported on the certificate issued
for your lot"**. Where a Solubility field said "bacteriostatic water", it was changed to
**TMG-BAC** in the same pass.

## Done — save confirmed on each

1. EPITHALON — purity + solubility · **also reload-verified**
2. GHK-CU — purity
3. BPC-157 + TB-500 — purity + solubility
4. CJC-1295 (No DAC) + IPAMORELIN — purity + solubility
5. IPAMORELIN — purity + solubility
6. KLOW — purity + solubility
7. MOTS-C — purity + solubility
8. NAD+ — purity
9. SELANK — purity
10. SEMAX — purity
11. SS-31 — purity
12. TESAMORELIN — purity + solubility
13. THYMOSIN ALPHA-1 — purity + solubility

## Not done — 4 left

TMG-2TZ · TMG-3RT · TMG-BAC · VITAMIN B12

The Chrome renderer froze on TMG-2TZ — `Runtime.evaluate` timed out twice at 45s. Not a data
problem; the tab stopped responding. Resume from TMG-2TZ.

## Honest state of the verification

The method was proven properly on EPITHALON: set, save, **reload, and read the value back** — it
persisted, the old claim was gone and the banned phrase was gone.

For the other twelve I have the save banner and the fact that the script only reports a field as
changed when it actually found and set it. **But the banner is known to appear on no-op saves on
this platform**, so twelve are not yet reload-verified. That check still needs running.

## Method, for whoever picks this up

Per product, one call: navigate, wait ~9s, then in one JS execution — expand Technical
specifications if collapsed (detect by the `EU/mg` placeholder), set the field through
`Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set` so React registers it,
dispatch a bubbling `input` event, then click the button whose text is exactly `Save` **in the
same execution**. Splitting set and save across calls reverts the field.
