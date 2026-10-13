"""Contact sheet for the 17 cut-out, rebranded vials — checkerboard behind the
alpha so a stray white halo shows up instead of hiding against a white page."""
from PIL import Image, ImageDraw, ImageFont
import os, glob, json

R = os.path.dirname(os.path.abspath(__file__))   # the vials live beside this script
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from _fonts import font as _font
# Roles, not filenames, and no hardcoded Linux path. See ../_fonts.py
F = lambda n, s: _font({"DejaVuSansMono.ttf": "mono",
                        "DejaVuSans.ttf": "sans",
                        "DejaVuSans-Bold.ttf": "bold"}.get(n, "sans"), s)
MONO, BOLD = F("DejaVuSansMono.ttf", 13), F("DejaVuSans-Bold.ttf", 21)
INK, MUT = (10, 10, 11), (138, 133, 125)
# The caption used to name #2365CD, hardcoded. That is the LEGACY blue and it
# was wrong from the day the brand changed, while the sheet went on asserting
# it. It comes from brand.json now, like everything else.
BRAND_HEX = json.load(open(os.path.join(R, "..", "brand.json")))["brand"]

files = sorted(glob.glob(os.path.join(R, "tmg-*.png")))
COLS, CW, CH = 6, 172, 236
rows = (len(files) + COLS - 1) // COLS
W = 40 + COLS * CW + 20
H = 108 + rows * CH + 24
c = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(c)
d.text((36, 28), "VIALS — cut out, rebranded, blue crimp", font=BOLD, fill=(237, 235, 230))
d.text((36, 60), "%d files · transparent PNG · Gila mark and crimp in %s, cap as photographed"
       % (len(files), BRAND_HEX), font=MONO, fill=MUT)

# checkerboard tile so transparency is visible
tile = Image.new("RGB", (16, 16), (30, 30, 32))
ImageDraw.Draw(tile).rectangle([8, 0, 15, 7], fill=(38, 38, 41))
ImageDraw.Draw(tile).rectangle([0, 8, 7, 15], fill=(38, 38, 41))

for i, p in enumerate(files):
    x = 36 + (i % COLS) * CW
    y = 104 + (i // COLS) * CH
    cell = Image.new("RGB", (CW - 14, CH - 44))
    for ty in range(0, cell.height, 16):
        for tx in range(0, cell.width, 16):
            cell.paste(tile, (tx, ty))
    v = Image.open(p).convert("RGBA")
    k = min((cell.width - 16) / v.width, (cell.height - 16) / v.height)
    v = v.resize((int(v.width * k), int(v.height * k)), Image.LANCZOS)
    cell.paste(v, ((cell.width - v.width) // 2, (cell.height - v.height) // 2), v)
    c.paste(cell, (x, y))
    name = os.path.basename(p)[4:-4]
    d.text((x, y + cell.height + 8), name[:21], font=MONO, fill=(222, 220, 214))

c.save(os.path.join(R, "contact-sheet.jpg"), quality=92)
print("contact-sheet.jpg  %dx%d  %d vials" % (W, H, len(files)))


# ---------------------------------------------------------------------------
# The single-vial detail shot.
#
# `blue-crimp-detail.jpg` had NO script behind it. It was cropped by hand once
# and then sat in the repo through the brand-blue change, the mark change and
# the cap fix, still showing the legacy blue, the smooth lizard and a silver
# strip under the white disc. It was the oldest wrong picture in the project
# precisely because nothing rebuilt it. It is built from the current render now.
DETAIL_SRC = "tmg-ipamorelin.png"      # the product the original happened to use
DETAIL_W = 369                         # and the width it happened to be


def detail(src=DETAIL_SRC, out="blue-crimp-detail.jpg", width=DETAIL_W):
    v = Image.open(os.path.join(R, src)).convert("RGBA")
    v = v.crop(v.getbbox())                       # the vial's own bounding box
    k = width / v.width
    v = v.resize((width, max(1, int(round(v.height * k)))), Image.LANCZOS)
    bg = Image.new("RGB", v.size, (255, 255, 255))
    bg.paste(v, (0, 0), v)
    bg.save(os.path.join(R, out), quality=94)
    print("%s  %dx%d  from %s" % (out, bg.width, bg.height, src))
    return bg


detail()
