# The legal pages — checked properly, 14 Oct 2026

> ## ⚠️ CORRECTION
>
> An earlier version of this file said **"Terms of Service is EMPTY — 0
> characters"** and called it the project's top priority. **That was wrong.**
>
> `legalTermsBody` being empty means *no override* — **Lapis serves a default
> Terms page**, and it is substantial: **1,383 words**, structured, *Last updated
> July 2026*, with sections for Who Operates This Store, Research Use Only and
> Buyer Eligibility. Read live at `/legal/terms`.
>
> The mistake was reading a database field and never loading the page. **Do not
> conclude a page is empty from an empty copy key** — on this platform an empty
> key means the theme default applies.

## The three pages, as a customer sees them

| URL | Title | Source | Words |
|---|---|---|---|
| `/legal/terms` | Terms of Service | **Lapis default** (no override set) | 1,383 |
| `/legal/refunds` | Shipping & Refund Policy | **Mila's own text** | 209 |
| `/legal/privacy` | Privacy Policy | Mila's own text (852 chars stored) | — |

All three return **200**. They are linked from the footer as *Shipping &
Returns*, *Terms*, *Privacy Policy* and *Terms & Conditions*, and Lapis does not
allow those links to be removed.

⚠️ Note the URL pattern is **`/legal/<name>`**. Guessing `/terms`,
`/privacy`, `/shipping-refunds` returns 404 — which is what produced the first
wrong reading of this. Get hrefs from the rendered footer, never guess slugs.

## What is genuinely worth fixing

> **Status, 14 Oct:** items 1 and 2 are **drafted and validated, awaiting one
> paste** — see `../copy/APPLY-REFUNDS-UPDATE.md`. The replacement
> `legalRefundsBody` was dry-run through `preview_design_change` and accepted
> with no rejections, and the paste block is byte-identical to the validated
> string. Item 3 remains a human job.

### 1. The refund deadline is stated two different ways

| Where | What it says |
|---|---|
| `/legal/refunds` | a claim must come *"within a reasonable window of delivery"* — **confirmed: the page contains no number at all** |
| FAQ, "What if a vial arrives damaged?" | *"email us **within 48 hours** of delivery"* |

A claim on day four sits inside one and outside the other. The FAQ's 48 hours is
the tighter, more useful rule; if that is the real one, `legalRefundsBody`
should say 48 hours rather than "reasonable". **One-line edit, needs Mila to
confirm the number.**

### 2. The policy never uses the word "return"

It covers transit damage and fulfilment error only. There is no stated position
on an intact order someone simply does not want. For laboratory reagents a
no-returns stance is defensible — but it should be said, or support fields the
question with nothing to give. Note the footer link is labelled **"Shipping &
Returns"**, which promises a returns position the page does not contain.

### 3. Worth Mila reading once: the default Terms are generic

They are real and they are better than nothing, but they are Lapis's boilerplate
rather than written for a research-compound store. Worth one read-through by
someone qualified to check the research-use restriction, the buyer undertaking
and the liability limit say what TrueMG needs them to say. **Not urgent, not
empty, not a crisis** — which is the opposite of what this file said before.
