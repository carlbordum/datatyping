"""Like pprint, but with types except for dictionary keys."""


__all__ = ['pprint', 'pformat']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


import pprint as _pprint
import contextlib


def _new_format_dict_items(self, items, stream, indent, allowance,
                           context, level):
    write = stream.write
    indent += self._indent_per_level
    last_index = len(items) - 1
    write('\n')
    write(' ' * indent)
    for i, (key, ent) in enumerate(items):
        last = i == last_index
        rep = repr(key)
        write(rep)
        write(': ')
        self._format(ent, stream, indent,
                     allowance if last else 1,
                     context, level)
        write(',\n')
        if last:
            write((' ' * indent)[:-self._indent_per_level])
        else:
            write(' ' * indent)


def _new_safe_repr(object, context, maxlevels, level):
    """Return object type name except for dict keys.
    
    Like `pprint._safe_repr`, but returns type name of object instead
    of object repr except for dictionary keys. Also formats lists and
    tuples nicely.

    Used to overwrite `pprint._safe_repr` with the context manager
    `change_pprint_repr`.
    """
    typerepr = lambda object: type(object).__name__
    type_ = type(object)
    if type_ in _pprint._builtin_scalars:
        return typerepr(object), True, False

    r = getattr(type_, '__repr__', None)
    if issubclass(type_, dict) and r is dict.__repr__:
        if not object:
            return 'dict', True, False
        context[id(object)] = 1
        readable = True
        recursive = False
        level += 1
        pairs = []
        for k, v in object.items():
            vrepr, vreadable, recur = _new_safe_repr(
                v, context, maxlevels, level)
            pairs.append('%s: %s' % (repr(k), vrepr))
            readable = readable and vreadable
            if recur:
                recursive = True
        del context[id(object)]
        return '{%s}' % ', '.join(pairs), readable, recursive
    if issubclass(type_, (list, tuple)):
        if issubclass(type_, list):
            if not object:
                return 'list', True, False
            format = '[%s]'
        else:  # its a tuple
            if not object:
                return 'tuple', True, False
            format = '(%s)' if len(object) != 1 else '(%s,)'
        context[id(object)] = 1
        readable = True
        recursive = False
        items = []
        level += 1
        for item in object:
            irepr, ireadable, irecur = _new_safe_repr(
                item, context, maxlevels, level)
            items.append(irepr)
            if not ireadable:
                readable = False
            if irecur:
                recursion = True
        del context[id(object)]
        if len(set(items)) == 1:
            items = [items[0]]
        return format % ', '.join(items), readable, recursive
    return typerepr(object), True, False


@contextlib.contextmanager
def change_pprint_repr():
    old_safe_repr = _pprint._safe_repr
    _pprint._safe_repr = _new_safe_repr
    old_format_dict_items = _pprint.PrettyPrinter._format_dict_items
    _pprint.PrettyPrinter._format_dict_items = _new_format_dict_items
    yield
    _pprint._safe_repr = old_safe_repr
    _pprint.PrettyPrinter._format_dict_items = old_format_dict_items


def pprint(object, stream=None, indent=4, width=80, depth=None,
           compact=False):
    """Pretty-prints the data structure."""
    with change_pprint_repr():
        _pprint.pprint(object, stream=stream, indent=indent, width=width,
                       depth=depth, compact=compact)


def pformat(object, indent=4, width=80, depth=None, compact=False):
    """Return the pretty printed data structure of *object*."""
    with change_pprint_repr():
        return _pprint.pformat(object, indent=indent, width=width,
                               depth=depth, compact=compact)
