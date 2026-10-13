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

### 1G. ⚠️ The store is unreliably slow, and when it is slow it shows a BLANK page

Measured 12 Oct 2026, five consecutive loads of `/catalog?peek=1`, cache-busted,
reading `domContentLoadedEventEnd` from the browser's own navigation timing:

| Run | Time to DOM ready |
|---|---|
| 1 | **21.1 s** |
| 2 | 3.8 s |
| 3 | 1.9 s |
| 4 | 1.1 s |
| 5 | **11.8 s** — still 15 characters of text after 10 s of waiting |

**Two of five took over ten seconds.** On the slow runs the page is not a
spinner or a skeleton — it is blank white. The home page `/store` did the same
thing twice in a row, then filled in somewhere between 10 s and 15 s.

**It is not the connection and not the hosting.**
- Control: `example.com` in the same browser, same minute — **0.22 s**.
- Time to first byte on the slow runs — **93 ms**. The server answers instantly.

So the delay is entirely client-side, after the HTML arrives. No console errors
were captured.

This almost certainly outranks every cosmetic task in this file: a visitor who
gets a blank page for ten seconds leaves before seeing any of it. It matches the
"one-in-four empty render" already noted in `NOTES.md`, but with numbers.

- [ ] **1G.1 Characterise it properly before escalating.** More runs, both
  pages, and a check of whether it tracks with a particular asset or request.
  Do not blame `customCss` without evidence — 25 rules do not cost 20 seconds.
- [ ] **1G.2 Likely a Lapis support question, like 1B.3.** If the delay is in
  their bundle or their data fetch, nothing in this repo can fix it, and the
  useful output is a reproducible report with these timings.

### 1H. The three odd catalog cards — DIAGNOSED 12 Oct 2026

The cause is not a per-size photo after all. It is simply an **older upload**.

Reading the live card images, fourteen of the seventeen point at one contiguous
batch (ids `179178944`–`179179029`). The three that break the grid point at a
much earlier batch:

| Product | Image id | |
|---|---|---|
| SS-31 | `179170427` | photograph |
| TMG-2TZ | `179170300` | photograph |
| TMG-3RT | `179170305` | photograph |

They are the pre-render photographs; they were never swapped when the other
fourteen were. The correct renders already exist and are already right.

- [ ] **1H.1 `ADMIN` Replace those three product images** — **ON HOLD, see 1I.**
  The renders that would replace them carry a cap defect. Doing this now spreads
  the defect to three more cards and means uploading twice.

### 1I. ⚠️ THE CAP IS WRONG ON ALL 17 RENDERS

Spotted by Mila 12 Oct 2026, looking at `tmg-ss-31.png` — *"the blue doesn't go
all the way to the white, and the white looks crooked."* Both are real.

**Fault 1 — the blue band stops short of the white.** A bare silver-metallic
ring sits between the underside of the white plastic flip-off disc and the top
of the blue anodised band. On a real crimped flip-off cap the blue runs up to
and under the white; there is no exposed aluminium there. This strip is clearly
visible at 3x.

**Fault 2 — the white disc sits tilted.** Its lower edge is **10 px lower on
the right than on the left** on the 2000px master (sampled at x=760 vs x=1240).
That also makes the silver strip wedge-shaped, which exaggerates the lean.

> A quick colour-classifier attempt to measure the silver strip's thickness
> across the cap returned garbage (0–134 px) because it mistook the specular
> highlight on the blue band for white. **Do not quote a thickness from it.**
> The 10 px slope figure is sound; the strip is documented visually.

**It is in the master, so it is in all seventeen.** Verified by cropping the cap
from `tmg-ss-31`, `tmg-epithalon`, `tmg-ghk-cu` and `tmg-nad`: identical cap,
identical faults. The seventeen renders are one vial photographed once and
re-labelled, so every live product image on the store has this.

**This is part of the answer to 1B ("ours look generated").** It is a geometry
error the eye catches before it can name it — a cap that could not be assembled
that way.

- [ ] **1I.1 Fix the cap in the master, then re-render all 17 and upload all 17
  once.** Folds 1H.1 into it. This is the big 1B vial job, not a quick pass.

### 1B. The vials (ours look generated, Nurish looks smooth)

The reference is not photography. It is a **repeatable render**: one master
vial, frontal, zero perspective, identical bounding box in every frame, label
typeset as crisp type directly on teal glass, transparent background. The glass
colour *is* their brand colour.

