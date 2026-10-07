"""Compose the header lockup: Gila mark beside the TrueMG Labs wordmark.

The storefront's header logo is an upload in the Lapis admin, which this
integration cannot reach. The lockup therefore ships as an SVG served off the
public repository and swapped in with CSS `content: url(...)`.
"""
import os, re

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

INK, BLUE = "#0A0A0B", "#2365CD"

def inner(path):
    """Everything between the <svg> wrapper, plus the viewBox."""
    s = open(path).read()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    body = re.sub(r'^.*?<svg[^>]*>', '', s, flags=re.S)
    body = re.sub(r'</svg>\s*$', '', body, flags=re.S)
    return body, vb

mark, mvb = inner("truemg-mark-ink.svg")
labs, lvb = inner("truemg-labs-onpaper.svg")

# the mark is drawn in ink; on the header it is the brand blue
mark = mark.replace(INK, BLUE)
# the Labs lockup ships gold-on-paper: gold is the accent slot, ink the text slot
labs = labs.replace("#9C7C34", BLUE).replace("#DAD7D0", "#D8DEE9")

H    = lvb[3]                   # 1024 — the wordmark lockup's own height
MARK = H * 1.16                 # the head reads small at the lockup's height, so it
                                # runs slightly taller and the wordmark centres to it
GAP  = int(H * 0.17)
S    = MARK / mvb[3]            # scale the 1600-unit mark to the mark height
DY   = (MARK - H) / 2           # drop the wordmark to sit on the mark's centre line
W    = MARK + GAP + lvb[2]

def svg(mark_fill, true_fill, accent, rule, out):
    m = mark.replace(BLUE, mark_fill)
    l = labs.replace(BLUE, accent).replace(INK, true_fill).replace("#D8DEE9", rule)
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
         'role="img" aria-label="TrueMG Labs">'
         '<g transform="scale(%.6f)">%s</g>'
         '<g transform="translate(%.0f,%.0f)">%s</g></svg>'
         % (W, MARK, S, m, MARK + GAP, DY, l))
    open(out, "w").write(s)
    print("%-34s %6.0f x %4.0f  %5d bytes" % (out, W, H, len(s)))

svg(BLUE,    INK,     BLUE,    "#D8DEE9", "truemg-lockup-header.svg")
svg("#FFFFFF","#FFFFFF","#65A0F5","#2B3344", "truemg-lockup-onink.svg")
