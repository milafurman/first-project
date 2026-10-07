"""TrueMG vial label artwork — print-ready SVG at true millimetre scale."""
import os, re, json, html, shutil

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

# ---- geometry (mm). CONFIRM WITH THE LABEL PRINTER BEFORE ANY RUN. ----
TRIM_W, TRIM_H = 60.0, 30.0     # finished label
BLEED          = 3.0            # artwork extends this far past the trim
SAFE           = 2.5            # nothing critical inside this margin
WRAP           = 9.0            # right-hand strip that wraps out of sight on the cylinder
W, H = TRIM_W + 2*BLEED, TRIM_H + 2*BLEED
OX, OY = BLEED, BLEED           # trim origin inside the bleed box

INK, GOLD, PAPER, MUTED = "#0A0A0B", "#D8B46A", "#FCFBF8", "#9A948A"

# Ground / text / accent / muted / which lockup cut to place.
PALETTES = {
 "ink-gold":   dict(bg="#0A0A0B", fg="#FCFBF8", accent="#D8B46A", muted="#9A948A", lock="onink"),
 # THE brand blue, sampled from the original wordmark. Confirmed by Mila.
 "paper-blue": dict(bg="#FCFBF8", fg="#0A0A0B", accent="#2365CD", muted="#6E6A63", lock="onpaper"),
 "paper-teal": dict(bg="#FCFBF8", fg="#0A0A0B", accent="#0E7A8C", muted="#6E6A63", lock="onpaper"),
 "ink-blue":   dict(bg="#0A0A0B", fg="#FCFBF8", accent="#4C8BE8", muted="#9A948A", lock="onink"),
 # Gold on paper. #9C7C34 is the brand book's "accent on paper" and measures 3.80:1
 # against #FCFBF8 — under AA for small text. #866A2C is the same hue one step down
 # at 4.94:1 and is the safe choice for the strength line and the hairline.
 "paper-gold":     dict(bg="#FCFBF8", fg="#0A0A0B", accent="#9C7C34", muted="#6E6A63", lock="onpaper"),
 "paper-gold-aa":  dict(bg="#FCFBF8", fg="#0A0A0B", accent="#866A2C", muted="#5F5B54", lock="onpaper"),
 # Teal on ink, brightened to 10.02:1 — the same contrast the gold carries on ink,
 # so it reads with identical weight rather than merely being "a teal".
 "ink-teal":       dict(bg="#0A0A0B", fg="#FCFBF8", accent="#45C9DB", muted="#9A948A", lock="onink"),
}

def asset(path, want_viewbox=False):
    s = open(path).read()
    g = re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>', s, re.S)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    return (g.group(1), g.group(2).strip(), [float(x) for x in vb.split()])

MARK_TR, MARK_BODY, MARK_VB = asset("vec/truemg-mark-ink.svg")
WORD_TR, WORD_BODY, WORD_VB = asset("vec/truemg-wordmark-ink.svg")

def place(tr, body, vb, x, y, w, fill):
    """Drop a traced asset at (x,y) in mm, scaled to width w, recoloured."""
    s = w / vb[2]
    return (f'<g transform="translate({x:.3f},{y:.3f}) scale({s:.6f})">'
            f'<g transform="{tr}" fill="{fill}" stroke="none">{body}</g></g>')


def lockup_asset(path):
    """Read a finished lockup SVG and return (inner markup, width, height) in its own units."""
    raw = open(path).read()
    vb  = [float(x) for x in re.search(r'viewBox="([^"]+)"', raw).group(1).split()]
    inner = re.sub(r'^.*?<svg[^>]*>', '', raw, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner, flags=re.S)
    return inner, vb[2], vb[3]

_LOCK_CACHE = {}
def lockup_for(pal):
    key = (pal["lock"], pal["accent"], pal["fg"])
    if key not in _LOCK_CACHE:
        inner, w, h = lockup_asset("vec/truemg-labs-compact-%s.svg" % pal["lock"])
        if pal["lock"] == "onink":
            inner = inner.replace("#D8B46A", pal["accent"]).replace("#EDEBE6", pal["fg"])
        else:
            inner = inner.replace("#9C7C34", pal["accent"]).replace("#0A0A0B", pal["fg"])
        _LOCK_CACHE[key] = (inner, w, h)
    return _LOCK_CACHE[key]

def lockup_at(x, y, w, pal):
    inner, lw, _ = lockup_for(pal)
    s = w / lw
    return f'<g transform="translate({x:.3f},{y:.3f}) scale({s:.6f})">{inner}</g>'


