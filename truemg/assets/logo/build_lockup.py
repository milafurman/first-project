"""Compose the header lockup: Gila mark beside the TrueMG Labs wordmark.

The storefront's header logo is an upload in the Lapis admin, which this
integration cannot reach. The lockup therefore ships as an SVG served off the
public repository and swapped in with CSS `content: url(...)`.
"""
import os, re, shutil, subprocess

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
inline_mark, _ = inner("truemg-mark-inline.svg")   # same drawing, lighter trace
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

def web(true_fill, accent, rule, out):
    """The site header: wordmark and LABS, no Gila mark.

    Mila's instruction is that the lizard appears in exactly two places, the
    browser tab and the vial, and nowhere on the site itself. This is also what
    makes the header affordable: the storefront has no logo copy key, so the
    file ships inlined as a base64 data URI inside customCss, and customCss is
    capped at 10,000 characters. With the mark it minifies to 9,464 characters
    of base64 and the rest of the CSS no longer fits. Without it, it fits with
    room to spare."""
    l = labs.replace(BLUE, accent).replace(INK, true_fill).replace("#D8DEE9", rule)
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
         'role="img" aria-label="TrueMG Labs">%s</svg>' % (lvb[2], H, l))
    open(out, "w").write(s)
    print("%-34s %6.0f x %4.0f  %5d bytes" % (out, lvb[2], H, len(s)))

def inline_svg(out):
    """The header lockup again, built from the lighter trace, for customCss.

    The storefront's Logo slot is an upload, and when that upload is in place
    this file is not needed. It exists because customCss is the only route this
    integration can drive itself, and there the budget is 10,000 characters:
    the full-fidelity lockup costs 9,464 of base64 and leaves no room for the
    rest of the stylesheet, while this one costs 7,288 and leaves 1,226 spare.
    """
    m = inline_mark.replace(INK, BLUE)
    l = labs.replace(BLUE, BLUE).replace(INK, INK).replace("#D8DEE9", "#D8DEE9")
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
         'role="img" aria-label="TrueMG Labs">'
         '<g transform="scale(%.6f)">%s</g>'
         '<g transform="translate(%.0f,%.0f)">%s</g></svg>'
         % (W, MARK, S, m, MARK + GAP, DY, l))
    open(out, "w").write(s)
    print("%-34s %6.0f x %4.0f  %5d bytes" % (out, W, H, len(s)))

# with the mark: for print, Canva, and anywhere that is not the storefront
svg(BLUE,    INK,     BLUE,    "#D8DEE9", "truemg-lockup-header.svg")
svg("#FFFFFF","#FFFFFF","#65A0F5","#2B3344", "truemg-lockup-onink.svg")
# without it: the storefront header and footer
web(INK,      BLUE,    "#D8DEE9", "truemg-lockup-web.svg")
web("#FFFFFF","#65A0F5","#2B3344", "truemg-lockup-web-onink.svg")
# and the budget cut, for inlining
inline_svg("truemg-lockup-inline.svg")


# The .min.svg beside each lockup is what actually ships: it is base64'd into
# customCss, where the budget is 10,000 characters. Minifying was a command
# somebody typed by hand, so a rebuilt lockup and its .min could disagree —
# and did, for as long as the header carried the old Gila drawing. svgo does
# the work because a hand-rolled regex once produced a file that rendered
# nothing at all; this only automates *calling* it.
SVGO = shutil.which("svgo") or shutil.which("npx")
for name in ("truemg-lockup-header", "truemg-lockup-onink",
             "truemg-lockup-web", "truemg-lockup-web-onink",
             "truemg-lockup-inline"):
    src, out = name + ".svg", name + ".min.svg"
    if not SVGO:
        print("  ! svgo not found - %s is now STALE. `npm i -g svgo`, then re-run." % out)
        continue
    cmd = [SVGO] + (["-y", "svgo"] if SVGO.endswith("npx") else [])
    subprocess.run(cmd + ["--precision=0", "--quiet", "-i", src, "-o", out], check=True)
    b64 = (os.path.getsize(out) + 2) // 3 * 4
    print("  %-30s %5d bytes -> %5d base64 chars" % (out, os.path.getsize(out), b64))
