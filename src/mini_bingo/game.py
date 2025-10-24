"""
Game orchestration for Mini Bingo.

This module wires together:
- Card generation (per player)
- Draw pool lifecycle
- Marking + bingo detection for all players after each draw
- Winner tracking (supports multiple winners on a single draw)

It exposes a lightweight, UI‑friendly API that higher layers (CLI/GUI) can call
without touching internals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Iterable, Tuple
import random

from .card import Card, generate_player_card, display_player_card
from .draw import DrawPool
from .rules import check_for_bingo, mark_number, winning_lines, WinLine, format_bingo_announcement


# --- Data models ---

@dataclass
class Player:
    pid: int
    name: str
    card: Card
    has_bingo: bool = False
    win_lines: List[WinLine] = field(default_factory=list)

    def mark(self, n: int) -> bool:
        return mark_number(self.card, n)

    def refresh_status(self) -> None:
        res = check_for_bingo(self.card)
        self.has_bingo = res.has_bingo
        self.win_lines = res.lines


# --- Helpers ---

def _split_seed(master_seed: Optional[int], count: int) -> List[Optional[int]]:
    """Derive `count` deterministic child seeds from an optional master seed.

    If master_seed is None, return a list of Nones (non‑deterministic children).
    """
    if master_seed is None:
        return [None] * count
    rng = random.Random(master_seed)
    return [rng.randrange(0, 2**31 - 1) for _ in range(count)]


# --- Game controller ---

class Game:
    """Mini Bingo game controller.

    Typical usage:
        game = Game(num_players=3, master_seed=123)
        info = game.draw_next()  # draw, mark, evaluate, winners if any
        if info["winners"]:
            ...
    """

    def __init__(
        self,
        num_players: int,
        player_names: Optional[List[str]] = None,
        master_seed: Optional[int] = None,
        draw_seed: Optional[int] = None,
        player_seeds: Optional[List[Optional[int]]] = None,
    ) -> None:
        if num_players <= 0:
            raise ValueError("num_players must be >= 1")

        # Seeds: either provided explicitly, or derived from a master
        if player_seeds is None:
            player_seeds = _split_seed(master_seed, num_players)
        if draw_seed is None:
            draw_seed = (random.Random(master_seed).randrange(0, 2**31 - 1)
                         if master_seed is not None else None)

        # Names
        if player_names is None:
            player_names = [f"Player {i+1}" for i in range(num_players)]
        if len(player_names) != num_players:
            raise ValueError("player_names length must match num_players")

        # Build players with deterministic cards
        self.players: List[Player] = []
        for i in range(num_players):
            card = generate_player_card(seed=player_seeds[i])
            self.players.append(Player(pid=i+1, name=player_names[i], card=card))

        # Draw pool
        self.pool = DrawPool(seed=draw_seed)
        self.called: List[int] = []  # history of called numbers
        self.finished = False
        self.winners: List[int] = []  # store PIDs of winners in order of win

    # --- Core loop ---
    def draw_next(self) -> Dict[str, Any]:
        """Draw the next number, mark every player's card, re‑evaluate winners.

        Returns a dict with:
            {
              'number': int,                 # the number drawn
              'marked': {pid: bool, ...},    # whether each player marked it
              'new_winners': [pid, ...],     # players who achieved bingo due to this draw
              'announcements': [str, ...],   # ready‑to‑speak strings
            }
        Raises IndexError if the draw pool is exhausted.
        """
        if self.finished:
            raise IndexError("Game already finished — draw pool exhausted or concluded.")

        n = self.pool.draw()
        self.called.append(n)

        marked: Dict[int, bool] = {}
        for p in self.players:
            marked[p.pid] = p.mark(n)

        # Update statuses and detect *new* winners caused by this number
        new_winners: List[int] = []
        for p in self.players:
            prev = p.has_bingo
            p.refresh_status()
            if p.has_bingo and not prev:
                new_winners.append(p.pid)
                self.winners.append(p.pid)

        if self.pool.empty:
            self.finished = True

        announcements: List[str] = []
        if new_winners:
            # Collect line details for those players
            for pid in new_winners:
                player = self.player_by_id(pid)
                announcements.append(
                    format_bingo_announcement([player.name], player.win_lines)
                )

        return {
            "number": n,
            "marked": marked,
            "new_winners": new_winners,
            "announcements": announcements,
        }

    # --- Queries ---
    def player_by_id(self, pid: int) -> Player:
        for p in self.players:
            if p.pid == pid:
                return p
        raise KeyError(f"No player with id {pid}")

    def snapshot(self) -> Dict[str, Any]:
        """Return a serializable snapshot of the whole game state for UI/storage."""
        return {
            "called": list(self.called),
            "pool_remaining": self.pool.remaining(),
            "finished": self.finished,
            "winners": list(self.winners),
            "players": [
                {
                    "pid": p.pid,
                    "name": p.name,
                    "has_bingo": p.has_bingo,
                    "win_lines": [(w.kind, w.index) for w in p.win_lines],
                    "card": p.card.grid,
                    "marked": p.card.marked,
                }
                for p in self.players
            ],
        }

    # --- Control ---
    def reset(self, *, new_master_seed: Optional[int] = None) -> None:
        """Soft reset for a new game with fresh cards and a fresh pool.

        If `new_master_seed` is given, derive fresh deterministic seeds; otherwise
        keep nondeterministic behavior.
        """
        n = len(self.players)
        seeds = _split_seed(new_master_seed, n) if new_master_seed is not None else [None] * n
        for i, p in enumerate(self.players):
            p.card = generate_player_card(seed=seeds[i])
            p.has_bingo = False
            p.win_lines.clear()
        draw_seed = (random.Random(new_master_seed).randrange(0, 2**31 - 1)
                     if new_master_seed is not None else None)
        self.pool.reset(seed=draw_seed)
        self.called.clear()
        self.finished = False
        self.winners.clear()

    # --- Pretty helpers ---
    def render_cards_text(self) -> str:
        """Return a human‑readable dump of all player cards (for CLI/debug)."""
        parts: List[str] = []
        for p in self.players:
            parts.append(f"=== {p.name} (P{p.pid}) ===")
            parts.append(display_player_card(p.card))
        return "\n\n".join(parts)


__all__ = ["Player", "Game"]
