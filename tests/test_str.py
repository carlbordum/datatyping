import pytest
from datatyping import validate


def test_simple():
    assert validate([str], ['ab', 'cd']) is None


def test_simple_error():
    with pytest.raises(TypeError):
        validate([str], 'asd')


def test_nested():
    assert validate([[str]], [['ab', 'cd'], ['ef', 'g']]) is None
