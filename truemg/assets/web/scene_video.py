"""The warm room, with the sun moving through it.

A still of the vials on stone fixed the bigger problem — they were floating on
a gradient with no light and nowhere to be. But a still is still a still, and
the thing that sells a room is time passing in it.

So this moves the LIGHT, not the bottles. Over eight seconds the sun tracks a
little across the frame, the pool on the stone slides with it, and every
shadow swings and lengthens in step. The bottles themselves barely stir. That
is the opposite of the first hero loop, where four cut-outs bobbed against a
flat field and the result read as a screensaver: motion that nothing in the
scene accounts for looks fake, and motion with a cause looks filmed.

Three things carry it:

  * the shadows are recomputed every frame from the light's current angle, so
    they swing and stretch rather than sliding around rigidly. This is most of
    the render cost and all of the effect.
  * a foreground bottle, very close and far out of focus, that the camera
    drifts past. Nothing says depth like something passing in front.
  * a slow lateral parallax, each bottle moving by its distance. Pixels, not
    inches — enough to feel, not enough to notice.

Everything is a sine over the full clip, so the last frame lands exactly where
the first began.

Run from this directory. Needs ffmpeg.
"""
import math
import os
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageFilter

import scene as S

FPS, SECONDS = 24, 8
FRAMES = os.environ.get("SCENE_FRAMES") or tempfile.mkdtemp(prefix="scene-frames-")
KEEP = bool(os.environ.get("SCENE_FRAMES"))

# name, centre x, height, defocus, parallax. The last entry is the foreground
# bottle: huge, soft, half out of frame, there purely to be passed.
CAST = [
    ("nad",            .560, .300, 2.6, 0.45),
    ("tmg-3rt",        .655, .345, 1.1, 0.70),
    ("ghk-cu",         .762, .420, 0.0, 1.00),
    ("bpc-157-tb-500", .868, .330, 1.4, 1.30),
    ("semax",          .205, .620, 9.0, 2.10),
]

LIGHT_SWING = 0.075      # how far the sun tracks, as a fraction of the width


def prep(W, H):
    out = []
    for name, fx, fh, dof, para in CAST:
        v = S.vial(name)
        h = max(1, int(H * fh))
        v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)
        v = S.warm(v)
        if dof:
            v = v.filter(ImageFilter.GaussianBlur(dof))
        out.append((v, fx, h, dof, para))
    return out


def render(W, H, name):
    print(f"{name}  {W}x{H}")
    shutil.rmtree(FRAMES, ignore_errors=True)
    os.makedirs(FRAMES, exist_ok=True)
    N = FPS * SECONDS
    parts = prep(W, H)
    base_light = S.LIGHT_X

    for f in range(N):
        t = f / N
        # the sun tracks across and back once per loop
        S.LIGHT_X = base_light + LIGHT_SWING * math.sin(2 * math.pi * t)
        room, hz = S.room(W, H)
        frame = room.convert("RGBA")
        drift = 7.0 * math.sin(2 * math.pi * t)          # the camera's slow slide

        for v, fx, h, dof, para in parts:
            cx = int(W * fx + drift * para)
            base = hz + int(H * 0.035)
            x, y = cx - v.width // 2, base - v.height

            # the shadow follows the light: further from it, longer and more
            # raked. This is why the frame reads as lit rather than composited.
            gap = fx - S.LIGHT_X
            lean = 1.0 if gap > 0 else -1.0
            cs, cpad = S.cast_shadow(v, 0.44 + abs(gap) * 0.42,
                                     lean * (0.85 + abs(gap) * 1.5),
                                     max(5, int(h * 0.028)))
            frame.alpha_composite(cs, (x - cpad, base - cpad))

            frame.alpha_composite(S.reflection(v), (x, base))
            cp, band = S.contact(v, max(5, int(h * 0.022)))
            frame.alpha_composite(cp, (x, base - band))
            frame.alpha_composite(v, (x, y))

        frame.convert("RGB").save(f"{FRAMES}/f{f:04d}.png")
        if f % 24 == 0:
            print(f"    frame {f}/{N}", flush=True)

    S.LIGHT_X = base_light
    encode(name)


def encode(name):
    seq = f"{FRAMES}/f%04d.png"
    common = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", seq]
    subprocess.run(common + ["-c:v", "libx264", "-preset", "slow", "-crf", "28",
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                             "-an", f"{name}.mp4"], check=True, capture_output=True)
    subprocess.run(common + ["-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0",
                             "-row-mt", "1", "-pix_fmt", "yuv420p",
                             "-an", f"{name}.webm"], check=True, capture_output=True)
    Image.open(f"{FRAMES}/f0000.png").convert("RGB").save(
        f"{name}-poster.jpg", quality=88, optimize=True)
    for f in (f"{name}.mp4", f"{name}.webm", f"{name}-poster.jpg"):
        print(f"    {f:26s} {os.path.getsize(f) // 1024} KB")


if __name__ == "__main__":
    render(1920, 1080, "scene-loop")
    if KEEP:
        print("  frames kept in", FRAMES)
    else:
        shutil.rmtree(FRAMES, ignore_errors=True)
