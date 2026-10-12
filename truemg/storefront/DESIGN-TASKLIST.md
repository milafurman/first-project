# Getting TrueMG to Nurish / Amino Club calibre

Written 12 Oct 2026 against the live store, both reference sites, and the
assets already in this repo. Every claim below is measured, not impressions.

**Channel key** — who can actually do each task:
`MCP` the Lapis connector (copy keys, palette, customCss) ·
`ADMIN` the Lapis admin UI, a human at a browser (uploads, product data) ·
`BUILD` a script in this repo (asset generation)

**One hard sequencing rule.** A Design studio save (logo, favicon) **wipes
customCss**. Product image uploads do not. So: logo/favicon first → product
images any time → stylesheet apply LAST.

---

## The honest diagnosis

The site does not look AI because AI touched it. It looks AI because of five
specific, measurable things. Worth knowing up front: **Nurish's vials are
AI-generated too** — their files are literally named
`ChatGPT-Image-Sep-1-2026-04_04_03-PM-4-300x300.png`. The gap is craft, not
provenance.

**1. Every product description is the same sentence.** Six of six checked:

> TESAMORELIN — "Tesamorelin **is a** synthetic peptide analog **classified within** the GHRH…"
> IPAMORELIN — "Ipamorelin **is a** pentapeptide **classified within** the growth-hormone secretagogue family…"
> GHK-CU — "GHK-Cu **is a** copper-binding tripeptide complex…"
> KLOW — "KLOW **is a** research-formulated blend combining…"
> BPC-157 + TB-500 — "BPC-157 + TB-500 **is a** combination research blend…"
> CJC-1295 + IPAMORELIN — "CJC-1295 (No DAC) + Ipamorelin **is a** combination research blend…"

`[NAME] is a [noun phrase] classified within [family]`, every time. Nurish
writes nine words: *"Triple-agonist research peptide — the newest in its class."*
This is the single loudest tell on the site.

**2. Seventeen product shots, seventeen different background colours** — sage,
dusty pink, lavender, grey-blue, cream, mauve — and not one of them is the brand
blue. Each sits on a defocused "ledge" with a mystery horizontal rail and a
mushy fake reflection. Nurish uses one transparent background for the entire
catalog. Our own `vials/README.md` already admits it: *"these are still shot
dead-straight, centred and flat."*

  **And the ready-made replacements carry the wrong blue.** `cut/src` and
  `tinted` both sample `#2365CD` — legacy, flagged in `brand.json`. Re-render
  before upload. See 1B.1.

**3. Product images render at 1.86×.** 640×640 natural into a 344×344 box. Below
2× they are visibly soft on any retina screen. Nurish serves 600×600 into ~200px
— a 3× buffer. Soft edges read as "generated" even when the art is fine.

**4. The cards carry almost no information.** Nurish's card holds purity `99.5%`,
a `View COA ›` link, a mechanism eyebrow, the name, a one-line description, size
chips `10mg · 30mg`, `From $99.00` and `Add to bag` — before a single click.
Ours holds a name, an encyclopedia sentence, a price and a button.

**5. The vial label fights itself.** `TRUEMG` runs vertically up the right side
of the label in the largest type on the artwork, while the actual product name
sits small and tucked into the top-left. Nurish inverts it: brand small at top,
**product name large and centred**, mg in a boxed chip, purity line, research-use
line, hairline rules — one centred axis, top to bottom.

---

## Phase 0 — Reconcile the main design (blocks nothing, but do it first)

- [ ] **0.1 `ADMIN` Make Meridian the main design.** `/admin/templates` still
  holds `arcane` as the revert target. "Meridian" is this admin's display name
  for template `revive` — see `NOTES.md`. Click *"Make this my main design"* on
  the Meridian card, **not** "Return to my main", which would apply `arcane` and
  destroy half the copy keys and every `.lf-section-*` rule.
  Capture `customCss` before clicking; restore after if it wipes.

---

## Phase 1 — The four things Mila called out

> **Applied live 12 Oct 2026.** The styling pass shipped: card field, catalog
> title, FDA heading, Lab Results panel, dead rule removed, banner slowed and
> cut to one message, second marquee hidden. The entry gate (1D.6) was held
> back deliberately — it has no stable class to target, so any rule risks
> leaking onto buttons and cards elsewhere, and it is under attorney review.

### 1A. The scrolling banner (too fast)

