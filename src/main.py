"""
Mini Bingo - CLI runner

A small interactive command‑line app that wires the Game controller to a
terminal UI. This is intentionally simple so it works in any environment.

Usage examples
--------------
$ python -m mini_bingo            # package entry, or: python src/main.py
$ python src/main.py --players 3 --seed 123 --names Alice Bob Carol
$ python src/main.py -p 2 --auto

Controls (interactive)
---------------------
[D]raw, [P]eek, [S]tatus, show [C]ards, [A]uto-draw to first win, [Q]uit

Design notes
------------
- Uses Game(master_seed=...) to derive deterministic player/draw seeds.
- Prints winner announcements immediately when they occur.
- Supports an --auto mode to draw until the first bingo (or exhaustion).
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from mini_bingo.game import Game


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="mini-bingo", description="Play Mini Bingo in the terminal")
    parser.add_argument("--players", "-p", type=int, default=1, help="Number of players (default: 1)")
    parser.add_argument("--seed", type=int, default=None, help="Master seed for reproducible games")
    parser.add_argument("--names", nargs="*", help="Optional list of player names (space‑separated)")
    parser.add_argument("--auto", action="store_true", help="Auto‑draw until the first bingo or exhaustion")
    return parser.parse_args(argv)


def print_header(game: Game) -> None:
    print("=" * 60)
    print("MINI BINGO — Terminal Edition")
    print("Players:")
    for p in game.players:
        print(f"  P{p.pid}: {p.name}")
    print("=" * 60)


def show_status(game: Game) -> None:
    snap = game.snapshot()
    called = ", ".join(str(n) for n in snap["called"]) or "(none)"
    print(f"Numbers called ({len(snap['called'])}): {called}")
    print(f"Remaining in pool: {snap['pool_remaining']}")
    if snap["winners"]:
        print("Winners so far:")
        for pid in snap["winners"]:
            p = game.player_by_id(pid)
            lines = ", ".join(f"{k}:{i+1}" if k != 'diag' else ("diag main" if i == 0 else "diag anti")
                                for (k, i) in [(w.kind, w.index) for w in p.win_lines])
            print(f"  {p.name} (P{p.pid}) — {lines}")
    else:
        print("No winners yet.")


def show_cards(game: Game) -> None:
    print(game.render_cards_text())


def step_draw(game: Game) -> bool:
    """Draw one number and handle announcements. Returns True if game continues."""
    try:
        info = game.draw_next()
    except IndexError as e:
        print("\nDraw pool exhausted — game over.")
        return False

    n = info["number"]
    print(f"\nNumber drawn: {n}")

    # Who marked it
    marked_players = [game.player_by_id(pid).name for pid, did in info["marked"].items() if did]
    if marked_players:
        print("Marked by:", ", ".join(marked_players))
    else:
        print("No player had it.")

    # Announcements
    for msg in info["announcements"]:
        print("\n" + "!" * 8)
        print(msg)
        print("!" * 8)

    return not game.finished


def auto_until_first_win(game: Game) -> None:
    while True:
        cont = step_draw(game)
        if not cont:
            break
        if game.winners:
            break
    print()
    show_status(game)


def repl(game: Game) -> None:
    print_header(game)
    show_status(game)
    show_cards(game)

    while True:
        print("\n[D]raw  [P]eek  [S]tatus  [C]ards  [A]uto  [Q]uit")
        choice = input("> ").strip().lower()
        if choice in ("d", "draw"):
            if not step_draw(game):
                break
        elif choice in ("p", "peek"):
            nxt = game.pool.peek()
            print(f"Next up (peek): {nxt if nxt is not None else '(pool empty)'}")
        elif choice in ("s", "status"):
            show_status(game)
        elif choice in ("c", "cards"):
            show_cards(game)
        elif choice in ("a", "auto"):
            auto_until_first_win(game)
        elif choice in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        else:
            print("Unknown command — try D/P/S/C/A/Q")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    names = args.names if args.names else None

    game = Game(num_players=args.players, player_names=names, master_seed=args.seed)

    if args.auto:
        print_header(game)
        auto_until_first_win(game)
        return 0

    repl(game)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


