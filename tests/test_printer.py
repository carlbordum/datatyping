import pytest
from datatyping.printer import write
from io import StringIO


def test_simple_ints():
    f = StringIO()
    write([1, 2, 3], stream=f)
    assert f.getvalue() == '[int]'


def test_simple_strs():
    f = StringIO()
    write(['a', 'b', 'c'], stream=f)
    assert f.getvalue() == '[str]'


def test_simple_mix():
    f = StringIO()
    write(['a', 1, 2, 'b'], stream=f)
    assert f.getvalue() == '[str, int, int, str]'
