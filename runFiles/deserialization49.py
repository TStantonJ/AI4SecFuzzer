from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    result = marshalled_string.find('%')
    if (result != -1):
        ret = marshalled_string.replace('%', '\\x')
    else:
        length = len(marshalled_string)
        mstring = marshalled_string[:length-1]
    # TODO: Validate and convert

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    str = marshalled_integer[1:]
    ret = int(str)
    # TODO: Validate and convert

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    indexCol = marshalled_map.find(':')
    indexBrack = marshalled_map.find('}')
    key = marshalled_map[1:indexCol]
    value = marshalled_map[indexCol + 1:indexBrack]
    if value[len(value)-1].isdigit():
        value = __unmarshal_integer(value)
        ret[key] = value
    # TODO: Validate and parse using the data-type specific functions
    else:
        value = __unmarshal_string(marshalled_map)
    
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if len(marshalled_state) == 0:
        raise DeserializationError('Input is empty')
    if marshalled_state.find('[') != -1 or marshalled_state.find(']') != -1:
        raise DeserializationError('Invalid Bracket')
    result = marshalled_state.find(':')
    if result == -1:
        if marshalled_state == '{}':
            pass
        else:
            raise DeserializationError('Invalid Format')
    

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
