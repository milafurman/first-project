# The 17 product descriptions — redraft

Drafted 12 Oct 2026. Paste into Lapis admin → Products → Catalog → each product
→ Description. The connector cannot reach product data, so this step is manual.

## Why they changed

Every one of the seventeen opened the same way:

> TESAMORELIN — "Tesamorelin **is a** synthetic peptide analog **classified within** the GHRH research family…"
> IPAMORELIN — "Ipamorelin **is a** pentapeptide **classified within** the growth-hormone secretagogue family…"
> GHK-CU — "GHK-Cu **is a** copper-binding tripeptide complex…"
> KLOW — "KLOW **is a** research-formulated blend combining…"

`[NAME] is a [noun phrase] classified within [family]`, seventeen times. One
sentence skeleton repeated is the loudest machine tell on a page, louder than
any individual word, and no amount of styling hides it. The replacements vary
their construction on purpose — some lead with the sequence, some with the
composition, some with where the molecule came from.

They are also much shorter. The card truncates at two lines, so anything past
roughly twenty words was never being read anyway.

## What they may and may not say

Each line states **what the molecule is** — composition, residue count, origin,
pharmacological class. None states what it does in a person or an animal,
because none may.

Receptor class ("dual GIP and GLP-1 receptor agonist") is a property of the
molecule and standard catalogue nomenclature, not an outcome claim, so it
stays. "Studied for" and "common in … work" describe the literature rather
than promising a result.

The card already carries "Research use only." as its own field, so these lines
do not repeat it and spend their words on something useful instead.

## The seventeen

| Product | Description |
|---|---|
| **BPC-157 + TB-500** | Two of the most-cited sequences in the peptide literature, supplied as one blend. |
| **CJC-1295 (No DAC) + IPAMORELIN** | Two secretagogue peptides premixed in one vial, for labs that run them together. |
| **EPITHALON** | Ala-Glu-Asp-Gly. Four residues, synthesised after a pineal peptide fraction. |
| **GHK-CU** | Glycyl-histidyl-lysine holding a copper(II) ion. Three residues and a metal. |
| **IPAMORELIN** | Five residues. Selective at the ghrelin receptor in non-clinical models. |
| **KLOW** | A multi-peptide blend under a single designation, with the same lot-matched paperwork as everything else. |
| **MOTS-C** | Encoded in mitochondrial DNA rather than nuclear DNA. That is the part researchers are interested in. |
| **NAD+** | The redox cofactor itself, not a peptide. Standard material for metabolic and enzyme assays. |
| **SELANK** | Seven residues, built out from the tuftsin fragment. Fully synthetic. |
| **SEMAX** | A modified fragment of ACTH. Common in structure-activity work on neuropeptides. |
| **SS-31** | Elamipretide. A tetrapeptide that localises to mitochondrial membranes, where cardiolipin is the usual subject. |
| **TESAMORELIN** | A synthetic analogue of growth-hormone-releasing hormone, supplied for in-vitro receptor work. |
| **THYMOSIN ALPHA-1** | Twenty-eight residues matching a sequence the thymus produces. Made synthetically. |
| **TMG-2TZ** | Thirty-nine residues. A dual GIP and GLP-1 receptor agonist, supplied as a reference compound. |
| **TMG-3RT** | A triple agonist at the GIP, GLP-1 and glucagon receptors — the most recent class represented here. |
| **TMG-BAC** | A 10 mL research solution rather than a compound, stocked so an order can be completed in one place. |
| **VITAMIN B12** | Cobalamin, a cobalt-centred corrinoid. Supplied for analytical and reference work. |

## Two judgement calls worth your eye

**TMG-3RT.** The shipped copy says only "a research compound supplied for
laboratory and in-vitro investigational use", which tells a buyer nothing. The
draft above names the receptor class. The identity is inferred from
`characters/002-retatrutide.md` in this repo and from TMG-2TZ being tirzepatide
— **confirm it before publishing.** If you would rather not name the class at
all, the fallback is: *"The newest compound in the catalogue, and the least
written about so far."*

**TMG-BAC.** Deliberately not called bacteriostatic water. `specs/BRAND.md`
settles this: that is a specific regulated drug product name, and a research
catalogue calls the item a research solution. The label already reads that way
and the description now matches it.

## Still missing from the card

Copy alone will not close the gap with the reference sites. Their cards also
carry a purity figure and a "View COA" link before the click, and an anchored
price. Those are product fields and pricing, not description text — tracked in
`DESIGN-TASKLIST.md` under Phase 2.
