"""Render the hero loops: the vial cluster breathing over the brand field.

Every motion is a sine over the clip's full length, so the last frame lands
exactly where the first one started and the loop has no visible seam. The
shadows travel at a fraction of their vial's drift, which is what sells the
vials as floating rather than as a sticker sliding around.

Two cuts come out of the same mechanics:

  hero-loop       1920x740, 2.6:1. Sits INSIDE the hero as a strip, which is
                  what the custom-CSS route needed.
  hero-bg-loop    1920x1080, 16:9. Goes in the Design studio's "Hero
                  background" slot, which is full-bleed behind the headline.
                  A 2.6:1 file in that slot crops hard on a tall screen, so
                  this cut is framed for 16:9 and keeps the left half clear
                  for the headline that lands on top of it.

Run from this directory. Needs ffmpeg and the rendered vials in ../vials.
"""
import math
import os
import shutil
import subprocess
import tempfile

import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC = "../vials"          # relative to D: an absolute path here pointed at one checkout

# The frames are scratch — a few hundred PNGs — so they go to a temp directory
# that is wiped afterwards. Set HERO_FRAMES to a path to keep them for
# inspection; either way the directory is emptied before each cut, because one
# cut leaving another's leftovers behind would hand stale frames to the encoder.
FRAMES = os.environ.get("HERO_FRAMES") or tempfile.mkdtemp(prefix="hero-frames-")
KEEP = bool(os.environ.get("HERO_FRAMES"))

FPS, SECONDS = 24, 8

# name, centre x and y as fractions of the frame, height as a fraction of the
# frame height, tilt in degrees, drift in px, and a phase so they do not all
# rise together.
STRIP_CAST = [
    ("tmg-3rt",        .690, .500, .432, -13, 11, 0.00),
    ("ghk-cu",         .795, .450, .522,   6, 16, 0.38),
    ("nad",            .897, .520, .405,  17, 13, 0.72),
    ("bpc-157-tb-500", .745, .635, .297,  -4,  9, 0.18),
]

# Framed for a full-bleed background: the cluster sits right of centre and a
# little smaller in frame, so the headline has the left half to itself and a
# narrow crop on a phone still catches the glass.
BG_CAST = [
    ("tmg-3rt",        .640, .520, .360, -13, 11, 0.00),
    ("ghk-cu",         .762, .460, .440,   6, 16, 0.38),
    ("nad",            .878, .540, .335,  17, 13, 0.72),
    ("bpc-157-tb-500", .700, .700, .250,  -4,  9, 0.18),
]


def vial(name):
    im = Image.open(f"{SRC}/tmg-{name}.png").convert("RGBA")
    a = np.asarray(im); ys, xs = np.where(a[:, :, 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def field(W, H):
    """A flat vertical gradient, white to #EFF4FC, the hero's own background.

    A bloom here looked like a seam on the page: the video covers the section,
    so any shape in its field reads as an edge against the theme's gradient
    around it."""
    f = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(f)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=(255 - int(16 * t), 255 - int(11 * t), 255 - int(3 * t)))
    return f


def shadow(v, blur, opacity=0.30):
    """A soft shadow, on a canvas big enough for it to fade out on.

    `vial()` crops the sprite tight to its own alpha, so the glass touches all
    four edges. Blurring the shadow inside that same rectangle clips the
    Gaussian's falloff square: the corners land at ~30/255 instead of 0, and
    every vial sits on a hard-edged navy box. That box shipped in the hero
    video and in every still compose.py made. Padding by three blur radii
    gives the blur somewhere to go, so the shadow reaches zero before the
    canvas ends. The pad is returned because the caller has to paste that
    much further up and left.
    """
    pad = blur * 3
    mask = Image.new("L", (v.width + pad * 2, v.height + pad * 2), 0)
    mask.paste(v.getchannel("A").point(lambda q: int(q * opacity)), (pad, pad))
    sh = Image.new("RGBA", mask.size, (12, 24, 56, 0))
    sh.putalpha(mask)
    return sh.filter(ImageFilter.GaussianBlur(blur)), pad


def prep(cast, W, H):
    """Scale, lift, tilt and shadow each vial once, before the frame loop."""
    out = []
    for name, fx, fy, fh, ang, amp, phase in cast:
        v = vial(name)
        h = max(1, int(H * fh))
        v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)

        # The theme lays a white wash over the hero, which drains clear glass to
        # nearly nothing, so the glass is pre-lifted in contrast and saturation
        # to survive it. The printed blue and the crimp are held OUT of that
        # lift. They are #2365CD by construction, and 1.35x saturation on a
        # colour already that saturated just clips it — the video was shipping a
        # #0050F8 neon crimp for exactly this reason. A wash lightens; it does
        # not shift hue, so the brand blue needs no help from here.
        base = v.convert("RGB")
        lift = ImageEnhance.Color(ImageEnhance.Contrast(base).enhance(1.22)).enhance(1.35)
        px = np.asarray(base).astype(int)
        r_, g_, b_ = px[:, :, 0], px[:, :, 1], px[:, :, 2]
        brand = (b_ - r_ > 45) & (b_ - g_ > 25) & (b_ > 90)   # as in vials/render.py
        hold = Image.fromarray((ndimage.gaussian_filter(brand.astype(float), 1.2) * 255)
                               .clip(0, 255).astype(np.uint8))
        v = Image.merge("RGBA", (*Image.composite(base, lift, hold).split(),
                                 v.getchannel("A")))

        v = v.rotate(ang, resample=Image.BICUBIC, expand=True)
        sh, pad = shadow(v, max(8, int(H * 0.022)))
        out.append((v, sh, pad, int(W * fx), int(H * fy), amp, phase))
    return out


