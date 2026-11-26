"""Draw the 25 November 2026 world-news front page (1024x1024 PNG)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (20, 33, 61)
RED = (178, 58, 72)
TEAL = (31, 122, 109)
AMBER = (199, 145, 45)
SLATE = (88, 98, 116)
LINE = (205, 198, 182)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill, leading=6):
    step = int(fnt.size * 1.3) + leading
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def story(draw, x, y, w, color, kicker, headline, sub, source):
    kx = x + 24
    draw.text((kx, y), kicker, font=font("DejaVuSans-Bold.ttf", 18), fill=color)
    yy = text_block(draw, kx, y + 27, headline,
                    font("DejaVuSerif-Bold.ttf", 28), w - 24, INK, leading=2)
    yy = text_block(draw, kx, yy + 1, sub,
                    font("DejaVuSans.ttf", 19), w - 24, SLATE, leading=2)
    draw.text((kx, yy + 1), source, font=font("DejaVuSans-Bold.ttf", 14), fill=SLATE)
    bottom = yy + 22
    draw.rectangle([x, y, x + 10, bottom], fill=color)
    return bottom


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # Masthead
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((48, 22), "WORLD NEWS", font=font("DejaVuSerif-Bold.ttf", 64),
           fill=(255, 255, 255))
    d.text((50, 98), "Wednesday, 25 November 2026",
           font=font("DejaVuSans-Bold.ttf", 27), fill=(255, 214, 130))
    tag = "THE DAY IN ONE PAGE"
    tw = d.textlength(tag, font=font("DejaVuSans-Bold.ttf", 19))
    d.text((W - 48 - tw, 108), tag, font=font("DejaVuSans-Bold.ttf", 19),
           fill=(200, 210, 230))

    # Lead story
    d.rectangle([48, 176, W - 48, 348], outline=LINE, width=2)
    d.text((72, 192), "TRADE — WASHINGTON",
           font=font("DejaVuSans-Bold.ttf", 21), fill=RED)
    d.rounded_rectangle([764, 186, 952, 230], radius=14, fill=AMBER)
    d.text((788, 196), "14 PARTNERS", font=font("DejaVuSans-Bold.ttf", 21), fill=INK)
    y = text_block(d, 72, 222, "US proposes new tariffs on 14 partners",
                   font("DejaVuSerif-Bold.ttf", 37), 880, INK, leading=2)
    y = text_block(d, 72, y + 4,
                   "China faces the highest rate; a hearing comes before any duties take effect.",
                   font("DejaVuSans.ttf", 22), 880, SLATE, leading=2)
    d.text((72, y + 4), "Reuters / AP", font=font("DejaVuSans-Bold.ttf", 15), fill=SLATE)

    # Story grid
    col_w = 440
    left, right = 48, 536
    rows = [
        (TEAL, "TECH TRIAL — NEW YORK", "US jury convicts Huawei",
         "Guilty of trade-secret conspiracy and bank fraud.", "AP",
         NAVY, "SPACE — TIANGONG", "Pakistan's first astronaut rides Shenzhou-24",
         "Muhammad Zeeshan Ali joins two Chinese crew members.", "Reuters"),
        (RED, "EGYPT — CAIRO", "Fuel tanker blaze kills at least 21",
         "Petroleum vehicle overturns on the ring road.", "Reuters",
         AMBER, "NIGERIA — NIGER STATE", "Militants kill at least 30, residents say",
         "Homes burned in village attacks.", "Reuters"),
        (NAVY, "MARKETS — WALL STREET", "Stocks recover most of an AI-led slide",
         "Losses ease despite inflation and tariff fears.", "AP",
         TEAL, "UNITED STATES — IOWA", "Army destroys lead azide stockpile",
         "First checks show no toxic spread to nearby homes.", "AP"),
    ]
    y = 366
    for (c1, k1, h1, s1, src1, c2, k2, h2, s2, src2) in rows:
        b1 = story(d, left, y, col_w, c1, k1, h1, s1, src1)
        b2 = story(d, right, y, col_w, c2, k2, h2, s2, src2)
        y = max(b1, b2) + 12
        if y < 920:
            d.line([48, y - 8, W - 48, y - 8], fill=LINE, width=2)
            y += 6

    # Footer
    d.rectangle([0, 944, W, H], fill=NAVY)
    d.text((48, 966), "Also today: a Houthi drone hits a Riyadh tower again, wounding 11.",
           font=font("DejaVuSans-Bold.ttf", 21), fill=(255, 255, 255))
    d.text((48, 994), "Reuters", font=font("DejaVuSans.ttf", 16), fill=(200, 210, 230))

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
