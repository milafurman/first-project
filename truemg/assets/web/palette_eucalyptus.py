from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, colorsys

WEB = "/Users/milafurman/first-project/.claude/worktrees/sad-noether-552cd4/truemg/assets/web"

BLUE=(28,140,208); DEEP=(15,84,126); INK=(26,24,22)
PAGE=(238,242,238); CARD=(252,253,251); BAND=(219,228,219)
QUIET=(124,135,124); LINE=(214,224,214)

def f(n,s):
    for p in ["/System/Library/Fonts/Supplemental/"+n,"/System/Library/Fonts/"+n]:
        if os.path.exists(p): return ImageFont.truetype(p,s)
    return ImageFont.load_default()
B=lambda s:f("Arial Bold.ttf",s); R=lambda s:f("Arial.ttf",s)
NB=lambda s:f("Arial Narrow Bold.ttf",s); AB=lambda s:f("Arial Black.ttf",s)

def fit(d, text, maxw, bold, narrow, hi=22, lo=9):
    """largest size at which text fits maxw; falls back to the narrow face"""
    for face in (bold, narrow):
        for sz in range(hi, lo-1, -1):
            if d.textlength(text, font=face(sz)) <= maxw:
                return face(sz)
    return narrow(lo)

def wash(tint, amt):
    """ultra-pale version of a tint, for the card's image field"""
    return tuple(int(c + (255-c)*amt) for c in tint)

# five families, five well-separated hues so none of them collides with the
# green page: rose / butter / sage / lilac / ice blue, plus white
PRODUCTS = [
 ("GHK-CU",            "50MG",   (245,230,229), "repair"),
 ("BPC-157 + TB-500",  "10+10MG",(243,227,226), "repair"),
 ("KLOW",              "70MG",   (241,224,224), "repair"),
 ("IPAMORELIN",        "5MG",    (246,242,226), "signal"),
 ("CJC-1295 + IPA",    "5+5MG",  (244,240,221), "signal"),
 ("TESAMORELIN",       "10MG",   (242,238,218), "signal"),
 ("TMG-2TZ",           "10MG",   (227,238,228), "metabolic"),
 ("TMG-3RT",           "10MG",   (222,235,223), "metabolic"),
 ("MOTS-C",            "10MG",   (231,240,231), "metabolic"),
 ("SEMAX",             "30MG",   (234,230,242), "neuro"),
 ("SELANK",            "10MG",   (230,227,240), "neuro"),
 ("NAD+",              "1000MG", (225,236,245), "cofactor"),
 ("EPITHALON",         "10MG",   (231,239,246), "cofactor"),
 ("THYMOSIN ALPHA-1",  "5MG",    (228,237,245), "cofactor"),
 ("SS-31",             "10MG",   (222,234,244), "cofactor"),
 ("VITAMIN B12",       "5MG",    (234,241,247), "cofactor"),
 ("TMG-BAC",           "10ML",   (253,253,252), "plain"),
]

# ---------------------------------------------------------------- the shelf
W=2000; M=80
COLS=5; CW=(W-M*2-(COLS-1)*26)//COLS; GAP=26
ROWS=(len(PRODUCTS)+COLS-1)//COLS
IMGH=int(CW*0.92); CH=IMGH+128

HEAD=190; HERO=250
H = HEAD+HERO+70 + ROWS*(CH+30) + 230
im=Image.new("RGB",(W,H),PAGE); d=ImageDraw.Draw(im)

# header
d.rectangle([0,0,W,HEAD],fill=(252,253,251))
d.text((M,62),"T R U E",font=AB(40),fill=INK)
d.text((M+196,62),"M G",font=AB(40),fill=BLUE)
d.text((M+2,112),"L  A  B  S",font=B(18),fill=QUIET)
nav=["CATALOG","CERTIFICATES","ABOUT","CONTACT"]; nx=W-M
for lbl in reversed(nav):
    nx -= d.textlength(lbl,font=B(22))
    d.text((nx,76),lbl,font=B(22),fill=(70,76,70)); nx -= 58
d.line([(0,HEAD),(W,HEAD)],fill=LINE,width=2)

# hero band
y=HEAD
d.rectangle([0,y,W,y+HERO],fill=BAND)
d.text((M,y+58),"Seventeen compounds. Lot-matched paperwork.",font=B(44),fill=DEEP)
d.text((M,y+124),"Research use only. Not for human consumption.",font=R(28),fill=(84,96,84))
y+=HERO+56

d.text((M,y),"CATALOG",font=B(26),fill=QUIET); y+=56

