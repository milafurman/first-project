"""Trace the Gila mark from the master raster and write the four mark SVGs.

Run from this directory.

There were two different Gila drawings loose in this project. One sat in
`truemg/assets/marks/mark-original.png` and on the storefront's favicon: a head
with a spiky crest and a fine feathered mane. The other is on all seventeen
vials and in the Canva label pages: a smoother head with bolder strokes and a
heavier ring. Measured as silhouettes they overlap only 53%, so they are not
two exports of one drawing, they are two drawings.

Mila picked the vial one. `../vials/mark-2365CD.png` is therefore the master
here: it is what is printed on the product, it has a real alpha channel, and
97% of its opaque pixels are a single colour, so the trace is taken from a
clean edge rather than from a JPEG-ish blue-vs-grey threshold.

The old SVGs were traced from the OTHER drawing, which is why the logo files
and the product never matched. Nothing reads the mark from a raster at build
time, so without this script the SVGs and the master could drift apart again
with nobody noticing. That is what happened the first time.
"""
import os
import re
import subprocess

import numpy as np
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

MASTER = "../vials/mark-2365CD.png"
# Upsample the master's ANTI-ALIASED alpha and threshold after, never the other
# way round. Enlarging an already-hard-edged mask just magnifies its staircase,
# and potrace then spends hundreds of segments tracing the steps: that route gave
# a 128KB file at WORSE fidelity than this one gives at 10KB.
UPSAMPLE = 2          # 2x: 99.66% silhouette match. 4x buys 0.14% for 2.5x the bytes,
                      # and the lockup built from this gets base64'd into a 10,000
                      # character customCss budget, so the bytes are not free.
ALPHAMAX = 0.9        # corner threshold: high enough to keep the mane's points
QUANTIZE = 1          # potrace -u: coordinates on the pixel grid, not tenths

# A second, lighter trace, for the one place bytes are rationed: the lockup that
# gets base64'd into customCss, which is capped at 10,000 characters. At 1x the
# mark is 3,822 bytes against 10,434 and the silhouette match drops from 99.66%
# to 99.22% — a difference that does not survive being drawn 42px tall in a site
# header. That saving is what lets the Gila into the header at all.
INLINE_UPSAMPLE = 1
VIEWBOX = 1600        # the coordinate space every other script expects

# fill, filename. `currentColor` lets CSS colour it; the rest are literal.
VARIANTS = [
    ("#2365CD",      "truemg-mark-brand.svg"),    # the brand blue. What ships
    ("#0A0A0B",      "truemg-mark-ink.svg"),      # on paper, and for one-colour print
    ("#FCFBF8",      "truemg-mark-paper.svg"),    # knocked out of a dark photograph
    ("currentColor", "truemg-mark-current.svg"),  # inherits from its CSS container
]


def bitmap(path, out):
    """The master's alpha channel, upsampled smooth, as a 1-bit PBM for potrace."""
    im = Image.open(path).convert("RGBA")
    alpha = Image.fromarray(np.asarray(im)[:, :, 3], "L")
    if UPSAMPLE > 1:
        alpha = alpha.resize((im.width * UPSAMPLE, im.height * UPSAMPLE), Image.LANCZOS)
    alpha.point(lambda p: 0 if p > 128 else 255).convert("1").save(out)
    return im.size, (np.asarray(im)[:, :, 3] > 128).mean()


def trace(pbm):
    """potrace, then the path data and the coordinate space it is drawn in."""
    svg = pbm.replace(".pbm", ".svg")
    subprocess.run(["potrace", "-s", "-a", str(ALPHAMAX), "-O", "0.2",
                    "-u", str(QUANTIZE), "-o", svg, pbm], check=True)
    s = open(svg).read()
    g = re.search(r'translate\(([\d.]+),([\d.]+)\) scale\(([\d.]+),-[\d.]+\)', s)
    space = float(g.group(2)) / float(g.group(3))      # 2048 for a 2x-upsampled 1024px master
    paths = "".join(re.findall(r'<path d="[^"]+"/>', s))
    return paths, space


def write(paths, space, fill, out):
    """Same wrapper the rest of the project already reads: a 1600-unit viewBox
    with potrace's own flipped group inside it."""
    k = VIEWBOX / space
    open(out, "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
        'aria-label="TrueMG Gila monster mark">'
        '<g transform="translate(0.000000,%d.000000) scale(%.8f,-%.8f)" '
        'fill="%s" stroke="none">%s</g></svg>'
        % (VIEWBOX, VIEWBOX, VIEWBOX, k, k, fill, paths))


if __name__ == "__main__":
    os.makedirs("_trace", exist_ok=True)
    size, cover = bitmap(MASTER, "_trace/mark.pbm")
    print("master %s, %s, ink coverage %.1f%%" % (MASTER, size, 100 * cover))
    paths, space = trace("_trace/mark.pbm")
    print("traced %d paths in a %.0f-unit space" % (paths.count("<path"), space))
    for fill, out in VARIANTS:
        write(paths, space, fill, out)
        print("  %-30s %5d bytes  %s" % (out, os.path.getsize(out), fill))

    globals()["UPSAMPLE"] = INLINE_UPSAMPLE
    bitmap(MASTER, "_trace/mark-inline.pbm")
    paths, space = trace("_trace/mark-inline.pbm")
    write(paths, space, "#0A0A0B", "truemg-mark-inline.svg")
    print("  %-30s %5d bytes  for the customCss lockup"
          % ("truemg-mark-inline.svg", os.path.getsize("truemg-mark-inline.svg")))
