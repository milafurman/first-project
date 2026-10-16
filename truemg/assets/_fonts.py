"""One font lookup for every script here.

Four scripts had `ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + n)`
hardcoded. That path exists on Linux and on no Mac, so each of them raised
`OSError: cannot open resource` the moment anyone ran it here — which is how
`foil/foil-spec.jpg` and `vials/contact-sheet.jpg` came to be unrebuildable
while still sitting in the repo looking current.

Ask for a ROLE, not a filename. The roles are the three things these spec
sheets and contact sheets actually need.
"""
import os
from PIL import ImageFont

DIRS = ("/usr/share/fonts/truetype/dejavu/",       # Linux, the original target
        "/System/Library/Fonts/",                  # macOS
        "/System/Library/Fonts/Supplemental/",
        "/Library/Fonts/",
        "/usr/share/fonts/truetype/liberation/")

ROLES = {
    "mono": ("DejaVuSansMono.ttf", "Menlo.ttc", "Courier New.ttf", "LiberationMono-Regular.ttf"),
    "sans": ("DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttc", "LiberationSans-Regular.ttf"),
    "bold": ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Arial Black.ttf", "LiberationSans-Bold.ttf"),
}


def font(role, size):
    """A real TrueType face for `role`, whatever machine this is."""
    for name in ROLES[role]:
        for d in DIRS:
            p = d + name
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except OSError:
                    continue
    # Never raise: a missing typeface should degrade a spec sheet, not stop a
    # render that has nothing to do with type.
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()
