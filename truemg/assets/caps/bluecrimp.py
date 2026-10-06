"""Blue crimp, white cap, across the whole line — Mila's pick.

The cap is left exactly as photographed rather than recoloured to a nominal white:
it is already white, and a recolour would only cost it a little of its shading.
"""
import numpy as np, colorsys, os, glob
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
CRIMP = (0.085, 0.170)
BLUE  = "#2866CD"
hexrgb = lambda h: tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def recolour(im, band, target):
    a = np.asarray(im).astype(float).copy()
    al = a[:, :, 3] > 128
    rows = np.where(al.any(axis=1))[0]
    y0 = rows.min() + int((rows.max() - rows.min()) * band[0])
    y1 = rows.min() + int((rows.max() - rows.min()) * band[1])
    sl = a[y0:y1, :, :3]; m = al[y0:y1]
    if not m.any(): raise SystemExit("empty crimp band")
    hsv = np.array([colorsys.rgb_to_hsv(*(p / 255)) for p in sl[m]])
    th, ts, tv = colorsys.rgb_to_hsv(*(np.array(hexrgb(target)) / 255))
    scale = tv / max(hsv[:, 2].mean(), 1e-6)
    sl[m] = np.array([colorsys.hsv_to_rgb(th, ts, min(v * scale, 1.0))
                      for v in hsv[:, 2]]) * 255
    a[y0:y1, :, :3] = sl
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")

os.makedirs("blue", exist_ok=True)
files = sorted(glob.glob("cut/brand/tmg-*.png"))
for f in files:
    recolour(Image.open(f).convert("RGBA"), CRIMP, BLUE).save("blue/" + os.path.basename(f))
print("recoloured", len(files))

# ---- contact sheet, checkerboard behind the alpha so a white halo would show ----
F = lambda n, s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + n, s)
MONO, BOLD = F("DejaVuSansMono.ttf", 13), F("DejaVuSans-Bold.ttf", 21)
INK, MUT = (10, 10, 11), (138, 133, 125)
COLS, CW, CH = 6, 172, 236
rows = (len(files) + COLS - 1) // COLS
W, H = 40 + COLS * CW + 20, 108 + rows * CH + 24
c = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(c)
d.text((36, 28), "BLUE CRIMP, WHITE CAP — the whole line", font=BOLD, fill=(237, 235, 230))
d.text((36, 60), "%d vials · crimp #2866CD · cap as photographed · transparent PNG"
       % len(files), font=MONO, fill=MUT)
tile = Image.new("RGB", (16, 16), (30, 30, 32))
ImageDraw.Draw(tile).rectangle([8, 0, 15, 7], fill=(38, 38, 41))
ImageDraw.Draw(tile).rectangle([0, 8, 7, 15], fill=(38, 38, 41))
for i, p in enumerate(files):
    x, y = 36 + (i % COLS) * CW, 104 + (i // COLS) * CH
    cell = Image.new("RGB", (CW - 14, CH - 44))
    for ty in range(0, cell.height, 16):
        for tx in range(0, cell.width, 16): cell.paste(tile, (tx, ty))
    v = Image.open("blue/" + os.path.basename(p)).convert("RGBA")
    k = min((cell.width - 16) / v.width, (cell.height - 16) / v.height)
    v = v.resize((int(v.width * k), int(v.height * k)), Image.LANCZOS)
    cell.paste(v, ((cell.width - v.width) // 2, (cell.height - v.height) // 2), v)
    c.paste(cell, (x, y))
    d.text((x, y + cell.height + 8), os.path.basename(p)[4:-4][:21], font=MONO,
           fill=(222, 220, 214))
c.save("shots/blue-line.jpg", quality=93)
print("shots/blue-line.jpg", c.size)
