import pytest
from hypothesis import given
from hypothesis.strategies import lists, text
from datatyping import validate


@given(ss=lists(text()))
def test_simple(ss):
    assert validate([str], ss) is None


@given(s=text())
def test_simple_error(s):
    with pytest.raises(TypeError):
        validate([str], s)


@given(ss=lists(lists(text())))
def test_nested(ss):
    assert validate([[str]], ss) is None
