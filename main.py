"""
main.py – Single-player (Player vs Computer) Tic-Tac-Toe with Neon UI.

Architecture
------------
* AI LAYER  – pure game-logic, no Tkinter (unchanged from feature/computer-ai-improvements).
  Contains the Minimax algorithm and board helpers.
* GUI LAYER – Tkinter widgets built with the neon theme from theme.py.

Board representation
--------------------
Each cell is stored as an integer:
  -1  → empty
   0  → human player (circle / O)  →  NEON_CYAN
   1  → computer      (cross  / X) →  NEON_PURPLE
"""

import tkinter as tk
import theme as T

# ──────────────────────────────────────────────────────────────────────────────
# AI LAYER  (pure logic – no Tkinter, identical to feature/computer-ai-improvements)
# ──────────────────────────────────────────────────────────────────────────────

HUMAN    = 0    # circle  / O
COMPUTER = 1    # cross   / X
EMPTY    = -1

# All winning lines as 0-based indices into a flat 9-cell list
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # cols
    (0, 4, 8), (2, 4, 6),               # diagonals
]


def board_from_globals(b1, b2, b3, b4, b5, b6, b7, b8, b9):
    """Convert the nine module-level cell variables into a list."""
    return [b1, b2, b3, b4, b5, b6, b7, b8, b9]


def check_winner_board(board):
    """
    Return the winner (HUMAN or COMPUTER) if any, else None.
    Uses the flat 9-cell board list.
    """
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board):
    """True when all cells are filled and there is no winner."""
    return all(cell != EMPTY for cell in board) and check_winner_board(board) is None


def get_empty_cells(board):
    """Return list of 0-based indices for empty cells."""
    return [i for i, v in enumerate(board) if v == EMPTY]


def minimax(board, depth, is_maximising):
    """
    Minimax with depth-aware scoring.

    Returns a score from the computer's perspective:
      +10 - depth  → computer wins  (prefer faster wins)
      -10 + depth  → human wins     (prefer to delay losses)
       0           → draw
    """
    winner = check_winner_board(board)
    if winner == COMPUTER:
        return 10 - depth
    if winner == HUMAN:
        return -10 + depth
    if is_draw(board):
        return 0

    empty = get_empty_cells(board)

    if is_maximising:
        best = -100
        for idx in empty:
            board[idx] = COMPUTER
            score = minimax(board, depth + 1, False)
            board[idx] = EMPTY
            best = max(best, score)
        return best
    else:
        best = 100
        for idx in empty:
            board[idx] = HUMAN
            score = minimax(board, depth + 1, True)
            board[idx] = EMPTY
            best = min(best, score)
        return best


def best_move(board):
    """
    Choose the best 0-based cell index for the computer using Minimax.
    Returns -1 if the board is full (caller must guard against this).
    """
    empty = get_empty_cells(board)
    if not empty:
        return -1

    best_score = -100
    best_idx = empty[0]  # safe fallback

    for idx in empty:
        board[idx] = COMPUTER
        score = minimax(board, 0, False)
        board[idx] = EMPTY
        if score > best_score:
            best_score = score
            best_idx = idx

    return best_idx


# ──────────────────────────────────────────────────────────────────────────────
# GUI LAYER  – Neon theme
# ──────────────────────────────────────────────────────────────────────────────

# Module-level state (set by start_tic_tac_toe)
b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = EMPTY
bt1 = bt2 = bt3 = bt4 = bt5 = bt6 = bt7 = bt8 = bt9 = None
status_label = None
p1_name = p2_name = ""
game_over = False
score_x = score_o = score_d = 0   # X wins, O wins, draws
score_labels = {}                  # keys: "x", "o", "d"


# ── Board helpers ─────────────────────────────────────────────────────────────

def _cell_buttons():
    return [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]


def _board():
    return [b1, b2, b3, b4, b5, b6, b7, b8, b9]


