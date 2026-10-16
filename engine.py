"""
=============================================================================
File: engine.py
Description: Core Tic-Tac-Toe Game Logic.
What this file does:
  - Stores the 3x3 board state.
  - Manages player turns ('X' and 'O').
  - Validates moves (checks bounds and prevents overwriting occupied cells).
  - Checks for winning lines (rows, columns, diagonals) and ties.
  - Completely independent of the user interface (used by both GUI and CLI).
=============================================================================
"""


class TicTacToe:
    """
    Manages the state and rules for a standard 3x3 Tic-Tac-Toe game.
    """

    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.winning_line = None  # Stores the 3 coordinates of a winning line
        self.game_over = False

    def reset(self):
        """Resets the game state back to an empty board."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.winning_line = None
        self.game_over = False

    def get_empty_cells(self):
        """Returns a list of (row, col) coordinates that are still empty."""
        empty_cells = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    empty_cells.append((r, c))
        return empty_cells

    def is_valid_move(self, row, col):
        """Checks if a move is within bounds and the cell is empty."""
        if 0 <= row < 3 and 0 <= col < 3:
            return self.board[row][col] == " "
        return False

    def make_move(self, row, col):
        """
        Attempts to place the current player's mark at (row, col).
        Returns True if the move was successful, False if invalid.
        """
        if self.game_over or not self.is_valid_move(row, col):
            return False

        # Place the mark
        self.board[row][col] = self.current_player

        # Check if this move won the game
        if self.check_winner(self.current_player):
            self.winner = self.current_player
            self.game_over = True
        # Check if the board is full (tie)
        elif len(self.get_empty_cells()) == 0:
            self.game_over = True
        else:
            # Switch to the other player's turn
            self.current_player = "O" if self.current_player == "X" else "X"

        return True

    def check_winner(self, player):
        """
        Checks if the given player ('X' or 'O') has won.
        If a win is found, records the winning line coordinates and returns True.
        """
        # All 8 possible winning lines in a 3x3 grid
        lines = [
            # 3 Rows
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # 3 Columns
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # 2 Diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        for line in lines:
            if all(self.board[r][c] == player for r, c in line):
                self.winning_line = line
                return True

        return False

    def is_draw(self):
        """Returns True if the game is over and there is no winner."""
        return self.game_over and self.winner is None
