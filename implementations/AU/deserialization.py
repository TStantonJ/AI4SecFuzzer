from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = marshalled_string

    if '%2C' in ret or '%00' in ret:
        # do escape
        ret = ret.replace('%2C', ',')
        ret = ret.replace('%00', u'\x00')
        return ret
    elif ret[-1] == 's':
        # remove tail s
        return ret[0:-1]

def __unmarshal_integer(marshalled_integer):
    # parse int
    ret = ''
    try:
        ret = int(marshalled_integer)
    except:
        raise DeserializationError('Not a valid int')

    return ret

def __unmarshal_value(val):
    if val[0] == 'i':
        return __unmarshal_integer(val[1:])
    elif val[0] == '{':
        # sub-dict
        return __unmarshal_map(val)
    else:
        return __unmarshal_string(val)

def __unmarshal_map(marshalled_map):
    ret = {}

    # check { and }
    if marshalled_map == '' or marshalled_map[0] != '{' or marshalled_map[-1] != '}':
        raise DeserializationError('Not a marshalled {}')

    # null string
    if marshalled_map == "{}": return ret

    # multi-marshalled string
    mar_strs = marshalled_map[1:-1].split(',')

    for one_ms in mar_strs:
        if ':' not in one_ms: 
            raise DeserializationError('Not a dict string')

        pos = one_ms.find(':')
        key = one_ms[0:pos]
        val = one_ms[pos+1:]
        # add one key-value
        ret[key] = __unmarshal_value(val)

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    return __unmarshal_map(marshalled_state)
