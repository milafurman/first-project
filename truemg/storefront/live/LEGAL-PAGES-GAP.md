# The legal pages — one empty, two contradicting each other

Checked 14 Oct 2026, prompted by Mila asking simply whether the site has a
return policy. It does. Two worse things turned up while confirming it.

## What is live

| Page | State |
|---|---|
| Shipping and Refunds (`legalRefundsBody`) | **693 characters, present** |
| Privacy (`legalPrivacyBody`) | **852 characters, present** |
| **Terms of Service (`legalTermsBody`)** | ⚠️ **EMPTY — 0 characters** |

Lapis forces these into the footer: *"Legal links (Terms, Privacy, Shipping and
Refunds, Research use only) are always shown and cannot be removed."* So the
Terms link **is** on every page of the store, pointing at nothing.

## ⚠️ 1. Terms of Service is blank, and the FAQ requires agreement to it

The FAQ answer to *"Who is allowed to order?"* reads:

> Orders are accepted from qualified researchers and laboratory or institutional
> accounts who are at least 18 years of age and **who accept the Terms of
> Service.**

Customers are being asked to accept terms that do not exist. On a
research-compound store this is the page least able to afford being empty — it is
where the research-use-only restriction, the buyer's compliance undertaking, the
age gate and the limitation of liability normally live.

**This outranks every design task in the project.** It is also not a copy problem
to be solved by an agent: it is the one page that should be written or reviewed
by someone qualified, because it is the document a dispute turns on.

## ⚠️ 2. The refund deadline is stated two different ways

| Where | What it says |
|---|---|
| `legalRefundsBody` | a claim must be submitted *"within a reasonable window of delivery"* |
| FAQ, "What if a vial arrives damaged?" | *"email us **within 48 hours** of delivery"* |

A claim on day four is simultaneously inside the policy and outside the FAQ.
Pick one number and make both say it. The FAQ's 48 hours is the tighter and more
useful of the two; if that is the real rule, the refunds page should say 48
hours, not "reasonable".

## Also worth noting

The refunds text never uses the word **return**. It covers damage in transit and
fulfilment error only — there is no stated position on an unwanted-but-intact
order. For laboratory reagents that is a defensible stance, but it should be
said out loud rather than left as a silence, or support will field the question
with no answer to give.

## Status

**Not fixed, deliberately.** Terms of Service needs a human with the
qualification to write it. The 48-hour inconsistency is a one-line edit in
`legalRefundsBody` once Mila confirms which number is real.
