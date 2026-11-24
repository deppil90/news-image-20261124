#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page to entry.png.

Draws a newspaper-style one-page summary of Tuesday 24 November 2026
with Pillow only. Deterministic: no randomness, no network, no timestamps.
Run:  python3 draw.py            (writes entry.png next to this file)
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 86, 76)
NAVY = (14, 42, 71)
GREEN = (16, 122, 60)
RED = (178, 34, 34)
ORANGE = (214, 96, 20)
GOLD = (176, 132, 24)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left"):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        if align == "center":
            lx = x - draw.textlength(line, font=fnt) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_burst(draw, cx, cy, r, fill):
    """Simple 8-point star burst (explosion / breaking news mark)."""
    import math

    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_factory(draw, x, y, s, fill):
    """Factory silhouette: body, sawtooth roof, two chimneys, flame."""
    draw.rectangle([x, y + 0.45 * s, x + s, y + s], fill=fill)
    draw.polygon(
        [(x, y + 0.45 * s), (x + 0.33 * s, y + 0.2 * s), (x + 0.33 * s, y + 0.45 * s)],
        fill=fill,
    )
    draw.polygon(
        [(x + 0.33 * s, y + 0.45 * s), (x + 0.66 * s, y + 0.2 * s),
         (x + 0.66 * s, y + 0.45 * s)],
        fill=fill,
    )
    draw.rectangle([x + 0.7 * s, y, x + 0.82 * s, y + 0.5 * s], fill=fill)
    draw.rectangle([x + 0.86 * s, y + 0.12 * s, x + 0.95 * s, y + 0.5 * s], fill=fill)
    draw.ellipse([x + 0.68 * s, y - 0.22 * s, x + 0.86 * s, y - 0.04 * s], fill=ORANGE)
    draw.polygon(
        [(x + 0.72 * s, y - 0.05 * s), (x + 0.77 * s, y - 0.3 * s),
         (x + 0.82 * s, y - 0.05 * s)],
        fill=ORANGE,
    )


def draw_ship(draw, x, y, s, fill):
    """Cargo ship on waves with a plume of smoke."""
    draw.polygon(
        [(x, y + 0.55 * s), (x + s, y + 0.55 * s), (x + 0.85 * s, y + 0.85 * s),
         (x + 0.15 * s, y + 0.85 * s)],
        fill=fill,
    )
    draw.rectangle([x + 0.2 * s, y + 0.25 * s, x + 0.55 * s, y + 0.55 * s], fill=fill)
    draw.rectangle([x + 0.6 * s, y + 0.35 * s, x + 0.8 * s, y + 0.55 * s], fill=fill)
    draw.ellipse([x + 0.6 * s, y - 0.05 * s, x + 0.78 * s, y + 0.13 * s], fill=ORANGE)
    draw.ellipse([x + 0.68 * s, y - 0.2 * s, x + 0.82 * s, y - 0.06 * s], fill=MUTED)
    for i, wy in enumerate((0.92, 1.0)):
        draw.arc(
            [x + i * 0.3 * s, y + wy * s, x + (i + 0.45) * s, y + (wy + 0.12) * s],
            start=180, end=360, fill=NAVY, width=3,
        )


def draw_chessboard(draw, x, y, s):
    n = 4
    cell = s / n
    for r in range(n):
        for c in range(n):
            fill = INK if (r + c) % 2 == 0 else PAPER
            draw.rectangle(
                [x + c * cell, y + r * cell, x + (c + 1) * cell, y + (r + 1) * cell],
                fill=fill, outline=INK, width=1,
            )
    draw.ellipse(
        [x + 0.62 * s, y + 0.1 * s, x + 0.88 * s, y + 0.36 * s], fill=RED
    )