def _apply_move(index_0based, player):
    """Write a move into module globals and update the button appearance."""
    global b1, b2, b3, b4, b5, b6, b7, b8, b9

    symbol = "O" if player == HUMAN else "X"
    color  = T.NEON_CYAN if player == HUMAN else T.NEON_PURPLE

    btn = _cell_buttons()[index_0based]
    btn.config(
        text=symbol,
        fg=color,
        state=tk.DISABLED,
        disabledforeground=color,
    )

    def _set(pos, val):
        global b1, b2, b3, b4, b5, b6, b7, b8, b9
        if pos == 0: b1 = val
        elif pos == 1: b2 = val
        elif pos == 2: b3 = val
        elif pos == 3: b4 = val
        elif pos == 4: b5 = val
        elif pos == 5: b6 = val
        elif pos == 6: b7 = val
        elif pos == 7: b8 = val
        elif pos == 8: b9 = val

    _set(index_0based, player)


def disable_all():
    """Disable all board buttons after a terminal state."""
    for bt in _cell_buttons():
        bt.config(state=tk.DISABLED)


def _highlight_winner(winning_line):
    """Highlight the three winning cells with the SUCCESS colour."""
    buttons = _cell_buttons()
    for idx in winning_line:
        buttons[idx].config(bg=T.SUCCESS, disabledforeground=T.BG_MAIN)


def _find_winning_line():
    """Return the winning (a,b,c) triple, or None."""
    board = _board()
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return (a, b, c)
    return None


# ── Game state ────────────────────────────────────────────────────────────────

def _set_status(text, color=T.TEXT_MAIN):
    if status_label:
        status_label.config(text=text, fg=color)


def _update_scores():
    if score_labels:
        score_labels["x"].config(text=str(score_x))
        score_labels["o"].config(text=str(score_o))
        score_labels["d"].config(text=str(score_d))


def retry():
    """Reset the board for a new game."""
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global game_over

    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = EMPTY
    game_over = False

    for bt in _cell_buttons():
        bt.config(
            text="",
            state=tk.NORMAL,
            bg=T.CELL_BG,
            fg=T.TEXT_MAIN,
            disabledforeground=T.TEXT_MAIN,
        )

    _set_status(f"{p1_name}'s turn  (O)", T.NEON_CYAN)


def check_winner():
    """
    Inspect the current board.  Display result and lock the board
    if the game has reached a terminal state.

    Returns True if the game ended, False otherwise.
    """
    global game_over, score_x, score_o, score_d

    board = _board()
    winner = check_winner_board(board)

    if winner == HUMAN:
        wline = _find_winning_line()
        if wline:
            _highlight_winner(wline)
        disable_all()
        game_over = True
        score_o += 1
        _update_scores()
        _set_status(f"🎉  {p1_name} Wins!", T.SUCCESS)
        return True

    if winner == COMPUTER:
        wline = _find_winning_line()
        if wline:
            _highlight_winner(wline)
        disable_all()
        game_over = True
        score_x += 1
        _update_scores()
        _set_status("💻  Computer Wins!", T.ERROR)
        return True

    if is_draw(board):
        # Tint all cells for draw
        for bt in _cell_buttons():
            bt.config(bg=T.BG_SECONDARY)
        disable_all()
        game_over = True
        score_d += 1
        _update_scores()
        _set_status("🤝  It's a Draw!", T.TEXT_DIM)
        return True

    return False


def player_move(index):
    """
    Handle a human click on cell ``index`` (1-based).

    Flow:
      1. Ignore if game is already over.
      2. Apply the human move.
      3. Check for terminal state.
      4. If still playing, let the computer respond via Minimax.
      5. Check for terminal state again.
    """
    global game_over

    if game_over:
        return

    idx0 = index - 1   # convert to 0-based

    board = _board()
    if board[idx0] != EMPTY:
        return

    # ── Human move ────────────────────────────────────────────────────────────
    _set_status("Computer is thinking…", T.TEXT_DIM)
    _apply_move(idx0, HUMAN)

    if check_winner():
        return

    # ── Computer move (Minimax) ───────────────────────────────────────────────
    board = _board()
    comp_idx = best_move(board)

    if comp_idx == -1:
        return  # board full (draw already caught above, but safe)

    _apply_move(comp_idx, COMPUTER)
    if not check_winner():
        _set_status(f"{p1_name}'s turn  (O)", T.NEON_CYAN)


# ── Cell hover effects ────────────────────────────────────────────────────────

