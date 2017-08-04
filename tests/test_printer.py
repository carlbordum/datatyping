import pytest
from datatyping.printer import pformat


def test_simple_ints():
    assert pformat([1, 2, 3]) == '[int]'


def test_simple_strs():
    assert pformat(['a', 'b', 'c']) == '[str]'


def test_simple_mix():
    assert pformat(['a', 1, 2, 'b']) == '[str, int, int, str]'
