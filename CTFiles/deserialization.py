from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}

    # TODO: Validate and parse using the data-type specific functions

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
