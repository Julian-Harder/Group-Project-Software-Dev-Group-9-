from mini_bingo.card import generate_player_card, is_valid_card, DEFAULT_SIZE, CENTER, COLUMN_RANGES


def test_card_is_valid():
    card = generate_player_card(seed=1)
    assert is_valid_card(card)


def test_center_is_free_and_marked():
    card = generate_player_card(seed=2)
    r, c = CENTER
    assert card.grid[r][c] == 0
    assert card.marked[r][c] is True


def test_column_ranges_and_no_duplicates():
    card = generate_player_card(seed=3)
    for c, rng in enumerate(COLUMN_RANGES):
        for r in range(DEFAULT_SIZE):
            if (r, c) == CENTER:
                continue
            assert card.grid[r][c] in rng
    nums = [n for row in card.grid for n in row if n != 0]
    assert len(nums) == len(set(nums))
