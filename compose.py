#!/usr/bin/env python3
"""Build the front page for Tuesday 24 November 2026.

Three generated photos plus headlines, decks and a footer strip are laid
out as a 1024 by 1024 newspaper page. Run from this folder:

    python3 compose.py
"""

import os

from PIL import Image, ImageDraw
from PIL import ImageFont

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

SIZE = 1024
BG = (247, 243, 234)
FG = (12, 12, 12)
ACCENT = (178, 34, 34)
MUTED = (90, 86, 78)
EDGE = 28
GAP = 20

SERIF = "DejaVuSerif.ttf"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


def face(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def cover(path, width, height):
    """Crop a photo to fill a width by height box, centred."""
    photo = Image.open(path).convert("RGB")
    zoom = max(width / photo.width, height / photo.height)
    big = photo.resize((round(photo.width * zoom), round(photo.height * zoom)), Image.LANCZOS)
    left = (big.width - width) // 2
    top = (big.height - height) // 2
    return big.crop((left, top, left + width, top + height))


def wrap_text(draw, text, fnt, width):
    """Split text into lines that fit width, by word."""
    words = text.split()
    out = []
    line = ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def text_block(draw, lines, x, y, fnt, color, gap=4, width=None, centre=False):
    for line in lines:
        if centre:
            x0 = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            x0 = x
        draw.text((x0, y), line, font=fnt, fill=color)
        y += fnt.size + gap
    return y


def rule(draw, y, weight=1):
    draw.line([(EDGE, y), (SIZE - EDGE, y)], fill=FG, width=weight)


def photo_block(page, draw, path, x, y, width, height):
    page.paste(cover(path, width, height), (x, y))
    draw.rectangle([x, y, x + width - 1, y + height - 1], outline=FG, width=2)


def story_block(page, draw, x, y, width, photo, photo_h, headline, deck):
    if photo:
        photo_block(page, draw, photo, x, y, width, photo_h)
        y += photo_h + 10
    head = face(SERIF_BOLD, 23)
    y = text_block(draw, wrap_text(draw, headline, head, width), x, y, head, FG, gap=2)
    body = face(SERIF, 17)
    y = text_block(draw, wrap_text(draw, deck, body, width), x, y + 2, body, MUTED, gap=2)
    return y


def main():
    page = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(page)
    inner = SIZE - 2 * EDGE

    mast = face(SERIF_BOLD, 66)
    title = "THE WORLD TODAY"
    draw.text(((SIZE - draw.textlength(title, font=mast)) / 2, 14), title, font=mast, fill=FG)
    rule(draw, 92, 3)
    rule(draw, 97)

    day = face(SANS_BOLD, 40)
    date = "TUESDAY 24 NOVEMBER 2026"
    draw.text(((SIZE - draw.textlength(date, font=day)) / 2, 106), date, font=day, fill=ACCENT)
    rule(draw, 156, 2)

    lead = os.path.join(ASSETS, "media-generation-nvidia-huang-keynote-0-23fc2062-4a0f-4203-ab4f-c135c276f03a.webp")
    photo_block(page, draw, lead, EDGE, 166, inner, 248)

    y = 424
    big = face(SERIF_BOLD, 42)
    y = text_block(draw, ["HUANG IS BACK AT NVIDIA"], EDGE, y, big, FG, gap=2)
    deck = face(SERIF, 20)
    y = text_block(draw, wrap_text(draw, "Board reinstates Jensen Huang as chief executive after Trump intervenes, saying the chip boss poses no national security threat.", deck, inner), EDGE, y + 2, deck, MUTED, gap=3)
    rule(draw, 520)

    half = (inner - GAP) // 2
    y = 530
    left = os.path.join(ASSETS, "media-generation-space-weapon-satellite-0-daf6da1f-7b98-4002-b15d-5035eb17e9a8.webp")
    right = os.path.join(ASSETS, "media-generation-mexico-capture-dawn-0-0d8e8a87-7abc-46f8-a079-986a4d573aff.webp")
    story_block(page, draw, EDGE, y, half, left, 176, "NUCLEAR SPACE WEAPON FEAR", "Allies warn Russia may launch an orbital weapon next month; NATO vows to defend space.")
    story_block(page, draw, EDGE + half + GAP, y, half, right, 176, "DRUG LORD NABBED WITH US DRONE HELP", "Mexico captures Chapo Isidro, one of its most wanted cartel bosses, with US intelligence help.")
    rule(draw, 850)

    y = 862
    small_head = face(SERIF_BOLD, 21)
    small_body = face(SERIF, 16)
    text_block(draw, wrap_text(draw, "STATES SUE MUSK FIRMS OVER GROK IMAGES", small_head, half), EDGE, y, small_head, FG, gap=2)
    text_block(draw, wrap_text(draw, "US states say the chatbot made sexualised images of real people.", small_body, half), EDGE, y + 56, small_body, MUTED, gap=2)
    text_block(draw, wrap_text(draw, "KYIV STRIKES KILL AT LEAST 14", small_head, half), EDGE + half + GAP, y, small_head, FG, gap=2)
    text_block(draw, wrap_text(draw, "Russian strikes hit the Kyiv region; Ukraine says Moscow is planning more.", small_body, half), EDGE + half + GAP, y + 56, small_body, MUTED, gap=2)

    draw.rectangle([0, 968, SIZE - 1, SIZE - 1], fill=FG)
    foot = face(SANS_BOLD, 14)
    strip = "ALSO TODAY:  Moscow warns Estonia over acts near open war  |  UN chief calls for AI rules within a year"
    draw.text(((SIZE - draw.textlength(strip, font=foot)) / 2, 986), strip, font=foot, fill=BG)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    page.save(out, format="PNG", optimize=True)
    print("saved", out, os.path.getsize(out))


if __name__ == "__main__":
    main()
