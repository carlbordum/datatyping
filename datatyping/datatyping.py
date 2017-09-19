__all__ = ['validate', 'customtype']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


import collections.abc


class CustomType:
    def __init__(self, function):
        self.validate = function


customtype = CustomType


def validate(structure, data, *, strict=True):
    """Verify that values in a dataset is of correct types.

    Usage:
        >>> validate([str], ['a', 'b', 'c'])
        >>> validate(
                {'id': int, 'lucky_numbers': [int]},
                {'id': 700, 'lucky_numbers': [1, 3, 7, 13]}
            )
        >>> validate([int], [1, 2, 3, 4.5])
        TypeError: 4.5 is of type float, expected type int.

    Parameters
    ----------
    strict : bool
        Dicts in `data` must have the **exact** keys specified in
        `structure`. No more.

    Raises
    ------
    TypeError
        If an elements in `data` has wrong type.
    KeyError
        If a dict in `data` misses a key or `strict` is True and a dict
        has keys not in `structure`.

    """
    if (isinstance(structure, collections.abc.Sequence)
            and not isinstance(data, str)):
        if len(structure) == 1:
            for item in data:
                validate(structure[0], item, strict=strict)
        else:
            assert len(structure) == len(data), 'Malformed structure'
            for type_, item in zip(structure, data):
                validate(type_, item, strict=strict)
    elif isinstance(structure, collections.abc.Mapping):
        for key, type_ in structure.items():
            item = data[key]
            validate(type_, item, strict=strict)
        if strict and len(structure) != len(data):
            raise KeyError(set(structure.keys()) ^ set(data.keys()))
    elif isinstance(structure, CustomType):
        structure.validate(data)
    elif not isinstance(data, structure):  # structure is a type here
        error_msg = '%s is of type %s, expected type %s' % (
                data, type(data).__name__, structure.__name__)
        raise TypeError(error_msg)
