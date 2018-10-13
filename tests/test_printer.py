import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers, characters, composite, \
    fixed_dictionaries, dictionaries, none

from datatyping.printer import pformat


@given(lst=lists(integers(), min_size=1))
def test_simple_ints(lst):
    assert pformat(lst) == '[int]'


@given(lst=lists(characters(), min_size=1))
def test_simple_strs(lst):
    assert pformat(lst) == '[str]'


@composite
def list_mix(draw):
    return [
        draw(characters()),
        draw(integers()),
        draw(integers()),
        draw(characters())
    ]


@given(lst=list_mix())
def test_simple_mix(lst):
    assert pformat(lst) == '[str, int, int, str]'


@given(dct=fixed_dictionaries(
    {'a': integers(), 'b': integers()}
))
def test_simple_dict(dct):
    assert pformat(dct) == "{'a': int, 'b': int}"


@given(dct=fixed_dictionaries(
    {'a': lists(integers(), min_size=1), 'b': characters()}
))
def test_dict_mix(dct):
    assert pformat(dct) == "{'a': [int], 'b': str}"


@composite
def request_data(draw):
    return {
        'args': {},
        'data': draw(characters()),
        'headers': {
            'Accept': draw(characters()),
            'Accept-Encoding': draw(characters()),
            'Connection': draw(characters()),
            'Host': draw(characters()),
            'User-Agent': draw(characters()),
        },
        'json': draw(none()),
        'method': draw(characters()),
        'url': draw(characters())
    }


@given(request=request_data())
def test_advanced(request):
    expected = (
        "{   "
        "\n    'args': dict,"
        "\n    'data': str,"
        "\n    'headers': {   "
        "\n        'Accept': str,"
        "\n        'Accept-Encoding': str,"
        "\n        'Connection': str,"
        "\n        'Host': str,"
        "\n        'User-Agent': str,"
        "\n    },"
        "\n    'json': NoneType,"
        "\n    'method': str,"
        "\n    'url': str,"
        "\n}"
    )
    assert pformat(request) == expected
