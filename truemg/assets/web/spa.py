"""Stand the vials on the spa counter.

`scene.py` builds a room from scratch in code. This does the opposite: it takes
a real photographic plate — `plate-spa.jpg`, generated in Canva and approved by
Mila — and composites the actual product art onto it. The division is
deliberate. An image model makes a convincing room and a terrible vial, because
it invents label text; the label text is the one thing on this site that has to
be exactly right, both because it is the brand and because "NOT FOR HUMAN
CONSUMPTION / RESEARCH USE ONLY" is a compliance line, not a design element.
So the model gets the room and never touches the product.

Two things have to be true for a composite to read as a photograph:

  * the bottles have to sit on the counter's actual plane, at its actual
    perspective. The plane here was measured off the plate, not guessed — see
    FRONT_EDGE and HORIZON_Y below.
  * the background has to defocus the way a real lens does, which is by
    DISTANCE, not by height in the frame. A flat gaussian over the top half is
    the giveaway that something was blurred in post.

Run from this directory.
"""
import os

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage

import scene as S

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)

PLATE = "plate-spa.jpg"

# --- framing ----------------------------------------------------------------
# A crop is not a cosmetic choice here, it is the fix for the scale problem.
# The plate is an architectural wide shot, and a wide shot says the camera is
# across the room — which makes a hero-sized vial physically impossible and is
# most of why the first composite read as a collage. Cropping in says the
# camera is close, and a close camera makes the same bottles reasonable. The
# measured plane below stays in ORIGINAL plate coordinates and is transformed
# through this crop in code, so the geometry cannot drift out of step with the
# framing the way hand-copied numbers would.
CROP = (500, 300, 1389, 800)               # left, top, right, bottom
OUT_W = 1680

# --- the counter plane, measured off the plate ------------------------------
# The front-top edge of the counter, found by gradient search along each column
# (the vertical front face is darker than the lit top, so the edge is a clean
# bright-to-dark fall). A straight edge in 3D projects to a straight line, and
# this one fits to within a few pixels across 850px of frame.
FRONT_M, FRONT_C = 0.262, 540.0            # y = Mx + C

# Where the counter's edge and the lit niche above it converge. Everything on
# this plane scales with distance from that line, which is what stops the
# bottles reading as four stickers at four arbitrary sizes.
HORIZON_Y = 471.0

# The bottles stand back from the front edge by this much of the counter's
# visible depth — far enough not to look like they are about to fall off.
SETBACK = 0.34
BASE_M, BASE_C = 0.222, 529.0              # the line their bases sit on

# Scale: a vial's height in pixels is SCALE x its distance below the horizon.
#
# Knowingly generous, and worth being honest about. A 45mm vial on a reception
# counter this deep would be about fifteen pixels tall and completely useless
# as a hero. The perspective between the four bottles is correct — they scale
# against each other and against the counter exactly as the plane demands —
# but the group as a whole is larger than physics would put it. That is an
# ordinary product-photography cheat and it survives because the background is
# defocused: a soft background reads as distant, and a distant background
# stops the eye auditing absolute scale.
SCALE = 0.92

# --- defocus ----------------------------------------------------------------
# Peak blur radius, at the far wall. The near edge of the counter stays sharp.
# Swept at 6 / 10 / 16: 16 destroys the orchids, 10 softens the canopy more
# than asked, 6 leaves the top leaves sharp enough to compete with the product.
# 8 is the dial — turn it, nothing else in the frame moves.
BLUR_MAX = 13.0
BLUR_LEVELS = 12

# The four vials, left to right. No per-bottle size, on purpose.
#
# An earlier version carried a height ratio per name — 0.715, 0.82, 1.0, 0.785
# — inherited from older code and never checked. It has no basis: all four
# sprites are 652x1589 pixels. They are the same vial photographed once, with
# a different label. Making them different sizes was invention, and it was the
# single loudest thing wrong with the composite.
CAST = ["nad", "tmg-3rt", "ghk-cu", "bpc-157-tb-500"]

# They stand in a row at CONSTANT DEPTH, which is what keeps them identical in
# size. On a receding plane a line of constant image-y is a line of constant
# distance from the camera, so a horizontal row sits flat on the counter AND
# renders every bottle at the same height. A row following the counter's own
# diagonal would be equally correct and would vary them by about 28%, which is
# exactly the thing being fixed.
ROW_Y = 809.0
ROW_X = (661, 882, 1102, 1323)      # inside the band where ROW_Y is on the top


