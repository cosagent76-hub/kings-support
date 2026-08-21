#!/usr/bin/env python3
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "rules" / "kings-one-page-rules.pdf"
CARDS = ROOT / "assets" / "cards"

APP_STORE_URL = "https://apps.apple.com/us/app/kings-card-game-scoring/id6791298125"
HELP_URL = "https://cosagent76-hub.github.io/kings-support/play/"

GREEN = colors.HexColor("#1e7a6b")
DARK = colors.HexColor("#0b241d")
GOLD = colors.HexColor("#f5b942")
MUTED = colors.HexColor("#5f5a52")
LINE = colors.HexColor("#d8cdbc")
PAPER = colors.HexColor("#fbf7ef")
PANEL = colors.white
RED = colors.HexColor("#c0262d")


styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.15,
    leading=11.4,
    textColor=colors.HexColor("#222222"),
    spaceAfter=3,
)
SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=7.7,
    leading=9.4,
    textColor=MUTED,
)


def draw_round_rect(c, x, y, w, h, radius=8, fill=PANEL, stroke=LINE, width=0.8):
    c.saveState()
    c.setLineWidth(width)
    c.setStrokeColor(stroke)
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    c.restoreState()


def text(c, x, y, s, size=8, color=colors.black, font="Helvetica"):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, s)
    c.restoreState()


def centered(c, x, y, w, s, size=8, color=colors.black, font="Helvetica-Bold"):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(x + w / 2, y, s)
    c.restoreState()


def para(c, x, y, w, html, style=BODY):
    p = Paragraph(html, style)
    _, h = p.wrap(w, 200)
    p.drawOn(c, x, y - h)
    return y - h


def heading(c, x, y, label):
    text(c, x, y, label.upper(), 9.1, GREEN, "Helvetica-Bold")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(x, y - 3, x + 96, y - 3)
    return y - 13


def bullet(c, x, y, w, html):
    text(c, x, y - 7, "-", 8, GREEN, "Helvetica-Bold")
    return para(c, x + 9, y, w - 9, html, BODY) - 1


def card(c, name, x, y, w, rotate=0, outline=None, alpha=1):
    path = CARDS / name
    h = w * 1.4
    c.saveState()
    c.translate(x + w / 2, y + h / 2)
    c.rotate(rotate)
    if alpha != 1:
        c.setFillAlpha(alpha)
    c.drawImage(str(path), -w / 2, -h / 2, width=w, height=h, mask="auto")
    if outline:
        c.setStrokeColor(outline)
        c.setLineWidth(2)
        c.roundRect(-w / 2, -h / 2, w, h, 4, stroke=1, fill=0)
    c.restoreState()
    return h


def draw_header(c, width, height):
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(DARK)
    c.roundRect(0.45 * inch, height - 0.82 * inch, width - 0.9 * inch, 0.48 * inch, 12, stroke=0, fill=1)
    text(c, 0.68 * inch, height - 0.56 * inch, "Kings One-Page Rules", 18, colors.white, "Helvetica-Bold")
    text(c, 3.95 * inch, height - 0.54 * inch, "2-6 players | 13 hands | lowest score wins", 9, GOLD, "Helvetica-Bold")


def draw_visuals(c, x, y, w):
    draw_round_rect(c, x, y - 200, w, 200, radius=10)
    centered(c, x, y - 18, w, "Critical card examples", 11, DARK)

    # Set with wild laid sideways.
    sx = x + 18
    sy = y - 88
    card(c, "3_of_clubs.png", sx, sy, 36, rotate=-7)
    card(c, "3_of_diamonds.png", sx + 28, sy, 36, rotate=2)
    card(c, "8_of_hearts.png", sx + 44, sy - 17, 34, rotate=90, outline=RED)
    text(c, sx, sy - 32, "Set: 2 real 3s + wild", 7.3, MUTED, "Helvetica-Bold")
    text(c, sx + 84, sy + 12, "wild", 7.2, RED, "Helvetica-Bold")

    # Run with wild upright.
    rx = x + 142
    card(c, "4_of_spades.png", rx, sy, 30)
    card(c, "8_of_diamonds.png", rx + 36, sy, 30, outline=RED)
    card(c, "6_of_spades.png", rx + 72, sy, 30)
    text(c, rx + 6, sy - 32, "Run: wild stands for 5S", 7.3, MUTED, "Helvetica-Bold")
    text(c, rx + 2, sy - 42, "wild stays upright in the gap", 6.8, RED, "Helvetica-Bold")

    # Scoring.
    bx = x + 18
    by = y - 178
    card(c, "ace_of_hearts.png", bx, by, 27)
    card(c, "7_of_diamonds.png", bx + 34, by, 27)
    card(c, "jack_of_spades.png", bx + 68, by, 27)
    card(c, "joker_red.png", bx + 102, by, 27, outline=RED)
    text(c, bx + 146, by + 20, "Count cards left:", 7.8, DARK, "Helvetica-Bold")
    text(c, bx + 146, by + 9, "A=1, 2-10=face value,", 7.1, MUTED)
    text(c, bx + 146, by - 2, "J/Q/K=10, wilds/jokers=20", 7.1, MUTED)


def draw_footer(c, width):
    y = 0.34 * inch
    c.setStrokeColor(LINE)
    c.line(0.55 * inch, y + 22, width - 0.55 * inch, y + 22)
    text(c, 0.6 * inch, y + 8, "Get Kings:", 7.2, MUTED, "Helvetica-Bold")
    text(c, 1.18 * inch, y + 8, APP_STORE_URL, 7.0, GREEN)
    text(c, 0.6 * inch, y - 3, "Help:", 7.2, MUTED, "Helvetica-Bold")
    text(c, 0.96 * inch, y - 3, HELP_URL, 7.0, GREEN)
    c.linkURL(APP_STORE_URL, (1.16 * inch, y + 6, 4.95 * inch, y + 17), relative=0)
    c.linkURL(HELP_URL, (0.94 * inch, y - 5, 4.9 * inch, y + 6), relative=0)


