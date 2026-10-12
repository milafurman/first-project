from PIL import Image, ImageDraw, ImageFont
import os

WEB = "/Users/milafurman/first-project/.claude/worktrees/sad-noether-552cd4/truemg/assets/web"
OUT = os.path.join(WEB, "palette-grounds-v2.jpg")

BLUE = (28,140,208); DEEP = (15,84,126); INK = (26,24,22)

def f(n,s):
    for p in ["/System/Library/Fonts/Supplemental/"+n, "/System/Library/Fonts/"+n]:
        if os.path.exists(p): return ImageFont.truetype(p,s)
    return ImageFont.load_default()
B  = lambda s: f("Arial Bold.ttf", s)
R  = lambda s: f("Arial.ttf", s)
NB = lambda s: f("Arial Narrow Bold.ttf", s)

# name, page, card, band, quiet-type, three label tints, blurb
GROUNDS = [
 ("BONE",
  (248,245,239),(255,255,253),(238,233,224),(140,133,122),
  [(243,234,229),(234,238,233),(236,240,245)],
  "Warm white and almost nothing\nelse. The warmth is in the light,\nnot in a colour. The most\nexpensive-looking of the four."),
 ("GREIGE",
  (241,240,237),(252,252,250),(226,224,219),(132,129,123),
  [(242,235,231),(233,238,233),(234,238,243)],
  "Warm grey. Same calm, none of\nthe tan. Modern and quiet rather\nthan spa. The safest pick, and the\neasiest to photograph against."),
 ("EUCALYPTUS",
  (238,242,238),(252,253,251),(219,228,219),(124,135,124),
  [(243,236,231),(231,238,231),(233,238,244)],
  "The green off the orchids and the\nmonstera in your spa shot, taken\nright down. Nothing like anyone\nelse in this category. The boldest."),
 ("BLUSH",
  (248,243,241),(255,253,252),(240,229,226),(142,128,125),
  [(244,233,230),(234,238,233),(234,238,244)],
  "The warmth off the skin in your\nhand shot. Soft, human, no brown\nat all. Leans feminine - either\nexactly right or exactly wrong."),
]
CARDS = [("GHK-CU","50MG"),("NAD+","1000MG"),("SEMAX","30MG")]

W = 2000; ROW = 500
im = Image.new("RGB",(W, 300 + ROW*len(GROUNDS) + 180),(255,255,255))
d  = ImageDraw.Draw(im)
M  = 80

d.text((M,70),"FOUR WARM GROUNDS, NO BROWN", font=B(48), fill=INK)
d.text((M,136),"Same bottles, same blue, same tints. Only the ground changes. Pick the one that feels calm.",
       font=R(30), fill=(110,106,100))
d.line([(M,210),(W-M,210)], fill=(224,221,216), width=2)

y = 250
for name, page, card, band, quiet, tints, blurb in GROUNDS:
    d.rectangle([0,y,W,y+ROW-30], fill=page)
    # left: the name and why
    d.text((M, y+42), name, font=B(42), fill=DEEP)
    d.text((M, y+104), blurb, font=R(24), fill=quiet, spacing=9)
    # swatches
    sx = M
    _ = 0
    for lbl, c in (("page",page),("card",card),("band",band),("blue",BLUE)):
        d.rectangle([sx, y+248, sx+86, y+304], fill=c, outline=(200,197,192), width=2)
        d.text((sx, y+312), lbl, font=R(20), fill=quiet)
        sx += 100
    # a band, like a section strip
    d.rectangle([M, y+368, M+486, y+436], fill=band)
    d.text((M+22, y+390), "RESEARCH USE ONLY", font=B(24), fill=(70,66,62))

    # right: three catalog cards
    cx = 700; cw = 390; ch = 400; gap = 26
    for i,(nm,mg) in enumerate(CARDS):
        x = cx + i*(cw+gap)
        d.rectangle([x, y+40, x+cw, y+40+ch], fill=card, outline=(228,225,220), width=2)
        # tinted label chip standing in for the vial
        lx, ly, lw, lh = x+96, y+78, 198, 248
        d.rectangle([lx,ly,lx+lw,ly+lh], fill=tints[i], outline=(214,210,204), width=2)
        d.text((lx+16, ly+20), nm, font=B(24) if len(nm)<8 else NB(24), fill=BLUE)
        d.text((lx+16, ly+54), mg, font=B(19), fill=INK)
        d.ellipse([lx+16, ly+92, lx+16+40, ly+92+40], outline=BLUE, width=4)
        d.text((lx+16, ly+186), "NOT FOR HUMAN", font=R(11), fill=(70,66,62))
        d.text((lx+16, ly+201), "CONSUMPTION", font=R(11), fill=(70,66,62))
        d.text((lx+16, ly+216), "RESEARCH USE ONLY", font=R(11), fill=(70,66,62))
        d.rectangle([lx+lw-28, ly+2, lx+lw-2, ly+lh-2], fill=(253,252,251))
        d.text((lx+lw-24, ly+28), "T R U E", font=B(13), fill=INK)
        d.text((lx+lw-24, ly+64), "M G", font=B(13), fill=BLUE)
        # card footer
        d.text((x+22, y+40+ch-72), nm, font=B(26), fill=INK)
        d.text((x+22, y+40+ch-38), "Research use only.", font=R(20), fill=quiet)
    y += ROW

# the one she just saw, for reference
d.rectangle([0,y,W,y+150], fill=(245,241,234))
d.text((M, y+36), "FOR COMPARISON - the one you just saw", font=B(30), fill=(120,112,102))
d.text((M, y+80), "Same idea, but the ground was pulled off the spa photo's tan furniture. That is the brown.",
       font=R(25), fill=(130,122,112))
sx = W-M-4*100
for c in ((245,241,234),(193,171,145),(176,160,141),BLUE):
    d.rectangle([sx, y+44, sx+86, y+100], fill=c, outline=(205,196,183), width=2); sx += 100

im.save(OUT, quality=92)
print("wrote", OUT, im.size)