def sweep_band(W, H):
    """One soft light band that crosses the frame exactly once per loop."""
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).polygon(
        [(0, 0), (int(W * .17), 0), (int(W * .30), H), (int(W * .13), H)], fill=72)
    return np.asarray(band.filter(ImageFilter.GaussianBlur(int(W * 0.047))))


def render(W, H, cast, name):
    print(f"{name}  {W}x{H}")
    shutil.rmtree(FRAMES, ignore_errors=True)
    os.makedirs(FRAMES, exist_ok=True)

    N = FPS * SECONDS
    bg, parts, BAND = field(W, H), prep(cast, W, H), sweep_band(W, H)
    white, SPAN = Image.new("RGB", (W, H), (255, 255, 255)), int(W * 1.6)

    for f in range(N):
        t = f / N
        frame = bg.copy()
        for v, sh, pad, cx, cy, amp, phase in parts:
            dy = amp * math.sin(2 * math.pi * (t + phase))
            dx = 5 * math.sin(2 * math.pi * (2 * t + phase))
            x = cx - v.width // 2 + int(round(dx))
            y = cy - v.height // 2 + int(round(dy))
            # shadow lags the lift; -pad because the shadow canvas is oversized
            frame.paste(sh, (x - pad, y + 18 - int(round(dy * 0.6)) - pad), sh)
            frame.paste(v, (x, y), v)
        # Two copies of the band, one a full period behind, combined with a MAX
        # so the wrap blends. Pasting the second would overwrite the first with
        # its own zeros and tear the loop open at the seam.
        off = int((t * SPAN) - W * .3)
        m = np.zeros((H, W), np.uint8)
        for o in (off, off - SPAN):
            a, b_ = max(0, o), min(W, o + W)
            if b_ > a:
                np.maximum(m[:, a:b_], BAND[:, a - o:b_ - o], out=m[:, a:b_])
        frame = Image.composite(white, frame, Image.fromarray((m * 0.42).astype(np.uint8)))
        frame.save(f"{FRAMES}/f{f:04d}.png")
        if f % 48 == 0:
            print(f"    frame {f}/{N}", flush=True)
    encode(name)


def encode(name):
    """Frames to MP4, WebM and a poster.

    This used to be an ffmpeg command somebody typed by hand, which is how
    hero-loop.mp4, hero-loop.webm and hero-poster.jpg ended up carrying the old
    neon crimp long after the vials they are made of had been fixed: the frames
    were regenerated, the videos were not. Encoding here means there is no step
    left to forget.

    Two codecs because neither covers the field alone: Safari needs H.264, and
    some Chromium builds ship without it and need VP9.
    """
    seq = f"{FRAMES}/f%04d.png"
    common = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", seq]
    subprocess.run(common + ["-c:v", "libx264", "-preset", "slow", "-crf", "30",
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                             "-an", f"{name}.mp4"], check=True, capture_output=True)
    subprocess.run(common + ["-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0",
                             "-row-mt", "1", "-pix_fmt", "yuv420p",
                             "-an", f"{name}.webm"], check=True, capture_output=True)
    # Frame 0 is the first frame the video paints, so using it as the poster
    # makes the swap from still to video invisible rather than a jump.
    Image.open(f"{FRAMES}/f0000.png").convert("RGB").save(
        f"{name}-poster.jpg", quality=86, optimize=True)
    for f in (f"{name}.mp4", f"{name}.webm", f"{name}-poster.jpg"):
        print(f"    {f:26s} {os.path.getsize(f) // 1024} KB")


if __name__ == "__main__":
    render(1920, 740, STRIP_CAST, "hero-loop")
    render(1920, 1080, BG_CAST, "hero-bg-loop")
    if KEEP:
        print("  frames kept in", FRAMES)
    else:
        shutil.rmtree(FRAMES, ignore_errors=True)
