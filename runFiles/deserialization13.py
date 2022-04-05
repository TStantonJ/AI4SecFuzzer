from exceptions import DeserializationError
import urllib.parse
import string
key_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_+."
py_dict = {}

def __unmarshal_string(marshalled_string):
    ret = ''

    # check if simple string
    if marshalled_string.find('%') != -1:
        return urllib.parse.unquote(marshalled_string)
        
    elif marshalled_string.endswith('s') == 1 and marshalled_string.find(',') == -1 and marshalled_string.find('{') == -1 and marshalled_string.find('}') == -1:
        return marshalled_string[:-1]

    else:
        raise DeserializationError('Input is not a string')


def __unmarshal_integer(marshalled_integer):
    ret = ""
    if type(marshalled_integer) != str: # make sure it is a string
        raise DeserializationError('Input is not a string')

    # TODO: Validate and convert
    marshalled_integer = marshalled_integer[1:]
    if marshalled_integer[0] == '-': # take of minus sight before isnumeric check
        ret += "-"
        marshalled_integer = marshalled_integer[1:]
    if marshalled_integer.isnumeric(): # check if numeric
        ret += marshalled_integer
    else:
        raise SerializationError('Input is not a string')

    return int(ret) # make sure this works with a negative


def __unmarshal_map(marshalled_map):
    if len(marshalled_map) == 0 or marshalled_map == '' or marshalled_map == None:
        raise DeserializationError('Input is None')

    if marshalled_map[0] != '{' or marshalled_map[-1] != '}':
        raise DeserializationError('Input is not a string')

    marshalled_map = marshalled_map[1:-1] # get rid of end brackets
    colon = 0
    vStart = 0
    vEnd = -2
    kStart = 0
    kEnd = 0
    bTest = 0
    global py_dict

    while vEnd != len(marshalled_map)-1:
        colon = marshalled_map.find(':', colon + 1)
        if colon != -1:
            while marshalled_map[vEnd+2] == '}' or marshalled_map[vEnd+2] == ',':
                vEnd += 1
        kStart = vEnd + 2
        kEnd = colon - 1
        vStart = colon + 1
        vEnd = colon
        # create key
        key = marshalled_map[kStart:kEnd+1]
        # now convert found value
        if marshalled_map[vStart] == '{': # map test
            vEnd = marshalled_map.find('}',vStart)
            bTest = marshalled_map.find('{',vStart+1)
            while bTest < vEnd and bTest != -1:
                vEnd = marshalled_map.find('}',vEnd+1)
                bTest = marshalled_map.find('{',bTest+1)

            value = marshalled_map[vStart:vEnd + 1]
            __unmarshal_map(marshalled_map[vStart:vEnd + 1])
            py_dict[key] = value
            colon = vEnd
            continue

        if vEnd == -2: # needed for next if statement
            vEnd = 0
        if marshalled_map.find(',',vEnd) == - 1:
            vEnd = len(marshalled_map) - 1
        else:
            vEnd = marshalled_map.find(',',vEnd + 2) - 1

        if vEnd == len(marshalled_map) - 1:
            if marshalled_map[vStart] == 'i' and marshalled_map[vStart+1:].isnumeric() and '.' not in marshalled_map[vStart:] or marshalled_map[vStart] == 'i' and marshalled_map[vStart+1:vStart+2] == '-' and marshalled_map[vStart+2:].isnumeric() and '.' not in marshalled_map[vStart:]:
                value = __unmarshal_integer(marshalled_map[vStart:])
            else:
                value = __unmarshal_string(marshalled_map[vStart:])
        else:
            if marshalled_map[vStart] == 'i' and marshalled_map[vStart+1:vEnd+1].isnumeric() and '.' not in marshalled_map[vStart+1:vEnd+1] or marshalled_map[vStart] == 'i' and marshalled_map[vStart+1:vStart+2] == '-' and marshalled_map[vStart+2:vEnd+1].isnumeric() and '.' not in marshalled_map[vStart+2:vEnd+1]:
                value = __unmarshal_integer(marshalled_map[vStart:vEnd+1])
            else:
                value = __unmarshal_string(marshalled_map[vStart:vEnd+1])

        py_dict[key] = value

    return py_dict
            
def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    
    return __unmarshal_map(marshalled_state)
