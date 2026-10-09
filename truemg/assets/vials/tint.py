"""MOCK ONLY — what a colour-coded label line would look like.

The reference storefront gives every compound its own pale label colour, so
its catalog grid reads as a designed family. Ours is seventeen identical white
labels, which is why the grid reads as a spreadsheet however good each vial is.

This does NOT reprint anything. It tints the label paper in the existing
photographs so the idea can be looked at before anyone commits a print run.
If Mila takes it, the colour belongs in the Canva artwork, not here.

The tint has to leave the ink alone. "Paper" is bright AND low-chroma; the
blue type, the mark and the black compliance block are one or the other. So
paperness drives the blend, and the tint is multiplied by each pixel's own
normalised luminance first, which keeps the cylinder's shading instead of
flooding the label flat.
"""
import os

import numpy as np
from PIL import Image, ImageFilter

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

LABEL_TOP, LABEL_BOT = 0.360, 0.900      # the paper, as fractions of vial height
STRENGTH = 1.0

# Grouped by what the compound is for, so the colour carries information
# rather than decoration — which is the only thing that justifies it on a
# storefront whose whole argument is "we document things".
FAMILY = {
    "repair":    ("#D9E7DC", ["bpc-157-tb-500", "ghk-cu", "thymosin-alpha-1"]),
    "metabolic": ("#D8E6F5", ["nad", "mots-c", "ss-31"]),
    "growth":    ("#F3E1E0", ["tesamorelin", "ipamorelin", "cjc-1295-no-dac-ipamorelin", "tmg-2tz", "tmg-3rt"]),
    "cognitive": ("#E3DEF2", ["semax", "selank", "epithalon", "klow"]),
    "supplies":  ("#EFE9DE", ["tmg-bac", "vitamin-b12"]),
}


def tint_of(name):
    for hexc, members in FAMILY.values():
        if name in members:
            return tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return None


def paperness(rgb):
    """1 where the pixel is label stock, 0 where it is ink."""
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    chroma = (mx - mn) / np.maximum(mx, 1.0)          # relative, so shadow still reads as paper
    bright = np.clip((mx - 120.0) / 80.0, 0, 1)
    plain = np.clip(1.0 - (chroma - 0.05) / 0.12, 0, 1)
    return bright * plain


def apply(path, out, rgb_tint, strength=STRENGTH):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(float).copy()
    ys, xs = np.where(a[:, :, 3] > 8)
    y0 = int(ys.min() + (ys.max() - ys.min()) * LABEL_TOP)
    y1 = int(ys.min() + (ys.max() - ys.min()) * LABEL_BOT)

    reg = a[y0:y1, xs.min():xs.max() + 1, :3]
    p = paperness(reg) * strength
    # feather the band's top and bottom so the tint does not end on a hard line
    p = np.asarray(Image.fromarray((p * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2))).astype(float) / 255.0
    fade = np.clip(np.minimum(np.arange(p.shape[0]), p.shape[0] - 1 - np.arange(p.shape[0])) / 26.0, 0, 1)
    p *= fade[:, None]

    lum = reg.max(axis=2) / 255.0                      # keep the cylinder's shading
    tint = np.array(rgb_tint, float)[None, None] * np.clip(lum, 0, 1)[..., None]
    a[y0:y1, xs.min():xs.max() + 1, :3] = reg * (1 - p[..., None]) + tint * p[..., None]

    Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA").save(out)
    return out


if __name__ == "__main__":
    os.makedirs("tinted", exist_ok=True)
    n = 0
    for f in sorted(x for x in os.listdir(".") if x.startswith("tmg-") and x.endswith(".png")):
        t = tint_of(f[4:-4])
        if t:
            apply(f, "tinted/" + f, t); n += 1
    print("%d tinted (mock)" % n)
