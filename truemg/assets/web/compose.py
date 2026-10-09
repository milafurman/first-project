"""Compose the hero and category art from the transparent vials.

The cut-outs have a real alpha channel, so a drop shadow here casts the shape of
the glass rather than of a bounding box — the opposite of the product cards,
where the uploaded files are still white-backed and a shadow would draw the box.
"""
import os, math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC = "../vials"   # relative to D, above: an absolute path here wrote into whichever
OUT = "."          # checkout it was typed in, no matter where the script was run from
os.makedirs(OUT, exist_ok=True)

def vial(name):
    im = Image.open(f"{SRC}/tmg-{name}.png").convert("RGBA")
    a = np.asarray(im); ys, xs = np.where(a[:, :, 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def field(w, h, stops):
    """Vertical-ish brand gradient with two soft radial blooms."""
    g = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(g)
    (c0, c1) = stops
    for y in range(h):                       # linear base
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3)))
    bloom = Image.new("L", (w, h), 0)
    bd = ImageDraw.Draw(bloom)
    bd.ellipse([int(w * .42), int(-h * .30), int(w * 1.25), int(h * .95)], fill=150)
    bd.ellipse([int(w * .05), int(h * .55), int(w * .62), int(h * 1.45)], fill=85)
    bloom = bloom.filter(ImageFilter.GaussianBlur(w * 0.11))
    return Image.composite(Image.new("RGB", (w, h), (214, 229, 252)), g, bloom)

def place(canvas, v, cx, cy, height, angle, shadow=(26, 34, 0.30)):
    """Scale to `height`, rotate, cast a shadow from the alpha, composite."""
    k = height / v.height
    v = v.resize((max(1, int(v.width * k)), height), Image.LANCZOS)
    v = v.rotate(angle, resample=Image.BICUBIC, expand=True)
    blur, dy, op = shadow

    # The shadow is built on a canvas padded by three blur radii, NOT on one the
    # size of the vial. `vial()` crops the sprite tight to its own alpha, so the
    # glass touches all four edges; blurring inside that rectangle clips the
    # Gaussian's falloff square, leaving the corners at roughly 30/255 instead
    # of 0. The result is a hard-edged navy box behind every vial, which is what
    # these images shipped with. The pad gives the blur somewhere to fade out.
    pad = blur * 3
    mask = Image.new("L", (v.width + pad * 2, v.height + pad * 2), 0)
    mask.paste(v.getchannel("A").point(lambda p: int(p * op)), (pad, pad))
    sh = Image.new("RGBA", mask.size, (12, 24, 56, 0))
    sh.putalpha(mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))

    x, y = cx - v.width // 2, cy - v.height // 2
    canvas.alpha_composite(sh, (x - pad, y + dy - pad))
    canvas.alpha_composite(v, (x, y))