def depth_blur(im, horizon):
    """Defocus by distance, not by height in the frame.

    On a ground plane receding from the camera, distance goes as
    1 / (y - horizon): the counter's near edge is close, its far end is not,
    and the wall behind it is further still. Blurring on that curve puts the
    softest part of the picture where the leaves are and holds the near edge
    sharp, without anyone having to mask anything by hand.

    Built as a stack of progressively blurred copies cross-faded by the depth
    map, because PIL has no per-pixel-radius blur. Twelve steps is enough that
    the banding is invisible at this size.
    """
    W, H = im.size
    yy = np.mgrid[0:H, 0:W][0].astype(float)

    far = 1.0 / np.maximum(yy - horizon, 1.0)            # small = near
    near = 1.0 / max(H - horizon, 1.0)                   # the bottom of frame
    d = np.clip((far - near) / (far.max() - near), 0, 1) ** 0.55
    d[yy <= horizon] = 1.0                               # the wall and the canopy
    d = ndimage.gaussian_filter(d, 12)                     # no hard edge at the horizon

    out = np.asarray(im).astype(float)
    for i in range(1, BLUR_LEVELS + 1):
        lo, hi = (i - 1) / BLUR_LEVELS, i / BLUR_LEVELS
        layer = np.asarray(im.filter(ImageFilter.GaussianBlur(BLUR_MAX * hi))).astype(float)
        w = np.clip((d - lo) / (hi - lo), 0, 1) * np.clip((hi + 1 / BLUR_LEVELS - d) * BLUR_LEVELS, 0, 1)
        out = out * (1 - w[..., None]) + layer * w[..., None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def relight(v, rim=1.0, blur=0.0):
    """Light the bottle with the room's light instead of the studio's.

    This is the difference between a composite and a collage. The vial PNGs
    were shot flat on white seamless: even frontal light, bright white faces,
    hard edges. The plate is lit the opposite way — a sheer curtain behind and
    to the left, throwing warm light toward the camera. Dropping one into the
    other and tinting it warm does not work, and should not: a frontlit object
    with a warm filter on it is still a frontlit object, and the eye reads the
    mismatch instantly even when it cannot name it.

    Four moves, in the order light actually does them:

      1. KNOCK THE KEY DOWN. Nothing in this room is lit from the camera, so
         the bright frontal faces lose most of their brightness. This alone
         does more than everything else combined.
      2. RIM THE LEFT EDGE. A backlight wraps the silhouette facing it. Taken
         from the alpha channel shifted right and subtracted, so the band
         follows the real outline including the cap and the crimp.
      3. FILL FROM THE RIGHT. The lit niche is a long warm source on that
         side, so the shadow side is not black, it is bronze.
      4. SIT IT IN THE AIR. Match the local defocus and drop the contrast to
         the plate's, because a studio curve against a hazy room is its own
         kind of cut-out.

    The brand blue is held through all of it, as everywhere else.
    """
    a = np.asarray(v.getchannel("A")).astype(float) / 255.0
    px = np.asarray(v.convert("RGB")).astype(float)
    r_, g_, b_ = px[:, :, 0], px[:, :, 1], px[:, :, 2]
    brand = (b_ - r_ > 45) & (b_ - g_ > 25) & (b_ > 90)
    hold = ndimage.gaussian_filter(brand.astype(float), 1.2)[..., None]

    lit = px * 0.78                                        # 1. kill the studio key
    lit += (np.array((120, 104, 86), float) - lit) * 0.16  # ambient, warm not grey

    # 1b. ACROSS the body, not just at its edge. This was the piece missing
    # after the rim went in: a rim alone puts a bright line on the silhouette
    # and leaves everything inside it evenly lit, which is a studio softbox,
    # not a window. One source to the left means the whole bottle — label
    # included — falls off continuously from left to right, and a little from
    # top to bottom. Without it the label reads as a flat white rectangle
    # pasted on a lit scene, because that is exactly what it is.
    H0, W0 = px.shape[:2]
    gy, gx = np.mgrid[0:H0, 0:W0]
    across = 1.0 + 0.26 * (0.5 - gx / max(W0 - 1, 1))      # window is to the left
    down = 1.0 + 0.07 * (0.5 - gy / max(H0 - 1, 1))        # and a little above
    lit *= (across * down)[..., None]

    H_, W_ = a.shape
    sh = max(2, int(W_ * 0.034))
    left = np.clip(a - np.pad(a, ((0, 0), (sh, 0)))[:, :W_], 0, 1)      # 2. the wrap
    left = ndimage.gaussian_filter(left, W_ * 0.0055) * rim
    lit += (np.array((255, 238, 208), float) - lit) * np.clip(left * 1.25, 0, 0.66)[..., None]

    right = np.clip(a - np.pad(a, ((0, 0), (0, sh)))[:, sh:], 0, 1)     # 3. the niche
    right = ndimage.gaussian_filter(right, W_ * 0.014)
    lit += (np.array((236, 196, 142), float) - lit) * np.clip(right * 0.80, 0, 0.38)[..., None]

    px = px * hold * 0.45 + lit * (1 - hold * 0.45)
    rgb = Image.fromarray(px.clip(0, 255).astype(np.uint8))
    rgb = ImageEnhance.Contrast(rgb).enhance(0.88)         # 4. the plate's curve
    out = Image.merge("RGBA", (*rgb.split(), v.getchannel("A")))
    return out.filter(ImageFilter.GaussianBlur(blur)) if blur else out


def view():
    """The crop, and the transform that carries the measured plane through it."""
    k = OUT_W / (CROP[2] - CROP[0])
    front = lambda x: (FRONT_M * (x / k + CROP[0]) + FRONT_C - CROP[1]) * k
    base = lambda x: (BASE_M * (x / k + CROP[0]) + BASE_C - CROP[1]) * k
    return k, front, base, (HORIZON_Y - CROP[1]) * k


def settle(im, horizon, row=None):
    """Take the room down so the product can come up.

    Nurish's hero works because the vials are dark teal glass on a dark, nearly
    monochrome background: the product is the only contrast in the frame. These
    vials are clear glass with white labels, and a bright cream room gives them
    almost nothing to separate against. Since the glass cannot be changed, the
    room is: pulled down, pulled toward neutral, and pulled down harder the
    further it is from the camera, which is also what a real exposure set for
    the product would do to a background.
    """
    a = np.asarray(im).astype(float)
    H, W = a.shape[:2]
    yy = np.mgrid[0:H, 0:W][0].astype(float)
    r = ROW_Y if row is None else row
    far = np.clip((r - yy) / max(r - horizon, 1.0), 0, 1) ** 0.8
    # Exposure only. An earlier pass also pulled 20% of the saturation out,
    # which separated the product but drained exactly the warmth this plate was
    # chosen for. Stopping the light down is what a camera exposing for the
    # product would do; desaturating is not, and it showed.
    k = 1.0 - 0.22 * far
    return Image.fromarray((a * k[..., None]).clip(0, 255).astype(np.uint8))


# Where the bottle is glass rather than cap or label, as fractions of sprite
# height. All four sprites are the same photograph, so one set of bands serves
# all of them. The upper band deliberately starts inside the stopper: the
# transmission below is driven by brightness, so the dark stopper keeps itself
# opaque without needing its own boundary.
GLASS_BANDS = ((0.18, 0.395), (0.86, 1.0))


def transmit(v, under):
    """Let the room show through the glass.

    This is the one that mattered. The sprite is 92% fully opaque: it was
    photographed on a white background and the white got baked into the glass,
    so the clear shoulder arrives as a solid grey panel. Composited over a
    room, nothing behind the bottle shows through it — and clear glass that
    does not transmit is the loudest possible signal that something was pasted
    on top of a picture rather than photographed in it. No amount of grading,
    shadow or reframing fixes it, which is why none of those passes did.

    The inversion is approximate and has to be: the plate behind the glass was
    white, so a pixel is roughly 255 x transmission + the glass's own
    scattering, and one equation cannot recover two unknowns. But brightness is
    a good enough proxy — where the glass let the white through it reads near
    white, and where it has structure (the neck ring, the meniscus, the
    stopper, the dark edges that give it its shape) it reads dark. So
    brightness drives transmission and the structure survives untouched.

    What shows through is blurred a little further than the plate behind it,
    because curved glass is a bad lens.
    """
    a = np.asarray(v).astype(float)
    H_, W_ = a.shape[:2]
    yy = np.mgrid[0:H_, 0:W_][0] / max(H_ - 1, 1)

    band = np.zeros((H_, W_))
    for lo, hi in GLASS_BANDS:
        band[(yy >= lo) & (yy <= hi)] = 1.0
    band = ndimage.gaussian_filter(band, H_ * 0.012)       # no hard seam at the label

    lum = a[:, :, :3].mean(axis=2)
    t = np.clip((lum - 120.0) / 115.0, 0, 1) ** 1.1        # bright glass transmits
    t = t * band * 0.80

    seen = np.asarray(under.filter(ImageFilter.GaussianBlur(max(1.0, W_ * 0.010)))).astype(float)
    a[:, :, :3] = seen * t[..., None] + a[:, :, :3] * (1 - t[..., None])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def mirror(v, h):
    """The bottle in the stone.

    scene.py's version is a dim ghost at a fixed 3.5px blur, which was written
    for bottles a third of this size and reads as a smudge at this one. A honed
    stone counter is not a mirror, but it is reflective enough that four glass
    bottles standing on it HAVE to appear in it, and the absence of that is one
    of the things that makes them look placed rather than photographed.

    Foreshortened, because the surface is seen at a grazing angle, and blurred
    progressively with distance from the contact point, because the stone
    scatters more the further the light has to travel across it.
    """
    r = v.transpose(Image.FLIP_TOP_BOTTOM)
    r = r.resize((r.width, max(2, int(h * 0.46))), Image.LANCZOS)
    H_ = r.height
    a = np.asarray(r.getchannel("A")).astype(float)
    a *= (np.linspace(1, 0, H_)[:, None] ** 1.35) * 0.44
    r.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8)))

    out = Image.new("RGBA", r.size, (0, 0, 0, 0))
    steps = 5
    for i in range(steps):
        lo, hi = int(H_ * i / steps), int(H_ * (i + 1) / steps)
        if hi <= lo:
            continue
        band = r.crop((0, lo, r.width, hi)).filter(
            ImageFilter.GaussianBlur(h * 0.006 + h * 0.022 * (i / steps)))
        out.paste(band, (0, lo))
    return out


