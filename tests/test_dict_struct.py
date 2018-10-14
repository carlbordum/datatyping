import pytest
from hypothesis import given, assume
from hypothesis.strategies import fixed_dictionaries, integers, characters, composite, \
    dictionaries, booleans, floats, lists

from datatyping.datatyping import validate


def test_empty():
    assert validate({}, {}) is None


@given(dct=fixed_dictionaries({'a': integers(), 'b': characters()}))
def test_plain(dct):
    assert validate({'a': int, 'b': str}, dct) is None


@given(dct=fixed_dictionaries({'a': characters()}))
def test_plain_type_error(dct):
    with pytest.raises(TypeError):
        validate({'a': int}, dct)


@given(dct=fixed_dictionaries({'a': characters()}))
def test_plain_key_error(dct):
    with pytest.raises(KeyError):
        validate({'a': str, 'b': float}, dct)


@composite
def dict_with_a(draw):
    sample = draw(dictionaries(characters(), integers()))
    sample['a'] = draw(characters())
    return sample


@given(dct=dict_with_a())
def test_plain_no_strict(dct):
    assert validate({'a': str}, dct, strict=False) is None


@composite
def dict_with_a_without_b(draw):
    sample = draw(dictionaries(characters(), integers()))
    sample['a'] = draw(characters())
    sample.pop('b', None)
    return sample


@given(dct=dict_with_a_without_b())
def test_plain_no_strict_error(dct):
    with pytest.raises(KeyError):
        validate({'a': str, 'b': float}, dct, strict=False)


@given(dct=dict_with_a())
def test_strict(dct):
    assume(len(dct) > 1)
    with pytest.raises(KeyError):
        validate({'a': str}, dct)


@given(dct=fixed_dictionaries({
    'a': fixed_dictionaries({'b': integers()})
}))
def test_nested_dict(dct):
    assert validate({'a': {'b': int}}, dct) is None


@composite
def advanced_data(draw):
    return {
        'total_count': draw(integers()),
        'active': draw(booleans()),
        'people': [
            draw(fixed_dictionaries(
                {
                    'id': integers(),
                    'title': characters(),
                    'salary': floats()
                }
            ))
        ],
        'timestamps': draw(lists(integers(), min_size=1))
    }


@given(dct=advanced_data())
def test_advanced(dct):
    structure = {
        'total_count': int,
        'active': bool,
        'people': [
            {
                'id': int,
                'title': str,
                'salary': float,
            }
        ],
        'timestamps': [int],
    }
    assert validate(structure, dct) is None
