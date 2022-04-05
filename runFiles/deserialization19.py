from exceptions import DeserializationError
import urllib

def __unmarshal_string(marshalled_string):
    ret = ''

    if not marshalled_string.find('%') == -1: #if the string contains a % it is a complext string
        ret += urllib.parse.unquote(marshalled_string)
    elif marshalled_string[-1] == 's':    #determines if its a simple string
        ret += marshalled_string[:-1]
    else:   #if the string is not percent encoded or ending with an s it is invalid
        raise DeserializationError('Input string is not valid')

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    if marshalled_integer[0] != 'i':
        raise DeserializationError('Input string for int is not valid')
    if marshalled_integer[1] == '-':
        ret -= int(marshalled_integer[2:])
    else:
        ret += int(marshalled_integer[1:])

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}

    if marshalled_map == '{}':
        return ret
    
    pairs = marshalled_map[1:-1].split(',') #splits the input string into pairs of keys and values
    for x in pairs:
        parameters = x.split(':' , 1)   #for each pair split at the ':' to determine the key and the value
        key = parameters[0]
        if key[0] == '{':   #removes the beginning bracket of the string
            key = key[1:]
        value = parameters[1]
        if value[0] == 'i':
            ret[key] = __unmarshal_integer(value)
        elif value[0] == '{':
            ret[key] = __unmarshal_map(value) 
        else:
            ret[key] = __unmarshal_string(value)




    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if len(marshalled_state) == 0:
        raise DeserializationError('Input has a lenght of 0')
    if (marshalled_state[0] != "{") or (marshalled_state[-1] != '}'):
        raise DeserializationError('Input is missing a bracket') 
    if len(marshalled_state) > 2:   #checks if the string contains a ':' indicating a key and a value
        y = 0
        for x in marshalled_state:
            if x == ':':
                y = 1
        if y == 0:
            raise DeserializationError('Input does not contain a key and a value')

    return __unmarshal_map(marshalled_state)
