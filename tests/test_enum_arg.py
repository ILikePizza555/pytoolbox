import pytest
from command.utils.arg import EnumArg
from enum import auto

def test_simple_creation():
    class TestEnum(EnumArg):
        a = 1, ["-a"]
        b = 2, ["-b"], "dest"
    
    assert TestEnum.a.value == 1
    assert TestEnum.a.arg_flags == ["-a"]
    assert not TestEnum.a.dest

    assert TestEnum.b.value == 2
    assert TestEnum.b.arg_flags == ["-b"]
    assert TestEnum.b.dest == "dest"


def test_auto_value():
    class TestEnum(EnumArg):
        a = auto(), ["-a"]
        b = auto(), ["-b"]

    assert not isinstance(TestEnum.a.value, auto)
    assert not isinstance(TestEnum.b.value, auto)