# Site writing — the backlog, worst gap first

Mila, 15 Oct: *"Do one task at a time and just do all the verbiage, all the content, all the
writing for the site."* Each item gets written, applied, and verified on the live page before
the next one starts.

| # | Task | Where | Status |
|---|---|---|---|
| 1 | Coming-soon page | `comingSoonHeadline/Sub/Cta/Note` | **DONE 15 Oct — verified signed-out** |
| 2 | Contact page | 7 `contact*` keys | **DONE 15 Oct — verified live** |
| 3 | Technical specifications | per product, Lapis admin | next — needs Chrome |
| 4 | Shipping & delivery detail | `legalRefundsBody` + FAQ | **blocked — needs facts from Mila** |
| 5 | Lab Results page body | `labIntro` + surrounding | to do |

Order note: specs were meant to be #2, but the Chrome tab wedged mid-navigation, and specs are
per-product admin work that needs it. Contact was done instead because it is API-reachable and
needed no facts from anyone. Specs resume when Chrome recovers.

## 1. Coming-soon page — done

It was entirely unwritten: all four fields empty, so the page rendered Lapis's default
*"Something new is coming."* with a bare email box. **This is the only page the public can
reach** while the curtain is up, so it was the highest-impact writing on the site.

Now live:

- **Headline:** Research compounds, documented to the lot.
- **Sub:** Reference-grade compounds for in-vitro laboratory research, with independent identity
  and purity analysis filed to the lot number on each vial. Leave your address and we'll tell you
  when the catalog opens.
- **Button:** Tell me when it opens
- **Small print:** For laboratory research use only. Not for human or veterinary use. One email
  when the catalog opens — nothing else, and you can leave at any time.

Within the field limits — 120 / 220 / 40 / 200. Research-use framed, no outcome or human-use
claim, no shipping promise, no certificate claim beyond what the rest of the site says. Verified
by clearing the preview cookie and loading the site cold, which is what a stranger gets.

Deliberately left alone: `comingSoonBg` and `comingSoonImageUrl`. The background image is
Codex's now — see `truemg/assets/IMAGE-SPECS.md`.


## 2. Contact page — done

Six fields were empty and the intro was generic. Now live and verified:

- **Intro** rewritten to say who the store serves and, deliberately, what it will not answer:
  *"We do not advise on what to do with research material, and we cannot answer questions about
  use in a person or an animal."* That limit belongs on the contact page more than anywhere —
  it is where someone would ask.
- **"What we can help with"** — seven real topics, rendering as a ticked list: a certificate for
  a specific lot, documentation questions before ordering, a compound not in the catalog, volume
  pricing from ten vials, order status and tracking, a damaged parcel or fulfillment error,
  laboratory and institutional account setup.
- **Form intro:** asks for the order or lot number up front, which saves a round trip.
- **Confirmation** after sending, which was previously the theme default.
- **A second button, "Read the FAQ first"**, pointing at `/faq`, to deflect what the FAQ already
  answers.

Left empty on purpose: the whole text-us band (`contactBandPhone` and friends). Empty hides it,
and there is no number to publish. Do not invent one.

## 4. Shipping detail — what is actually blocking it

The QA sweep was right that a buyer gets no shipping information beyond "48 hours". But the
missing pieces are **business facts, not copy**:

- What shipping costs, and whether it is free over a threshold
- Which countries are served, and which are excluded
- Which carrier, and whether signature on delivery is available
- Who pays customs and duties on an international order

There is no dedicated shipping page on this platform — it all lives in `legalRefundsBody`, which
is already written with everything that *is* established: 48-hour business-day dispatch, next
business day over weekends and holidays, tracking at handover, carrier tracking as the record,
plain packaging, the damage-claim process.

Those four answers are all that stand between it and being complete. Writing a guess there would
be worse than the gap.
