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
#
# Here the cast also carries depth. Everything at one distance, drifting the
# same amount, reads as a sticker sheet jiggling — which is exactly how the
# first cut of this looked. Each vial gets a blur and a drift multiplier
# instead: the far ones sit soft and barely move, the near one is slightly off
# the focal plane and travels furthest. That difference in rate IS the depth;
# the blur only sells it.
#
# name, x, y, height, tilt, drift, phase, blur px, parallax
BG_CAST = [
    ("nad",            .878, .540, .300,  17, 13, 0.72, 2.0, 0.45),   # back
    ("tmg-3rt",        .640, .520, .345, -13, 11, 0.00, 1.6, 0.70),
    ("ghk-cu",         .757, .455, .470,   6, 16, 0.38, 0.0, 1.00),   # focal plane
    ("bpc-157-tb-500", .700, .730, .285,  -4,  9, 0.18, 1.4, 1.45),   # near
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
    for row in cast:
        name, fx, fy, fh, ang, amp, phase = row[:7]
        blur, para = (row[7], row[8]) if len(row) > 7 else (0.0, 1.0)
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
        if blur:
            v = v.filter(ImageFilter.GaussianBlur(blur))
        sh, pad = shadow(v, max(8, int(H * 0.022)))
        out.append((v, sh, pad, int(W * fx), int(H * fy), amp, phase, para))
    return out


def sweep_band(W, H):
    """One soft light band that crosses the frame exactly once per loop."""
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).polygon(
        [(0, 0), (int(W * .17), 0), (int(W * .30), H), (int(W * .13), H)], fill=72)
    return np.asarray(band.filter(ImageFilter.GaussianBlur(int(W * 0.047))))


def bloom(W, H):
    """A soft pool of light that drifts behind the cluster.

    The product is photographed, with its own highlights already in it, so
    dragging a big fake one across the glass just fights the photograph — the
    first attempt at this washed the labels out. Lighting the field behind
    instead gives the frame somewhere to breathe without touching the product.
    """
    d = int(min(W, H) * 1.25)
    b = Image.new("L", (d, d), 0)
    ImageDraw.Draw(b).ellipse([0, 0, d, d], fill=255)
    return b.filter(ImageFilter.GaussianBlur(d * 0.22)), d


def glint_band(W, H):
    """A narrow, hard highlight — the thing that makes glass read as glass.

    The wide soft wash in sweep_band lights the whole frame evenly, which is
    why the first cut looked like a photograph that happened to be moving
    rather than like glass. A specular is the opposite: narrow, bright, and
    travelling. Masked to the vials' own alpha it runs along the curve of each
    bottle and across the crimp, and that single moving highlight does more
    for the material than any amount of drift.
    """
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).polygon(
        [(0, 0), (int(W * .013), 0), (int(W * .075), H), (int(W * .062), H)], fill=255)
    return np.asarray(band.filter(ImageFilter.GaussianBlur(int(W * 0.0035))))


