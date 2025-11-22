"""
Card model and generator for Mini Bingo (75-ball, 5x5).

Responsibilities
- Define the `Card` dataclass that holds the number grid and a parallel
  boolean mask for marked cells.
- Generate a valid player card using classic B I N G O column ranges with a
  free center.
- Validation helpers for duplicates and structure.
- Simple text display helper for terminal UI.

This module is intentionally self‑contained and has no side effects so it can
be unit tested in isolation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence
import random

# Classic 75-ball bingo column ranges
# B: 1–15, I: 16–30, N: 31–45 (center is free), G: 46–60, O: 61–75
COLUMN_RANGES: List[range] = [
    range(1, 16),   # B
    range(16, 31),  # I
    range(31, 46),  # N
    range(46, 61),  # G
    range(61, 76),  # O
]

DEFAULT_SIZE = 5
CENTER = (2, 2)  # (row, col) for 0-indexed center


@dataclass
class Card:
    """A single bingo card.

    Attributes
    -----------
    grid: 5x5 list of lists containing ints; the center is set to 0 to denote
          a free space (never drawn). Keeping it numeric simplifies display.
    marked: 5x5 list of lists of booleans indicating whether a cell is marked.
    seed: Optional seed used when generating this card (for reproducibility in tests).
    """

    grid: List[List[int]]
    marked: List[List[bool]] = field(default_factory=lambda: [[False]*DEFAULT_SIZE for _ in range(DEFAULT_SIZE)])
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        # Ensure 5x5 structure
        if len(self.grid) != DEFAULT_SIZE or any(len(row) != DEFAULT_SIZE for row in self.grid):
            raise ValueError("Card.grid must be a 5x5 matrix")
        # Center free space is always marked
        r, c = CENTER
        self.marked[r][c] = True

    def copy(self) -> "Card":
        return Card([row[:] for row in self.grid], [row[:] for row in self.marked], self.seed)

    def numbers(self) -> List[int]:
        """Return all non-zero numbers on the card as a flat list. (Center is 0.)"""
        return [n for row in self.grid for n in row if n != 0]

    def position_of(self, number: int) -> Optional[tuple[int, int]]:
        """Return (row, col) if number is on the card, else None."""
        for r, row in enumerate(self.grid):
            for c, n in enumerate(row):
                if n == number:
                    return r, c
        return None

    def mark_if_present(self, number: int) -> bool:
        """Mark the cell if the number is present. Returns True if a mark occurred."""
        pos = self.position_of(number)
        if pos is None:
            return False
        r, c = pos
        self.marked[r][c] = True
        return True

    def display(self) -> str:
        """Return a formatted string representation for terminal output.

        Marked cells are wrapped with brackets like `[ 7]` while unmarked cells
        use spaces: `  7 `; the free center shows as `FREE`.
        """
        headers = " B   I   N   G   O"
        lines = [headers]
        for r in range(DEFAULT_SIZE):
            parts: List[str] = []
            for c in range(DEFAULT_SIZE):
                n = self.grid[r][c]
                if r == CENTER[0] and c == CENTER[1]:
                    cell = "FREE"
                else:
                    cell = f"{n:>2d}"
                if self.marked[r][c]:
                    parts.append(f"[{cell:>3}]")
                else:
                    parts.append(f" {cell:>3} ")
            lines.append(" ".join(parts))
        return "\n".join(lines)


def _choose_unique(sample_range: Sequence[int], k: int, rng: random.Random) -> List[int]:
    """Utility: choose k unique numbers from a range using provided RNG."""
    if k > len(sample_range):
        raise ValueError("k cannot exceed the size of sample_range")
    return rng.sample(list(sample_range), k)


def generate_player_card(seed: Optional[int] = None) -> Card:
    """Generate a valid 5x5 bingo card with classic column ranges and a free center.

    The center (row=2, col=2) is set to 0 and pre-marked.
    If `seed` is provided, card generation is reproducible.
    """
    rng = random.Random(seed)

    columns: List[List[int]] = []
    for col_idx, col_range in enumerate(COLUMN_RANGES):
        # The N column has a free center, so select only 4 numbers for that column.
        need = 4 if col_idx == 2 else 5
        nums = sorted(_choose_unique(col_range, need, rng))
        columns.append(nums)

    # Build grid row-wise from column lists; insert the free center in N column
    grid: List[List[int]] = [[0 for _ in range(DEFAULT_SIZE)] for _ in range(DEFAULT_SIZE)]

    for r in range(DEFAULT_SIZE):
        for c in range(DEFAULT_SIZE):
            if (r, c) == CENTER:
                grid[r][c] = 0  # free
                continue
            # Determine the index within its column list (skip center for N)
            if c == 2 and r >= 2:
                # rows 2..4 in N column pull from indices 1..3 because index 2 is the free cell
                src_index = r - 1
            else:
                src_index = r
            grid[r][c] = columns[c][src_index]

    marked = [[False] * DEFAULT_SIZE for _ in range(DEFAULT_SIZE)]
    r, c = CENTER
    marked[r][c] = True
    card = Card(grid=grid, marked=marked, seed=seed)

    # Final sanity checks
    if not is_valid_card(card):
        raise AssertionError("Generated card failed validation")

    return card


def check_for_duplicates(card: Card) -> bool:
    """Return True if duplicates exist in the card numbers (excluding the free center).

    This is primarily a helper for tests.
    """
    nums = card.numbers()
    return len(nums) != len(set(nums))


def is_valid_card(card: Card) -> bool:
    """Validate size, ranges, and absence of duplicates for a 5x5 classic card."""
    # 5x5 shape
    if len(card.grid) != DEFAULT_SIZE or any(len(row) != DEFAULT_SIZE for row in card.grid):
        return False

    # Column ranges, excluding center
    for c, col_range in enumerate(COLUMN_RANGES):
        for r in range(DEFAULT_SIZE):
            if (r, c) == CENTER:
                continue
            n = card.grid[r][c]
            if n == 0:  # only allowed at center
                return False
            if n not in col_range:
                return False

    # No duplicates
    if check_for_duplicates(card):
        return False

    # Center must be 0 and marked
    if card.grid[CENTER[0]][CENTER[1]] != 0:
        return False
    if not card.marked[CENTER[0]][CENTER[1]]:
        return False

    return True


# Convenience function names expected by other modules / tests

def display_player_card(card: Card) -> str:
    """Public helper that forwards to Card.display()."""
    return card.display()
