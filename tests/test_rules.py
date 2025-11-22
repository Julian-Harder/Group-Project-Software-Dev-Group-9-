from mini_bingo.card import Card, DEFAULT_SIZE, CENTER
from mini_bingo.rules import mark_number, winning_lines, check_for_bingo, WinLine


def make_empty_marked():
    # Build a card with arbitrary numbers; we only manipulate the marked mask.
    grid = [[(r * DEFAULT_SIZE + c + 1) for c in range(DEFAULT_SIZE)] for r in range(DEFAULT_SIZE)]
    r0, c0 = CENTER
    grid[r0][c0] = 0
    card = Card(grid=grid)
    # ensure only center is marked at start
    for r in range(DEFAULT_SIZE):
        for c in range(DEFAULT_SIZE):
            card.marked[r][c] = (r, c) == CENTER
    return card


def test_row_win():
    card = make_empty_marked()
    r = 1
    for c in range(DEFAULT_SIZE):
        card.marked[r][c] = True
    wins = winning_lines(card)
    assert WinLine("row", r) in wins
    assert check_for_bingo(card).has_bingo is True


def test_col_win():
    card = make_empty_marked()
    c = 3
    for r in range(DEFAULT_SIZE):
        card.marked[r][c] = True
    wins = winning_lines(card)
    assert WinLine("col", c) in wins


def test_diag_wins():
    card = make_empty_marked()
    # main diag
    for i in range(DEFAULT_SIZE):
        card.marked[i][i] = True
    assert WinLine("diag", 0) in winning_lines(card)

    # anti diag
    card = make_empty_marked()
    for i in range(DEFAULT_SIZE):
        card.marked[i][DEFAULT_SIZE - 1 - i] = True
    assert WinLine("diag", 1) in winning_lines(card)


def test_mark_number_marks_if_present():
    card = make_empty_marked()
    # Put a known number at (0,0)
    card.grid[0][0] = 99
    assert mark_number(card, 99) is True
    assert card.marked[0][0] is True
    # Not present
    assert mark_number(card, 12345) is False


