"""Render the vial line from the original photographs in one pass.

This replaces the old cutout -> rebrand -> bluecrimp chain, which recoloured
already-recoloured output and drifted away from the brand blue twice over:

  * the product type came out #2560C1 against #2365CD on the Canva artwork,
    because `rebrand.py` multiplied the brand colour by each pixel's own
    lightness (0.55 + 0.45*lum), which can only ever darken it;
  * the crimp came out #317EFF, a colour in no palette anywhere, because
    `bluecrimp.py` scaled value so the band's MEAN hit the target and then
    clamped at 1.0. Aluminium is full of specular highlights, so a large part
    of the band clipped to V=1.0 — and at the brand's saturation that is
    #2B7EFF. The neon was clipping, not choice.

Both are now mapped onto a ramp built from the brand colour itself, so the
mid-tone lands exactly on brand and the extremes stay believable.

Run from this directory. The original photographs are fetched into cut/src/ on
first run from the URLs in manifest.json, because cut/ is gitignored (17 MB of
source photography) and a fresh clone would otherwise have nothing to render.
"""
import json
import os
import urllib.request
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter

import cutout

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

BRAND = np.array([0x23, 0x65, 0xCD], float)   # #2365CD, sampled from the Canva labels
LIZARD_BOX = (725, 1185, 950, 1420)           # old mark on the 2000px label, measured
CRIMP = (0.085, 0.170)                        # aluminium band, as a fraction of height
PAPER = np.array([246, 246, 247], float)      # the label stock

# The mark printed on the label. Mila went back to the ORIGINAL Gila — the
# spiky crest with the feathered mane — and no vials had been printed yet, so
# the label artwork moves with the brand rather than diverging from it. The two
# drawings overlap only 53% as silhouettes, so this is a real change, not a
# re-export. mark-2365CD.png (the smooth drawing) stays in the tree as the
# record of what the labels used to carry.
MARK = "mark-og-2365CD.png"


def blue_mask(rgb):
    """The printed blue: strongly blue-dominant, unlike white, black or grey."""
    r, g, b = rgb[:, :, 0].astype(int), rgb[:, :, 1].astype(int), rgb[:, :, 2].astype(int)
    return (b - r > 45) & (b - g > 25) & (b > 90)


def ramp(t, dark, mid, light):
    """Map t in [0,1] onto dark -> mid -> light, so t=0.5 lands exactly on mid."""
    t = t[..., None]
    lo = dark + (mid - dark) * np.clip(t * 2, 0, 1)
    hi = mid + (light - mid) * np.clip((t - 0.5) * 2, 0, 1)
    return np.where(t < 0.5, lo, hi)


def recolour_type(a, mask):
    """Printed ink: hold each pixel's coverage, swap the pigment for the brand.

    Antialiased glyph edges are part paper, part ink. Coverage is how far the
    pixel has travelled from the paper toward full ink, so re-inking it means
    walking that same distance toward the brand colour instead."""
    if not mask.any():
        return
    px = a[:, :, :3][mask].astype(float)
    far = np.linalg.norm(PAPER - BRAND)
    cov = np.clip(np.linalg.norm(PAPER - px, axis=1) / far, 0, 1)[:, None]
    a[:, :, :3][mask] = np.clip(PAPER + (BRAND - PAPER) * cov, 0, 255).astype(np.uint8)


