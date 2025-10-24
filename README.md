# Group-Project-Software-Dev-Group-9-
Group 9

A compact 75‑ball Bingo game with a clean core engine and a friendly CLI. Built to match the project expectations and structure you provided.

## Features

* 5×5 classic B‑I‑N‑G‑O card generation with free center.
* Deterministic seeding for reproducible runs (great for demos/tests).
* Random draw pool with no repeats and a queryable history.
* Auto‑marking + row/column/diagonal bingo detection.
* Multi‑winner support with ready‑to‑use announcement strings.

---

## Install & Run

### Local (editable)

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### Play via module entry

```bash
python -m mini_bingo --players 3 --seed 123 --names Alice Bob Carol
```

### Or use the console script (after install)

```bash
mini-bingo -p 2 --auto
```

---

## CLI Controls

```
[D]raw  [P]eek  [S]tatus  [C]ards  [A]uto  [Q]uit
```

* **Draw**: call the next number, mark all cards, announce winners.
* **Peek**: preview the next number (deterministic, non‑consuming).
* **Status**: show called numbers, remaining pool, winners so far.
* **Cards**: print all player cards in a readable grid.
* **Auto**: keep drawing until first win or pool exhaustion.

---

## Public API (for integrations)

```python
from mini_bingo import Game, DrawPool, Card, generate_player_card

# Game orchestration
game = Game(num_players=3, player_names=["A","B","C"], master_seed=42)
info = game.draw_next()  # { 'number': int, 'marked': {pid: bool}, 'new_winners': [...], 'announcements': [...] }
state = game.snapshot()   # serializable dict for UI/state saving

# Card utilities
card = generate_player_card(seed=7)
print(card.display())

# Draw pool (low‑level)
pool = DrawPool(seed=99)
```

---

## Project Layout

```
mini-bingo/
├─ pyproject.toml
├─ README.md
└─ src/
   ├─ main.py                 # simple CLI runner (outside package)
   └─ mini_bingo/
      ├─ __init__.py          # public API
      ├─ __main__.py          # `python -m mini_bingo`
      ├─ card.py              # card model + generator + validation
      ├─ draw.py              # no‑repeat draw pool, seedable
      ├─ rules.py             # marking & bingo detection
      └─ game.py              # game controller orchestrating everything
```

---

## Seeding / Reproducibility

* Pass `master_seed` to `Game(...)` for a fully reproducible session.
* Internally, the game derives per‑player card seeds and a draw‑pool seed from the master seed.
* Use explicit `player_seeds`/`draw_seed` if you want custom deterministic splits.

---

## Testing

After installing dev deps (pytest), run:

```bash
pytest
```

Suggested tests (to be added):

* `test_card.py`: shape, ranges, uniqueness, free center marked.
* `test_draw.py`: 75 unique draws, deterministic order with seed.
* `test_rules.py`: mark/line detection (rows, cols, diagonals).
* `test_game_flow.py`: winners appear and are announced.

---

## Notes

* The engine is side‑effect free and suitable for other UIs (web, GUI) to build on.
* All modules are small and unit‑test friendly.

## License

MIT
