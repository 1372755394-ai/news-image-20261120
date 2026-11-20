#!/usr/bin/env python3
"""Render the 20 November 2026 front page of THE WORLD as a 1024x1024 PNG.

Everything on the page (headlines, figures, dates) comes from the story list
in README.md, which was checked against live news on the morning of
20 November 2026 (Beijing time). The only picture is the pre-generated hero
illustration in assets/; all text is drawn here with PIL.

Layout is a single vertical flow: a cursor walks down the page and each
section (masthead, lead story, hero photo, ticker, story grid, footer)
advances it. No network access, no secrets.
"""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(
    HERE,
    "assets",
    "media-generation-hero-chip-market-storm-2026112-0-163c88a4-5e03-4ca7-a6da-e7cdd32ad5ba.webp",
)
OUT_PATH = os.path.join(HERE, "entry.png")

# --- page geometry -------------------------------------------------------
PAGE_W, PAGE_H = 1024, 1024
MARGIN = 40                       # side margin; content spans 944 px
CONTENT_W = PAGE_W - 2 * MARGIN
MAX_BYTES = 1_000_000

# --- palette -------------------------------------------------------------
PAPER = (247, 241, 229)           # warm newsprint
INK = (17, 17, 17)
SOFT_INK = (68, 60, 52)
RED = (143, 29, 29)               # kicker / dateline red
NAVY = (27, 42, 74)              # ticker bar
RULE = (30, 30, 30)

# --- fonts ---------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype"
SERIF = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Regular.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")
SERIF_ITALIC = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# --- small drawing helpers ------------------------------------------------
def text_width(draw: ImageDraw.ImageDraw, text: str,
               fnt: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(text, font=fnt)


def wrap(draw: ImageDraw.ImageDraw, text: str,
         fnt: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
    """Greedy word wrap; returns lines that each fit inside max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if text_width(draw, trial, fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw: ImageDraw.ImageDraw, cx: int, y: int, text: str,
                  fnt: ImageFont.FreeTypeFont, fill=INK) -> None:
    draw.text((cx - text_width(draw, text, fnt) / 2, y), text,
              font=fnt, fill=fill)


def draw_tracked(draw: ImageDraw.ImageDraw, cx: int, y: int, text: str,
                 fnt: ImageFont.FreeTypeFont, tracking: int, fill=INK) -> None:
    """Draw text with extra space between letters, centred on cx."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def draw_rule(draw: ImageDraw.ImageDraw, y: int, weight: int,
              x0: int = MARGIN, x1: int = PAGE_W - MARGIN) -> None:
    draw.line([(x0, y), (x1, y)], fill=RULE, width=weight)


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: str,
             start_size: int, max_width: float) -> ImageFont.FreeTypeFont:
    """Largest size (stepping down by 2) at which text fits max_width."""
    size = start_size
    while size > 10:
        fnt = font(path, size)
        if text_width(draw, text, fnt) <= max_width:
            return fnt
        size -= 2
    return font(path, 10)


