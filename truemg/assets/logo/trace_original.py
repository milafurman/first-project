"""Trace the ORIGINAL Gila — the spiky-crest drawing — to clean vector.

Mila has gone back to the original mark, the one with the spiky crest and the
fine feathered mane, and asked for it sharper. Sharper does not mean a sharpen
filter. The master is a 900px screenshot of the drawing: soft edges, JPEG
mush, and visible paper texture in the background. No amount of filtering adds
detail that is not there, and unsharp masking a blurry edge just gives it a
halo. Tracing does fix it, because the drawing underneath is flat two-colour
line art, which is exactly what a vector describes perfectly.

This is the sibling of `trace_mark.py`, which does the same job for the vial
drawing. The two differ in one place only: how the ink is separated from the
ground.

  * the vial master is a PNG with a real alpha channel, so the silhouette is
    simply the alpha.
  * this master is flat RGB on a mottled off-white background with no alpha,
    so the ink has to be separated by COLOUR. Blueness — blue minus the
    stronger of red and green — does that cleanly and, critically, degrades
    smoothly at the edges, which gives an anti-aliased mask rather than a
    jagged one.

That matters because of the lesson `trace_mark.py` paid for: upsample the
ANTI-ALIASED mask and threshold afterwards, never the reverse. Enlarging an
already-hard-edged mask magnifies its staircase, and potrace then spends
hundreds of segments tracing the steps — that route produced a 128KB file at
WORSE fidelity than the good route gives at 10KB.

Run from this directory. Needs potrace.
"""
import os
import re
import subprocess

import numpy as np
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

MASTER = "../marks/mark-original.png"
UPSAMPLE = 3          # the master is only 900px and soft, so it needs more room
                      # than the vial's 1024px master did
INLINE_UPSAMPLE = 1   # the lean cut, for the customCss lockup's byte budget
ALPHAMAX = 0.9        # corner threshold: high enough to keep the crest's points
QUANTIZE = 1
VIEWBOX = 1600

# These are the CANONICAL mark filenames. build_lockup.py and render_png.mjs
# read them by name, so writing them here means the lockups, the PNGs and the
# specimen sheet all follow the mark without a single edit — and, more to the
# point, cannot quietly disagree with it later. That disagreement is exactly
# what happened the first time two Gila drawings were loose in this project.
VARIANTS = [
    ("#2365CD",      "truemg-mark-brand.svg"),
    ("#0A0A0B",      "truemg-mark-ink.svg"),
    ("#FCFBF8",      "truemg-mark-paper.svg"),
    ("currentColor", "truemg-mark-current.svg"),
]


def ink(path):
    """The drawing, separated from the ground by colour, with soft edges kept.

    Blueness rather than brightness. A brightness threshold would eat the white
    shapes INSIDE the mark — the eye, the gap under the jaw, the splits between
    the mane strokes — because those are the same white as the background. Blue
    minus the stronger of red and green is near zero on both whites and high on
    the ink, and it falls off gradually across an anti-aliased edge, which is
    the gradient the upsample needs.
    """
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    blue = a[:, :, 2] - np.maximum(a[:, :, 0], a[:, :, 1])
    lo, hi = 12.0, 60.0                               # ground ~0, solid ink ~90
    m = np.clip((blue - lo) / (hi - lo), 0, 1)
    return Image.fromarray((m * 255).astype(np.uint8), "L")


def bitmap(out, upsample):
    m = ink(MASTER)
    size = m.size
    if upsample > 1:
        m = m.resize((m.width * upsample, m.height * upsample), Image.LANCZOS)
    m.point(lambda p: 0 if p > 128 else 255).convert("1").save(out)
    cover = (np.asarray(ink(MASTER)) > 128).mean()
    return size, cover


def trace(pbm):
    svg = pbm.replace(".pbm", ".svg")
    subprocess.run(["potrace", "-s", "-a", str(ALPHAMAX), "-O", "0.2",
                    "-u", str(QUANTIZE), "-o", svg, pbm], check=True)
    s = open(svg).read()
    g = re.search(r'translate\(([\d.]+),([\d.]+)\) scale\(([\d.]+),-[\d.]+\)', s)
    space = float(g.group(2)) / float(g.group(3))
    return "".join(re.findall(r'<path d="[^"]+"/>', s)), space


def write(paths, space, fill, out):
    k = VIEWBOX / space
    open(out, "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
        'aria-label="TrueMG Gila monster mark">'
        '<g transform="translate(0.000000,%d.000000) scale(%.8f,-%.8f)" '
        'fill="%s" stroke="none">%s</g></svg>'
        % (VIEWBOX, VIEWBOX, VIEWBOX, k, k, fill, paths))


if __name__ == "__main__":
    os.makedirs("_trace", exist_ok=True)
    size, cover = bitmap("_trace/og.pbm", UPSAMPLE)
    print("master %s, %s, ink coverage %.1f%%" % (MASTER, size, 100 * cover))
    paths, space = trace("_trace/og.pbm")
    print("traced %d paths in a %.0f-unit space" % (paths.count("<path"), space))
    for fill, out in VARIANTS:
        write(paths, space, fill, out)
        print("  %-32s %6d bytes  %s" % (out, os.path.getsize(out), fill))

    bitmap("_trace/og-inline.pbm", INLINE_UPSAMPLE)
    p2, s2 = trace("_trace/og-inline.pbm")
    write(p2, s2, "#0A0A0B", "truemg-mark-inline.svg")
    print("  %-32s %6d bytes  for the customCss lockup"
          % ("truemg-mark-inline.svg", os.path.getsize("truemg-mark-inline.svg")))
