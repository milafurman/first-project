"""Product tiles: the vial standing on the spa ledge, the ledge colour-coded.

Mila, on the reference storefront: colour-code only the photo background, and
put the vial on the ledge we built. Those are the same note. Their product
panel is a tinted wash with the bottle floating on it; the tint is the PANEL,
never the label. Ours gets a real surface instead of a wash, which is the one
thing we have that a CGI render does not.

The crop is deliberately tight — counter, the lit niche behind it, and nothing
else. The orchids and the monstera are the best part of that plate and they
have no business in a 240px product tile: at that size they fight the vial and
neither wins. They stay in the hero, where there is room for them.

Order of operations matters and is not obvious. The plate is graded FIRST and
the vial placed into it afterwards, so the colour lands on the room and not on
the product. Grading the finished composite would tint the white label, which
is the exact thing she ruled out, and grading before placing also means
`spa.relight` keeps doing its job against the room it was tuned against.

Softness in the background is free here: a 381px crop of the plate blown up to
1200 is a 3x upscale, but the region is defocused stone and a glow with no
detail to lose, while the vial composites at full resolution. Soft ground,
sharp subject — which is what a real product photograph looks like anyway.

Run from this directory.
"""
import os

import numpy as np
from PIL import Image

import spa

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

OUT = "../vials/ledge"
SIZE = 1200
SLOT = 1083.0                     # the row position to centre on, in plate pixels
TILE = 330.0                      # square crop, in plate pixels
DROP = 0.300                      # how far below the crop's centre the row sits

STRENGTH = 0.70                   # how far the room travels toward the tint
KEY = 0.96                        # studio light kept on the vial; the hero keeps 0.78
SETTLE = 0.35                     # how much of the hero's background pulldown to use

# Same families as the label mock, so a compound keeps one colour wherever it
# appears. The hues sit a little stronger than the label version did: a wall
# three metres back can carry colour that a label 40mm wide cannot.
FAMILY = {
    "repair":    ("#C6D8C9", ["bpc-157-tb-500", "ghk-cu", "thymosin-alpha-1"]),
    "metabolic": ("#C2D6EC", ["nad", "mots-c", "ss-31"]),
    "growth":    ("#E6CFCB", ["tesamorelin", "ipamorelin", "cjc-1295-no-dac-ipamorelin",
                              "tmg-2tz", "tmg-3rt"]),
    "cognitive": ("#CFC8E2", ["semax", "selank", "epithalon", "klow"]),
    "supplies":  ("#DFD6C6", ["tmg-bac", "vitamin-b12"]),
}


def family(name):
    for key, (hexc, members) in FAMILY.items():
        if name in members:
            return key, tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "supplies", tuple(int(FAMILY["supplies"][0][i:i + 2], 16) for i in (1, 3, 5))


def grade(im, tint, strength=STRENGTH):
    """Move the room onto one colour without flattening it.

    Two steps, and the first one is the one that was missing. Mixing a sage
    tint straight into a warm cream room gives olive, because the cream is
    still in there fighting it — every family came out a muddy variant of the
    same khaki. So the plate is pulled to its own LUMINANCE first, which
    throws the cream away and leaves the light, and only then colourised.

    The tint is multiplied by that luminance rather than laid over it, so the
    lit niche stays the brightest thing in the frame and the counter keeps its
    falloff. A flat colour mixed in gives a room with coloured fog in front of
    it, which is the usual way a tinted photograph goes wrong.
    """
    a = np.asarray(im.convert("RGB")).astype(float)
    lum = (a * np.array((0.299, 0.587, 0.114))).sum(axis=2, keepdims=True) / 255.0
    neutral = lum * 255.0
    t = np.array(tint, float)[None, None] * np.clip(lum * 1.14, 0, 1)
    return Image.fromarray((neutral * (1 - strength) + t * strength).clip(0, 255).astype(np.uint8))


def crop_box():
    cy = spa.ROW_PLATE_Y - TILE * DROP
    return (int(SLOT - TILE / 2), int(cy - TILE / 2),
            int(SLOT + TILE / 2), int(cy + TILE / 2))


def tile(name, out, size=SIZE):
    box = crop_box()
    k = size / (box[2] - box[0])
    horizon = (spa.HORIZON_Y - box[1]) * k
    base = (spa.ROW_PLATE_Y - box[1]) * k

    plate = Image.open(spa.PLATE).convert("RGB").crop(box).resize((size, size), Image.LANCZOS)
    plate = spa.depth_blur(plate, horizon)
    plate = grade(plate, family(name)[1])
    # the hero pulls the room down hard so a small bottle can separate from it;
    # a tile does not need nearly as much, and the full amount leaves the
    # ledge muddy at the bottom of the frame
    scene = Image.blend(plate, spa.settle(plate, horizon, base), SETTLE).convert("RGBA")

    # row_x only feeds the "how near the window is this one" term, and a tile
    # holds a single bottle, so it gets the middle of the row's lighting
    spa.place(scene, name, size / 2, k, horizon, base, (0.0, size, 2 * size), key=KEY)
    scene.convert("RGB").save(out, quality=92, optimize=True)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sorted(n[4:-4] for n in os.listdir("../vials")
                   if n.startswith("tmg-") and n.endswith(".png"))
    for n in names:
        o = os.path.join(OUT, "tmg-%s.jpg" % n)
        tile(n, o)
        print("  %-40s %-10s %d KB" % (o, family(n)[0], os.path.getsize(o) // 1024))
    print("%d tiles" % len(names))
