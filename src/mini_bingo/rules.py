"""
Marking & bingo detection — mid‑sprint slice.

- mark_number(card, n): marks if present
- winning_lines(card): returns completed rows/cols/diagonals
- check_for_bingo(card): wrapper returning {has_bingo, lines}
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal

from .card import Card, DEFAULT_SIZE

LineKind = Literal["row", "col", "diag"]


@dataclass(frozen=True)
class WinLine:
    kind: LineKind  # "row", "col", or "diag"
    index: int      # row/col index (0..4) or diag index (0 main, 1 anti)


@dataclass(frozen=True)
class BingoResult:
    has_bingo: bool
    lines: List[WinLine]


def mark_number(card: Card, n: int) -> bool:
    return card.mark_if_present(n)


def _row_complete(card: Card, r: int) -> bool:
    return all(card.marked[r][c] for c in range(DEFAULT_SIZE))


def _col_complete(card: Card, c: int) -> bool:
    return all(card.marked[r][c] for r in range(DEFAULT_SIZE))


def _diag_complete(card: Card, which: int) -> bool:
    if which == 0:  # main
        return all(card.marked[i][i] for i in range(DEFAULT_SIZE))
    else:  # anti
        return all(card.marked[i][DEFAULT_SIZE - 1 - i] for i in range(DEFAULT_SIZE))


def winning_lines(card: Card) -> List[WinLine]:
    wins: List[WinLine] = []
    for r in range(DEFAULT_SIZE):
        if _row_complete(card, r):
            wins.append(WinLine("row", r))
    for c in range(DEFAULT_SIZE):
        if _col_complete(card, c):
            wins.append(WinLine("col", c))
    if _diag_complete(card, 0):
        wins.append(WinLine("diag", 0))
    if _diag_complete(card, 1):
        wins.append(WinLine("diag", 1))
    return wins


def check_for_bingo(card: Card) -> BingoResult:
    lines = winning_lines(card)
    return BingoResult(has_bingo=bool(lines), lines=lines)


__all__ = [
    "BingoResult",
    "WinLine",
    "mark_number",
    "winning_lines",
    "check_for_bingo",
]
