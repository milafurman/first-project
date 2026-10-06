# Cap and crimp

The vial top is the only surface on the whole package that can carry colour
without touching the label artwork, the copy, or the compliance block. Right
now it is a silver aluminium crimp under a white plastic flip-disc — the
default every contract filler ships, which is exactly why it reads as nobody's
brand in particular.

`caps.py` recolours the two bands on the existing vial photographs:

| region | fraction of vial height | what it is |
|---|---|---|
| `DISC`  | 0.000 – 0.085 | white plastic flip-top |
| `CRIMP` | 0.085 – 0.170 | aluminium crimp band |

Hue and saturation are replaced; value is scaled rather than set
(`scale = target_v / region_mean_v`), so every highlight, shadow and knurl on
the original photograph survives the recolour. A flat fill would have produced
a sticker, not a cap.

## Recommendation

**Blue crimp on every vial, cap colour as the family code.**

The crimp is the constant — brand blue, `#2866CD`, the same blue as the
wordmark and the Gila mark — so any two vials photographed together read as one
company. The flip-disc then groups what gets bought together:

| family | cap | products |
|---|---|---|
| Metabolic  | blue   | TMG-2TZ · TMG-3RT |
| Repair     | white  | BPC · TB-500 · KLOW |
| Longevity  | black  | NAD+ · MOTS-C · SS-31 |
| Cognitive  | green  | SEMAX · SELANK |
| Supplies   | grey   | Research Solution · B12 |

## Cost note

Colour-anodised crimps and custom flip-off caps carry supplier minimums —
usually five figures of units per colour. The cheapest first version is **blue
crimp, white cap, everywhere**, which is one colour and one minimum, and the
family colours get added at the next reorder once volume justifies five.

`caps-sheet.jpg` is the comparison sheet. `opt0`–`opt5` are the six crimp/cap
combinations; `fam0`–`fam4` are the five family codes.

## Every aluminium colour, one per frame

`crimps.py` builds `crimp-sheet.jpg`: the same vial, the same label, the same
white cap, with only the crimp changing — silver (what is on the vial now),
brand blue, gold, deep gold, gold-over-blue, black, gunmetal, copper and pearl
white. `c0`–`c8` are the individual frames.

Gold and blue can combine on either part, because the crimp and the flip-disc
are separate components, so the sheet shows all three: gold crimp with a blue
cap, blue crimp with a gold cap, and a blue crimp carrying a gold ring at the
top (`RING`, the top third of the crimp band, recoloured after the band so it
sits over it). `x0`–`x2` are those frames.

## Decided

**Blue crimp, white cap.** Mila's call, and it is now on all seventeen vials in
`truemg/assets/vials/`. `bluecrimp.py` is what rolled it across the line; the
cap is left exactly as photographed rather than recoloured to a nominal white,
since it is already white and a recolour would only cost it shading.

The family cap-coding set above stays on the table as a phase two, once volume
justifies more than one colour minimum.
