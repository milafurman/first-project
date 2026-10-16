# The Lapis console was redesigned — where things actually are now

Mila, 16 Oct: *"Where do I upload the logos? They changed everything. It no longer looks the
same."* She is right. Walked the new console and recorded what is where, because the old notes
no longer match.

## URGENT: there is an unpublished draft that would undo tonight's CSS

Design studio shows **"Draft: 1 change, not live yet"** next to a live **Publish** button. I
opened its Custom CSS box and read it. It is the **old stylesheet** — it still contains

```
footer{background-color:#0A192F!important;color:#FFFFFF!important}
```

which is the rule that left every footer line black on navy, and it is missing both the paired
footer text rules and the 17 per-product card colours added since.

**Pressing Publish overwrites the live Custom CSS with that older version.** Mila has been
warned and nothing has been touched without her say-so.

**Recovery is exact if it happens.** `truemg/storefront/live/customCss-blue.css` was verified
byte-identical to the live stylesheet on 16 Oct — same SHA-256 prefix `acc3c2efc1108add`, 4,063
characters, 48 rules. Re-apply it with `apply_design_change`.

**Offered, not done:** paste the current live CSS into the draft's Custom CSS box and "Save to
draft", which makes Publish a no-op for styling. Awaiting her answer.

## The logo: uploadable, but not settable

Checked all three plausible places.

| Place | What is actually there |
|---|---|
| **Settings → General → Brand identity** | the logo as a **read-only thumbnail**. The only Replace/Remove pair is for the **favicon**. Links out with "Edit in Appearance" |
| **Design studio → Manual controls** | Custom CSS, Colours and sizes (incl. **Logo size**), Home sections, Other parts. **No upload** |
| **Online store → Media library** | **Upload images** button, an "Add an image from a link" box, and tabs All / Uploads / Product photos / **Logos** / From links / Made with AI |

Opening a logo tile offers **Copy · Hero background · Phone hero background · Hero image**.
**There is no "set as logo" action anywhere I could find.**

**So:** uploading is Media library → Upload images. *Changing which logo the store uses* appears
to be possible only by asking the Design studio AI to swap it to one already in the library.

**20 images sit in the Logos tab already**, including lizard-mark variants and what appears to
be a white version.

## This settles the footer-logo question

There is **one logo slot, not two** — confirmed by the absence of any second control and by the
Brand identity panel showing a single image. A plain white wordmark would go **white-on-white in
the header**. So the footer's white box needs either a CSS treatment from here or a logo file
with its own background, not a white PNG.

See `../storefront/copy/SAM-FEEDBACK-15OCT.md`, where the earlier claim of a separate footer
slot was already withdrawn. This is the positive evidence for that withdrawal.

## Other things visible on the new dashboard

- **1 unread message from Sam**, 6h old, via the contact form. Flagged to her.
- **Low stock: 17** — every product. Still Sam's.
- **Setup checklist 4 of 5**: the outstanding item is **Upload lab results**, "0 of 17 live
  products have a COA". That is the single highest-value thing left on the whole store.
- **AI design credits:** 553 of 5,000 used this month.
- **Vial studio** still appears in the nav under Products. **Do not open it** — standing rule,
  it generates label text.

## Why the AI editor kept refusing her

Its own transcript, read on the Appearance page, shows it declining her edits with: *"this store
has no certificate of analysis on file yet"* — it blocks any claim about testing, purity or
analytical method, plus shipping speed and packaging wording, until a COA exists.

**Worth knowing:** the same claims went through fine via `apply_design_change`. The API and the
in-console AI do not enforce the same gate. Not a thing to exploit — it is a reason the COA
upload matters, and one for Austin.
