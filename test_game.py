"""
=============================================================================
File: test_game.py
Description: Unit Tests for Engine & AI.
What this file does:
  - Uses Python's built-in `unittest` module.
  - Verifies that winning rules (row, column, diagonal) work accurately.
  - Verifies that invalid moves and ties are handled correctly.
  - Runs simulated games to prove the Minimax AI never loses.
=============================================================================
"""

import unittest
from engine import TicTacToe
from ai import get_best_move, get_random_move


class TestTicTacToe(unittest.TestCase):
    """Tests the game rules and board states."""

    def setUp(self):
        self.game = TicTacToe()

    def test_initial_board(self):
        """Checks that a new game has an empty board and starts with X."""
        self.assertEqual(self.game.current_player, "X")
        self.assertEqual(len(self.game.get_empty_cells()), 9)
        self.assertFalse(self.game.game_over)

    def test_valid_move(self):
        """Checks placing a piece updates the cell and toggles player turn."""
        success = self.game.make_move(0, 0)
        self.assertTrue(success)
        self.assertEqual(self.game.board[0][0], "X")
        self.assertEqual(self.game.current_player, "O")

    def test_invalid_move_occupied(self):
        """Checks that placing on an already occupied cell is rejected."""
        self.game.make_move(0, 0)
        success = self.game.make_move(0, 0)
        self.assertFalse(success)

    def test_row_win(self):
        """Checks row win detection."""
        # X: (0,0), O: (1,0), X: (0,1), O: (1,1), X: (0,2)
        self.game.make_move(0, 0)
        self.game.make_move(1, 0)
        self.game.make_move(0, 1)
        self.game.make_move(1, 1)
        self.game.make_move(0, 2)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "X")

    def test_col_win(self):
        """Checks column win detection."""
        # X: (0,0), O: (0,1), X: (1,0), O: (1,1), X: (2,2), O: (2,1)
        self.game.make_move(0, 0)
        self.game.make_move(0, 1)
        self.game.make_move(1, 0)
        self.game.make_move(1, 1)
        self.game.make_move(2, 2)
        self.game.make_move(2, 1)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "O")

    def test_diagonal_win(self):
        """Checks diagonal win detection."""
        self.game.make_move(0, 0) # X
        self.game.make_move(0, 1) # O
        self.game.make_move(1, 1) # X
        self.game.make_move(0, 2) # O
        self.game.make_move(2, 2) # X
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "X")

    def test_draw(self):
        """Checks tie game detection."""
        # Board layout:
        # X | O | X
        # X | O | O
        # O | X | X
        moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,1), (2,0), (2,2)]
        for r, c in moves:
            self.game.make_move(r, c)
        self.assertTrue(self.game.game_over)
        self.assertTrue(self.game.is_draw())


class TestAI(unittest.TestCase):
    """Tests the AI decision-making algorithms."""

    def test_minimax_takes_immediate_win(self):
        """AI should take a winning move when one is available."""
        game = TicTacToe()
        game.make_move(0, 0) # X
        game.make_move(1, 0) # O
        game.make_move(2, 2) # X
        game.make_move(1, 1) # O
        game.make_move(0, 2) # X
        # O can win immediately by playing (1, 2)
        best_move = get_best_move(game, ai_player="O")
        self.assertEqual(best_move, (1, 2))

    def test_minimax_never_loses(self):
        """Simulates 10 matches: Minimax AI playing against Random moves must never lose."""
        for _ in range(10):
            game = TicTacToe()
            while not game.game_over:
                if game.current_player == "X":
                    r, c = get_random_move(game)
                else:
                    r, c = get_best_move(game, ai_player="O")
                game.make_move(r, c)

            # Minimax (O) must either win or draw; it must never lose to X
            self.assertIn(game.winner, ["O", None])


if __name__ == "__main__":
    unittest.main()
