"""Re-space LABS in the TrueMG Labs lockups.

`trace_labs.py` set `scale = WORD_W / lw`, forcing LABS to span the wordmark
exactly. With four narrow glyphs that meant roughly 65000 units of air against an
8000 unit glyph — tracking of about 8em. It read as four loose letters rather than
a word, and sat left of centre because the stretch was anchored at x=0.

This lays the glyphs out from their real bounding boxes: a chosen tracking, then
the run centred under the wordmark.
"""
import json, os, re, subprocess, sys, tempfile

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
WORD_W, WORD_H = 5634, 681
GROUP_OPEN = re.compile(r'<g transform="translate\(([^)]+)\) scale\(([^)]+)\)">')


def group_span(s, m):
    """End index of the <g> that m opens, found by counting nested tags.

    The old pattern ended at the first literal '</g></g>'. That held only while
    the group was two levels deep, which is how trace_labs.py first emitted it.
    This script nests one <g> per glyph, so on a second run the pattern stopped
    short and left the outer '</g>' behind — an unmatched tag, and malformed SVG.
    Counting makes the extraction independent of how deeply nested it already is,
    so re-running is safe.
    """
    depth, i = 1, m.end()
    for t in re.finditer(r'<g\b[^>]*>|</g>', s[m.end():]):
        depth += 1 if t.group(0) != '</g>' else -1
        if depth == 0:
            return m.end() + t.end()
    raise ValueError("unclosed <g>")

LOCKUPS = ["truemg-labs-onink.svg", "truemg-labs-onpaper.svg",
           "truemg-labs-ink.svg", "truemg-labs-paper.svg",
           "truemg-labs-compact-onink.svg", "truemg-labs-compact-onpaper.svg"]


def parse(src):
    """Pull the LABS group out of a lockup: its y, inner transform, and paths."""
    s = open(src).read()
    m = GROUP_OPEN.search(s)
    end = group_span(s, m)
    inner = s[m.end():end - len('</g>')]
    tr = re.search(r'<g transform="([^"]+)"', inner).group(1)
    colour = re.search(r'fill="([^"]+)"', inner).group(1)
    paths = re.findall(r'<path d="([^"]+)"/>', inner)
    unit = abs(float(re.search(r"scale\(([\d.]+)", tr).group(1)))
    top = float(re.search(r"translate\([\d.]+,([\d.]+)\)", tr).group(1))
    return s, m, end, tr, colour, paths, unit, top, float(m.group(1).split(",")[1])


def measure(tr, paths):
    """Glyph boxes, left to right. Each lockup was traced from its own raster, so
    the coordinate space differs per file and these cannot be shared between them."""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><g transform="%s">%s</g></svg>'
                % (tr, "".join('<path d="%s"/>' % d for d in paths)))
        tmp = f.name
    try:
        out = subprocess.run(["node", "_measure_glyphs.mjs", tmp],
                             capture_output=True, text=True, check=True).stdout
    finally:
        os.unlink(tmp)
    boxes = json.loads(out)
    order = sorted(range(len(boxes)), key=lambda i: boxes[i]["x"])
    return [paths[i] for i in order], [boxes[i] for i in order]


def rebuild(src, dst, cap_ratio, tracking_em):
    s, m, end, tr, colour, paths, unit, top, labs_y = parse(src)
    paths, boxes = measure(tr, paths)
    cap = max(b["h"] for b in boxes)
    scale = cap_ratio * WORD_H / (cap * unit)
    gap = tracking_em * cap

    placed, cursor = [], 0.0
    for d, b in zip(paths, boxes):
        placed.append('<g transform="translate(%.1f,0)"><path d="%s"/></g>' % (cursor - b["x"], d))
        cursor += b["w"] + gap
    width = (cursor - gap) * unit * scale          # drop the trailing gap

    g = ('<g transform="translate(%.1f,%.1f) scale(%.6f)">'
         '<g transform="%s" fill="%s" stroke="none">%s</g></g>'
         % ((WORD_W - width) / 2, labs_y, scale, tr, colour, "".join(placed)))
    out = s[:m.start()] + g + s[end:]

    # a taller LABS overruns the inherited viewBox and gets clipped at the foot
    need = labs_y + scale * top + 14
    vb = re.search(r'viewBox="0 0 (\d+) ([\d.]+)"', out)
    if need > float(vb.group(2)):
        out = out.replace(vb.group(0), 'viewBox="0 0 %s %.0f"' % (vb.group(1), need))
    open(dst, "w").write(out)
    return width


if __name__ == "__main__":
    cap, trk = float(sys.argv[1]), float(sys.argv[2])
    targets = LOCKUPS if "--all" in sys.argv[3:] else ["truemg-labs-onpaper.svg"]
    for f in targets:
        dst = sys.argv[3] if targets == ["truemg-labs-onpaper.svg"] and len(sys.argv) > 3 else f
        w = rebuild(f, dst, cap, trk)
        print("  %-36s LABS %.0f (%.0f%% of wordmark)" % (dst, w, 100 * w / WORD_W))
