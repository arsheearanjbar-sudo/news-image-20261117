#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Own work, drawn with PIL from the day's verified reporting:
  1. Trump arrives in Manila for the Quad summit (ASEAN sidelines).
  2. Ukraine strikes the Crimean Bridge; Russia hits two Kyiv bridges.
  3. Malicious code hits 178 websites incl. BBC and CNN.
  4. US loses its measles-free status (PAHO).
  5. Delhi eases smog curbs as its AQI improves to 204 (CAQM).
  6. Cyclone Akvan nears India's east coast.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 246, 233)
INK = (20, 20, 20)
RED = (163, 30, 34)
BLUE = (29, 78, 137)
GREY = (90, 90, 90)
LIGHT = (238, 231, 214)

FD = "/usr/share/fonts/truetype/dejavu/"
f_serif_b = lambda s: ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)
f_sans_b = lambda s: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
f_sans = lambda s: ImageFont.truetype(FD + "DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def center(x0, x1, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


def wrap_lines(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit_font(text, make_font, size, max_w):
    """Largest font size (<= size) at which text fits max_w on one line."""
    while size > 10:
        f = make_font(size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return make_font(size)


def text_block(x, y, max_w, text, font, fill=INK, leading=None):
    lines = wrap_lines(text, font, max_w)
    lh = leading or int(font.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------- masthead ----------------
center(0, W, 22, "THE WORLD IN ONE DAY", f_serif_b(62), INK)
center(0, W, 100, "TUESDAY, 17 NOVEMBER 2026", f_sans_b(38), RED)
d.line([(28, 152), (996, 152)], fill=INK, width=4)
d.line([(28, 160), (996, 160)], fill=INK, width=2)

# ---------------- hero: Manila / Quad ----------------
d.rectangle([28, 172, 996, 428], outline=INK, width=3)
# art zone: skyline + four flags
ax0, ax1, ay0, ay1 = 44, 372, 188, 416
d.rectangle([ax0, ay0, ax1, ay1], fill=(223, 232, 240))
# skyline
for (bx, bw, bh) in [(48, 34, 150), (86, 26, 110), (116, 40, 180),
                     (160, 30, 130), (194, 36, 165), (234, 28, 120),
                     (266, 34, 150), (304, 30, 120), (338, 30, 165)]:
    d.rectangle([bx, ay1 - bh, bx + bw, ay1], fill=(52, 68, 92))
# four flag poles
flag_x = [60, 140, 220, 300]
for i, fx in enumerate(flag_x):
    d.line([(fx, 196), (fx, ay1 - 60)], fill=INK, width=3)
    d.rectangle([fx, 196, fx + 62, 226], outline=INK, width=2)
    if i == 0:  # USA: stripes + canton
        for s in range(5):
            d.rectangle([fx + 1, 197 + s * 6, fx + 61, 197 + s * 6 + 3],
                        fill=RED if s % 2 == 0 else PAPER)
        d.rectangle([fx + 1, 197, fx + 26, 212], fill=BLUE)
        for dx in (6, 14, 22):
            for dy in (200, 206):
                d.ellipse([fx + dx, dy, fx + dx + 3, dy + 3], fill=(255, 255, 255))
    elif i == 1:  # India: saffron / white / green
        d.rectangle([fx + 1, 197, fx + 61, 207], fill=(255, 153, 51))
        d.rectangle([fx + 1, 207, fx + 61, 216], fill=(255, 255, 255))
        d.rectangle([fx + 1, 216, fx + 61, 225], fill=(19, 136, 8))
        d.ellipse([fx + 27, 208, fx + 35, 216], outline=BLUE, width=2)
    elif i == 2:  # Japan: red disc
        d.rectangle([fx + 1, 197, fx + 61, 225], fill=(255, 255, 255))
        d.ellipse([fx + 21, 203, fx + 41, 221], fill=RED)
    else:  # Australia: blue field, stars
        d.rectangle([fx + 1, 197, fx + 61, 225], fill=BLUE)
        for (sx, sy) in [(8, 202), (18, 212), (50, 202), (54, 216), (32, 208)]:
            d.ellipse([fx + sx, sy, fx + sx + 4, sy + 4], fill=(255, 255, 255))
# hero text (chained: headline fits one line, body wraps below it)
hy = 196
hf = fit_font("TRUMP IN MANILA", f_sans_b, 56, 570)
d.text((400, hy), "TRUMP IN MANILA", font=hf, fill=INK)
hy += hf.size + 16
hy = text_block(400, hy, 570,
                "Quad leaders meet on the ASEAN sidelines. "
                "China confirms a Nov 19 summit with Xi and Putin. "
                "Protests greet the US president in the capital.",
                f_sans(27), GREY)


def panel(x0, y0, x1, y1, headline, body, draw_icon):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)
    d.rectangle([x0, y0, x1, y0 + 4], fill=RED)
    draw_icon(x0 + 18, y0 + 34, 140, 110)
    tx = x0 + 176
    tw = x1 - tx - 14
    hf = fit_font(headline, f_sans_b, 34, tw)
    d.text((tx, y0 + 22), headline, font=hf, fill=INK)
    text_block(tx, y0 + 22 + hf.size + 12, tw, body, f_sans(24), INK)


def icon_bridge(x, y, w, h):
    d.line([(x, y + h - 8), (x + w, y + h - 8)], fill=BLUE, width=3)
    d.arc([x + 8, y + 10, x + w // 2 + 8, y + h], 180, 360, fill=INK, width=5)
    d.arc([x + w // 2 - 8, y + 10, x + w - 8, y + h], 180, 360, fill=INK, width=5)
    d.line([(x + w // 2, y + 6), (x + w // 2, y + h - 8)], fill=INK, width=5)
    # blast burst on the left span
    cx, cy = x + 34, y + 26
    for ang in range(0, 360, 30):
        r = math.radians(ang)
        d.line([(cx, cy), (cx + 26 * math.cos(r), cy + 26 * math.sin(r))],
               fill=RED, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)


def icon_cyber(x, y, w, h):
    d.rounded_rectangle([x + 8, y, x + w - 8, y + h - 28], radius=8,
                        outline=INK, width=4)
    d.line([(x + w // 2, y + h - 28), (x + w // 2, y + h - 8)], fill=INK, width=4)
    d.line([(x + w // 2 - 26, y + h - 8), (x + w // 2 + 26, y + h - 8)],
           fill=INK, width=4)
    # warning triangle
    cx, cy = x + w // 2, y + 44
    d.polygon([(cx, cy - 26), (cx - 28, cy + 20), (cx + 28, cy + 20)],
              fill=(232, 178, 62), outline=INK)
    d.text((cx - 5, cy - 12), "!", font=f_sans_b(30), fill=INK)


def icon_virus(x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for ang in range(0, 360, 30):
        r = math.radians(ang)
        d.line([(cx + 26 * math.cos(r), cy + 26 * math.sin(r)),
                (cx + 42 * math.cos(r), cy + 42 * math.sin(r))],
               fill=RED, width=5)
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=RED)
    d.ellipse([cx - 10, cy - 12, cx + 2, cy], fill=(255, 255, 255))
    d.ellipse([cx + 8, cy + 6, cx + 18, cy + 16], fill=(255, 255, 255))


def icon_haze(x, y, w, h):
    # pale sun behind soft grey haze bands
    cx = x + w // 2
    d.ellipse([cx - 34, y + 2, cx + 34, y + 70], fill=(238, 214, 150))
    d.ellipse([cx - 24, y + 12, cx + 24, y + 60], fill=(232, 178, 62))
    for (by, bw, shade) in [(y + 66, 128, (150, 150, 150)),
                             (y + 80, 108, (170, 170, 170)),
                             (y + 94, 88, (128, 128, 128))]:
        d.rounded_rectangle([cx - bw // 2, by, cx + bw // 2, by + 7],
                            radius=3, fill=shade)


def icon_cyclone(x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for r, a0, a1 in [(14, 0, 300), (24, 40, 340), (34, 90, 30),
                      (44, 140, 80), (52, 190, 130)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=BLUE, width=5)


# ---------------- 2x2 grid ----------------
panel(28, 444, 502, 626, "BRIDGES HIT",
      "Ukraine strikes the Crimea bridge; Russia hits two Kyiv bridges.",
      icon_bridge)
panel(522, 444, 996, 626, "CYBERATTACK",
      "Malicious code hits 178 websites, incl. BBC and CNN.",
      icon_cyber)
panel(28, 636, 502, 818, "MEASLES BACK",
      "US loses its measles-free status for the first time since 2000.",
      icon_virus)
panel(522, 636, 996, 818, "DELHI BREATHES",
      "Smog curbs eased as Delhi's air improves; daily AQI falls to 204.",
      icon_haze)

# ---------------- bottom strip: cyclone ----------------
d.rectangle([28, 834, 996, 968], outline=INK, width=3)
d.rectangle([28, 834, 996, 838], fill=RED)
icon_cyclone(46, 850, 120, 100)
sy = text_block(190, 856, 780, "CYCLONE AKVAN", f_sans_b(36), INK)
text_block(190, sy + 6, 780,
           "India braces as the storm nears the east coast; Odisha evacuates.",
           f_sans(25), INK)

# ---------------- footer ----------------
center(0, W, 982, "Drawn from the day's reporting  •  17 November 2026",
       f_sans(20), GREY)

img.save("/home/hatch/workspace/makefun/news-image-20261117/entry.png",
         optimize=True)
print("saved entry.png")
