# The cross-sell section — renamed, and the pairing plan (15 Oct 2026)

## Done: the heading is no longer advisory

The theme calls this section **"Pairs well with"**, on every product page and in the cart. On a
research-use-only catalog that phrasing suggests combining compounds, which is use guidance and
is exactly what the standing rules forbid. There are keys for it, so it is now:

- `pairsWellWithHeading` → **"Related in the catalog"**
- `checkoutCrossSellHeading` → **"Related in the catalog"**

Purely navigational. No suggestion about using anything together. Applied and live.

There is also `hide:pairsWellWith` if the section should be removed entirely rather than renamed.

## Not done: the pairings themselves — needs a nod first

The per-product field takes up to three products. **The entries are only safe if the logic is
catalog adjacency, never a suggested combination.** Proposed basis, in order of safety:

1. **Blend ↔ its components.** KLOW contains BPC-157, TB-500 and GHK-Cu, so it pairs with
   BPC-157 + TB-500 and GHK-CU. CJC-1295 + IPAMORELIN pairs with IPAMORELIN. This is factual
   composition, already stated in the descriptions.
2. **Same stated class.** TMG-2TZ ↔ TMG-3RT, both incretin-receptor agonists. SEMAX ↔ SELANK,
   both short synthetic neuropeptides. NAD+ ↔ VITAMIN B12, both cofactors rather than peptides.
   The class is already printed on each product page, so the adjacency is public and factual.
3. **TMG-BAC on the lyophilised powders.** A laboratory ordering a powder needs a solution; this
   is basket logic, not a protocol.

**What is deliberately excluded:** anything that groups two actives on the basis of what they do.
That is the line between a catalog and a recommendation.

## The judgement call for Mila

Even on this basis the section still shows three products next to each other under a heading, and
a regulator reads total impression. Three options:

- **Populate as above** — defensible, and makes the catalog feel built rather than listed.
- **TMG-BAC only** — the narrowest version. Pure logistics, nothing adjacent to a claim.
- **Hide the section** — `hide:pairsWellWith` set to "1". Zero risk, slightly flatter catalog.

Not started pending that choice. It is 17 products of admin work either way, so worth deciding
once rather than redoing.

---

## Closed, 15 Oct 2026 — and I nearly did the wrong thing

I told Mila I would hide the section. Then I checked the live product page before writing, and
**the section does not render at all** when the per-product field is empty, which it is on all
17. The theme already does exactly what she asked for.

There *is* a `hide:pairsWellWith` flag. **Setting it would be actively harmful.** Left unset,
the theme shows the section only when a product actually has cross-sells, which is the correct
behaviour. Set, it would silently suppress them later and quietly waste the time of whoever
fills those fields wondering why nothing appears.

**So: no change made.** Verified on the live GHK-CU page — headings are `GHK-CU`,
`Compound class`, `Certificate of Analysis` and the disclaimer. No cross-sell section.

The outcome Mila wanted was already true. The right move was to write nothing.
