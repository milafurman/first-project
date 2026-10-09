"""Favicons from the spiky mark.

A favicon is 32 logical pixels wide in a browser tab, and the mark's mane is
made of fine separated strokes. Shrink it straight down and those strokes
collapse into a blue smear — not a bad-looking smear, just an unidentifiable
one. So there are two cuts, and the choice is a real one:

  * KNOCKED OUT — the mark in white on a solid brand-blue rounded square.
    One shape, maximum contrast, legible at 16px, and it holds its own
    against the coloured squares every other tab is showing.
  * PLAIN — the blue mark on white with breathing room. Prettier large,
    quieter small, and it disappears against a light browser chrome.

Knocked-out is the default because the job of a favicon is to be found in a
row of twenty tabs, not to be admired.

Sizes: 512 (stores, PWA), 180 (iOS home screen, which has no transparency and
will composite onto black if you give it any), 32 and 16 (the tab itself).

Run from this directory.
"""
import os

import numpy as np
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

MARK = "../vials/mark-og-2365CD.png"
BRAND = (0x23, 0x65, 0xCD)
SIZES = (512, 180, 32, 16)
RADIUS = 0.22                      # of the square's width, iOS-ish
INSET_KNOCK = 0.17                 # the mark's margin inside the blue square
INSET_PLAIN = 0.10


def mark(invert=False):
    """The mark, cropped to its ink, optionally knocked to white."""
    im = Image.open(MARK).convert("RGBA")
    im = im.crop(im.getbbox())
    if invert:
        a = np.asarray(im).copy()
        a[:, :, :3] = 255
        im = Image.fromarray(a, "RGBA")
    return im


def square(size, inset, fg, bg, radius=None):
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if bg is not None:
        d = ImageDraw.Draw(c)
        r = int(size * (RADIUS if radius is None else radius))
        d.rounded_rectangle([0, 0, size - 1, size - 1], r, fill=bg + (255,))
    room = int(size * (1 - 2 * inset))
    k = min(room / fg.width, room / fg.height)
    m = fg.resize((max(1, int(fg.width * k)), max(1, int(fg.height * k))), Image.LANCZOS)
    c.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return c


if __name__ == "__main__":
    os.makedirs("favicon", exist_ok=True)
    knock, plain = mark(invert=True), mark()
    for s in SIZES:
        # iOS strips alpha and composites what is left onto black, so the 180
        # gets an opaque square with no corner radius — the OS applies its own
        square(s, INSET_KNOCK, knock, BRAND, radius=0.0 if s == 180 else None
               ).save("favicon/truemg-icon-%d.png" % s)
        square(s, INSET_PLAIN, plain, (255, 255, 255)
               ).save("favicon/truemg-icon-plain-%d.png" % s)
        print("  truemg-icon-%-4d  and  -plain-%-4d" % (s, s))
