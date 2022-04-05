from exceptions import DeserializationError
from urllib.parse import unquote
#from serialization import allowed_keychar
from string import printable

def __unmarshal_string(marshalled_string):

    ret = ''
    disallowed_complex = '!"#$&\'()*+,:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c\x00'

    if type(marshalled_string) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_string))
    elif not marshalled_string:
        raise DeserializationError("Input cannot be empty string")
    elif '%' in marshalled_string:
        # If any of disallowed appear in the marshalled complex string,
        # it must be incorrectly marshalled

        allowed_percentencode = '0123456789abcdefABCDEF'

        if len(marshalled_string) < 3:
            raise DeserializationError('Complex string must contain percent encoded representation')

        for index, character in enumerate(marshalled_string):
            if character in disallowed_complex:
                raise DeserializationError('String input is marshalled incorrectly')
            elif character == '%':
                # Has to be at least 3 characters for percent representation
                if (len(marshalled_string) - index) < 3:
                    raise DeserializationError('String input is marshalled incorrectly')

                # Validate Complex string
                elif marshalled_string[index + 1] not in allowed_percentencode:
                    raise DeserializationError('String input is marshalled incorrectly')
                elif marshalled_string[index + 2] not in allowed_percentencode:
                    raise DeserializationError('String input is marshalled incorrectly')
                else:
                    ret += unquote(marshalled_string)

    elif marshalled_string[-1] == 's':

        allowed_simple = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$&\'()*+-./:;<=>?@[\\]^_`|~ \t\n\r\x0b\x0c'

        for character in marshalled_string:
            if character not in allowed_simple:
                raise DeserializationError('String input is marshalled incorrectly')
        ret += marshalled_string[:-1]
    else:
        raise DeserializationError("Input is malformed string")

    return ret

def __unmarshal_key(marshalled_key):
    if type(marshalled_key) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_key))
    elif not marshalled_key:
        raise DeserializationError("Input cannot be empty string")

    for index, character in enumerate(marshalled_key):
        if character not in allowed_keychar:
            raise DeserializationError('Illegal character in map key value')

    return marshalled_key

def __unmarshal_value(marshalled_value):
    if type(marshalled_value) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_value))
    elif not marshalled_value:
        raise DeserializationError("Input cannot be empty string")

    elif not bool(__remove_whitespace(marshalled_value)):
        raise DeserializationError("Input value not recognized")

    val_nowhitespace = __remove_whitespace(marshalled_value)

    if '{' in marshalled_value:
        return __ranoutoftime_unmarshalmap(marshalled_value)
    elif '%' in marshalled_value:
        return __unmarshal_string(marshalled_value)
    elif bool(__remove_whitespace(marshalled_value)) and val_nowhitespace[-1] == 's':
        return __unmarshal_string(marshalled_value)
    elif bool(__remove_whitespace(marshalled_value)) and val_nowhitespace[0] == 'i':
        return __unmarshal_integer(marshalled_value)
    else:
        raise DeserializationError("Input value not recognized")

def __unmarshal_integer(marshalled_integer):
    ret = 0
    
    # Ignore whitespace
    marshalled_integer = marshalled_integer.replace(" ", "")

    if type(marshalled_integer) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_integer))
    elif len(marshalled_integer) < 2:
        raise DeserializationError("Input is malformed integer")

    elif marshalled_integer[:1] == 'i':
        
        if marshalled_integer[:2] == 'i-' and len(marshalled_integer) > 2 and marshalled_integer[2:].isdecimal():
            ret = int(marshalled_integer[1:])

        elif marshalled_integer[1:].isdecimal():
            ret = int(marshalled_integer[1:])
        else:
            raise DeserializationError("Input is malformed integer")
    else:
        raise DeserializationError("Input is malformed integer")

    return ret


