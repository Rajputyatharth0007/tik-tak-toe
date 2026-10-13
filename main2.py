"""
main2.py – Two-player Tic-Tac-Toe with Neon UI.

Player 1 plays O  (NEON_CYAN).
Player 2 plays X  (NEON_PURPLE).
Turn alternates via choice IntVar (odd = O, even = X).

Board values: -1 empty  /  0 = O (P1)  /  1 = X (P2)
"""

import tkinter as tk
import theme as T
from PIL import Image, ImageTk   # kept for backward-compat; images no longer used in neon build

# ── Shared state set by start_tic_tac_toe ─────────────────────────────────────
b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = -1
bt1 = bt2 = bt3 = bt4 = bt5 = bt6 = bt7 = bt8 = bt9 = None
choice    = None
lb5       = None    # status label
p1_name   = ""
p2_name   = ""
score_p1 = score_p2 = score_d = 0
score_labels = {}


# ── Win lines (0-based flat list) ─────────────────────────────────────────────
_WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def _all_buttons():
    return [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]


def _board_vals():
    return [b1, b2, b3, b4, b5, b6, b7, b8, b9]


def disable_all():
    """Lock the board after a terminal state."""
    for bt in _all_buttons():
        bt.config(state=tk.DISABLED)


def _find_winning_line(player_val):
    """Return the winning (a,b,c) triple for player_val, or None."""
    board = _board_vals()
    for a, b, c in _WIN_LINES:
        if board[a] == board[b] == board[c] == player_val:
            return (a, b, c)
    return None


def _highlight_winner(line, color):
    buttons = _all_buttons()
    for idx in line:
        buttons[idx].config(bg=T.SUCCESS, disabledforeground=T.BG_MAIN)


def _set_status(text, color=T.TEXT_MAIN):
    if lb5:
        lb5.config(text=text, fg=color)


def _update_scores():
    if score_labels:
        score_labels["p1"].config(text=str(score_p1))
        score_labels["p2"].config(text=str(score_p2))
        score_labels["d"].config(text=str(score_d))


# ── Reset ─────────────────────────────────────────────────────────────────────

def reset():
    """Reset board for a new game."""
    global b1, b2, b3, b4, b5, b6, b7, b8, b9, choice

    choice.set(1)
    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = -1

    for bt in _all_buttons():
        bt.config(text="", state=tk.NORMAL, bg=T.CELL_BG, fg=T.TEXT_MAIN,
                  disabledforeground=T.TEXT_MAIN)

    _set_status(f"{p1_name}'s turn  (O)", T.NEON_CYAN)


# ── Check winner ──────────────────────────────────────────────────────────────

def check_winner():
    global score_p1, score_p2, score_d

    board = _board_vals()

    # Player 1 (O = 0)
    wline = _find_winning_line(0)
    if wline:
        _highlight_winner(wline, T.NEON_CYAN)
        disable_all()
        score_p1 += 1
        _update_scores()
        _set_status(f"🎉  {p1_name} Wins!", T.SUCCESS)
        return

    # Player 2 (X = 1)
    wline = _find_winning_line(1)
    if wline:
        _highlight_winner(wline, T.NEON_PURPLE)
        disable_all()
        score_p2 += 1
        _update_scores()
        _set_status(f"🎉  {p2_name} Wins!", T.SUCCESS)
        return

    # Draw
    if all(v != -1 for v in board):
        for bt in _all_buttons():
            bt.config(bg=T.BG_SECONDARY)
        disable_all()
        score_d += 1
        _update_scores()
        _set_status("🤝  It's a Draw!", T.TEXT_DIM)
        return

    # Game still going – update turn indicator
    next_is_p1 = (choice.get() % 2 != 0)
    if next_is_p1:
        _set_status(f"{p1_name}'s turn  (O)", T.NEON_CYAN)
    else:
        _set_status(f"{p2_name}'s turn  (X)", T.NEON_PURPLE)


