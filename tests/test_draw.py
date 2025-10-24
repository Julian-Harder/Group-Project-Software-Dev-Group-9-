from mini_bingo.draw import DrawPool


def test_unique_and_in_range():
    pool = DrawPool(seed=123)
    seen = set()
    while not pool.empty:
        n = pool.draw()
        assert 1 <= n <= 75
        assert n not in seen
        seen.add(n)
    assert len(seen) == 75


def test_deterministic_with_seed():
    a = DrawPool(seed=42)
    b = DrawPool(seed=42)
    assert [a.draw() for _ in range(10)] == [b.draw() for _ in range(10)]


def test_peek_is_non_consuming():
    pool = DrawPool(seed=999)
    first_peek = pool.peek()
    first_draw = pool.draw()
    assert first_peek == first_draw