> ### ⚠️ Why ours still reads "generated" — the reference compared, 12 Oct 2026
>
> Mila asked why we were not emulating the reference. Fair. **1B.1 below was
> ticked off on COLOUR and FILE SIZE. The look — the actual brief — was never
> compared.** That is the drift. Verified first-hand against Nurish's own hero
> image (`hero-shop-glp3rt-opt-v2.webp`) rather than from this note.
>
> **Their vial is one object in one colour.** Dark green glass, dark green cap,
> a single thin silver crimp ring, type printed directly onto the glass in
> white. Brand small at the top, product name large, mg in a small chip,
> "Purity ≥ 99%", one tiny footer line.
>
> **Ours is four materials with three junctions.** Clear glass + white paper
> label + white plastic cap + blue anodised band. Every junction is a place a
> render can fail — **and the cap fault in 1I is exactly one of them.** Nurish
> cannot have that fault: their cap is the same colour as their bottle, so the
> junction does not exist.
>
> **So the gap is not render quality. Their bottle is a simpler object to
> depict.** We have been rendering a complicated thing imperfectly; they
> designed a thing that is hard to render badly.
>
> ### ⚠️ CORRECTION, same day — the above generalises from ONE reference
>
> Mila: *"What about the amino peptides bottles? Those are multicolored. Go
> look."* She is right, and Amino Club is the reference she sent **first**.
>
> Checked three of their live product pages. **Amino Club's bottle is TrueMG's
> bottle**: clear glass, plain silver crimped cap, and a **paper label** — not
> coloured glass. What changes is the **label's tint, one pale colour per
> compound**, with the card's glow keyed to match:
>
> | Their product | Label + field |
> |---|---|
> | BPC-157 | mint |
> | GHK-Cu | pale blue |
> | AMP-3 (RT) | lilac |
>
> Same bottle every time. Only the colour changes.
>
> **This kills option (b) below as the only way to get there.** Nurish solved it
> with one-colour glass; Amino Club solved it with colour on the label, and
> Amino Club's solution needs **no product redesign at all** — TrueMG already
> prints paper labels on clear glass with a crimped cap.
>
> **It also explains the flat grid better than "the cap is broken" does.**
> Seventeen white labels on seventeen identical pale-blue tiles read as a parts
> bin. `1B.6` already said exactly this — *"Amino Club keys the field to each
> vial's own colour and it is the single biggest reason their grid looks
> designed rather than stocked"* — **and it was never done.** The cards are one
> blue for all seventeen.
>
> **So the real job is a colour system:** a pale shade per compound, carried on
> the label and echoed in the card behind it, with `#1C8CD0` kept as the house
> colour so the range still reads as TrueMG rather than a rainbow.
>
> - [x] **1B.7 Propose a palette** — DONE 12 Oct 2026, awaiting Mila's approval.
>   Sheet at `truemg/assets/web/palette-proposal-v1.jpg`, built by
>   `scratchpad/palette.py`. Consequence stated: the Canva labels finished
>   12 Oct are white and would take a tint. That is artwork, not a change to the
>   physical bottle.
>
> ### What building it turned up — the warm/cold split
>
> Mila said the thing she likes about Nurish is *"the vibe it gives… a really
> calm vibe. That's why I created that hand."* So the palette was derived from
> **her own assets** rather than invented. Dominant colours, sampled:
>
> | Asset | Hue | Reads as |
> |---|---|---|
> | `web/hand-vial-labelled.jpg` | 20–42, sat 18–28% | warm sand, clay, cream |
> | `web/hero-spa.jpg` | 32–34, sat 19–37% | warm stone, brass, soft green |
> | `web/hero-float.jpg` | **206–229**, sat 12–44% | cold blue-grey |
>
> **The two moods she has are near opposites on the wheel.** The hand and the spa
> are warm; the floating-vials hero — the one actually carrying product — is
> cold. That, not the cap, is the biggest reason the store reads clinical while
> the hand reads calm. In the hand shot the vial is the *only* cool object in a
> warm room, and that single contrast is doing all the work.
>
> So the proposal is: **warm paper as the ground, brand blue as the one cool
> note, and a pale paper tint per compound.** Five families — repair, signal,
> metabolic, cofactor, plain — so seventeen labels read as a range rather than a
> rainbow. TMG-BAC stays white because it is a solution, not a compound.
>
> Nothing in it touches the glass, the cap, the mark or the blue.
>
> **Mila's verdict, same day: warm is right, the browns are wrong.**
> *"It's right. I don't know if I like that. The Browns. Could we do another?"*
>
> The browns came from sampling `hero-spa.jpg` wholesale — but the tan in that
> picture is the **furniture**, not the thing that makes it calm. What makes it
> calm is the quality of the light. So v2 keeps the warmth and drops the tan:
> four grounds at `truemg/assets/web/palette-grounds-v2.jpg`
> (`palette_grounds.py`), each shown as three real catalog cards rather than as
> swatches.
>
> | Ground | What it is | Risk |
> |---|---|---|
> | **Bone** | warm white, warmth carried by light alone | can go blank if the photography is weak |
> | **Greige** | warm grey, no tan, modern and quiet | the safe one; least distinctive |
> | **Eucalyptus** | the green off the spa shot's orchids and monstera, taken right down | boldest; nothing else in the category does it |
> | **Blush** | the skin warmth from the hand shot | leans feminine — right or wrong, no middle |
>
> The per-compound tints are unchanged and are **not** what she objected to.
>
> **Mila picked EUCALYPTUS, 12 Oct 2026** — *"Definitely go with the eucalyptus."*
> That is the ground. Full build at `truemg/assets/web/palette-eucalyptus-shelf.jpg`
> and `-hero.jpg`, generator `palette_eucalyptus.py`.
>
> ### The tints had to be re-cut for a green ground
>
> v1's five families were rose / sage / wheat / lilac / ice. On a **green** page
> the sage and moss members stopped being a distinction — they just echoed the
> ground and read as "no colour". So the families were respaced to five hues
> that are each far from the page's green and from each other:
>
> | Family | Hue | Members |
> |---|---|---|
> | repair | rose | GHK-CU, BPC-157+TB-500, KLOW |
> | signal | butter | IPAMORELIN, CJC-1295+IPA, TESAMORELIN |
> | metabolic | sage — deliberately the house green, worn by the flagships | TMG-2TZ, TMG-3RT, MOTS-C |
> | neuro | lilac | SEMAX, SELANK |
> | cofactor | ice blue | NAD+, EPITHALON, THYMOSIN ALPHA-1, SS-31, VITAMIN B12 |
> | plain | white | TMG-BAC |
>
> **`1B.6` is finally answered in the same move.** The card's image field is now
> a very pale wash of that compound's own tint instead of one pale blue for all
> seventeen, which is the thing Amino Club does and the single biggest reason
> their grid looks designed rather than stocked.
>
> ### What eucalyptus costs: the hand shot needs a regrade
>
> `hand-vial-labelled.jpg` has a **beige** background. On a green page it reads
> as a photograph from a different room. `-hero.jpg` shows it as-is against a
> regrade — saturation pulled to about two-thirds and a 12% eucalyptus wash laid
> over. It works, it is one pass in software, and **no reshoot is needed.** The
> blue cap actually gains from it, because it is no longer competing with an
> orange wall.
>
> Open: the regrade is a global adjustment, so the skin cools slightly along with
> the room. A masked version that protects the hand would be better and is a
> bigger job. Worth doing only once the ground is locked for real.
>
> ⚠️ The composites in `web/` all carry the **old smooth lizard and the old label
> layout**, from before the 12 Oct rebuild. Whatever happens with the palette,
> every hero and mood image needs re-rendering — which folds neatly into the
> cap fix at `1I.1`, one render pass for all of it.
>
> That splits the work in two, and it is Mila's call which:
>
> **(a) Copy the discipline, keep the product.** Fix the cap junction, lock all
> 17 to one frame and one lighting setup, drop the paper-label shading that
> reads as fake. Her physical vials are unchanged. **Recommended** — the site
> should show what is in the box, and her real labels are white paper.
>
> **(b) Copy the design.** Brand-blue glass, type on glass, matching cap. This
> is what actually produces their shelf. But the site would stop matching the
> product being shipped, and the Canva label artwork (finished 12 Oct) would
> have to be redone. **This is a PRODUCT decision, not a website one, and it is
> far cheaper before a print run than after.**

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
- [x] **1B.3 `BUILD` Re-rendering would change nothing — CLOSED 12 Oct 2026.**
  This task rested on a wrong premise and is withdrawn before anyone spends a
  day on it. The uploaded masters are **already 2000x2000**: the live
  TESAMORELIN object downloads at 2000px RGBA and is **byte-identical** to
  `assets/vials/tmg-tesamorelin.png` (same md5, zero differing pixels).

  The 640px is **Lapis's own transform**, requested by the theme's markup as
  `?width=640&quality=80` on a `/render/image/` URL. The origin serves whatever
  width is asked for — 1024, 1200 and 2000 all return at full size on request —
  so the pixels exist and are simply not being asked for. CSS cannot rewrite an
  `img` `src`, so this is **not reachable from `customCss`**. It belongs with
  2.5 as a question for Lapis support: ask the theme to request `width=1024`.

  ⚠️ **Correction — there may be no softness at all.** This note first repeated
  the diagnosis's 344px figure and concluded the card needs 688 device pixels
  and gets 640, i.e. 0.93x. **That 344 was never measured on the live card.**
  A parallel session measured the rendered image box at **307px**, which against
  a 640px source is **2.08x** — above the 2x a retina screen asks for. On that
  measurement the images are already sharp enough and nothing needs doing.

  Either way the task is withdrawn: re-rendering cannot help, because the
  masters are already 2000px. The only open question is whether the delivered
  width is worth raising with Lapis at all, and the live measurement says
  probably not. Re-measure the box before spending anything on it.
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