def render(W, H, cast, name):
    print(f"{name}  {W}x{H}")
    shutil.rmtree(FRAMES, ignore_errors=True)
    os.makedirs(FRAMES, exist_ok=True)

    N = FPS * SECONDS
    bg, parts, BAND = field(W, H), prep(cast, W, H), sweep_band(W, H)
    GLINT = glint_band(W, H)
    BLOOM, BD = bloom(W, H)
    LIT = Image.new("RGB", (W, H), (255, 255, 255))
    white, SPAN = Image.new("RGB", (W, H), (255, 255, 255)), int(W * 1.6)

    for f in range(N):
        t = f / N
        # the bloom travels a slow ellipse behind everything, once per loop
        frame = bg.copy()
        bx = int(W * 0.60 + W * 0.30 * math.cos(2 * math.pi * t)) - BD // 2
        by = int(H * 0.46 + H * 0.22 * math.sin(2 * math.pi * t)) - BD // 2
        mask = Image.new("L", (W, H), 0)
        mask.paste(BLOOM, (bx, by))
        frame = Image.composite(LIT, frame, mask.point(lambda q: int(q * 0.55)))
        ink = np.zeros((H, W), np.uint8)     # where the glass is, this frame
        for v, sh, pad, cx, cy, amp, phase, para in parts:
            dy = amp * para * math.sin(2 * math.pi * (t + phase))
            dx = 5 * para * math.sin(2 * math.pi * (2 * t + phase))
            x = cx - v.width // 2 + int(round(dx))
            y = cy - v.height // 2 + int(round(dy))
            # shadow lags the lift; -pad because the shadow canvas is oversized
            frame.paste(sh, (x - pad, y + 18 - int(round(dy * 0.6)) - pad), sh)
            frame.paste(v, (x, y), v)
            a_ = np.asarray(v.getchannel("A"))
            yy0, xx0 = max(0, y), max(0, x)
            yy1, xx1 = min(H, y + v.height), min(W, x + v.width)
            if yy1 > yy0 and xx1 > xx0:
                np.maximum(ink[yy0:yy1, xx0:xx1],
                           a_[yy0 - y:yy1 - y, xx0 - x:xx1 - x],
                           out=ink[yy0:yy1, xx0:xx1])
        # Two copies of the band, one a full period behind, combined with a MAX
        # so the wrap blends. Pasting the second would overwrite the first with
        # its own zeros and tear the loop open at the seam.
        off = int((t * SPAN) - W * .3)
        m = np.zeros((H, W), np.uint8)
        for o in (off, off - SPAN):
            a, b_ = max(0, o), min(W, o + W)
            if b_ > a:
                np.maximum(m[:, a:b_], BAND[:, a - o:b_ - o], out=m[:, a:b_])
        frame = Image.composite(white, frame, Image.fromarray((m * 0.26).astype(np.uint8)))

        # the specular, clipped to the glass. It runs at a different rate from
        # the wash so the two never line up and read as one object passing.
        goff = int((t * SPAN * 1.35) - W * .45)
        g = np.zeros((H, W), np.uint8)
        for o in (goff, goff - int(SPAN * 1.35)):
            a, b_ = max(0, o), min(W, o + W)
            if b_ > a:
                np.maximum(g[:, a:b_], GLINT[:, a - o:b_ - o], out=g[:, a:b_])
        g = (g.astype(np.uint16) * ink // 255).astype(np.uint8)   # only on the vials
        frame = Image.composite(white, frame, Image.fromarray((g * 0.40).astype(np.uint8)))
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


# A third cut: the line passing, rather than four bottles breathing.
#
# The bobbing cluster reads as nothing happening, and four vials is not what
# the catalog is. This runs the range past in two bands at different speeds —
# continuous travel instead of a sine, so there is always something arriving.
# It loops because the strip is cyclic: after one period it has advanced by
# exactly its own width and is back where it started.
#
# The bands are feathered out before the left half of the frame, because the
# headline sits there and product crossing it would be worse than no motion
# at all.
MARQUEE = [
    # A row only loops if it travels a WHOLE number of its own tile widths per
    # period. 0.55 of one leaves it mid-stride at the wrap and tears the seam
    # open — measured at 8.95/255 against the 1.0 a clean loop gives. So the
    # speed column is an integer count of laps, and the parallax comes from
    # the tiles being different widths: the near row's vials are bigger and
    # more widely spaced, so one lap of its tile covers more ground in the
    # same eight seconds. Nearer travels faster, which is what parallax is.
    # height, y, blur, laps, gap, products
    (.255, .345, 2.1, 1, 1.55,
     ["semax", "ghk-cu", "epithalon", "mots-c", "selank", "ss-31", "tmg-2tz"]),
    (.400, .640, 0.3, 1, 1.70,
     ["ghk-cu", "nad", "tmg-3rt", "bpc-157-tb-500", "tesamorelin", "ipamorelin"]),
]


def strip(names, H, fh, blur, gap):
    """One cyclic row of vials, as a single wide RGBA image."""
    vs = []
    for n in names:
        v = vial(n)
        h = max(1, int(H * fh))
        v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)
        base = v.convert("RGB")
        lift = ImageEnhance.Color(ImageEnhance.Contrast(base).enhance(1.18)).enhance(1.28)
        px = np.asarray(base).astype(int)
        r_, g_, b_ = px[:, :, 0], px[:, :, 1], px[:, :, 2]
        brand = (b_ - r_ > 45) & (b_ - g_ > 25) & (b_ > 90)
        hold = Image.fromarray((ndimage.gaussian_filter(brand.astype(float), 1.2) * 255)
                               .clip(0, 255).astype(np.uint8))
        v = Image.merge("RGBA", (*Image.composite(base, lift, hold).split(),
                                 v.getchannel("A")))
        if blur:
            v = v.filter(ImageFilter.GaussianBlur(blur))
        vs.append(v)

    pitch = int(max(v.width for v in vs) * gap)
    pad = int(H * 0.05)
    tile = Image.new("RGBA", (pitch * len(vs), int(H * fh) + pad * 4), (0, 0, 0, 0))
    for i, v in enumerate(vs):
        sh, sp = shadow(v, max(6, int(H * 0.018)))
        x = i * pitch + (pitch - v.width) // 2
        tile.alpha_composite(sh, (x - sp, pad * 2 + int(H * 0.012) - sp))
        tile.alpha_composite(v, (x, pad * 2))
    return tile


