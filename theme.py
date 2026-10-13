"""
theme.py – Shared neon-gaming theme constants.

Import this module in entry.py, main.py and main2.py to keep
all colors, fonts, and sizes in one place.
"""

# ── Colour palette ────────────────────────────────────────────────────────────
BG_MAIN       = "#0B1020"   # deep space background
BG_PANEL      = "#151C32"   # game panel
BG_SECONDARY  = "#1D2742"   # secondary panel / cell base
NEON_CYAN     = "#00E5FF"   # player O  / accents
NEON_PURPLE   = "#A855F7"   # player X  / accents
SUCCESS       = "#22C55E"   # win state
ERROR         = "#FB7185"   # loss / draw state
TEXT_MAIN     = "#F8FAFC"   # primary text
TEXT_DIM      = "#94A3B8"   # secondary / subdued text

# Cell colours
CELL_BG        = "#1D2742"
CELL_HOVER     = "#263355"
CELL_DISABLED  = "#141C30"

# Button colours
BTN_BG         = "#1D2742"
BTN_ACTIVE     = "#263355"

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_TITLE     = ("Segoe UI", 28, "bold")
FONT_SUBTITLE  = ("Segoe UI", 13)
FONT_HEADING   = ("Segoe UI", 16, "bold")
FONT_BODY      = ("Segoe UI", 12)
FONT_BTN       = ("Segoe UI", 12, "bold")
FONT_CELL      = ("Segoe UI", 44, "bold")
FONT_STATUS    = ("Segoe UI", 14, "bold")
FONT_SCORE     = ("Segoe UI", 11)

# ── Layout ────────────────────────────────────────────────────────────────────
WIN_W          = 820
WIN_H          = 680
CELL_SIZE      = 140   # px per board cell
CELL_GAP       = 6     # gap between cells