# ── Cell hover ────────────────────────────────────────────────────────────────

def _bind_hover(btn):
    def on_enter(e):
        if btn["state"] == tk.NORMAL:
            btn.config(bg=T.CELL_HOVER)

    def on_leave(e):
        if btn["state"] == tk.NORMAL and btn["text"] == "":
            btn.config(bg=T.CELL_BG)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


# ── Generic cell handler ───────────────────────────────────────────────────────

def _handle_cell(btn, cell_idx_0based):
    """
    Generic click handler for any of the 9 cells.

    cell_idx_0based: 0-8
    choice odd  → O (P1, value 0, NEON_CYAN)
    choice even → X (P2, value 1, NEON_PURPLE)
    """
    global b1, b2, b3, b4, b5, b6, b7, b8, b9

    is_p1 = (choice.get() % 2 != 0)
    symbol = "O" if is_p1 else "X"
    color  = T.NEON_CYAN if is_p1 else T.NEON_PURPLE
    value  = 0 if is_p1 else 1

    btn.config(text=symbol, fg=color, state=tk.DISABLED, disabledforeground=color)
    choice.set(choice.get() + 1)

    # Write board value
    targets = [None, None, None, None, None, None, None, None, None]
    ref = _board_vals()
    # update the correct global
    if cell_idx_0based == 0: b1 = value
    elif cell_idx_0based == 1: b2 = value
    elif cell_idx_0based == 2: b3 = value
    elif cell_idx_0based == 3: b4 = value
    elif cell_idx_0based == 4: b5 = value
    elif cell_idx_0based == 5: b6 = value
    elif cell_idx_0based == 6: b7 = value
    elif cell_idx_0based == 7: b8 = value
    elif cell_idx_0based == 8: b9 = value

    check_winner()


# ── Window builder ────────────────────────────────────────────────────────────

