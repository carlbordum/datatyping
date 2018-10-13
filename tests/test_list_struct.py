import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers, floats, text, one_of, dictionaries, \
    fixed_dictionaries

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


def test_dict_empty():
    assert validate([dict], [{}]) is None


@given(lst=lists(fixed_dictionaries({'a': integers()})))
def test_dict_strict(lst):
    assert validate([{'a': int}], lst) is None


@given(lists(dictionaries(one_of(integers(), text()), one_of(integers(), text()))))
def test_any_dict(d):
    assert validate([dict], d) is None


def test_dict_nested():
    assert validate([{'a': {'b': [dict]}}],
                    [
                        {'a': {'b': [{}, {}]}},
                        {'a': {'b': [{'any': 'key'}, {'used': 'here'}]}},
    ]) is None
