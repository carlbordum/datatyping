import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats, one_of, iterables

from datatyping.datatyping import validate


# The `hypothesis.strategies.tuples` is not used because it doesn't
# work in the same way as `hypothesis.strategies.lists`.
# See https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.tuples
@given(tpl=iterables(integers()).map(tuple))
def test_plain(tpl):
    assert validate((int,), tpl) is None


@given(tpl=iterables(floats(), min_size=1).map(tuple))
def test_plain_type_error(tpl):
    with pytest.raises(TypeError):
        validate((int,), tpl)


@given(tpl=one_of(iterables(integers(), min_size=5).map(tuple),
                  iterables(integers(), max_size=3).map(tuple)))
def test_list_lengths(tpl):
    with pytest.raises(ValueError):
        validate((int, int, int, str), tpl)
