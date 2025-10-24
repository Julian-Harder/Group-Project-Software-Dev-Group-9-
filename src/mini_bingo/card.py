"""
Card model and generator for Mini Bingo (75-ball, 5x5) — mid‑sprint core.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence
import random

# Column ranges: B(1–15) I(16–30) N(31–45) G(46–60) O(61–75)
COLUMN_RANGES: List[range] = [
    range(1, 16),
    range(16, 31),
    range(31, 46),
    range(46, 61),
    range(61, 76),
]

DEFAULT_SIZE = 5
CENTER = (2, 2)


@dataclass
class Card:
    grid: List[List[int]]
    marked: List[List[bool]] = field(default_factory=lambda: [[False]*DEFAULT_SIZE for _ in range(DEFAULT_SIZE)])
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        if len(self.grid) != DEFAULT_SIZE or any(len(r) != DEFAULT_SIZE for r in self.grid):
            raise ValueError("Card.grid must be 5x5")
        # pre‑mark free center
        r, c = CENTER
        self.marked[r][c] = True

    def numbers(self) -> List[int]:
        return [n for row in self.grid for n in row if n != 0]

    def position_of(self, number: int):
        for r, row in enumerate(self.grid):
            for c, n in enumerate(row):
                if n == number:
                    return r, c
        return None

    def mark_if_present(self, number: int) -> bool:
        pos = self.position_of(number)
        if pos is None:
            return False
        r, c = pos
        self.marked[r][c] = True
        return True

    def display(self) -> str:
        headers = " B   I   N   G   O"
        lines = [headers]
        for r in range(DEFAULT_SIZE):
            parts: List[str] = []
            for c in range(DEFAULT_SIZE):
                n = self.grid[r][c]
                cell = "FREE" if (r, c) == CENTER else f"{n:>2d}"
                parts.append(f"[{cell:>3}]" if self.marked[r][c] else f" {cell:>3} ")
            lines.append(" ".join(parts))
        return "\n".join(lines)


def _choose_unique(sample_range: Sequence[int], k: int, rng: random.Random) -> List[int]:
    return rng.sample(list(sample_range), k)


def generate_player_card(seed: Optional[int] = None) -> Card:
    rng = random.Random(seed)
    columns: List[List[int]] = []
    for col_idx, col_range in enumerate(COLUMN_RANGES):
        need = 4 if col_idx == 2 else 5  # N column has free center
        nums = sorted(_choose_unique(col_range, need, rng))
        columns.append(nums)

    grid: List[List[int]] = [[0 for _ in range(DEFAULT_SIZE)] for _ in range(DEFAULT_SIZE)]
    for r in range(DEFAULT_SIZE):
        for c in range(DEFAULT_SIZE):
            if (r, c) == CENTER:
                grid[r][c] = 0
                continue
            src_index = (r - 1) if (c == 2 and r >= 2) else r
            grid[r][c] = columns[c][src_index]

    marked = [[False]*DEFAULT_SIZE for _ in range(DEFAULT_SIZE)]
    marked[CENTER[0]][CENTER[1]] = True
    return Card(grid=grid, marked=marked, seed=seed)


def is_valid_card(card: Card) -> bool:
    # 5x5 shape
    if len(card.grid) != DEFAULT_SIZE or any(len(row) != DEFAULT_SIZE for row in card.grid):
        return False
    # Column ranges (except center)
    for c, col_range in enumerate(COLUMN_RANGES):
        for r in range(DEFAULT_SIZE):
            if (r, c) == CENTER:
                continue
            n = card.grid[r][c]
            if n == 0 or n not in col_range:
                return False
    # No duplicates ignoring center
    nums = card.numbers()
    if len(nums) != len(set(nums)):
        return False
    # Center check
    if card.grid[CENTER[0]][CENTER[1]] != 0 or not card.marked[CENTER[0]][CENTER[1]]:
        return False
    return True


def display_player_card(card: Card) -> str:
    return card.display()