def mark(x, y, w, fill):  return place(MARK_TR, MARK_BODY, MARK_VB, x, y, w, fill)
def word(x, y, w, fill):  return place(WORD_TR, WORD_BODY, WORD_VB, x, y, w, fill)

SLOGAN = "RESEARCH \u00b7 PURITY \u00b7 PRECISION"

DISPLAY = "Archivo Black, Archivo, Helvetica Neue, Arial, sans-serif"
MONO    = "IBM Plex Mono, SF Mono, Menlo, monospace"

# usable front panel: the right-hand WRAP strip curves out of sight on the vial
PANEL = TRIM_W - 2*SAFE - WRAP

def fit(text, avail, ratio, cap):
    """Largest font size (mm) at which `text` still fits `avail` mm."""
    return min(cap, avail / max(1e-6, ratio * len(text)))

def label_side(name, strength, net, lot="__________", guides=False, palette="paper-blue"):
    """Mila's own arrangement, kept: product name top left, strength under it, the
    Gila mark standing alone mid-left, the wordmark rotated up the right edge, and
    the compliance block across the bottom. Nothing of hers moves. What is added —
    the slogan, the lot and manufacture line, the third compliance line, and LABS
    on the wordmark — goes into the white space beside the mark, which was empty.

    The mark is 11.0mm here against the 7.4mm of the first pass: on the original
    vial it reads about half the width of the product name, and at 7.4 it had
    shrunk to a bullet point next to the text it used to stand apart from."""
    P = PALETTES[palette]
    e = html.escape
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{P["bg"]}"/>']
    cx, top = OX + SAFE, OY + SAFE
    bot   = OY + TRIM_H - SAFE
    right = cx + PANEL
    COL = PANEL - 7.0                      # the vertical wordmark takes the last 7mm

    MARK_W   = 11.0                        # standalone, mid-left, as on the original vial
    MARK_Y   = OY + 11.6
    ASIDE_X  = cx + MARK_W + 1.2           # the column of added text beside the mark
    ASIDE_W  = COL - (MARK_W + 1.2)

    # vertical wordmark, reading bottom to top
    wx, wy = right - 2.2, OY + TRIM_H - SAFE
    wlen = TRIM_H - 2*SAFE
    inner, lw, _ = lockup_for(P)
    g.append(f'<g transform="translate({wx:.2f},{wy:.2f}) rotate(-90) scale({wlen/lw:.6f})">{inner}</g>')

    NAME_Y, STR_Y = OY + 7.0, OY + 10.9
    ns = fit(name, COL, 0.62, 4.6)
    g.append(f'<text x="{cx}" y="{NAME_Y:.2f}" font-family="{DISPLAY}" font-weight="900" '
             f'font-size="{ns:.2f}" letter-spacing="-0.12" fill="{P["accent"]}">{e(name)}</text>')
    # the display face, not the mono one: on the original vial the strength is set
    # in the same heavy sans as the product name, a half-step down, and the mono
    # version read as a caption rather than the second half of the heading
    ss = fit(strength, COL, 0.60, 3.1)
    g.append(f'<text x="{cx}" y="{STR_Y:.2f}" font-family="{DISPLAY}" font-weight="900" '
             f'font-size="{ss:.2f}" letter-spacing="-0.04" fill="{P["fg"]}">{e(strength)}</text>')

    g.append(mark(cx, MARK_Y, MARK_W, P['accent']))

    SLOG_Y, LOT_Y = OY + 14.6, OY + 17.4
    sl = min(fit(SLOGAN, ASIDE_W, 0.60, 1.5), 1.5)
    g.append(f'<text x="{ASIDE_X:.2f}" y="{SLOG_Y:.2f}" font-family="{MONO}" '
             f'font-size="{sl:.2f}" letter-spacing="0.1" fill="{P["accent"]}">{e(SLOGAN)}</text>')
    dl = f"LOT {lot}  MFG __________"
    dz = min(fit(dl, ASIDE_W, 0.60, 1.35), 1.35)
    g.append(f'<text x="{ASIDE_X:.2f}" y="{LOT_Y:.2f}" font-family="{MONO}" '
             f'font-size="{dz:.2f}" letter-spacing="0.05" fill="{P["muted"]}">{e(dl)}</text>')

    lines = ["NOT FOR HUMAN OR VETERINARY USE",
             "FOR LABORATORY RESEARCH USE ONLY",
             "NOT FOR DIAGNOSTIC USE"]
    CMP_Y, LEAD = OY + 24.2, 1.55
    cs = min(fit(max(lines, key=len), COL, 0.60, 1.5), 1.5)
    for i, ln in enumerate(lines):
        g.append(f'<text x="{cx}" y="{CMP_Y + i*LEAD:.2f}" font-family="{MONO}" '
                 f'font-size="{cs:.2f}" letter-spacing="0.03" '
                 f'fill="{P["fg"] if i == 0 else P["muted"]}">{e(ln)}</text>')

    # Every baseline inside the safe box, and the mark clear of the block below it.
    for tag, y in [("name", NAME_Y), ("strength", STR_Y), ("slogan", SLOG_Y),
                   ("lot", LOT_Y), ("compliance", CMP_Y + 2*LEAD)]:
        assert top <= y <= bot, "%s baseline %.2f outside the safe box" % (tag, y)
    assert MARK_Y + MARK_W <= CMP_Y - cs, "the mark runs into the compliance block"
    assert MARK_Y >= STR_Y + 0.6, "the mark runs into the strength line"
    assert SLOG_Y - sl >= MARK_Y, "the slogan sits above the mark it should sit beside"

    if guides:
        g.append(f'<g fill="none" stroke-width="0.12">'
                 f'<rect x="{OX}" y="{OY}" width="{TRIM_W}" height="{TRIM_H}" stroke="#FF3B6B" stroke-dasharray="1.2 .8"/>'
                 f'<rect x="{OX+SAFE}" y="{OY+SAFE}" width="{TRIM_W-2*SAFE}" height="{TRIM_H-2*SAFE}" stroke="#36C9F0" stroke-dasharray=".8 .8"/>'
                 f'<line x1="{right}" y1="{OY}" x2="{right}" y2="{OY+TRIM_H}" stroke="#F0B24A" stroke-dasharray=".6 .6"/></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}">{"".join(g)}</svg>')


