"""Stand the vials on the spa counter.

`scene.py` builds a room from scratch in code. This does the opposite: it takes
a real photographic plate — `plate-spa.jpg`, generated in Canva and approved by
Mila — and composites the actual product art onto it. The division is
deliberate. An image model makes a convincing room and a terrible vial, because
it invents label text; the label text is the one thing on this site that has to
be exactly right, both because it is the brand and because "NOT FOR HUMAN
CONSUMPTION / RESEARCH USE ONLY" is a compliance line, not a design element.
So the model gets the room and never touches the product.

Two things have to be true for a composite to read as a photograph:

  * the bottles have to sit on the counter's actual plane, at its actual
    perspective. The plane here was measured off the plate, not guessed — see
    FRONT_EDGE and HORIZON_Y below.
  * the background has to defocus the way a real lens does, which is by
    DISTANCE, not by height in the frame. A flat gaussian over the top half is
    the giveaway that something was blurred in post.

Run from this directory.
"""
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

import scene as S

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

PLATE = "plate-spa.jpg"

# --- the counter plane, measured off the plate ------------------------------
# The front-top edge of the counter, found by gradient search along each column
# (the vertical front face is darker than the lit top, so the edge is a clean
# bright-to-dark fall). A straight edge in 3D projects to a straight line, and
# this one fits to within a few pixels across 850px of frame.
FRONT_M, FRONT_C = 0.262, 540.0            # y = Mx + C

# Where the counter's edge and the lit niche above it converge. Everything on
# this plane scales with distance from that line, which is what stops the
# bottles reading as four stickers at four arbitrary sizes.
HORIZON_Y = 471.0

# The bottles stand back from the front edge by this much of the counter's
# visible depth — far enough not to look like they are about to fall off.
SETBACK = 0.34
BASE_M, BASE_C = 0.222, 529.0              # the line their bases sit on

# Scale: a vial's height in pixels is SCALE x its distance below the horizon.
#
# Knowingly generous, and worth being honest about. A 45mm vial on a reception
# counter this deep would be about fifteen pixels tall and completely useless
# as a hero. The perspective between the four bottles is correct — they scale
# against each other and against the counter exactly as the plane demands —
# but the group as a whole is larger than physics would put it. That is an
# ordinary product-photography cheat and it survives because the background is
# defocused: a soft background reads as distant, and a distant background
# stops the eye auditing absolute scale.
SCALE = 0.86

# --- defocus ----------------------------------------------------------------
# Peak blur radius, at the far wall. The near edge of the counter stays sharp.
# Swept at 6 / 10 / 16: 16 destroys the orchids, 10 softens the canopy more
# than asked, 6 leaves the top leaves sharp enough to compete with the product.
# 8 is the dial — turn it, nothing else in the frame moves.
BLUR_MAX = 8.0
BLUR_LEVELS = 12

# name, x centre, height relative to the tallest vial
CAST = [
    ("nad",             905, 0.715),
    ("tmg-3rt",        1065, 0.820),
    ("ghk-cu",         1245, 1.000),
    ("bpc-157-tb-500", 1435, 0.785),
]


def depth_blur(im):
    """Defocus by distance, not by height in the frame.

    On a ground plane receding from the camera, distance goes as
    1 / (y - horizon): the counter's near edge is close, its far end is not,
    and the wall behind it is further still. Blurring on that curve puts the
    softest part of the picture where the leaves are and holds the near edge
    sharp, without anyone having to mask anything by hand.

    Built as a stack of progressively blurred copies cross-faded by the depth
    map, because PIL has no per-pixel-radius blur. Twelve steps is enough that
    the banding is invisible at this size.
    """
    W, H = im.size
    yy = np.mgrid[0:H, 0:W][0].astype(float)

    far = 1.0 / np.maximum(yy - HORIZON_Y, 1.0)            # small = near
    near = 1.0 / max(H - HORIZON_Y, 1.0)                   # the bottom of frame
    d = np.clip((far - near) / (far.max() - near), 0, 1) ** 0.55
    d[yy <= HORIZON_Y] = 1.0                               # the wall and the canopy
    d = ndimage.gaussian_filter(d, 12)                     # no hard edge at the horizon

    out = np.asarray(im).astype(float)
    for i in range(1, BLUR_LEVELS + 1):
        lo, hi = (i - 1) / BLUR_LEVELS, i / BLUR_LEVELS
        layer = np.asarray(im.filter(ImageFilter.GaussianBlur(BLUR_MAX * hi))).astype(float)
        w = np.clip((d - lo) / (hi - lo), 0, 1) * np.clip((hi + 1 / BLUR_LEVELS - d) * BLUR_LEVELS, 0, 1)
        out = out * (1 - w[..., None]) + layer * w[..., None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def place(scene, name, cx, rel):
    """One bottle, with its shadow, standing on the plane at cx."""
    base = BASE_M * cx + BASE_C
    h = max(8, int(SCALE * rel * (base - HORIZON_Y)))

    v = S.vial(name)
    v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)
    v = S.warm(v, 0.34)

    x, y = int(cx - v.width / 2), int(base - h)

    # The key light is the sheer curtain on the left, so shadows fall right and
    # toward the camera. Length grows with distance from the window, the way
    # they do in the plate's own leaf shadows.
    lean = 0.95 + (cx - CAST[0][1]) / 2600.0
    cs, pad = S.cast_shadow(v, 0.46, lean, max(5, int(h * 0.030)))
    scene.alpha_composite(cs, (x - pad, int(base) - pad))

    scene.alpha_composite(S.reflection(v, drop=0.34, strength=0.20), (x, int(base)))
    cp, band = S.contact(v, max(5, int(h * 0.022)))
    scene.alpha_composite(cp, (x, int(base) - band))
    scene.alpha_composite(v, (x, y))


def compose(out="spa-hero.jpg"):
    plate = Image.open(PLATE).convert("RGB")
    scene = depth_blur(plate).convert("RGBA")
    for name, cx, rel in CAST:
        place(scene, name, cx, rel)
    scene.convert("RGB").save(out, quality=90, optimize=True)
    print(f"  {out:24s} {scene.width}x{scene.height}  {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    compose()
