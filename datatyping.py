def _check_elem(elem, type_, strict):
    print(elem, type_)
    if isinstance(elem, list) and len(type_) == 1:
        for item in elem:
            _check_elem(item, type_[0], strict=strict)
    elif isinstance(type_, list) and isinstance(elem, list):
        for item, type__ in zip(elem, type_):
            _check_elem(item, type__, strict=strict)
    elif isinstance(type_, dict):
        validate_data(type_, elem, strict=strict)
    elif not isinstance(elem, type_):
        error_msg = '{} is of type {}, expected type {}'
        raise TypeError(error_msg.format(elem, type(elem), type_))


def validate_data(structure, data, strict=True):
    for key, type_ in structure.items():
        value = data[key]
        _check_elem(value, type_, strict=strict)
    if strict and len(structure) != len(data):
        raise KeyError(set(structure.keys()) ^ set(data.keys()))
    return True
