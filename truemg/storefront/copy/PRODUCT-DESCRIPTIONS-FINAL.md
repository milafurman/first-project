# Product descriptions — all ten, APPLIED 15 Oct 2026

**Status: done.** All ten are live and verified on the storefront catalog — 10/10 carry the
new text and no card shows a fragment any more. Applied through Mila's own Chrome session in
the Lapis admin at Products -> Catalog -> product -> Description, because product fields are
not design copy keys and `apply_design_change` cannot reach them.

**How to do this again, because it is fiddly.** Typing into the description box with synthetic
clicks and keystrokes is unreliable — it landed 3 times out of 10, and the "Saved — storefront
updated." banner appears even when the save is a no-op, so the banner proves nothing. What works
every time, in ONE javascript_tool call per product: grab the textarea by its
"Marketing description" placeholder, set its value through
`Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set` so React registers
it, dispatch a bubbling `input` event, then find the button whose text is exactly "Save" and
call `.click()` on it in the same execution. Then verify by reloading the product page and
reading the textarea back, or by reading the live catalog card — never by the banner.

Listed in the order the admin lists products (alphabetical), so they can be worked
top to bottom in one pass.

**Every one is a single sentence with exactly one period, at the end.** That is deliberate:
the catalog card drops everything after the first period, so a two-sentence description
loses half of itself with no warning. See [[lapis-card-truncates-at-first-period]].

---

**EPITHALON**
Ala-Glu-Asp-Gly, four residues, synthesised after a peptide fraction originally isolated from the pineal gland.

**KLOW**
A four-peptide blend — KPV, GHK-Cu, BPC-157 and TB-500 — premixed in a single vial for labs that run them together.

**MOTS-C**
Sixteen residues encoded in mitochondrial DNA rather than nuclear DNA, which is the part researchers are interested in.

**NAD+**
Nicotinamide adenine dinucleotide, a redox cofactor rather than a peptide, standard material for metabolic and enzyme assays.

**SELANK**
Seven residues, fully synthetic, built out from the tuftsin fragment and supplied as a lyophilised powder.

**SEMAX**
A modified seven-residue fragment of ACTH, common in structure-activity work on neuropeptides.

**SS-31**
Elamipretide, a four-residue peptide that localises to mitochondrial membranes, where cardiolipin is the usual subject of study.

**THYMOSIN ALPHA-1**
Twenty-eight residues made synthetically to match a sequence the thymus produces, supplied as a lyophilised powder.

**TMG-2TZ**
Thirty-nine residues, a dual agonist at the GIP and GLP-1 receptors, supplied as a reference compound.

**VITAMIN B12**
Cobalamin, a cobalt-centred corrinoid, supplied as a dark red crystalline powder for analytical and reference work.

---

## What each one replaces, and why

Six were visibly broken on the card — EPITHALON showed only `Ala-Glu-Asp-Gly.`, SS-31 showed
the single word `Elamipretide.`, TMG-2TZ showed `Thirty-nine residues.` which identifies nothing.
Three more — MOTS-C, THYMOSIN ALPHA-1, SELANK — were losing their second sentence silently,
because what survived still read as a grammatical sentence. Thymosin's loss mattered most:
the dropped words were "Made synthetically", which is what stops the card implying the material
was harvested from a thymus.

KLOW is the tenth. Its old description talked about the paperwork instead of the contents,
because the blend was not published anywhere on the site. Mila confirmed the components on
15 Oct 2026, and they match the size label on the product, `80MG (TB10 + BPC10 + GHK50 + KPV10)`.

## Rules every line above obeys

Research-use framing throughout. No dosing. No therapeutic, human-use or veterinary claim, and
nothing about an outcome in a person or an animal — each line says what the material *is*, never
what it does. The word "performance" appears nowhere. No testing or purity figure is stated as
fact in the copy. No shipping promise. TMG-BAC is never called bacteriostatic water.
The Gila monster does not appear — it is provenance for the name and the mark only.

## The eight that need no change

KLOW aside, these were already single sentences and already compliant, so the card renders them
whole: TMG-BAC, BPC-157 + TB-500, CJC-1295 (No DAC) + IPAMORELIN, IPAMORELIN, TESAMORELIN,
TMG-3RT, GHK-CU.
