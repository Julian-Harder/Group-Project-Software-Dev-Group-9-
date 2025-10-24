"""
Random no‑repeat draw pool (1..75) — mid‑sprint slice.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import random

ALL_NUMBERS = list(range(1, 76))


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

    def draw(self) -> int:
        if not self._remaining:
            raise IndexError("Draw pool exhausted")
        idx = self._rng.randrange(len(self._remaining))
        n = self._remaining.pop(idx)
        self._history.append(n)
        return n

    def remaining(self) -> int:
        return len(self._remaining)

    def history(self) -> List[int]:
        return list(self._history)

    def has_drawn(self, n: int) -> bool:
        return n in self._history

    def reset(self, seed: Optional[int] = None) -> None:
        if seed is not None:
            self.seed = seed
        self._rng = random.Random(self.seed)
        self._remaining = ALL_NUMBERS.copy()
        self._history.clear()

    @property
    def empty(self) -> bool:
        return not self._remaining

    def peek(self) -> Optional[int]:
        if not self._remaining:
            return None
        rng_copy = random.Random()
        rng_copy.setstate(self._rng.getstate())
        idx = rng_copy.randrange(len(self._remaining))
        return self._remaining[idx]
