"""
main.py – Single-player (Player vs Computer) Tic-Tac-Toe module.

Architecture
------------
* ``ai`` module (bottom section) – pure game-logic, no Tkinter.
  Contains the Minimax algorithm and board helpers.
* ``GUI`` section (top) – Tkinter widgets that call the AI.

Board representation
--------------------
Each cell is stored as an integer:
  -1  → empty
   0  → human player (circle / O)
   1  → computer      (cross  / X)
"""

from tkinter import *
from PIL import Image, ImageTk

# ──────────────────────────────────────────────────────────────
# AI LAYER  (pure logic – no Tkinter)
# ──────────────────────────────────────────────────────────────

HUMAN = 0       # circle
COMPUTER = 1    # cross
EMPTY = -1

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


# ──────────────────────────────────────────────────────────────
# GUI LAYER
# ──────────────────────────────────────────────────────────────

def retry():
    """Reset the board for a new game (New Game button)."""
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global lb5, game_over

    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = EMPTY
    game_over = False

    for bt in [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]:
        bt.config(image='', state=NORMAL)

    lb5.config(text="", bg="light blue")


def disable_all():
    """Disable all board buttons (called after a terminal state)."""
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    for bt in [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]:
        bt.config(state=DISABLED)


def _cell_buttons():
    """Return the nine board buttons as a list (index 0 = bt1)."""
    return [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]


def _board():
    """Snapshot of the current board state as a flat list."""
    return [b1, b2, b3, b4, b5, b6, b7, b8, b9]


def _apply_move(index_0based, player):
    """
    Write a move into the module globals and update the button image.

    Parameters
    ----------
    index_0based : int
        0-based cell index (0–8).
    player : int
        HUMAN (0) or COMPUTER (1).
    """
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    buttons = _cell_buttons()
    img = circleimgtk if player == HUMAN else crossimgtk

    buttons[index_0based].config(image=img, state=DISABLED)

    # Update the matching global variable
    cell_map = [None] * 9

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


def check_winner():
    """
    Inspect the current board.  Display result and lock the board
    if the game has reached a terminal state.

    Returns True if the game ended, False otherwise.
    """
    global lb5, game_over

    board = _board()
    winner = check_winner_board(board)

    if winner == HUMAN:
        lb5.config(text=f"{p1_name} Wins!", fg="Red", bg="lightGreen")
        print(f"{p1_name} wins")
        disable_all()
        game_over = True
        return True

    if winner == COMPUTER:
        lb5.config(text="Computer Wins!", fg="Red", bg="lightGreen")
        print("Computer wins")
        disable_all()
        game_over = True
        return True

    if is_draw(board):
        lb5.config(text="It's a tie!", fg="Red", bg="Cyan")
        print("It's a tie!")
        disable_all()
        game_over = True
        return True

    return False


def player_move(index):
    """
    Handle a human click on cell ``index`` (1-based, matching button names).

    Flow:
      1. Ignore if game is already over.
      2. Apply the human move.
      3. Check for terminal state.
      4. If still playing, let the computer respond via Minimax.
      5. Check for terminal state again.
    """
    global game_over

    # Guard: ignore clicks after the game has ended
    if game_over:
        return

    idx0 = index - 1   # convert to 0-based

    # Guard: cell should not be occupied (button is disabled, but belt-and-braces)
    board = _board()
    if board[idx0] != EMPTY:
        return

    # ── Human move ──────────────────────────────────────────────
    _apply_move(idx0, HUMAN)

    if check_winner():
        return  # human just won or board is full

    # ── Computer move (Minimax) ──────────────────────────────────
    board = _board()   # refresh after human move
    comp_idx = best_move(board)

    if comp_idx == -1:
        # Board is full (shouldn't happen if check_winner caught draw, but safe)
        return

    _apply_move(comp_idx, COMPUTER)
    check_winner()


def start_tic_tac_toe(parent, p1, p2):
    """
    Launch the Single-Player game window.

    Parameters
    ----------
    parent : Tk
        The root window (from entry.py), hidden while this window is open.
    p1 : str
        Human player's name.
    p2 : str
        Always "Computer" when called from entry.py.
    """
    global choice, b1, b2, b3, b4, b5, b6, b7, b8, b9
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global circleimgtk, crossimgtk, lb5
    global p1_name, p2_name, game_over

    p1_name = p1
    p2_name = p2

    # Initialise state
    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = EMPTY
    game_over = False

    # ── Create game window ───────────────────────────────────────
    game = Toplevel(parent)
    game.title("Tic Tac Toe Game")
    game.config(bg="light blue")
    game.geometry("1400x800")

    Label(
        game,
        text=f"Player 1: {p1} (O)  vs  Computer (X)",
        font=("Arial", 14),
        bg="cornsilk",
        fg="grey"
    ).place(x=540, y=120, width=500, height=50)

    # ── Load images ──────────────────────────────────────────────
    circleimgtk = ImageTk.PhotoImage(Image.open("circle.png"))
    crossimgtk  = ImageTk.PhotoImage(Image.open("cross.png"))

    # ── Board buttons ────────────────────────────────────────────
    bt1 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(1))
    bt1.place(x=590, y=200, width=130, height=110)

    bt2 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(2))
    bt2.place(x=720, y=200, width=130, height=110)

    bt3 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(3))
    bt3.place(x=855, y=200, width=130, height=110)

    bt4 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(4))
    bt4.place(x=590, y=320, width=130, height=110)

    bt5 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(5))
    bt5.place(x=720, y=320, width=130, height=110)

    bt6 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(6))
    bt6.place(x=855, y=320, width=130, height=110)

    bt7 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(7))
    bt7.place(x=590, y=440, width=130, height=110)

    bt8 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(8))
    bt8.place(x=720, y=440, width=130, height=110)

    bt9 = Button(game, text="", font=("Arial", 30), width=6, height=3,
                 bg="Grey", command=lambda: player_move(9))
    bt9.place(x=855, y=440, width=130, height=110)

    # ── Decorative labels ────────────────────────────────────────
    Label(game, text="Tic Tac Tok Game",
          font=("Bernard MT Condensed", 30), bg="Cyan", fg="Red"
          ).place(x=580, y=50, width=400, height=50)

    Label(game, font=("Arial", 12), bg="black").place(x=590, y=310,  width=395, height=10)
    Label(game, font=("Arial", 12), bg="black").place(x=590, y=430,  width=395, height=10)
    Label(game, font=("Arial", 12), bg="black").place(x=710, y=200,  width=10,  height=350)
    Label(game, font=("Arial", 12), bg="black").place(x=850, y=200,  width=10,  height=350)

    lb5 = Label(game, font=("Arial", 12), bg="light blue")
    lb5.place(x=615, y=650, width=350, height=50)

    # ── Control buttons ──────────────────────────────────────────
    Button(game, text="Exit Game", font=("Arial", 14),
           command=game.destroy).place(x=1300, y=20, width=80, height=30)

    Button(game, text="New Game", font=("Arial", 14),
           command=retry).place(x=1150, y=20, width=100, height=30)

    game.mainloop()