for i,(name,mg,tint,fam) in enumerate(PRODUCTS):
    col,row=i%COLS, i//COLS
    x=M+col*(CW+GAP); cy=y+row*(CH+30)
    d.rectangle([x,cy,x+CW,cy+CH],fill=CARD,outline=(226,234,226),width=2)
    # image field - keyed to this compound, NOT one blue for all seventeen
    d.rectangle([x+2,cy+2,x+CW-2,cy+IMGH],fill=wash(tint,0.45))
    # the label, standing in for the vial render
    lw=int(CW*0.44); lh=int(IMGH*0.70)
    lx=x+(CW-lw)//2; ly=cy+(IMGH-lh)//2
    d.rectangle([lx,ly,lx+lw,ly+lh],fill=tint,outline=(206,214,206),width=2)
    avail = lw - 22 - 12 - 8          # chip width less wordmark strip and pads
    fn = fit(d, name, avail, B, NB, hi=20, lo=9)
    d.text((lx+12,ly+16),name,font=fn,fill=BLUE)
    d.text((lx+12,ly+44),mg,font=B(16),fill=INK)
    d.ellipse([lx+12,ly+74,lx+12+32,ly+74+32],outline=BLUE,width=3)
    d.text((lx+12,ly+lh-42),"NOT FOR HUMAN",font=R(9),fill=(60,66,60))
    d.text((lx+12,ly+lh-31),"CONSUMPTION",font=R(9),fill=(60,66,60))
    d.text((lx+12,ly+lh-20),"RESEARCH USE ONLY",font=R(9),fill=(60,66,60))
    d.rectangle([lx+lw-22,ly+2,lx+lw-2,ly+lh-2],fill=(253,253,252))
    d.text((lx+lw-19,ly+22),"T R U E",font=B(10),fill=INK)
    d.text((lx+lw-19,ly+52),"M G",font=B(10),fill=BLUE)
    # card text
    d.text((x+18,cy+IMGH+18),name,font=fit(d,name,CW-36,B,NB,hi=21,lo=13),fill=INK)
    d.text((x+18,cy+IMGH+50),"Research use only.",font=R(17),fill=QUIET)
    d.text((x+18,cy+IMGH+78),"99%+  ·  View COA",font=B(16),fill=BLUE)

y=y+ROWS*(CH+30)+26
d.rectangle([0,y,W,H],fill=(32,42,34))
d.text((M,y+52),"T R U E",font=AB(30),fill=(240,244,240))
d.text((M+148,y+52),"M G",font=AB(30),fill=(120,190,235))
d.text((M,y+112),"Research use only. Not for human consumption. Not for diagnostic or therapeutic use.",
       font=R(22),fill=(150,166,152))
im.save(os.path.join(WEB,"palette-eucalyptus-shelf.jpg"),quality=92)
print("shelf", im.size)

# ---------------------------------------------------------- the hero question
src=Image.open(os.path.join(WEB,"hand-vial-labelled.jpg")).convert("RGB")
def regrade(o):
    o=ImageEnhance.Color(o).enhance(0.66)          # pull the orange down
    wash_layer=Image.new("RGB",o.size,(222,232,222))
    return Image.blend(o, wash_layer, 0.12)        # lay the eucalyptus over it
W2=2000
sw,sh=src.size; s=W2/sw
asis=src.resize((W2,int(sh*s)),Image.LANCZOS); hh=asis.height
reg=regrade(asis)
im2=Image.new("RGB",(W2, 150+hh*2+200),PAGE); d2=ImageDraw.Draw(im2)
d2.text((M,54),"YOUR HAND SHOT ON A EUCALYPTUS SITE",font=B(44),fill=INK)
d2.text((M,112),"The background of that photo is beige. On a green page it reads as a different room.",
        font=R(27),fill=QUIET)
yy=170
im2.paste(asis,(0,yy)); d2.rectangle([0,yy,W2,yy+hh],outline=LINE,width=2)
d2.text((M,yy+hh+16),"AS IT IS - warm beige behind the hand, fighting the page",font=B(26),fill=(150,90,70))
yy+=hh+66
im2.paste(reg,(0,yy)); d2.rectangle([0,yy,W2,yy+hh],outline=LINE,width=2)
d2.text((M,yy+hh+16),"REGRADED - same photo, colour pulled toward the ground. One pass, no reshoot.",
        font=B(26),fill=DEEP)
im2=im2.crop((0,0,W2,yy+hh+70))
im2.save(os.path.join(WEB,"palette-eucalyptus-hero.jpg"),quality=92)
print("hero", im2.size)
