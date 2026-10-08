"""Stand the vials in a warm room instead of floating them on a gradient.

The cut-outs read as a catalogue sheet: no surface, no light source, nothing
holding them anywhere. A competitor's shop felt like wellness rather than a
lab purely because the same kind of bottle was photographed on a sunlit stone
counter. The product was not the difference, the room was.

So the bottle stays exactly as it is — clear glass, brand-blue crimp, the
label as printed — and the warmth comes from everything around it. Against a
warm ground the blue reads as the one deliberate accent in the frame, which
it never does against white.

There is no new photography here. Everything is built from the existing
alpha cut-outs plus a synthetic room, which means it regenerates whenever the
vials do.

What makes it read as a photograph rather than a paste-up, in rough order of
how much each one matters:

  * three shadows per bottle, not one. A tight dark contact patch where the
    glass meets the stone, a long soft cast shadow raking away from the
    light, and a dim reflection in the surface. Miss the contact patch and
    the bottle hovers no matter how good the rest is.
  * warm shadows. Shadow in warm light is brown, not grey, and certainly not
    black. These are mixed toward #6B5F52.
  * one light direction, obeyed by everything — the wall gradient, the sheen
    on the stone, the shadow angle and the highlight side of each bottle.
  * depth of field. The wall is far out of focus, the stone softens toward
    the camera, and only the hero bottle is truly sharp.

Run from this directory.
"""
import math
import os

import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC = "../vials"

# The room, as colour. Warm neutrals only; the brand blue is the one cool
# thing in the frame and it should stay that way.
WALL_TOP   = (228, 216, 202)
WALL_BOT   = (205, 190, 174)
STONE_FAR  = (226, 214, 198)
STONE_NEAR = (198, 183, 166)
SUNWARM    = (255, 243, 223)      # the light itself
SHADOW     = (107, 95, 82)        # warm brown, never grey

LIGHT_X = 0.26                    # where the sun comes from, across the frame
HORIZON = 0.615                   # where the stone meets the wall


