# TrueMG image manifest — everything the site consumes, and who makes it

**Rewritten 15 Oct 2026. This replaces every earlier version of this file.**
Git history has the old one if you need it.

## Ownership

**Codex owns all photo and graphics creation.** Mila, 15 Oct: *"All the photo and graphics
creations should now be coming from Codex."* Nothing in `truemg/assets/vials/` or
`truemg/assets/web/` is to be used as final artwork — those are placeholders and they are
off-brand. Do not render new vials here, do not composite new heroes here, do not stage files
for upload from here.

**The reference for everything** is Sam's TMG-3RT 10MG cutout in
`drive.google.com/drive/folders/1RnTchA_5Tiz3tk0KEAhYu85-R3QKdlxq` → `vial/Labels`.
Match its label design: compound name in blue, strength in black beneath, `TRUE MG LABS`
vertical up the right side, large pale ghosted lizard behind the mark, solid blue lizard lower
left, `NOT FOR HUMAN CONSUMPTION` / `RESEARCH USE ONLY` on two lines, DNA-helix motif down the
right edge, white flip-top cap over a blue crimp.

**Never write or alter label text.** The compliance block is fixed and must not be
AI-generated.

---

## A. Product vial cutouts — 20 needed, 1 delivered

The main job. **Transparent PNG, square, 1254x1254** to match the delivered reference. A baked-in
background is a bug: the storefront sits these on a tinted card colour, so any backdrop shows as
a visible box.

Each **size** needs its own, because the storefront swaps the image when a shopper picks a
strength and the label must show the matching one.

| Product (store name) | Strength | SKU | Status |
|---|---|---|---|
| BPC-157 + TB-500 | 20MG (10+10) | TMG-BPC157TB500-20MG | needed |
| CJC-1295 (No DAC) + IPAMORELIN | 10MG (5+5) | TMG-CJC1295IPA-10MG | needed |
| EPITHALON | 10MG | TMG-EPI-10MG | needed |
| GHK-CU | 50MG | TMG-GHKCU-50MG | needed |
| IPAMORELIN | 10MG | TMG-IPA-10MG | needed |
| KLOW | 80MG blend (TB10+BPC10+GHK50+KPV10) | TMG-KLOW-80MG | needed |
| MOTS-C | 20MG | TMG-MOTSC-20MG | needed |
| NAD+ | 1000MG | TMG-NAD-1000MG | needed |
| SELANK | 10MG | TMG-SELANK-10MG | needed |
| SEMAX | 10MG | TMG-SEMAX-10MG | needed |
| SS-31 | 10MG | TMG-SS31-10MG | **needed — empty slot on the live site** |
| SS-31 | 50MG | TMG-SS31-50MG | needed |
| TESAMORELIN | 20MG | TMG-TESA-20MG | needed |
| THYMOSIN ALPHA-1 | 10MG | TMG-TA1-10MG | needed |
| TMG-2TZ | 10MG | TMG-2TZ-10MG | **needed — empty slot on the live site** |
| TMG-2TZ | 20MG | TMG-2TZ-20MG | needed |
| TMG-3RT | 10MG | TMG-3RT-10MG | **DELIVERED — the reference** |
| TMG-3RT | 20MG | TMG-3RT-20MG | **needed — empty slot on the live site** |
| TMG-BAC | 10ML | TMG-BAC-10ML | needed |
| VITAMIN B12 | 10ML | TMG-B12-10ML | needed |

**Do these three first.** They are the only size-slots with no photo at all, so choosing that
strength currently shows a mismatched image: **SS-31 10MG · TMG-2TZ 10MG · TMG-3RT 20MG**

**How these reach the site:** product photos are NOT design keys. They are uploaded by hand in
the Lapis admin, per product and per size, at Products → Catalog → product → Sizes, pricing &
stock. No agent can do it. Deliver the files; Mila uploads.

---

## B. The master images — the five slots the site pulls by URL

All five currently hold a placeholder of mine. Each is a plain URL field: whatever Codex makes
has to end up at a public URL, then the key gets pointed at it.

| Lapis key | What it is | Format needed | Status |
|---|---|---|---|
| `heroBackgroundUrl` | Full-bleed hero behind the headline, desktop | **2560x1150 JPG** | placeholder |
| `heroBackgroundMobileUrl` | Same for screens under 768px | **1080x1500 JPG** | placeholder |
| `aboutImageUrl` | Photo beside the About story | square-ish, ~1600x1100 | placeholder |
| `seoImageUrl` | Social share card | **1200x630 JPG** | placeholder |
| `comingSoonImageUrl` | Full-bleed behind the coming-soon page | 2560x1150 JPG | **empty** |

`heroMediaUrl` currently holds a 1x1 transparent pixel. That is deliberate — it suppresses the
theme's default of showing the first featured product. Leave it unless you intend to replace the
hero visual outright.

### Hero composition — learned the hard way, do not re-derive

- **Desktop:** cluster right of centre. The left half must stay clear; the headline sits over a
  white gradient wash that fades left-to-right.
- **Phone:** cluster **low in the frame, centre about 88% down**. Above it sit the headline, body
  copy, two buttons and three trust badges, all over a near-white wash. A centred cluster puts
  vials behind the body text; a tight crop clips them. Three attempts to get this right.
- **Background:** the pale blue-white gradient the catalog bands already use, so the hero matches
  the site instead of fighting it.

The hero cannot be built until enough cutouts exist — the current composition uses five vials.

---

## C. Logo and favicon — already correct, leave alone

The header and footer wordmark and the favicon are **uploads**, not URL keys, done in Design
studio → Manual. They are already right and are not part of this job.

---

## Naming rules that apply to every file

- **TMG-BAC is never called bacteriostatic water**, in copy or in a file name.
- Use store names — **TMG-2TZ, TMG-3RT, TMG-BAC** — not the underlying compound names.
- Research-use framing only. No dosing, no therapeutic or outcome claims, no before/after, no
  human-use suggestion, in any image or any file name. The word "performance" never appears.

## Where finished files go

Sam's shared folder, above. It is currently shared "anyone with the link — Viewer", so only Sam
can add to it; if Codex writes elsewhere, say where.
