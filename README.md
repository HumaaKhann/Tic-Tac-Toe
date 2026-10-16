# 🎮 Tic-Tac-Toe (Python with Tkinter GUI & Minimax AI)

A clean, object-oriented Tic-Tac-Toe project written in **pure Python** (using only the Python standard library).

This project enhances the basic console game into an intermediate-level application:
- **Tkinter GUI with OOP Subclassing**: Subclasses `tk.Frame` to build an interactive 3x3 button grid with real-time scorekeeping and winning line highlights.
- **Unbeatable Minimax AI**: Uses game-tree recursion so the computer always makes the optimal move.
- **Terminal CLI Mode**: Includes crash-proof input validation to prevent crashes from letters or blank spaces.
- **Clean Flat Architecture**: Simple 5-file structure 
- **Automated Tests**: Unit tests verifying winning rules, draws, and AI play.

---

## 📁 File Structure

Everything is organized cleanly in a single folder (no nested subfolders):

```
Tic-Tac-Toe/
├── engine.py       # Core game state, rules, move validation, win & draw checks
├── ai.py           # Computer player: Random moves (Easy) and Minimax algorithm (Hard)
├── gui.py          # Tkinter GUI (subclasses tk.Frame for the 3x3 grid)
├── test_game.py    # Unit tests testing game rules and AI moves
├── main.py         # Clear entry point with distinct, single-purpose functions
└── README.md       # Project guide and instructions
```

---

## 📄 What Each File Does

## What Each File Does

|     File       |      Purpose        |                                      What to Look For                                           |
|----------------|---------------------|-------------------------------------------------------------------------------------------------|
| `engine.py`    | Core Game Engine    | Manages the 3x3 board, player turns, move validation, and win detection.                        |
| `ai.py`        | Computer Opponent   | Implements random moves and the Minimax algorithm to select the best move.                      |
| `gui.py`       | Graphical Interface | Creates interactive buttons, highlights winning lines, and schedules AI turns using `.after()`. |
| `main.py`      | Main Entry Point    | Provides functions to print the board, get player moves, and run CLI or GUI games.              |
| `test_game.py` | Automated Tests     | Tests wins, draws, invalid moves, and AI gameplay using Python's `unittest` framework.          |

---

## 🚀 How to Run

### 1. Run the Graphical User Interface (Default)
Double-click or run:
```powershell
python main.py
```
- Play as **X** vs **O (AI)** or switch to **Two-Player** mode.
- Change AI difficulty between **Hard (Minimax)** and **Easy (Random)**.
- Winning cells automatically turn **green**.

---

### 2. Run in Terminal / Command Prompt Mode
If you want to play inside your terminal:
```powershell
python main.py cli
```
This presents an interactive menu to choose your game mode:
- **[1] Hard**: Unbeatable Minimax AI
- **[2] Easy**: Random Computer Moves
- **[3] Two-Player**: Local Pass & Play with a friend

You can also specify the mode directly in your command:
```powershell
python main.py cli easy    # Play vs Easy AI directly
python main.py cli 2p      # Play Two-Player directly
python main.py cli hard    # Play vs Hard AI directly
```

---

### 3. Run the Unit Tests
To verify all rules and AI calculations:
```powershell
python test_game.py
```
