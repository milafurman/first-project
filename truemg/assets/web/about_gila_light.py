"""About image, light. Matches the storefront: pale blue ground, brand-blue mark."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os, math
R = "/Users/milafurman/first-project/.claude/worktrees/sad-noether-552cd4/truemg/assets"
W, H = 1600, 1100

TOP  = np.array([246, 250, 254], float)   # near-white, like the page
BOT  = np.array([222, 235, 248], float)   # the pale blue the catalog bands use
BLUE = (28, 140, 208)                     # brand accent

yy, xx = np.mgrid[0:H, 0:W].astype(float)
g = (yy / H) ** 0.85
base = TOP[None, None, :] + (BOT - TOP)[None, None, :] * g[..., None]
# one soft light from upper left so it is not a flat wash
warm = np.clip(1.0 - np.sqrt(((xx - W*0.30)/(W*0.95))**2 + ((yy - H*0.22)/(H*1.05))**2), 0, 1) ** 1.5
base += np.array([9, 7, 3], float)[None, None, :] * warm[..., None]
im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
d = ImageDraw.Draw(im, "RGBA")

# the same strata, inverted: faint blue lines on a light ground
rng = np.random.default_rng(11)
for i in range(9):
    y0 = int(H * (0.58 + i * 0.055))
    amp = 10 + i * 4
    ph = rng.uniform(0, math.tau)
    pts = [(x, y0 + amp*math.sin(ph + x/(W/2.2)) + amp*.4*math.sin(ph*2 + x/(W/5.5)))
           for x in range(0, W + 1, 6)]
    d.line(pts, fill=(28, 140, 208, 24 - i*2), width=2, joint="curve")

im = im.filter(ImageFilter.GaussianBlur(0.5)).convert("RGBA")

mk = Image.open(os.path.join(R, "vials", "mark-og.png")).convert("RGBA")
mk = mk.crop(mk.getbbox())
k = (H * 0.70) / mk.height
mk = mk.resize((int(mk.width*k), int(mk.height*k)), Image.LANCZOS)
mx, my = int(W*0.60 - mk.width//2), int(H*0.46 - mk.height//2)

# a soft drop shadow instead of a glow — light grounds need weight, not light
sh = Image.new("RGBA", im.size, (0,0,0,0))
sh.paste(Image.new("RGBA", mk.size, (18, 60, 100, 66)), (mx, my+14), mk)
sh = sh.filter(ImageFilter.GaussianBlur(34))
im = Image.alpha_composite(im, sh)

lit = Image.new("RGBA", mk.size, BLUE + (255,))
lit.putalpha(mk.getchannel("A"))
im.alpha_composite(lit, (mx, my))

out = os.path.join(R, "web", "about-gila-light.jpg")
im.convert("RGB").save(out, quality=94, optimize=True)
print("wrote", out, im.size)
