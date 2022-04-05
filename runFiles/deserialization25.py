from exceptions import DeserializationError
import string

def __unmarshal_string(marshalled_string):
    if not isinstance(marshalled_string, str):
        raise DeserializationError("Trying to deserialize a non-string")
    if not all(c in string.printable for c in marshalled_string):
        raise DeserializationError("Invalid marshalled string")

    #check if the string is simple or complex
    if '%' in marshalled_string:
        return __unmarshal_complex_string(marshalled_string)
    else:
        return __unmarshal_simple_string(marshalled_string)

def __unmarshal_complex_string(complex_marshal):
    ret = ''
    index = 0
    while index < len(complex_marshal):
        if complex_marshal[index] == '%':
            if len(complex_marshal) < index + 3 \
                    or complex_marshal[index + 1] not in string.hexdigits \
                    or complex_marshal[index + 2] not in string.hexdigits:
                raise DeserializationError("Invalid ASCII code in complex string")

            #decode the ASCII character
            code = complex_marshal[index+1:index+3]
            ret = ret + bytes.fromhex(code).decode("ASCII")
            index = index + 2 #skip 2 iterations           

        else:
            #no decoding needed
            ret = ret + complex_marshal[index]
        index = index + 1
    return ret

def __unmarshal_simple_string(simple_marshal):
    if simple_marshal[-1] != 's':
        raise DeserializationError("Deserializing invalid simple string")
    return simple_marshal[:-1]

def __unmarshal_integer(marshalled_integer):
    if not isinstance(marshalled_integer, str):
        raise DeserializationError("Trying to deserialize a non-string")
    return int(marshalled_integer[1:])

def __unmarshal_map(marshalled_map):
    if not isinstance(marshalled_map, str):
        raise DeserializationError("Trying to deserialize a non-string")
    #because hardcoding edge cases is easier than robust validation :D
    if marshalled_map == '':
        raise DeserializationError("Trying to deserialize an empty string")
    if marshalled_map == r'{}':
        return {}

    open_brace = 0
    close_brace = 0
    colons = 0
    commas = 0
    for c in marshalled_map:
        if c == '{':
            open_brace = open_brace + 1
        elif c == '}':
            close_brace = close_brace + 1
        elif c == ':':
            colons = colons + 1
        elif c == ',':
            commas = commas + 1
    # < instead of == because strings can have colons in them
    if open_brace != close_brace or colons - open_brace < commas or colons == 0:
        raise DeserializationError("Invalid map format")

    #Why yes, I do my work in C++, how can you tell?
    ret = {}
    start = 0
    end_of_value = 0
    while end_of_value < len(marshalled_map) - 1:
        colon = marshalled_map.find(':', start)

        #Since commas may actually be inside the next value, we need
        #to make sure our end_of_value marker isn't in a different map
        index = colon
        submap_depth = 0
        end_of_value = len(marshalled_map) - 1
        while index < len(marshalled_map):
            if marshalled_map[index] == '{':
                submap_depth = submap_depth + 1
            elif marshalled_map[index] == '}' and index < len(marshalled_map) - 1:
                submap_depth = submap_depth - 1
                if submap_depth < 0:
                    raise DeserializationError("Invalid map format")
            elif submap_depth == 0 and marshalled_map[index] == ',':
                end_of_value = index
                break
            index = index + 1
        if submap_depth > 0:
            raise DeserializationError("Invalid map format")

        key = marshalled_map[start+1:colon] #everything before the colon
        if not all(c in (string.ascii_letters + string.digits + ' -_+.') for c in key):
            #invalid character in the key
            raise DeserializationError("Invalid key")

        value = marshalled_map[colon+1:end_of_value] #everything after the colon
        ret[key] = __unmarshal_dispatch(value) #deserialize the value

        start = end_of_value #prepare for the next iteration

    return ret

def __unmarshal_dispatch(value):
    if value[0] == '{' and value[-1] == '}':
        return __unmarshal_map(value)
    elif '%' not in value and value[-1] != 's':
        return __unmarshal_integer(value)
    elif '%' in value or value[-1] == 's':
        return __unmarshal_string(value)
    else:
        raise DeserializationError("Can't determine encoded type")


def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    return __unmarshal_map(marshalled_state)
