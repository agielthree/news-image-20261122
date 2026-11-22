#!/usr/bin/env python3
"""The World in One Day -- Sunday, 22 November 2026.

Draws a 1024x1024 newspaper poster summing up six verified news
stories first reported on 22 November 2026. Everything on the page is
drawn with Pillow primitives: no network, no randomness, no clock, no
external images. Running this script twice writes byte-identical PNGs.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (246, 241, 229)
CARD = (255, 253, 246)
TINT = (237, 230, 212)
INK = (25, 25, 25)
GREY = (112, 107, 96)
LINE = (198, 190, 172)
RED = (142, 27, 27)
NAVY = (29, 53, 87)
GOLD = (176, 124, 22)
ORANGE = (214, 110, 30)

LEAD = {
    "tag": "MIDDLE EAST  —  LEAD STORY",
    "headline": "IRGC Claims Missile and Drone Strikes on U.S. Positions in Bahrain",
    "body": "Bahrain says a civilian industrial facility was hit and caught "
            "fire, with no casualties. Air defences intercepted several of "
            "the attacks.",
    "dateline": "BAHRAIN  •  22 NOVEMBER 2026",
}

GRID = [
    {
        "tag": "CLIMATE  —  ANTALYA",
        "headline": "COP31 Talks Stall Over Fossil Fuels in Overtime",
        "body": "Final draft drops all fossil-fuel mentions; Panama threatens "
                "to block a deal without oil production limits.",
        "icon": "globe",
    },
    {
        "tag": "MEXICO  —  SINALOA",
        "headline": "Mexico Captures Cartel Kingpin 'El Chapo Isidro'",
        "body": "Meza-Flores arrested in Guasave; 11 killed in the operation. "
                "He was a top-10 FBI fugitive with a $5m reward.",
        "icon": "cuffs",
    },
    {
        "tag": "UNITED STATES  —  CYBER",
        "headline": "FBI Criminal Database Reported Hacked",
        "body": "The FBI is investigating a reported breach of its NCIC "
                "database, the second FBI system broken into in months.",
        "icon": "database",
    },
    {
        "tag": "NIGERIA  —  BAYELSA",
        "headline": "Overcrowded Boat Capsizes in Nigeria",
        "body": "An overloaded boat carrying mourners capsized in Bayelsa; at "
                "least 24 died, 24 rescued. As many as 300 were aboard.",
        "icon": "boat",
    },
]

WIDE = {
    "tag": "EUROPE  —  BALTIC SEA",
    "headline": "Russian Cargo Ship Hit by Drone Off Finland; Poland Accuses Russia of Provocation",
    "body": "Sparta II caught fire after a drone strike and drifted into "
            "Finnish waters; 16 crew evacuated. Poland says Russian "
            "missiles and a drone fell on its soil.",
    "icon": "ship",
}


def font(size, serif=False, bold=True):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, text, cx, y, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def ruled(draw, x0, x1, y, weight, fill):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def star(draw, cx, cy, r_out, r_in, fill):
    import math

    points = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)


# ---------------------------------------------------------------- icons

def icon_lead(draw, x, y, w, h):
    """Missile, burst and defence dome for the Bahrain lead story."""
    # defence dome
    draw.arc([x + 18, y + h - 118, x + w - 18, y + h - 8], 180, 360,
             fill=NAVY, width=5)
    for dx in (-52, 0, 52):
        draw.line([(x + w // 2 + dx, y + h - 66), (x + w // 2 + dx, y + h - 14)],
                  fill=NAVY, width=3)
    draw.line([(x + 8, y + h - 8), (x + w - 8, y + h - 8)], fill=NAVY, width=4)
    # rocket body, flying right
    bx, by = x + 52, y + 58
    draw.rectangle([bx, by, bx + 108, by + 26], fill=RED)
    draw.polygon([(bx + 108, by), (bx + 138, by + 13), (bx + 108, by + 26)],
                 fill=RED)
    draw.polygon([(bx + 6, by + 26), (bx + 26, by + 26), (bx + 6, by + 44)],
                 fill=RED)
    draw.polygon([(bx + 6, by), (bx + 26, by), (bx + 6, by - 18)], fill=RED)
    draw.rectangle([bx + 34, by + 6, bx + 46, by + 20], fill=PAPER)
    # flame behind the tail
    draw.polygon([(bx, by + 4), (bx - 34, by + 13), (bx, by + 22)], fill=ORANGE)
    draw.polygon([(bx, by + 8), (bx - 20, by + 13), (bx, by + 18)], fill=GOLD)
    # burst above the nose
    star(draw, x + w - 42, y + 30, 20, 8, GOLD)
    star(draw, x + 34, y + 26, 10, 4, GOLD)


def icon_globe(draw, x, y, w, h):
    """Globe with a crack: the COP31 fossil-fuel deadlock."""
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY,
                 width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=NAVY,
             width=2)
    crack = [(cx - r + 8, cy - r // 3), (cx - r // 3, cy + 2),
             (cx, cy - r // 4), (cx + r // 3, cy + r // 3),
             (cx + r - 10, cy + r // 4)]
    draw.line(crack, fill=RED, width=4, joint="curve")


def icon_cuffs(draw, x, y, w, h):
    """Handcuffs and a badge star: the cartel arrest."""
    cy = y + h // 2 + 6
    r = 24
    left, right = x + 16, x + w - 16
    draw.ellipse([left - r, cy - r, left + r, cy + r], outline=NAVY, width=5)
    draw.ellipse([right - r, cy - r, right + r, cy + r], outline=NAVY,
                 width=5)
    mid = (left + right) // 2
    for dx in (-14, 0, 14):
        draw.ellipse([mid + dx - 6, cy - 26, mid + dx + 6, cy - 14],
                     outline=NAVY, width=3)
    star(draw, mid, y + 22, 18, 8, GOLD)


def icon_database(draw, x, y, w, h):
    """Database cylinder split by a lightning bolt: the NCIC breach."""
    cx = x + w // 2
    top, bottom = y + 14, y + h - 14
    draw.rectangle([cx - 34, top + 10, cx + 34, bottom - 10], outline=NAVY,
                   width=4)
    draw.ellipse([cx - 34, top - 2, cx + 34, top + 22], outline=NAVY, width=4)
    draw.arc([cx - 34, bottom - 22, cx + 34, bottom + 2], 0, 180, fill=NAVY,
             width=4)
    draw.line([(cx - 34, top + 34), (cx + 34, top + 34)], fill=NAVY, width=3)
    draw.line([(cx - 34, top + 58), (cx + 34, top + 58)], fill=NAVY, width=3)
    bolt = [(cx + 8, top - 6), (cx - 12, y + h // 2 + 4), (cx + 2, y + h // 2 + 4),
            (cx - 8, bottom + 6), (cx + 14, y + h // 2 - 2),
            (cx, y + h // 2 - 2)]
    draw.polygon(bolt, fill=RED)


def icon_boat(draw, x, y, w, h):
    """Capsized hull, waves and a life ring: the Bayelsa boat."""
    cx = x + w // 2
    draw.pieslice([cx - 42, y + 6, cx + 42, y + 66], 180, 360, fill=NAVY)
    draw.rectangle([cx - 42, y + 34, cx + 42, y + 40], fill=NAVY)
    for i, wy in enumerate((y + h - 34, y + h - 20, y + h - 6)):
        draw.arc([x + 6 + i * 8, wy - 8, x + w - 6 - i * 8, wy + 8], 180, 360,
                 fill=NAVY, width=3)
    rx, ry = x + w - 26, y + h - 30
    draw.ellipse([rx - 16, ry - 16, rx + 16, ry + 16], outline=RED, width=6)
    draw.ellipse([rx - 7, ry - 7, rx + 7, ry + 7], outline=RED, width=2)


def icon_ship(draw, x, y, w, h):
    """Cargo ship, fire and a drone overhead: the Sparta II strike."""
    # drone, top right
    dx, dy = x + w - 52, y + 22
    draw.rectangle([dx - 12, dy - 5, dx + 12, dy + 5], fill=INK)
    for sx in (-1, 1):
        draw.line([(dx + sx * 10, dy), (dx + sx * 26, dy - 6)], fill=INK,
                  width=3)
        draw.ellipse([dx + sx * 26 - 9, dy - 11, dx + sx * 26 + 9, dy - 1],
                     outline=INK, width=2)
    # flame over the containers
    fx, fy = x + w // 2 - 30, y + 34
    draw.polygon([(fx, fy + 22), (fx + 12, fy), (fx + 24, fy + 22)], fill=ORANGE)
    draw.polygon([(fx + 8, fy + 22), (fx + 16, fy + 8), (fx + 26, fy + 22)],
                 fill=GOLD)
    # containers and hull
    draw.rectangle([x + 18, y + 58, x + 52, y + 86], fill=RED)
    draw.rectangle([x + 56, y + 58, x + 90, y + 86], fill=GOLD)
    draw.rectangle([x + 94, y + 58, x + 128, y + 86], fill=NAVY)
    draw.polygon([(x + 8, y + 86), (x + w - 8, y + 86), (x + w - 26, y + 108),
                  (x + 26, y + 108)], fill=NAVY)
    draw.line([(x + 132, y + 58), (x + 132, y + 30)], fill=INK, width=3)
    # waves
    for wy in (y + h - 14, y + h - 2):
        draw.arc([x + 6, wy - 8, x + w - 6, wy + 8], 180, 360, fill=NAVY,
                 width=3)


ICONS = {
    "globe": icon_globe,
    "cuffs": icon_cuffs,
    "database": icon_database,
    "boat": icon_boat,
    "ship": icon_ship,
}


# ---------------------------------------------------------------- page

def card(draw, x, y, w, h, story, head_size, body_size, icon_box):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    ix, iy, iw, ih = icon_box
    draw.rounded_rectangle([ix, iy, ix + iw, iy + ih], radius=10, fill=TINT)
    ICONS[story["icon"]](draw, ix, iy, iw, ih)
    tx = ix + iw + 14
    tw = x + w - 14 - tx
    tag_font = font(14)
    head_font = font(head_size)
    body_font = font(body_size, bold=False)
    draw.text((tx, y + 11), story["tag"], font=tag_font, fill=NAVY)
    head_lines = wrap(draw, story["headline"], head_font, tw)
    if len(head_lines) > 2:
        sys.exit("OVERFLOW headline: %s -> %d lines"
                 % (story["headline"], len(head_lines)))
    by = draw_lines(draw, head_lines, tx, y + 33, head_font, INK, head_size + 5)
    body_lines = wrap(draw, story["body"], body_font, tw)
    if len(body_lines) > 3:
        sys.exit("OVERFLOW body: %s -> %d lines"
                 % (story["body"], len(body_lines)))
    draw_lines(draw, body_lines, tx, by + 4, body_font, INK, body_size + 5)
    print("card %-28s headline=%d body=%d"
          % (story["tag"], len(head_lines), len(body_lines)))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # double outer border
    draw.rectangle([14, 14, W - 14, H - 14], outline=INK, width=2)
    draw.rectangle([20, 20, W - 20, H - 20], outline=LINE, width=1)

    # masthead
    centered(draw, "MAKE.FUN  •  DAILY NEWS POSTER", W // 2, 40,
             font(17), NAVY)
    centered(draw, "THE WORLD IN ONE DAY", W // 2, 62, font(60, serif=True),
             INK)
    centered(draw, "SUNDAY, 22 NOVEMBER 2026", W // 2, 130, font(23), RED)
    ruled(draw, 36, W - 36, 164, 3, INK)
    ruled(draw, 36, W - 36, 170, 1, INK)

    # lead story
    lx, ly, lw, lh = 36, 182, W - 72, 262
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=LINE,
                   width=1)
    draw.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    icon_lead(draw, lx + 22, ly + 20, 196, lh - 40)
    tx = lx + 240
    tw = lx + lw - 16 - tx
    draw.text((tx, ly + 18), LEAD["tag"], font=font(17), fill=RED)
    head_lines = wrap(draw, LEAD["headline"], font(33, serif=True), tw)
    if len(head_lines) > 2:
        sys.exit("OVERFLOW lead headline -> %d lines" % len(head_lines))
    by = draw_lines(draw, head_lines, tx, ly + 44, font(33, serif=True), INK,
                    39)
    body_lines = wrap(draw, LEAD["body"], font(19, bold=False), tw)
    if len(body_lines) > 3:
        sys.exit("OVERFLOW lead body -> %d lines" % len(body_lines))
    by = draw_lines(draw, body_lines, tx, by + 8, font(19, bold=False), INK,
                    25)
    draw.text((tx, ly + lh - 30), LEAD["dateline"], font=font(15), fill=GREY)
    print("lead headline=%d body=%d" % (len(head_lines), len(body_lines)))

    # grid: two half cards, two half cards, one wide card
    gx, gy = 36, 456
    cw = (W - 72 - 14) // 2
    ch = 154
    rows = [(GRID[0], GRID[1]), (GRID[2], GRID[3])]
    for r, (left, right) in enumerate(rows):
        y = gy + r * (ch + 12)
        for c, story in enumerate((left, right)):
            x = gx + c * (cw + 14)
            card(draw, x, y, cw, ch, story, 21, 16, (x + 12, y + 29, 104, 96))
    wy = gy + 2 * (ch + 12)
    card(draw, gx, wy, W - 72, ch, WIDE, 25, 17, (gx + 12, wy + 17, 168, 120))

    # footer
    ruled(draw, 36, W - 36, 956, 1, LINE)
    centered(draw,
             "All six stories were first reported on Sunday, 22 November 2026  •  Sources: wire reports",
             W // 2, 966, font(14, bold=False), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    size = os.path.getsize(out)
    print("wrote %s %dx%d %d bytes" % (out, W, H, size))
    if size > 1048576:
        sys.exit("entry.png exceeds 1 MiB")


if __name__ == "__main__":
    main()
