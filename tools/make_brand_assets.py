"""Regenerate the Open Graph cards and favicon set.

    python tools/make_brand_assets.py

Requires Pillow and the Inter typeface (the same font the site loads).
Writes, relative to the repo root:

    assets/images/og-card.png     1200x630, homepage — headline and price are
                                  baked into the pixels, so re-run this whenever
                                  the hero copy or the $297 figure changes
    assets/images/og-default.png  1200x630, every other page
    favicon.ico                   16/32/48, transparent
    favicon-16x16.png
    favicon-32x32.png
    apple-touch-icon.png          180x180, opaque

Source art is assets/images/gentoolink-logo.png (emblem) and
gentoolink-mark.png (penguin only, used for the icons). Colours below mirror
the custom properties at the top of style.css — keep them in sync.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")

BG = (7, 9, 13)           # --bg
CARD = (12, 16, 23)       # --bg-card
TEXT = (242, 244, 248)    # --text
MUTED = (154, 164, 178)   # --text-muted
SUBTLE = (98, 108, 120)   # --text-subtle
TEAL = (45, 212, 191)     # --accent
GOLD = (240, 192, 64)     # --gold-bright
GOLD_DEEP = (201, 150, 10)  # --gold-deep

HAIRLINE = (28, 36, 48)   # --border

W, H = 1200, 630

# Inter ships under different filenames depending on how it was installed.
_INTER_CANDIDATES = {
    "bold": ["Inter_FXH-Bold.ttf", "Inter-Bold.ttf", "InterDisplay-Bold.ttf"],
    "regular": ["Inter_FXH-Regular.ttf", "Inter-Regular.ttf", "InterDisplay-Regular.ttf"],
}
_FONT_DIRS = [
    os.environ.get("INTER_DIR", ""),
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
    os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts"),
    "/usr/share/fonts/truetype/inter",
    os.path.expanduser("~/Library/Fonts"),
]


def find_font(weight):
    for d in _FONT_DIRS:
        if not d:
            continue
        for name in _INTER_CANDIDATES[weight]:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                return p
    sys.exit(
        f"Could not find Inter {weight}. Install Inter, or point INTER_DIR at "
        f"the folder holding {_INTER_CANDIDATES[weight][0]}."
    )


INTER_BOLD = find_font("bold")
INTER_REGULAR = find_font("regular")


def font(path, size):
    return ImageFont.truetype(path, size)


def glow(center, radius, color, strength):
    """A soft radial brand glow, as an RGBA layer the size of the card."""
    layer = Image.new("RGBA", (W, H), color + (0,))
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    cx, cy = center
    steps = 60
    for i in range(steps, 0, -1):
        r = radius * i / steps
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=int(strength * (1 - i / steps) ** 2))
    layer.putalpha(mask.filter(ImageFilter.GaussianBlur(radius / 8)))
    return layer


def over(im, layer):
    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")


def draw_tracked(d, xy, text, fnt, fill, tracking=0.0):
    """Pillow has no letter-spacing, so step glyph by glyph."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking


def tracked_width(d, text, fnt, tracking=0.0):
    if not text:
        return 0.0
    return sum(d.textlength(c, font=fnt) + tracking for c in text) - tracking


def emblem(size):
    logo = Image.open(os.path.join(IMG, "gentoolink-logo.png")).convert("RGBA")
    return logo.resize((size, size), Image.LANCZOS)


def save(im, path, label):
    im.save(path, "PNG", optimize=True)
    print(f"{label:24} {os.path.getsize(path):>8,} bytes")


