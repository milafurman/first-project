"""Cut the blue foil seal out of the rendered vials as a standalone asset.

The seal is pixel-identical across all seventeen products — the photographs are
the same vial shot once, with the label swapped — so this is one asset, not
seventeen copies of one asset.

Two cuts, because "foil" means both things depending on who is asking:
  foil-seal   the whole flip-off seal, white button and blue skirt together,
              which is what the vial actually wears
  foil-band   the blue aluminium skirt alone, which is the part a crimp
              supplier colour-matches against
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

SRC = "tmg-nad.png"
CRIMP = (0.085, 0.170)      # the band, as a fraction of the subject's height
SEAL_BOTTOM = 0.178         # just below the skirt, where the glass shoulder starts
BRAND = "#2365CD"


def subject_box(a):
    al = a[:, :, 3] > 128
    rows = np.where(al.any(axis=1))[0]
    cols = np.where(al.any(axis=0))[0]
    return rows.min(), rows.max(), cols.min(), cols.max()


def cut(a, y_from, y_to):
    """Crop a band of the subject, then trim to its own alpha."""
    r0, r1, c0, c1 = subject_box(a)
    h = r1 - r0
    top = a[r0 + int(h * y_from): r0 + int(h * y_to), c0:c1 + 1]
    im = Image.fromarray(top, "RGBA")
    al = np.asarray(im)[:, :, 3] > 8
    if al.any():
        ys, xs = np.where(al)
        im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return im


def spec(seal, band):
    """A card the printer or crimp supplier can work from."""
    F = lambda n, s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + n, s)
    MONO, BOLD, SMALL = F("DejaVuSansMono.ttf", 15), F("DejaVuSans-Bold.ttf", 26), F("DejaVuSansMono.ttf", 12)
    W, H = 900, 560
    c = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(c)
    d.text((40, 32), "TrueMG Labs — blue foil seal", font=BOLD, fill=(10, 10, 11))
    d.text((40, 70), "flip-off seal, anodised blue aluminium skirt", font=MONO, fill=(120, 118, 112))

    for im, x, label in ((seal, 60, "full seal"), (band, 330, "blue band only")):
        k = min(220 / im.width, 190 / im.height)
        v = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        bg = Image.new("RGB", (240, 200), (250, 250, 251))
        bg.paste(v, ((240 - v.width) // 2, (200 - v.height) // 2), v)
        c.paste(bg, (x, 120))
        d.text((x, 330), label, font=MONO, fill=(40, 40, 44))

    d.rectangle([620, 120, 840, 200], fill=tuple(int(BRAND[i:i + 2], 16) for i in (1, 3, 5)))
    d.text((620, 212), BRAND, font=BOLD, fill=(10, 10, 11))
    d.text((620, 246), "the brand blue", font=SMALL, fill=(120, 118, 112))

    lines = [
        "Sampled from the TRUEMG Labels artwork in Canva: it is the",
        "literal fill on the product-name text, so the foil and the",
        "label printing are the same colour by construction.",
        "",
        "The skirt is rendered as anodised metal, not flat colour — it",
        "keeps the shading of the aluminium underneath, ramping from a",
        "deep shadow through #2365CD to a near-white specular crown.",
        "Quoted to a supplier, match on #2365CD as the body colour.",
        "",
        "Identical on all 17 products.",
    ]
    for i, ln in enumerate(lines):
        d.text((60, 380 + i * 19), ln, font=SMALL, fill=(60, 60, 66))
    return c


if __name__ == "__main__":
    os.makedirs("foil", exist_ok=True)
    a = np.asarray(Image.open(SRC).convert("RGBA"))

    seal = cut(a, 0.0, SEAL_BOTTOM)
    band = cut(a, CRIMP[0], CRIMP[1])
    seal.save("foil/foil-seal.png")
    band.save("foil/foil-band.png")
    spec(seal, band).save("foil/foil-spec.jpg", quality=94)

    print("foil/foil-seal.png ", seal.size)
    print("foil/foil-band.png ", band.size)
    print("foil/foil-spec.jpg")
