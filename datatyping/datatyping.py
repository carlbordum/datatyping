__all__ = ['validate', 'customtype']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


import collections.abc
import reprlib


def customtype(check_function):
    """Decorate a function, so it can be used for type checking.

    Usage:
        @customtype
        def two_item_list(l):
            if len(l) != 2:
                raise TypeError('length %d!!!' % len(l))

        validate([two_item_list], [[1, 2], [3, 4]])  # passes
        validate([two_item_list], [[1, 2], [3, 4, 5]])  # TypeError

    Sets the `check_function.__datatyping_validate` attribute.

    Parameters
    ----------
    check_function : function
        Function that should be used to type check.

    """
    check_function.__datatyping_validate = True
    return check_function


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
    structure : type or collection of types
        The data structure that `data` should follow.
    data : anything
        The data you want type checked.
    strict : bool
        Dicts in `data` must have the **exact** keys specified in
        `structure`. No more.

    Raises
    ------
    TypeError
        If an elements in `data` has wrong type.
    ValueError
        If the length of `structure` doesn't make sense for validating
        `data`.
    KeyError
        If a dict in `data` misses a key or `strict` is True and a dict
        has keys not in `structure`.

    """
    if hasattr(structure, '__datatyping_validate'):
        structure(data)
    elif (isinstance(structure, collections.abc.Sequence)
            and not isinstance(data, str)):
        if len(structure) == 1:
            for item in data:
                validate(structure[0], item, strict=strict)
        else:
            if len(structure) != len(data):
                error_msg = ('%s has the wrong length. Expected %d, got %d.'
                        ) % (reprlib.repr(data), len(structure), len(data))
                raise ValueError(error_msg)
            for type_, item in zip(structure, data):
                validate(type_, item, strict=strict)
    elif isinstance(structure, collections.abc.Mapping):
        if strict and len(structure) != len(data):
            raise KeyError(set(structure.keys()) ^ set(data.keys()))
        for key, type_ in structure.items():
            item = data[key]  # or KeyError :)
            validate(type_, item, strict=strict)
    elif not isinstance(data, structure):  # structure is a type here
        error_msg = '%s is of type %s, expected type %s' % (
                data, type(data).__name__, structure.__name__)
        raise TypeError(error_msg)