def place(scene, name, cx, k, horizon):
    """One bottle, with its shadow, standing on the row."""
    base = ROW_Y
    h = max(8, int(SCALE * (base - horizon)))

    v = S.vial(name)
    v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)
    # defocus to match the plane the bottle stands on — nearer than the wall
    # behind it, so a fraction of the plate's blur at this depth
    # The curtain is off-frame left, so the nearer a bottle is to it the harder
    # it is rimmed. Four identically lit bottles is a product sheet; a row lit
    # by one window is a photograph.
    near_window = 1.0 - (cx - ROW_X[0]) / max(ROW_X[-1] - ROW_X[0], 1) 
    v = relight(v, rim=0.72 + 0.55 * near_window,
                blur=max(0.0, BLUR_MAX * k * 0.05 * (1 - (base - horizon) / 620.0)))
    # take the knife-edge off the cut-out: a real lens has no perfect edge
    av = v.getchannel("A").filter(ImageFilter.GaussianBlur(max(0.6, h * 0.0022)))
    v.putalpha(av)

    x, y = int(cx - v.width / 2), int(base - h)

    # The key light is the sheer curtain on the left, so shadows fall right and
    # toward the camera. Length grows with distance from the window, the way
    # they do in the plate's own leaf shadows.
    # The curtain is a hard, low source, so the shadows in this room are long
    # and definite — look at what the orchid throws on the wall. The first pass
    # used scene.py's soft studio shadow and the bottles floated because of it.
    lean = 1.35 + (cx - ROW_X[0]) / 2000.0
    for length, blur, n in ((0.95, 0.055, 2), (0.34, 0.016, 3)):
        cs, pad = S.cast_shadow(v, length, lean, max(4, int(h * blur)))
        for _ in range(n):                            # deepen: one pass is too pale
            scene.alpha_composite(cs, (x - pad, int(base) - pad))

    scene.alpha_composite(mirror(v, h), (x, int(base)))
    cp, band = S.contact(v, max(4, int(h * 0.018)))
    for _ in range(2):
        scene.alpha_composite(cp, (x, int(base) - band))
    under = scene.crop((x, y, x + v.width, y + v.height)).convert("RGB")
    scene.alpha_composite(transmit(v, under), (x, y))


