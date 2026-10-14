# Refund policy + FAQ — two pastes

Both go into the Design studio chat at **app.uselapis.io/admin/appearance**,
then **Publish**. Do them together: one without the other re-creates the
contradiction this was fixing.

Both were dry-run through Lapis **together** and accepted — `ok`, no rejections,
no readability fixes.

---

## PASTE 1 — the policy

```
Replace the Shipping & Refund Policy text (legalRefundsBody) with exactly this, keeping the paragraph breaks:

All orders are packaged and documented for laboratory research use, with certificates of analysis available for verification prior to or upon shipment. Shipping timelines and carrier options are confirmed at checkout.

Delivery is confirmed by carrier tracking. An order the carrier records as delivered counts as received, and carrier tracking is the record TrueMG works from for any question about whether a parcel arrived.

Products are made to order, so TrueMG does not accept returns or issue refunds on intact orders. Once material has left our control, it cannot be re-verified against its certificate or returned to stock.

If your shipment arrives damaged or contains a documented fulfillment error, report it within 48 hours of delivery. Include your order number, photos of the parcel and vial as received, and one continuous, unedited video of the package being opened. The video should start with the sealed parcel, show the shipping label, and show the contents and any damage. Claims without this video cannot be approved. Approved claims are resolved by replacement.

Orders confirmed as inconsistent with research-use terms will not be fulfilled. Contact our support channel for any shipping or order-accuracy concern.
```

## PASTE 2 — the FAQ answer

```
In the FAQ, replace the answer to "What if a vial arrives damaged?" with exactly this, leaving every other question and answer untouched:

Report it within 48 hours of delivery. Email us your order number, photographs of the parcel and the vial as they arrived, and one continuous, unedited video of the package being opened — starting with the sealed parcel, showing the shipping label, then the contents and any damage. Claims without that video cannot be approved. Approved claims are resolved by replacement. The full terms are on the Shipping & Refunds page.
```

---

## ⚠️ One word had to change, and it is worth knowing why

The tracking line first read *"an order the carrier records as delivered is
**treated** as received"*. **Lapis refused the whole policy over it:**

> *Compliance rejection: this is a research-use-only store and the flagged
> wording is not allowed. Offending text: legalRefundsBody: "treated".*

Their filter reads **"treated"** as treatment language. A false positive on a
shipping sentence, but it is a hard block, so the line now says **"counts as
received"**. Re-tested and accepted.

**Lesson for any future copy: avoid "treat", "treated" and "treatment" entirely,
even in a sentence about parcels.** Their rejection names the offending word,
so a refusal is cheap to diagnose — but only if you dry-run before handing it
over.

Their message also warns against second-person "you". That is **not** actually
blocked — this text passed with "your shipment" and "your order number"
throughout, as does the FAQ.

## Checked

Every requirement appears in **both** documents: 48 hours, order number,
continuous unedited video, sealed parcel, shipping label, "cannot be approved",
replacement.

Mila's seven sentences are carried **verbatim**. Added around them: the three
operational lines from the old policy she did not address, and the tracking line
she asked for.

## One consequence of the new wording

The old policy resolved approved claims by *"replacement or credit at TrueMG's
discretion."* The new one says **"resolved by replacement"** only — stronger and
simpler, but if a compound is out of stock there is no stated fallback. Keep as
is if replacement is always possible; otherwise *"replacement, or credit where
replacement is not available"* keeps the firmness and closes the gap.

---

# Signature on delivery — not available from Lapis

Read `/admin/shipping` in full. **No signature, signed-for, adult-signature or
insurance control exists on it.** What is there:

| | |
|---|---|
| Ship-from | TrueMGLabs · 1090 Honeysuckle Dr, Wheeling, IL 60090 |
| Labels | **Shippo — connected** (EasyPost available, not connected) |
| Saved packages | Poly mailer; Waterproof Insulated Foil Thermal Bubble |
| Checkout rates | Standard $10.50, free over $500, 3–5 business days; local pickup |

**Labels are bought through Shippo, and Shippo supports signature confirmation
per label.** The capability exists one layer down.

1. **Set it in Shippo** — a default or per-shipment service option. Needs nothing
   from Lapis.
2. **Check Lapis's buy-label screen on the first real order.** Lapis may already
   pass Shippo's service options through; **there are no orders yet, so this
   could not be tested.**
3. **Ask Austin** to expose signature confirmation and insurance at label-buying
   time, with a rule like "require signature over $X". Add to the list already
   with him.

⚠️ **Do not write a signature requirement into the policy until one of those is
live.** A policy promising signature-on-delivery while labels ship without it is
worse than silence. The tracking line is the honest version of that protection
today.
