from command.touch import parse_time_decimal
import datetime
import pytest

current_year = datetime.date.today().year

@pytest.mark.parametrize(("func_input", "expected"), [
    ("04200420",        datetime.datetime(current_year, 4, 20, 4, 20)),
    ("10111213.14",     datetime.datetime(current_year, 10, 11, 12, 13, 14)),
    ("9709091234",      datetime.datetime(1997, 9, 9, 12, 34)),
    ("9702021234.15",   datetime.datetime(1997, 2, 2, 12, 34, 15)),
    ("1401010730",      datetime.datetime(2014, 1, 1, 7, 30)),
    ("1501020420.20",   datetime.datetime(2015, 1, 2, 4, 20, 20)),
    ("240103211234"),   datetime.datetime(2401, 3, 21, 12, 34),
    ("240103211234.20", datetime.datetime(2401, 3, 21, 12, 34, 20))
])
def test_unix_time_decimal(func_input, expected):
    assert parse_time_decimal(func_input) == expected