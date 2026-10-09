"""Lift the vials off the page: the catalog set, floating, with a cast shadow.

Mila pointed at a competitor's product page and said the bottles there look 3D
and floating. Theirs are CGI renders. Hers are photographs, which are already
as three-dimensional as an object gets — what they were missing is not depth,
it is CONTACT. A cut-out photograph dropped on a white card has no shadow, so
the eye reads it as a sticker lying flat on the page rather than an object
standing in a space. Give it a shadow it does not quite touch and the same
photograph lifts.

Two other things were costing her the look, both measured rather than guessed:

  * the uploaded product images are RGB, not RGBA. The transparency was
    flattened on the way in, so no amount of CSS can draw a shadow that
    follows the silhouette — a `drop-shadow` filter on a flat white square
    outlines the SQUARE. The shadow has to be baked into the pixels.
  * the sprite is 652x1589 of ink inside a 2000x2000 canvas. That LOOKS like
    wasted canvas, and the first version of this script was written to reclaim
    it — but the card is square and `object-contain` fits the square, so the
    binding dimension is the height, and the vial is already at 79% of it.
    Reframing buys almost nothing. Measuring it first saved shipping a change
    that would have been sold as "bigger" and delivered nothing. The shadow is
    the whole effect.

The shadow is built in two parts, because one blurred blob never convinces:

  * a CONTACT pool — the silhouette's own footprint, squashed almost flat and
    blurred a little. It carries the vial's actual outline, which is what makes
    it belong to this object rather than to a generic bottle.
  * an AMBIENT pool — much wider, much softer, much fainter, offset further.
    It is the room, not the lamp.

Both are drawn with a gap below the glass. That gap is the whole trick: a
shadow starting exactly at the base reads as standing, a shadow starting a
little below reads as hovering.

Run from this directory.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

OUT = "float"
SIZE = 1600                 # square, to match the card's aspect-square well
VIAL_H = 0.790              # matches the height the uploads already render at
VIAL_TOP = 0.040            # leaves 17% under the base for the shadow to live in

GAP = 0.012                 # clear air between the glass and its shadow, in canvas
# `shift` is the light direction. The photographs are lit from the upper left,
# so both pools lean right; a shadow sitting dead centre under the vial reads
# as a turntable render rather than an object on a surface.
CONTACT = dict(squash=0.075, blur=0.020, alpha=0.30, spread=1.04, drop=0.006, shift=0.012)
AMBIENT = dict(squash=0.150, blur=0.062, alpha=0.15, spread=1.60, drop=0.032, shift=0.035)

TILT = 0.0                  # degrees; the catalog set stays upright (see below)


def sprite(path):
    """The vial, cropped to its own ink."""
    im = Image.open(path).convert("RGBA")
    ys, xs = np.where(np.asarray(im)[:, :, 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def pool(alpha, cx, base, cfg, size):
    """One elliptical shadow, carrying the silhouette's own footprint.

    The silhouette is squashed to a sliver rather than drawn as an ellipse, so
    the shadow inherits the vial's real width profile — wider at the shoulder,
    narrower at the neck — instead of a shape that fits any bottle.
    """
    w = max(1, int(alpha.width * cfg["spread"]))
    h = max(1, int(alpha.height * cfg["squash"]))
    sh = alpha.resize((w, h), Image.LANCZOS)

    lay = Image.new("L", (size, size), 0)
    lay.paste(sh, (int(cx - w / 2 + cfg["shift"] * size),
                   int(base + (GAP + cfg["drop"]) * size)))
    lay = lay.filter(ImageFilter.GaussianBlur(cfg["blur"] * size))
    return Image.fromarray((np.asarray(lay).astype(float) * cfg["alpha"]).astype(np.uint8))


def build(path, out, tilt=TILT, size=SIZE):
    v = sprite(path)
    if tilt:
        v = v.rotate(tilt, Image.BICUBIC, expand=True)

    k = (VIAL_H * size) / v.height
    v = v.resize((max(1, int(v.width * k)), max(1, int(v.height * k))), Image.LANCZOS)

    x = (size - v.width) // 2
    y = int(VIAL_TOP * size)
    base = y + v.height

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    alpha = v.getchannel("A")
    # shadow first, ambient under contact, both as soft black
    for cfg in (AMBIENT, CONTACT):
        m = pool(alpha, size / 2, base, cfg, size)
        canvas.paste(Image.new("RGBA", (size, size), (17, 22, 33, 255)), (0, 0), m)
    canvas.paste(v, (x, y), v)

    canvas.save(out, optimize=True)
    return canvas


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sorted(n for n in os.listdir(".") if n.startswith("tmg-") and n.endswith(".png"))
    for n in names:
        o = os.path.join(OUT, n)
        im = build(n, o)
        print("  %-36s %dx%d  %d KB" % (o, im.width, im.height, os.path.getsize(o) // 1024))
    print("%d floated" % len(names))


# ---------------------------------------------------------------------------
# The marketing cluster: several vials at different tilts and depths, the way
# the competitor's hero does it. Tilt is where a photograph starts to show its
# limits — the cap's ellipse and the label's wrap were fixed when the shutter
# fired and cannot open up to match a new angle — so these stay inside about
# 22 degrees, where nobody reads the discrepancy.

# Weighted to the right. The hero's headline owns the left 45% of the frame,
# and a cluster centred in the plate puts a vial directly under the first line
# of type — the same mistake the spa plate made before the row was moved.
CLUSTER = [
    # name,                 tilt,  scale, x,     y    (fractions of the frame)
    ("tmg-nad",             -21.0, 1.00, 0.545, 0.560),
    ("tmg-ghk-cu",           13.0, 0.74, 0.705, 0.470),
    ("tmg-tmg-3rt",          -7.0, 0.63, 0.820, 0.545),
    ("tmg-bpc-157-tb-500",   19.0, 0.52, 0.880, 0.470),
]
# A phone has no left and right to trade, so the cluster recentres there.
CLUSTER_MOBILE = [(n, t, s, (x - 0.21), y) for n, t, s, x, y in CLUSTER]
PANEL = ((247, 248, 252), (235, 239, 248))


def cluster(out, size=(2560, 1150), bg=PANEL, cast=None):
    W, H = size
    g = np.linspace(0, 1, H)[:, None, None]
    a = np.array(bg[0], float)[None, None] * (1 - g) + np.array(bg[1], float)[None, None] * g
    frame = Image.fromarray(np.repeat(a, W, axis=1).astype(np.uint8), "RGB").convert("RGBA")

    unit = H * 0.74                                  # the tallest vial
    for name, tilt, scale, fx, fy in (cast or CLUSTER):
        v = sprite(name + ".png").rotate(tilt, Image.BICUBIC, expand=True)
        k = (unit * scale) / v.height
        v = v.resize((max(1, int(v.width * k)), max(1, int(v.height * k))), Image.LANCZOS)
        cx, base = int(W * fx), int(H * fy) + v.height // 2

        # the same two pools, drawn into a frame-sized layer so they can fall
        # anywhere rather than only inside the vial's own box
        for cfg in (AMBIENT, CONTACT):
            w = max(1, int(v.width * cfg["spread"]))
            h = max(1, int(v.height * cfg["squash"]))
            lay = Image.new("L", (W, H), 0)
            lay.paste(v.getchannel("A").resize((w, h), Image.LANCZOS),
                      (int(cx - w / 2 + cfg["shift"] * H), int(base + (GAP + cfg["drop"]) * H)))
            lay = lay.filter(ImageFilter.GaussianBlur(cfg["blur"] * H))
            m = Image.fromarray((np.asarray(lay).astype(float) * cfg["alpha"]).astype(np.uint8))
            frame.paste(Image.new("RGBA", (W, H), (17, 22, 33, 255)), (0, 0), m)

        frame.paste(v, (cx - v.width // 2, base - v.height), v)

    frame.convert("RGB").save(out, quality=90, optimize=True)
    print("  %-36s %dx%d  %d KB" % (out, W, H, os.path.getsize(out) // 1024))
