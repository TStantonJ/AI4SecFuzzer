from exceptions import DeserializationError
import urllib

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert
    if marshalled_string is None or type(marshalled_string) != str or not(marshalled_string.isascii()):
        raise DeserializationError('marshalled_string is not str')

    if marshalled_string.find('%') > -1:
        ret = urllib.parse.unquote(marshalled_string)
    elif marshalled_string.endswith('s'):
        ret = marshalled_string[:len(marshalled_string) - 1]
    else:
        raise DeserializationError('marshalled_string is invalid')

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    if marshalled_integer is None or type(marshalled_integer) != str or not(marshalled_integer.isascii()) or not(marshalled_integer.startswith('i')):
        raise DeserializationError('marshalled_integer is invalid')
    
    i = marshalled_integer[1:]
    if i.startswith('-'):
        if not(i[1:].isdigit()):
            raise DeserializationError('marshalled_integer is not int')
    elif not(i.isdigit()):
        raise DeserializationError('marshalled_integer is not int')
    ret = int(i)

    return ret

def __validate_key(py_key):
    if py_key is None or type(py_key) != str or not(py_key.isascii()):
        raise DeserializationError('py_key is invalid')
    for c in py_key:
        if not(ord(c) in range(65, 91)) and not(ord(c) in range(97, 123))\
                and ord(c) != 32 and ord(c) != 43 and ord(c) != 45 and ord(c) != 46 and ord(c) != 95:
                    raise DeserializationError('py_key is invalid')
    return py_key

def __validate_value(py_value):
    if py_value is None:
        raise DeserializationError('value is None')
    elif type(py_value) == dict:
        return py_value
    elif type(py_value) == str:
        if py_value.endswith('s') or py_value.find('%') > -1:
            return __unmarshal_string(py_value)
        elif py_value.startswith('i'):
            return __unmarshal_integer(py_value)
    raise DeserializationError('value is invalid')

def __unmarshal_map(marshalled_map):
    ret = {}

    # TODO: Validate and parse using the data-type specific functions
    if marshalled_map is None or type(marshalled_map) != str or not(marshalled_map.isascii()):
        raise DeserializationError('marshalled_map is invalid')
    
    while marshalled_map.startswith(' '):
        marshalled_map = marshalled_map[1:]
    while marshalled_map.endswith(' '):
        marshalled_map = marshalled_map[:len(marshalled_map) - 1]
    
    if not(marshalled_map.startswith('{')) or not(marshalled_map.endswith('}')):
        raise DeserializationError('marshalled_map is invalid')
    elif len(marshalled_map) == 2:
        return ret
    elif len(marshalled_map) < 5 or marshalled_map.find(':') == -1:
        raise DeserializationError('marshalled_map is invalid')
    
    s = ''
    v = ''
    k = ''
    i = 1
    ao = []
    ac = []
    while i < len(marshalled_map) - 1:
        if marshalled_map[i] == '{':
            ao.append(marshalled_map[i])
            if v == '' and k != '':
                s += marshalled_map[i]
            else:
                raise DeserializationError('value is invalid')
        elif marshalled_map[i] == ':':
            if s != '':
                s += marshalled_map[i]
            elif k != '':
                v += marshalled_map[i]
            else:
                k = __validate_key(v)
                v = ''
        elif marshalled_map[i] == ',':
            if s != '':
                s += marshalled_map[i]
            else:
                ret[k] = __validate_value(v)
                v = ''
                k = ''
        elif marshalled_map[i] == '}':
            ac.append(marshalled_map[i])
            if s != '':
                s += marshalled_map[i]
                if len(ao) == len(ac):
                    v = __unmarshal_map(s)
                    s = ''
            ao.pop()
            ac.pop()
        else:
            if s != '':
                s += marshalled_map[i]
            else:
                v += marshalled_map[i]
        i += 1
    
    if k != '' or v != '':
        if k != '' and v != '':
            ret[k] = __validate_value(v)
        else:
            raise DeserializationError('Input is invalid')
    elif len(ao) != 0 or len(ac) != 0:
        raise DeserializationError('Unmatched brackets found')

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    if not(marshalled_state.isascii()):
        raise DeserializationError('Input is not ASCII')
    
    while marshalled_state.startswith(' '):
        marshalled_state = marshalled_state[1:]
    while marshalled_state.endswith(' '):
        marshalled_state = marshalled_state[:len(marshalled_state) - 1]
    
    if not(marshalled_state.startswith('{')) or not(marshalled_state.endswith('}')):
        raise DeserializationError('Input is invalid')

    return __unmarshal_map(marshalled_state)
