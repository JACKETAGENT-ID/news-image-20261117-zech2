#!/usr/bin/env python3
"""Draw "THE WORLD TODAY" -- a dense modern tabloid front page summing up
Tuesday 17 November 2026. Deterministic: fixed fonts, fixed geometry, no
randomness, no timestamps, no network. Run: python3 draw.py -> entry.png
(1024x1024, PNG, well under 1 MiB). Written from scratch for zech's v2 entry.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- palette (own scheme: ink navy, paper cream, crimson, teal, amber) ----
PAPER = (246, 241, 230)
INK = (18, 38, 58)
NAVY = (15, 32, 50)
CRIMSON = (179, 39, 30)
TEAL = (14, 107, 107)
AMBER = (217, 142, 0)
GREY = (90, 96, 104)
LIGHT = (255, 255, 255)
SKY = (168, 196, 214)
SEA = (38, 84, 104)
RULE = (18, 38, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap to pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, fill, max_w, leading=None):
    lines = wrap(text, fnt, max_w, d)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hline(d, x0, x1, y, fill, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------------------
# Flat vector illustrations (drawn, no photos, no copied art)
# ---------------------------------------------------------------------------
def draw_bridge_scene(d, x, y, w, h):
    """Kerch bridge at dusk: broken deck, smoke, blast glow."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    d.ellipse([x + w - 92, y + 14, x + w - 32, y + 74], fill=(232, 178, 84))
    # distant headland
    d.polygon([(x, y + h - 58), (x + 90, y + h - 96), (x + 190, y + h - 58)],
              fill=(96, 118, 132))
    # sea
    d.rectangle([x, y + h - 52, x + w, y + h], fill=SEA)
    for i in range(5):
        yy = y + h - 44 + i * 9
        d.line([(x + 12 + i * 34, yy), (x + 60 + i * 40, yy)],
               fill=(88, 138, 158), width=2)
    # bridge deck: left span intact, middle collapsed, right span tilted
    deck_y = y + h - 108
    d.rectangle([x, deck_y, x + int(w * 0.42), deck_y + 10], fill=(52, 58, 66))
    d.polygon([(x + int(w * 0.42), deck_y),
               (x + int(w * 0.50), deck_y + 34),
               (x + int(w * 0.50), deck_y + 44),
               (x + int(w * 0.42), deck_y + 10)], fill=(52, 58, 66))
    d.rectangle([x + int(w * 0.62), deck_y - 14, x + w, deck_y - 4],
                fill=(52, 58, 66))
    # pylons
    for px in (x + 60, x + int(w * 0.30), x + int(w * 0.82)):
        d.rectangle([px, deck_y - 62, px + 8, deck_y], fill=(52, 58, 66))
    # cables on the right span
    d.line([(x + int(w * 0.82), deck_y - 62), (x + int(w * 0.62), deck_y - 14)],
           fill=(120, 128, 136), width=2)
    d.line([(x + int(w * 0.82), deck_y - 62), (x + w - 8, deck_y - 4)],
           fill=(120, 128, 136), width=2)
    # blast glow + smoke over the gap
    gx, gy = x + int(w * 0.52), deck_y - 6
    d.ellipse([gx - 34, gy - 30, gx + 34, gy + 26], fill=(232, 120, 40))
    d.ellipse([gx - 18, gy - 16, gx + 18, gy + 14], fill=(244, 196, 80))
    for cx, cy, r, col in ((gx - 44, gy - 52, 26, (120, 124, 128)),
                           (gx - 8, gy - 72, 32, (140, 144, 148)),
                           (gx + 34, gy - 56, 24, (110, 114, 118))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def draw_tanker(d, x, y, w, h):
    """Oil tanker at sea with a smoke plume."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 205, 220))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(44, 92, 110))
    for i in range(3):
        yy = y + int(h * 0.70) + i * 10
        d.line([(x + 6, yy), (x + 30, yy)], fill=(96, 150, 168), width=2)
    # hull
    d.polygon([(x + 4, y + int(h * 0.52)), (x + w - 4, y + int(h * 0.52)),
               (x + w - 18, y + int(h * 0.66)), (x + 18, y + int(h * 0.66))],
              fill=(139, 32, 26))
    # containers
    cx = x + 14
    for col in ((217, 142, 0), (14, 107, 107), (220, 220, 210)):
        d.rectangle([cx, y + int(h * 0.34), cx + 26, y + int(h * 0.52)],
                    fill=col, outline=(60, 60, 60))
        cx += 30
    # funnel + smoke
    d.rectangle([x + w - 34, y + int(h * 0.36), x + w - 18, y + int(h * 0.52)],
                fill=(40, 44, 50))
    for sx, sy, r in ((x + w - 26, y + 12, 12), (x + w - 34, y + 22, 15),
                      (x + w - 16, y + 24, 10)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 124, 128))


def draw_jets(d, x, y, w, h):
    """Two fighter jets over a rising-sun disc."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 228))
    d.ellipse([x + w - 66, y + 10, x + w - 10, y + 66], fill=(232, 178, 84))
    for jx, jy, s in ((x + 12, y + 26, 1.0), (x + 44, y + 52, 0.8)):
        pts = [(jx, jy + int(10 * s)), (jx + int(46 * s), jy + int(16 * s)),
               (jx + int(46 * s), jy + int(22 * s)), (jx, jy + int(28 * s))]
        d.polygon(pts, fill=(52, 58, 66))
        d.polygon([(jx + int(30 * s), jy + int(6 * s)),
                   (jx + int(38 * s), jy + int(16 * s)),
                   (jx + int(30 * s), jy + int(26 * s))], fill=(52, 58, 66))
    d.line([(x + 8, y + h - 18), (x + w - 8, y + h - 18)], fill=(140, 150, 158),
           width=2)


def draw_court(d, x, y, w, h):
    """Courthouse portico: pediment, columns, steps."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 206, 190))
    d.polygon([(x + 8, y + 26), (x + w // 2, y + 6), (x + w - 8, y + 26)],
              fill=(52, 58, 66))
    d.rectangle([x + 8, y + 26, x + w - 8, y + 34], fill=(52, 58, 66))
    for i in range(4):
        cx = x + 16 + i * 24
        d.rectangle([cx, y + 38, cx + 10, y + h - 22], fill=(240, 236, 224),
                    outline=(120, 116, 108))
    d.rectangle([x + 8, y + h - 22, x + w - 8, y + h - 14], fill=(52, 58, 66))
    d.rectangle([x + 4, y + h - 14, x + w - 4, y + h - 6], fill=(90, 88, 82))


# ---------------------------------------------------------------------------
# Stories -- every item was first reported on Tuesday 17 November 2026
# (BBC, AFP, Al Jazeera, Le Monde, Reuters/AP wires, COP31 presidency).
# ---------------------------------------------------------------------------
RAIL = [
    ("WAR AT SEA", "FOURTH TANKER HIT IN HORMUZ",
     "Mine blast sets a tanker ablaze; Iran seizes a US drone.",
     draw_tanker),
    ("ASIA", "JETS SCRAMBLED OVER JAPAN",
     "Tokyo sends fighters up and protests the airspace breach.",
     draw_jets),
    ("FRANCE", "DEPARDIEU ADMITS GUILT",
     "Film star drops his appeal and pleads guilty in Paris.",
     draw_court),
]

# (tag, colour, headline)
BRIEF = [
    ("WORLD", CRIMSON, "Trump: US takes 'very seriously' alleged Iran plot on Washington"),
    ("WORLD", CRIMSON, "Xi, Trump, Putin to hold first trilateral summit in Shenzhen"),
    ("WAR", CRIMSON, "Iran drone hits US base in Bahrain, third strike in five days"),
    ("WAR", CRIMSON, "Zaporizhzhia toll rises to 40; aid-centre strike kills 26"),
    ("MIDEAST", TEAL, "UK, Australia, Canada, Italy urge Israel to open Gaza crossings"),
    ("MIDEAST", TEAL, "Settlers kill woman, 72, in West Bank"),
    ("ASIA", TEAL, "Mongolia's president resigns amid corruption scandal"),
    ("EUROPE", TEAL, "146,000 march across France demanding higher pay"),
    ("CLIMATE", TEAL, "COP31 ministers take over in Antalya as draft deal draws fire"),
    ("CLIMATE", TEAL, "Draft: fossil-fuel phaseout, $120bn climate aid by 2035"),
    ("USA", NAVY, "FEMA tests emergency alert nationwide at 2:20 p.m. \u2014 no blackout"),
    ("TECH", NAVY, "Nvidia climbs ahead of earnings; US curbs chips to China"),
    ("HEALTH", NAVY, "US loses measles-free status after 26 years; 5,400 cases"),
    ("USA", NAVY, "Pentagon fails its audit for the ninth year in a row"),
    ("SPORT", AMBER, "India edge Pakistan 2\u20131 to win SAFF final in Dhaka"),
    ("SPORT", AMBER, "Germany rout Netherlands 5\u20130"),
    ("WORLD", CRIMSON, "Houthis advance in Yemen; troops pull back to defend Aden"),
    ("WORLD", CRIMSON, "Moldova: Russian drone over Chisinau, Sandu says"),
]

TIMELINE = [
    ("09:00 PKT", "Pakistan cuts petrol and diesel by Rs2 a litre"),
    ("14:20 ET", "FEMA's nationwide alert test sounds; officials: \u201cNo blackout\u201d"),
    ("17:00 CET", "France marches end in Paris; unions count 146,000 nationwide"),
    ("21:04 GMT", "US loses measles elimination status after 26 years"),
    ("21:06 GMT", "Russian military plane crashes in Kemerovo; 19 dead"),
    ("21:24 GMT", "Crimea bridge partly collapses after Ukrainian strike"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 20  # page margin

    # ---- masthead ----
    d.rectangle([M, 14, W - M, 118], fill=NAVY)
    d.rectangle([M, 118, W - M, 122], fill=CRIMSON)
    d.text((M + 18, 26), "THE WORLD TODAY", font=SERIF_B(56), fill=LIGHT)
    d.text((M + 20, 92), "ONE DAY \u2022 ONE PAGE \u2022 EVERY STORY THAT MATTERED",
           font=SANS_B(13), fill=(200, 214, 226))
    d.text((W - M - 252, 30), "TUESDAY", font=SANS_B(30), fill=AMBER)
    d.text((W - M - 252, 62), "17 NOVEMBER 2026", font=SANS_B(22), fill=LIGHT)
    d.text((W - M - 252, 92), "28 STORIES \u2022 FREE", font=SANS_B(13),
           fill=(200, 214, 226))

    # ---- dateline strip ----
    d.text((M, 132), "TUESDAY 17 NOVEMBER 2026 \u2014 THE DAY IN FULL",
           font=SANS_B(15), fill=CRIMSON)
    d.text((W - M - 300, 132), "ALL EVENTS REPORTED TODAY",
           font=SANS_B(13), fill=GREY)

    # ---- lead story: Crimea bridge (drawn on a temp layer: clipped) ----
    LX, LY, LW = M, 158, 636
    scene = Image.new("RGB", (LW, 168), SKY)
    draw_bridge_scene(ImageDraw.Draw(scene), 0, 0, LW, 168)
    img.paste(scene, (LX, LY))
    y = LY + 178
    d.text((LX, y), "WAR IN UKRAINE \u2014 LEAD STORY", font=SANS_B(14),
           fill=CRIMSON)
    y += 22
    y = draw_wrapped(d, LX, y, "CRIMEA BRIDGE IN RUINS", SERIF_B(38), INK,
                     LW, leading=44)
    y += 4
    y = draw_wrapped(
        d, LX, y,
        "Kyiv says a missile-and-drone strike, weeks in the planning, partly "
        "collapses the Kerch crossing; Zelensky hails an \u201cunprecedented\u201d "
        "blow. Moscow answers with strikes on Kyiv bridges.",
        SANS(16), INK, LW, leading=21)
    hline(d, LX, LX + LW, 478, RULE, 2)

    # ---- right rail: three stories ----
    RX, RW = 676, W - M - 676
    ry = 158
    for tag, head, deck, art in RAIL:
        d.rectangle([RX, ry, RX + RW, ry + 100], fill=LIGHT,
                    outline=(200, 194, 178))
        art(d, RX + 8, ry + 8, 92, 84)
        tx = RX + 110
        d.text((tx, ry + 8), tag, font=SANS_B(12), fill=CRIMSON)
        ty = draw_wrapped(d, tx, ry + 26, head, SANS_B(17), INK, RW - 120,
                          leading=20)
        draw_wrapped(d, tx, ty + 2, deck, SANS(11), GREY, RW - 120, leading=14)
        ry += 112
    hline(d, RX, RX + RW, 478, RULE, 2)

    # ---- the day in brief: 18 headlines, 3 columns ----
    d.text((M, 492), "THE DAY IN BRIEF", font=SERIF_B(24), fill=INK)
    hline(d, M, W - M, 522, RULE, 2)
    col_w, gap = 318, 15
    for i, (tag, col, head) in enumerate(BRIEF):
        c, r = divmod(i, 6)
        x = M + c * (col_w + gap)
        y = 534 + r * 46
        d.text((x, y), tag, font=SANS_B(11), fill=col)
        draw_wrapped(d, x, y + 15, head, SANS_B(13), INK, col_w, leading=15)
    hline(d, M, W - M, 812, RULE, 2)

    # ---- hour by hour timeline ----
    d.text((M, 824), "HOUR BY HOUR \u2014 TUESDAY 17 NOVEMBER",
           font=SERIF_B(20), fill=INK)
    ty = 856
    hline(d, M + 6, W - M - 6, ty + 6, (180, 172, 156), 2)
    seg = (W - 2 * M) // 6
    for i, (t, txt) in enumerate(TIMELINE):
        x = M + i * seg + 4
        d.ellipse([x + 2, ty, x + 14, ty + 12], fill=CRIMSON)
        d.text((x, ty + 18), t, font=SANS_B(13), fill=CRIMSON)
        draw_wrapped(d, x, ty + 36, txt, SANS(12), INK, seg - 14, leading=15)

    # ---- footer ----
    hline(d, M, W - M, 962, RULE, 2)
    d.text((M, 972),
           "Every story above was first reported on Tuesday 17 November 2026.",
           font=SANS_B(13), fill=INK)
    d.text((M, 992),
           "Sources: BBC, AFP, Al Jazeera, Le Monde, Reuters, AP. Drawn by code; no photographs.",
           font=SANS(11), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
