# Mini Bingo – Mid‑Sprint Snapshot

Core logic is playable in scripts/tests; orchestration & CLI are pending.

## What works

* **Card generation** (5×5, FREE center, no duplicates) — `mini_bingo/card.py`
* **Draw pool** (1..75, no repeats, seedable, peek) — `mini_bingo/draw.py`
* **Rules** (marking + row/col/diagonal detection) — `mini_bingo/rules.py`

## Try it in a quick script

```python
from mini_bingo.card import generate_player_card
from mini_bingo.draw import DrawPool
from mini_bingo.rules import mark_number, check_for_bingo

card = generate_player_card(seed=7)
pool = DrawPool(seed=7)
print(card.display())

while not pool.empty:
    n = pool.draw()
    if mark_number(card, n):
        res = check_for_bingo(card)
        if res.has_bingo:
            print("BINGO!", [(w.kind, w.index) for w in res.lines])
            break
```

## Tests

Run the subset that exists so far:

```bash
pytest mid-sprint/tests -q
```

## Next up

* Game orchestration (multi‑player, announcements, snapshots)
* CLI (`python -m mini_bingo`) and packaging
* End‑to‑end tests and docs polish
