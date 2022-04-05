from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    
    # TODO: Validate and convert
    if marshalled_string.isprintable():
        #check if input is a simple string without "s" encoding
        #if marshalled_string.isalnum()
            #raise DeserializationError("Marshalled simple strings require s at the end")
        # replace invalid characters with percent encoding
        if '%2C' in marshalled_string:
            ret += marshalled_string.replace('%2C', ',')
        elif '%25' in marshalled_string:
            ret += marshalled_string.replace('%25', '%')
        elif '%00' in marshalled_string:  # nullbyte
            ret += marshalled_string.replace('%00', '\x00')
        else:
            ret += marshalled_string
    else:
        raise DeserializationError("Not deserializable")

    return ret


def __unmarshal_integer(marshalled_integer):
    # TODO: Validate and encode
    if type(marshalled_integer) != int:
        ret = int(marshalled_integer)
    else:
        raise DeserializationError("Input is not an integer")

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    # TODO: Validate and parse using the data-type specific functions

    #empty, return str - ex: (testcase 0)
    if len(list(marshalled_map)) <= 2:
        return ret
    
    #more than 1 key
    elif (marshalled_map.count(':') > 1) and (marshalled_map.count('}') == 1):
        marshalled_map = marshalled_map[1:-1]
        mapList = marshalled_map.split(',')

        for dict in mapList:
            newStr = '{' + dict + '}'
            newDict = __unmarshal_map(newStr)
            ret.update(newDict)

    #more than 1 dict
    elif (marshalled_map.count(':') > 1) and (marshalled_map.count('}') > 1):
        key = marshalled_map[1]
        ret[key] = __unmarshal_map(marshalled_map[3:-1])

    #input: string
    elif marshalled_map[-2] == 's':
        key = marshalled_map[1]
        ret[key] = __unmarshal_string(marshalled_map[3:-2])

    #input: int
    elif marshalled_map[3] == 'i':
        key = marshalled_map[1]
        ret[key] = __unmarshal_integer(marshalled_map[4:-1])

    else:
        key = marshalled_map[1]
        ret[key] = __unmarshal_string(marshalled_map[3:-1])


    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    
    # TODO: Validate things about the overall marshalled state
    if marshalled_state.isspace():
        raise DeserializationError("Input is whitespace")

    mapValidity(marshalled_state)  # check for validity of the marshalled state

    return __unmarshal_map(marshalled_state)
            

def mapValidity(keyStr):
    #all alphanum chars are valid
    if keyStr.isalnum():
        return True