- [x] **1D.1 `ADMIN` All 17 descriptions are LIVE — verified 12 Oct 2026.**
  Checked against the rendered catalog, not assumed: every one of the seventeen
  now carries its redraft from `PRODUCT-DESCRIPTIONS.md`. The
  `[NAME] is a [noun] classified within [family]` skeleton is gone from the
  site. An earlier note here and the header of `PRODUCT-DESCRIPTIONS.md` both
  said these were "written but not yet live" — that was stale.

- [ ] **1D.1b `ADMIN` Nine of them truncate to a fragment on the catalog card.**
  The new fault, created by the fix. The card renders **only the first
  sentence**; the product page renders the whole thing. Nine redrafts were
  written as two sentences, so the card shows sentence one alone — and three of
  those are useless on their own:

  | Product | What the card shows today |
  |---|---|
  | **SS-31** | "Elamipretide." |
  | **TMG-2TZ** | "Thirty-nine residues." |
  | **EPITHALON** | "Ala-Glu-Asp-Gly." |
  | SEMAX | "A modified fragment of ACTH." |
  | MOTS-C · NAD+ · SELANK · THYMOSIN ALPHA-1 · VITAMIN B12 | reads as a sentence, but the second half is lost |

  **Proven, not inferred, on EPITHALON:** the product page at
  `/catalog/epithalon-f9mh` renders "Ala-Glu-Asp-Gly. Four residues, synthesised
  after a pineal peptide fraction." in full, while its card shows the first four
  words. The full text is stored; the card is what truncates. The catalog page's
  own HTML never contains the second sentence at all, so the truncation happens
  in the data the catalog receives, not in CSS — **no stylesheet rule can fix
  this.**

  Fix: replace the first full stop with a comma or an em dash, exactly as was
  already done for GHK-CU ("…copper(II) ion — three residues and a metal.") and
  IPAMORELIN ("Five residues, selective at…"), which is why those two read
  correctly on the card today. Nothing is lost on the product page. Nine edits,
  one punctuation mark each. Confirm each field's live text at edit time rather
  than pasting from the markdown — only EPITHALON's stored text has been read
  back in full.
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

