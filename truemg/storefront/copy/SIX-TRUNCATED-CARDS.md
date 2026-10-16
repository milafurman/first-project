# Six catalog cards show a fragment — measured 14 Oct 2026

The catalog card renders **only the first sentence** of a product description.
Six of the seventeen were written as two sentences, so six cards currently say
almost nothing. Read off the live catalog, not from notes:

| Product | What a shopper sees today |
|---|---|
| **SS-31** | *"Elamipretide."* |
| **TMG-2TZ** | *"Thirty-nine residues."* |
| **EPITHALON** | *"Ala-Glu-Asp-Gly."* |
| SEMAX | *"A modified fragment of ACTH."* |
| VITAMIN B12 | *"Cobalamin, a cobalt-centred corrinoid."* |
| NAD+ | *"The redox cofactor itself, not a peptide."* |

The first three are the bad ones — a single word or a bare formula on a product
card. The other three are at least complete thoughts.

The full text exists in each product's description; the card just cuts at the
first full stop. **The fix is to merge each pair into one sentence**, which is
how GHK-CU and IPAMORELIN were already written — they display fine.

## The six replacements

| Product | Replace the description with |
|---|---|
| **SS-31** | Elamipretide, a tetrapeptide that localises to mitochondrial membranes, where cardiolipin is the usual subject. |
| **TMG-2TZ** | Thirty-nine residues, a dual GIP and GLP-1 receptor agonist supplied as a reference compound. |
| **EPITHALON** | Ala-Glu-Asp-Gly — four residues, synthesised after a pineal peptide fraction. |
| **SEMAX** | A modified fragment of ACTH, common in structure-activity work on neuropeptides. |
| **VITAMIN B12** | Cobalamin, a cobalt-centred corrinoid, supplied for analytical and reference work. |
| **NAD+** | The redox cofactor itself rather than a peptide, standard material for metabolic and enzyme assays. |

## Where to do it — NOT Design studio

**Products → Catalog → click the product row → the Description box → Save.**

One at a time, six products. It is the same screen as the Pictures panel, so it
pairs with the photo uploads: fix the description and replace the photo in one
visit.

## ⚠️ Validation status, stated honestly

These were **not** dry-run through `preview_design_change`, because product
descriptions are product fields rather than design copy keys — that endpoint
does not accept them, so there is no way to pre-test them from here.

The risk is low: **every one of these sentences is already live**, just split in
two. Merging them adds no new claim. But Lapis's compliance gate did refuse FAQ
answers for claiming "testing, purity or an analytical method" with no
certificate on file, so if any of these six is refused on save, the likely
candidates are **TMG-2TZ** ("receptor agonist") and **SS-31** ("localises to
mitochondrial membranes").

If one is refused, the message names the offending wording — send it over rather
than guessing at a rewrite.
