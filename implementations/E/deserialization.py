from exceptions import DeserializationError

# marshalled_string: a complex string that contains an encoded '%##' character, or
#                    a simple string terminated by the character 's'.
#           returns: a decoded string
def __unmarshal_string(marshalled_string):
    ret = ''
    i = 0
    length = len(marshalled_string)
    
    if marshalled_string.find('%') != -1:
        while i < length:
            if marshalled_string[i] != '%':
                ret += marshalled_string[i]
            else:
                if marshalled_string[i:i+3] == '%00':
                    ret += '\x00'
                elif marshalled_string[i:i+3] == '%25':
                    ret += '%'
                elif marshalled_string[i:i+3] == '%2C':
                    ret += ','
                elif marshalled_string[i:i+3] == '%7B':
                    ret += '{'
                elif marshalled_string[i:i+3] == '%7D':
                    ret += '}'
                else:
                    raise DeserializationError('Invalid encoded character')
                i += 2
            i += 1
    else:
        ret = marshalled_string[:-1]

    return ret

# marshalled_integer: a positive or negative integer encoded as a string and
#                     prefixed by the character 'i' at index [0]
#            returns: a positive or negative integer
def __unmarshal_integer(marshalled_integer):
    ret = 0
    
    # marshalled_integer[0] is i by default
    if len(marshalled_integer) < 2:
        raise DeserializationError('Missing integer')
    elif marshalled_integer[1] == '-':
        if marshalled_integer[2:].isdigit():
            ret = int(marshalled_integer[1:])
        else:
            raise DeserializationError('Invalid negative integer')
    elif marshalled_integer[1:].isdigit():
        ret = int(marshalled_integer[1:])
    else:
        raise DeserializationError('Invalid integer')

    return ret

# marshalled_map: a dict encoded as a string.
#                 can be empty or contain a string, an integer, or another dict.
#        returns: a dict
def __unmarshal_map(marshalled_map):
    ret = {}
    length = len(marshalled_map)
    i = 1
    end = -1
    end2= -1
    key = ''
    value = None

    if length < 1:
        raise DeserializationError('Missing input')
    elif not __validate_brackets(marshalled_map):
        raise   DeserializationError('Unbalanced brackets')
    elif marshalled_map[0] == '{' and marshalled_map[1] == '}':
        pass
    elif marshalled_map[0] == '{':
        while i > 0 and i < length:
            # Get key
            end = i + marshalled_map[i:].find(':')
            if end < i+1:
                raise DeserializationError('Missing key')
            elif not all(x.isalnum() \
                    or x == ' ' \
                    or x == '-' \
                    or x == '_' \
                    or x == '+' \
                    or x == '.' for x in marshalled_map[i:end-1]):
                raise DeserializationError('Invalid key')
            else:
                key = marshalled_map[i:end]
            i = end + 1
            if i >= length:
                raise DeserializationError('Missing value')
                
            # If map, find matching bracket and start recursion
            if marshalled_map[i] == '{':
                end = i + __match_brackets(marshalled_map[i:])
                if end < i:
                    raise DeserializationError('Unbalanced brackets in map')
                else:
                    value = __unmarshal_map(marshalled_map[i:end+1])
                i = end + 1
            else:          
                # Find closest delimiter after string or int
                end = i + marshalled_map[i:].find(',')
                end2 = i + marshalled_map[i:].find('}')
                if end > i and end2 > i:
                    end = min(end, end2)
                elif end2 > i:
                    end = end2
                    
                # Get string/int value
                if end < i:
                    raise DeserializationError('Missing closing bracket')
                elif marshalled_map[i:end].find('%') > -1:
                    value = __unmarshal_string(marshalled_map[i:end])
                elif marshalled_map[end-1] == 's':
                    value = __unmarshal_string(marshalled_map[i:end])
                elif marshalled_map[i] == 'i':
                    value = __unmarshal_integer(marshalled_map[i:end])
                else:
                    raise DeserializationError('Invalid data type')
                    break
                i = end
                
            # if comma after value, find next key/value pair
            if i < length:
                if marshalled_map[i] != ',':
                    i = length
                else:
                    i += 1
        
            ret[key] = value

    return ret

# marshalled_state: a dict encoded as a nosj string
#          returns: a dict
def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    if len(marshalled_state) < 1:
        raise DeserializationError('Missing marshalled_State')
    if marshalled_state[0] != '{':
        raise DeserializationError('Missing brackets')
    if not __validate_brackets(marshalled_state):
        raise DeserializationError('Unbalanced brackets')

    return __unmarshal_map(marshalled_state)

#  string: a string with an open bracket '{' at index [0]
# returns: True  if the string contains fully balanced brackets
#          False if the string does not contain balanced brackets
def __validate_brackets(string):
    ret = True
    counter = 0
    
    for character in string:
        if character == '}':
            counter -= 1
            if counter < 0:
                ret = False
                break
        elif character == '{':
            counter += 1
    if counter != 0:
        ret = False
        
    return ret

#  string: a string with an open bracket '{' at index [0]
# returns: the index of the corresponding closing bracket
def __match_brackets(string):
    ret = -1
    counter = 0
    index = 0
    
    if string[index] == '{':
        for character in string:
            if character == '{':
                counter += 1
            elif character == '}':
                counter -= 1
            if counter == 0:
                ret = index
                break
            index += 1
                
    return ret