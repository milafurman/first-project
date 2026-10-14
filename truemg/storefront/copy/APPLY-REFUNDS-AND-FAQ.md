# Refund policy + FAQ — two pastes to match each other

Both go into the Design studio chat at **app.uselapis.io/admin/appearance**,
then **Publish**. Doing one without the other re-creates the contradiction that
started this.

---

## PASTE 1 — the policy

> Replace the Shipping & Refund Policy text (legalRefundsBody) with exactly this,
> keeping the paragraph breaks:
>
> All orders are packaged and documented for laboratory research use, with certificates of analysis available for verification prior to or upon shipment. Shipping timelines and carrier options are confirmed at checkout.
>
> Delivery is confirmed by carrier tracking. An order the carrier records as delivered is treated as received, and tracking is the record TrueMG works from for any question about whether a parcel arrived.
>
> Products are made to order, so TrueMG does not accept returns or issue refunds on intact orders. Once material has left our control, it cannot be re-verified against its certificate or returned to stock.
>
> If your shipment arrives damaged or contains a documented fulfillment error, report it within 48 hours of delivery. Include your order number, photos of the parcel and vial as received, and one continuous, unedited video of the package being opened. The video should start with the sealed parcel, show the shipping label, and show the contents and any damage. Claims without this video cannot be approved. Approved claims are resolved by replacement.
>
> Orders confirmed as inconsistent with research-use terms will not be fulfilled. Contact our support channel for any shipping or order-accuracy concern.

## PASTE 2 — the FAQ answer

> In the FAQ, replace the answer to "What if a vial arrives damaged?" with
> exactly this:
>
> Report it within 48 hours of delivery. Email us your order number, photographs of the parcel and the vial as they arrived, and one continuous, unedited video of the package being opened — starting with the sealed parcel, showing the shipping label, then the contents and any damage. Claims without that video cannot be approved. Approved claims are resolved by replacement. The full terms are on the Shipping & Refunds page.

---

## Checked

Every requirement now appears in **both** documents: 48 hours, order number,
continuous unedited video, sealed parcel, shipping label, "cannot be approved",
replacement. A customer reading either one gets the same instruction.

Mila's seven sentences are carried **verbatim** — the policy is hers, not a
rewrite of hers. What was added around them: the three operational lines from
the previous policy she did not address (certificates available for
verification, shipping timelines confirmed at checkout, orders inconsistent with
research-use terms not fulfilled) and the tracking line she asked for.

No banned vocabulary, research-use framing intact, no exclamation marks.

## ⚠️ One change worth a second's thought

The old policy resolved approved claims by **"replacement or credit at TrueMG's
discretion."** Mila's version says **"resolved by replacement"** only.

That is stronger and simpler, and it removes an option: if the compound is out
of stock, replacement is the only promise on the page and there is no stated
fallback. Worth keeping as-is if replacement is always possible; if not,
"replacement, or credit where replacement is not available" keeps the firmness
and closes the gap.

---

# Signature on delivery — the answer is "not from Lapis"

Checked `/admin/shipping` in full. **There is no signature, signed-for, adult-
signature or insurance control anywhere on it.** What that page has:

| | |
|---|---|
| Ship-from | TrueMGLabs · 1090 Honeysuckle Dr, Wheeling, IL 60090 |
| Labels | **Shippo — connected** (EasyPost available, not connected) |
| Saved packages | Poly mailer, Waterproof Insulated Foil Thermal Bubble |
| Checkout rates | Standard $10.50, free over $500, 3–5 business days; local pickup |

**But labels are bought through Shippo, and Shippo does support signature
confirmation as a per-label option.** So the capability exists one layer down.

Three routes, in order of effort:

1. **Set it in Shippo** — a default or per-shipment service option on the Shippo
   account. Does not need Lapis at all.
2. **Check the buy-label screen in Lapis** once a real order exists. Lapis may
   already pass Shippo's service options through; **there are no orders yet, so
   this could not be tested.** Worth looking the first time a label is bought.
3. **Ask Austin** to expose signature confirmation and insurance as options when
   buying a label, with a rule like "require signature over $X". A reasonable
   ask — add it to the list already with him.

⚠️ **Until one of those is in place, do not write a signature requirement into
the policy.** A policy that promises signature-on-delivery while labels ship
without it is worse than silence. The tracking line above is the honest version
of that protection today.