### 1F. Two product web addresses carry names the copy rules forbid

Spotted 12 Oct 2026 while reading the live catalog. The descriptions were
cleaned up; **the URLs were not**, and they are public, indexable and quoted in
every share link.

| Product | Its address on the store today |
|---|---|
| **TMG-BAC** | `/catalog/bacteriostatic-water-tzbc` |
| **TMG-2TZ** | `/catalog/tirzepatide-k8ms` |

`PRODUCT-DESCRIPTIONS.md` is explicit that TMG-BAC "is deliberately not called
bacteriostatic water" because that is a specific regulated drug product name —
and the address says it anyway. `tirzepatide` names the originator molecule
outright rather than the catalogue designation.

The slug is generated from whatever the product was first called, so these are
fossils of the pre-rebrand names. **Changing a URL is not cosmetic** — old links
break and search engines have to be told — so this is Mila's call with whoever
advises her on the wording, not a tidy-up. Raised here so it is not discovered
later. `ADMIN`, and likely needs a redirect from the old address.

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

- [ ] **1E.4 ⚠️ WRONG LIZARD ON ALL 20 LABELS.** Raised by Mila 12 Oct 2026,
  confirmed by side-by-side render. The labels carry the **smooth-head** mark
  from `assets/_archive/smooth-mark/` — no crest, thinner strokes, simpler mane.
  The real mark (`assets/logo/truemg-mark-brand.svg`) has a **spiked crest along
  the top of the head**, a fuller mane and heavier strokes. Different drawings.

  The archive file is named `mark-2365CD.png` — the legacy blue — which is
  exactly why the labels carried the wrong blue. **Task 1E.1 recoloured the
  wrong lizard.** The recolour is not wasted (it also covered the MG block and
  the product names) but the mark itself must be replaced, not tinted.

  Fix: upload `truemg-mark-brand.svg` to Canva, then `update_fill` on the mark
  element on each of the 20 pages. Blocked only on Mila confirming the official
  mark is the one she wants — `_archive/rejected-marks/marks-sheet.jpg` holds
  other options she may prefer.

