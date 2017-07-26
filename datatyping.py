def validate_data(structure, data, strict=True):
    if isinstance(data, list) and len(structure) == 1:
        for item in data:
            validate_data(structure[0], item, strict=strict)
    elif isinstance(structure, list) and isinstance(data, list):
        for item, type_ in zip(data, structure):
            validate_data(type_, item, strict=strict)
    elif isinstance(structure, dict):
        for key, type_ in structure.items():
            item = data[key]
            validate_data(type_, item, strict=strict)
        if strict and len(structure) != len(data):
            raise KeyError(set(structure.keys()) ^ set(data.keys()))
    elif not isinstance(data, structure):
        error_msg = '{} is of type {}, expected type {}'
        raise TypeError(error_msg.format(data, type(data), structure))
    return True