def label(name, strength, net, lot="__________", guides=False, palette="ink-gold"):
    P = PALETTES[palette]
    """Explicit vertical budget. Content box is 25mm tall; every baseline is placed,
    not derived, so nothing can collide as text lengths change."""
    e = html.escape
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{P['bg']}"/>']
    cx   = OX + SAFE
    top  = OY + SAFE
    right = cx + PANEL            # right edge of the readable front panel

    # --- identity row ---
    g.append(mark(cx, top - 0.2, 5.6, P['accent']))
    g.append(lockup_at(cx + 7.0, top + 0.5, 17.0, P))
    g.append(f'<text x="{right:.2f}" y="{top+4.6:.2f}" text-anchor="end" '
             f'font-family="{MONO}" font-size="1.75" letter-spacing="0.05" '
             f'fill="{P["muted"]}">truemglabs.com</text>')

    # --- compound name + strength ---
    ns = fit(name, PANEL, 0.68, 4.8)
    g.append(f'<text x="{cx}" y="{OY+12.2:.2f}" font-family="{DISPLAY}" font-weight="900" '
             f'font-size="{ns:.2f}" letter-spacing="-0.12" fill="{P["fg"]}">{e(name)}</text>')
    ss = fit(strength, PANEL, 0.62, 3.1)
    g.append(f'<text x="{cx}" y="{OY+16.0:.2f}" font-family="{MONO}" font-weight="600" '
             f'font-size="{ss:.2f}" letter-spacing="0.14" fill="{P["accent"]}">{e(strength)}</text>')

    # --- rule ---
    g.append(f'<text x="{cx}" y="{OY+18.0:.2f}" font-family="{MONO}" font-size="1.7" '
             f'letter-spacing="0.1" fill="{P["accent"]}">{e(SLOGAN)}</text>')
    g.append(f'<rect x="{cx}" y="{OY+19.1:.2f}" width="{PANEL:.2f}" height="0.26" fill="{P["accent"]}"/>')

    # --- compliance. Non-negotiable; sized to stay inside the panel. ---
    lines = ["FOR LABORATORY RESEARCH USE ONLY",
             "NOT FOR HUMAN OR VETERINARY USE",
             "NOT FOR DIAGNOSTIC USE"]
    cs = min(fit(max(lines, key=len), PANEL, 0.60, 1.9), 1.9)
    for i, ln in enumerate(lines):
        g.append(f'<text x="{cx}" y="{OY+20.8 + i*1.8:.2f}" font-family="{MONO}" '
                 f'font-size="{cs:.2f}" letter-spacing="0.04" '
                 f'fill="{P['fg'] if i == 0 else P['muted']}">{e(ln)}</text>')

    # --- variable data, last line, clear of everything above ---
    dline = f"LOT {lot}   MFG __________"
    ds = min(fit(dline, PANEL, 0.60, 1.8), 1.8)
    g.append(f'<text x="{cx}" y="{OY+26.9:.2f}" font-family="{MONO}" '
             f'font-size="{ds:.2f}" letter-spacing="0.05" fill="{P["muted"]}">{e(dline)}</text>')

    if guides:
        g.append(f'<g fill="none" stroke-width="0.12">'
                 f'<rect x="{OX}" y="{OY}" width="{TRIM_W}" height="{TRIM_H}" stroke="#FF3B6B" stroke-dasharray="1.2 0.8"/>'
                 f'<rect x="{OX+SAFE}" y="{OY+SAFE}" width="{TRIM_W-2*SAFE}" height="{TRIM_H-2*SAFE}" stroke="#36C9F0" stroke-dasharray="0.8 0.8"/>'
                 f'<line x1="{right}" y1="{OY}" x2="{right}" y2="{OY+TRIM_H}" stroke="#F0B24A" stroke-dasharray="0.6 0.6"/></g>'
                 f'<text x="{OX+0.4}" y="{OY-0.9}" font-family="{MONO}" font-size="1.4" fill="#FF3B6B">TRIM {TRIM_W:.0f}\u00d7{TRIM_H:.0f}mm \u00b7 bleed {BLEED:.0f} \u00b7 safe {SAFE:.1f}</text>'
                 f'<text x="{right+0.3}" y="{OY+TRIM_H+2.2}" font-family="{MONO}" font-size="1.4" fill="#F0B24A">wrap \u2192</text>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}">{"".join(g)}</svg>')