def swap_mark(a, mark):
    """Erase the old lizard, rebuilding the label's gradient, then drop the new one."""
    x0, y0, x1, y1 = LIZARD_BOX
    rgb = a[:, :, :3]
    old = blue_mask(rgb)[y0:y1, x0:x1]
    patch = rgb[y0:y1, x0:x1].copy()
    if old.any():
        grow = ndimage.binary_dilation(old, iterations=4)
        clean = ~grow
        glob = (np.median(patch[clean].reshape(-1, 3), axis=0)
                if clean.any() else PAPER)
        # the label carries a soft vertical gradient; a flat fill leaves a patch,
        # so rebuild it row by row from the clean pixels on that row
        for yy in range(patch.shape[0]):
            if not grow[yy].any():
                continue
            src = patch[yy][clean[yy]]
            fill = np.median(src, axis=0) if src.shape[0] >= 8 else glob
            patch[yy][grow[yy]] = fill.astype(np.uint8)
        sm = np.asarray(Image.fromarray(patch).filter(ImageFilter.GaussianBlur(2.5))).astype(float)
        w = ndimage.gaussian_filter(grow.astype(float), 3.0)[..., None]
        patch = np.clip(patch * (1 - w) + sm * w, 0, 255).astype(np.uint8)
        a[y0:y1, x0:x1, :3] = patch

    out = Image.fromarray(a, "RGBA")
    bw, bh = x1 - x0, y1 - y0
    # FIT inside the box, do not fill it. The box is 225x235 and was being used
    # as the output size directly, which stretched whatever mark it was handed
    # by about 4%. That was invisible while one mark was in use and its own
    # proportions were baked into the master; it stops being invisible the
    # moment the mark changes shape.
    ms = mark.crop(mark.getbbox())
    k = min(bw * 0.94 / ms.width, bh * 0.94 / ms.height)
    m = ms.resize((max(1, int(ms.width * k)), max(1, int(ms.height * k))), Image.LANCZOS)
    out.alpha_composite(m, (x0 + (bw - m.width) // 2, y0 + (bh - m.height) // 2))
    return out


def recolour_crimp(im):
    """Anodised blue aluminium: keep the metal's shading, change what it is made of.

    The band's own luminance, normalised between its 2nd and 98th percentile,
    drives a ramp from a deep shadow through the brand colour to a near-white
    specular. Normalising on percentiles rather than the mean is what stops the
    highlights piling up at full value and turning neon.
    """
    a = np.asarray(im).astype(float).copy()
    al = a[:, :, 3] > 128
    rows = np.where(al.any(axis=1))[0]
    y0 = rows.min() + int((rows.max() - rows.min()) * CRIMP[0])
    y1 = rows.min() + int((rows.max() - rows.min()) * CRIMP[1])
    band, m = a[y0:y1, :, :3], al[y0:y1]
    if not m.any():
        raise SystemExit("empty crimp band")

    # Anchor the ramp on the band's MEDIAN, not the midpoint of its range.
    # Aluminium is a bright object: its luminance is bunched up near the top, so
    # a midpoint anchor puts most of the band in the highlight half and the crimp
    # reads as pale sky (#AAC3EB). Splitting at the median instead puts half the
    # pixels either side of the brand colour, which is what makes it read as brand.
    lum = band[..., :3].max(axis=2)
    lo, med, hi = np.percentile(lum[m], (2, 50, 98))
    v = lum[m]
    t = np.where(v < med,
                 0.5 * (v - lo) / max(med - lo, 1e-6),
                 0.5 + 0.5 * (v - med) / max(hi - med, 1e-6))
    t = np.clip(t, 0, 1)

    dark = BRAND * 0.34                      # the shadowed underside of the band
    light = BRAND + (255 - BRAND) * 0.78     # the specular along its crown
    band[m] = np.clip(ramp(t, dark, BRAND, light), 0, 255)
    a[y0:y1, :, :3] = band
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def render(name, mark):
    img, _ = cutout.cut("cut/src/" + name)
    a = np.asarray(img).astype(np.uint8).copy()

    x0, y0, x1, y1 = LIZARD_BOX
    inbox = np.zeros(a.shape[:2], bool); inbox[y0:y1, x0:x1] = True
    recolour_type(a, blue_mask(a[:, :, :3]) & ~inbox)

    return recolour_crimp(swap_mark(a, mark))


def fetch_sources():
    """Pull any missing original photograph from the store's CDN."""
    os.makedirs("cut/src", exist_ok=True)
    got = 0
    for e in json.load(open("manifest.json")):
        p = "cut/src/" + e["file"]
        if not os.path.exists(p):
            urllib.request.urlretrieve(e["url"], p)
            got += 1
    if got:
        print("  fetched %d original photograph(s)" % got)


if __name__ == "__main__":
    fetch_sources()
    mark = Image.open(MARK).convert("RGBA")
    names = sorted(os.listdir("cut/src"))
    for n in names:
        render(n, mark).save(n)
        print("  rendered", n)
    print("done:", len(names))