def start_tic_tac_toe(parent, p1, p2):
    """
    Launch the Two-Player game window.

    Parameters
    ----------
    parent : Tk
        The root window (from entry.py), hidden while this window is open.
    p1, p2 : str
        Player names.
    """
    global choice, lb5, score_labels
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global p1_name, p2_name
    global score_p1, score_p2, score_d
    global b1, b2, b3, b4, b5, b6, b7, b8, b9

    p1_name = p1
    p2_name = p2
    score_p1 = score_p2 = score_d = 0
    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = -1

    # ── Window ───────────────────────────────────────────────────────────────
    game = tk.Toplevel(parent)
    game.title("Tic-Tac-Toe  ✦  Two Player")
    game.config(bg=T.BG_MAIN)
    game.geometry(f"{T.WIN_W}x{T.WIN_H}")
    game.resizable(False, False)

    def _on_close():
        parent.deiconify()
        game.destroy()

    game.protocol("WM_DELETE_WINDOW", _on_close)

    choice = tk.IntVar(game)
    choice.set(1)

    # ── Neon stripes ─────────────────────────────────────────────────────────
    tk.Frame(game, bg=T.NEON_CYAN).place(x=0, y=0, width=4, height=T.WIN_H)
    tk.Frame(game, bg=T.NEON_PURPLE).place(x=T.WIN_W - 4, y=0, width=4, height=T.WIN_H)

    # ── Header ───────────────────────────────────────────────────────────────
    tk.Label(
        game, text="✦  TIC-TAC-TOE  ✦",
        font=T.FONT_TITLE, bg=T.BG_MAIN, fg=T.NEON_CYAN,
    ).place(x=0, y=18, width=T.WIN_W, height=44)

    tk.Label(
        game,
        text=f"{p1}  (O)   vs   {p2}  (X)",
        font=T.FONT_SUBTITLE, bg=T.BG_MAIN, fg=T.TEXT_DIM,
    ).place(x=0, y=66, width=T.WIN_W, height=22)

    tk.Frame(game, bg=T.NEON_CYAN).place(x=160, y=96, width=T.WIN_W - 320, height=2)

    # ── Score panel ───────────────────────────────────────────────────────────
    score_frame = tk.Frame(game, bg=T.BG_PANEL, bd=0)
    score_frame.place(x=20, y=108, width=200, height=120)

    tk.Label(score_frame, text="SCORE", font=("Segoe UI", 9, "bold"),
             bg=T.BG_PANEL, fg=T.TEXT_DIM).pack(pady=(8, 4))

    score_labels = {}
    for label_text, key, color in [
        (f"{p1} (O)", "p1", T.NEON_CYAN),
        (f"{p2} (X)", "p2", T.NEON_PURPLE),
        ("Draws",     "d",  T.TEXT_DIM),
    ]:
        row = tk.Frame(score_frame, bg=T.BG_PANEL)
        row.pack(fill=tk.X, padx=10, pady=1)
        tk.Label(row, text=label_text, font=T.FONT_SCORE,
                 bg=T.BG_PANEL, fg=color, anchor="w").pack(side=tk.LEFT)
        val_lbl = tk.Label(row, text="0", font=("Segoe UI", 11, "bold"),
                           bg=T.BG_PANEL, fg=color, anchor="e")
        val_lbl.pack(side=tk.RIGHT)
        score_labels[key] = val_lbl

    # ── Status label ──────────────────────────────────────────────────────────
    lb5 = tk.Label(
        game,
        text=f"{p1}'s turn  (O)",
        font=T.FONT_STATUS,
        bg=T.BG_MAIN,
        fg=T.NEON_CYAN,
        anchor="center",
    )
    lb5.place(x=0, y=108, width=T.WIN_W, height=36)

    # ── Board ─────────────────────────────────────────────────────────────────
    BOARD_LEFT = (T.WIN_W - (3 * T.CELL_SIZE + 2 * T.CELL_GAP)) // 2
    BOARD_TOP  = 158

    cell_buttons = []
    for row in range(3):
        for col in range(3):
            idx0 = row * 3 + col
            x = BOARD_LEFT + col * (T.CELL_SIZE + T.CELL_GAP)
            y = BOARD_TOP  + row * (T.CELL_SIZE + T.CELL_GAP)

            btn = tk.Button(
                game,
                text="",
                font=T.FONT_CELL,
                bg=T.CELL_BG,
                fg=T.TEXT_MAIN,
                activebackground=T.CELL_HOVER,
                activeforeground=T.TEXT_MAIN,
                disabledforeground=T.TEXT_MAIN,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
            )
            # capture idx0 in closure
            btn.config(command=lambda b=btn, i=idx0: _handle_cell(b, i))
            btn.place(x=x, y=y, width=T.CELL_SIZE, height=T.CELL_SIZE)
            _bind_hover(btn)
            cell_buttons.append(btn)

    bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9 = cell_buttons

    # ── Control buttons ───────────────────────────────────────────────────────
    BTN_Y = BOARD_TOP + 3 * T.CELL_SIZE + 2 * T.CELL_GAP + 20

    def _make_ctrl_btn(text, color, cmd, x):
        b = tk.Button(
            game, text=text, font=T.FONT_BTN,
            bg=color, fg=T.BG_MAIN,
            activebackground=T.TEXT_MAIN, activeforeground=T.BG_MAIN,
            relief=tk.FLAT, bd=0, cursor="hand2",
            command=cmd,
        )
        b.place(x=x, y=BTN_Y, width=160, height=40)
        b.bind("<Enter>", lambda e: b.config(bg=T.TEXT_MAIN))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    _make_ctrl_btn("↺  New Game", T.NEON_CYAN,   reset,      BOARD_LEFT)
    _make_ctrl_btn("✕  Exit",     T.ERROR, _on_close, BOARD_LEFT + T.CELL_SIZE * 3 + T.CELL_GAP * 2 - 160)

    game.mainloop()
