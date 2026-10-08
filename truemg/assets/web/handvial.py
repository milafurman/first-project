"""Put the real label on the vial in the hand shot.

`hand-vial.jpg` is generated: an elegant hand holding a vial whose label is
deliberately BLANK. That blankness is the whole point. An image model asked to
draw a research-compound label will invent a compound name and a purity
figure, and on this storefront that is not an ugly mistake, it is a legal one —
"NOT FOR HUMAN CONSUMPTION / RESEARCH USE ONLY" is a compliance line, not
decoration. So the model gets the hand, the glass and the light, and never
touches the label.

The useful accident: Mila's vial sprites were photographed on a real round
vial, so the label artwork already carries its cylinder projection. There is
no need to map a flat texture onto a cylinder and fake the wrap — the wrap is
in the source. It only has to be placed, fitted and relit.

Relighting is what sells it. The blank label in the plate is not flat white: it
has a highlight down its left side and falls into shadow on the right, because
that is where the window is. Pasting bright artwork over it would read as a
sticker on a photograph. So the blank panel's own luminance is extracted and
multiplied back over the artwork, which inherits the exact shading the
photograph already had.

Run from this directory.
"""
import os

import numpy as np
from PIL import Image, ImageFilter

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

PLATE = "hand-vial.jpg"
NAME = "ghk-cu"                            # any sprite in ../vials
OUT = "hand-vial-labelled.jpg"

# The blank panel, measured off the plate.
BOX = (748, 390, 873, 562)                 # left, top, right, bottom

# The label inside Mila's sprite, as fractions of its height. The sprite is the
# same photograph for all seventeen products, so one set of bounds serves them.
LABEL_TOP, LABEL_BOT = 0.390, 0.875
LABEL_INSET = 8                            # px of glass either side of the label

# The crimp ring in the plate reads slate-teal; the brand is #2365CD and the
# printed crimp on the real vial is that blue. Nudged, not repainted: the
# highlight and the shading stay, only the hue moves.
CRIMP = (752, 283, 870, 322)
BRAND = np.array((35, 101, 205), float)


def label_art():
    """Mila's label, cropped out of the product sprite."""
    im = Image.open(f"../vials/tmg-{NAME}.png").convert("RGBA")
    a = np.asarray(im); ys, xs = np.where(a[:, :, 3] > 8)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    w, h = im.size
    return im.crop((LABEL_INSET, int(h * LABEL_TOP),
                    w - LABEL_INSET, int(h * LABEL_BOT))).convert("RGB")


def fit(art, w, h):
    """Fill the panel's width, then pad to its height with the label's own white.

    The generated vial is taller and narrower than Mila's, so the artwork does
    not share its aspect. Squashing it 14% to fit would show in the type.
    Padding does not show at all: the pad is sampled from the label's own
    background, which is the same white as the panel it is covering.
    """
    k = w / art.width
    art = art.resize((w, max(1, int(art.height * k))), Image.LANCZOS)
    if art.height >= h:
        top = (art.height - h) // 2
        return art.crop((0, top, w, top + h))
    pad = Image.new("RGB", (w, h), tuple(np.asarray(art)[:6].reshape(-1, 3).mean(axis=0).astype(int)))
    pad.paste(art, (0, (h - art.height) // 2))
    return pad


def relight(art, panel):
    """Give the artwork the shading the blank panel already had."""
    lum = np.asarray(panel.convert("L")).astype(float)
    lum = lum / max(float(np.percentile(lum, 92)), 1.0)        # 1.0 at the highlight
    lum = np.clip(lum, 0.45, 1.12)
    lum = np.asarray(Image.fromarray((lum * 200).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(2.0))).astype(float) / 200.0
    return np.asarray(art).astype(float) * lum[..., None]


def recolour_crimp(im):
    """Move the crimp ring's hue to the brand blue without flattening it."""
    a = np.asarray(im).astype(float)
    x0, y0, x1, y1 = CRIMP
    reg = a[y0:y1, x0:x1]
    r, g, b = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
    blue = (b > r + 12) & (b > 60)                             # the ring, not the fingers
    m = np.zeros(reg.shape[:2]); m[blue] = 1.0
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2))).astype(float) / 255.0
    tone = reg.mean(axis=2, keepdims=True) / max(reg[blue].mean(), 1.0)   # keep the shading
    a[y0:y1, x0:x1] = reg * (1 - m[..., None]) + (BRAND * tone) * m[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


if __name__ == "__main__":
    im = Image.open(PLATE).convert("RGB")
    x0, y0, x1, y1 = BOX
    w, h = x1 - x0, y1 - y0

    panel = im.crop(BOX)
    art = relight(fit(label_art(), w, h), panel)

    # feather the panel's edge so the artwork meets the glass the way the
    # printed label does, rather than as a pasted rectangle
    mask = Image.new("L", (w, h), 0)
    mask.paste(255, (2, 2, w - 2, h - 2))
    mask = mask.filter(ImageFilter.GaussianBlur(1.1))

    im.paste(Image.fromarray(art.clip(0, 255).astype(np.uint8)), (x0, y0), mask)
    im = recolour_crimp(im)
    im.save(OUT, quality=93, optimize=True)
    print(f"  {OUT:26s} {im.width}x{im.height}  {os.path.getsize(OUT) // 1024} KB  [{NAME}]")
