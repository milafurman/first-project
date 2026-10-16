# Sam's review notes — checked, sorted, 15 Oct 2026

Each item below was verified on the live site or in the admin before being answered. Who owns it
is marked, because several are not writing problems at all.

## 1. "Black footer font is hard to read" — it is not the font

**Checked:** measured every text element in the footer against its background. **Zero** fall below
the readable threshold; body text runs about 11:1 and links about 14:1. The contrast fix from
earlier today is holding. Re-confirmed 15 Oct on the live FAQ page — footer still navy
`rgb(10,25,47)` with body text `rgb(195,211,228)`.

**A measurement I nearly reported wrong.** A first reading put the footer logo at an effective
height of **10 pixels**, which would have been a serious defect. A screenshot showed it
rendering correctly at 182x40 inside its box. The first number came from measuring during a
transient layout state. **Screenshot before reporting a sizing defect** — the geometry can lie
mid-layout.

**What he is actually looking at:** the footer logo. It sits in a **white rounded box** with the
dark wordmark inside it, on the navy footer. It reads as a sticker, and the black letters in it
are the "black font".

**Fix — with one claim corrected, 15 Oct.** I previously wrote that Lapis has a separate
footer-logo slot so the header could keep the dark mark. **I could not verify that**, and it
should not be relied on. What is verified: the live site serves **one file to both** header and
footer, and there is **no logo key in the API at all** — it is an admin upload only.

So before uploading a white wordmark, check the admin for a *second* slot. If there is only
one, a white logo would disappear against the white header. Options in that case: keep the
white box as it is (it is legible — see the measurement below), or have me recolour the footer
mark with CSS, which is mine to do and needs no upload, though it would turn the blue "MG"
white as well.

## 2. "Logo is wrong across pages (header and footer, FAQ)" — one file, not three

**Checked, and re-verified 15 Oct by reading the image URLs off the live pages.** Header,
footer, FAQ and the home page all load the identical file:
`brand-logos/9d58c6be-60d7-4e06-90ff-c93d17e9990e-1791788391380.png`, 1200x231, transparent
PNG, black `TRUE` / blue `MG` / black `LABS`. **One upload corrects every page.**

Whether it is the *older* wordmark I am taking from Sam, not from my own comparison — I cannot
reach his folder from here to diff them. **Mila's hands** either way: there is no logo key in
the API.

## 3. "A product photo with backdrop may show the wrong vial" — he is right, and here is the one

**Checked three products:**

- **EPITHALON** — two pictures. Clean vial, plus one on a grey surface. Both EPITHALON 10MG. Match.
- **GHK-CU** — two pictures. Both GHK-CU 50MG. Match.
- **SS-31** — **three** pictures. The clean vial plus **two** backdrop shots, and **both are
  labelled 10MG**. SS-31 sells in 10MG and 50MG, so one of those is almost certainly standing in
  for the 50MG and showing the wrong strength. **This is the defect he spotted.**

**Also worth knowing:** only the **first** picture ever appears on the storefront. Verified on the
live EPITHALON page — one product image renders, the backdrop ones never show. So deleting the
backdrop photos changes nothing a customer sees.

**Recommendation:** delete every backdrop photo on all 17 products. They are invisible, at least
one is wrong, and they are a trap for whoever next assumes picture two is correct. Deleting a
product image is **admin-only — Mila's hands.**

## 4. Footer line "In vitro research only, not for human or veterinary use" — keep it

Whether it is strictly required is a lawyer's question, not one to settle from here. But it is the
standard line for this category, and the standing rule is research-use wording on every page.
Removing it makes the position weaker, not tidier. **Leave it; ask a lawyer if he wants certainty.**

## 5. "Analyse lot by lot" — already live

On the home page trust row. No action.

## 6. "Lab Results verbiage too minimal" — needs a steer, and there is a hard limit

**Checked every key on the store:** that page has **one** editable paragraph. The eyebrow, the
"Lab Results" heading, the "No Certificates of Analysis are published yet" box, the Browse catalog
button and the whole four-step "How documentation is posted" block are **theme-generated with no
key behind them.** Sections cannot be added.

The paragraph was rewritten today to say what a certificate actually contains — identity, purity
as a percentage with the method beside it, filed to the lot on the vial.

**Needed from Sam:** what he wants to see there. If the answer is "the certificates", that is the
COA upload, not copy.

## 7. "Design feels too bloggy" — needs one sentence from him, but partly answered

Too much text? Too soft a palette? Too little product on screen? Not actionable as written.

**Partly answered since:** the About page now ends with a published reference list — 21
citations, identity and method papers only, every one checked against PubMed's own record,
with the five compounds that have no usable citation named as such. Whatever "bloggy" turns
out to mean, that section is the opposite of it: it is the most checkable thing on the site.
See `CITATIONS-VERIFIED.md`. His one sentence is still worth having.

## 8. "All catalog bottle images need replacing" — already with Codex

Nineteen cutouts outstanding, three prioritised. See `truemg/assets/IMAGE-SPECS.md`.

---

## Summary of ownership

- **Mila (admin uploads):** white footer logo · replace the main logo · delete the backdrop photos
- **Sam:** what he wants on Lab Results · what "bloggy" means · stock · the vial set
- **Codex:** the nineteen cutouts
- **A lawyer:** whether the research-use line is mandatory
- **Already done:** footer contrast, "analyse lot by lot", Lab Results paragraph, the
  About-page reference list
