# ============================================================
# How to Run the Bingo Game in Your Terminal
# ============================================================

# ------------------------------------------------------------
# 1. Prerequisites
# ------------------------------------------------------------
# - Python 3 installed (check with:)
#     python --version      # or: python3 --version
# - Git installed
#
# On Windows, you may need to use `py` instead of `python`
# and run the commands in PowerShell instead of bash.
# ------------------------------------------------------------

# ------------------------------------------------------------
# 2. Clone the repository
# ------------------------------------------------------------

# Replace <REPO_URL> with the actual GitHub URL of this project.
git clone https://github.com/Julian-Harder/Group-Project-Software-Dev-Group-9-
cd Group-Project-Software-Dev-Group-9-

# ------------------------------------------------------------
# 3. Create and activate a virtual environment
# ------------------------------------------------------------

# --- macOS / Linux ---
python -m venv .venv
# Activate the virtual environment:
source .venv/bin/activate

# --- Windows (PowerShell) equivalent ---
# py -m venv .venv
# .\.venv\Scripts\Activate.ps1

# ------------------------------------------------------------
# 4. Install the project
# ------------------------------------------------------------

# From the project root:
python -m pip install --upgrade pip
python -m pip install -e .

# This installs the `mini_bingo` package from the src/ directory in editable mode.

# ------------------------------------------------------------
# 5. Run the tests
# ------------------------------------------------------------

python -m pip install pytest
python -m pytest

# All tests should pass. If they do, the core logic of the game is working correctly.

# ------------------------------------------------------------
# 6. Start the game
# ------------------------------------------------------------

# Run the game module:
python -m mini_bingo

# This launches the interactive game with default settings (1 player, random seed).

# ------------------------------------------------------------
# 7. Command-line options
# ------------------------------------------------------------
# You can customize the game with the following options:
#   -p N, --players N        number of players
#   --seed N                 master seed for reproducible games
#   --names NAME1 NAME2 ...  names for each player (must match number of players)
#   --auto                   automatically draw numbers until the first bingo
#                            (or all numbers are drawn), then exit

# --- Examples ---

# 3 players, fixed seed:
python -m mini_bingo --players 3 --seed 42

# 2 named players, auto-draw until first winner:
python -m mini_bingo --players 2 --names Alice Bob --auto

# Show help:
python -m mini_bingo --help

# ------------------------------------------------------------
# 8. In-game controls (interactive mode)
# ------------------------------------------------------------
# When you run without --auto, you enter an interactive menu.
# The main commands are:
#   D  - draw the next number
#   P  - peek at the next number (without drawing it)
#   S  - show current status (called numbers, winners, remaining numbers)
#   C  - show all player cards
#   A  - auto-draw until the first bingo (or no numbers left)
#   Q  - quit the game
#
# Follow the prompts shown in the terminal to control the game.
# ------------------------------------------------------------
