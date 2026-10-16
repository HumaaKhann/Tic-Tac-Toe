"""
=============================================================================
File: ai.py
Description: Computer Opponent (AI) Logic.
What this file does:
  - Provides computer moves for Single Player mode.
  - Easy Difficulty: Chooses a random available cell.
  - Hard Difficulty (Minimax): Uses game theory to evaluate future moves,
    making the computer unbeatable.
=============================================================================
"""

import random

def get_random_move(game):
    """Picks any random empty cell on the board."""
    empty_cells = game.get_empty_cells()
    if not empty_cells:
        return None
    return random.choice(empty_cells)


def get_best_move(game, ai_player="O"):
    """
    Finds the optimal move for the AI using the Minimax algorithm.
    Returns (row, col) coordinates of the best move.
    """
    human_player = "X" if ai_player == "O" else "O"
    empty_cells = game.get_empty_cells()

    # Optimization: If the board is completely empty, take the center cell
    if len(empty_cells) == 9:
        return (1, 1)

    best_score = float("-inf")
    best_move = None

    for row, col in empty_cells:
        # Simulate the move
        game.board[row][col] = ai_player
        # Call minimax for the human's response (minimizing turn)
        score = _minimax(game, depth=0, is_maximizing=False, ai_player=ai_player, human_player=human_player)
        # Undo the simulated move
        game.board[row][col] = " "

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move


def _minimax(game, depth, is_maximizing, ai_player, human_player):
    """
    Recursive Minimax function:
    - Gives a positive score (+10 - depth) if the AI wins.
    - Gives a negative score (-10 + depth) if the Human wins.
    - Gives 0 for a tie.
    """
    # 1. Terminal Base Cases
    if game.check_winner(ai_player):
        return 10 - depth
    if game.check_winner(human_player):
        return depth - 10
    if len(game.get_empty_cells()) == 0:
        return 0

    empty_cells = game.get_empty_cells()

    # 2. Maximizing turn (AI's turn)
    if is_maximizing:
        max_score = float("-inf")
        for row, col in empty_cells:
            game.board[row][col] = ai_player
            score = _minimax(game, depth + 1, False, ai_player, human_player)
            game.board[row][col] = " "
            max_score = max(max_score, score)
        return max_score

    # 3. Minimizing turn (Human's turn)
    else:
        min_score = float("inf")
        for row, col in empty_cells:
            game.board[row][col] = human_player
            score = _minimax(game, depth + 1, True, ai_player, human_player)
            game.board[row][col] = " "
            min_score = min(min_score, score)
        return min_score


def get_computer_move(game, difficulty="hard", ai_player="O"):
    """
    Helper function to get a move based on selected difficulty.
    Difficulty options: 'easy', 'hard'.
    """
    if difficulty == "easy":
        return get_random_move(game)
    return get_best_move(game, ai_player=ai_player)
