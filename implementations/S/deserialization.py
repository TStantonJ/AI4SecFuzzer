from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = {}
    for keys in marshalled_string:
        indexCol = marshalled_string.find(':')
        key = marshalled_string[1:indexCol]
        result = marshalled_string.find('%00')
        if (result != -1):
            str = marshalled_string.replace('%00', '\x00')
            value = str[indexCol+1:len(str)-1]
            ret[key] = value
            return ret
        result = marshalled_string.find('%2C')
        if (result != -1):
            str = marshalled_string.replace('%2C', ',')
            value = str[indexCol+1:len(str)-1]
            ret[key] = value
            return ret
        else:
            length = len(marshalled_string)
            mstring = marshalled_string[indexCol+1:length-2]
            ret[key] = mstring
            return ret
    # TODO: Validate and convert

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = {}
    indexCol = marshalled_integer.find(':')
    if indexCol != -1:
        key = marshalled_integer[1:indexCol]
        value = marshalled_integer[indexCol+1:]
        result = value.find(':')
        if result != -1:
            value = value[result:]
            value = int(value[2:])
            ret[key] = value
            return ret
        else:
            value = int(value[1:])
            ret[key] = value
            return ret
    ret = 0
    str = marshalled_integer[1:]
    ret = int(str)
    # TODO: Validate and convert

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    if marshalled_map == '{}':
        return {}
    indexCol = marshalled_map.find(':')
    indexBrack = marshalled_map.find('}')
    key = marshalled_map[1:indexCol]
    value = marshalled_map[indexCol + 1:indexBrack]
    if value[len(value)-1].isdigit():
        value = __unmarshal_integer(value)
        ret[key] = value
    # TODO: Validate and parse using the data-type specific functions
    else:
        ret = __unmarshal_string(marshalled_map)
    
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