def __ranoutoftime_unmarshalmap(marshalled_map):
    if type(marshalled_map) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_map))
    elif not marshalled_map:
        raise DeserializationError('Input cannot be empty string')

    no_whitespace = __remove_whitespace(marshalled_map)

    if no_whitespace == '{}':
        return {}

    elif ':' not in marshalled_map:
        raise DeserializationError('Input is malformed map')

    num_open = 0
    num_closed = 0

    for character in marshalled_map:
        if character == '{':
            num_open += 1
        elif character == '}':
            num_closed += 1

    # Weak validation
    if num_open != num_closed:
        raise DeserializationError('Input is malformed map')

    # Handle no comma case
    elif ',' not in marshalled_map:

        if ':{' in __remove_whitespace(marshalled_map):
            key = __unmarshal_key(marshalled_map[1:].split(':')[0])

            value_b4 = marshalled_map[1:].split(':')[1]
            print('Marshalledmap: ' + marshalled_map[1:])

            for index, character in enumerate(value_b4):
                if character == '}':
                    value_b4 = value_b4[:index]

            print('Valueb4: ' + value_b4)
            value = __unmarshal_value(value_b4)
        else:
            key = __unmarshal_key(marshalled_map[1:(len(marshalled_map) - 1)].split(':')[0])
            value = __unmarshal_value(marshalled_map[1:(len(marshalled_map) - 1)].split(':')[1])
            return {key:value}

    # Comma case
    else:
        ret = {}
        comma_count = 0

        for character in marshalled_map:
            if character == ',':
                comma_count += 1

        no_comma = marshalled_map.split(',')

        for location, split_str in enumerate(no_comma):
                if ':' not in split_str:
                    if __remove_whitespace(split_str) == '{}':
                        raise DeserializationError('')
                
                ind = -1

                for index, character in enumerate(split_str):
                    if character == '{':
                        ind = index

                # Doesnt have open brace
                if not (ind == -1):
                    key = __unmarshal_key(split_str[(ind + 1):].split(':')[0])
                    val_str = no_comma[location].split(':')[1]
                    loc_closes = []

                    for i, character in enumerate(val_str):
                        if character == '}':
                            loc_closes.append(i)

                    if len(loc_closes) == 0:
                        value = __unmarshal_value(val_str)
                        ret[key] = value
                    else:
                        var = loc_closes.pop()
                        value = __unmarshal_value(val_str[:var])
                        ret[key] = value
                # Has open brace
                else:
                    key = __unmarshal_key(split_str.split(':')[0])
                    end_index = -1

                    if bool(split_str.split(':')[1]):
                        split_value = split_str.split(':')[1]
                        for k, character in enumerate(split_value):
                        # check if bracket at end,
                            if character == "}":
                                split_value = split_value[:k]

                        value = __unmarshal_value(split_value)
                        ret[key] = value

                    else:
                        raise DeserializationError("Found empty key value")       
        return ret

# Tried to implement bracket matching, unsuccessfully
def __unmarshal_map(marshalled_map):
    if type(marshalled_map) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_map))
    elif not marshalled_map:
        raise DeserializationError('Input cannot be empty string')
    
    bracket_stack = []
    ret = {}
    open_indexes = []
    close_indexes = []

    num_open = 0
    num_closed = 0

    for character in marshalled_map:
        if character == '{':
            num_open += 1
        elif character == '}':
            num_closed += 1

    # Weak validation
    if num_open != num_closed:
        raise DeserializationError('Input is malformed map')

    for index, character in enumerate(marshalled_map):
        if character == '{':
            bracket_stack.append(character)
            indexes.append(index + 1)

        elif character == '}':
            check = bracket_stack.pop()
            start = indexes.pop()

            if bool(check):
                nobrace = marshalled_map[start:index - 1]

                if not nobrace:
                    return ret

                keyvalue = __unmarshal_key(nobrace.split(':')[0])

                colon_count = 0

                for index, character in enumerate(nobrace):
                    if character == ':':
                        colon_count += 1
                    elif (colon_count == 0) and (index + 1) == len(nobrace):
                        a = 1
            else:
                raise DeserializationError('Input is malformed map')

        if (index + 1) == len(marshalled_map):
            raise DeserializationError('Input is malformed map')
    ret = {}
    # TODO: Validate and parse using the data-type specific functions
    return ret


def unmarshal(marshalled_state):
    if type(marshalled_state) is not str:
        raise DeserializationError(__debug_helper(str, marshalled_state))

    return __ranoutoftime_unmarshalmap(marshalled_state)


# Generate debug string with expected type, found type
def __debug_helper(expected_type, found):
    
    ret = '*** Expected '

    if expected_type is dict:
        ret += 'dict'
    elif expected_type is int:
        ret += 'integer'
    elif expected_type is str:
        ret += 'string'

    ret += ', instead found: ' + str(type(found)) + ' ***'
    return ret

def __confirm_one_openbrace(keystr_in):
    if not keystr_in:
        raise DeserializationError('')
    open_count = 0

    for character in keystr_in:
        if character == '{':
            open_count += 1
    return open_count <= 1

def __remove_whitespace(str_in):
    if not str_in:
        raise DeserializationError('Map is formatted incorrectly')

    ret = str_in

    for character in ' \t\n\r\x0b\x0c':
        ret = ret.replace(character, '')

    return ret