def draw_cricket(draw, x, y, s):
    """Red cricket ball with seam plus a bat."""
    draw.ellipse([x, y + 0.35 * s, x + 0.55 * s, y + 0.9 * s], fill=RED)
    draw.arc(
        [x + 0.08 * s, y + 0.4 * s, x + 0.47 * s, y + 0.85 * s],
        start=300, end=120, fill=PAPER, width=3,
    )
    draw.rounded_rectangle(
        [x + 0.6 * s, y, x + 0.85 * s, y + 0.62 * s], radius=6, fill=(205, 164, 110),
        outline=INK, width=2,
    )
    draw.rectangle([x + 0.68 * s, y + 0.6 * s, x + 0.77 * s, y + 0.95 * s], fill=INK)


def draw_bars(draw, x, y, s, fill):
    """Three rising bars (markets / business)."""
    heights = (0.35, 0.6, 0.9)
    bw = s * 0.22
    for i, hfrac in enumerate(heights):
        bx = x + i * (bw + s * 0.08)
        draw.rectangle([bx, y + s * (1 - hfrac), bx + bw, y + s], fill=fill)


def draw_document(draw, x, y, s, fill):
    """Signed document with a seal (deal / agreement)."""
    draw.rectangle([x, y, x + 0.7 * s, y + s], fill=PAPER, outline=fill, width=3)
    for i in range(3):
        ly = y + (0.25 + 0.2 * i) * s
        draw.line([(x + 0.12 * s, ly), (x + 0.58 * s, ly)], fill=fill, width=3)
    draw.ellipse(
        [x + 0.55 * s, y + 0.62 * s, x + 0.95 * s, y + 1.02 * s],
        fill=GOLD, outline=INK, width=2,
    )


