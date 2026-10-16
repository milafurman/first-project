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

---

# The logo cannot be changed from this console at all (16 Oct)

Mila: *"I don't want the original footer I want the new one with the correct damn logo from the
drive."* The footer half is done. The logo half is **blocked by the platform**, and here is
every place checked before saying so.

| Place | What it offers |
|---|---|
| Settings → General → Brand identity | three file inputs, mapped by reading their surrounding UI: **favicon**, **social share image**, **coming-soon background**. The logo is a read-only thumbnail |
| Design studio → Manual controls | Custom CSS · Colours and sizes · Home sections · Other parts. The only logo item anywhere is **"Logo size"** |
| Media library → a logo tile | Copy · Hero background · Phone hero background · Hero image |
| Layouts | no control. Its own text says *"colors, copy and logo stay editable in Appearance"* |
| **Design studio AI**, asked directly | **refused**: *"I couldn't change the logo. The store logo isn't one of the images I can edit here."* Cost 80 credits. It then gave contradictory advice — console settings in one sentence, *"the design studio's Logo control"* in the next. Neither exists |

**So Layouts points at Appearance, Appearance's AI points back at Settings, and Settings points
at Appearance.** There is no logo control at either end. This looks like a regression in the
redesign — **one for Austin.**

## What was achieved instead

**Both correct logos are now in the Media library**, under the "From links" tab, ready to pick
the moment a control exists:

- dark wordmark, 2169x725 — `brand-images/…import-1792118303650.png`
- white wordmark, 2168x725 — `brand-images/…import-1792118318708.png`

They came from the LOGOS folder in Drive (`trueMG labs Black.png`, `truemg labs white .png`),
unmodified, routed in through **"Add an image from a link"** off the public repo. Both confirmed
present after reload.

## The live logo really is the wrong file

Not a matter of taste — measured against the Drive original:

| | live on store | Drive original |
|---|---|---|
| size | 1200x231 | 2169x725 |
| aspect | 5.19 | 2.99 |
| blue | `rgb(0,128,192)` | `rgb(0,128,224)` |
| stray colours | ~2,400 px of pale lavender | none |

A flatter crop, under a third of the resolution, a duller blue, and some stray pixels. **Sam's
"logo is wrong across pages" was correct.**

## A quality scare that was not real

The white file previewed with heavy black speckling through TRUE and LABS and looked ruined.
**It is fine.** Checked the actual pixels: 78.5% fully transparent, 0.85% semi-transparent
(ordinary antialiasing), opaque pixels are 218,369 of near-white plus 106,142 of the brand blue.
The speckling was the image viewer compositing white-on-transparent against black. **Inspect the
pixels before calling a file low quality.**
