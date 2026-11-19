#!/usr/bin/env python3
"""Render the entry image for news-image-20261118: a TV news broadcast
frame, 1024x576, drawn with PIL primitives only (no photos, no network).

All six stories are the verified Wednesday 18 November 2026 facts from
the brief. Broadcast layout, as fractions of the 576 px height:
masthead 8%, breaking banner 7%, middle 63% (schematic panel 66% of the
width + headline rail 34%), lead lower-third 14%, ticker 8%.
A 4% safe margin is kept on the left and right.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 576
EDGE = 41                     # 4% safe margin
EDGE_R = CANVAS_W - EDGE

INK_NAVY = (8, 21, 37)
INK_PANEL = (13, 33, 56)
INK_LOWER = (11, 29, 49)
INK_RED = (200, 16, 46)
INK_WHITE = (255, 255, 255)
INK_MIST = (215, 227, 244)
INK_GREY = (169, 192, 222)
INK_FAINT = (120, 145, 175)
INK_AMBER = (255, 213, 74)
INK_RULE = (30, 58, 86)
INK_SEA = (9, 30, 52)
INK_SEA_DEEP = (7, 24, 43)
INK_LAND = (64, 78, 58)
INK_LAND_EDGE = (96, 112, 88)
INK_SAND = (150, 138, 96)
INK_FLAME = (255, 138, 0)
INK_SMOKE = (90, 104, 122)

HEAVY = [
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
LIGHT = [
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def pick_font(px, heavy=True):
    """First usable face from the candidate list, else the bitmap font."""
    for path in HEAVY if heavy else LIGHT:
        if os.path.exists(path):
            return ImageFont.truetype(path, px)
    return ImageFont.load_default()


def measure(canvas, text, face):
    return canvas.textlength(text, font=face)


def fit_face(canvas, text, px, limit, heavy=True, floor=12):
    """Largest face size at or under px whose text fits inside limit."""
    size = px
    face = pick_font(size, heavy)
    while size > floor and measure(canvas, text, face) > limit:
        size -= 1
        face = pick_font(size, heavy)
    return face


def flow_lines(canvas, text, face, limit):
    """Greedy word wrap into lines no wider than limit."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if not current or measure(canvas, trial, face) <= limit:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def burst(canvas, cx, cy, outer, inner):
    """Jagged starburst: orange spikes, amber core, white centre."""
    spikes = []
    for k in range(24):
        radius = outer if k % 2 == 0 else outer * 0.47
        ang = math.radians(k * 15)
        spikes.append((cx + int(radius * math.cos(ang)),
                       cy + int(radius * math.sin(ang))))
    canvas.polygon(spikes, fill=INK_FLAME)
    core = []
    for k in range(16):
        radius = inner if k % 2 == 0 else inner * 0.45
        ang = math.radians(k * 22.5 + 11)
        core.append((cx + int(radius * math.cos(ang)),
                     cy + int(radius * math.sin(ang))))
    canvas.polygon(core, fill=INK_AMBER)
    canvas.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=INK_WHITE)


