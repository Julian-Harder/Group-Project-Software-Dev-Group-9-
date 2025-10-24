"""
Draw pool for Mini Bingo (75-ball).

Based on the backlog and sprint notes (Group 9): numbers must be drawn
randomly without repetition, history must be queryable, and behavior should be
reproducible with an optional seed. See project docs for acceptance criteria.

Public API (stable):
- DrawPool(seed: Optional[int] = None)
- draw() -> int                      # draw next random number (1..75) without repeat
- remaining() -> int                 # count of numbers left in the pool
- history() -> list[int]             # numbers drawn so far in draw order
- has_drawn(n: int) -> bool          # whether `n` has been drawn already
- reset(seed: Optional[int] = None)  # reset pool & history (seed may be changed)

Conveniences:
- __len__() == remaining()
- empty property
- peek() -> Optional[int]            # deterministic next number *without* consuming (best effort)

Implementation notes:
- Internally we maintain a list of the numbers that have *not* yet been drawn and
  pop from it using a Random instance seeded once at construction (or reset).
- peek() is implemented by looking at the next index that would be chosen by the
  RNG if we were to draw; to avoid corrupting state, we copy the RNG. This keeps
  determinism but is optional to use.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import random

ALL_NUMBERS = list(range(1, 76))  # 1..75 inclusive


@dataclass
class DrawPool:
    seed: Optional[int] = None
    _rng: random.Random = field(init=False, repr=False)
    _remaining: List[int] = field(init=False, repr=False)
    _history: List[int] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self._remaining = ALL_NUMBERS.copy()
        self._history = []

    # --- Core API ---
    def draw(self) -> int:
        """Draw and return a random number from the remaining pool.

        Raises
        ------
        IndexError
            If the pool is empty (all numbers already drawn).
        """
        if not self._remaining:
            raise IndexError("Draw pool exhausted")
        # Choose a random index uniformly from remaining numbers
        idx = self._rng.randrange(len(self._remaining))
        n = self._remaining.pop(idx)
        self._history.append(n)
        return n

    def remaining(self) -> int:
        return len(self._remaining)

    def history(self) -> List[int]:
        # Return a copy to protect internal state
        return list(self._history)

    def has_drawn(self, n: int) -> bool:
        return n in self._history

    def reset(self, seed: Optional[int] = None) -> None:
        """Reset the pool and (optionally) the seed.

        If a seed is provided, reseed; otherwise reuse the existing seed.
        """
        if seed is not None:
            self.seed = seed
        self._rng = random.Random(self.seed)
        self._remaining = ALL_NUMBERS.copy()
        self._history.clear()

    # --- Conveniences ---
    def __len__(self) -> int:  # len(pool) == remaining count
        return self.remaining()

    @property
    def empty(self) -> bool:
        return not self._remaining

    def peek(self) -> Optional[int]:
        """Non-consuming look at what *would* be drawn next, if draw() were called now.

        Returns None if the pool is empty. This duplicates the RNG temporarily to
        preserve determinism and internal state.
        """
        if not self._remaining:
            return None
        rng_copy = random.Random()
        rng_copy.setstate(self._rng.getstate())
        idx = rng_copy.randrange(len(self._remaining))
        return self._remaining[idx]


# Small self-test utility (manual):
if __name__ == "__main__":
    pool = DrawPool(seed=42)
    seen = set()
    while not pool.empty:
        n = pool.draw()
        assert n not in seen
        seen.add(n)
    assert len(seen) == 75
    print("OK: drew 75 unique numbers deterministically with seed=42")
