"""Render the 23 November 2026 world-news front page to entry.png.

One 1024x1024 image, 39 stories reported on Monday 23 November 2026,
grouped by region and field. Every letter is drawn programmatically
with Pillow from the story lists below, so no lettering can be garbled.
The render is deterministic: fixed palette, fixed fonts, no clock,
no randomness, no network. Running it twice writes identical bytes.
Layout: navy masthead with the date in large serif, a three-story
lead band (the Merkury sinking dominates), two columns of sections,
and a "day in numbers" strip at the foot.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 248, 241)
INK = (13, 16, 22)
BODY = (34, 37, 44)
MUTED = (92, 96, 104)
RULE = (196, 188, 168)
NAVY = (16, 32, 56)
RED = (168, 32, 36)
TEAL = (14, 102, 96)
GOLD = (176, 124, 22)
LEAD_BG = (232, 226, 208)
GOLD_TEXT = (214, 186, 120)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


LEADS = [
    ("UKRAINE SINKS WARSHIP",
     "Kyiv says seven naval drones sank the corvette Merkury off Libya "
     "and hit the cargo ship Angara; the UN mission calls for an "
     "independent probe."),
    ("COP31 ENDS WITH NO DEAL",
     "The UN climate summit in Antalya collapses after record-long talks "
     "as the EU and island states reject a final draft that never "
     "mentions fossil fuels."),
    ("RUSSIAN STRIKES KILL 15",
     "Overnight bombardment of the Kyiv region kills at least 15; a boy, "
     "7, is pulled alive from rubble in Dymer after 14 hours."),
]

# (column, heading, colour, items) — left column first, then right.
SECTIONS = [
    ("L", "EUROPE & UKRAINE", RED, [
        "EU proposes Russia sanctions on banks, crypto",
        "Finland summons envoy; Russia warns Estonia",
        "Hungary PM Magyar to visit Transcarpathia",
        "Belgium airports shut as controllers strike",
        "Poland: Russia tried to kill rapper twice",
    ]),
    ("L", "ASIA-PACIFIC", TEAL, [
        "Indonesia factory fire: 24 dead, 30 missing",
        "India offers \u20ac1.4bn to rebuild Nepal",
        "Seoul defends Gulf of Aden deployment",
        "Kim rebuffs Trump offer of talks",
        "Kenya and DR Congo restore full ties",
        "Lion on the loose on Istanbul outskirts",
    ]),
    ("L", "AMERICAS", NAVY, [
        "Mexico captures 'El Chapo Isidro'; 17 killed",
        "Democrats take largest House majority since 1992",
        "FBI probes hack of its crime database",
        "Amtrak derails in Louisiana after truck crash",
        "Nine shot at concert in California",
        "Trump curbs Congress access to agency files",
    ]),
    ("R", "MIDDLE EAST & IRAN", GOLD, [
        "US sanctions Iran shadow banking network",
        "Iran vows to counter Hormuz blockade",
        "Iran flogs singer Parastoo Ahmadi, 74 lashes",
        "Netanyahu urges Trump to strike Iran soon",
        "Gaza 99% contaminated, Oxfam report says",
    ]),
    ("R", "AFRICA", RED, [
        "Drones hit Khartoum homes and UN building",
        "Nigeria boat search after funeral capsizing",
        "Fighting disrupts Ebola response in DR Congo",
        "Cameroon ex-rebels caught in broken promises",
    ]),
    ("R", "ECONOMY & TECHNOLOGY", TEAL, [
        "Asian tech shares fall as AI sell-off deepens",
        "Euro inflation rises to 4.0%",
        "SK hynix jumps 20% as Huang returns to Nvidia",
        "AI 'proves' Riemann hypothesis, Anthropic says",
    ]),
    ("R", "SCIENCE & HEALTH", GOLD, [
        "BepiColombo orbits Mercury after 8 years",
        "NHS trials AI in breast cancer screening",
    ]),
    ("R", "SPORT & CULTURE", RED, [
        "Verstappen wins Las Vegas Grand Prix",
        "Alcaraz wins first ATP Finals title",
        "49ers rout Vikings 35-10 in Mexico City",
        "Skubal signs record $450m Mets deal",
    ]),
]

NUMBERS = [
    ("15", "killed in Kyiv strikes"),
    ("24", "dead in Indonesia fire"),
    ("4.0%", "euro-area inflation"),
    ("8 yrs", "BepiColombo to Mercury"),
    ("$450m", "Skubal's Mets deal"),
]


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns lines that all fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def check_fit(draw):
    """Fail loudly if any one-line story is wider than its column."""
    item_font = F(SANS, 19)
    for _, _, _, items in SECTIONS:
        for item in items:
            w = draw.textlength(item, font=item_font)
            if w > 458:
                raise SystemExit(f"OVERFLOW: {item!r} is {w:.0f}px wide")
    for i, (head, _) in enumerate(LEADS):
        w = draw.textlength(head, font=F(SANS_B, 22 if i == 0 else 20))
        if w > 306:
            raise SystemExit(f"LEAD OVERFLOW: {head!r} is {w:.0f}px wide")


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.text((36, 14), "THE WORLD IN ONE DAY", font=F(SANS_B, 21), fill=GOLD_TEXT)
    draw.text((36, 40), "Monday 23 November 2026", font=F(SERIF_B, 46), fill=(255, 255, 255))
    draw.text((36, 94), "39 stories  \u00b7  every region  \u00b7  one page",
              font=F(SANS, 16), fill=(196, 208, 224))
    draw.text((812, 48), "23 NOV", font=F(SERIF_B, 34), fill=(255, 255, 255))
    draw.text((812, 86), "2026", font=F(SANS_B, 18), fill=GOLD_TEXT)


def draw_leads(draw):
    y = 130
    draw.rectangle([24, y, W - 24, y + 160], fill=LEAD_BG)
    for i, (head, body) in enumerate(LEADS):
        x = 40 + i * 324
        col_w = 312
        draw.text((x, y + 12), head, font=F(SANS_B, 22 if i == 0 else 20),
                  fill=RED if i == 0 else INK)
        lines = wrap(draw, body, F(SANS, 16 if i == 0 else 15), col_w - 6)
        by = y + 46
        for line in lines[:5]:
            draw.text((x, by), line, font=F(SANS, 16 if i == 0 else 15), fill=BODY)
            by += 21 if i == 0 else 20
    return y + 172


def draw_column(draw, side, y0):
    x = 24 if side == "L" else 524
    width = 484 if side == "L" else 476
    y = y0
    for col, title, colour, items in SECTIONS:
        if col != side:
            continue
        draw.rectangle([x, y, x + width, y + 28], fill=colour)
        draw.text((x + 10, y + 5), title, font=F(SANS_B, 18), fill=(255, 255, 255))
        y += 34
        for item in items:
            draw.text((x + 4, y), "\u2022", font=F(SANS_B, 19), fill=colour)
            draw.text((x + 22, y), item, font=F(SANS, 19), fill=INK)
            y += 23
        y += 4
    return y


def draw_numbers(draw, y):
    draw.rectangle([24, y, W - 24, y + 58], outline=RULE, width=2)
    draw.text((40, y + 4), "THE DAY IN NUMBERS", font=F(SANS_B, 13), fill=NAVY)
    nx = 40
    for value, label in NUMBERS:
        draw.text((nx, y + 20), value, font=F(SERIF_B, 20), fill=RED)
        draw.text((nx, y + 43), label, font=F(SANS, 9), fill=MUTED)
        nx += 192


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    check_fit(draw)
    draw_masthead(draw)
    y = draw_leads(draw)
    left_end = draw_column(draw, "L", y)
    right_end = draw_column(draw, "R", y)
    ny = max(left_end, right_end) + 2
    draw_numbers(draw, ny)
    draw.text((24, H - 18),
              "Sources: AP, Reuters, AFP, Al Jazeera, The Guardian, ESA and national reports of 23 Nov 2026.",
              font=F(SANS, 11), fill=MUTED)
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