def draw_hormuz(canvas, x0, y0, x1, y1):
    """Schematic of the Strait of Hormuz inside the given box.

    Top land = Iran, bottom land = the Arabian Peninsula, the strait
    between them. Qeshm island sits in the strait; Bahrain and Kuwait
    are marked up in the Gulf to the left. A burst marks the strike
    on Qeshm and small drone silhouettes fly over the water.
    """
    canvas.rectangle([x0, y0, x1, y1], fill=INK_SEA)
    # Subtle depth bands in the water.
    for i, band_y in enumerate((y0 + 90, y0 + 170, y0 + 250)):
        canvas.line([x0 + 30 + i * 40, band_y, x1 - 40 - i * 30, band_y],
                    fill=(38, 78, 120), width=2)
    # Iran coast along the top.
    canvas.polygon([(x0, y0), (x1, y0), (x1, y0 + 58), (x0 + 470, y0 + 78),
                    (x0 + 300, y0 + 66), (x0, y0 + 92)], fill=INK_LAND)
    canvas.line([(x0, y0 + 92), (x0 + 300, y0 + 66), (x0 + 470, y0 + 78),
                 (x1, y0 + 58)], fill=INK_LAND_EDGE, width=2)
    canvas.text((x0 + 170, y0 + 12), "IRAN", font=pick_font(20),
                fill=INK_MIST)
    # Arabian Peninsula coast along the bottom.
    canvas.polygon([(x0, y1), (x1, y1), (x1, y1 - 64), (x0 + 420, y1 - 84),
                    (x0 + 180, y1 - 70), (x0, y1 - 96)], fill=INK_LAND)
    canvas.line([(x0, y1 - 96), (x0 + 180, y1 - 70), (x0 + 420, y1 - 84),
                 (x1, y1 - 64)], fill=INK_LAND_EDGE, width=2)
    canvas.text((x0 + 26, y1 - 62), "ARABIAN PENINSULA",
                font=pick_font(16), fill=INK_MIST)
    # Strait label across the water.
    label = "STRAIT OF HORMUZ"
    face = pick_font(19)
    canvas.text(((x0 + x1 - measure(canvas, label, face)) / 2, y0 + 132),
                label, font=face, fill=INK_GREY)
    # Qeshm island: long narrow landmass in the strait, right of centre.
    island = [(x0 + 330, y0 + 168), (x0 + 560, y0 + 150),
              (x0 + 596, y0 + 176), (x0 + 540, y0 + 196),
              (x0 + 360, y0 + 200), (x0 + 322, y0 + 186)]
    canvas.polygon(island, fill=INK_SAND)
    canvas.line(island + [island[0]], fill=(110, 100, 66), width=2)
    face = pick_font(16)
    canvas.text((x0 + 396, y0 + 208), "QESHM ISLAND", font=face,
                fill=INK_WHITE)
    # Strike burst on Qeshm, smoke rising above it.
    bx, by = x0 + 470, y0 + 168
    burst(canvas, bx, by, 30, 18)
    for cx, cy, cr in ((bx - 24, by - 38, 12), (bx + 4, by - 54, 16),
                       (bx + 30, by - 36, 11)):
        canvas.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                       fill=INK_SMOKE)
    # Small drone silhouettes over the water, left of the island.
    for dx, dy, s in ((x0 + 150, y0 + 220, 1.0), (x0 + 210, y0 + 246, 0.8),
                      (x0 + 120, y0 + 268, 0.7)):
        w = int(26 * s)
        canvas.line([dx - w, dy, dx + w, dy], fill=INK_WHITE, width=2)
        canvas.line([dx, dy - int(6 * s), dx, dy + int(6 * s)],
                    fill=INK_WHITE, width=2)
        canvas.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=INK_WHITE)
    # Gulf markers: Kuwait and Bahrain, up in the Gulf (top-left water).
    for mx, my, name in ((x0 + 120, y0 + 118, "KUWAIT"),
                         (x0 + 210, y0 + 118, "BAHRAIN")):
        canvas.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=INK_RED)
        canvas.ellipse([mx - 10, my - 10, mx + 10, my + 10],
                       outline=INK_RED, width=2)
        canvas.text((mx + 14, my - 9), name, font=pick_font(15),
                    fill=INK_WHITE)
    canvas.text((x0 + 26, y0 + 96), "PERSIAN GULF", font=pick_font(15),
                fill=INK_FAINT)


