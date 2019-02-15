from command.column import Table
import pytest


@pytest.mark.parametrize("table,n,start,expected_rv,expected_state", [
    (Table([["a"], ["b"], ["c"], ["d"]]), 1, 1, ["b"], [["a"], ["c"], ["d"]]),
    (Table([["a"], ["b"], ["c"], ["d"]]), 3, 1, ["b", "c", "d"], [["a"]]),
    (Table([["a", "b"], ["c", "d"], ["e"], ["f"]]), 1, 1, ["c"], [["a", "b"], ["d"], ["e"], ["f"]]),
    (Table([["a", "b"], ["c", "d"], ["e"], ["f"]]), 3, 1, ["c", "d", "e"], [["a", "b"], ["f"]]),
])
def test_take(table, n, start, expected_rv, expected_state):
    actual = table._take(n, start)
    assert actual == expected_rv
    assert table.columns == expected_state