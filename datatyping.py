__all__ = ['validate']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


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
    if isinstance(data, list) and len(structure) == 1:
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
    elif not isinstance(data, structure):
        error_msg = '{} is of type {}, expected type {}'
        raise TypeError(error_msg.format(data, type(data), structure))
