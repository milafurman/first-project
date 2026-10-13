# Tonight — finish the site. Two jobs, in this order.

Both are Mila's hands. Nothing here can be done from the session: the live store
cannot be written from an auto-mode session (three refusals, see
`WHY-THE-SITE-LOOKS-UNCHANGED.md`) and product photos are admin-only uploads.

---

## JOB 1 — the design save (~2 min, changes everything at once)

Lapis → Design studio. **All three parts in ONE save** — saving colours wipes
the custom CSS, so splitting them loses part 3.

**a) Three hero fields.** Each holds a web address containing `a2e36e7`.
Change those seven characters to **`95bbfb1`**. Nothing else in the address
changes.

| Field | |
|---|---|
| `heroBackgroundUrl` | …@**95bbfb1**/truemg/assets/web/hero-hand.jpg |
| `heroBackgroundMobileUrl` | …@**95bbfb1**/truemg/assets/web/hero-spa-mobile.jpg |
| `heroMediaUrl` | …@**95bbfb1**/truemg/assets/web/pixel.png |

**b) Six colours.** Leave `accent`, `themeAccent`, `themeAccentDeep` and
`primary` alone — that is the brand blue and it does not change.

| Key | Value |
|---|---|
| `background` | `#EEF2EE` |
| `card` | `#FCFDFB` |
| `secondary` | `#E9EDE9` |
| `border` | `#DCE5DC` |
| `muted` | `#E4EBE4` |
| `mutedForeground` | `#6E7A6E` |

**c) Custom CSS.** Paste the whole of `customCss-eucalyptus.css`.

After this the site is green, each card has its own colour, and the home page
hero is the re-rendered one. The bottles will still have the old cap — that is
job 2.

---

## JOB 2 — the seventeen product photos (~10 min)

Lapis admin → Products → Catalog → each product → image.

The files are staged, numbered **in the order the catalog grid shows them**:

```
truemg/assets/vials/UPLOAD/
```

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

These are **drop-in**: same 2000×2000 canvas, same framing, same silhouette as
what is up now, so no layout can shift. They are the plain cut-outs, matching
what is already on the store — not the `float/` set with the baked shadow, which
is a separate look and not a change to make at the same time as everything else.

Doing all seventeen also clears `1H` — the three mismatched cards (SS-31,
TMG-2TZ, TMG-3RT) were an older upload batch and get replaced here.

### Verified tonight: transparency survives

The card's image transform returns PNG with the alpha intact — 310,460
transparent pixels of 409,600 on a live card image. So the bottles sit **on** the
new coloured panels rather than as white squares.

⚠️ A note in `../../assets/vials/README.md` claims the store CDN flattens alpha
to RGB. **That is wrong**, at least for the path the catalog card uses, and it
would have argued against the whole coloured-card design. Tested, not assumed.

---

## Then

Reload truemglabs.com with `?peek=1` on the end to see it past the curtain.
