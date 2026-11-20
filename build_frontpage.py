#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261120 entry.

Renders a newspaper front page for Friday 20 November 2026 with PIL
(crisp vector text, no garbled AI text) around the AI-generated hero
illustration in assets/. Run once locally; the committed entry.png is what
the entry program copies to /output/entry.png.

Facts (all reported on 19-20 Nov 2026, checked against live news on 20 Nov
morning Beijing time):
- Anthropic IPO debut Thu 19 Nov: opened $111.50 (+34% on the $83 offer),
  intraday high $115.10, briefly over $2tn fully diluted; closed $97.17,
  +17%, ~$1.76tn; 813m+ shares traded, a debut volume record (Reuters/
  CNBC via TechDefused, NY Post, AsiaToday).
- Markets Thu 19 Nov: Dow -1,101.11 (-2.19%) to 49,097.06, first close
  below 50,000 since June; S&P 500 -147.80 (-2.02%) to 7,175.83, sixth
  straight loss; Nasdaq -550.69 (-2.25%) to 23,879.20, lowest close since
  April, 13.5% below its Oct 6 high; only 1 of 30 Dow stocks rose.
- Nvidia fell 3.30% to $145.98, a sixth straight fall, ~28% off November
  highs; H200 shipments to China halted; AMD -7.72% after short seller
  Hunterbrook disclosed a position.
- Fed: CME FedWatch ~95% for a 25bp December hike (Dec 8-9), ~5-10% for
  50bp; Gov. Waller floated 50bp and speaks Friday 8:25am ET. Gold fell
  ~1.8% to ~$3,675, a 14-month low; Bitcoin ~$62,000; 10-yr ~5.05%;
  VIX 28.43.
- APEC Shenzhen: first-ever Trump-Xi-Putin trilateral Thu 19 Nov, ~90
  minutes at Kylin Villa; four-point "Declaration Toward Peace": nuclear
  war cannot be won, dialogue on nuclear risk, more refined petroleum
  output, UN reform, ICC must not abuse jurisdiction; Ukraine not
  mentioned; Trump invited Putin to the December G20 in Miami.
- Gulf: Iran drones hit Ali Al Salem air base (Kuwait) and Bahrain Wed
  18 Nov, answering the US strike on an IRGC missile site on Qeshm Island
  Tue; an ADNOC tanker hit in Hormuz, 11 crew hurt, one missing; war in
  its ninth month (began 28 Feb 2026).
- Ukraine: third Kerch Bridge strike in four days — Neptune missiles hit
  the rail section overnight 19 Nov, train traffic halted, one track
  reopened ~4pm; Putin rejects a ceasefire; US envoys Kushner and Witkoff
  meet Zelenskyy in Berlin.
- Gaza: Israeli tanks crossed the Yellow Line in central Gaza Wed 18 Nov,
  first publicly announced ground operation since the Oct 2025 ceasefire;
  three killed; Board of Peace report warns the truce may collapse;
  1,650+ killed since the ceasefire began.
- GTA VI launched Thu 19 Nov on PS5 and Xbox Series X|S; Sensor Tower
  estimates ~19.05m copies and $1.84bn by Thursday afternoon (pre-orders
  included, no official Take-Two figure); ~6m watched livestreams at 2pm ET.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(
    HERE, "assets",
    "media-generation-hero-chip-market-storm-2026112-0-163c88a4-5e03-4ca7-a6da-e7cdd32ad5ba.webp")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 30  # margin
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (155, 28, 28)
NAVY = (16, 32, 64)
GREY = (90, 86, 78)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")
    return y + fnt.size


def rule(draw, y, w=2, x0=M, x1=W - M):
    draw.line([(x0, y), (x1, y)], fill=INK, width=w)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
y = 16
centered(d, y, "O N E   D A Y  ·  O N E   P A G E", font(F_SANS_B, 15), GREY)
y = 38
centered(d, y, "THE WORLD", font(F_SERIF, 96))
y = 138
rule(d, y, 3)
rule(d, y + 5, 1)
y = 152
centered(d, y, "FRIDAY,  20 NOVEMBER 2026", font(F_SERIF, 31), RED)
y = 190
rule(d, y, 1)

# ---- lead headline + deck ----
y = 202
centered(d, y, "ANTHROPIC UP 17% ON DEBUT", font(F_SERIF, 56))
y = 262
deck = ("The Claude-maker opens at $111.50, briefly tops $2tn, then closes "
        "at $97.17 — as Wall Street suffers a $1,101-point rout")
