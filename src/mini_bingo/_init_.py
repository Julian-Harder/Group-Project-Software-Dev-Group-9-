"""Mini Bingo – mid‑sprint public API.

Expose just the core pieces that already exist (card, draw, rules).
Game orchestration and CLI will be added in a later sprint.
"""
from .card import (
    Card,
    generate_player_card,
    display_player_card,
    is_valid_card,
    DEFAULT_SIZE,
    CENTER,
    COLUMN_RANGES,
)
from .draw import DrawPool
from .rules import BingoResult, WinLine, mark_number, winning_lines, check_for_bingo

__all__ = [
    # card
    "Card",
    "generate_player_card",
    "display_player_card",
    "is_valid_card",
    "DEFAULT_SIZE",
    "CENTER",
    "COLUMN_RANGES",
    # draw
    "DrawPool",
    # rules
    "BingoResult",
    "WinLine",
    "mark_number",
    "winning_lines",
    "check_for_bingo",
]

__version__ = "0.0.1-dev"
