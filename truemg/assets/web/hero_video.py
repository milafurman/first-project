"""Render the hero loop: the vial cluster breathing over the brand field.

Every motion is a sine over the clip's full length, so the last frame lands
exactly where the first one started and the loop has no visible seam. The
shadows travel at a fraction of their vial's drift, which is what sells the
vials as floating rather than as a sticker sliding around.
"""
import os, math, shutil, subprocess, tempfile
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC = "../vials"          # relative to D: an absolute path here pointed at one checkout

# The frames are scratch — 192 PNGs, about 60 MB — so they go to a temp directory
# that is wiped afterwards. Set HERO_FRAMES to a path to keep them for inspection;
# either way the directory is emptied first, because a short run leaving a long
# run's leftovers behind would hand stale frames to the encoder.
OUT = os.environ.get("HERO_FRAMES") or tempfile.mkdtemp(prefix="hero-frames-")
KEEP = bool(os.environ.get("HERO_FRAMES"))
shutil.rmtree(OUT, ignore_errors=True)
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
    # nearly nothing, so the glass is pre-lifted in contrast and saturation to survive
    # it. The printed blue and the crimp are held OUT of that lift. They are #2365CD by
    # construction, and 1.35x saturation on a colour already that saturated just clips
    # it — the video was shipping a #0050F8 neon crimp for exactly this reason, which
    # is the drift Mila caught in the stills reappearing one step further down the line.
    # A wash lightens; it does not shift hue, so the brand blue needs no help from here.
    base = v.convert("RGB")
    lift = ImageEnhance.Color(ImageEnhance.Contrast(base).enhance(1.22)).enhance(1.35)
    px = np.asarray(base).astype(int)
    r_, g_, b_ = px[:, :, 0], px[:, :, 1], px[:, :, 2]
    brand = (b_ - r_ > 45) & (b_ - g_ > 25) & (b_ > 90)        # same test as vials/render.py
    hold = Image.fromarray((ndimage.gaussian_filter(brand.astype(float), 1.2) * 255)
                           .clip(0, 255).astype(np.uint8))     # feathered: no hard seam
    rgb = Image.composite(base, lift, hold)
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

# ---- encode ----
# This used to be an ffmpeg command somebody typed by hand, which is exactly how
# hero-loop.mp4, hero-loop.webm and hero-poster.jpg ended up carrying the old neon
# crimp long after the vials they are made of had been fixed: the frames were
# regenerated, the videos were not. Encoding here means there is no step left to
# forget.
#
# Two codecs because neither one covers the field on its own: Safari needs H.264,
# and some Chromium builds ship without it and need VP9.
def run(*cmd):
    print(" ", " ".join(cmd[:6]), "...", flush=True)
    subprocess.run(cmd, check=True, capture_output=True)

SEQ = f"{OUT}/f%04d.png"
run("ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", SEQ,
    "-c:v", "libx264", "-preset", "slow", "-crf", "30",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", "hero-loop.mp4")
run("ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", SEQ,
    "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-row-mt", "1",
    "-pix_fmt", "yuv420p", "-an", "hero-loop.webm")

# Frame 0 is the first frame the video paints, so using it as the poster means the
# swap from still to video is invisible rather than a jump.
Image.open(f"{OUT}/f0000.png").convert("RGB").save("hero-poster.jpg", quality=86, optimize=True)

for f in ("hero-loop.mp4", "hero-loop.webm", "hero-poster.jpg"):
    print(f"  {f:18s} {os.path.getsize(f)//1024} KB")

if not KEEP:
    shutil.rmtree(OUT, ignore_errors=True)
else:
    print("  frames kept in", OUT)