- [x] **1A.1 `MCP` Slow the marquee.** `announcementBarSpeed` is currently `26`.
  Determine the unit by dry-running `40` and `60` and measuring the loop, then
  set the value that lands near a comfortable reading pace. Amino Club's bar does
  not race.
- [x] **1A.2 `MCP` Kill one of the two marquees.** There are two scrolling
  strips stacked above a white header: `announcementBar` and `promoStrip`. On a
  phone the announcement wraps to two lines and the pair eats the first ~100px
  of every page. Keep one. Recommend keeping `announcementBar` and setting
  `hide:promoStrip` to `1`.
- [x] **1A.3 `MCP` Give the bar one job.** Three claims separated by `·` is a
  list, not a message. Amino Club runs one offer plus a deadline. Ours should
  run the single strongest line — the lot match.
- [ ] **1A.4 — open question for Mila.** Amino Club's bar carries a *live
  countdown* ("Ends in 10d 02h 37m 19s"). Lapis has `announcementBarStartsAt` /
  `announcementBarEndsAt`; whether it renders a ticking clock is untested.
  **Do not ship a countdown we cannot honour** — a timer that resets forever is
  an FTC problem, and theirs works because their rotation is real.

### 1B. The vials (ours look generated, Nurish looks smooth)

The reference is not photography. It is a **repeatable render**: one master
vial, frontal, zero perspective, identical bounding box in every frame, label
typeset as crisp type directly on teal glass, transparent background. The glass
colour *is* their brand colour.

- [x] **1B.1 Checked 12 Oct 2026 — the shippable vials are ALREADY correct.**
  All 17 at `truemg/assets/vials/tmg-*.png` sample top blue `#1C8CD0` with
  **zero** legacy-blue pixels, 2000x2000 RGBA, 60-90% transparent. Re-running
  `render.py` reproduced them identically, so no re-render is needed.
  An earlier note here claimed otherwise; that was wrong. The legacy `#2365CD`
  lives only in `cut/src/*.png` — the ORIGINAL PHOTOGRAPHS, which are inputs to
  `render.py`, not outputs, and are correctly pre-rebrand — and in the older
  `tinted/` treatment. Neither ships.
  Note: `render.py` needs `scipy`, which is not in the system Python.
- [x] **1B.2 `ADMIN` 14 of 17 uploaded and live — 12 Oct 2026.** Verified on the
  rendered catalog: 14 `.png` against 3 `.jpg` across 17 cards. Each product was
  title-checked at upload, so the exact-text row matching correctly separated
  `IPAMORELIN` from `CJC-1295 (No DAC) + IPAMORELIN`.
- [ ] **1B.2b `ADMIN` The three multi-size products are the per-size-photo trap.**
  SS-31 (10/50MG), TMG-2TZ (10/20MG) and TMG-3RT (10/20MG) each have sizes that
  **already carry their own photos**, and Lapis says plainly: *"the storefront
  swaps the product image when a shopper picks that size. Sizes without a photo
  use the main product picture."* Replacing only the main picture would leave
  their cards unchanged — which is exactly why the other 14 were safe, their
  size slots being empty. Three ways out, in preference order:
  **(a)** render per-size vials — `labels.py` already holds the per-size label
  artwork, so `render.py` can emit a 10MG and a 50MG variant for their own
  slots. Only option where the picture matches the size selected.
  **(b)** clear the size photos so all sizes fall back to the new main picture —
  fast, but every size then shows the same mg on the label.
  **(c)** leave them on the old ledge photo.
  **How to drive a Lapis upload from a session:** the file inputs are hidden, so
  surface them first (set `aria-label` + a visible style via JS), then `find`
  that label and `file_upload` with `paths` — the client reads the file, so no
  base64 passes through context. Staging the file is not enough: click that
  card's own Upload button, then Save.
- [ ] **1B.3 `BUILD` Re-render at 3× density.** Cards display at 344px, so ship
  ≥1024×1024 and let Lapis downscale. Current 640px is the softness.
- [ ] **1B.4 `BUILD` Rebuild the label composition.** Product name large and
  centred; `TRUEMG` small above it; mg in a boxed chip; hairline rules.
  **Constraint: the label text itself must come from the approved artwork in
  `truemg/assets/labels/side/*.svg` — never generated.** This task is layout
  only. Nothing on the compliance block changes wording.
