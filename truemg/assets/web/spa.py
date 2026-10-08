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
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage

import scene as S

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

PLATE = "plate-spa.jpg"

# --- framing ----------------------------------------------------------------
# A crop is not a cosmetic choice here, it is the fix for the scale problem.
# The plate is an architectural wide shot, and a wide shot says the camera is
# across the room — which makes a hero-sized vial physically impossible and is
# most of why the first composite read as a collage. Cropping in says the
# camera is close, and a close camera makes the same bottles reasonable. The
# measured plane below stays in ORIGINAL plate coordinates and is transformed
# through this crop in code, so the geometry cannot drift out of step with the
# framing the way hand-copied numbers would.
CROP = (400, 120, 1680, 840)               # left, top, right, bottom
OUT_W = 1680

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
SCALE = 0.76

# --- defocus ----------------------------------------------------------------
# Peak blur radius, at the far wall. The near edge of the counter stays sharp.
# Swept at 6 / 10 / 16: 16 destroys the orchids, 10 softens the canopy more
# than asked, 6 leaves the top leaves sharp enough to compete with the product.
# 8 is the dial — turn it, nothing else in the frame moves.
BLUR_MAX = 6.0
BLUR_LEVELS = 12

# name, x centre, height relative to the tallest vial
CAST = [
    ("nad",             480, 0.715),
    ("tmg-3rt",         700, 0.820),
    ("ghk-cu",          940, 1.000),
    ("bpc-157-tb-500", 1190, 0.785),
]


