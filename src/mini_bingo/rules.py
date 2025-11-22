"""
Rules, marking, and bingo detection utilities.

Designed to satisfy the Group 9 acceptance criteria:
- Automatically mark numbers on cards as they are drawn.
- Detect Bingo when a full row, column, or diagonal is completed.
- Provide structured results (lines & indices) for UI announcements and
  multi‑winner scenarios.  
See Session 2 notes and backlog.  

Public API
----------
- mark_number(card: Card, n: int) -> bool
- check_for_bingo(card: Card) -> BingoResult
- winning_lines(card: Card) -> list[WinLine]
- format_bingo_announcement(players: list[int] | list[str], lines: list["WinLine"]) -> str

Implementation notes
--------------------
- We operate directly on the `Card` object from card.py which already maintains
  a boolean mask (`card.marked`). The center is free and pre‑marked by Card.
- Row/column/diagonal checks only look at `marked`.
- The module is side‑effect free and easy to unit test.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Tuple

from .card import Card, DEFAULT_SIZE, CENTER

LineKind = Literal["row", "col", "diag"]


@dataclass(frozen=True)
class WinLine:
    kind: LineKind  # "row", "col", or "diag"
    index: int      # row idx (0..4), col idx (0..4), or 0/1 for main/anti diagonal


@dataclass(frozen=True)
class BingoResult:
    has_bingo: bool
    lines: List[WinLine]


def mark_number(card: Card, n: int) -> bool:
    """Mark number `n` on the card if present.

    Returns True if the card contained the number and was marked; False otherwise.
    (Delegates to Card.mark_if_present.)
    """
    return card.mark_if_present(n)


def _row_complete(card: Card, r: int) -> bool:
    return all(card.marked[r][c] for c in range(DEFAULT_SIZE))


def _col_complete(card: Card, c: int) -> bool:
    return all(card.marked[r][c] for r in range(DEFAULT_SIZE))


def _diag_complete(card: Card, which: int) -> bool:
    """which=0 → main diagonal (top-left → bottom-right), which=1 → anti-diagonal."""
    if which == 0:
        return all(card.marked[i][i] for i in range(DEFAULT_SIZE))
    else:
        return all(card.marked[i][DEFAULT_SIZE - 1 - i] for i in range(DEFAULT_SIZE))


def winning_lines(card: Card) -> List[WinLine]:
    """Return all completed lines (rows/cols/diagonals) on this card.

    The free center (already marked by Card) contributes to the diagonals/row/col as expected.
    """
    wins: List[WinLine] = []

    # Rows
    for r in range(DEFAULT_SIZE):
        if _row_complete(card, r):
            wins.append(WinLine("row", r))

    # Columns
    for c in range(DEFAULT_SIZE):
        if _col_complete(card, c):
            wins.append(WinLine("col", c))

    # Diagonals
    if _diag_complete(card, 0):
        wins.append(WinLine("diag", 0))
    if _diag_complete(card, 1):
        wins.append(WinLine("diag", 1))

    return wins


def check_for_bingo(card: Card) -> BingoResult:
    """Check whether the card currently has any completed winning line(s).

    Returns a BingoResult with `has_bingo` and the list of WinLine entries.
    
    Acceptance criteria (Group 9): Bingo when a full row, column, or diagonal is
    completed; diagonals respect the free center. Multiple lines are supported and
    returned to the caller for announcement and scoring.  
    """
    lines = winning_lines(card)
    return BingoResult(has_bingo=bool(lines), lines=lines)


def format_bingo_announcement(players: List[int | str], lines: List[WinLine]) -> str:
    """Return a concise announcement string for the UI.

    Examples
    --------
    >>> format_bingo_announcement([1], [WinLine('row', 3)])
    'Player 1: BINGO! (row 4)'
    >>> format_bingo_announcement(["Alice", "Bob"], [WinLine('diag', 0)])
    'Players Alice, Bob: BINGO! (diag main)'
    """
    if not players:
        who = "Player"
    elif len(players) == 1:
        who = f"Player {players[0]}"
    else:
        who = "Players " + ", ".join(str(p) for p in players)

    # Map lines to friendly labels; we list unique kinds/indices for brevity
    def line_label(w: WinLine) -> str:
        if w.kind == "row":
            return f"row {w.index + 1}"
        if w.kind == "col":
            return f"col {w.index + 1}"
        # diag
        return "diag main" if w.index == 0 else "diag anti"

    # Unique labels while preserving order
    seen: set[Tuple[str, int]] = set()
    labels: List[str] = []
    for w in lines:
        key = (w.kind, w.index)
        if key not in seen:
            seen.add(key)
            labels.append(line_label(w))

    suffix = " (" + ", ".join(labels) + ")" if labels else ""
    return f"{who}: BINGO!{suffix}"


__all__ = [
    "BingoResult",
    "WinLine",
    "mark_number",
    "check_for_bingo",
    "winning_lines",
    "format_bingo_announcement",
]
