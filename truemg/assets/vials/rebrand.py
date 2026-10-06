import sys, os
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter

BRAND_BLUE = np.array([40,102,205], float)   # #2866CD — the decided brand accent
LIZARD_BOX = (725, 1185, 950, 1420)         # old mark on the 2000px label, measured

def blue_mask(a):
    r,g,b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    # the brand blue is strongly B-dominant; white, black and grey are not
    return (b - r > 45) & (b - g > 25) & (b > 90)

def rebrand(path, mark_img):
    im  = Image.open(path).convert("RGBA")
    a   = np.asarray(im).astype(np.uint8).copy()
    rgb = a[:,:,:3]
    blue = blue_mask(rgb)

    x0,y0,x1,y1 = LIZARD_BOX
    inbox = np.zeros(blue.shape, bool); inbox[y0:y1, x0:x1] = True

    # 1. recolour the blue TYPE (product name, the MG) to the paper-ground gold,
    #    keeping each pixel's own lightness so anti-aliased edges stay smooth
    type_blue = blue & ~inbox
    if type_blue.any():
        lum = rgb[type_blue].astype(float).max(axis=1, keepdims=True) / 255.0
        a[:,:,:3][type_blue] = np.clip(BRAND_BLUE * (0.55 + 0.45*lum), 0, 255).astype(np.uint8)

    # 2. erase the old dragon. The label carries a soft vertical gradient, so a flat
    #    median fill leaves a visible patch — reconstruct it row by row instead.
    patch = rgb[y0:y1, x0:x1].copy()
    oldmark = blue[y0:y1, x0:x1]
    if oldmark.any():
        grow = ndimage.binary_dilation(oldmark, iterations=4)
        clean = ~grow
        glob = (np.median(patch[clean].reshape(-1,3), axis=0)
                if clean.any() else np.array([246,246,247], float))
        for yy in range(patch.shape[0]):
            row_clean = clean[yy]
            if not grow[yy].any():
                continue
            src = patch[yy][row_clean]
            fill = np.median(src, axis=0) if src.shape[0] >= 8 else glob
            patch[yy][grow[yy]] = fill.astype(np.uint8)
        # feather the seam so the reconstruction does not read as a rectangle
        sm = np.asarray(Image.fromarray(patch).filter(ImageFilter.GaussianBlur(2.5))).astype(float)
        w  = ndimage.gaussian_filter(grow.astype(float), 3.0)[..., None]
        patch = np.clip(patch*(1-w) + sm*w, 0, 255).astype(np.uint8)
        a[y0:y1, x0:x1, :3] = patch

    # 3. drop the new mark into the space the old one occupied
    out = Image.fromarray(a, "RGBA")
    bw, bh = x1-x0, y1-y0
    m = mark_img.resize((int(bw*0.94), int(bh*0.94)), Image.LANCZOS)
    out.alpha_composite(m, (x0 + (bw-m.width)//2, y0 + (bh-m.height)//2))
    return out

if __name__ == "__main__":
    D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
    mark = Image.open("mark-blue-600.png").convert("RGBA")
    os.makedirs("cut/brand", exist_ok=True)
    for f in sys.argv[1:]:
        rebrand("cut/out/"+f, mark).save("cut/brand/"+f)
        print("rebranded", f)
