"""Every aluminium crimp colour on the same vial, plus the gold-and-blue combinations.

Hue and saturation are replaced and value is scaled rather than set, so the knurl,
the highlight and the shadow on the photographed crimp all survive the recolour.
A flat fill would have produced a sticker.
"""
import numpy as np, colorsys, os
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC   = "cut/brand/tmg-ghk-cu.png"
DISC  = (0.000, 0.085)      # white plastic flip-top, as fractions of vial height
CRIMP = (0.085, 0.170)      # aluminium crimp band
RING  = (0.085, 0.118)      # the top third of the crimp, where a second colour reads as a ring

hexrgb = lambda h: tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def recolour(im, band, target):
    """Map a band's average to `target` while keeping its relative light and shade."""
    if target is None: return im
    a = np.asarray(im).astype(float).copy()
    al = a[:, :, 3] > 128
    rows = np.where(al.any(axis=1))[0]
    y0 = rows.min() + int((rows.max() - rows.min()) * band[0])
    y1 = rows.min() + int((rows.max() - rows.min()) * band[1])
    sl = a[y0:y1, :, :3]; m = al[y0:y1]
    if not m.any(): return im
    hsv = np.array([colorsys.rgb_to_hsv(*(p / 255)) for p in sl[m]])
    th, ts, tv = colorsys.rgb_to_hsv(*(np.array(hexrgb(target)) / 255))
    scale = tv / max(hsv[:, 2].mean(), 1e-6)
    sl[m] = np.array([colorsys.hsv_to_rgb(th, ts, min(v * scale, 1.0))
                      for v in hsv[:, 2]]) * 255
    a[y0:y1, :, :3] = sl
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")

def vial(crimp=None, cap=None, ring=None):
    im = Image.open(SRC).convert("RGBA")
    im = recolour(im, CRIMP, crimp)
    im = recolour(im, RING,  ring)     # applied after, so it sits over the crimp
    im = recolour(im, DISC,  cap)
    return im

BLUE, GOLD, GOLD_D = "#2365CD", "#D8B46A", "#9C7C34"
INK, PAPER, GUN, COPPER = "#141418", "#F2F2F0", "#5A6068", "#B87333"

# one photograph per aluminium colour; the white cap is held constant so the
# crimp is the only thing changing from frame to frame
CRIMPS = [
    ("silver",        None,   "what you have now"),
    ("brand blue",    BLUE,   "#2365CD · our blue"),
    ("gold",          GOLD,   "#D8B46A · bright"),
    ("deep gold",     GOLD_D, "#9C7C34 · antique"),
    ("gold + blue",   BLUE,   "blue band, gold ring"),
    ("black",         INK,    "#141418"),
    ("gunmetal",      GUN,    "#5A6068"),
    ("copper",        COPPER, "#B87333"),
    ("pearl white",   PAPER,  "#F2F2F0"),
]
# the three honest readings of "gold and blue combined"
COMBOS = [
    ("gold crimp, blue cap",      dict(crimp=GOLD, cap=BLUE)),
    ("blue crimp, gold cap",      dict(crimp=BLUE, cap=GOLD)),
    ("blue crimp, gold ring",     dict(crimp=BLUE, cap=PAPER, ring=GOLD)),
]

os.makedirs("crimps", exist_ok=True)
imgs = []
for i, (name, c, _n) in enumerate(CRIMPS):
    kw = dict(crimp=c, cap=PAPER)
    if name == "gold + blue": kw["ring"] = GOLD
    im = vial(**kw); im.save(f"crimps/c{i}.png"); imgs.append(im)
combos = []
for i, (name, kw) in enumerate(COMBOS):
    im = vial(**kw); im.save(f"crimps/x{i}.png"); combos.append(im)
print("crimps:", len(imgs), " combos:", len(combos))

# ---------------- contact sheet ----------------
F = lambda n, s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + n, s)
MONO, MONO_S, BOLD, H2 = F("DejaVuSansMono.ttf", 14), F("DejaVuSansMono.ttf", 12), \
                         F("DejaVuSans-Bold.ttf", 23), F("DejaVuSans-Bold.ttf", 19)
PAGE, TXT, MUT, ACC = (247, 246, 243), (18, 18, 20), (128, 124, 116), (35,101,205)

def tile(im, box_w, box_h):
    """Crop to the artwork, fit inside the box, return an RGB tile on the page colour."""
    a = np.asarray(im); ys, xs = np.where(a[:, :, 3] > 8)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    k = min(box_w / im.width, box_h / im.height)
    im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    cell = Image.new("RGB", (box_w, box_h), PAGE)
    cell.paste(im, ((box_w - im.width) // 2, box_h - im.height), im)
    return cell

CW, CH = 168, 300
W = 40 + len(CRIMPS) * CW + 40
H = 880
c = Image.new("RGB", (W, H), PAGE); d = ImageDraw.Draw(c)
d.text((40, 30), "THE ALUMINIUM — one colour per frame", font=BOLD, fill=TXT)
d.text((40, 64), "same vial, same label, same white cap. only the crimp changes.",
       font=MONO_S, fill=MUT)

for i, ((name, _c, note), im) in enumerate(zip(CRIMPS, imgs)):
    x = 40 + i * CW
    c.paste(tile(im, CW - 12, CH), (x, 96))
    d.text((x, 96 + CH + 14), name, font=MONO,
           fill=ACC if name in ("brand blue", "gold + blue") else TXT)
    d.text((x, 96 + CH + 34), note, font=MONO_S, fill=MUT)

y = 96 + CH + 74
d.line([(40, y), (W - 40, y)], fill=(222, 219, 212), width=1)
d.text((40, y + 26), "GOLD AND BLUE TOGETHER — three ways", font=H2, fill=TXT)
d.text((40, y + 54), "the crimp and the cap are separate parts, so the two colours "
       "can sit on either one", font=MONO_S, fill=MUT)
CW2, CH2 = 250, 250
for i, ((name, _kw), im) in enumerate(zip(COMBOS, combos)):
    x = 40 + i * (CW2 + 24)
    c.paste(tile(im, CW2, CH2), (x, y + 84))
    d.text((x, y + 84 + CH2 + 16), name, font=MONO, fill=TXT)

c.save("shots/crimps.jpg", quality=93)
print("shots/crimps.jpg", c.size)
