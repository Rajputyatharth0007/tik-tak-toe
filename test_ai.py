"""
test_ai.py – Automated tests for the Minimax computer AI in main.py.

Run with:
    python test_ai.py

Tests do NOT launch any Tkinter windows; they exercise only the pure
logic functions (minimax, best_move, check_winner_board, is_draw).
"""

import sys
import types
import unittest

# ── Stub tkinter so importing main.py doesn't open any windows ────────────────
# We only need the AI functions (minimax, best_move, etc.), not the GUI.
tk_stub = types.ModuleType("tkinter")
for _name in ("Tk", "Toplevel", "Label", "Button", "Entry", "IntVar",
              "Frame", "END"):
    setattr(tk_stub, _name, object)
tk_stub.NORMAL   = "normal"
tk_stub.DISABLED = "disabled"
tk_stub.FLAT     = "flat"
sys.modules.setdefault("tkinter", tk_stub)

pil_stub = types.ModuleType("PIL")
pil_image = types.ModuleType("PIL.Image")
pil_imagetk = types.ModuleType("PIL.ImageTk")
pil_image.open = lambda *a, **kw: None
pil_imagetk.PhotoImage = lambda *a, **kw: None
sys.modules.setdefault("PIL", pil_stub)
sys.modules.setdefault("PIL.Image", pil_image)
sys.modules.setdefault("PIL.ImageTk", pil_imagetk)

# Stub theme module so main.py can be imported without actual colors/fonts
theme_stub = types.ModuleType("theme")
for _attr in ("BG_MAIN", "BG_PANEL", "BG_SECONDARY", "NEON_CYAN", "NEON_PURPLE",
              "SUCCESS", "ERROR", "TEXT_MAIN", "TEXT_DIM", "CELL_BG", "CELL_HOVER",
              "CELL_DISABLED", "BTN_BG", "BTN_ACTIVE", "FONT_TITLE", "FONT_SUBTITLE",
              "FONT_HEADING", "FONT_BODY", "FONT_BTN", "FONT_CELL", "FONT_STATUS",
              "FONT_SCORE", "WIN_W", "WIN_H", "CELL_SIZE", "CELL_GAP"):
    setattr(theme_stub, _attr, "")
sys.modules.setdefault("theme", theme_stub)

# Now safely import the AI layer from main.py
import main as game_ai

EMPTY    = game_ai.EMPTY     # -1
HUMAN    = game_ai.HUMAN     #  0
COMPUTER = game_ai.COMPUTER  #  1


def make_board(*rows):
    """Helper: create a flat 9-cell board from three 3-element tuples."""
    return list(rows[0]) + list(rows[1]) + list(rows[2])


class TestCheckWinnerBoard(unittest.TestCase):

    def test_human_row_win(self):
        b = make_board([HUMAN,   HUMAN,    HUMAN],
                       [COMPUTER, EMPTY,   EMPTY],
                       [EMPTY,    EMPTY,   EMPTY])
        self.assertEqual(game_ai.check_winner_board(b), HUMAN)

    def test_computer_col_win(self):
        b = make_board([COMPUTER, HUMAN,    HUMAN],
                       [COMPUTER, HUMAN,    EMPTY],
                       [COMPUTER, EMPTY,   EMPTY])
        self.assertEqual(game_ai.check_winner_board(b), COMPUTER)

    def test_diagonal_win(self):
        b = make_board([HUMAN,  COMPUTER, COMPUTER],
                       [EMPTY,  HUMAN,    COMPUTER],
                       [EMPTY,  EMPTY,    HUMAN])
        self.assertEqual(game_ai.check_winner_board(b), HUMAN)

    def test_no_winner_yet(self):
        b = make_board([HUMAN,  COMPUTER, EMPTY],
                       [EMPTY,  EMPTY,    EMPTY],
                       [EMPTY,  EMPTY,    EMPTY])
        self.assertIsNone(game_ai.check_winner_board(b))

    def test_empty_board_no_winner(self):
        b = [EMPTY] * 9
        self.assertIsNone(game_ai.check_winner_board(b))


class TestIsDraw(unittest.TestCase):

    def test_full_board_draw(self):
        # O X O
        # X X O
        # X O X   → draw
        b = make_board([HUMAN,    COMPUTER, HUMAN],
                       [COMPUTER, COMPUTER, HUMAN],
                       [COMPUTER, HUMAN,    COMPUTER])
        self.assertTrue(game_ai.is_draw(b))

    def test_not_draw_winner_exists(self):
        b = make_board([HUMAN,  HUMAN,    HUMAN],
                       [COMPUTER, EMPTY,  EMPTY],
                       [EMPTY,  EMPTY,    EMPTY])
        self.assertFalse(game_ai.is_draw(b))

    def test_not_draw_empty_cells(self):
        b = [EMPTY] * 9
        self.assertFalse(game_ai.is_draw(b))


