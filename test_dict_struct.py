import pytest
from datatyping import validate


def test_empty():
    assert validate({}, {})


def test_plain():
    assert validate({'a': int, 'b': str}, {'a': 1, 'b': 'c'})


def test_plain_typeerror():
    with pytest.raises(TypeError):
        validate({'a': int}, {'a': 3.4})


def test_plain_keyerror():
    with pytest.raises(KeyError):
        validate({'a': str, 'b': float}, {'a': 'abc'})


def test_plain_no_strict():
    assert validate({'a': str}, {'a': 'abc', 'b': 123}, strict=False)


def test_plain_no_strict_error():
    with pytest.raises(KeyError):
        validate({'a': str, 'b': float}, {'a': 'abc'}, strict=False)


def test_strict():
    with pytest.raises(KeyError):
        validate({'a': str}, {'a': 'abc', 'oh no too much data': 123})


def test_list():
    assert validate({'a': [int]}, {'a': [1, 2, 3]})


def test_list_typeerror():
    with pytest.raises(TypeError):
        validate({'a': [int]}, {'a': [1, 2, 3.6]})


def test_nested_list():
    assert validate({'a': [[int], [str]]},
            {'a': [[1,2,3,4], ['a', 'b', 'c', 'd']]})


def test_nested_dict():
    assert validate({'a': {'b': [[int], [str]]}},
            {'a': {'b': [[1,2,3,4], ['a','b','c']]}})


def test_mad_nesting():
    assert validate({'list': [int, str, [[int], [int]]]},
            {'list': [1, 'a', [[1,2,3], [4,5,6]]]})


def test_advanced():
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
    data = {
        'total_count': 52,
        'active': False,
        'people': [
            {'id': 23974291847, 'title': 'big guy', 'salary': 256.12},
            {'id': 1932, 'title': 'python developer', 'salary': 4.5},
            {'id': 9828974, 'title': 'president', 'salary': 122352.23},
        ],
        'timestamps': [12351346, 12345134, 7684545, 1267457, 0],
    }
    assert validate(structure, data)
