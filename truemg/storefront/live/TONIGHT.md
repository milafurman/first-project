# TONIGHT — exactly what to save, and exactly where

Everything below is validated against the live store with a dry run:
`ok: true`, nothing refused. The only automatic adjustment is `mutedForeground`,
which Lapis nudges for contrast — expected, leave it.

Site: **app.uselapis.io/admin** → **Design studio**

> ⚠️ **ONE SAVE.** Saving colours wipes the custom CSS. Enter all three parts,
> then press save once. If you must split it, do the CSS **last**.

---

# PART 1 — COLOURS  (6 fields)

Design studio → **Colors**

| Field | Paste this |
|---|---|
| background | `#EEF2EE` |
| card | `#FCFDFB` |
| secondary | `#E9EDE9` |
| border | `#DCE5DC` |
| muted | `#E4EBE4` |
| mutedForeground | `#6E7A6E` |

**Do NOT touch:** accent, themeAccent, themeAccentDeep, primary, foreground,
primaryForeground, secondaryForeground, themeAccentForeground.
Those carry the brand blue and the black. They do not change.

---

# PART 2 — TEXT FIELDS  (4 fields)

Design studio → the copy/text fields. Labels as they appear in Lapis:

### "Hero background image URL"  (`heroBackgroundUrl`)
```
https://cdn.jsdelivr.net/gh/milafurman/first-project@95bbfb1/truemg/assets/web/hero-hand.jpg
```

### "Hero background image URL for phones"  (`heroBackgroundMobileUrl`)
```
https://cdn.jsdelivr.net/gh/milafurman/first-project@95bbfb1/truemg/assets/web/hero-spa-mobile.jpg
```

### "Hero media: image URL replacing the hero visual"  (`heroMediaUrl`)
```
https://cdn.jsdelivr.net/gh/milafurman/first-project@95bbfb1/truemg/assets/web/pixel.png
```

> All three are the SAME as what is there now except for seven characters:
> `a2e36e7` becomes `95bbfb1`. You can edit in place instead of retyping.

### "Flat colour behind product photos"  (`productImageBg`)
```
#F1F5F1
```
Currently `#ffffff`. This one is **not** cosmetic trivia: it controls the well
behind the bottle on the **individual product pages** as well as the cards.
Left white, every product page would keep a white box while the rest of the
site went green.

---

# PART 3 — CUSTOM CSS  (1 paste)

Design studio → **Custom CSS**. Select all, delete, paste the whole of:

**`customCss-eucalyptus.css`** (sent to you; also in this folder)

3,679 characters of the 10,000 allowed. It contains everything that is there
today, with the blue-white and cream blocks turned green, the navy footer turned
green-black, and **seventeen new lines that give each bottle its own panel
colour**.

---

# THEN PRESS SAVE. ONCE.

Check it at **https://truemglabs.com/?peek=1** — the `?peek=1` gets you past the
coming-soon curtain.

---

# PART 4 — THE SEVENTEEN PHOTOS  (~10 min, separate job)

Admin → **Products** → **Catalog** → each product → image.

Files are staged and numbered **in the order the catalog grid shows them**:

`truemg/assets/vials/UPLOAD/`

| # | Product | # | Product |
|---|---|---|---|
| 01 | TESAMORELIN | 10 | NAD+ |
| 02 | IPAMORELIN | 11 | SELANK |
| 03 | CJC-1295 (No DAC) + IPAMORELIN | 12 | SEMAX |
| 04 | BPC-157 + TB-500 | 13 | THYMOSIN ALPHA-1 |
| 05 | KLOW | 14 | VITAMIN B12 |
| 06 | GHK-CU | 15 | TMG-2TZ |
| 07 | EPITHALON | 16 | TMG-3RT |
| 08 | SS-31 | 17 | TMG-BAC |
| 09 | MOTS-C | | |

Drop-in: same 2000×2000 canvas, same framing, same silhouette as what is up now.
Also clears the three mismatched cards (SS-31, TMG-2TZ, TMG-3RT).

---

# IF YOU WANT IT ALL BACK

| Field | Old value |
|---|---|
| background | `#ffffff` |
| secondary | `#ecebee` |
| productImageBg | `#ffffff` |
| the three hero URLs | `a2e36e7` instead of `95bbfb1` |
| Custom CSS | paste `customCss-2026-10-12.css` from this folder |

`card`, `border` and `muted` were not set before, so clearing them is fine.