- [ ] **1B.5 `ADMIN` Upload all 17.** The connector cannot upload files.
  Watch the per-size-photo trap: a size's own photo beats the product's main
  picture on the catalog card.
- [ ] **1B.6 `MCP` Drop the white card backdrop.** `.lf-card .aspect-square` is
  pinned to `#fff`. With transparent vials, give each card a soft tinted field
  instead — Amino Club keys the field to each vial's own colour and it is the
  single biggest reason their grid looks designed rather than stocked.

### 1C. The logo and the Gila

**Corrected 12 Oct 2026.** An earlier note here claimed the hairline rule cut
88px through the Gila. It does not: measured by colour, the rule runs x245–1199
and the mark ends at x176 — a **69px gap**. That figure came from measuring a
horizontal band that contained both objects. "LABS" is also fine: dead centre
under TRUEMG, 0.0px off.

**The actual site fault is that the wrong file is live.** The header PNG is a
byte-exact match for `truemg-lockup-mark-light-1200.png`, but `render_png.mjs`
states the markless pair is the web lockup *"on purpose: the Gila mark belongs
on the browser tab and the vial, not in the site header."* Its 23px-left /
0px-right asymmetry is what reads as misaligned.

- [ ] **1C.1 `ADMIN` Decide and upload.** Either `truemg-lockup-light-1200.png`
  (markless, as the pipeline intended — one upload, question closed) or keep the
  mark and rebuild its optical alignment first. **A Design studio save wipes
  customCss — re-apply the stylesheet straight after.**
- [x] **1C.2 `BUILD` Label lockup — DONE.** The vertical lockup sat at
  x49.30–54.80 against a wrap line at x51.50, so **LABS printed entirely inside
  the strip that curves out of sight** and TRUEMG lost its last quarter — which
  is why the vial photo reads "TRUE M". Position is now derived from the
  lockup's own depth: x46.00–51.50, zero overhang, guarded by an assertion.
- [x] **1C.3 `BUILD` `fit()` ignored letter-spacing — DONE.** 29 characters at
  0.1mm tracking is 2.9mm the width estimate never counted, so the slogan was
  overrunning its column by 2.2mm. Hidden until 1C.2 moved the wordmark left.
  Fixed for the slogan, LOT line and compliance block, with a guard.
  Latent but harmless in the top layout — measured, nothing overruns.
- [ ] **1C.4 Gila size on the label is already maxed at 11mm.** 13mm and 15mm
  are rejected by the layout's own collision guard against the compliance
  block; only 11.2mm of vertical space exists. Bigger needs a layout rework.
- [ ] **1C.5 ⚠️ CONFIRM THE PRINT SPEC.** `labels.py` says it in capitals.
  Trim 60×30mm, bleed 3, safe 2.5, wrap 9 — unchanged from what already
  shipped, but every number above moves if the printer's spec differs.

### 1D. Overall UI/UX quality

- [ ] **1D.1 `ADMIN` Rewrite all 17 product descriptions.** The one-sentence
  skeleton is the loudest AI tell and **the MCP cannot reach it** — product data
  is out of the connector's scope. Target: one specific line each, under
  ~15 words, no "is a … classified within". Research-use framing intact; no
  mechanism-in-a-person claims.
- [x] **1D.2 `MCP` Fix the catalog type scale.** Catalog `h1` is 36px with 0px
  top padding and no max-width container, where About, FAQ and Lab Results are
  all 48px / 80px / 768px. The commercial page is the least considered one.
- [x] **1D.3 `MCP` Raise the 10px "FDA & Legal Disclaimer" heading** on catalog
  and FAQ. It is in the page body, not the protected footer, so it is
  restyleable.
- [x] **1D.4 `MCP` Delete the dead rule.** `.lf-section-hero img[src*="hero-media"]`
  matches nothing — `heroMediaUrl` is now `pixel.png`. The `float` animation
  rides nothing.
- [x] **1D.5 `MCP` Make Lab Results look deliberate.** Decent bones already
  (intro, empty notice, CTA, a 4-step explainer) sitting as a grey box in a lot
  of white. Give the notice the tinted-panel treatment the home page uses and
  let the 4-step explainer carry weight, so the page earns its place before a
  single COA exists.
