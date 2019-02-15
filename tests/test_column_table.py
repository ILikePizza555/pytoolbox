from command.column import Table
import pytest


@pytest.mark.parametrize("table,n,start,expected_rv,expected_state", [
    (Table([["a"], ["b"], ["c"], ["d"]]), 1, 1, ["b"], [["a"], ["c"], ["d"]]),
    (Table([["a"], ["b"], ["c"], ["d"]]), 3, 1, ["b", "c", "d"], [["a"]]),
    (Table([["a", "b"], ["c", "d"], ["e"], ["f"]]), 1, 1, ["c"], [["a", "b"], ["d"], ["e"], ["f"]]),
    (Table([["a", "b"], ["c", "d"], ["e"], ["f"]]), 3, 1, ["c", "d", "e"], [["a", "b"], ["f"]]),
    (Table([["a"]]), 1, 0, ["a"], [])
])
def test_take(table, n, start, expected_rv, expected_state):
    actual = table._take(n, start)
    assert actual == expected_rv
    assert table.columns == expected_state


@pytest.mark.parametrize("table,r,expected_state", [
    (Table([["a"], ["b"], ["c"], ["d"]]), 2, [["a", "b"], ["c", "d"]]),
    (Table([["a"], ["b"], ["c"], ["d"]]), 3, [["a", "b", "c"], ["d"]]),
    (Table([["a"], ["b"], ["c"], ["d"]]), 2, [["a", "b"], ["c", "d"]]),
    (Table([["a", "b", "c"], ["d", "e"], ["f"]]), 3, [["a", "b", "c"], ["d", "e", "f"]]),
    (Table([["a"], ["b", "c"], ["d", "e", "f"]]), 3, [["a", "b", "c"], ["d", "e", "f"]]),
])
def test_compress_columns(table, r, expected_state):
    table._compress_columns(r)

    assert table.columns == expected_state