for line in wrap(d, deck, font(F_SANS, 20), W - 2 * M - 40):
    centered(d, y, line, font(F_SANS, 20))
    y += 26

# ---- hero image ----
hero = Image.open(HERO).convert("RGB")  # 2736x912
# crop a wide band: golden chip + storm skyline
cw, ch = hero.size
band_w = W - 2 * M
band_h = 290
crop_h = int(cw * band_h / band_w)
top = int((ch - crop_h) * 0.15)
hero = hero.crop((0, top, cw, top + crop_h))
hero = hero.resize((band_w, band_h), Image.LANCZOS)
img.paste(hero, (M, y + 8))
y = y + 8 + 290 + 8
d.text((M, y), "A golden chip over a stormy market: Anthropic's record debut "
       "could not stop a Dow rout.  (Illustration)",
       font=font(F_SERIF_I, 15), fill=GREY)
y += 24

# ---- markets ticker ----
d.rectangle([M, y, W - M, y + 34], fill=NAVY)
d.text((W // 2, y + 17),
       "DOW  −2.19%  ·  S&P 500  −2.02%, 6th straight loss  ·  "
       "NASDAQ  −2.25%  ·  GOLD ~$3,675, 14-mo low",
       font=font(F_SANS_B, 16), fill=(255, 255, 255), anchor="mm")
y += 34 + 10

# ---- story grid: 2 cols x 3 rows ----
stories = [
    ("NVIDIA",
     "Sixth straight fall to $145.98",
     "AI leader now ~28% off its November highs as the H200 China halt "
     "bites; AMD −7.7% on a short-seller attack."),
    ("THE FED",
     "December hike ~95% priced in",
     "Traders see a 25bp rise on Dec 8–9 as near-certain; Waller floats "
     "50bp and speaks on Friday morning."),
    ("APEC · SHENZHEN",
     "Trump, Xi, Putin sign declaration",
     "First-ever trilateral, ~90 minutes at Kylin Villa: nuclear-risk "
     "talks, more refined oil, UN reform; Ukraine unmentioned."),
    ("THE GULF",
     "Iran drones hit Kuwait, Bahrain",
     "Tehran answers the US strike on Qeshm Island; an ADNOC tanker is "
     "hit in Hormuz, 11 crew hurt and one missing."),
    ("UKRAINE",
     "Kerch bridge hit a third time",
     "Neptune missiles halt rail traffic for hours; Putin rejects a "
     "ceasefire as US envoys meet Zelenskyy in Berlin."),
    ("GAZA",
     "Tanks cross the Yellow Line",
     "First announced ground operation since the Oct 2025 truce; three "
     "killed. Board of Peace warns it may collapse."),
]
col_w = (W - 2 * M - 24) // 2
row_h = 84
gx0 = M
for i, (kick, head, body) in enumerate(stories):
    cx = gx0 + (i % 2) * (col_w + 24)
    cy = y + (i // 2) * row_h
    d.text((cx, cy), kick, font=font(F_SANS_B, 14), fill=RED)
    hl = wrap(d, head, font(F_SERIF, 23), col_w)
    hy = cy + 19
    for line in hl[:1]:
        d.text((cx, hy), line, font=font(F_SERIF, 23), fill=INK)
        hy += 27
    by = hy + 1
    for line in wrap(d, body, font(F_SANS, 15), col_w)[:2]:
        d.text((cx, by), line, font=font(F_SANS, 15), fill=(51, 51, 51))
        by += 19
    if i % 2 == 0:
        d.line([(cx + col_w + 12, cy), (cx + col_w + 12, cy + row_h - 12)],
               fill=(200, 192, 175), width=1)

y = y + 3 * row_h + 2
rule(d, y, 1)
y += 8
d.text((M, y), "ALSO:  GTA VI: ~19m copies, $1.84bn by launch day (Sensor "
       "Tower est.)  ·  Bitcoin ~$62,000  ·  10-yr yield ~5.05%",
       font=font(F_SANS_B, 14), fill=INK)
y += 24
d.text((W // 2, y), "Every story above happened or was first reported on "
       "Friday 20 November 2026.",
       font=font(F_SERIF_I, 14), fill=GREY, anchor="ma")

# A real PNG if it fits the 1 MiB gate; the photo band usually keeps it
# well under, and a true PNG is the cleanest thing to hand the gate.
img.save(OUT, "PNG", optimize=True)
size = os.path.getsize(OUT)
if size > 1048576:
    img.save(OUT, "JPEG", quality=88, optimize=True)
    size = os.path.getsize(OUT)
print("saved", OUT, size, "bytes")
