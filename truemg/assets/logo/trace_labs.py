"""Trace LABS and compose the TrueMG Labs lockups as font-free vector."""
import subprocess, os, re
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
WORD_W, WORD_H = 5634, 681

# ---- trace the two LABS settings ----
labs = {}
for tag in ["labs-wide", "labs-compact"]:
    im = Image.open(tag + ".png").convert("L")
    bw = im.point(lambda v: 0 if v < 128 else 255).convert("1")   # glyphs black for potrace
    bw.save("vec/%s.pbm" % tag)
    subprocess.run(["potrace", "-s", "-a", "0.4", "-t", "8", "-u", "40", "-O", "0.2",
                    "-o", "vec/%s-raw.svg" % tag, "vec/%s.pbm" % tag], check=True)
    raw = open("vec/%s-raw.svg" % tag).read()
    g = re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>', raw, re.S)
    paths = re.findall(r'<path d="([^"]+)"\s*/>', g.group(2), re.S)
    labs[tag] = (g.group(1), paths, bw.size)
    print("%-14s %2d paths  bitmap %s" % (tag, len(paths), bw.size))

# ---- the wordmark, split into TRUE and MG ----
w = open("vec/truemg-wordmark-ink.svg").read()
wg = re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>', w, re.S)
WTR = wg.group(1)
wpaths = re.findall(r'<path d="([^"]+)"\s*/>', wg.group(2), re.S)
startx = lambda d: float(re.match(r'\s*M\s*(-?[\d.]+)', d).group(1))
order = sorted(range(len(wpaths)), key=lambda i: startx(wpaths[i]))
TRUE_I, MG_I = order[:-2], order[-2:]
print("wordmark split -> TRUE %s  MG %s" % (TRUE_I, MG_I))

def paths_svg(idx):
    return "".join('<path d="%s"/>' % wpaths[i] for i in idx)

def lockup(tag, c_true, c_mg, c_labs, c_rule, rule=True):
    tr, paths, (lw, lh) = labs[tag]
    scale = WORD_W / lw                 # LABS spans the wordmark exactly
    lh_s  = lh * scale
    rule_y = WORD_H + WORD_H * 0.085
    rule_h = max(6.0, WORD_H * 0.012)
    labs_y = rule_y + rule_h + WORD_H * 0.095
    total  = labs_y + lh_s
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %.0f" '
        'role="img" aria-label="TrueMG Labs">' % (WORD_W, total),
        '<g transform="%s" stroke="none">' % WTR,
        '<g fill="%s">%s</g>' % (c_true, paths_svg(TRUE_I)),
        '<g fill="%s">%s</g>' % (c_mg, paths_svg(MG_I)),
        '</g>',
    ]
    if rule:
        parts.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                     % (rule_y, WORD_W, rule_h, c_rule))
    inner = "".join('<path d="%s"/>' % d for d in paths)
    parts.append('<g transform="translate(0,%.1f) scale(%.6f)">'
                 '<g transform="%s" fill="%s" stroke="none">%s</g></g>'
                 % (labs_y, scale, tr, c_labs, inner))
    parts.append('</svg>')
    return "".join(parts)

INK, PAPER, GOLD, GOLD_D, LINE = "#0A0A0B", "#EDEBE6", "#D8B46A", "#9C7C34", "#33322D"
files = {
    "truemg-labs-onink.svg":        lockup("labs-wide", PAPER, GOLD, PAPER, LINE),
    "truemg-labs-onpaper.svg":      lockup("labs-wide", INK, GOLD_D, INK, "#DAD7D0"),
    "truemg-labs-ink.svg":          lockup("labs-wide", INK, INK, INK, INK, rule=True),
    "truemg-labs-paper.svg":        lockup("labs-wide", PAPER, PAPER, PAPER, PAPER, rule=True),
    "truemg-labs-compact-onink.svg":   lockup("labs-compact", PAPER, GOLD, GOLD, LINE, rule=False),
    "truemg-labs-compact-onpaper.svg": lockup("labs-compact", INK, GOLD_D, GOLD_D, LINE, rule=False),
}
for n, s in files.items():
    open("vec/" + n, "w").write(s)
    print("  %-34s %7d bytes" % (n, len(s)))
