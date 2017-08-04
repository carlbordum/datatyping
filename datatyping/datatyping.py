__all__ = ['validate', 'Contract']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


class Contract:
    """Ensure that data meets a certain requirement.
    
    Usage:
        >>> class ShortString(Contract):
                @staticmethod
        ...     def validate(s):
        ...         if len(s) > 5:
        ...             raise TypeError('%s is too long (%d > 5)' % (s, len(s)))
        ...
        >>> validate([ShortString], ['asdf', 'asdfg', 'asdfgh'])
        TypeError: asdfgh is too long (6 > 5)

    See Also
    --------
    https://github.com/Zaab1t/datatyping/blob/master/tests/test_contracts.py
    """
    def __init__(self, *children):
        self.children = list(children)


def validate(structure, data, *, strict=True):
    """Verifies that values in a dataset has the correct types.

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
        # structure is a class, not an instance
        structure.validate(data)
    elif isinstance(structure, Contract):
        if len(structure.children) == 1:
            for item in data:
                validate(structure.children[0], item, strict=strict)
        else:
            assert len(structure.children) == len(data)
            for type_, item in zip(structure.children, data):
                validate(type_, item, strict=strict)
    elif isinstance(data, list) and len(structure) == 1:
        for item in data:
            validate(structure[0], item, strict=strict)
    elif isinstance(structure, list) and isinstance(data, list):
        for item, type_ in zip(data, structure):
            validate(type_, item, strict=strict)
    elif isinstance(structure, dict):
        for key, type_ in structure.items():
            item = data[key]
            validate(type_, item, strict=strict)
        if strict and len(structure) != len(data):
            raise KeyError(set(structure.keys()) ^ set(data.keys()))
    elif not isinstance(data, structure):  # structure is a type here
        error_msg = '{} is of type {}, expected type {}'
        raise TypeError(error_msg.format(data, type(data).__name__, structure.__name__))
