"""Render the hero loop: the vial cluster breathing over the brand field.

Every motion is a sine over the clip's full length, so the last frame lands
exactly where the first one started and the loop has no visible seam. The
shadows travel at a fraction of their vial's drift, which is what sells the
vials as floating rather than as a sticker sliding around.
"""
import os, math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC = "/home/user/first-project/truemg/assets/vials"
OUT = "/tmp/claude-0/-home-user-first-project/a0f52b12-8e20-5aa6-91f8-6e19eeb1c139/scratchpad/frames"
os.makedirs(OUT, exist_ok=True)

# 2.6:1 matches the hero box, so `cover` barely crops. The cluster sits only
# slightly right of centre so a portrait crop on a phone still catches it, and
# the vials are small in frame because the hero scales the video up to fit.
W, H, FPS, SECONDS = 1920, 740, 24, 8
N = FPS * SECONDS

def vial(name):
    im = Image.open(f"{SRC}/tmg-{name}.png").convert("RGBA")
    a = np.asarray(im); ys, xs = np.where(a[:, :, 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

# ---- the field, rendered once ----
# A flat vertical gradient, white to #EFF4FC, which is the hero's own background.
# A bloom here looked like a seam on the page: the video covers the section, so any
# shape in its field reads as an edge against the theme's gradient around it.
field = Image.new("RGB", (W, H))
d = ImageDraw.Draw(field)
for y in range(H):
    t = y / (H - 1)
    d.line([(0, y), (W, y)], fill=(255 - int(16 * t), 255 - int(11 * t), 255 - int(3 * t)))

# ---- the cluster, prepared once: name, centre, height, tilt, drift, phase ----
CAST = [
    ("tmg-3rt",        .690, .50, 320, -13, 11, 0.00),
    ("ghk-cu",         .795, .45, 386,   6, 16, 0.38),
    ("nad",            .897, .52, 300,  17, 13, 0.72),
    ("bpc-157-tb-500", .745, .635, 220, -4,  9, 0.18),
]
PREP = []
for name, fx, fy, h, ang, amp, phase in CAST:
    v = vial(name)
    k = h / v.height
    v = v.resize((max(1, int(v.width * k)), h), Image.LANCZOS)
    # The theme lays a white wash over the hero video, which drains clear glass to
    # nearly nothing. Pre-lifting contrast and saturation is what survives it.
    rgb = ImageEnhance.Contrast(v.convert("RGB")).enhance(1.22)
    rgb = ImageEnhance.Color(rgb).enhance(1.35)
    v = Image.merge("RGBA", (*rgb.split(), v.getchannel("A")))
    v = v.rotate(ang, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", v.size, (12, 24, 56, 0))
    sh.putalpha(v.getchannel("A").point(lambda p: int(p * 0.30)))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    PREP.append((v, sh, int(W * fx), int(H * fy), amp, phase))

# ---- the light sweep, one soft band that crosses exactly once per loop ----
band = Image.new("L", (W, H), 0)
ImageDraw.Draw(band).polygon([(0, 0), (int(W * .17), 0), (int(W * .30), H), (int(W * .13), H)], fill=72)
band = band.filter(ImageFilter.GaussianBlur(90))
sweep = Image.new("RGB", (W, H), (255, 255, 255))
BAND = np.asarray(band)
SPAN = int(W * 1.6)

for f in range(N):
    t = f / N
    frame = field.copy()
    for v, sh, cx, cy, amp, phase in PREP:
        dy = amp * math.sin(2 * math.pi * (t + phase))
        dx = 5 * math.sin(2 * math.pi * (2 * t + phase))
        x = cx - v.width // 2 + int(round(dx))
        y = cy - v.height // 2 + int(round(dy))
        frame.paste(sh, (x, y + 18 - int(round(dy * 0.6))), sh)   # shadow lags the lift
        frame.paste(v, (x, y), v)
    # Two copies of the band, one a full period behind, combined with a MAX so the
    # wrap blends. Pasting the second one would overwrite the first with its own
    # zeros and tear the loop open at the seam.
    off = int((t * SPAN) - W * .3)
    m = np.zeros((H, W), np.uint8)
    for o in (off, off - SPAN):
        a, b_ = max(0, o), min(W, o + W)
        if b_ > a:
            np.maximum(m[:, a:b_], BAND[:, a - o:b_ - o], out=m[:, a:b_])
    frame = Image.composite(sweep, frame, Image.fromarray((m * 0.42).astype(np.uint8)))
    frame.save(f"{OUT}/f{f:04d}.png")
    if f % 48 == 0: print("frame", f, "/", N, flush=True)
print("done", N, "frames at", W, "x", H)