def story_panel(draw, x, y, w, h, kicker, kicker_fill, headline, summary, icon,
                icon_size=48, head_size=23, sum_size=18, full_headline=False):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    pad = 14
    ix, iy, isize = x + pad, y + pad, icon_size
    icon(draw, ix, iy, isize)
    tx = x + pad + isize + 12
    kf = font(SANS_B, 17)
    draw.text((tx, y + pad + 2), kicker, font=kf, fill=kicker_fill)
    hf = font(SANS_B, head_size)
    if full_headline:
        hy = y + pad + isize + 8
        lines = wrap(draw, headline, hf, w - 2 * pad)
        yy = text_block(draw, x + pad, hy, lines[:2], hf,
                        leading=int(head_size * 1.15))
    else:
        tw = (x + w - pad) - tx
        lines = wrap(draw, headline, hf, tw)
        yy = text_block(draw, tx, y + pad + 26, lines[:2], hf,
                        leading=int(head_size * 1.22))
    sf = font(SANS, sum_size)
    slines = wrap(draw, summary, sf, w - 2 * pad)
    text_block(draw, x + pad, yy + 8, slines[:2], sf, fill=MUTED,
               leading=int(sum_size * 1.22))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # page margin

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 28), title, font=tf, fill=INK)
    df = font(SANS_B, 25)
    date_line = "TUESDAY,  24  NOVEMBER  2026"
    dw = d.textlength(date_line, font=df)
    d.text(((W - dw) / 2, 104), date_line, font=df, fill=NAVY)
    hrule(d, mx, W - mx, 148, width=3)
    hrule(d, mx, W - mx, 154, width=1)

    # ---- Hero: Nvidia ----
    hx, hy, hw, hh = mx, 168, W - 2 * mx, 280
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=NAVY)
    # rising chart on the right
    chart = [
        (hx + 640, hy + 222), (hx + 700, hy + 200), (hx + 760, hy + 208),
        (hx + 820, hy + 158), (hx + 880, hy + 172), (hx + 930, hy + 104),
    ]
    d.line(chart, fill=(110, 220, 140), width=6, joint="curve")
    d.polygon(
        [(hx + 930, hy + 110), (hx + 906, hy + 118), (hx + 922, hy + 136)],
        fill=(110, 220, 140),
    )
    for px, py in chart:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(110, 220, 140))
    bf = font(SANS_B, 64)
    d.text((hx + 640, hy + 18), "+31.5%", font=bf, fill=(110, 220, 140))
    sf = font(SANS, 22)
    d.text((hx + 640, hy + 92), "Nvidia shares in one day", font=sf, fill=(200, 210, 225))
    kf = font(SANS_B, 20)
    d.text((hx + 28, hy + 22), "MARKETS  •  THE LEAD STORY", font=kf, fill=(110, 220, 140))
    hf = font(SANS_B, 38)
    head = wrap(d, "Huang returns to Nvidia — shares soar, Asia rallies", hf, 600)
    text_block(d, hx + 28, hy + 58, head[:2], hf, fill=(255, 255, 255), leading=46)
    sf2 = font(SANS, 23)
    sub = wrap(
        d,
        "Nvidia regains nearly $1 trillion in a day. Nikkei +4.5%, Kospi +7.5%, Taiwan +9.1%.",
        sf2, 600,
    )
    text_block(d, hx + 28, hy + 162, sub[:3], sf2, fill=(205, 215, 228), leading=30)

    # ---- Middle grid: 2 x 2 ----
    gy = 462
    gw = (W - 2 * mx - 14) // 2
    gh = 150
    story_panel(
        d, mx, gy, gw, gh, "GAZA", RED,
        "Israeli strike kills at least three in Khan Younis",
        "Medics say an airstrike hit near a police post in the southern Gaza Strip.",
        lambda dr, x, y, s: draw_burst(dr, x + s / 2, y + s / 2, s * 0.42, ORANGE),
    )
    story_panel(
        d, mx + gw + 14, gy, gw, gh, "INDONESIA", ORANGE,
        "Factory fire kills at least 24; dozens missing",
        "Rescuers search a burnt-out candy factory as the toll climbs.",
        lambda dr, x, y, s: draw_factory(dr, x, y + 6, s - 6, NAVY),
    )
    story_panel(
        d, mx, gy + gh + 14, gw, gh, "UKRAINE WAR", NAVY,
        "Russian cargo ship ablaze after drone strike",
        "Sparta II burns in the Gulf of Finland; Russian strikes hit the Kyiv region.",
        lambda dr, x, y, s: draw_ship(dr, x, y + 4, s - 4, NAVY),
    )
    story_panel(
        d, mx + gw + 14, gy + gh + 14, gw, gh, "SOUTH ASIA", GREEN,
        "Modi and Nepal's PM Shah sign eight deals",
        "A Rs 15,000-crore package for energy, trade and connectivity.",
        lambda dr, x, y, s: draw_document(dr, x + 6, y + 4, s - 8, NAVY),
    )

    # ---- Bottom row: 3 small panels ----
    by = gy + 2 * gh + 14
    bw = (W - 2 * mx - 28) // 3
    bh = 160
    panels = [
        ("CHESS", NAVY, "World title match opens in Geneva",
         "Champion Gukesh defends his crown against Sindarov.",
         lambda dr, x, y, s: draw_chessboard(dr, x, y + 4, s - 4)),
        ("CRICKET", RED, "India–NZ Test drawn at Wellington",
         "New Zealand hold on at 239 for 5 on the final day.",
         lambda dr, x, y, s: draw_cricket(dr, x, y + 4, s - 4)),
        ("BUSINESS", GOLD, "StarHub to buy M1 in $3.8bn deal",
         "Dollar nears a 20-month high as Fed hike bets rise.",
         lambda dr, x, y, s: draw_bars(dr, x, y + 8, s - 8, GREEN)),
    ]
    for i, (kick, kfill, head, summ, icon) in enumerate(panels):
        story_panel(
            d, mx + i * (bw + 14), by, bw, bh, kick, kfill, head, summ, icon,
            icon_size=36, head_size=22, sum_size=17, full_headline=True,
        )

    # ---- Footer ----
    fy = by + bh + 18
    hrule(d, mx, W - mx, fy, width=2)
    ff = font(SANS, 19)
    foot = "Headlines as reported on Tuesday, 24 November 2026  •  One day, one picture."
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy + 10), foot, font=ff, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
