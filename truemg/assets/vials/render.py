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

Run from this directory. The original photographs live in cut/src/ and are
COMMITTED. They used to be gitignored and fetched from the URLs in
manifest.json on first run, which quietly made the whole visual system depend
on files that are also the live product images in the store admin — replacing
those could have taken the masters with them, and nothing could be re-rendered
again without a reshoot. fetch_sources() stays as a fallback for a file that
somehow goes missing; it is no longer the normal path.
"""
import json
import os
import urllib.request
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter

import cutout

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
import json
BRAND_HEX = json.load(open("../brand.json"))["brand"]   # one source of truth

BRAND = np.array([int(BRAND_HEX[i:i + 2], 16) for i in (1, 3, 5)], float)
LIZARD_BOX = (725, 1185, 950, 1420)           # old mark on the 2000px label, measured
# Search windows for the aluminium band's two edges, as a fraction of the
# vial's height. These are NOT the band itself — the band is found per column
# inside these windows, because its edges are ellipse arcs and not straight
# lines. See find_crimp().
CRIMP_TOP = (0.055, 0.108)                    # the white disc -> metal seam
CRIMP_BOT = (0.158, 0.175)                    # the metal -> glass neck seam
PAPER = np.array([246, 246, 247], float)      # the label stock

# The mark printed on the label. Mila went back to the ORIGINAL Gila — the
# spiky crest with the feathered mane — and no vials had been printed yet, so
# the label artwork moves with the brand rather than diverging from it. The two
# drawings overlap only 53% as silhouettes, so this is a real change, not a
# re-export. The smooth drawing is archived at ../_archive/smooth-mark/ as
# the record of what the labels used to carry.
MARK = "mark-og.png"


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


def find_crimp(lum, al, r0, H, cols):
    """The aluminium band's real top and bottom edge, per column.

    The band used to be defined by two flat fractions of the vial's height,
    which is wrong for a reason you can see on the finished picture: the cap is
    a cylinder photographed slightly from above, so both of its edges are
    ELLIPSE ARCS. A horizontal cut can only agree with an arc at one point.

    Measured on the masters: the top edge sits at row 306 under the middle of
    the cap and 313 at either side, a 7px arch. The flat cut started at 322, so
    it left 16px of bare metal showing under the white disc in the middle and
    about 10px at the sides. That is both of the things Mila saw — a silver
    strip where the blue should meet the white, and a white edge that looks
    crooked, because the strip is wedge-shaped rather than parallel.

    Top edge: the steepest darkening in the window, which is the shadow seam
    where the white plastic disc overhangs the metal.
    Bottom edge: the first row that goes dark (the glass neck) or leaves the
    silhouette — the cap overhangs the glass, so at the outer columns there is
    background below the band, not glass.
    """
    def smooth(e, deg):
        """Median, reject outliers, then a low-order fit: the edge is a shallow
        arc, so a wild column is noise and not shape. The degree is kept low on
        purpose — a degree-4 fit to the bottom edge chased its own noise and
        scalloped the band."""
        ok = ~np.isnan(e)
        if ok.sum() < 64:
            raise SystemExit("could not find the crimp band")
        xv = np.where(ok)[0]
        med = ndimage.median_filter(e[ok], size=41, mode="nearest")
        keep = np.abs(med - np.median(med)) <= 12          # px
        if keep.sum() < 64:
            keep[:] = True
        out = np.full_like(e, np.nan)
        out[cols] = np.polyval(np.polyfit(xv[keep], med[keep], deg), cols)
        return out

    t0, t1 = r0 + int(H * CRIMP_TOP[0]), r0 + int(H * CRIMP_TOP[1])
    b0, b1 = r0 + int(H * CRIMP_BOT[0]), r0 + int(H * CRIMP_BOT[1])

    top = np.full(lum.shape[1], np.nan)
    bot = np.full(lum.shape[1], np.nan)
    for x in cols:
        seg, op = lum[t0:t1 + 1, x], al[t0:t1 + 1, x]
        if op.sum() >= 6:
            g = np.diff(np.where(op, seg, np.nan))
            if not np.all(np.isnan(g)):
                top[x] = t0 + int(np.nanargmin(g)) + 1

        # The LAST metal row, not the first dark one. Looking for the first dark
        # row runs past the band's bright lower crown and into the glass neck;
        # at the outer columns there is no glass under the cap at all, only
        # background, so "dark" never arrives and the search runs to the end of
        # its window.
        ys = [y for y in range(b0, b1 + 1) if al[y, x] and lum[y, x] >= 150]
        if ys:
            bot[x] = ys[-1]

    return np.ceil(smooth(top, 4)), np.floor(smooth(bot, 2))


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
    cols = np.where(al.any(axis=0))[0]
    r0, H = rows.min(), rows.max() - rows.min()
    lum = a[:, :, :3].max(axis=2)

    top, bot = find_crimp(lum, al, r0, H, cols)
    yy = np.arange(a.shape[0])[:, None]
    m = al & (yy >= top[None, :]) & (yy <= bot[None, :])
    if not m.any():
        raise SystemExit("empty crimp band")

    # Anchor the ramp on the band's MEDIAN, not the midpoint of its range.
    # Aluminium is a bright object: its luminance is bunched up near the top, so
    # a midpoint anchor puts most of the band in the highlight half and the crimp
    # reads as pale sky (#AAC3EB). Splitting at the median instead puts half the
    # pixels either side of the brand colour, which is what makes it read as brand.
    v = lum[m]
    lo, med, hi = np.percentile(v, (2, 50, 98))
    t = np.where(v < med,
                 0.5 * (v - lo) / max(med - lo, 1e-6),
                 0.5 + 0.5 * (v - med) / max(hi - med, 1e-6))
    t = np.clip(t, 0, 1)

    dark = BRAND * 0.34                      # the shadowed underside of the band
    light = BRAND + (255 - BRAND) * 0.78     # the specular along its crown
    new = np.clip(ramp(t, dark, BRAND, light), 0, 255)

    # Feather one pixel at the mask's edge. The boundary the band meets is an
    # anti-aliased photographic edge, so a hard binary swap there stair-steps.
    w = ndimage.gaussian_filter(m.astype(float), 0.7)[..., None]
    out = a[:, :, :3].copy()
    out[m] = new
    a[:, :, :3] = np.clip(a[:, :, :3] * (1 - w) + out * w, 0, 255)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def render(name, mark):
    img, _ = cutout.cut("cut/src/" + name)
    a = np.asarray(img).astype(np.uint8).copy()

    x0, y0, x1, y1 = LIZARD_BOX
    inbox = np.zeros(a.shape[:2], bool); inbox[y0:y1, x0:x1] = True
    recolour_type(a, blue_mask(a[:, :, :3]) & ~inbox)

    return recolour_crimp(swap_mark(a, mark))


def fetch_sources():
    """Fallback: pull any missing original photograph from the store's CDN.

    Normally a no-op, because cut/src/ is committed. Kept because the URLs are
    a second copy and cost nothing to keep working — but do not rely on them.
    They point at the live product images, which are replaceable from the
    admin, so they can stop resolving without warning.
    """
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