PRODUCTS = [
 ("BPC-157 + TB-500","20 MG (10+10)","20 mg"), ("CJC-1295 + IPAMORELIN","10 MG (5+5)","10 mg"),
 ("EPITHALON","10 MG","10 mg"), ("GHK-CU","50 MG","50 mg"), ("IPAMORELIN","10 MG","10 mg"),
 ("KLOW","80 MG BLEND","80 mg"), ("MOTS-C","20 MG","20 mg"), ("NAD+","1000 MG","1000 mg"),
 ("SELANK","10 MG","10 mg"), ("SEMAX","10 MG","10 mg"), ("SS-31","10 MG","10 mg"),
 ("SS-31","50 MG","50 mg"), ("TESAMORELIN","20 MG","20 mg"), ("THYMOSIN ALPHA-1","10 MG","10 mg"),
 ("TMG-2TZ","10 MG","10 mg"), ("TMG-2TZ","20 MG","20 mg"), ("TMG-3RT","10 MG","10 mg"),
 ("TMG-3RT","20 MG","20 mg"), ("TMG-BAC","10 ML RESEARCH SOLUTION","10 ml"), ("VITAMIN B12","10 ML","10 ml"),
]

if __name__ == "__main__":
    PALETTE = "paper-blue"          # confirmed: the brand blue, on white
    shutil.rmtree("labels", ignore_errors=True)   # stale artwork has shipped before
    os.makedirs("labels/side", exist_ok=True)
    os.makedirs("labels/top", exist_ok=True)
    open("labels/_TEMPLATE-with-guides.svg","w").write(
        label_side("GHK-CU","50 MG","50 mg", guides=True, palette=PALETTE))
    man=[]
    for n,st,net in PRODUCTS:
        slug = re.sub(r'[^a-z0-9]+','-', f"{n} {st}".lower()).strip('-')
        open(f"labels/side/{slug}.svg","w").write(label_side(n,st,net,palette=PALETTE))
        open(f"labels/top/{slug}.svg","w").write(label(n,st,net,palette=PALETTE))
        man.append({"product":n,"strength":st,"file":f"{slug}.svg"})
    # the palette set, kept reproducible so it can never go stale against the layout
    os.makedirs("labels/palettes", exist_ok=True)
    for pal in PALETTES:
        for n, st, _net in [("GHK-CU","50 MG","50 mg"), ("NAD+","1000 MG","1000 mg")]:
            slug = re.sub(r'[^a-z0-9]+','-', n.lower()).strip('-')
            open(f"labels/palettes/{pal}--{slug}.svg","w").write(label_side(n,st,_net,palette=pal))
    json.dump(man, open("labels/manifest.json","w"), indent=1)
    print(f"{len(man)} products x 2 layouts, palette {PALETTE}")
    print(f"artwork {W}x{H}mm (trim {TRIM_W}x{TRIM_H}, bleed {BLEED}, safe {SAFE}, wrap {WRAP})")
