from exceptions import SerializationError

def __marshal_string(py_string):
    ret = ''

    # TODO: Validate and encode

    return ret

def __marshal_integer(py_int):
    ret = ''

    # TODO: Validate and encode

    return ret

def __marshal_map(py_dict):
    ret = '{'

    for key, value in py_dict.items():
        pass
        # TODO: Validate, dispatch, and combine

    ret += '}'
    return ret

def marshal(unmarshalled_state):
    if unmarshalled_state is None:
        raise SerializationError('Input is None')
    if type(unmarshalled_state) != dict:
        raise SerializationError('Input is not a dict')

    # TODO: Validate things about the overall Python3 dict

    return __marshal_map(unmarshalled_state)
