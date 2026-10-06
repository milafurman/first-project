"""Recolour the flip-disc and the crimp band on a vial render, preserving all shading."""
import numpy as np, colorsys, os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

SRC = "cut/brand/tmg-ghk-cu.png"
DISC = (0.000, 0.085)      # white plastic flip-top, as fractions of vial height
CRIMP= (0.085, 0.170)      # aluminium crimp band

def hexrgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def recolour(im, band, target):
    """Map a band's average to `target` while keeping its relative light and shade."""
    if target is None: return im
    a = np.asarray(im).astype(float).copy()
    al = a[:,:,3] > 128
    rows = np.where(al.any(axis=1))[0]
    y0 = rows.min() + int((rows.max()-rows.min())*band[0])
    y1 = rows.min() + int((rows.max()-rows.min())*band[1])
    sl = a[y0:y1, :, :3]; m = al[y0:y1]
    if not m.any(): return im
    hsv = np.array([colorsys.rgb_to_hsv(*(p/255)) for p in sl[m]])
    th, ts, tv = colorsys.rgb_to_hsv(*(np.array(hexrgb(target))/255))
    scale = tv / max(hsv[:,2].mean(), 1e-6)
    out = np.array([colorsys.hsv_to_rgb(th, ts, min(v*scale, 1.0)) for v in hsv[:,2]])
    sl[m] = out*255
    a[y0:y1, :, :3] = sl
    return Image.fromarray(a.clip(0,255).astype(np.uint8), "RGBA")

def vial(crimp, cap):
    im = Image.open(SRC).convert("RGBA")
    im = recolour(im, CRIMP, crimp)
    im = recolour(im, DISC,  cap)
    return im

BLUE, INK, PAPER = "#2866CD", "#141418", "#F2F2F0"
OPTIONS = [
    ("now — silver + white",      None,   None),
    ("blue crimp + white cap",    BLUE,   PAPER),
    ("silver crimp + blue cap",   None,   BLUE),
    ("blue crimp + blue cap",     BLUE,   BLUE),
    ("black crimp + white cap",   INK,    PAPER),
    ("blue crimp + black cap",    BLUE,   INK),
]
os.makedirs("caps", exist_ok=True)
for i,(name,c,k) in enumerate(OPTIONS):
    vial(c,k).save(f"caps/opt{i}.png")
    print(f"  {name}")

# family coding: one constant blue crimp, cap colour carries the group
FAMILY = [("Metabolic","#2866CD"),("Repair","#F2F2F0"),("Longevity","#141418"),
          ("Cognitive","#5A9E86"),("Supplies","#9AA0A6")]
for i,(n,c) in enumerate(FAMILY):
    vial(BLUE, c).save(f"caps/fam{i}.png")
print("family set:", len(FAMILY))
