"""
entry.py – Neon-themed launcher / mode-selection screen.

Presents a premium lobby where the player:
  1. Chooses Single Player (vs Computer) or Two Player.
  2. Enters their name(s).
  3. Launches the appropriate game window.
"""

from tkinter import *
import main
import main2
import theme as T


# ── Helpers ───────────────────────────────────────────────────────────────────

def _styled_entry(parent):
    """Return a themed Entry widget."""
    e = Entry(
        parent,
        font=T.FONT_BODY,
        bg=T.BG_SECONDARY,
        fg=T.TEXT_MAIN,
        insertbackground=T.NEON_CYAN,
        relief=FLAT,
        highlightthickness=2,
        highlightcolor=T.NEON_CYAN,
        highlightbackground=T.BG_SECONDARY,
    )
    return e


def _neon_btn(parent, text, color, command):
    """Return a styled neon action button."""
    btn = Button(
        parent,
        text=text,
        font=T.FONT_BTN,
        bg=color,
        fg=T.BG_MAIN,
        activebackground=T.TEXT_MAIN,
        activeforeground=T.BG_MAIN,
        relief=FLAT,
        bd=0,
        cursor="hand2",
        command=command,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=T.TEXT_MAIN))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def _clear_lobby():
    """Destroy all lobby-phase widgets except the persistent header."""
    for w in root.winfo_children():
        if getattr(w, "_lobby_phase", False):
            w.destroy()


def _show_name_form(mode):
    """
    Render name-entry form for the chosen mode ('single' or 'two').
    Destroys any previous form widgets first.
    """
    _clear_lobby()

    form_y = 280

    # ── Player 1 label + entry ────────────────────────────────────────────────
    lbl1 = Label(root, text="Your Name" if mode == "single" else "Player 1 Name",
                 font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.TEXT_DIM)
    lbl1.place(x=160, y=form_y, width=300, height=24)
    lbl1._lobby_phase = True

    global entry1
    entry1 = _styled_entry(root)
    entry1.place(x=160, y=form_y + 28, width=300, height=36)
    entry1._lobby_phase = True
    entry1.focus_set()

    if mode == "two":
        # ── Player 2 ─────────────────────────────────────────────────────────
        lbl2 = Label(root, text="Player 2 Name",
                     font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.TEXT_DIM)
        lbl2.place(x=160, y=form_y + 80, width=300, height=24)
        lbl2._lobby_phase = True

        global entry2
        entry2 = _styled_entry(root)
        entry2.place(x=160, y=form_y + 108, width=300, height=36)
        entry2._lobby_phase = True

        btn_y = form_y + 168
    else:
        btn_y = form_y + 88

    # ── Error label ───────────────────────────────────────────────────────────
    global error_label
    error_label = Label(root, text="", font=("Segoe UI", 10),
                        bg=T.BG_MAIN, fg=T.ERROR)
    error_label.place(x=160, y=btn_y - 4, width=300, height=20)
    error_label._lobby_phase = True

    # ── Start button ──────────────────────────────────────────────────────────
    cmd = _start_single if mode == "single" else _start_two
    start_btn = _neon_btn(root, "▶  Launch Game", T.NEON_CYAN, cmd)
    start_btn.place(x=160, y=btn_y + 22, width=300, height=44)
    start_btn._lobby_phase = True

    # bind Enter key
    root.bind("<Return>", lambda e: cmd())


def _start_single():
    name = entry1.get().strip()
    if not name:
        error_label.config(text="⚠  Please enter your name.")
        return
    root.withdraw()
    main.start_tic_tac_toe(root, name, "Computer")


def _start_two():
    p1 = entry1.get().strip()
    p2 = entry2.get().strip()
    if not p1 or not p2:
        error_label.config(text="⚠  Please enter both names.")
        return
    root.withdraw()
    main2.start_tic_tac_toe(root, p1, p2)


# ── Root window ───────────────────────────────────────────────────────────────

root = Tk()
root.title("Tic-Tac-Toe  ✦  Neon Edition")
root.geometry(f"{T.WIN_W}x{T.WIN_H}")
root.resizable(False, False)
root.config(bg=T.BG_MAIN)

# ── Background accent bar ─────────────────────────────────────────────────────
accent = Frame(root, bg=T.BG_PANEL, height=T.WIN_H)
accent.place(x=0, y=0, width=T.WIN_W, height=T.WIN_H)

# Left neon stripe
Frame(root, bg=T.NEON_CYAN).place(x=0, y=0, width=4, height=T.WIN_H)
# Right neon stripe
Frame(root, bg=T.NEON_PURPLE).place(x=T.WIN_W - 4, y=0, width=4, height=T.WIN_H)

# ── Title block ───────────────────────────────────────────────────────────────
Label(
    root, text="✦  TIC-TAC-TOE  ✦",
    font=T.FONT_TITLE,
    bg=T.BG_PANEL, fg=T.NEON_CYAN,
).place(x=0, y=80, width=T.WIN_W, height=50)

Label(
    root, text="Neon Edition — Choose Your Mode",
    font=T.FONT_SUBTITLE,
    bg=T.BG_PANEL, fg=T.TEXT_DIM,
).place(x=0, y=136, width=T.WIN_W, height=26)

# ── Divider ───────────────────────────────────────────────────────────────────
Frame(root, bg=T.NEON_CYAN).place(x=200, y=172, width=T.WIN_W - 400, height=2)

# ── Mode buttons ─────────────────────────────────────────────────────────────
Label(
    root, text="SELECT MODE",
    font=("Segoe UI", 10, "bold"),
    bg=T.BG_PANEL, fg=T.TEXT_DIM,
).place(x=0, y=196, width=T.WIN_W, height=22)

btn_sp = _neon_btn(root, "🤖  Single Player  (vs Computer)", T.NEON_PURPLE,
                   lambda: _show_name_form("single"))
btn_sp.place(x=160, y=226, width=300, height=44)

btn_tp = _neon_btn(root, "👥  Two Player", T.NEON_CYAN,
                   lambda: _show_name_form("two"))
btn_tp.place(x=480, y=226, width=200, height=44)

# ── Initial mode hint ─────────────────────────────────────────────────────────
Label(
    root, text="↑  Pick a mode to enter player names",
    font=("Segoe UI", 10),
    bg=T.BG_PANEL, fg=T.TEXT_DIM,
).place(x=0, y=278, width=T.WIN_W, height=20)

# ── Footer ────────────────────────────────────────────────────────────────────
Label(
    root, text="Minimax AI  ·  Unbeatable Computer Opponent",
    font=("Segoe UI", 9),
    bg=T.BG_PANEL, fg=T.TEXT_DIM,
).place(x=0, y=T.WIN_H - 32, width=T.WIN_W, height=24)

root.mainloop()