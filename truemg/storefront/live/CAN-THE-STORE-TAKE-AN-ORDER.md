# Can the store take an order? — checked 13 Oct 2026

Mila, exhausted, at the end of a long night: *"I need the site to look good, and
I need it to fucking work. I need us to be able to put an order in and print the
label... we need to make sure that we put the payment info for Zelle and Venmo
somewhere."*

Checked the admin rather than guessing. Two of the three are better news than
she expected, and the third is the whole blocker.

## ✅ Payments — already done, nothing to do

`/admin/payments` → **Manual payment options**. Both are **on**, both carry her
details and customised wording:

| Method | Detail | State |
|---|---|---|
| **Venmo** | `@TrueMGLabs` | **on**, customised |
| **Zelle** | `sales@truemglabs.com`, recipient name `TrueMG` | **on**, customised |
| Crypto, Cash App, PayPal | — | off |

Both already carry the emoji rule: *"your payment note MUST contain an emoji…
Orders sent without an emoji in the note will be canceled and will not be
refunded."* The customer sees these **after** they order, which is how Lapis
handles manual payment.

## ⛔ Stock — this is what stops an order

`/admin/inventory`:

```
20  variants
 0  units in stock
20  out of stock
```

**Every variant is Out.** That is why every card on the storefront reads
*Out of stock* — visible in Mila's own screenshot — and why **nobody can check
out.** Nothing is broken; there is simply no stock entered.

Fix: Products → Inventory → click the **In stock** cell on a row → type a
quantity. Twenty rows. It is data entry, not a build.

**This is the single highest-value thing outstanding on the whole project.**
The site looking slightly flat does not matter while nobody can buy anything.

## ❔ Printing a label — not testable yet

There are **no orders**, so there is nothing to print a packing slip or label
from, and the flow cannot be verified. `/admin/shipping` has one rate
configured and there is a `3PL` section.

Once stock is in, the test is two minutes: place a real order through the
storefront, pay by Venmo, then look at what the order screen offers. Do not
speculate about it before then.

## Also outstanding, from the setup checklist

**Lab results: 0 of 17 live products have a COA.** The storefront copy leans
hard on "the certificate is filed against your lot number" — that claim is
currently unsupported by any published certificate. Worth raising with Mila; it
is a compliance-adjacent gap, not a cosmetic one.

## Everything else that is green

Take payments ✓ · Add products ✓ (17 live) · Set shipping rates ✓ (1 rate) ·
Add logo ✓ · Connect domain ✓ (truemglabs.com live) · Coming-soon curtain still
up (`comingSoonEnabled: 1`).