def depth_blur(im, horizon):
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

    far = 1.0 / np.maximum(yy - horizon, 1.0)            # small = near
    near = 1.0 / max(H - horizon, 1.0)                   # the bottom of frame
    d = np.clip((far - near) / (far.max() - near), 0, 1) ** 0.55
    d[yy <= horizon] = 1.0                               # the wall and the canopy
    d = ndimage.gaussian_filter(d, 12)                     # no hard edge at the horizon

    out = np.asarray(im).astype(float)
    for i in range(1, BLUR_LEVELS + 1):
        lo, hi = (i - 1) / BLUR_LEVELS, i / BLUR_LEVELS
        layer = np.asarray(im.filter(ImageFilter.GaussianBlur(BLUR_MAX * hi))).astype(float)
        w = np.clip((d - lo) / (hi - lo), 0, 1) * np.clip((hi + 1 / BLUR_LEVELS - d) * BLUR_LEVELS, 0, 1)
        out = out * (1 - w[..., None]) + layer * w[..., None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def relight(v, rim=1.0, blur=0.0):
    """Light the bottle with the room's light instead of the studio's.

    This is the difference between a composite and a collage. The vial PNGs
    were shot flat on white seamless: even frontal light, bright white faces,
    hard edges. The plate is lit the opposite way — a sheer curtain behind and
    to the left, throwing warm light toward the camera. Dropping one into the
    other and tinting it warm does not work, and should not: a frontlit object
    with a warm filter on it is still a frontlit object, and the eye reads the
    mismatch instantly even when it cannot name it.

    Four moves, in the order light actually does them:

      1. KNOCK THE KEY DOWN. Nothing in this room is lit from the camera, so
         the bright frontal faces lose most of their brightness. This alone
         does more than everything else combined.
      2. RIM THE LEFT EDGE. A backlight wraps the silhouette facing it. Taken
         from the alpha channel shifted right and subtracted, so the band
         follows the real outline including the cap and the crimp.
      3. FILL FROM THE RIGHT. The lit niche is a long warm source on that
         side, so the shadow side is not black, it is bronze.
      4. SIT IT IN THE AIR. Match the local defocus and drop the contrast to
         the plate's, because a studio curve against a hazy room is its own
         kind of cut-out.

    The brand blue is held through all of it, as everywhere else.
    """
    a = np.asarray(v.getchannel("A")).astype(float) / 255.0
    px = np.asarray(v.convert("RGB")).astype(float)
    r_, g_, b_ = px[:, :, 0], px[:, :, 1], px[:, :, 2]
    brand = (b_ - r_ > 45) & (b_ - g_ > 25) & (b_ > 90)
    hold = ndimage.gaussian_filter(brand.astype(float), 1.2)[..., None]

    lit = px * 0.78                                        # 1. kill the studio key
    lit += (np.array((120, 104, 86), float) - lit) * 0.16  # ambient, warm not grey

    H_, W_ = a.shape
    sh = max(2, int(W_ * 0.034))
    left = np.clip(a - np.pad(a, ((0, 0), (sh, 0)))[:, :W_], 0, 1)      # 2. the wrap
    left = ndimage.gaussian_filter(left, W_ * 0.0055) * rim
    lit += (np.array((255, 238, 208), float) - lit) * np.clip(left * 1.25, 0, 0.66)[..., None]

    right = np.clip(a - np.pad(a, ((0, 0), (0, sh)))[:, sh:], 0, 1)     # 3. the niche
    right = ndimage.gaussian_filter(right, W_ * 0.014)
    lit += (np.array((236, 196, 142), float) - lit) * np.clip(right * 0.80, 0, 0.38)[..., None]

    px = px * hold * 0.45 + lit * (1 - hold * 0.45)
    rgb = Image.fromarray(px.clip(0, 255).astype(np.uint8))
    rgb = ImageEnhance.Contrast(rgb).enhance(0.88)         # 4. the plate's curve
    out = Image.merge("RGBA", (*rgb.split(), v.getchannel("A")))
    return out.filter(ImageFilter.GaussianBlur(blur)) if blur else out


def view():
    """The crop, and the transform that carries the measured plane through it."""
    k = OUT_W / (CROP[2] - CROP[0])
    front = lambda x: (FRONT_M * (x / k + CROP[0]) + FRONT_C - CROP[1]) * k
    base = lambda x: (BASE_M * (x / k + CROP[0]) + BASE_C - CROP[1]) * k
    return k, front, base, (HORIZON_Y - CROP[1]) * k


def place(scene, name, cx, rel, k, baseline, horizon):
    """One bottle, with its shadow, standing on the plane at cx."""
    base = baseline(cx)
    h = max(8, int(SCALE * rel * (base - horizon)))

    v = S.vial(name)
    v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)
    # defocus to match the plane the bottle stands on — nearer than the wall
    # behind it, so a fraction of the plate's blur at this depth
    v = relight(v, rim=1.0, blur=max(0.0, BLUR_MAX * k * 0.05 * (1 - (base - horizon) / 620.0)))

    x, y = int(cx - v.width / 2), int(base - h)

    # The key light is the sheer curtain on the left, so shadows fall right and
    # toward the camera. Length grows with distance from the window, the way
    # they do in the plate's own leaf shadows.
    # The curtain is a hard, low source, so the shadows in this room are long
    # and definite — look at what the orchid throws on the wall. The first pass
    # used scene.py's soft studio shadow and the bottles floated because of it.
    lean = 1.35 + (cx - CAST[0][1]) / 2000.0
    for length, blur, n in ((0.95, 0.055, 2), (0.34, 0.016, 3)):
        cs, pad = S.cast_shadow(v, length, lean, max(4, int(h * blur)))
        for _ in range(n):                            # deepen: one pass is too pale
            scene.alpha_composite(cs, (x - pad, int(base) - pad))

    scene.alpha_composite(S.reflection(v, drop=0.34, strength=0.22), (x, int(base)))
    cp, band = S.contact(v, max(4, int(h * 0.018)))
    for _ in range(2):
        scene.alpha_composite(cp, (x, int(base) - band))
    scene.alpha_composite(v, (x, y))


def compose(out="spa-hero.jpg"):
    plate = Image.open(PLATE).convert("RGB").crop(CROP)
    k, _, baseline, horizon = view()
    plate = plate.resize((OUT_W, int(plate.height * k)), Image.LANCZOS)
    scene = depth_blur(plate, horizon).convert("RGBA")
    for name, cx, rel in CAST:
        place(scene, name, cx, rel, k, baseline, horizon)
    scene.convert("RGB").save(out, quality=90, optimize=True)
    print(f"  {out:24s} {scene.width}x{scene.height}  {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    compose()