class TestBestMove(unittest.TestCase):

    def test_computer_takes_winning_move(self):
        """Computer has two in a row – it must complete the win."""
        b = make_board([COMPUTER, COMPUTER, EMPTY],
                       [HUMAN,    HUMAN,    EMPTY],
                       [EMPTY,    EMPTY,    EMPTY])
        move = game_ai.best_move(b)
        self.assertEqual(move, 2,
            f"Computer should win at index 2, chose {move}")

    def test_computer_blocks_human_win(self):
        """Human has two in a row – computer must block."""
        b = make_board([HUMAN,  HUMAN,   EMPTY],
                       [COMPUTER, EMPTY, EMPTY],
                       [EMPTY,    EMPTY, EMPTY])
        move = game_ai.best_move(b)
        self.assertEqual(move, 2,
            f"Computer should block at index 2, chose {move}")

    def test_computer_takes_column_win(self):
        """Computer can win via column – it should take it."""
        b = make_board([COMPUTER, HUMAN,    HUMAN],
                       [COMPUTER, HUMAN,    EMPTY],
                       [EMPTY,    EMPTY,    EMPTY])
        move = game_ai.best_move(b)
        self.assertEqual(move, 6,
            f"Computer should win at index 6, chose {move}")

    def test_computer_blocks_diagonal(self):
        """Human threatens diagonal win – computer must block."""
        b = make_board([HUMAN,    COMPUTER, EMPTY],
                       [COMPUTER, HUMAN,    EMPTY],
                       [EMPTY,    EMPTY,    EMPTY])
        move = game_ai.best_move(b)
        self.assertEqual(move, 8,
            f"Computer should block diagonal at index 8, chose {move}")

    def test_no_move_on_full_board(self):
        b = make_board([HUMAN,    COMPUTER, HUMAN],
                       [COMPUTER, COMPUTER, HUMAN],
                       [COMPUTER, HUMAN,    COMPUTER])
        move = game_ai.best_move(b)
        self.assertEqual(move, -1)


class TestMinimaxUnbeatable(unittest.TestCase):
    """
    Exhaustive verification: simulate every possible game where the computer
    plays first as X against a random human.  The computer must NEVER lose.
    """

    def _simulate_all(self, board, is_computer_turn):
        """
        Recursively enumerate all legal game branches.
        Returns True if the computer never loses along any branch.
        """
        winner = game_ai.check_winner_board(board)
        if winner == COMPUTER:
            return True   # computer won – fine
        if winner == HUMAN:
            return False  # computer lost – fail
        if game_ai.is_draw(board):
            return True   # draw – acceptable

        empty = game_ai.get_empty_cells(board)

        if is_computer_turn:
            idx = game_ai.best_move(board)
            board[idx] = COMPUTER
            result = self._simulate_all(board, False)
            board[idx] = EMPTY
            return result
        else:
            # Human plays every possible move
            for idx in empty:
                board[idx] = HUMAN
                if not self._simulate_all(board, True):
                    board[idx] = EMPTY
                    return False
                board[idx] = EMPTY
            return True

    def test_computer_never_loses_going_first(self):
        """Computer goes first: must never lose against any human play."""
        board = [EMPTY] * 9
        self.assertTrue(
            self._simulate_all(board, True),
            "Computer lost at least one game – Minimax is broken!"
        )

    def test_computer_never_loses_going_second(self):
        """Computer goes second: must never lose against any human play."""

        def simulate_human_first(board, is_human_turn):
            winner = game_ai.check_winner_board(board)
            if winner == COMPUTER:
                return True
            if winner == HUMAN:
                return False
            if game_ai.is_draw(board):
                return True

            empty = game_ai.get_empty_cells(board)

            if is_human_turn:
                for idx in empty:
                    board[idx] = HUMAN
                    if not simulate_human_first(board, False):
                        board[idx] = EMPTY
                        return False
                    board[idx] = EMPTY
                return True
            else:
                idx = game_ai.best_move(board)
                board[idx] = COMPUTER
                result = simulate_human_first(board, True)
                board[idx] = EMPTY
                return result

        board = [EMPTY] * 9
        self.assertTrue(
            simulate_human_first(board, True),
            "Computer lost as second player – Minimax is broken!"
        )


class TestGetEmptyCells(unittest.TestCase):

    def test_all_empty(self):
        self.assertEqual(game_ai.get_empty_cells([EMPTY] * 9), list(range(9)))

    def test_none_empty(self):
        board = [HUMAN, COMPUTER] * 4 + [HUMAN]
        self.assertEqual(game_ai.get_empty_cells(board), [])

    def test_mixed(self):
        board = [HUMAN, EMPTY, COMPUTER, EMPTY, EMPTY, HUMAN, COMPUTER, EMPTY, EMPTY]
        self.assertEqual(game_ai.get_empty_cells(board), [1, 3, 4, 7, 8])


if __name__ == "__main__":
    unittest.main(verbosity=2)
