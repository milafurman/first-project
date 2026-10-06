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
