import pytest
from hypothesis import given
from hypothesis.strategies import integers, text

from datatyping.datatyping import validate


@given(string=text())
def test_simple(string):
    assert validate(str, string) is None


@given(not_string=integers())
def test_simple_error(not_string):
    with pytest.raises(TypeError):
        validate(str, not_string)
