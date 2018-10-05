import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers, floats, text, one_of, dictionaries

from datatyping.datatyping import validate


def test_empty():
    assert validate([], []) is None


@given(li=lists(integers()))
def test_plain(li):
    assert validate([int], li) is None


@given(lst=lists(one_of(floats(), text()), min_size=1))
def test_plain_typeerror(lst):
    with pytest.raises(TypeError):
        validate([int], lst)


def test_list_lengths():
    with pytest.raises(ValueError):
        validate([int, int, int, str], [1, 2, 3, 'a', 'a'])


@given(li=lists(integers(), max_size=1))
def test_list_too_short_same_type(li):
    with pytest.raises(ValueError):
        validate([int, int], li)


@given(li=lists(integers(), min_size=3))
def test_list_too_long_same_type(li):
    with pytest.raises(ValueError):
        validate([int, int], li)


def test_dict_empty():
    assert validate([dict], [{}, {}, {}]) is None


@given(i=integers())
def test_dict_strict(i):
    assert validate([{'a': int}], [{'a': i}, {'a': 456}]) is None


@given(lists(dictionaries(one_of(integers(), text()), one_of(integers(), text()))))
def test_any_dict(d):
    assert validate([dict], d) is None


def test_dict_nested():
    assert validate([{'a': {'b': [dict]}}],
                    [
                        {'a': {'b': [{}, {}]}},
                        {'a': {'b': [{'any': 'key'}, {'used': 'here'}]}},
    ]) is None