def draw_reference_box(c, x, y, w, h, title, lines):
    draw_round_rect(c, x, y, w, h, radius=8, fill=colors.HexColor("#fffdf8"), stroke=LINE, width=0.8)
    text(c, x + 10, y + h - 17, title.upper(), 8.4, GREEN, "Helvetica-Bold")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(x + 10, y + h - 21, x + 98, y + h - 21)
    line_y = y + h - 36
    for line in lines:
        text(c, x + 12, line_y, "-", 7.6, GREEN, "Helvetica-Bold")
        text(c, x + 23, line_y, line, 7.45, colors.HexColor("#222222"))
        line_y -= 11


def draw_bottom_reference(c, width):
    y = 1.02 * inch
    h = 0.98 * inch
    gap = 0.18 * inch
    x = 0.62 * inch
    w = (width - 1.24 * inch - gap) / 2
    draw_reference_box(
        c,
        x,
        y,
        w,
        h,
        "Table reminders",
        [
            "Keep hands private around the table.",
            "Dealer gets 8 and skips the first draw.",
            "Use Kings as the scorekeeper, not the card dealer.",
        ],
    )
    draw_reference_box(
        c,
        x + w + gap,
        y,
        w,
        h,
        "Optional table rules",
        [
            "Learning game: keep the help page open.",
            "Short game: stop after an agreed hand.",
            "House rules: agree before hand 1 starts.",
        ],
    )


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    width, height = letter
    draw_header(c, width, height)

    left_x = 0.62 * inch
    right_x = 4.10 * inch
    col_w = 3.12 * inch
    right_w = 3.15 * inch
    y = height - 1.05 * inch

    y = heading(c, left_x, y, "Goal")
    y = bullet(c, left_x, y, col_w, "<b>Play 13 hands.</b> Each hand has a different wild rank.")
    y = bullet(c, left_x, y, col_w, "<b>Go out first to score 0.</b> Everyone else counts cards left in hand.")
    y = bullet(c, left_x, y, col_w, "<b>Lowest total after hand 13 wins.</b>")

    y -= 5
    y = heading(c, left_x, y, "Setup")
    y = bullet(c, left_x, y, col_w, "Use one standard deck plus two jokers.")
    y = bullet(c, left_x, y, col_w, "Deal 7 cards to each player. The dealer gets 8 and takes the first turn.")
    y = bullet(c, left_x, y, col_w, "The dealer does not draw first. The dealer discards to start the discard pile.")

    y -= 5
    y = heading(c, left_x, y, "Turn Order")
    y = bullet(c, left_x, y, col_w, "Draw 1 card from the deck or take the top discard.")
    y = bullet(c, left_x, y, col_w, "Play cards if you can: lay down a set/run or add to an existing meld.")
    y = bullet(c, left_x, y, col_w, "Discard 1 card to end your turn, unless your play used your last card.")

    y -= 5
    y = heading(c, left_x, y, "Sets and Runs")
    y = bullet(c, left_x, y, col_w, "<b>Set:</b> 3 or 4 cards with the same rank. Suits can be different. A set cannot have more than 4 cards total.")
    y = bullet(c, left_x, y, col_w, "<b>Run:</b> 3 or more cards in order, all the same suit. Aces are low, so A-2-3 works; Q-K-A does not.")
    y = bullet(c, left_x, y, col_w, "<b>Meld:</b> any set or run.")

    ry = height - 1.05 * inch
    draw_visuals(c, right_x, ry, right_w)
    ry -= 222

    ry = heading(c, right_x, ry, "Wild Cards")
    ry = bullet(c, right_x, ry, right_w, "Jokers are always wild.")
    ry = bullet(c, right_x, ry, right_w, "The wild rank changes by hand: hand 1 Aces, hand 2 Twos, and so on through hand 13 Kings.")
    ry = bullet(c, right_x, ry, right_w, "In a set, lay a wild sideways across the bottom. The set must have more real cards than wilds.")
    ry = bullet(c, right_x, ry, right_w, "In a run, place the wild upright where the missing card belongs. Wilds cannot sit next to each other.")

    ry -= 5
    ry = heading(c, right_x, ry, "Opening and Adding")
    ry = bullet(c, right_x, ry, right_w, "Before adding to another player's meld, lay down your own set or run first. This is called opening.")
    ry = bullet(c, right_x, ry, right_w, "You may open and add to another meld on the same turn.")

    ry -= 5
    ry = heading(c, right_x, ry, "Replace or Cover a Wild")
    ry = bullet(c, right_x, ry, right_w, "If you have the real card a wild represents in a run, you may play it.")
    ry = bullet(c, right_x, ry, right_w, "Replace: take the wild into your hand to use later.")
    ry = bullet(c, right_x, ry, right_w, "Cover: leave the wild under the real card if you do not want another wild in your hand.")

    y -= 5
    y = heading(c, left_x, y, "Going Out and Scoring")
    y = bullet(c, left_x, y, col_w, "Go out when you have no cards left. You do not need a final discard.")
    y = bullet(c, left_x, y, col_w, "If you can go out, you must go out and the hand ends right away.")
    y = bullet(c, left_x, y, col_w, "Aces count 1. Cards 2-10 count their number. Jacks, Queens, and Kings count 10. Jokers and the wild rank count 20.")

    draw_bottom_reference(c, width)
    draw_footer(c, width)
    c.setTitle("Kings One-Page Rules")
    c.setAuthor("SCIM Ventures")
    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
