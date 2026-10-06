# TrueMG — Blockers to "place and complete an order by Friday"

Verified live against the Lapis API and a real browser session on 2026-10-06.

## P0 — kills the Friday goal outright

### 1. Every product is out of stock
All **20 variants across all 17 products** are at `stock: 0`. Every card on the
storefront reads `Unavailable`. There is no add-to-cart button rendered anywhere
on the site.

This is the whole ballgame. The Friday goal is "place and complete an order,
internally and as a customer, beginning to end." That is impossible at 0 stock,
and **no agent can fix it** — the Lapis design endpoint explicitly cannot reach
products, inventory, prices, checkout or settings. Mila sets stock in the Lapis
admin. Everything else on this list is cosmetic by comparison.

### 2. Product pages 404
`/catalog/bpc-157-tb-500` returns **"Product not found"** while the catalog grid
links to exactly that URL. Analytics shows 34 sessions hit that page in 30 days —
the single most-visited product page on the site — and every one of them hit a dead
end. Some product slugs resolve (`bpc-157-tb-500-r20n`, `tesamorelin-9ruh`), so the
catalog is generating at least one link that does not match its own product.
Admin-side; needs Mila or Lapis support.

## P1 — the site cannot sell even once stock is on

### 3. The funnel is flat on its face
30 days: **310 sessions → 4 add-to-cart (1.3%) → 2 checkouts → 0 orders → $0.**
306 of 310 visitors leave the grid without touching anything. Partly #1, but the
grid gives nobody a reason: no strike-through price, no purity number, no COA
badge, no urgency, no bundle, no reason to want it.

### 4. There is no front door
**100% of traffic is Direct.** Zero organic, zero referral, zero campaign. The
store is invisible to search.

### 5. Zero custom CSS, zero visual identity
`customCss` is an empty string. Nothing has been styled. Every vial sits in a hard
white box on a grey card — the exact thing Mila flagged. The hero's entire right
half is dead space.

## P2 — trust and correctness

### 6. Contact email does not match the domain
Site is `truemglabs.com`; the published contact address is `research@truemg.com`.
Either the domain is wrong or the mailbox is. A mismatched contact address reads
as a scam signal to a cautious buyer, and bounces kill deliverability.

### 7. No entry gate
`entryGateEnabled` is off. The reference competitor gates every first-time
visitor on 21+ and qualified-researcher before showing a single product. For an
RUO catalog this is the industry norm, and it is a documented attestation if
anyone ever asks. It costs some conversion. See `COMPLIANCE.md`.

### 8. Legal copy is template-default and unreviewed
`legalTermsBody` / `legalPrivacyBody` / `legalRefundsBody` are carrying generic
text. No attorney has reviewed the Terms, the gate language, or the labeling.
This should not go live taking money without that review.

---

## Who can fix what

| Fix | Reachable by an agent | Needs Mila in the Lapis admin |
|---|---|---|
| Stock levels | ✗ | ✓ |
| Prices, discounts, bundles, volume tiers | ✗ | ✓ |
| Product photos | ✗ | ✓ |
| Payment methods on/off | ✗ | ✓ |
| Broken product slug / 404 | ✗ | ✓ |
| Palette, CSS, layout, hero, backgrounds | ✓ | |
| All page copy, FAQ, About, legal bodies | ✓ | |
| Entry gate, disclaimers, compliance text | ✓ | |
| Trust blocks, comparison table, promo, popup | ✓ | |
| SEO metadata, internal linking | ✓ | |