- [ ] **1D.6 `MCP` Redesign the entry gate.** Both references solve this the
  same way and ours does none of it:

  | | Nurish | Amino Club | TrueMG today |
  |---|---|---|---|
  | Logo on the gate | yes | yes | **no** |
  | Heading | "You must be 21+ to enter" | "Researcher verification" | a 10-line paragraph |
  | Confirmation | one checkbox | two checkboxes | none |
  | CTA | disabled until checked | disabled until checked | always live, black |
  | Decline | tiny "Exit site" text link | tiny "Exit" link | a pill nearly as loud as accept |
  | Brand colour | yes | yes | **none — pure black/white** |

  CSS-reachable without touching a word: brand-blue accept button, demote
  "Leave" to a text link, add a size/colour step between the two paragraphs,
  tighten the measure. **The legal wording is under attorney review — do not
  edit it.** A checkbox + disabled CTA is a theme capability question for Lapis,
  not CSS.
- [ ] **1D.7 `MCP` Borrow Amino Club's motion.** Their gate floats their own
  vials behind it on two layers: a slow vertical drift (26–38s linear) plus a
  small bob (`float` 4–5s ease-in-out). Our theme already ships a `float`
  keyframe. **Custom `@keyframes` are stripped while `animation:` survives**, so
  only theme keyframes work — and never override `animation` on
  `.lf-section-hero .justify-center`, which would make the hero invisible.

---

## Phase 2 — What Nurish and Amino Club do that we have not attempted

Ranked by likely commercial impact. Several are owner-side, not design.

- [ ] **2.1 `ADMIN` Purity number + "View COA" on every card.** Both references
  show the number before the click. We own the proof and we are hiding it behind
  a page.
- [ ] **2.2 `ADMIN` Anchored pricing.** Neither reference ever shows a bare
  number. Struck compare-at, live price, a `-40%` corner badge. Still the single
  biggest missing selling mechanic.
- [ ] **2.3 `MCP` Mechanism eyebrow on the card** — Nurish's
  `TRIPLE GIP/GLP-1/GLUCAGON RECEPTOR AGONIST` in small caps above the name.
  Classification, not an effect claim, so it stays compliant.
- [ ] **2.4 `MCP` Asymmetric sections.** Both references bleed an image to one
  edge against copy on the other. We are a stack of centred boxes. Note the
  Lapis limit: there is **no full-bleed** — `clip-path`, `overflow` and `-50vw`
  margins are all blocked, so this is tinted rounded panels, not true bleed.
- [ ] **2.5 — Server rendering.** `/admin/experiments` says the store builds
  itself in the visitor's browser. That is the likely cause of the one-in-four
  blank cold load, and it blocks A/B tests. **A support request to Lapis, not a
  setting.**

---

## What Lapis cannot do, so nobody wastes a day on it

- **No full-bleed sections.** `clip-path`, `overflow`, `position`, `inset`,
  `z-index`, `filter`, `transition`, `backdrop-filter` are all rejected.
- **No custom animation.** `@keyframes` blocks are stripped while `animation:`
  is kept, so a custom animation validates, saves, reports the right
  `animationName` and does nothing. Theme keyframes only: `float`, `pulse`,
  `bounce`, `spin`, `rev-fade-up`, `fade-up`.
- **The connector cannot touch product data or upload a file.** Descriptions,
  prices, purity fields and images are all `ADMIN`.
- **The footer is protected.** Colours must be set as a pair with `!important`;
  its text cannot be resized, faded or moved.
- **`customCss` caps at 10,000 characters** (2,029 used) and preview URLs die
  around 8,000.

### 1E. Canva label artwork — the live labels

The print PDFs in `truemg/assets/labels/` are a *different* artifact from the
labels that actually go on the vials. The live ones are the Canva design
`DAHXw-xpMJk` ("Copy of TRUEMG Labels", 20 pages, 1654×593). Edits there do not
come back to this repo — this section is the record.

- [x] **1E.1 Brand blue on all 20 pages — DONE 12 Oct 2026.** Every page carried
  the legacy `#2365CD` family, confirmed two ways: Canva's stored values read
  `#2365cd`, and pixel-sampling the rendered label gave `#2467ca` / `#276ac9` /
  `#3265b2`. The tell is the green channel — 140 on brand blue against 101–130
  on the legacy one, which is why it passes as "blue" at a glance.
  Now `#1C8CD0` on **three** elements per page: the product-name text, the Gila
  mark and the MG half of the vertical wordmark. **TRUE stays black** — it is a
  separate element and was never wrong. Verified page by page at zoom, then
  across all 20 thumbnails in grid view. Canva reports all changes saved.
  **Do not verify this through `read-design` thumbnails** — they lag the
  document badly. Page 20's came back on render version 6 against a design
  on version 32, flagged `fallbackstale=T`, and showed the *old* blue on the
  MG. Re-checking page 20 live in the editor at zoom showed correct brand
  blue. The stale thumbnail was the only thing wrong.