def build():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), INK_NAVY)
    c = ImageDraw.Draw(img)

    # ---- Masthead: 8% (0-46) ----
    c.rectangle([EDGE, 11, EDGE + 30, 35], fill=INK_RED)
    c.text((EDGE + 7, 12), "G", font=pick_font(20), fill=INK_WHITE)
    c.text((EDGE + 38, 11), "GLOBAL 18", font=pick_font(25),
           fill=INK_WHITE)
    centre = "WORLD TONIGHT"
    face_c = pick_font(26)
    c.text(((CANVAS_W - measure(c, centre, face_c)) / 2, 9), centre,
           font=face_c, fill=INK_WHITE)
    date = "18 NOV 2026"
    face_d = pick_font(24)
    c.text((EDGE_R - measure(c, date, face_d), 11), date, font=face_d,
           fill=INK_WHITE)
    c.line([0, 46, CANVAS_W, 46], fill=INK_RULE, width=1)

    # ---- Breaking banner: 7% (46-86) ----
    c.rectangle([0, 46, CANVAS_W, 86], fill=INK_RED)
    face_b = pick_font(24)
    c.text((EDGE, 53), "BREAKING", font=face_b, fill=INK_WHITE)
    after = EDGE + measure(c, "BREAKING  ", face_b)
    c.text((after, 53), "•  US STRIKES IRAN SITE; IRAN HITS GULF BASES",
           font=face_b, fill=INK_WHITE)

    # ---- Middle: 63% (86-449) ----
    top, bottom = 86, 449
    panel_end = EDGE + 622
    rail_start = panel_end + 12

    # Schematic panel.
    c.rectangle([EDGE, top, panel_end, bottom], fill=INK_PANEL)
    draw_hormuz(c, EDGE + 2, top + 2, panel_end - 2, bottom - 2)
    # Yellow locator tab + FILE bug.
    c.rectangle([EDGE + 14, top + 12, EDGE + 104, top + 42],
                fill=INK_AMBER)
    c.text((EDGE + 24, top + 15), "GULF", font=pick_font(19),
           fill=(0, 0, 0))
    c.rectangle([panel_end - 74, top + 12, panel_end - 14, top + 42],
                fill=(20, 20, 20))
    c.rectangle([panel_end - 74, top + 12, panel_end - 14, top + 42],
                outline=(150, 150, 150), width=1)
    c.text((panel_end - 64, top + 15), "FILE", font=pick_font(19),
           fill=INK_WHITE)
    # Caption strip at the panel bottom.
    c.rectangle([EDGE, bottom - 28, panel_end, bottom], fill=(5, 13, 24))
    c.text((EDGE + 14, bottom - 24),
           "STRAIT OF HORMUZ  •  SCHEMATIC ILLUSTRATION",
           font=pick_font(14, heavy=False), fill=INK_GREY)

    # Headline rail: stories 02-06.
    rail = [
        ("02", "KERCH BRIDGE HIT",
         "Second day of attacks; a road span falls"),
        ("03", "XI, PUTIN MEET IN SHENZHEN",
         "Ahead of Thursday's trilateral with Trump"),
        ("04", "PELTOLA WINS ALASKA",
         "Beats incumbent Sullivan; AP calls the race"),
        ("05", "EBOLA PASSES 11,000 CASES",
         "Cases doubled in 3 months; 5,400 dead"),
        ("06", "VOYAGER 1 ONE LIGHT-DAY",
         "Farthest human-made object, ~16 billion miles"),
    ]
    rail_w = EDGE_R - rail_start
    slot = (bottom - top) / 5.0
    for i, (num, head, sub) in enumerate(rail):
        iy = top + int(i * slot)
        if i:
            c.line([rail_start, iy, EDGE_R, iy], fill=INK_RULE, width=1)
        c.text((rail_start, iy + 8), num, font=pick_font(18),
               fill=INK_RED)
        hx = rail_start + 34
        hw = EDGE_R - hx
        face_h = pick_font(21)
        lines = flow_lines(c, head, face_h, hw)
        while len(lines) > 2 and face_h.size > 17:
            face_h = pick_font(face_h.size - 1)
            lines = flow_lines(c, head, face_h, hw)
        y = iy + 5
        for line in lines[:2]:
            c.text((hx, y), line, font=face_h, fill=INK_WHITE)
            y += face_h.size + 3
        face_s = fit_face(c, sub, 16, rail_w, heavy=False, floor=13)
        c.text((rail_start, iy + int(slot) - 22), sub, font=face_s,
               fill=INK_GREY)

    # ---- Lead lower-third: 14% (449-530) ----
    c.rectangle([0, 449, CANVAS_W, 530], fill=INK_LOWER)
    c.rectangle([0, 449, 8, 530], fill=INK_RED)
    c.text((EDGE + 16, 452), "US–IRAN GULF STRIKES", font=pick_font(15),
           fill=INK_AMBER)
    lead = "US HITS QESHM; IRAN STRIKES GULF BASES"
    face_l = fit_face(c, lead, 37, EDGE_R - (EDGE + 16), floor=28)
    c.text((EDGE + 16, 466), lead, font=face_l, fill=INK_WHITE)
    c.text((EDGE + 16, 506),
           "US hits Qeshm missile site; Iran strikes Kuwait and Bahrain",
           font=pick_font(17, heavy=False), fill=INK_MIST)

    # ---- Ticker: 8% (530-576) ----
    c.rectangle([0, 530, CANVAS_W, 576], fill=(5, 13, 24))
    c.line([0, 530, CANVAS_W, 530], fill=INK_RED, width=3)
    c.rectangle([EDGE, 537, EDGE + 168, 569], fill=INK_RED)
    tab = "WORLD UPDATE"
    face_t = pick_font(17)
    c.text((EDGE + (168 - measure(c, tab, face_t)) / 2, 541), tab,
           font=face_t, fill=INK_WHITE)
    tick = ("US loses measles-free status after 26 years as cases pass "
            "5,400.   •   Israel elects Matan Kahana as Knesset speaker.")
    face_k = fit_face(c, tick, 17, EDGE_R - (EDGE + 184), heavy=False,
                      floor=13)
    c.text((EDGE + 184, 542), tick, font=face_k, fill=INK_WHITE)

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