def feather(W, H):
    """Alpha ramp that dissolves the bands before they reach the headline."""
    g = np.zeros((H, W), np.uint8)
    a, b = int(W * 0.40), int(W * 0.60)
    g[:, b:] = 255
    g[:, a:b] = (np.linspace(0, 255, b - a)[None, :]).astype(np.uint8)
    return Image.fromarray(g)


def render_marquee(W, H, name):
    print(f"{name}  {W}x{H}")
    shutil.rmtree(FRAMES, ignore_errors=True)
    os.makedirs(FRAMES, exist_ok=True)
    N = FPS * SECONDS
    bg = field(W, H)
    BLOOM, BD = bloom(W, H)
    LIT = Image.new("RGB", (W, H), (255, 255, 255))
    fade = feather(W, H)
    rows = [(strip(ns, H, fh, bl, gap), int(H * y), sp)
            for fh, y, bl, sp, gap, ns in MARQUEE]

    for f in range(N):
        t = f / N
        frame = bg.copy()
        bx = int(W * 0.62 + W * 0.26 * math.cos(2 * math.pi * t)) - BD // 2
        by = int(H * 0.46 + H * 0.20 * math.sin(2 * math.pi * t)) - BD // 2
        m = Image.new("L", (W, H), 0); m.paste(BLOOM, (bx, by))
        frame = Image.composite(LIT, frame, m.point(lambda q: int(q * 0.5)))

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for tile, y, sp in rows:
            tw = tile.width
            off = int(t * sp * tw) % tw      # sp laps per period, integer
            x = -off
            while x < W:
                layer.alpha_composite(tile, (x, y - tile.height // 2))
                x += tw
        layer.putalpha(Image.fromarray(
            (np.asarray(layer.getchannel("A")).astype(int) *
             np.asarray(fade).astype(int) // 255).astype(np.uint8)))
        frame = Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")
        frame.save(f"{FRAMES}/f{f:04d}.png")
        if f % 48 == 0:
            print(f"    frame {f}/{N}", flush=True)
    encode(name)


if __name__ == "__main__":
    render(1920, 740, STRIP_CAST, "hero-loop")
    render(1920, 1080, BG_CAST, "hero-bg-loop")
    render_marquee(1920, 1080, "hero-bg-marquee")
    if KEEP:
        print("  frames kept in", FRAMES)
    else:
        shutil.rmtree(FRAMES, ignore_errors=True)
