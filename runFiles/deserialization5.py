from exceptions import DeserializationError
import string

VALID_KEY = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '-', '_', '+', '.']

SIMPLE_INVALID_CHARS = ['%', ',', '{', '}']
COMPLEX_INVALID_CHARS = [',', '{', '}']

# Determines if a string is a valid nsoj int
def is_int(test_int):
    if len(test_int) < 2:
        return False

    if test_int[0] != 'i':
        return False

    test_int = "".join(test_int.split())

    if test_int[1] == '-':
        if len(test_int) < 3:
            return False

    if not(test_int[1] == '-' or test_int[1].isnumeric()):
        return False

    for c in test_int[2:]:
        if not c.isnumeric():
            return False

    return True

# Determines if a string is a simple nsoj string
# Simple strings may contain only printable ascii, minus the given
# invalid characters.
def is_simple_ascii(s):
    for c in s:
        if c in SIMPLE_INVALID_CHARS:
            return False
        if not (c.isascii() and c.isprintable()):
            return False

    return True

# Convert nsoj strings to python strings
def __unmarshal_string(marshalled_string):
    ret = ''

    mar_string = str(marshalled_string)

    # Simple string
    if mar_string[-1] == 's' and is_simple_ascii(mar_string):
        if len(mar_string[:-1]) < 1:
            raise DeserializationError('Simple string should not be empty')
        if not is_simple_ascii(mar_string):
            raise DeserializationError('Simple string contains invalid characters')
        else:
            # Remove trailing s
            ret += mar_string[:-1]

    # Complex string
    else:
        if '%' not in mar_string:
            raise DeserializationError('Complex string does not contain atleast one percent-encoded representation')
        else:
            # Validate complex string
            i = 0
            while i < len(mar_string):
                if mar_string[i] in COMPLEX_INVALID_CHARS:
                    raise DeserializationError('Complex string contains restricted characters')
                if mar_string[i] == '%':
                    if i > len(mar_string) - 3:
                        raise DeserializationError('Complex strings must have two hex characters after percent sign')

                    hex_chars = mar_string[i+1] + mar_string[i+2]

                    if not(all(c in string.hexdigits for c in hex_chars)):
                        raise DeserializationError('Percent encoded characters are not valid hex digits')

                    hex_value = int(hex_chars, 16)
                    ret += chr(hex_value)
                    i += 3
                elif is_simple_ascii(mar_string[i]):
                    ret += mar_string[i]
                    i += 1
                else:
                    raise DeserializationError('Complex string contains non-printable or restricted ascii chacracters that are not percent encoded')

    return ret

# Convert nsoj int to python int
def __unmarshal_integer(marshalled_integer):
    ret = 0

    mar_int = str(marshalled_integer)
    mar_int = "".join(mar_int.split())
    # Remove 'i' and convert
    ret = int(mar_int[1:])

    return ret

# Converts a nsoj map to a python dictionary
# The general strategy is to parse the nosj string left to right
# and remove the key value pairs as they are processed.
def __unmarshal_map(marshalled_map):
    ret = {}

    mar_map = marshalled_map.strip()

    # Map has a minimum lenght of two {}
    if len(mar_map) < 2:
        raise DeserializationError('Map must contain atleast 2 characters')

    # Map must be wrapped in braces
    if not(mar_map[0] == '{' and mar_map[-1] == '}'):
        raise DeserializationError('Map is not warppped with braces')

    # Remove braces
    mar_map = mar_map[1:-1]

    if mar_map != '':

        # Detect trailing comma
        if mar_map[-1] == ',':
            raise DeserializationError('Map has a trailing comma')

        while len(mar_map.strip()) > 0:

            colon_index = mar_map.find(':')
            if colon_index == -1:
                raise DeserializationError('Map key and value not sperated by colon')

            # Carve out key
            key = mar_map[:colon_index].strip('\t\n\v\f\r')
            if len(key) < 1:
                raise DeserializationError('Map key value is empty')

            # Validate key
            for c in str(key):
                    if c not in VALID_KEY:
                        raise DeserializationError('Map key contains invalid characters')

            # Remove processed key
            mar_map = mar_map[colon_index+1:]

            # Check for nested map
            if mar_map.strip()[0] == '{':
                # Find end of map
                # Valid maps will always end with a }
                # The last } will either be followed by a comma
                # or at the end of the nsoj string
                map_end_index = mar_map.find('},')
                if map_end_index != -1:
                    # Carve out value
                    value = mar_map[:map_end_index+1]
                    # Remove proccessed value
                    mar_map = mar_map[map_end_index+2:]
                else:
                    # Find last } in nosj string
                    map_end_index = mar_map.rfind('}')
                    if map_end_index != -1:
                        # Carve out value
                        value = mar_map[:map_end_index+1]
                        # Remove proccessed value
                        mar_map = mar_map[map_end_index+1:]
                    else:
                        raise DeserializationError('Map is not wrapped with braces')

                ret[key] = __unmarshal_map(value)

            # Check for string or int
            else:
                # A comma indicates the end of a value
                comma_index = mar_map.find(',')

                if comma_index != -1:
                    # Carve out value
                    value = mar_map[:comma_index]
                    # Remove proccessed value
                    mar_map = mar_map[comma_index+1:]

                # If no comma is present, then it is assumed that the
                # value goes to the end of the map
                else:
                    # Carve out value
                    value = mar_map
                    # Remove proccessed value
                    mar_map = ''
                if len(value.strip()) < 2:
                    raise DeserializationError('Map value must be at least 2 characters')
                if is_int(value.strip()):
                    ret[key] = __unmarshal_integer(value.strip())
                else:
                    ret[key] = __unmarshal_string(value.strip('\t\n\v\f\r'))

    return ret

# Public function to accept nsoj string
def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    return __unmarshal_map(marshalled_state)
