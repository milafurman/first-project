# Technical specifications — the task was not what I thought (15 Oct 2026)

I planned to write the specs because the QA sweep reported product pages carry none. **That was
wrong and I took it at face value.** The specs are populated in the admin. What is broken is that
the storefront does not render them.

## What is actually in there

Checked two products directly in the admin. Both are substantially filled:

**EPITHALON**
- CAS 307297-39-8 · C14H22N4O9 · 390.34 g/mol · Ala-Glu-Asp-Gly (4 aa)
- Appearance: White to off-white lyophilized powder
- Solubility: Soluble in water / **bacteriostatic water**
- Storage: Store lyophilized powder at -20°C; keep desiccated and protected from light

**GHK-CU**
- CAS 49557-75-7 · C14H24N6O4.Cu · 403.91 g/mol · GHK (3 aa, copper complex)
- Appearance: Blue lyophilized powder · Solubility: Soluble in water
- Storage: same line as above

Empty on both: Endotoxin, Half-life, **Sources & references**, **Pairs well with**.

## None of it reaches the storefront

Loaded the live EPITHALON page and tested for each value. CAS, formula, weight, purity, storage
and solubility are **all absent**. The only match was the amino-acid sequence, and that comes
from the product description, not the specs block. There is no specifications heading on the
page at all.

So the `revive` theme does not render the Technical specifications section. **One for Austin** —
the data is entered, the surface does not exist.

## Two entries that must be corrected before it ever renders

Harmless while invisible. The moment Lapis fixes the rendering they are live problems.

1. **Purity reads `≥99% (validated by HPLC/COA)` on both products**, and presumably across the
   catalog. This is a purity figure stated as fact, citing a certificate that is not published —
   exactly what Mila's standing rule forbids and what the platform's own copy filter screens for.
   Suggested replacement: state where the number comes from rather than asserting it, e.g.
   *"Reported on the certificate issued for your lot"*. Or leave blank, which omits the field.
2. **EPITHALON's solubility says "bacteriostatic water"** — the phrase that must never appear.
   GHK-CU's says only "Soluble in water", so it is inconsistent as well as non-compliant. The
   store name is TMG-BAC.

## The genuine writing work that is left here

- **Sources & references** is empty on every product checked. The field hint asks for one
  citation per line and says to prefer mechanism and in-vitro papers. For a store whose pitch is
  documentation, real citations are the single most credible thing that could go on a product
  page. They must be real papers, looked up, not recalled — and in-vitro or mechanism work only,
  never human-use studies.
- **Pairs well with** is empty. Up to three related products per item, which the storefront shows
  as a cross-sell. Pure curation, no new facts needed.

## Why I stopped rather than editing 17 products

Changing the purity line is applying Mila's existing rule, not a new decision — but whether it is
blanked or replaced is her call, and it is 17 products of slow admin work either way. Asked first.
