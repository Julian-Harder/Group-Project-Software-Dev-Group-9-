"""Mini Bingo package.

Exports the primary public API for use by UIs and tests.
"""
from .card import Card, generate_player_card, display_player_card, is_valid_card
from .draw import DrawPool
from .rules import (
    BingoResult,
    WinLine,
    mark_number,
    winning_lines,
    check_for_bingo,
    format_bingo_announcement,
)
from .game import Game, Player

__all__ = [
    # card
    "Card",
    "generate_player_card",
    "display_player_card",
    "is_valid_card",
    # draw
    "DrawPool",
    # rules
    "BingoResult",
    "WinLine",
    "mark_number",
    "winning_lines",
    "check_for_bingo",
    "format_bingo_announcement",
    # game
    "Game",
    "Player",
]

__version__ = "0.1.0"