def noise(w, h, scale, seed):
    """Low-frequency mottle, for stone that is not a flat swatch."""
    rng = np.random.default_rng(seed)
    small = rng.random((max(2, h // scale), max(2, w // scale)))
    big = np.asarray(Image.fromarray((small * 255).astype(np.uint8))
                     .resize((w, h), Image.BICUBIC)).astype(float) / 255
    return ndimage.gaussian_filter(big, scale * 0.35)


def leaf(d, cx, cy, length, width, angle, fill):
    """One leaf: a pointed oval, drawn as a polygon.

    Pointed at both ends, widest a little past the middle. The two cusps are
    what make it read as a leaf rather than a blob — an ellipse at this blur
    is indistinguishable from noise, which is exactly what the first attempt
    at this scene produced.
    """
    ca, sa = math.cos(angle), math.sin(angle)
    pts = []
    for side in (1, -1):
        rng_t = np.linspace(0, 1, 22)[::side]
        for t in rng_t:
            w = math.sin(math.pi * t) ** 0.62 * width * side
            u, v = (t - 0.5) * length, w
            pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    d.polygon(pts, fill=fill)


def sprig(d, ox, oy, span, scale, angle, fill, rng, leaves=7):
    """A stem with leaves alternating off it. Clusters read as a plant; lone
    leaves read as litter."""
    for i in range(leaves):
        t = (i + 1) / (leaves + 1)
        side = 1 if i % 2 else -1
        px = ox + math.cos(angle) * span * t
        py = oy + math.sin(angle) * span * t
        la = angle + side * rng.uniform(0.55, 1.05)
        ln = scale * rng.uniform(0.72, 1.15) * (1.15 - 0.45 * t)
        leaf(d, px + math.cos(la) * ln * 0.5, py + math.sin(la) * ln * 0.5,
             ln, ln * rng.uniform(0.26, 0.34), la, fill)


def gobo(W, H, hz, seed=23):
    """Light coming through leaves — the single strongest cue in the frame.

    Not an object: the absence of light in leaf-shaped patches. Built once at
    full size, then resampled twice, because the wall and the stone are two
    different planes. On the wall the pattern is seen more or less head on. On
    the stone it is a floor seen at a grazing angle, so it compresses towards
    the horizon and shears away from the light. Skipping that second sampling
    is what made the first version read as a stain: the same pattern laid flat
    over both planes has no geometry in it, and the eye reads the absence.
    """
    rng = np.random.default_rng(seed)
    m = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(m)
    for _ in range(13):                                   # the canopy
        ox = rng.uniform(-0.15, 0.95) * W
        oy = rng.uniform(-0.25, 0.85) * H
        sprig(d, ox, oy, rng.uniform(0.16, 0.34) * W, rng.uniform(0.07, 0.13) * W,
              rng.uniform(-0.5, 1.9), 0, rng, leaves=rng.integers(5, 9))
    g = np.asarray(m.filter(ImageFilter.GaussianBlur(W * 0.0055))).astype(float) / 255.0

    out = np.empty_like(g)
    out[:hz] = g[:hz]                                     # the wall, head on
    yy = np.arange(hz, H)
    # the stone: compressed towards the horizon, sheared away from the light
    src_y = np.clip(hz + (yy - hz) * 0.42, 0, H - 1).astype(int)
    shift = ((yy - hz) * 0.30).astype(int)
    xx = np.arange(W)
    for i, y in enumerate(yy):
        out[y] = g[src_y[i]][(xx - shift[i]) % W]
    return out


def canopy(W, H, seed=41):
    """Leaves in front of the camera, not in front of the light.

    A frond entering top-left, close enough to be well outside the focal
    plane. It costs one corner of the frame and buys the whole depth cue: a
    photograph with something soft and dark in the near foreground reads as
    taken through a room, and a clean rectangle reads as rendered.
    """
    rng = np.random.default_rng(seed)
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    for ox, oy, span, sc, ang, n in (
            (-0.08, -0.10, 0.30, 0.17, 0.75, 7),
            (-0.02, -0.16, 0.26, 0.14, 1.15, 6),
            (0.16, -0.14, 0.22, 0.12, 1.45, 5)):
        sprig(d, ox * W, oy * H, span * W, sc * W, ang, 255, rng, leaves=n)
    return m.filter(ImageFilter.GaussianBlur(W * 0.011))


def room(W, H):
    """Wall behind, stone in front, lit from one side."""
    hz = int(H * HORIZON)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    for y in range(hz):                                   # the wall
        t = y / max(hz - 1, 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(WALL_TOP[i] + (WALL_BOT[i] - WALL_TOP[i]) * t) for i in range(3)))
    for y in range(hz, H):                                # the stone
        t = (y - hz) / max(H - hz - 1, 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(STONE_FAR[i] + (STONE_NEAR[i] - STONE_FAR[i]) * t) for i in range(3)))

    a = np.asarray(img).astype(float)

    # stone grain: fine mottle plus a faint horizontal drift, like cut travertine
    g = noise(W, H, 26, 7) * 0.55 + noise(W, H, 110, 3) * 0.45
    g = (g - g.mean()) * 16
    a[hz:] += g[hz:, :, None]
    a[:hz] += (g[:hz, :, None]) * 0.35                    # the wall is smoother

    # the light. A broad warm pool from LIGHT_X, falling off across the frame,
    # brightest just under the horizon where a window would catch the stone.
    yy, xx = np.mgrid[0:H, 0:W]
    dx = (xx / W - LIGHT_X)
    dy = (yy / H - HORIZON * 0.75)
    pool = np.exp(-(dx * dx) / 0.14 - (dy * dy) / 0.22)
    a += (np.array(SUNWARM) - a) * (pool * 0.42)[..., None]

    # a soft bright band on the stone just past the horizon: the sheen of a
    # polished surface catching the window
    band = np.exp(-((yy - hz - H * 0.03) ** 2) / (2 * (H * 0.045) ** 2))
    band = band * np.clip(1.25 - np.abs(xx / W - LIGHT_X) * 1.5, 0, 1)
    a += (255 - a) * (band * 0.22)[..., None]

    # the crease where the wall meets the stone. Without it the join is a
    # razor-straight paper edge and the whole thing reads as a backdrop.
    crease = np.exp(-((yy - hz) ** 2) / (2 * (H * 0.013) ** 2))
    a += (np.array(SHADOW, float) - a) * (crease * 0.30)[..., None]
    # and a wider ambient darkening just under it, where light does not reach
    tuck = np.exp(-((yy - hz - H * 0.012) ** 2) / (2 * (H * 0.030) ** 2)) * (yy > hz)
    a += (np.array(SHADOW, float) - a) * (tuck * 0.12)[..., None]

    # leaf shadows on the wall and the stone. Strongest where the light is,
    # because that is the only place there is light to interrupt.
    g = gobo(W, H, hz)
    lit = np.clip(pool * 1.9, 0, 1)                   # only where there is light to block
    a += (np.array(SHADOW, float) - a) * ((1 - g) * lit * 0.42)[..., None]
    # and the gaps between the leaves are brighter than the open wall would be,
    # because that is what a hard source behind foliage does
    a += (255 - a) * (np.clip(g - 0.85, 0, 1) * lit * 0.55)[..., None]

    out = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    # the wall is a long way behind the bottles
    wall = out.crop((0, 0, W, hz)).filter(ImageFilter.GaussianBlur(W * 0.012))
    out.paste(wall, (0, 0))
    # feather the join itself so it is a transition, not a cut
    seam = out.crop((0, hz - int(H * .02), W, hz + int(H * .02)))
    out.paste(seam.filter(ImageFilter.GaussianBlur(H * 0.006)), (0, hz - int(H * .02)))
    return out, hz


def warm(v, amount=0.30):
    """Sit the glass in the room's light, without moving the brand blue.

    Everything in a warm room picks up the colour of the light. If the bottle
    does not, it reads as cut out — which is the whole problem being solved
    here. But the crimp and the printed type are #2365CD by construction and
    Mila has been clear about that blue, so the shift is held to a quarter
    strength wherever the mask says brand.
    """
    px = np.asarray(v.convert("RGB")).astype(float)
    r_, g_, b_ = px[:, :, 0], px[:, :, 1], px[:, :, 2]
    brand = (b_ - r_ > 45) & (b_ - g_ > 25) & (b_ > 90)
    hold = ndimage.gaussian_filter(brand.astype(float), 1.2)[..., None]

    lit = px + (np.array(SUNWARM, float) - px) * amount * 0.55
    lit[:, :, 2] *= 0.985                                  # pull a touch of blue out of the glass
    px = px * hold + lit * (1 - hold) + (lit - px) * hold * 0.25
    rgb = Image.fromarray(px.clip(0, 255).astype(np.uint8))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
    return Image.merge("RGBA", (*rgb.split(), v.getchannel("A")))


def cast_shadow(v, length, lean, blur):
    """The long shadow lying on the stone, raking away from the light.

    Row 0 of the result is the bottle's own base and each row below is further
    away, sheared sideways and fading, so the shadow leaves the bottle rather
    than floating near it. Getting that orientation backwards is what made the
    first attempt look like window blinds lying on the counter.

    The canvas is padded by three blur radii, for the same reason the vial
    shadows are: blurring inside a tight box clips the falloff square and
    leaves a visible rectangle on the stone.
    """
    a = np.asarray(v.getchannel("A")).astype(float) / 255
    h, w = a.shape
    sh = max(1, int(h * length))
    pad = int(blur * 3)
    sw = int(w + abs(lean) * sh) + pad * 2
    out = np.zeros((sh + pad * 2, sw))
    for y in range(sh):
        t = y / max(sh - 1, 1)                       # 0 at the bottle, 1 at the tip
        # sample up the bottle: the near end of the shadow is its base, the far
        # end is its shoulder, foreshortened
        src = a[min(h - 1, int(h - 1 - t * (h - 1) * 0.55))]
        off = pad + int(t * abs(lean) * sh) * (1 if lean > 0 else 0)
        if lean < 0:
            off = pad + int((1 - t) * abs(lean) * sh)
        out[pad + y, off:off + w] = src * (1 - t) ** 1.5
    sm = ndimage.gaussian_filter(out, blur)
    img = Image.new("RGBA", (sw, sh + pad * 2), SHADOW + (0,))
    img.putalpha(Image.fromarray((sm * 255 * 0.50).clip(0, 255).astype(np.uint8)))
    return img, pad


def contact(v, blur=7):
    """The small dark patch where glass meets stone. Without this it hovers."""
    a = np.asarray(v.getchannel("A")).astype(float) / 255
    h, w = a.shape
    foot = a[int(h * 0.93):].max(axis=0)
    band = max(6, int(h * 0.035))
    out = np.zeros((band * 3, w))
    for y in range(band):
        out[band + y] = foot * (1 - y / band) ** 0.7
    sm = ndimage.gaussian_filter(out, blur)
    img = Image.new("RGBA", (w, band * 3), SHADOW + (0,))
    img.putalpha(Image.fromarray((sm * 255 * 0.78).clip(0, 255).astype(np.uint8)))
    return img, band


def reflection(v, drop=0.42, strength=0.30):
    """A dim upside-down ghost in the polished stone."""
    r = v.transpose(Image.FLIP_TOP_BOTTOM)
    h = int(r.height * drop)
    r = r.crop((0, 0, r.width, h))
    a = np.asarray(r.getchannel("A")).astype(float)
    fade = np.linspace(1, 0, h)[:, None] ** 1.6
    r.putalpha(Image.fromarray((a * fade * strength).clip(0, 255).astype(np.uint8)))
    return r.filter(ImageFilter.GaussianBlur(3.5))


def vial(name):
    im = Image.open(f"{SRC}/tmg-{name}.png").convert("RGBA")
    a = np.asarray(im); ys, xs = np.where(a[:, :, 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


# name, centre x, height as a fraction of frame, tilt, defocus
CAST = [
    ("nad",            .560, .300,  0, 2.6),
    ("tmg-3rt",        .655, .345,  0, 1.1),
    ("ghk-cu",         .762, .420,  0, 0.0),
    ("bpc-157-tb-500", .868, .330,  0, 1.4),
]


# The square crop is narrower, so the same fractional positions bunch the
# bottles and NAD+ ends up hiding behind TMG-3RT. Its own spacing, wider and
# a little shorter, so all four read.
SQUARE_CAST = [
    ("nad",            .455, .234,  0, 2.6),
    ("tmg-3rt",        .585, .269,  0, 1.1),
    ("ghk-cu",         .728, .328,  0, 0.0),
    ("bpc-157-tb-500", .872, .257,  0, 1.4),
]


def compose(W, H, out, cast=None):
    scene, hz = room(W, H)
    scene = scene.convert("RGBA")

    for name, fx, fh, ang, dof in (cast or CAST):
        v = vial(name)
        h = max(1, int(H * fh))
        v = v.resize((max(1, int(v.width * h / v.height)), h), Image.LANCZOS)
        v = warm(v)
        if dof:
            v = v.filter(ImageFilter.GaussianBlur(dof))

        cx = int(W * fx)
        base = hz + int(H * 0.035)                 # bottles stand just past the horizon
        x, y = cx - v.width // 2, base - v.height

        lean = 1.0 if fx > LIGHT_X else -1.0       # shadows fall away from the light
        cs, cpad = cast_shadow(v, 0.52, lean * 1.25, max(5, int(h * 0.028)))
        scene.alpha_composite(cs, (x - cpad, base - cpad))

        ref = reflection(v)
        scene.alpha_composite(ref, (x, base))

        cp, band = contact(v, max(5, int(h * 0.022)))
        scene.alpha_composite(cp, (x, base - band))

        scene.alpha_composite(v, (x, y))

    # the near leaves go on last, because they are in front of the camera and
    # therefore in front of the bottles too. Unlit, so they are dark and
    # desaturated rather than green — foreground foliage in a bright room is
    # almost a silhouette.
    near = Image.new("RGBA", (W, H), (58, 64, 52, 0))
    near.putalpha(canopy(W, H).point(lambda q: int(q * 0.80)))
    scene.alpha_composite(near)

    scene.convert("RGB").save(out, quality=90, optimize=True)
    print(f"  {out:28s} {W}x{H}  {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    compose(2560, 1440, "scene-hero.jpg")
    compose(1600, 1400, "scene-square.jpg", SQUARE_CAST)