def build_home_card():
    """Left-aligned card carrying the homepage headline and the audit price."""
    im = Image.new("RGB", (W, H), BG)
    im = over(im, glow((935, 300), 380, TEAL, 30))
    im = over(im, glow((120, 640), 420, GOLD_DEEP, 18))

    PAD = 78
    lsize = 300
    logo = emblem(lsize)
    lx, ly = W - PAD - lsize, (H - lsize) // 2 - 8
    im = over(im, glow((lx + lsize // 2, ly + lsize // 2), 210, TEAL, 26))
    im.paste(logo, (lx, ly), logo)

    d = ImageDraw.Draw(im)
    f_eyebrow = font(INTER_BOLD, 20)
    f_head = font(INTER_BOLD, 58)
    f_sub = font(INTER_REGULAR, 27)
    f_price = font(INTER_BOLD, 25)
    f_url = font(INTER_REGULAR, 22)

    y = 112
    draw_tracked(d, (PAD, y), "GENTOOLINK WEB SERVICES", f_eyebrow, SUBTLE, 2.4)
    y += 52

    for line in ("Is Your Business", "Showing Up When", "Customers Ask AI?"):
        d.text((PAD, y), line, font=f_head, fill=TEXT)
        y += 70
    y += 18

    d.line([(PAD, y), (PAD + 64, y)], fill=GOLD, width=3)
    y += 30

    d.text((PAD, y), "ChatGPT  ·  Perplexity  ·  Google AI Overviews",
           font=f_sub, fill=MUTED)
    y += 48

    lead = "AI Visibility Audit — "
    d.text((PAD, y), lead, font=f_price, fill=MUTED)
    d.text((PAD + d.textlength(lead, font=f_price), y),
           "$297, delivered in 24 hours", font=f_price, fill=GOLD)

    d.text((PAD, H - PAD - 4), "gentoolinkwebservices.com", font=f_url, fill=SUBTLE)
    d.line([(0, 0), (W, 0)], fill=HAIRLINE, width=3)

    save(im, os.path.join(IMG, "og-card.png"), "og-card.png")


def build_default_card():
    """Centred brand card for every page that isn't the homepage."""
    im = Image.new("RGB", (W, H), BG)
    im = over(im, glow((600, 250), 430, TEAL, 26))
    im = over(im, glow((600, 700), 460, GOLD_DEEP, 16))

    lsize = 190
    logo = emblem(lsize)
    lx, ly = (W - lsize) // 2, 84
    im = over(im, glow((W // 2, ly + lsize // 2), 150, TEAL, 24))
    im.paste(logo, (lx, ly), logo)

    d = ImageDraw.Draw(im)
    f_name = font(INTER_BOLD, 46)
    f_tag = font(INTER_REGULAR, 28)
    f_sub = font(INTER_BOLD, 22)
    f_url = font(INTER_REGULAR, 22)

    def centre(y, text, fnt, fill, tracking=0.0):
        x = (W - tracked_width(d, text, fnt, tracking)) / 2
        draw_tracked(d, (x, y), text, fnt, fill, tracking)

    y = ly + lsize + 44
    centre(y, "GENTOOLINK WEB SERVICES", f_name, TEXT, 1.5)
    y += 74
    centre(y, "AI Visibility Audits & GEO for Local Business", f_tag, MUTED)
    y += 56
    d.line([(W / 2 - 32, y), (W / 2 + 32, y)], fill=GOLD, width=3)
    y += 32
    centre(y, "ChatGPT  ·  Perplexity  ·  Google AI Overviews", f_sub, GOLD, 0.4)

    centre(H - 78, "gentoolinkwebservices.com", f_url, SUBTLE)
    d.line([(0, 0), (W, 0)], fill=HAIRLINE, width=3)

    save(im, os.path.join(IMG, "og-default.png"), "og-default.png")


def build_icons():
    mark = Image.open(os.path.join(IMG, "gentoolink-mark.png")).convert("RGBA")
    mark = mark.crop(mark.getchannel("A").getbbox())

    s = max(mark.size)
    sq = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sq.paste(mark, ((s - mark.width) // 2, (s - mark.height) // 2), mark)

    def tile(n):
        src = sq
        if n <= 32:
            # Trim the disc edge, else the penguin is unreadable at tab size.
            k = int(src.width * 0.05)
            src = src.crop((k, k, src.width - k, src.height - k))
        out = src.resize((n, n), Image.LANCZOS)
        if n <= 48:
            out = out.filter(ImageFilter.UnsharpMask(0.6, percent=95, threshold=0))
        return out

    # Pillow stores ICO frames as uncompressed bitmaps, so a 256px frame alone
    # costs ~256 KB. Browsers never ask for one — 16/32/48 is the whole story.
    sizes = [16, 32, 48]
    frames = [tile(n) for n in sizes]
    ico = os.path.join(ROOT, "favicon.ico")
    frames[-1].save(ico, format="ICO", sizes=[(n, n) for n in sizes],
                    append_images=frames[:-1])
    print(f"{'favicon.ico':24} {os.path.getsize(ico):>8,} bytes  {sizes}")

    # iOS composites home-screen icons onto white and rounds them itself,
    # so this one is opaque and padded rather than transparent.
    ati = Image.new("RGB", (180, 180), CARD)
    inner = sq.resize((156, 156), Image.LANCZOS)
    ati.paste(inner, (12, 12), inner)
    save(ati, os.path.join(ROOT, "apple-touch-icon.png"), "apple-touch-icon.png")

    for n in (32, 16):
        save(tile(n), os.path.join(ROOT, f"favicon-{n}x{n}.png"), f"favicon-{n}x{n}.png")


def main():
    build_home_card()
    build_default_card()
    build_icons()


if __name__ == "__main__":
    main()
