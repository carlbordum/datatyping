from collections import OrderedDict

import pytest
from hypothesis import given
from hypothesis.strategies import lists, iterables, integers, dictionaries, \
    fixed_dictionaries

from datatyping.datatyping import validate


# The `hypothesis.strategies.tuples` is not used because it doesn't
# work in the same way as `hypothesis.strategies.lists`.
# See https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.tuples
@given(lst=lists(integers()), tpl=iterables(integers()).map(tuple))
def test_different_sequences(lst, tpl):
    with pytest.raises(TypeError):
        if tpl:
            validate([int], tpl)
        else:
            validate([], tpl)

    with pytest.raises(TypeError):
        if lst:
            validate((int), lst)
        else:
            validate((), lst)


@given(dct=dictionaries(integers(), integers()))
def test_different_mappings(dct):
    with pytest.raises(TypeError):
        validate(dict, OrderedDict(dct))
        validate(OrderedDict, dct)


@given(lst=lists(
    fixed_dictionaries({
        'a': fixed_dictionaries({
            'b': lists(
                dictionaries(integers(), integers(), min_size=1, max_size=3),
                min_size=1,
                max_size=3
            )
        })
    }),
    min_size=1
))
def test_dict_nested(lst):
    assert validate([{'a': {'b': [dict]}}], lst) is None
