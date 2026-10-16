"""
=============================================================================
File: main.py
Description: Main Entry Point & Game Launcher.
What this file does:
  - Serves as the central starting point for the Tic-Tac-Toe application.
  - Organizes execution into clear, obvious, single-purpose functions:
      1. play_gui_game(): Starts the Tkinter graphical interface.
      2. play_cli_game(): Starts the terminal text-based interface.
      3. get_player_move(): Safely asks human player for row & column inputs.
      4. print_board(): Displays the 3x3 grid cleanly in the console.
      5. main(): Main coordinator asking how you want to play.
=============================================================================
"""

import sys
from engine import TicTacToe
from ai import get_computer_move
from gui import run_gui


def print_board(game):
    """
    Prints the 3x3 board cleanly in the terminal.
    Example:
       1   2   3
    1  X |   | O
      ---+---+---
    2    | X |  
      ---+---+---
    3  O |   | X
    """
    print("\n    1   2   3")
    for r in range(3):
        row_cells = [f" {game.board[r][c]} " for c in range(3)]
        print(f" {r + 1} " + "|".join(row_cells))
        if r < 2:
            print("   ---+---+---")
    print()


def get_player_move(game):
    """
    Safely prompts the player for row and column numbers.
    Prevents crashes if the user types letters or out-of-range numbers.
    """
    while True:
        try:
            user_input = input(f"Player {game.current_player}'s turn. Enter row and column (e.g. 1 2) or 'q' to quit: ").strip()
            if user_input.lower() in ("q", "quit"):
                print("Game exited.")
                sys.exit(0)

            parts = user_input.replace(",", " ").split()
            if len(parts) != 2:
                print("[!] Please enter two numbers separated by a space (e.g., 1 3).")
                continue

            row = int(parts[0]) - 1  # Convert 1-based input to 0-based index
            col = int(parts[1]) - 1

            if not game.is_valid_move(row, col):
                print("[!] That cell is invalid or already taken. Try again.")
                continue

            return row, col

        except ValueError:
            print("[!] Invalid input! Please enter integers (e.g., 2 1).")


def choose_cli_mode(cli_args=None):
    """
    Allows selecting game mode via arguments or an interactive menu.
    Modes:
      - 'hard': Unbeatable Minimax AI
      - 'easy': Random Computer AI
      - '2p':   Local Two-Player Pass & Play
    """
    if cli_args:
        for arg in cli_args:
            if arg in ("easy", "e", "2"):
                return "easy"
            if arg in ("2p", "two", "friend", "3"):
                return "2p"
            if arg in ("hard", "h", "1"):
                return "hard"

    # Interactive prompt in terminal
    print("\n" + "=" * 40)
    print("        SELECT GAME MODE")
    print("=" * 40)
    print("  [1] Hard (Unbeatable Minimax AI)")
    print("  [2] Easy (Random Computer Moves)")
    print("  [3] Two-Player (Play with a Friend)")
    print("=" * 40)

    while True:
        choice = input("Select mode (1, 2, or 3) [Default: 1]: ").strip().lower()
        if choice in ("1", "hard", "h", ""):
            return "hard"
        elif choice in ("2", "easy", "e"):
            return "easy"
        elif choice in ("3", "2p", "3p", "two", "p"):
            return "2p"
        else:
            print("[!] Please enter 1, 2, or 3.")


def play_cli_game(mode=None):
    """
    Runs a complete Tic-Tac-Toe match in the terminal.
    mode options:
      - 'hard' (Unbeatable Minimax AI)
      - 'easy' (Random AI)
      - '2p'   (Two Human Players)
    """
    if mode is None:
        mode = choose_cli_mode()

    game = TicTacToe()
    mode_names = {"hard": "HARD (MINIMAX)", "easy": "EASY (RANDOM)", "2p": "TWO PLAYERS"}
    print("\n" + "=" * 40)
    print(f"   TIC-TAC-TOE TERMINAL MODE: {mode_names.get(mode, mode.upper())}")
    print("=" * 40)
    print_board(game)

    while not game.game_over:
        # Check if it's the computer's turn in vs AI mode
        if mode != "2p" and game.current_player == "O":
            print("[AI] Computer is thinking...")
            row, col = get_computer_move(game, difficulty=mode, ai_player="O")
            print(f"[AI] Computer played at Row {row + 1}, Col {col + 1}")
        else:
            row, col = get_player_move(game)

        game.make_move(row, col)
        print_board(game)

    # Announce result
    if game.winner:
        winner_name = "Computer (O)" if (mode != "2p" and game.winner == "O") else f"Player {game.winner}"
        print(f"[Result] {winner_name} won the game!")
    else:
        print("[Result] The game is a TIE!")

    # Ask to play again
    while True:
        again = input("\nPlay another round? (y/n) [Default: y]: ").strip().lower()
        if again in ("n", "no", "q", "quit"):
            print("Thanks for playing! Goodbye.")
            break
        elif again in ("y", "yes", ""):
            # Offer to keep same mode or choose a new one
            change = input("Keep the same mode? (y/n) [Default: y]: ").strip().lower()
            next_mode = mode if change not in ("n", "no") else None
            play_cli_game(mode=next_mode)
            break
        else:
            print("[!] Please enter 'y' for yes or 'n' for no.")


def play_gui_game():
    """Launches the Tkinter Graphical User Interface."""
    print("Starting Tkinter Graphical Interface...")
    run_gui()


def main():
    """
    Main application function:
    Checks if the user wants to play in the terminal, otherwise launches the GUI window.
    Supports: --cli, cli, -c, terminal (even with accidental trailing dots like '--cli.').
    """
    # Clean arguments by stripping dashes, dots, and converting to lowercase
    user_args = [arg.strip("-./ ").lower() for arg in sys.argv[1:]]

    # If user typed 'cli', 'terminal', 'console', or '-c'
    if any(a in ("cli", "c", "terminal", "console", "t") for a in user_args):
        # Extract any difficulty specified as a flag (e.g. 'python main.py cli easy')
        remaining_args = [a for a in user_args if a not in ("cli", "c", "terminal", "console", "t")]
        selected_mode = choose_cli_mode(remaining_args) if not remaining_args else remaining_args[0]
        if selected_mode not in ("hard", "easy", "2p"):
            selected_mode = choose_cli_mode()
        play_cli_game(mode=selected_mode)
    else:
        # Default: Launch GUI window, with automatic fallback to CLI if no display is available
        try:
            play_gui_game()
        except Exception as e:
            print(f"[!] Unable to open GUI window: {e}")
            print("Starting Terminal CLI mode instead...")
            play_cli_game()


if __name__ == "__main__":
    main()
