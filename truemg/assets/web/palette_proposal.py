from PIL import Image, ImageDraw, ImageFont
import os

WEB = "/Users/milafurman/first-project/.claude/worktrees/sad-noether-552cd4/truemg/assets/web"
OUT = os.path.join(WEB, "palette-proposal-v1.jpg")

BLUE   = (28,140,208)
DEEP   = (15,84,126)
INK    = (26,24,22)
GROUND = (245,241,234)   # warm paper, pulled from the hand/spa shots
SAND   = (193,171,145)
STONE  = (176,160,141)

def f(name, size):
    for p in ["/System/Library/Fonts/Supplemental/"+name,
              "/System/Library/Fonts/"+name]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

B  = lambda s: f("Arial Bold.ttf", s)
R  = lambda s: f("Arial.ttf", s)
NB = lambda s: f("Arial Narrow Bold.ttf", s)

# name, tint, family
TINTS = [
 ("GHK-CU",              (240,223,214), "repair"),
 ("BPC-157 + TB-500",    (240,225,211), "repair"),
 ("KLOW",                (236,224,213), "repair"),
 ("IPAMORELIN",          (226,233,222), "signal"),
 ("CJC-1295 + IPA",      (219,230,221), "signal"),
 ("TESAMORELIN",         (230,233,218), "signal"),
 ("TMG-2TZ",             (241,234,215), "metabolic"),
 ("TMG-3RT",             (243,230,208), "metabolic"),
 ("MOTS-C",              (226,231,214), "metabolic"),
 ("SEMAX",               (231,227,238), "neuro"),
 ("SELANK",              (224,229,240), "neuro"),
 ("NAD+",                (219,232,241), "cofactor"),
 ("EPITHALON",           (233,233,232), "cofactor"),
 ("THYMOSIN ALPHA-1",    (238,231,217), "cofactor"),
 ("SS-31",               (222,228,234), "cofactor"),
 ("VITAMIN B12",         (243,226,228), "cofactor"),
 ("TMG-BAC",             (252,252,251), "plain"),
]

W = 2000
im = Image.new("RGB", (W, 2460), GROUND)
d  = ImageDraw.Draw(im)
M  = 90

def text(xy, s, font, fill=INK, **kw):
    d.text(xy, s, font=font, fill=fill, **kw)

y = 80
text((M, y), "TRUEMG — PROPOSED PALETTE", B(46)); y += 62
text((M, y), "Built from the two pictures you made, not from Amino Club.", R(30), (90,84,78)); y += 70

# ---------- 1. the two moods ----------
d.line([(M,y),(W-M,y)], fill=(216,208,196), width=2); y += 40
text((M, y), "1.  YOUR CALM IS WARM.  THE STORE'S PRODUCT SHOT IS COLD.", B(34), DEEP); y += 56

ph, pw = 300, (W - M*2 - 30)//2
def place(src, box, dest):
    o = Image.open(os.path.join(WEB, src)).convert("RGB")
    sw, sh = o.size
    s = max(box[0]/sw, box[1]/sh)
    o = o.resize((int(sw*s), int(sh*s)), Image.LANCZOS)
    l = (o.width-box[0])//2; t = (o.height-box[1])//2
    im.paste(o.crop((l,t,l+box[0],t+box[1])), dest)

place("hand-vial-labelled.jpg", (pw//2-8, ph), (M, y))
place("hero-spa.jpg",           (pw//2-8, ph), (M+pw//2+8, y))
place("hero-float.jpg",         (pw, ph),      (M+pw+30, y))
d.rectangle([M,y,M+pw,y+ph], outline=(205,196,183), width=2)
d.rectangle([M+pw+30,y,W-M,y+ph], outline=(205,196,183), width=2)
y += ph + 16
text((M, y), "The hand and the spa — warm sand, stone, cream.", B(26), (70,64,58))
text((M+pw+30, y), "The floating vials — cold blue-grey.", B(26), (70,64,58))
y += 40
text((M, y), "These are near opposites on the colour wheel. That is why the store feels clinical\n"
             "and the hand feels calm. The fix is not a new photo — it is making the warm one the ground\n"
             "and letting the blue be the only cool thing in the frame, exactly like the hand shot already does.",
     R(27), (90,84,78), spacing=10)
y += 150

# ---------- 2. the ground ----------
d.line([(M,y),(W-M,y)], fill=(216,208,196), width=2); y += 40
text((M, y), "2.  THE GROUND AND THE HOUSE COLOUR", B(34), DEEP); y += 56
base = [("Paper", GROUND, "every page sits on this"),
        ("Sand",  SAND,   "section bands, cards"),
        ("Stone", STONE,  "rules, quiet type"),
        ("Brand blue", BLUE, "the one cool note"),
        ("Deep blue", DEEP, "headings, the footer")]
cw = (W - M*2 - 4*24)//5
for i,(n,c,use) in enumerate(base):
    x = M + i*(cw+24)
    d.rectangle([x,y,x+cw,y+150], fill=c, outline=(205,196,183), width=2)
    text((x, y+162), n, B(28))
    text((x, y+196), use, R(23), (120,113,105))
y += 260

# ---------- 3. the per-compound tints ----------
d.line([(M,y),(W-M,y)], fill=(216,208,196), width=2); y += 40
text((M, y), "3.  ONE PAPER TINT PER COMPOUND", B(34), DEEP); y += 50
text((M, y), "Tinted label paper, not coloured glass. The bottle, the cap and the blue never change —\n"
             "only the paper. Grouped so the shelf reads as five families, not seventeen random colours.",
     R(27), (90,84,78), spacing=10); y += 90

COLS, LW, LH, GAP = 6, 280, 200, 26
fam_shown = set()
x, ry = M, y
for i,(name, tint, fam) in enumerate(TINTS):
    col, row = i % COLS, i // COLS
    x  = M + col*(LW+GAP)
    ry = y + row*(LH+78)
    # mini label
    d.rectangle([x,ry,x+LW,ry+LH], fill=tint, outline=(206,198,186), width=2)
    fn = NB(26) if len(name) > 13 else B(27)
    text((x+18, ry+22), name, fn, BLUE)
    text((x+18, ry+58), "10MG", B(22), INK)
    d.ellipse([x+18, ry+96, x+18+46, ry+96+46], outline=BLUE, width=4)
    text((x+18, ry+154), "NOT FOR HUMAN CONSUMPTION", R(13), (60,56,52))
    text((x+18, ry+172), "RESEARCH USE ONLY", R(13), (60,56,52))
    # wordmark edge
    d.rectangle([x+LW-40, ry+2, x+LW-2, ry+LH-2], fill=(252,251,249))
    text((x+LW-34, ry+30), "T R U E", B(17), INK)
    text((x+LW-34, ry+78), "M G", B(17), BLUE)
    text((x+6, ry+LH+12), fam.upper(), B(20), (150,142,132))

y = ry + LH + 70
d.line([(M,y),(W-M,y)], fill=(216,208,196), width=2); y += 36
text((M, y), "TMG-BAC stays plain white on purpose — it is a solution, not a compound, and the eye should see that.",
     R(26), (90,84,78))
y += 44
text((M, y), "Nothing here touches the glass, the cap, the lizard or the blue. It is the paper only.",
     B(26), DEEP)

im = im.crop((0,0,W, y+90))
im.save(OUT, quality=92)
print("wrote", OUT, im.size)