# --- page builder ---------------------------------------------------------
class FrontPage:
    """A blank newsprint sheet plus a cursor that walks down it."""

    def __init__(self) -> None:
        self.image = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.draw = ImageDraw.Draw(self.image)
        self.y = 0

    # -- masthead block ----------------------------------------------------
    def masthead(self) -> None:
        self.y = 22
        eyebrow = font(SANS_BOLD, 15)
        draw_tracked(self.draw, PAGE_W // 2, self.y, "ONE DAY · ONE PAGE",
                     eyebrow, tracking=6, fill=SOFT_INK)
        self.y += 30
        name = fit_font(self.draw, "THE WORLD", SERIF_BOLD, 118, CONTENT_W)
        draw_centered(self.draw, PAGE_W // 2, self.y - 14, "THE WORLD",
                      name)
        self.y += 98
        draw_rule(self.draw, self.y, 3)
        self.y += 5
        draw_rule(self.draw, self.y, 1)
        self.y += 12
        date_font = font(SERIF_BOLD, 30)
        draw_centered(self.draw, PAGE_W // 2, self.y,
                      "FRIDAY,  20 NOVEMBER 2026", date_font, fill=RED)
        self.y += 42
        draw_rule(self.draw, self.y, 1)
        self.y += 14

    # -- lead story --------------------------------------------------------
    def lead(self) -> None:
        headline = fit_font(self.draw, "ANTHROPIC UP 17% ON DEBUT",
                            SERIF_BOLD, 58, CONTENT_W)
        draw_centered(self.draw, PAGE_W // 2, self.y,
                      "ANTHROPIC UP 17% ON DEBUT", headline)
        self.y += 58
        deck_font = font(SERIF, 22)
        deck = ("The Claude-maker opens at $111.50, briefly tops $2tn, then "
                "closes at $97.17 — as Wall Street suffers a $1,101-point rout")
        for line in wrap(self.draw, deck, deck_font, CONTENT_W - 40):
            draw_centered(self.draw, PAGE_W // 2, self.y, line, deck_font)
            self.y += 26
        self.y += 8

    # -- hero illustration -------------------------------------------------
    def hero(self) -> None:
        photo = Image.open(HERO_PATH).convert("RGB")
        # Crop the 3:1 source to the banner's wider aspect, centred.
        target_ratio = CONTENT_W / 224
        src_w, src_h = photo.size
        if src_w / src_h > target_ratio:
            new_w = int(src_h * target_ratio)
            left = (src_w - new_w) // 2
            photo = photo.crop((left, 0, left + new_w, src_h))
        else:
            new_h = int(src_w / target_ratio)
            top = (src_h - new_h) // 2
            photo = photo.crop((0, top, src_w, top + new_h))
        photo = photo.resize((CONTENT_W, 224), Image.LANCZOS)
        self.image.paste(photo, (MARGIN, self.y))
        self.draw.rectangle([MARGIN, self.y, PAGE_W - MARGIN, self.y + 224],
                            outline=RULE, width=1)
        self.y += 224 + 8
        caption = font(SERIF_ITALIC, 16)
        self.draw.text(
            (MARGIN, self.y),
            "A golden chip over a stormy market: Anthropic's record debut "
            "could not stop a Dow rout. (Illustration)",
            font=caption, fill=SOFT_INK)
        self.y += 20

    # -- markets ticker ----------------------------------------------------
    def ticker(self) -> None:
        bar_h = 36
        self.draw.rectangle([MARGIN, self.y, PAGE_W - MARGIN, self.y + bar_h],
                            fill=NAVY)
        ticker_font = font(SANS_BOLD, 19)
        line = ("DOW −2.19%  ·  S&P 500 −2.02%, 6th straight loss  ·  "
                "NASDAQ −2.25%  ·  GOLD ~$3,675, 14-mo low")
        draw_centered(self.draw, PAGE_W // 2, self.y + 8, line, ticker_font,
                      fill=(255, 255, 255))
        self.y += bar_h + 10

    # -- one story inside the two-column grid ------------------------------
    def story(self, x: int, col_w: int, kicker: str, headline: str,
              body: str) -> int:
        """Draw a story at column x; return the y just below it."""
        y = self.y
        kick_font = font(SANS_BOLD, 15)
        self.draw.text((x, y), kicker, font=kick_font, fill=RED)
        y += 22
        head_font = font(SERIF_BOLD, 25)
        for line in wrap(self.draw, headline, head_font, col_w):
            self.draw.text((x, y), line, font=head_font, fill=INK)
            y += 28
        y += 2
        body_font = font(SERIF, 17)
        for line in wrap(self.draw, body, body_font, col_w):
            self.draw.text((x, y), line, font=body_font, fill=INK)
            y += 21
        return y + 10

    def story_grid(self) -> None:
        gutter = 30
        col_w = (CONTENT_W - gutter) // 2
        left_x, right_x = MARGIN, MARGIN + col_w + gutter
        grid_top = self.y
        left = [
            ("NVIDIA",
             "Sixth straight fall to $145.98",
             "AI leader now ~28% off its November highs as the H200 China "
             "halt bites; AMD −7.7% on a short-seller attack."),
            ("APEC · SHENZHEN",
             "Trump, Xi, Putin sign declaration",
             "First-ever trilateral, ~90 minutes at Kylin Villa: "
             "nuclear-risk talks, more refined oil, UN reform; Ukraine "
             "unmentioned."),
            ("UKRAINE",
             "Kerch bridge hit a third time",
             "Neptune missiles halt rail traffic for hours; Putin rejects "
             "a ceasefire as US envoys meet Zelenskyy in Berlin."),
        ]
        right = [
            ("THE FED",
             "December hike ~95% priced in",
             "Traders see a 25bp rise on Dec 8–9 as near-certain; Waller "
             "floats 50bp and speaks on Friday morning."),
            ("THE GULF",
             "Iran drones hit Kuwait, Bahrain",
             "Tehran answers the US strike on Qeshm Island; an ADNOC "
             "tanker is hit in Hormuz, 11 crew hurt and one missing."),
            ("GAZA",
             "Tanks cross the Yellow Line",
             "First announced ground operation since the Oct 2025 truce; "
             "three killed. Board of Peace warns it may collapse."),
        ]
        # Left column flows top to bottom; remember where it ends.
        col_y = grid_top
        for kicker, headline, body in left:
            self.y = col_y
            col_y = self.story(left_x, col_w, kicker, headline, body)
        left_bottom = col_y
        col_y = grid_top
        for kicker, headline, body in right:
            self.y = col_y
            col_y = self.story(right_x, col_w, kicker, headline, body)
        right_bottom = col_y
        # Vertical divider between the columns, spanning the taller side.
        mid_x = MARGIN + col_w + gutter // 2
        self.draw.line([(mid_x, grid_top),
                        (mid_x, max(left_bottom, right_bottom) - 12)],
                       fill=RULE, width=1)
        self.y = max(left_bottom, right_bottom) + 2

    # -- bottom strip and footer -------------------------------------------
    def footer(self) -> None:
        draw_rule(self.draw, self.y, 1)
        self.y += 10
        also_font = font(SANS_BOLD, 17)
        also = ("ALSO:   GTA VI: ~19m copies, $1.84bn by launch day "
                "(Sensor Tower est.)  ·  Bitcoin ~$62,000  ·  "
                "10-yr yield ~5.05%")
        draw_centered(self.draw, PAGE_W // 2, self.y, also, also_font)
        self.y += 26
        note = font(SERIF_ITALIC, 15)
        draw_centered(self.draw, PAGE_W // 2, self.y,
                      "Every story above happened or was first reported on "
                      "Friday 20 November 2026.",
                      note, fill=SOFT_INK)
        self.y += 24

    def build(self) -> None:
        self.masthead()
        self.lead()
        self.hero()
        self.ticker()
        self.story_grid()
        self.footer()
        assert self.y <= PAGE_H, f"page overflowed: cursor at {self.y}"
        self.image.save(OUT_PATH, format="PNG", optimize=True)


def main() -> None:
    page = FrontPage()
    page.build()
    size = os.path.getsize(OUT_PATH)
    print(f"wrote {OUT_PATH}: {PAGE_W}x{PAGE_H}, {size} bytes, "
          f"cursor ended at y={page.y}")
    if size >= MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")


if __name__ == "__main__":
    main()
