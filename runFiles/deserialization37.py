import urllib.parse

from exceptions import DeserializationError

valid_characters = [' ', '-', '_', '+', '.']
invalid_characters = ['%', ',', '%2C', '{', '}']

def __unmarshal_string(is_simple, marshalled_string):
    if is_simple:
        if marshalled_string[-1] != 's':
            raise DeserializationError('Simple strings must end with "s"')
        return marshalled_string[:-1]
    else:
        ret = urllib.parse.unquote(marshalled_string)
        return ret

def __unmarshal_integer(marshalled_integer):

    return int(marshalled_integer[1:])

def __unmarshal_map(marshalled_map):
    ret = {}

    if marshalled_map == '{}':
        return ret

    if marshalled_map[0] != '{':
        raise  DeserializationError('Marshalled map must begin with "{"')

    key_value_string = ''
    current_bracket_level = 0
    for i, character in enumerate(marshalled_map):
        if character == '{':
            current_bracket_level += 1
            if i == 0:
                continue
        if character == '}':
            current_bracket_level -= 1

        if (character == ',' and current_bracket_level == 1) or (character == '}' and current_bracket_level == 0):
            split_key_value = key_value_string.split(':', 1)

            if len(split_key_value) == 1:
                raise DeserializationError('Nosj dicts must take the form {key:value}')

            key = split_key_value[0]
            value = split_key_value[1]
            if is_valid_key(key):
                ret[key] = determine_value(value)
            key_value_string = ''
            continue
        if current_bracket_level > 0:
            key_value_string += character

    if current_bracket_level != 0:
        raise DeserializationError('Mismatched brackets in nosj string : ' + marshalled_map)


    return ret

def is_valid_key(key):
    if key is None:
        raise DeserializationError('Key is None')
    if not key:
        raise DeserializationError('An empty key was provided')

    for character in key:
        ascii_value = ord(character)
        if ord('a') <= ascii_value <= ord('z'):
            continue
        if ord('A') <= ascii_value <= ord('Z'):
            continue
        if ord('1') <= ascii_value <= ord('9'):
            continue
        if character in valid_characters:
            continue

        raise DeserializationError('The key ' + key + ' is not valid')
    return True


def determine_value(value):
    is_integer = True
    is_simple_string = True
    is_complex_string = True

    if value is None:
        raise DeserializationError('A None value was provided')

    if not value:
        raise DeserializationError('An empty value was provided. Valid values are str, int, or map')

    if value[0] == '{' and value[-1] == '}':
        return __unmarshal_map(value)

    for i, character in enumerate(value):
        if i == 0:
            if character  != 'i':
                is_integer = False
        if is_integer and i == 1 and not (ord('1') <= ord(character) <= ord('9') or character == '-'):
            is_integer = False
        if character in invalid_characters:
            is_simple_string = False

    if is_integer:
        return __unmarshal_integer(value)
    elif is_simple_string:
        return __unmarshal_string(True, value)
    elif is_complex_string:
        return __unmarshal_string(False, value)


def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if not marshalled_state:
        raise DeserializationError('Input string is empty')

    if marshalled_state[0] != '{' and marshalled_state[-1] != '}':
        raise DeserializationError('Marshalled map must begin with "{" and end with "}"')

    return __unmarshal_map(marshalled_state)
