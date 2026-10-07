"""Contact sheet for the 17 cut-out, rebranded vials — checkerboard behind the
alpha so a stray white halo shows up instead of hiding against a white page."""
from PIL import Image, ImageDraw, ImageFont
import os, glob, json

R = "/home/user/first-project/truemg/assets/vials"
F = lambda n, s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + n, s)
MONO, BOLD = F("DejaVuSansMono.ttf", 13), F("DejaVuSans-Bold.ttf", 21)
INK, MUT, BLUE = (10, 10, 11), (138, 133, 125), (64, 126, 224)

files = sorted(glob.glob(os.path.join(R, "tmg-*.png")))
COLS, CW, CH = 6, 172, 236
rows = (len(files) + COLS - 1) // COLS
W = 40 + COLS * CW + 20
H = 108 + rows * CH + 24
c = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(c)
d.text((36, 28), "VIALS — cut out, rebranded, blue crimp", font=BOLD, fill=(237, 235, 230))
d.text((36, 60), "%d files · transparent PNG · Gila mark and crimp in #2365CD, cap as photographed"
       % len(files), font=MONO, fill=MUT)

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
