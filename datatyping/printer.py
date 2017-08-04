"""Like pprint, but with types."""


import pprint


def _new_safe_repr(object, context, maxlevels, level):
    typerepr = lambda object: type(object).__name__
    type_ = type(object)
    if type_ in pprint._builtin_scalars:
        return typerepr(object), True, False

    r = getattr(type_, '__repr__', None)
    if issubclass(type_, dict) and r is dict.__repr__:
        if not object:
            return '{}', True, False
        context[id(object)] = 1
        readable = True
        recursive = False
        level += 1
        pairs = []
        for k, v in object.items():
            vrepr, vreadable, recur = _new_safe_repr(v, context, maxlevels, level)
            pairs.append('%s: %s' % (repr(k), vrepr))
            readable = readable and vreadable
            if recur:
                recursive = True
        del context[id(object)]
        return '{%s}' % ', '.join(pairs), readable, recursive
    if issubclass(type_, (list, tuple)):
        if issubclass(type_, list):
            if not object:
                return '[]', True, False
            format = '[%s]'
        else:  # its a tuple
            if not object:
                return '()', True, False
            format = '(%s)' if len(object) != 1 else '(%s,)'
        context[id(object)] = 1
        readable = True
        recursive = False
        items = []
        level += 1
        for item in object:
            irepr, ireadable, irecur = _new_safe_repr(item, context, maxlevels, level)
            items.append(irepr)
            if not ireadable:
                readable = False
            if irecur:
                recursion = True
        del context[id(object)]
        return format % ', '.join(items), readable, recursive
    return typerepr(object), True, False


def write(data, stream=None, indent=4, width=80, depth=None,
          compact=False):
    """Pretty-prints the data structure, but prints types instead of most
    values. Arguments are passed on to pprint.pprint. This means that
    this function prints to stdout if *stream* is None.
    """
    old_safe_repr = pprint._safe_repr
    pprint._safe_repr = _new_safe_repr
    pprint.pprint(data, stream=stream, indent=indent, width=width,
        depth=depth, compact=compact)
    pprint._safe_repr = old_safe_repr
