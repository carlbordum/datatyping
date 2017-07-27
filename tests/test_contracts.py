import pytest
from datatyping import validate, Contract


class PositiveInteger(Contract):
    @staticmethod
    def validate(i):
        if i < 1:
            raise TypeError('%d is negative (smile :))' % i)


class Title(Contract):
    @staticmethod
    def validate(s):
        if s != s.title():
            raise TypeError('%s is not a title' % s)


class TwoItemList(Contract):
    @staticmethod
    def validate(l):
        if len(l) != 2:
            raise TypeError('list is of length %d, not 2' % len(l))


# pi = PositiveInteger
# t = Title
# til = TwoItemList


def test_simple_pi():
    assert validate([PositiveInteger], [1, 2, 3, 4, 1203]) is None


def test_simple_t():
    assert validate([Title], ['A Title', 'Another Title String']) is None


def test_simple_til():
    assert validate([TwoItemList], [[1, 2], ['a', -4], [3.4, 'b']]) is None


def test_simple_pi_error():
    with pytest.raises(TypeError):
        validate(PositiveInteger, -1)


def test_simple_t_error():
    with pytest.raises(TypeError):
        validate(Title, 'I do not write title like the Brittish')


def test_simple_til_error():
    with pytest.raises(TypeError):
        validate(TwoItemList, [0, 1, 2, 3])


def test_nested_contracts():
    struct = TwoItemList(
        {'id': PositiveInteger, 'name': Title}
    )
    data = [
        {'id': 5, 'name': 'Donald Duck'},
        {'id': 6, 'name': 'Walt Disney'},
    ]
    assert validate(struct, data) is None


def test_nested_contracts_error():
    with pytest.raises(TypeError):
        validate(TwoItemList({'id': PositiveInteger, 'name': Title}),
            [
                {'id': 7, 'name': 'Donald Duck'},
                {'id': -8, 'name': 'Walt Disney'},
            ])

def test_insane_nesting():
    struct = TwoItemList(
            TwoItemList(
                {},
                {
                    'name': Title,
                    'age': PositiveInteger,
                },
            ),
            PositiveInteger,
    )
    data = [
        [
            {'any': 1, 'keys': 'r', 'valid': 'here'},
            {'name': 'Carl Bordum Hansen', 'age': 18},
        ],
        23987348650,
    ]
    assert validate(struct, data, strict=False) is None
