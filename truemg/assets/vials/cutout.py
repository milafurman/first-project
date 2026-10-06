import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image

WHITE = 244        # a pixel this bright on every channel is candidate background
RAMP  = 14         # grey levels over which the edge fades in, kills white fringing
BAND  = 3          # how many px inward the soft edge is allowed to reach

def cut(path):
    im  = Image.open(path).convert("RGB")
    a   = np.asarray(im).astype(np.int16)
    minc = a.min(axis=2)

    # candidate background, then keep only what is CONNECTED TO THE BORDER.
    # enclosed white — the label, highlights inside the glass — is never touched.
    cand = minc >= WHITE
    lab, n = ndimage.label(cand)
    border = np.unique(np.concatenate([lab[0,:], lab[-1,:], lab[:,0], lab[:,-1]]))
    border = border[border != 0]
    bg = np.isin(lab, border)

    alpha = np.where(bg, 0.0, 255.0)
    # soften only the few px just inside the subject, ramped on how white they are
    dist = ndimage.distance_transform_edt(~bg)
    edge = (~bg) & (dist <= BAND)
    ramp = np.clip((255 - minc) / RAMP, 0, 1) * 255
    alpha[edge] = np.minimum(alpha[edge], ramp[edge])
    alpha = ndimage.gaussian_filter(alpha, 0.6)

    out = np.dstack([np.asarray(im).astype(np.uint8),
                     np.clip(alpha, 0, 255).astype(np.uint8)])
    return Image.fromarray(out, "RGBA"), bg

def stats(img, bg):
    al = np.asarray(img)[:,:,3]
    return dict(size=img.size,
                bg_pct=round(100*bg.mean(),1),
                opaque_pct=round(100*(al>250).mean(),1),
                soft_px=int(((al>5)&(al<250)).sum()))

if __name__ == "__main__":
    D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
    for f in sys.argv[1:]:
        img, bg = cut("cut/src/"+f)
        img.save("cut/out/"+f)
        print(f"{f:34} {stats(img,bg)}")