- [ ] **1E.5 The warning block's third line is out of rhythm.** The warning is
  **two** text boxes, not one: "not for human consumption" wraps to two lines in
  box one, "research use only" is a separate box below. Measured on page 1 —
  lines 1→2 sit 28.75 apart, lines 2→3 sit 33.81 apart, so the last line drops
  **5.06 too far, an 18% wider gap**. That is the unevenness Mila saw by eye.
  Fix: one box, three lines, single line-height. **The wording is not to be
  touched — this is a position change only.**

- [ ] **1E.6 Three left edges where there should be one, and the block roams.**
  Measured across all 18 pages whose geometry was read:
  - The **lizard sits 4.006 right of the product name on every single page.**
    Worse than a plain offset: a circle must hang slightly *left* to look level
    against straight-edged text, so the error reads double.
  - The **strength** sits 4.006 right of the name on pages 1, 3, 5 and 13, and
    flush on the rest — so the labels are not even wrong consistently.
  - The whole block starts at **five different left edges across the set**
    (537.77, 576.70, 587.82, 593.38, 602.46), so the labels do not line up with
    each other when seen together.

  Fix: one left edge per label, same edge on every label, lizard nudged left to
  sit optically flush.

- [x] **1E.7 LABEL REBUILD — DONE 12 Oct 2026.** All four faults fixed on all
  20 pages, verified in the live editor after a reload.

  **Mark.** `truemg-mark-brand.svg` rendered at 1600px on transparency, trimmed
  to the ink, squared, uploaded, swapped into all 20. Canva forces an image to
  *cover* its box, and the box was 135.48 x 137.12 — taller than wide — so it
  shaved the circle's edges. Fixed by squaring the element to 137.122 and
  cropping 1:1. The SVG was already brand blue, so no recolour was needed.

  **One left edge.** Everything on every label now starts at 537.766; the mark
  at 535.766, 2 left, because a circle must overhang slightly to read flush
  against straight-edged text.

  ⚠️ **The shared edge had to be the LEFTMOST, not the most common.** First
  attempt used 602.46 (14 of 20 pages) and TESAMORELIN immediately collided
  with the wordmark — the long names had been pushed left deliberately. At
  537.766 every name clears at its existing size, so no type was resized.

  **Warning rhythm.** Third line lifted from 512.228 to 507.169. Still two
  boxes, deliberately: merging them would mean retyping the compliance words,
  which is forbidden. Moving a box touches no text.

  **Batch field.** `BATCH:` plus a blank line, in Inter at 28 bold, on all 20
  at (1040, 455). Count verified: exactly one per page.

- **The font trap, and the way through it.** `add_text` always lands in Canva's
  default (Arimo); `format_text` has no font family. But **a pasted element
  keeps its font** — so the method is: set one element's font by hand in the
  editor, then copy/paste it to every page.

  Pasting is unreliable about *which* page receives it: Canva's "current page"
  lags the scroll, so a paste can land on the previous page, as a duplicate, or
  dumped at page centre. Clicking inside the target page first helps but does
  not guarantee it. **Do not fight it — position is fixable by API, font is
  not.** Paste freely, then read every page, delete the duplicates and set every
  keeper's position in one call. This run produced 8 duplicates and 4 strays;
  all were cleaned up by data afterwards.
