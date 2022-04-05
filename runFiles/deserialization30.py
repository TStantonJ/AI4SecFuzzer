from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''

    hasS = 1
    ret = marshalled_string
    
    if ret.find('%2C') >= 0:
        ret = ret.replace('%2C', ',')
        hasS = 0

    if ret.find('%00') >= 0:
        ret = ret.replace('%00', u'\x00')
        hasS = 0

    # Validate and convert
    if hasS == 1:
        ret = ret[0:-1]

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    #Validate and convert
    ret = int(marshalled_integer[1:])

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}

    # Validate and parse using the data-type specific functions
    if marshalled_map[0] != '{' or marshalled_map[-1] != '}':
        raise DeserializationError('Input is not a marshalled string')

    mstr = marshalled_map[1:-1]
    if mstr == '': return ret

    items = mstr.split(',')

    for m1 in items:
        loc = m1.find(':')
        if loc == -1:
            raise DeserializationError('Input is not a marshalled string')

        k = m1[0:loc]
        v = m1[loc+1:]

        if v[0] == 'i' and \
            (v[1:].isdigit()  \
                    or (len(v)>1 and v[1] == '-' and v[2:].isdigit())):
            ret[k] = __unmarshal_integer(v)
        elif v[0] == '{':
            ret[k] = __unmarshal_map(v)
        else:
            ret[k] = __unmarshal_string(v)

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # Validate things about the overall marshalled state
    if len(marshalled_state) < 2 \
        or marshalled_state[0] != '{' or marshalled_state[-1] != '}':
        raise DeserializationError('Input is not a marshalled string')

    return __unmarshal_map(marshalled_state)
