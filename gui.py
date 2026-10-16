"""
=============================================================================
File: gui.py
Description: Tkinter Graphical User Interface.
What this file does:
  - Uses Python Object-Oriented Programming (OOP) to subclass `tk.Frame`.
  - Displays a clean 3x3 grid of interactive buttons.
  - Connects button clicks to the game logic in `engine.py`.
  - Lets the computer take its turn automatically when playing vs AI.
  - Highlights the winning 3-in-a-row line and tracks scores across rounds.
=============================================================================
"""

import tkinter as tk
from engine import TicTacToe
from ai import get_computer_move


class TicTacToeGrid(tk.Frame):
    """
    Subclasses tk.Frame to manage the 3x3 button grid.
    This fulfills the OOP Frame sub-classing enhancement.
    """

    def __init__(self, master, game, on_game_event, **kwargs):
        super().__init__(master, bg="#1e1e2e", **kwargs)
        self.game = game
        self.on_game_event = on_game_event
        self.buttons = {}
        self._create_buttons()

    def _create_buttons(self):
        """Builds the 3x3 grid of buttons inside this Frame."""
        for r in range(3):
            self.rowconfigure(r, weight=1, minsize=80)
            for c in range(3):
                self.columnconfigure(c, weight=1, minsize=80)
                btn = tk.Button(
                    self,
                    text=" ",
                    font=("Helvetica", 28, "bold"),
                    bg="#313244",
                    fg="#cdd6f4",
                    activebackground="#45475a",
                    activeforeground="#cdd6f4",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda row=r, col=c: self.on_cell_clicked(row, col),
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                self.buttons[(r, c)] = btn

    def on_cell_clicked(self, row, col):
        """Triggered when a player clicks a cell on the grid."""
        self.on_game_event("player_click", (row, col))

    def update_cell(self, row, col, player):
        """Updates a button text and color with the player mark."""
        btn = self.buttons[(row, col)]
        color = "#f38ba8" if player == "X" else "#89b4fa"  # Coral for X, Blue for O
        btn.config(text=player, fg=color, state="disabled")

    def highlight_winner(self, winning_line):
        """Highlights the 3 winning cells in bright green."""
        for r, c in winning_line:
            self.buttons[(r, c)].config(bg="#a6e3a1", disabledforeground="#11111b")

    def reset_grid(self):
        """Clears all grid buttons for a fresh round."""
        for btn in self.buttons.values():
            btn.config(text=" ", bg="#313244", state="normal")


class TicTacToeApp(tk.Tk):
    """
    Main Tkinter Window application managing the scoreboard,
    the grid frame, and game settings.
    """

    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.geometry("400x560")
        self.configure(bg="#1e1e2e")

        # Initialize Game & Scores
        self.game = TicTacToe()
        self.scores = {"X": 0, "O": 0, "Ties": 0}

        # Game Mode: 'hard' (AI), 'easy' (AI), '2p' (Two Players)
        self.mode_var = tk.StringVar(value="hard")

        self._build_ui()

    def _build_ui(self):
        """Assembles title, scoreboard, grid, and control buttons."""
        # 1. Title Label
        title_lbl = tk.Label(
            self,
            text="TIC - TAC - TOE",
            font=("Helvetica", 18, "bold"),
            fg="#cba6f7",
            bg="#1e1e2e",
            pady=10,
        )
        title_lbl.pack()

        # 2. Scoreboard
        score_frame = tk.Frame(self, bg="#252538", pady=6)
        score_frame.pack(fill="x", padx=16, pady=4)
        score_frame.columnconfigure((0, 1, 2), weight=1)

        self.score_x_lbl = tk.Label(score_frame, text="X: 0", font=("Helvetica", 11, "bold"), fg="#f38ba8", bg="#252538")
        self.score_x_lbl.grid(row=0, column=0)

        self.score_tie_lbl = tk.Label(score_frame, text="Ties: 0", font=("Helvetica", 11, "bold"), fg="#a6adc8", bg="#252538")
        self.score_tie_lbl.grid(row=0, column=1)

        self.score_o_lbl = tk.Label(score_frame, text="O (AI): 0", font=("Helvetica", 11, "bold"), fg="#89b4fa", bg="#252538")
        self.score_o_lbl.grid(row=0, column=2)

        # 3. Status Banner
        self.status_lbl = tk.Label(
            self,
            text="Player X's Turn",
            font=("Helvetica", 12, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e",
            pady=6,
        )
        self.status_lbl.pack()

        # 4. Interactive Grid (Subclassed tk.Frame)
        self.grid_frame = TicTacToeGrid(self, self.game, self.handle_game_event)
        self.grid_frame.pack(padx=20, pady=10)

        # 5. Mode Selector & Reset Controls
        ctrl_frame = tk.Frame(self, bg="#1e1e2e", pady=8)
        ctrl_frame.pack(fill="x", padx=20)

        tk.Label(ctrl_frame, text="Opponent:", font=("Helvetica", 10), fg="#a6adc8", bg="#1e1e2e").pack(side="left")

        mode_menu = tk.OptionMenu(ctrl_frame, self.mode_var, "hard", "easy", "2p", command=lambda _: self.new_round())
        mode_menu.config(bg="#313244", fg="#cdd6f4", activebackground="#45475a", highlightthickness=0, bd=0)
        mode_menu.pack(side="left", padx=8)

        new_game_btn = tk.Button(
            ctrl_frame,
            text="New Round",
            font=("Helvetica", 10, "bold"),
            bg="#cba6f7",
            fg="#11111b",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.new_round,
        )
        new_game_btn.pack(side="right")

    def handle_game_event(self, event_type, data):
        """Processes player clicks and coordinates with game engine."""
        if event_type == "player_click":
            row, col = data
            if self.game.game_over:
                return

            # Prevent player clicking during AI turn in vs AI mode
            if self.mode_var.get() != "2p" and self.game.current_player == "O":
                return

            player = self.game.current_player
            if self.game.make_move(row, col):
                self.grid_frame.update_cell(row, col, player)
                self._check_game_status()

                # If game is still ongoing and opponent is AI, schedule AI move
                if not self.game.game_over and self.mode_var.get() != "2p":
                    self.after(300, self.handle_ai_turn)

    def handle_ai_turn(self):
        """Computes and executes the computer's move."""
        if self.game.game_over:
            return

        difficulty = self.mode_var.get()
        move = get_computer_move(self.game, difficulty=difficulty, ai_player="O")
        if move:
            row, col = move
            self.game.make_move(row, col)
            self.grid_frame.update_cell(row, col, "O")
            self._check_game_status()

    def _check_game_status(self):
        """Checks if there is a winner or tie and updates scoreboard."""
        if self.game.winner:
            self.status_lbl.config(text=f"Player {self.game.winner} Wins!", fg="#a6e3a1")
            self.grid_frame.highlight_winner(self.game.winning_line)
            self.scores[self.game.winner] += 1
            self._update_score_labels()
        elif self.game.is_draw():
            self.status_lbl.config(text="It's a Tie!", fg="#cba6f7")
            self.scores["Ties"] += 1
            self._update_score_labels()
        else:
            self.status_lbl.config(
                text=f"Player {self.game.current_player}'s Turn",
                fg="#f38ba8" if self.game.current_player == "X" else "#89b4fa",
            )

    def _update_score_labels(self):
        """Refreshes scoreboard text."""
        o_title = "O" if self.mode_var.get() == "2p" else "O (AI)"
        self.score_x_lbl.config(text=f"X: {self.scores['X']}")
        self.score_tie_lbl.config(text=f"Ties: {self.scores['Ties']}")
        self.score_o_lbl.config(text=f"{o_title}: {self.scores['O']}")

    def new_round(self):
        """Starts a new round without clearing overall scores."""
        self.game.reset()
        self.grid_frame.reset_grid()
        self.status_lbl.config(text="Player X's Turn", fg="#f38ba8")
        self._update_score_labels()


def run_gui():
    """Starts the Tkinter application."""
    app = TicTacToeApp()
    app.mainloop()
