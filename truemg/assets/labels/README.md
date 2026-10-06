# TrueMG vial labels — print artwork

20 labels, one per product variant, as vector SVG and press-ready PDF.
`labels.py` regenerates all of them; `_TEMPLATE-with-guides.svg` shows the
geometry with trim, safe zone and wrap line marked.

## Geometry

| | |
|---|---|
| Trim (finished label) | **60 × 30 mm** |
| Bleed | 3 mm all round → artwork is 66 × 36 mm |
| Safe zone | 2.5 mm inside trim; nothing critical crosses it |
| Wrap allowance | 9 mm on the right, which curves out of sight on the vial |
| Readable front panel | 46 mm wide — every element is laid out inside this |

> **Confirm the trim size before ordering anything.** 60 × 30 mm is the common
> size for a 10 mL serum vial, but it is an assumption, not a measurement. Get
> the real figure from the vial supplier or the label printer, change `TRIM_W`
> and `TRIM_H` at the top of `labels.py`, and re-run. Everything reflows: the
> compound name and all text auto-size to the panel.

## Design

Ink ground with the gold accent, which inverts the category — almost every
peptide vial on the market wears a white label. Against the brand book this is
correct: ink is the ground, gold is the single signal, and it appears once.

Layout, top to bottom: the Gila mark in gold beside the wordmark in paper;
the compound name in heavy grotesk; the strength in gold mono, because every
number in this brand is monospaced; a gold hairline; the compliance block;
then the variable data line.

The compound name **auto-sizes**. `BPC-157 + TB-500` and `CJC-1295 + IPAMORELIN`
set smaller than `NAD+` so that no name can ever collide with the rule below it.
Every baseline is placed explicitly and asserted to fall inside the safe box.

## Compliance text — fixed on every label

```
FOR LABORATORY RESEARCH USE ONLY
NOT FOR HUMAN OR VETERINARY USE
NOT FOR DIAGNOSTIC USE · STORE AT −20°C
```

Plus `LOT` and `MFG` fields for the filler to overprint or hand-write.

**This wording has not been reviewed by a lawyer.** It follows the research-use
convention and matches the site, and it is the piece of this project most worth
an attorney's twenty minutes before a print run.

## Typography — and why not the brand's own faces

Set in **Archivo Black** and **IBM Plex Mono**, both open-licensed, both
embedded in the PDFs. The brand book names Helvetica Neue and SF Mono; neither
can legally be embedded in artwork sent to a commercial printer. Archivo Black
is a close read for Helvetica Neue at weight 900 and carries the same density.

The first PDF build silently fell back to DejaVu because this machine had no
Helvetica. Caught by inspecting the embedded font table rather than by looking
at the proof, which is the only way that particular error shows up.

## Before the press run

1. **Confirm the trim size.** Everything else is downstream of it.
2. **Convert colour.** The files are RGB. Ask the printer for CMYK, or better,
   specify gold `#D8B46A` as a **metallic spot** — on a black label that is the
   single highest-value upgrade available, and the brand already treats gold as
   the one luxury signal.
3. **Flag the ink coverage.** A solid black label at this size is heavy; the
   printer may want to adjust for it.
4. **Have the compliance block reviewed.**
5. **Pull a physical proof on the real stock and wrap it on an actual vial**
   before committing to quantity. The wrap allowance is calculated, not tested.
