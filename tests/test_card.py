import pytest

from mini_bingo.card import generate_player_card, is_valid_card, CENTER, COLUMN_RANGES, DEFAULT_SIZE


def test_generate_card_is_valid():
    card = generate_player_card(seed=1)
    assert is_valid_card(card)


def test_card_shape_and_center_marked():
    card = generate_player_card(seed=2)
    assert len(card.grid) == DEFAULT_SIZE
    assert all(len(row) == DEFAULT_SIZE for row in card.grid)
    r, c = CENTER
    assert card.grid[r][c] == 0
    assert card.marked[r][c] is True


def test_column_ranges_and_no_duplicates():
    card = generate_player_card(seed=3)
    # ranges (except the free center)
    for c, rng in enumerate(COLUMN_RANGES):
        for r in range(DEFAULT_SIZE):
            if (r, c) == CENTER:
                continue
            assert card.grid[r][c] in rng

    # no duplicates across the whole card (ignoring center)
    nums = [n for row in card.grid for n in row if n != 0]
    assert len(nums) == len(set(nums))