# ---------------- hero, desktop ----------------
W, H = 2560, 1150
c = field(W, H, ((255, 255, 255), (233, 240, 252))).convert("RGBA")
# cluster sits right of centre; the theme puts the headline in the left column
place(c, vial("tmg-3rt"),           int(W*.585), int(H*.50),  660, -13)
place(c, vial("ghk-cu"),            int(W*.730), int(H*.46),  790,   6)
place(c, vial("nad"),               int(W*.872), int(H*.52),  615,  17)
place(c, vial("bpc-157-tb-500"),    int(W*.663), int(H*.635), 450,  -4, (18,20,.22))
c.convert("RGB").save(f"{OUT}/hero-desktop.jpg", quality=86, optimize=True)
print("hero-desktop.jpg", os.path.getsize(f"{OUT}/hero-desktop.jpg")//1024, "KB")

# ---------------- hero, phone ----------------
W2, H2 = 1080, 1400
c2 = field(W2, H2, ((255, 255, 255), (231, 238, 251))).convert("RGBA")
place(c2, vial("ghk-cu"),  int(W2*.50), int(H2*.62), 640,   4)
place(c2, vial("tmg-3rt"), int(W2*.25), int(H2*.68), 510, -14)
place(c2, vial("nad"),     int(W2*.77), int(H2*.69), 495,  15)
c2.convert("RGB").save(f"{OUT}/hero-mobile.jpg", quality=86, optimize=True)
print("hero-mobile.jpg", os.path.getsize(f"{OUT}/hero-mobile.jpg")//1024, "KB")

# ---------------- the split section ----------------
W3, H3 = 1600, 1400
c3 = field(W3, H3, ((255, 255, 255), (228, 237, 252))).convert("RGBA")
place(c3, vial("ipamorelin"), int(W3*.50), int(H3*.50), 1000, -6)
c3.convert("RGB").save(f"{OUT}/documented.jpg", quality=88, optimize=True)
print("documented.jpg", os.path.getsize(f"{OUT}/documented.jpg")//1024, "KB")

# ---------------- three category tiles ----------------
TILES = [("all",    ["tmg-2tz","tmg-3rt","ghk-cu"], (243,247,254), (219,232,252)),
         ("tested", ["nad","mots-c","ss-31"],       (245,246,250), (226,231,246)),
         ("new",    ["semax","selank","epithalon"], (246,248,253), (222,235,253))]
for name, names, a, bcol in TILES:
    W4, H4 = 1200, 900
    t = field(W4, H4, (a, bcol)).convert("RGBA")
    for i, n in enumerate(names):
        place(t, vial(n), int(W4*(.28+.22*i)), int(H4*(.58 if i==1 else .62)),
              int(H4*(.74 if i==1 else .62)), (-11, 3, 13)[i], (20, 24, .26))
    t.convert("RGB").save(f"{OUT}/tile-{name}.jpg", quality=86, optimize=True)
    print(f"tile-{name}.jpg", os.path.getsize(f"{OUT}/tile-{name}.jpg")//1024, "KB")

# ---------------- revive: a plain field for the background, vials as the media ----------------
W5, H5 = 2560, 1150
field(W5, H5, ((255, 255, 255), (232, 240, 253))).save(f"{OUT}/hero-field.jpg", quality=84, optimize=True)
print("hero-field.jpg", os.path.getsize(f"{OUT}/hero-field.jpg")//1024, "KB")

W6, H6 = 1700, 1450
m = Image.new("RGBA", (W6, H6), (0, 0, 0, 0))
place(m, vial("tmg-3rt"),        int(W6*.26), int(H6*.50),  820, -13)
place(m, vial("ghk-cu"),         int(W6*.52), int(H6*.45),  980,   6)
place(m, vial("nad"),            int(W6*.78), int(H6*.52),  770,  17)
place(m, vial("bpc-157-tb-500"), int(W6*.40), int(H6*.67),  560,  -4, (18, 20, .22))
m.save(f"{OUT}/hero-media.png", optimize=True)
print("hero-media.png", os.path.getsize(f"{OUT}/hero-media.png")//1024, "KB")

# The webp is what the storefront actually loads. It used to be converted by hand
# outside this script, so it kept the crimp colour of whatever vials existed on the
# day someone remembered to run the conversion — it was still carrying #317EFF long
# after the vials were fixed. Writing it here ties it to the same source.
m.save(f"{OUT}/hero-media.webp", quality=88, method=6)
print("hero-media.webp", os.path.getsize(f"{OUT}/hero-media.webp")//1024, "KB")

field(1080, 1500, ((255, 255, 255), (231, 238, 251))).save(f"{OUT}/hero-field-mobile.jpg", quality=84, optimize=True)
print("hero-field-mobile.jpg", os.path.getsize(f"{OUT}/hero-field-mobile.jpg")//1024, "KB")

# ---------------- coming-soon background ----------------
# The theme centres its text and lays a white wash over this image, so the
# artwork has to keep out of the middle entirely rather than rely on contrast.
W7, H7 = 2560, 1440
c7 = field(W7, H7, ((255, 255, 255), (234, 241, 253))).convert("RGBA")
place(c7, vial("ghk-cu"),         int(W7*.845), int(H7*.78),  640,   6)
place(c7, vial("tmg-3rt"),        int(W7*.735), int(H7*.845), 500, -13)
place(c7, vial("nad"),            int(W7*.945), int(H7*.86),  470,  17)
place(c7, vial("bpc-157-tb-500"), int(W7*.072), int(H7*.885), 400,  -7, (18, 20, .22))
c7.convert("RGB").save(f"{OUT}/coming-soon.jpg", quality=86, optimize=True)
print("coming-soon.jpg", os.path.getsize(f"{OUT}/coming-soon.jpg")//1024, "KB")
