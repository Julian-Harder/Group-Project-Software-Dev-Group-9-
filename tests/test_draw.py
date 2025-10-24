import pytest

from mini_bingo.draw import DrawPool


def test_draws_75_unique_numbers():
    pool = DrawPool(seed=123)
    seen = set()
    while not pool.empty:
        n = pool.draw()
        assert 1 <= n <= 75
        assert n not in seen
        seen.add(n)
    assert len(seen) == 75
    assert pool.remaining() == 0


def test_deterministic_order_with_seed():
    a = DrawPool(seed=42)
    b = DrawPool(seed=42)
    seq_a = [a.draw() for _ in range(10)]
    seq_b = [b.draw() for _ in range(10)]
    assert seq_a == seq_b


def test_peek_does_not_consume():
    pool = DrawPool(seed=999)
    first_peek = pool.peek()
    first_draw = pool.draw()
    assert first_peek == first_draw
    # second peek should match second draw as well
    second_peek = pool.peek()
    second_draw = pool.draw()
    assert second_peek == second_draw


def test_reset_changes_sequence_if_seed_changes():
    pool = DrawPool(seed=1)
    seq1 = [pool.draw() for _ in range(5)]
    pool.reset(seed=2)
    seq2 = [pool.draw() for _ in range(5)]
    assert seq1 != seq2


def test_exhaustion_raises_indexerror():
    pool = DrawPool(seed=7)
    for _ in range(75):
        pool.draw()
    with pytest.raises(IndexError):
        pool.draw()
