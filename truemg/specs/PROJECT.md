# TrueMG Labs — storefront build

**Store:** https://truemglabs.com · Lapis platform · `arcane` template
**Definition of done for Friday 2026-10-09:** a real order can be placed and
completed end to end — once by Mila internally, once by a stranger as a customer —
on a site that looks and behaves 90% finished.

Today is Tuesday 2026-10-06. **Three working days.**

---

## The teams

Seven agents in `.claude/agents/`. Each owns a lane and knows the edge of it.

| Agent | Owns | Cannot do |
|---|---|---|
| `truemg-pm` | Sequencing, critical path, status, the cut list | Build anything |
| `truemg-brand` | Logo, palette, vial art direction, dynamic backgrounds, CSS visual system | Replace product photos |
| `truemg-storefront` | Every live change through the Lapis design endpoint — copy, layout, CSS | Touch products or checkout config |
| `truemg-cro` | The funnel, offers, pricing presentation, button copy | Switch an offer on |
| `truemg-seo` | Metadata, FAQ, About, internal links, speed | Invent human-use keywords |
| `truemg-compliance` | RUO framing, entry gate, Terms/Privacy/Refunds, screening every line | Give legal advice |
| `truemg-ops-qa` | The end-to-end order test on real devices | Set stock |

**The structural fact that governs everything:** the Lapis design endpoint reaches
~281 copy keys, the full palette, the template, and a custom CSS block — but it
explicitly *cannot* reach products, inventory, prices, images, checkout or settings.
So the work splits cleanly in two, and only one half is ours.

---

## Critical path to Friday

### Mila's lane — nothing else matters until these are done
Blocking, admin-only, no agent can start them:

1. **Set stock on at least 6 products.** At 0 stock there is no add-to-cart button
   anywhere on the site and the Friday test cannot run at all. This is the single
   gate on the whole week.
2. **Fix the `/catalog/bpc-157-tb-500` 404.** The catalog links to a product page
   that does not resolve. 34 sessions hit it last month and every one bounced.
3. **Confirm at least one payment method is live** and can take a real charge.
4. **Decide the contact address** — `research@truemg.com` vs the `truemglabs.com`
   domain. Then make the mailbox actually receive.
5. **Upload transparent-PNG vial renders** to the spec in `../assets/IMAGE-SPECS.md`.

### Day 1 (Tue) — identity and structure
- `brand`: palette + logo treatment + the CSS system that kills the white boxes
  and puts a color field behind every vial. Preview only.
- `compliance`: entry gate decision and wording; rewrite Terms/Privacy/Refunds.
- `seo`: fix the contact-address defect; draft FAQ JSON and the long-form About.

### Day 2 (Wed) — conversion surface
- `cro`: trust triad, comparison table, promo banner, popup, announcement bar,
  every button rewritten to promise possession instead of work.
- `storefront`: apply the approved Day 1 + Day 2 batches to the live store.
- `brand`: hero background, discovery and browse tiles, mobile hero.

### Day 3 (Thu) — proof
- `ops-qa`: full end-to-end order at 1440px and 390px, screenshot every step,
  confirm the order lands in `get_orders`.
- Everything that fails goes back out the same day. Nothing new starts.

### Friday — the two live orders, then the cut list

---

## Cut list — drops first if the date is at risk
Daily rotating half-price list · split payment · subscription panel builder ·
volume tiers · blog/journal · account area.

None of these block an order being completed. All of them are the right
post-Friday roadmap, in roughly that order.

---

## Open decisions
Tracked live in the project manager artifact. The four that gate Day 1 are brand
direction, logo assets, image hosting, and whether the entry gate ships.
