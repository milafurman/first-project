# Citations — the finding, the placement, and the rule

Mila, 15 Oct: *"do the citations — identity and method papers only and anything else that
makes us sound good."*

## The finding: there is no per-product citation surface

The Lapis admin has a **Sources & references** field on every product. It is empty on all of
them, and writing into it would have been invisible work: the `revive` theme does not render
the Technical specifications block at all, and Sources & references sits inside it. Verified
by loading a live product page and reading the DOM — a product renders its one-sentence
description, a "Compound class" line, the four trust badges, the COA block and the compliance
statement. Nothing else. Same finding as the specs in `SPECS-FINDING.md`, same cause.

So per-product citations are not possible on this theme today. One for Austin.

## Where they go instead

Checked every writable surface on the store and how full each one is:

| Surface | Capacity | Free | Verdict |
|---|---|---|---|
| `aboutBody` (About page) | 12,000 | 9,860 | **chosen** |
| `faq` | 4,000 | 401 | one cross-reference entry, if it fits |
| `labIntro` (Lab Results) | 600 | 36 | full |
| `legalTermsBody` | 20,000 | — | renders the platform's own Terms; leave alone |

The About page is the right home anyway. It is where a cautious buyer — or a payment
processor doing diligence — goes looking for substance, and Sam's note that the design reads
"too bloggy" is answered more by a references section than by any amount of rewriting.

## The rule every citation obeys

**Identity and method only.** Two kinds, nothing else:

1. **Identity / characterization** — the paper that first isolated, sequenced, synthesized or
   structurally described the compound. This supports the only claim the store makes about a
   compound: that it is what the label says.
2. **Analytical method** — how identity and purity are determined. RP-HPLC, LC-MS, amino acid
   analysis, impurity profiling. This supports the second claim: that it was tested properly.

**No effects papers.** Not healing, not outcomes, not clinical trials, not anti-ageing, not
cognition. A citation to an efficacy paper is an implied claim even with no sentence attached
to it, and it is exactly what the compliance rules forbid. Where the only literature available
for a compound is effects literature, the compound gets no citation and the gap is stated.

**Nothing unverified ships.** Every reference is confirmed against PubMed metadata — title,
journal, year, authors, DOI — before it goes on the page. An invented citation on a page whose
entire purpose is credibility would be worse than no page at all.

## Status

Research in progress across the 17 catalog items. Verified list and the applied text follow.
