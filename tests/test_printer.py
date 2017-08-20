import pytest
import requests
from datatyping.printer import pformat


def test_simple_ints():
    assert pformat([1, 2, 3]) == '[int]'


def test_simple_strs():
    assert pformat(['a', 'b', 'c']) == '[str]'


def test_simple_mix():
    assert pformat(['a', 1, 2, 'b']) == '[str, int, int, str]'


def test_simple_dict():
    assert pformat({'a': 1, 'b': 2}) == "{'a': int, 'b': int}"


def test_dict_mix():
    assert pformat({'a': [1, 2, 3], 'b': 'c'}) == "{'a': [int], 'b': str}"


def test_advanced():
    expected = ("{   'args': dict,"
    "\n    'data': str,"
    "\n    'files': dict,"
    "\n    'form': dict,"
    "\n    'headers': {'Accept': str,"
    "\n                'Accept-Encoding': str,"
    "\n                'Connection': str,"
    "\n                'Host': 'httpbin.org',"
    "\n                'User-Agent': str},"
    "\n    'json': NoneType,"
    "\n    'method': str,"
    "\n    'origin': str,"
    "\n    'url': str}")
    r = requests.get('http://httpbin.org/anything')
    assert pformat(r.json()) == expected
