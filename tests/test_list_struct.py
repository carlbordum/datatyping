import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers, floats, one_of, composite

from datatyping.datatyping import validate


def test_empty():
    assert validate([], []) is None


@given(li=lists(integers()))
def test_plain(li):
    assert validate([int], li) is None


@given(lst=lists(floats(), min_size=1))
def test_plain_type_error(lst):
    with pytest.raises(TypeError):
        validate([int], lst)


@given(lst=one_of(lists(integers(), min_size=5),
                  lists(integers(), max_size=3)))
def test_list_lengths(lst):
    with pytest.raises(ValueError):
        validate([int, int, int, str], lst)


@given(lst=lists(lists(integers())))
def test_nested(lst):
    assert validate([[int]], lst)

    with pytest.raises(TypeError):
        validate([int], lst)


@composite
def heavy_nested_data(draw):
    return [draw(lists(integers)), draw(floats()), lists(lists(floats()))]


@given(lst=heavy_nested_data())
def test_heavy_nested(lst):
    assert validate([[int], float, [[float]]], lst) is None

    with pytest.raises(TypeError):
        assert validate([[str], int, int], lst)

    with pytest.raises(ValueError):
        validate([[[float]]], lst)
