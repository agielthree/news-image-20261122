#!/usr/bin/env python3
"""Draw the 22 November 2026 news poster for make.fun news-image-20261122.

Renders a 1024x1024 newspaper front page, "THE WORLD IN ONE DAY",
summarising six stories from Sunday, 22 November 2026. Fixed palette,
fixed fonts, fixed geometry: running this script twice produces a
byte-identical entry.png.

Usage: python3 draw_poster.py [output-path]   (default: entry.png)
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette -----------------------------------------------------------------
PAPER = (247, 243, 234)      # warm newsprint
INK = (20, 33, 61)           # deep navy ink
CARD = (255, 255, 255)       # story card
CARD_EDGE = (203, 199, 186)  # card outline
MUTED = (90, 96, 110)        # secondary text
GOLD = (233, 196, 106)       # masthead accent
RED = (178, 44, 38)          # alert / lead accent
BLUE = (38, 84, 124)         # law-enforcement accent
GREEN = (43, 122, 83)        # climate accent
TEAL = (15, 118, 110)        # europe accent
BROWN = (146, 90, 43)        # disaster accent
PURPLE = (106, 76, 147)      # cyber accent

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_TITLE = font("DejaVuSans-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 25)
F_STRIP = font("DejaVuSans.ttf", 19)
F_KICKER = font("DejaVuSans-Bold.ttf", 16)
F_HEAD = font("DejaVuSans-Bold.ttf", 23)
F_HEAD_LEAD = font("DejaVuSans-Bold.ttf", 31)
F_HEAD_LAST = font("DejaVuSans-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 16)
F_BODY_LEAD = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=CARD_EDGE, width=1)
    draw.rectangle([x, y + 10, x + 6, y + h - 10], fill=accent)


# --- icons (simple flat pictograms, drawn with shapes only) ------------------
def icon_burst(draw, cx, cy, r, color):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
                 fill=GOLD)
    for dx, dy in ((-r, -r * 0.7), (r * 0.9, -r * 0.8), (-r * 0.8, r * 0.9)):
        draw.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4],
                     fill=INK)


def icon_globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=color, width=3)
    draw.ellipse([cx + r * 0.45, cy - r * 0.75, cx + r * 0.95, cy - r * 0.25],
                 fill=GREEN)


def icon_badge(draw, cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18],
                 fill=GOLD)


def icon_ship(draw, cx, cy, s, color):
    # hull
    draw.polygon([(cx - s * 0.5, cy + s * 0.05),
                  (cx + s * 0.5, cy + s * 0.05),
                  (cx + s * 0.32, cy + s * 0.32),
                  (cx - s * 0.32, cy + s * 0.32)], fill=color)
    # mast + flag
    draw.line([(cx, cy + s * 0.05), (cx, cy - s * 0.38)], fill=INK, width=4)
    draw.polygon([(cx, cy - s * 0.38), (cx + s * 0.28, cy - s * 0.3),
                  (cx, cy - s * 0.22)], fill=RED)
    # waves
    for dy in (s * 0.42, s * 0.52):
        pts = []
        for i in range(25):
            x = cx - s * 0.5 + i * s * 0.5 / 24
            y = cy + dy + 6 * math.sin(i * math.pi * 2 / 12)
            pts.append((x, y))
        draw.line(pts, fill=BLUE, width=4, joint="curve")


def icon_lock(draw, cx, cy, s, color):
    # shackle
    draw.arc([cx - s * 0.22, cy - s * 0.42, cx + s * 0.22, cy + s * 0.02],
             start=180, end=360, fill=color, width=6)
    # body
    draw.rounded_rectangle([cx - s * 0.3, cy - s * 0.02,
                            cx + s * 0.3, cy + s * 0.4],
                           radius=8, fill=color)
    # keyhole
    draw.ellipse([cx - 5, cy + s * 0.1, cx + 5, cy + s * 0.1 + 10],
                 fill=(255, 255, 255))
    draw.line([(cx, cy + s * 0.1 + 8), (cx, cy + s * 0.28)],
              fill=(255, 255, 255), width=4)


def icon_waves(draw, cx, cy, s, color):
    for k, dy in enumerate((-s * 0.22, 0, s * 0.22)):
        pts = []
        for i in range(25):
            x = cx - s * 0.5 + i * s * 0.5 / 24
            y = cy + dy + 7 * math.sin(i * math.pi * 2 / 12 + k * 1.1)
            pts.append((x, y))
        draw.line(pts, fill=color, width=5, joint="curve")


STORIES = [
    dict(kicker="BAHRAIN  ·  IRAN STRIKES", accent=RED,
         head="Iran hits US positions in Bahrain with missiles and drones",
         body=("The IRGC said it struck US positions at Al-Riffa and "
               "Awali. Bahrain said a civilian industrial site caught "
               "fire, with no casualties; air defences stopped several "
               "attacks."),
         icon="burst"),
    dict(kicker="CLIMATE  ·  COP31", accent=GREEN,
         head="COP31 stalls in overtime as fossil talks collapse",
         body=("The draft dropped all fossil-fuel mentions; Panama "
               "threatened to block a deal without oil output limits."),
         icon="globe"),
    dict(kicker="MEXICO  ·  CARTEL", accent=BLUE,
         head="Mexico captures cartel boss 'El Chapo Isidro'",
         body=("Seized in Guasave, Sinaloa; 11 died in the raid. The "
               "top-10 FBI fugitive carried a $5m reward."),
         icon="badge"),
    dict(kicker="FINLAND  ·  WAR SPREADS", accent=TEAL,
         head="Russian ship hit by drones off Finland",
         body=("Sparta II drifted into Finnish waters; 16 crew "
               "evacuated. Finland suspects Ukraine; Poland blamed "
               "Russia."),
         icon="ship"),
    dict(kicker="USA  ·  CYBER", accent=PURPLE,
         head="FBI crime database reportedly hacked",
         body=("The FBI is investigating a reported breach of its NCIC "
               "database — the second FBI system hit in months."),
         icon="lock"),
    dict(kicker="NIGERIA  ·  DISASTER", accent=BROWN,
         head="Overloaded boat capsizes in Nigeria, at least 24 dead",
         body=("The boat was carrying mourners to a funeral in Bayelsa "
               "when it overturned; 24 were rescued. As many as 300 "
               "people were on board."),
         icon="waves"),
]


def draw_icon(draw, kind, cx, cy, size, accent):
    if kind == "burst":
        icon_burst(draw, cx, cy, size * 0.5, accent)
    elif kind == "globe":
        icon_globe(draw, cx, cy, size * 0.42, accent)
    elif kind == "badge":
        icon_badge(draw, cx, cy, size * 0.45, accent)
    elif kind == "ship":
        icon_ship(draw, cx, cy, size, accent)
    elif kind == "lock":
        icon_lock(draw, cx, cy, size, accent)
    elif kind == "waves":
        icon_waves(draw, cx, cy, size, accent)


def story_card(draw, s, x, y, w, h, big=False):
    """One story card. big=True for the lead story (larger type)."""
    card(draw, x, y, w, h, s["accent"])
    head_f = F_HEAD_LEAD if big else F_HEAD
    body_f = F_BODY_LEAD if big else F_BODY
    head_lead = 38 if big else 28
    body_lead = 26 if big else 21
    icon_r = 190 if big else 72
    pad = 24
    tx = x + pad + 8
    tw = w - pad * 2 - 8 - icon_r - 16
    cy = y + h // 2
    draw_icon(draw, s["icon"], x + w - pad - icon_r // 2, cy, icon_r,
              s["accent"])
    yy = y + 16 if not big else y + 20
    draw.text((tx, yy), s["kicker"], font=F_KICKER, fill=s["accent"])
    yy += 24 if not big else 30
    head_lines = wrap(draw, s["head"], head_f, tw)[:2]
    yy = text_block(draw, tx, yy, head_lines, head_f, INK, head_lead)
    yy += 4
    body_lines = wrap(draw, s["body"], body_f, tw)[:3 if big else 3]
    text_block(draw, tx, yy, body_lines, body_f, MUTED, body_lead)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ---------------------------------------------------------
    draw.rectangle([0, 0, W, 118], fill=INK)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((W - tw) / 2, 16), title, font=F_TITLE, fill=(255, 255, 255))
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = draw.textlength(date, font=F_DATE)
    draw.text(((W - dw) / 2, 80), date, font=F_DATE, fill=GOLD)

    strip = "Six stories that defined the day"
    sw = draw.textlength(strip, font=F_STRIP)
    draw.text(((W - sw) / 2, 128), strip, font=F_STRIP, fill=MUTED)
    draw.line([(28, 156), (W - 28, 156)], fill=CARD_EDGE, width=2)

    # --- lead story: Bahrain, full width ----------------------------------
    story_card(draw, STORIES[0], 28, 168, W - 56, 232, big=True)

    # --- grid: stories 2-5, two columns x two rows ------------------------
    gx, gy = 28, 412
    gw, gh = 474, 180
    gap = 20
    for i, s in enumerate(STORIES[1:5]):
        cx = gx + (i % 2) * (gw + gap)
        cy = gy + (i // 2) * (gh + gap)
        story_card(draw, s, cx, cy, gw, gh)

    # --- last story: Nigeria boat, full width ------------------------------
    story_card(draw, STORIES[5], 28, 796, W - 56, 140)

    # --- footer ------------------------------------------------------------
    foot = "THE WORLD IN ONE DAY  ·  22 NOVEMBER 2026  ·  make.fun news-image"
    fw = draw.textlength(foot, font=F_FOOT)
    draw.text(((W - fw) / 2, 956), foot, font=F_FOOT, fill=MUTED)

    img.save(out, format="PNG")
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
