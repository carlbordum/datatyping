import pytest
from datatyping.datatyping import validate, customtype


@customtype
def positive_int(i):
    if i < 1:
        raise TypeError('%d is negative (smile :))' % i)


@customtype
def title(s):
    if s != s.title():
        raise TypeError('%s is not a title' % s)


@customtype
def two_item_list(sequence):
    if len(sequence) not in (2, 3):
        raise TypeError(len(sequence))


# pi = positive_int
# t = title
# til = two_item_list


def test_simple_pi():
    assert validate([positive_int], [1, 2, 3, 4, 1203]) is None


def test_simple_t():
    assert validate([title], ['A Title', 'Another Title String']) is None


def test_simple_til():
    assert validate([two_item_list], [
                    [1, 2], ['a', -4, 5], [3.4, 'b']]) is None


def test_simple_til2():
    assert validate(two_item_list, [1, 2]) is None


def test_simple_pi_error():
    with pytest.raises(TypeError):
        validate(positive_int, -1)


def test_simple_t_error():
    with pytest.raises(TypeError):
        validate(title, 'I do not write title like the Brittish')


def test_simple_til_error():
    with pytest.raises(TypeError):
        validate(two_item_list, [0, 1, 2, 3])


def test_nested():
    struct = [
        {'id': positive_int, 'name': title}
    ]
    data = [
        {'id': 5, 'name': 'Donald Duck'},
        {'id': 6, 'name': 'Walt Disney'},
    ]
    assert validate(struct, data) is None


def test_nested_error():
    with pytest.raises(TypeError):
        validate([{'id': positive_int, 'name': title}],
                 [
            {'id': 7, 'name': 'Donald Duck'},
            {'id': -8, 'name': 'Walt Disney'},
        ]
        )


def test_deep_nesting():
    struct = [two_item_list, [positive_int, two_item_list], [title]]
    data = [[1, 2], [3, [4, 5]], ['Carl', 'Bordum', 'Hansen']]
    assert validate(struct, data, strict=False) is None
