#!/usr/bin/env python3
"""Render the 24 November 2026 world-news infographic (1024x1024 PNG).

Drawn entirely with PIL: masthead with the date, six story blocks each
with a small drawn pictogram, a headline and a one-line summary, plus a
footer strip of three more stories reported today. No AI image generation.
All stories were first reported on Tuesday 24 November 2026.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
MUTED = (90, 96, 110)
CARD = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)

STORIES = [
    {
        "tag": "ASIA  •  SECURITY",
        "color": (30, 90, 168),
        "icon": "jet",
        "head": "Russian jet enters South Korean airspace",
        "body": "Seoul briefly orders Ulleung islanders to shelter; the jet leaves after a warning.",
    },
    {
        "tag": "EUROPE  •  SPACE",
        "color": (120, 40, 140),
        "icon": "satellite",
        "head": "NATO vows space defence over satellite weapon",
        "body": "Allies warn Moscow may launch one next month, German media report.",
    },
    {
        "tag": "USA  •  POLITICS",
        "color": (178, 34, 34),
        "icon": "capitol",
        "head": "Congressman Gomez resigns after ethics finding",
        "body": "Democrat Jimmy Gomez quits after a House panel finds sexual misconduct.",
    },
    {
        "tag": "USA  •  TECH",
        "color": (20, 120, 110),
        "icon": "chat",
        "head": "States sue Musk firms over Grok images",
        "body": "Lawsuits say the AI chatbot produced sexualised images.",
    },
    {
        "tag": "WORLD  •  CLIMATE",
        "color": (40, 130, 60),
        "icon": "globe",
        "head": "COP31 talks stall on cover text",
        "body": "Negotiators fail to agree a closing text, dealing ocean-climate action a setback.",
    },
    {
        "tag": "UK  •  COURTS",
        "color": (200, 120, 20),
        "icon": "pad",
        "head": "GTA VI hacker jailed 7 years - and walks free",
        "body": "Arion Kurtaj, 21, is freed on time served after the 2021-22 Rockstar Games hacks.",
    },
]

ALSO = ("Also today:  World chess title defence opens in Geneva  •  "
        "More bodies found after Indonesia factory fire  •  "
        "Storms threaten US Thanksgiving travel")


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, cx, cy, r, color):
    """Simple flat pictogram inside a circle of radius r centred (cx, cy)."""
    if kind == "jet":
        d.polygon([(cx - r, cy + r * 0.55), (cx + r * 0.9, cy - r * 0.25),
                   (cx + r * 0.35, cy + r * 0.1), (cx + r * 0.1, cy + r * 0.8)],
                  fill=color)
        d.polygon([(cx - r * 0.5, cy + r * 0.1), (cx + r * 0.1, cy - r * 0.6),
                   (cx + r * 0.45, cy - r * 0.1)], fill=color)
    elif kind == "satellite":
        d.rectangle([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
                    fill=color)
        d.rectangle([cx - r * 0.95, cy - r * 0.45, cx - r * 0.35, cy + r * 0.45],
                    outline=color, width=4)
        d.rectangle([cx + r * 0.35, cy - r * 0.45, cx + r * 0.95, cy + r * 0.45],
                    outline=color, width=4)
        d.line([cx - r * 0.35, cy, cx - r * 0.95, cy], fill=color, width=4)
        d.line([cx + r * 0.35, cy, cx + r * 0.95, cy], fill=color, width=4)
        d.ellipse([cx - r * 0.12, cy - r * 0.12, cx + r * 0.12, cy + r * 0.12],
                  fill=(255, 255, 255))
    elif kind == "capitol":
        d.pieslice([cx - r * 0.55, cy - r * 0.85, cx + r * 0.55, cy + r * 0.25],
                   180, 360, fill=color)
        d.rectangle([cx - r * 0.7, cy + r * 0.15, cx + r * 0.7, cy + r * 0.3],
                    fill=color)
        for i in range(-1, 2):
            d.rectangle([cx + i * r * 0.42 - 4, cy + r * 0.3,
                         cx + i * r * 0.42 + 4, cy + r * 0.85], fill=color)
        d.rectangle([cx - r * 0.75, cy + r * 0.85, cx + r * 0.75, cy + r * 0.95],
                    fill=color)
    elif kind == "chat":
        d.rounded_rectangle([cx - r * 0.8, cy - r * 0.75, cx + r * 0.8, cy + r * 0.45],
                            radius=12, fill=color)
        d.polygon([(cx - r * 0.35, cy + r * 0.4), (cx - r * 0.55, cy + r * 0.9),
                   (cx + r * 0.15, cy + r * 0.4)], fill=color)
        d.text((cx - 13, cy - r * 0.55), "AI", font=F_SANS_B(26),
               fill=(255, 255, 255))
    elif kind == "globe":
        d.ellipse([cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8],
                  outline=color, width=5)
        d.arc([cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8],
              200, 340, fill=color, width=5)
        d.line([cx - r * 0.8, cy, cx + r * 0.8, cy], fill=color, width=4)
        d.ellipse([cx - r * 0.35, cy - r * 0.8, cx + r * 0.35, cy + r * 0.8],
                  outline=color, width=4)
    elif kind == "pad":
        d.rounded_rectangle([cx - r * 0.85, cy - r * 0.5, cx + r * 0.85, cy + r * 0.55],
                            radius=16, fill=color)
        d.ellipse([cx - r * 0.55, cy - r * 0.15, cx - r * 0.2, cy + r * 0.2],
                  fill=(255, 255, 255))
        d.ellipse([cx + r * 0.2, cy - r * 0.15, cx + r * 0.55, cy + r * 0.2],
                  fill=(255, 255, 255))
        d.polygon([(cx + r * 0.05, cy - r * 0.35), (cx + r * 0.3, cy - r * 0.1),
                   (cx + r * 0.05, cy + r * 0.15), (cx - r * 0.2, cy - r * 0.1)],
                  fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 174], fill=RED)
    d.text((36, 18), "THE WORLD IN ONE PICTURE", font=F_SANS_B(24),
           fill=(240, 200, 90))
    date_size = 58
    while d.textlength("TUESDAY 24 NOVEMBER 2026",
                       font=F_SERIF_B(date_size)) > W - 72 and date_size > 30:
        date_size -= 2
    d.text((36, 48), "TUESDAY 24 NOVEMBER 2026", font=F_SERIF_B(date_size),
           fill=(255, 255, 255))
    d.text((36, 122), "Six stories from a Tuesday morning - first reported today, 24 November 2026",
           font=F_SANS(22), fill=(200, 210, 225))

    # ---- Story grid: 2 columns x 3 rows ----
    margin, gap = 36, 14
    col_w = (W - 2 * margin - gap) // 2
    row_h = 232
    top0 = 190
    for i, s in enumerate(STORIES):
        x = margin + (i % 2) * (col_w + gap)
        y = top0 + (i // 2) * (row_h + gap)
        d.rounded_rectangle([x, y, x + col_w, y + row_h], radius=10, fill=CARD)
        d.rectangle([x, y + 8, x + 8, y + row_h - 8], fill=s["color"])
        # pictogram disc
        cx, cy, r = x + 52, y + 52, 34
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(238, 240, 244))
        draw_icon(d, s["icon"], cx, cy, 24, s["color"])
        # tag
        d.text((x + 100, y + 22), s["tag"], font=F_SANS_B(19), fill=s["color"])
        # headline
        tx = x + 26
        tw = col_w - 52
        lines = wrap(d, s["head"], F_SANS_B(26), tw)
        yy = y + 96
        for ln in lines[:2]:
            d.text((tx, yy), ln, font=F_SANS_B(26), fill=INK)
            yy += 33
        # body
        blines = wrap(d, s["body"], F_SANS(20), tw)
        yy += 6
        for ln in blines[:2]:
            d.text((tx, yy), ln, font=F_SANS(20), fill=(52, 58, 72))
            yy += 27

    # ---- Footer ----
    fy = top0 + 3 * row_h + 2 * gap + 14
    d.rectangle([margin, fy, W - margin, fy + 2], fill=(190, 190, 180))
    flines = wrap(d, ALSO, F_SANS_B(20), W - 2 * margin)
    yy = fy + 10
    for ln in flines:
        d.text((margin, yy), ln, font=F_SANS_B(20), fill=INK)
        yy += 27
    d.text((margin, yy + 2), "Morning snapshot  •  Sources: Reuters, AP, SCMP, AFP, Japan Times",
           font=F_SERIF(18), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
