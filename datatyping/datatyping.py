__all__ = ['validate', 'Contract']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


import collections.abc


class Contract(collections.abc.Sequence):
    """Ensure that data meets a certain requirement.

    Usage:
        >>> class ShortString(Contract):
        ...     @staticmethod
        ...     def validate(s):
        ...         if len(s) > 5:
        ...             error_msg = '%s is too long (%d > 5)' % (s, len(s))
        ...             raise TypeError(error_msg)
        ...
        >>> validate([ShortString], ['asdf', 'asdfg', 'asdfgh'])
        TypeError: asdfgh is too long (6 > 5)

    See Also
    --------
    https://github.com/Zaab1t/datatyping/blob/master/tests/test_contracts.py
    
    """

    def __init__(self, *children):
        self.children = list(children)

    def __len__(self):
        return len(self.children)

    def __getitem__(self, i):
        return self.children[i]


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
    if isinstance(structure, type) and issubclass(structure, Contract):
        structure.validate(data)  # *structure* is a `Contract` class
    elif isinstance(structure, collections.abc.Sequence):
        # if *structure* is `Contract` it's a sequence
        if len(structure) == 1:
            for item in data:
                validate(structure[0], item, strict=strict)
        else:
            assert len(structure) == len(data), 'Malformed structure'
            for type_, item in zip(structure, data):
                validate(type_, item, strict=strict)
    elif isinstance(structure, dict):
        for key, type_ in structure.items():
            item = data[key]
            validate(type_, item, strict=strict)
        if strict and len(structure) != len(data):
            raise KeyError(set(structure.keys()) ^ set(data.keys()))
    elif not isinstance(data, structure):  # structure is a type here
        error_msg = '%s is of type %s, expected type %s' % (
                data, type(data).__name__, structure.__name__)
        raise TypeError(error_msg)