def compose(out="spa-hero.jpg", product=True):
    """The room, with the bottles on it or without.

    The empty version is not a debug view. The vial art is a flat mockup shot
    dead-on against white, which is right for a product tile and wrong for a
    photographic hero, so the room on its own — headline over the clear left
    third, product left to the tiles where flat lighting is expected — is a
    real option rather than a fallback. It is generated here rather than by
    hand so it cannot drift from the framing and defocus the composite uses.
    """
    plate = Image.open(PLATE).convert("RGB").crop(CROP)
    k, _, _, horizon = view()
    plate = plate.resize((OUT_W, int(plate.height * k)), Image.LANCZOS)
    scene = settle(depth_blur(plate, horizon), horizon).convert("RGBA")
    for name, cx in (zip(CAST, ROW_X) if product else ()):
        place(scene, name, cx, k, horizon)
    scene.convert("RGB").save(out, quality=90, optimize=True)
    print(f"  {out:24s} {scene.width}x{scene.height}  {os.path.getsize(out) // 1024} KB")


# The hero background is a different job from the composite above. Nothing
# stands on the counter, so the framing does not have to keep a row of bottles
# on a measured plane — it only has to be a room with somewhere quiet for a
# headline to sit. So it is cropped wider and shallower, to the shapes the
# storefront already serves.
HERO = (
    ("hero-spa.jpg",        (0, 105, 1680, 859), (2560, 1150)),   # desktop
    ("hero-spa-mobile.jpg", (250, 0, 930, 944),  (1080, 1500)),   # portrait
)


