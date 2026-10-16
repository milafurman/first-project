"""About image, take 2. Deep ground, real light, the mark as a found object."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os, math
R = "/Users/milafurman/first-project/.claude/worktrees/sad-noether-552cd4/truemg/assets"
W, H = 1600, 1100

INK  = np.array([10, 22, 38], float)     # near her footer navy
MID  = np.array([16, 44, 74], float)
BLUE = (28, 140, 208)

# ground: a deep field with a single warm-cool light from upper left
yy, xx = np.mgrid[0:H, 0:W].astype(float)
cx, cy = W * 0.34, H * 0.30
dist = np.sqrt(((xx - cx) / (W * 0.85)) ** 2 + ((yy - cy) / (H * 0.95)) ** 2)
fall = np.clip(1.0 - dist, 0, 1) ** 1.6
base = INK[None, None, :] + (MID - INK)[None, None, :] * fall[..., None]
# a cold rim toward the lower right so the frame has two light sources
rim = np.clip(1.0 - np.sqrt(((xx - W * 1.02) / (W * 0.75)) ** 2 + ((yy - H * 1.05) / (H * 0.8)) ** 2), 0, 1) ** 2
base += np.array([18, 52, 84], float)[None, None, :] * rim[..., None] * 0.55
im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
d = ImageDraw.Draw(im, "RGBA")

# strata: now readable, because the ground is dark
rng = np.random.default_rng(11)
for i in range(9):
    y0 = int(H * (0.58 + i * 0.055))
    amp = 10 + i * 4
    ph = rng.uniform(0, math.tau)
    pts = [(x, y0 + amp * math.sin(ph + x / (W / 2.2)) + amp * .4 * math.sin(ph * 2 + x / (W / 5.5)))
           for x in range(0, W + 1, 6)]
    d.line(pts, fill=(120, 190, 240, 26 - i), width=2, joint="curve")

im = im.filter(ImageFilter.GaussianBlur(0.5))

# the mark, with a real glow so it reads as lit rather than pasted
mk = Image.open(os.path.join(R, "vials", "mark-og.png")).convert("RGBA")
mk = mk.crop(mk.getbbox())
k = (H * 0.70) / mk.height
mk = mk.resize((int(mk.width * k), int(mk.height * k)), Image.LANCZOS)
mx, my = int(W * 0.60 - mk.width // 2), int(H * 0.46 - mk.height // 2)

glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
glow.paste(Image.new("RGBA", mk.size, (40, 160, 230, 150)), (mx, my), mk)
glow = glow.filter(ImageFilter.GaussianBlur(55))
im = Image.alpha_composite(im.convert("RGBA"), glow)
glow2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
glow2.paste(Image.new("RGBA", mk.size, (150, 215, 255, 110)), (mx, my), mk)
glow2 = glow2.filter(ImageFilter.GaussianBlur(14))
im = Image.alpha_composite(im, glow2)

# the mark itself, lightened a touch so it sits above its own glow
lit = Image.new("RGBA", mk.size, (96, 186, 240, 255))
lit.putalpha(mk.getchannel("A"))
im.alpha_composite(lit, (mx, my))

out = os.path.join(R, "web", "about-gila.jpg")
im.convert("RGB").save(out, quality=94, optimize=True)
print("wrote", out, im.size)
