"""Rasterise-free SVG -> print PDF, the same way the shipped set was made.

The original PDFs carry Producer "Skia/PDF" and Creator "Chromium": they were
printed by a headless Chrome at the artwork's own bleed size. This reproduces
that without playwright, which is not installed everywhere this repo is opened.
"""
import os, subprocess, sys, tempfile, shutil

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W_MM, H_MM = 66.0, 36.0          # artwork box = trim + bleed on all four sides

PAGE = ('<html><head><meta charset="utf-8"><style>'
        '@page{size:%gmm %gmm;margin:0}html,body{margin:0;padding:0}'
        'svg{display:block}</style></head><body>%s</body></html>')

def main():
    if not os.path.exists(CHROME):
        sys.exit("Chrome not found at %s — install it or use playwright." % CHROME)
    tmp = tempfile.mkdtemp(prefix="tmglabels-")
    profile = os.path.join(tmp, "cdata")
    made = 0
    try:
        for sub in ("side", "top"):
            out = os.path.join("pdf", sub)
            os.makedirs(out, exist_ok=True)
            for f in sorted(os.listdir(sub)):
                if not f.endswith(".svg"):
                    continue
                svg = open(os.path.join(sub, f), encoding="utf-8").read()
                html = os.path.join(tmp, "p.html")
                open(html, "w", encoding="utf-8").write(PAGE % (W_MM, H_MM, svg))
                pdf = os.path.join(out, f[:-4] + ".pdf")
                subprocess.run(
                    [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                     "--user-data-dir=" + profile, "--no-pdf-header-footer",
                     "--print-to-pdf=" + os.path.abspath(pdf), "file://" + html],
                    check=True, capture_output=True)
                made += 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("%d PDFs at %g x %g mm (trim 60x30 + 3mm bleed)" % (made, W_MM, H_MM))

if __name__ == "__main__":
    main()
