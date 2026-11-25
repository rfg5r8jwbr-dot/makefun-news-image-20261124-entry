#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news poster (1024x1024, PIL, deterministic).

Layout: navy masthead, one lead story, two mid stories side by side,
three short stories in rows, source footer. All text is drawn with
DejaVu (bundled with most Linux systems); no network, no external files.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (19, 41, 75)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
GREY = (90, 88, 80)
RULE = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 52)
F_MAST_SUB = font("DejaVuSans.ttf", 24)
F_KICKER = font("DejaVuSans-Bold.ttf", 24)
F_LEAD = font("DejaVuSans-Bold.ttf", 62)
F_DECK = font("DejaVuSans.ttf", 27)
F_MID_HEAD = font("DejaVuSans-Bold.ttf", 33)
F_MID_DECK = font("DejaVuSans.ttf", 23)
F_ROW_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_ROW_DECK = font("DejaVuSans.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
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


def para(draw, x, y, text, fnt, max_w, fill, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((48, 22), "THE WORLD IN ONE IMAGE", font=F_MAST_SUB, fill=GOLD)
    d.text((48, 58), "TUESDAY, 24 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255))
    d.text((W - 48 - d.textlength("6 STORIES", font=F_MAST_SUB), 22),
           "6 STORIES", font=F_MAST_SUB, fill=(255, 255, 255))
    d.rectangle([0, 148, W, 154], fill=GOLD)

    # ---- Lead story: Huawei guilty ----
    y = 172
    d.text((48, y), "LEAD  \u2014  NEW YORK", font=F_KICKER, fill=RED)
    y += 36
    d.text((48, y), "HUAWEI FOUND GUILTY", font=F_LEAD, fill=INK)
    y += 74
    d.text((48, y), "ON 10 OF 12 COUNTS", font=F_LEAD, fill=INK)
    y += 74
    y = para(d, 48, y,
             "A Brooklyn jury convicts the Chinese telecom giant of bank fraud, "
             "wire fraud, sanctions violations and trade-secret conspiracy.",
             F_DECK, W - 96, INK, 36)
    d.rectangle([48, 444, W - 48, 447], fill=RULE)

    # ---- Two mid stories ----
    col_w = (W - 96 - 40) // 2
    mid_y = 462
    d.text((48, mid_y), "STRAIT OF HORMUZ", font=F_KICKER, fill=RED)
    d.text((48 + col_w + 40, mid_y), "UKRAINE  \u2014  BLACK SEA", font=F_KICKER, fill=RED)
    y2 = mid_y + 36
    y2 = para(d, 48, y2, "Four tankers hit by mines, Iran says",
              F_MID_HEAD, col_w, INK, 40)
    para(d, 48 + col_w + 40, mid_y + 36,
         "Kyiv's drones strike Russian ships",
         F_MID_HEAD, col_w, INK, 40)
    y3 = mid_y + 36 + 80
    para(d, 48, y3,
         "Four tankers struck mines and caught fire, Tehran reports; "
         "the Joint Maritime Information Centre says the claims are unconfirmed.",
         F_MID_DECK, col_w, GREY, 30)
    para(d, 48 + col_w + 40, y3,
         "A cargo ship in the Gulf of Finland and a corvette off Libya are hit; "
         "Poland accuses Russia of a new airspace violation.",
         F_MID_DECK, col_w, GREY, 30)
    d.rectangle([48, 716, W - 48, 719], fill=RULE)

    # ---- Three short rows: red kicker + headline on one line, one-line deck ----
    rows = [
        ("RIYADH", "PIF tower hit again in Riyadh",
         "Houthi drone strike wounds at least 11 \u2014 the second hit in under a week."),
        ("CARTAGENA", "25 held hostage in supermarket siege",
         "Armed men seize a Cartagena supermarket and hold 25 people hostage."),
        ("FOOTBALL", "Senegal champions again",
         "Top court gives Senegal its Africa Cup title back, overturning the Morocco ruling."),
    ]
    y = 734
    for kicker, head, deck in rows:
        d.text((48, y), kicker, font=F_ROW_HEAD, fill=RED)
        kx = 48 + d.textlength(kicker, font=F_ROW_HEAD) + 16
        d.text((kx, y), head, font=F_ROW_HEAD, fill=INK)
        d.text((48, y + 36), deck, font=F_ROW_DECK, fill=GREY)
        y += 78
    d.rectangle([48, 968, W - 48, 971], fill=RULE)
    foot = "Sources: Reuters  \u2022  AP  \u2022  CNN  \u2022  WSJ  \u2022  Al Jazeera  \u2022  SCMP  \u2022  Le Temps"
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, 980), foot,
           font=F_FOOT, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
