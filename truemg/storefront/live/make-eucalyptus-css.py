"""Build the eucalyptus stylesheet from the mock Mila approved."""
import re, json

LIVE = "truemg/storefront/live/customCss-2026-10-12.css"
live = open(LIVE).read().rstrip()

# the tints, lifted straight out of the approved sheet's generator
PRODUCTS = [
 ("GHK-CU",            "/catalog/ghk-cu-hxoc",                   (245,230,229)),
 ("BPC-157 + TB-500",  "/catalog/bpc-157-tb-500-r20n",           (243,227,226)),
 ("KLOW",              "/catalog/klow-snoj",                     (241,224,224)),
 ("IPAMORELIN",        "/catalog/ipamorelin-5pwi",               (246,242,226)),
 ("CJC-1295 + IPA",    "/catalog/cjc-1295-no-dac-ipamorelin-8jay",(244,240,221)),
 ("TESAMORELIN",       "/catalog/tesamorelin-9ruh",              (242,238,218)),
 ("TMG-2TZ",           "/catalog/tirzepatide-k8ms",              (227,238,228)),
 ("TMG-3RT",           "/catalog/tmg-3rt-2k6j",                  (222,235,223)),
 ("MOTS-C",            "/catalog/mots-c-atky",                   (231,240,231)),
 ("SEMAX",             "/catalog/semax-m7yh",                    (234,230,242)),
 ("SELANK",            "/catalog/selank-nsn7",                   (230,227,240)),
 ("NAD+",              "/catalog/nad-pjb7",                      (225,236,245)),
 ("EPITHALON",         "/catalog/epithalon-f9mh",                (231,239,246)),
 ("THYMOSIN ALPHA-1",  "/catalog/thymosin-alpha-1-jvna",         (228,237,245)),
 ("SS-31",             "/catalog/ss-31-c73t",                    (222,234,244)),
 ("VITAMIN B12",       "/catalog/vitamin-b12-vx6i",              (234,241,247)),
 ("TMG-BAC",           "/catalog/bacteriostatic-water-tzbc",     (253,253,252)),
]

def wash(t, amt=0.0):           # the card field is a paler wash of the label tint
    return "#%02X%02X%02X" % tuple(int(c + (255 - c) * amt) for c in t)

css = live

# 1. the section bands: blue-white and cream -> eucalyptus and a green-neutral
css = css.replace(".lf-section-howItWorks{background-color:#F3F6FC",
                  ".lf-section-howItWorks{background-color:#E8EEE8")
css = css.replace(".lf-section-faq{background-color:#F8F6F1",
                  ".lf-section-faq{background-color:#F2F5F1")
css = css.replace(".lf-section-ctaBanner{background-color:#EDF2FB",
                  ".lf-section-ctaBanner{background-color:#DBE4DB")
# 2. the two dark blocks: navy -> the mock's green-black
css = css.replace(".lf-section-quality{background-color:#0A192F!important}",
                  ".lf-section-quality{background-color:#202A22!important}")
css = css.replace("footer{background-color:#0A192F!important",
                  "footer{background-color:#202A22!important")
# 3. header and rules pick up the warm-green neutral
css = css.replace("header.glass{background:#fff!important;border-bottom:1px solid #E8EBF0!important}",
                  "header.glass{background:#FCFDFB!important;border-bottom:1px solid #DCE5DC!important}")
# 4. the pale-blue panel inside the quality section
css = css.replace(".max-w-5xl .rounded-2xl.text-center{background-color:#EDF4FB!important",
                  ".max-w-5xl .rounded-2xl.text-center{background-color:#EDF2ED!important")
# 5. the fallback card field: no longer blue, so a URL change degrades to green
css = css.replace(".lf-card .aspect-square{background:#EDF4FB!important}",
                  ".lf-card .aspect-square{background:#F1F5F1!important}")
# 6. hover glow: keep the brand blue, it is still the accent
css = css.replace(".lf-section-howItWorks .rounded-2xl:hover{border-color:#1C8CD0",
                  ".lf-section-howItWorks .rounded-2xl:hover{border-color:#1C8CD0")

# 7. one field per compound, keyed on the product URL
rules = "\n".join('a[href="%s"] .aspect-square{background:%s!important}' % (h, wash(t))
                  for _n, h, t in PRODUCTS)
css = css + "\n" + rules

open("/private/tmp/claude-501/-Users-milafurman-first-project--claude-worktrees-sad-noether-552cd4/69452b06-3ae7-4a8a-bfd6-f3f97ae74acf/scratchpad/euc.css","w").write(css)
print("chars:", len(css), "of 10000")
print()
print("--- the 17 card fields ---")
for n,h,t in PRODUCTS:
    print("  %-20s %s" % (n, wash(t)))
print()
print("--- leftover old colours that should be gone ---")
for bad in ("#F3F6FC","#F8F6F1","#EDF2FB","#0A192F","#EDF4FB","#E8EBF0"):
    print("  %-10s %s" % (bad, "STILL PRESENT" if bad in css else "gone"))