def hero_media(src="hero-media.webp", out="hero-media-warm.webp"):
    """The floating vial cluster, graded to sit over the warm room.

    This one is a much easier problem than the row on the counter, because it
    floats. Nothing has to agree with a measured surface, a horizon or a
    reflection — it only has to be lit like the room it hangs in front of. So
    the same three moves as relight(): the studio key comes down, warm ambient
    goes in, and the whole cluster falls off from left to right because the
    window is on the left.

    The soft white halo baked around the group is the one thing that cannot
    stay. On white it is invisible; over a warm room it is a grey fog with a
    bottle-shaped hole in it. It lives in the partially transparent pixels, so
    pushing those toward either fully on or fully off removes it without
    touching the bottles themselves.
    """
    im = Image.open(src).convert("RGBA")
    a = np.asarray(im).astype(float)
    rgb, al = a[:, :, :3], a[:, :, 3]

    H0, W0 = rgb.shape[:2]
    gx = np.mgrid[0:H0, 0:W0][1] / max(W0 - 1, 1)
    lit = rgb * 0.80
    lit += (np.array((124, 108, 88), float) - lit) * 0.15
    lit *= (1.0 + 0.22 * (0.5 - gx))[..., None]

    # kill the halo: harden the soft shroud, keep the anti-aliased edge
    al = np.clip((al / 255.0 - 0.34) / 0.52, 0, 1) ** 0.85 * 255.0

    Image.fromarray(np.dstack([lit, al]).clip(0, 255).astype(np.uint8)).save(
        out, quality=88, method=6)
    print(f"  {out:24s} {W0}x{H0}  {os.path.getsize(out) // 1024} KB")


def hero_backgrounds():
    """The room on its own, at the sizes the storefront's hero keys expect."""
    src = Image.open(PLATE).convert("RGB")
    for out, box, size in HERO:
        im = src.crop(box)
        k = size[0] / im.width
        im = im.resize(size, Image.LANCZOS)
        horizon = (HORIZON_Y - box[1]) * k
        im = settle(depth_blur(im, horizon), horizon, row=size[1] * 0.86)
        im.save(out, quality=86, optimize=True)
        print(f"  {out:24s} {size[0]}x{size[1]}  {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    compose("spa-hero.jpg")
    compose("spa-plate-hero.jpg", product=False)
    hero_backgrounds()
    hero_media()
