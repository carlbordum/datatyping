import pytest
from datatyping.datatyping import validate


def test_empty():
    with pytest.raises(TypeError):
        assert validate([], ()) is None


def test_empty_reversed():
    with pytest.raises(TypeError):
        assert validate((), []) is None


def test_plain():
    with pytest.raises(TypeError):
        assert validate([int], (1, 2, 3, 4, 5)) is None


def test_plain_reversed():
    with pytest.raises(TypeError):
        assert validate((int, ), [1, 2, 3, 4, 5]) is None


from types import SimpleNamespace


def test_mapping_empty():
    with pytest.raises(TypeError):
        assert validate([dict], [SimpleNamespace(),
                                 SimpleNamespace(), SimpleNamespace()]) is None


def test_mapping_empty_reversed():
    with pytest.raises(TypeError):
        assert validate([SimpleNamespace], [{}, {}, {}]) is None


def test_dict_nested():
    with pytest.raises(TypeError):
        assert validate([{'a': {'b': [dict]}}],
                        [
            {'a': {'b': [{}, SimpleNamespace()]}},
            {'a': {'b': [{'any': 'key'}, {'used': 'here'}]}},
        ]) is None