- **How it had to be done.** The Canva *API* refuses this: `recolor_element`
  returns `not_permitted` on images, so the Gila and the MG block — both images,
  not text — are unreachable from the connector. The *editor* does both fine.
  Drive it through Chrome.
  - Text took one pass: the colour panel offers **"Change all"**, which recolours
    that text colour across every page at once. There is no equivalent for
    images.
  - Images are one element at a time, 36 of them. The loop that works:
    screenshot → click the element → click the toolbar swatch **as its own tool
    call** → click the "From your search" swatch → verify by zoom. The hex
    persists in the picker's search field between elements.
  - Two traps. The canvas re-zooms and re-scrolls on every selection, so
    coordinates must be re-read from a fresh screenshot each time — batched
    clicks land on empty space and fail *silently*. And a swatch click issued in
    the same batch as the selection click never registers; it needs its own
    round trip.

- [x] **1E.2 The batch field — DONE 12 Oct 2026.** `BATCH:` plus an empty line
  to write on, on all 20 pages, at (left 1040, top 455): the open right margin
  beside the wordmark, first line level with the compliance block. 28px bold
  `#070707`, matching the compliance block's size and colour.

  **No batch number was invented.** The field is blank by design — the value is
  per print run and is not AI's to write.

  **Where "the right" actually is.** The artwork occupies only x 602–1015 of a
  1654px canvas, roughly centred, so there is ~640px of empty canvas to its
  right. The wordmark is the rightmost artwork at x 926.68–1003.46 (both halves
  are rotation-90 rects; rendered extents come from the centre, not top/left).
  The margin was chosen over the one print-guaranteed gap — inside the artwork,
  right of the Gila at x 742–926 — on Mila's explicit call.

  ⚠️ **Unresolved: whether that margin prints.** The repo's approved side label
  is 66×36mm (1.83:1); the Canva artwork region is 413×487px (0.85:1). They do
  not correspond, so the repo cannot locate Canva's trim. If the printer crops
  to the artwork, the batch field falls off the label. **Settle this with 1C.5
  (Sam's spec).** Moving it inside is one `position_element` call.

  **Font mismatch, accepted.** The label is `fontRef YAFdJvSyp_k,3`; API-added
  text can only be Canva's default `YACgEZ1cb1Q,0`. `format_text` has no font
  family. Size, weight and colour were matched to narrow the gap. To make it
  exact, restyle the 20 elements by hand in the editor.

  **What made this tractable via the API.** One `edit-design` call carries
  operations for *many* pages — `page_index` only selects which page's document
  comes back, it does not restrict the ops. 20 pages took one add call, one
  format call. But `add_text` does not return the new element's locator_id for
  any page other than `page_index`, so the ids have to be collected with
  `read-design` before formatting.

- [ ] **1E.3 The label wordmark is not in the logo set.** Raised 12 Oct 2026.
  Each label carries two logo pieces: the Gila mark (correct — the standard
  mark, now in brand blue) and a **vertical** TRUE MG with **no LABS**. The
  vertical one matches no file in `assets/logo/`.

  Checked by viewBox across all 26 logo SVGs — **every one is wider than tall**,
  so nothing vertical exists anywhere in the set:
  - marks `1600×1600`
  - wordmark, no LABS `5634×681`
  - with LABS `5634×1086`
  - full lockups, mark + text `7078×1260`

  So the non-standard thing is the **orientation, not the missing LABS** — a
  LABS-less wordmark is already sanctioned, it is just horizontal. An earlier
  note that said every official version carries LABS was wrong.

  The label's source image is also not the official wordmark: its fill box is
  ~`534×267` (2:1), against the official wordmark's 8.27:1. Two crops of that
  one 2:1 image give the black TRUE and the blue MG, so it is a stacked
  two-line composition made for the labels and nothing else.

  Decision is Mila's: leave it (it fits the vial better than a wide lockup),
  add LABS to it, or rebuild the label around the official horizontal lockup.
  If LABS is added, note 1C.2 — it previously landed in the wrap strip that
  curves out of sight.
