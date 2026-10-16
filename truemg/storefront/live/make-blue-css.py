"""The card tints re-cut for Mila's BLUE ground (chosen 13 Oct 2026).

She published a blue palette and kept it: *"I don't want the eucalyptus. Like
the blue more. The eucalyptus didn't match the logo."* That reasoning is sound —
the mark is #1C8CD0, and a green ground puts the only piece of brand colour on
the page in tension with everything behind it.

The consequence is that the tints had to move. The eucalyptus set spaced five
families AWAY from green and parked the five cofactors on ICE BLUE. On a blue
page those five would have disappeared into the ground — the same failure the
green set had with its sage family, in reverse. So the cofactors move to a
deeper cornflower, a clear step up from the page rather than a match to it.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.path.join(HERE, "customCss-2026-10-12.css")

# the palette Mila published and is keeping
PAGE   = "#F5F8FB"
CARD   = "#FFFFFF"
BORDER = "#CCDDEA"

# name, product URL, card-field tint
PRODUCTS = [
 # repair — blush rose, furthest from the blue ground
 ("GHK-CU",           "/catalog/ghk-cu-hxoc",                    "#F7E7E6"),
 ("BPC-157 + TB-500", "/catalog/bpc-157-tb-500-r20n",            "#F5E3E2"),
 ("KLOW",             "/catalog/klow-snoj",                      "#F3DFDF"),
 # signal — butter
 ("IPAMORELIN",       "/catalog/ipamorelin-5pwi",                "#F7F2E0"),
 ("CJC-1295 + IPA",   "/catalog/cjc-1295-no-dac-ipamorelin-8jay","#F5EFD9"),
 ("TESAMORELIN",      "/catalog/tesamorelin-9ruh",               "#F3ECD3"),
 # metabolic — sage; reads as a real contrast now the page is blue
 ("TMG-2TZ",          "/catalog/tirzepatide-k8ms",               "#E4EFE5"),
 ("TMG-3RT",          "/catalog/tmg-3rt-2k6j",                   "#DDEBDF"),
 ("MOTS-C",           "/catalog/mots-c-atky",                    "#EAF2EA"),
 # neuro — lilac
 ("SEMAX",            "/catalog/semax-m7yh",                     "#EBE5F4"),
 ("SELANK",           "/catalog/selank-nsn7",                    "#E5DEF1"),
 # cofactor — DEEPER cornflower. Was ice blue, which on this page is invisible.
 ("NAD+",             "/catalog/nad-pjb7",                       "#D8E6F7"),
 ("EPITHALON",        "/catalog/epithalon-f9mh",                 "#E0EBF8"),
 ("THYMOSIN ALPHA-1", "/catalog/thymosin-alpha-1-jvna",          "#DCE8F7"),
 ("SS-31",            "/catalog/ss-31-c73t",                     "#D4E2F5"),
 ("VITAMIN B12",      "/catalog/vitamin-b12-vx6i",               "#E4EDF9"),
 # the solution, deliberately plain
 ("TMG-BAC",          "/catalog/bacteriostatic-water-tzbc",      "#FCFDFE"),
]


def build():
    css = open(LIVE).read().rstrip()
    # the no-match fallback: a touch deeper than the page so a missed rule still
    # reads as a field rather than as nothing
    css = css.replace(".lf-card .aspect-square{background:#EDF4FB!important}",
                      ".lf-card .aspect-square{background:#E1EAF4!important}")
    css += "\n" + "\n".join(
        'a[href="%s"] .aspect-square{background:%s!important}' % (u, t)
        for _n, u, t in PRODUCTS)
    return css


if __name__ == "__main__":
    css = build()
    out = os.path.join(HERE, "customCss-blue.css")
    open(out, "w").write(css)
    print("wrote", out, len(css), "chars of 10000")
    print("card rules:", css.count(".aspect-square{background:"))
