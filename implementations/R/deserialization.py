from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    ret = ret.replace('s', '', 1)
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    ret = ret.replace('i', '', 1)
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    ret.replace('i', '')
    ret.replace('s', '')
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    substring = 's'
    substring1 = 'i'
    if substring in ret:
        print('Input is invalid')
    elif substring not in ret:
        print('Input is valid')
    if substring1 in ret:
        print('Input is invalid')
    elif substring1 not in ret:
        print('Input is invalid')
    # Validate the unmarshalled state
    return __unmarshal_map(marshalled_state)