def _bind_hover(btn):
    """Attach enter/leave hover highlight to an empty cell button."""
    def on_enter(e):
        if btn["state"] == tk.NORMAL:
            btn.config(bg=T.CELL_HOVER)

    def on_leave(e):
        if btn["state"] == tk.NORMAL and btn["text"] == "":
            btn.config(bg=T.CELL_BG)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


# ── Window builder ────────────────────────────────────────────────────────────

def start_tic_tac_toe(parent, p1, p2):
    """
    Launch the Single-Player (vs Computer) game window.

    Parameters
    ----------
    parent : Tk
        The root window (from entry.py), hidden while this window is open.
    p1 : str
        Human player's name.
    p2 : str
        Always "Computer" when called from entry.py.
    """
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global status_label, score_labels
    global p1_name, p2_name, game_over
    global score_x, score_o, score_d

    p1_name = p1
    p2_name = p2

    # Reset state
    score_x = score_o = score_d = 0
    retry.__wrapped__ = False  # clear any stale state
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = EMPTY
    game_over = False

    # ── Window ───────────────────────────────────────────────────────────────
    game = tk.Toplevel(parent)
    game.title("Tic-Tac-Toe  ✦  vs Computer")
    game.config(bg=T.BG_MAIN)
    game.geometry(f"{T.WIN_W}x{T.WIN_H}")
    game.resizable(False, False)

    def _on_close():
        parent.deiconify()
        game.destroy()

    game.protocol("WM_DELETE_WINDOW", _on_close)

    # ── Left neon stripe ─────────────────────────────────────────────────────
    tk.Frame(game, bg=T.NEON_PURPLE).place(x=0, y=0, width=4, height=T.WIN_H)
    tk.Frame(game, bg=T.NEON_CYAN).place(x=T.WIN_W - 4, y=0, width=4, height=T.WIN_H)

    # ── Header ───────────────────────────────────────────────────────────────
    tk.Label(
        game, text="✦  TIC-TAC-TOE  ✦",
        font=T.FONT_TITLE, bg=T.BG_MAIN, fg=T.NEON_CYAN,
    ).place(x=0, y=18, width=T.WIN_W, height=44)

    tk.Label(
        game,
        text=f"{p1}  (O)   vs   Computer  (X)",
        font=T.FONT_SUBTITLE, bg=T.BG_MAIN, fg=T.TEXT_DIM,
    ).place(x=0, y=66, width=T.WIN_W, height=22)

    # Divider
    tk.Frame(game, bg=T.NEON_PURPLE).place(x=160, y=96, width=T.WIN_W - 320, height=2)

    # ── Score panel ───────────────────────────────────────────────────────────
    # Container
    score_frame = tk.Frame(game, bg=T.BG_PANEL, bd=0)
    score_frame.place(x=20, y=108, width=200, height=120)

    tk.Label(score_frame, text="SCORE", font=("Segoe UI", 9, "bold"),
             bg=T.BG_PANEL, fg=T.TEXT_DIM).pack(pady=(8, 4))

    for label_text, key, color in [
        (f"{p1} (O)", "o", T.NEON_CYAN),
        ("Computer (X)", "x", T.NEON_PURPLE),
        ("Draws", "d", T.TEXT_DIM),
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
    status_label = tk.Label(
        game,
        text=f"{p1}'s turn  (O)",
        font=T.FONT_STATUS,
        bg=T.BG_MAIN,
        fg=T.NEON_CYAN,
        anchor="center",
    )
    status_label.place(x=0, y=108, width=T.WIN_W, height=36)

    # ── Board ─────────────────────────────────────────────────────────────────
    BOARD_LEFT = (T.WIN_W - (3 * T.CELL_SIZE + 2 * T.CELL_GAP)) // 2
    BOARD_TOP  = 158

    cell_buttons = []
    for row in range(3):
        for col in range(3):
            idx = row * 3 + col + 1   # 1-based
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
                command=lambda i=idx: player_move(i),
            )
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

    _make_ctrl_btn("↺  New Game", T.NEON_CYAN,   retry,        BOARD_LEFT)
    _make_ctrl_btn("✕  Exit",     T.ERROR, _on_close, BOARD_LEFT + T.CELL_SIZE * 3 + T.CELL_GAP * 2 - 160)

    game.mainloop()