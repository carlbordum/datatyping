import pytest
from datatyping import validate


def test_simple():
    with pytest.raises(TypeError):
        validate([str], 'asd')
