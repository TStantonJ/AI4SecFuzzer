from exceptions import DeserializationError
import string
#import urllib.parse


# sets for validating characters
invalid_simple_chars = set('%,}{')
invalid_complex_chars = set(',}{')
valid_hex_chars = set('0123456789abcdefABCDEF')
ints = set('0123456789')

# allows replacing everything except the ' ' character with strip()
whitespace_without_space = string.whitespace.replace(" ", "")

def __unmarshal_simple_string(marshalled_string):
    ret = ''

    for c in marshalled_string:
        # check if there is an invalid character in the string
        if c in invalid_simple_chars:
            raise DeserializationError('Invalid character: \',\', \'%\', \'{\', and\'}\' must be percent encoded')
        # check if there are non-printable characters in the string
        if not c.isprintable() or not c.isascii():
            raise DeserializationError('Invalid character: non-printable characters must be percent encoded')

    ret = marshalled_string[:-1]

    return ret

def __unmarshal_complex_string(marshalled_complex_string):
    ret = ''
    i = 0

    # shouldn't really get here, but if there happen to be any invalid characters here still, error
    for c in marshalled_complex_string:
        if c in invalid_complex_chars:
            raise DeserializationError('Invalid character: \',\', \'{\', and\'}\' must be percent encoded')
        # check for non-printable characters still in string
        if not c.isprintable():
            raise DeserializationError('Invalid character: non-printable characters must be percent encoded')

    # iterate through complex string
    while i < len(marshalled_complex_string):
        # if there is percent sign, next two digits are hex encoded
        # so decode, add to output string, then skip the two old hex digits
        if marshalled_complex_string[i] == '%':
            x = marshalled_complex_string[i+1:i+3]

            # make sure hex value is a full byte
            if len(x) < 2:
                raise DeserializationError('Invalid character: percent sign must be followed by at least two hex digits')

            # make sure only valid hex digits are being parsed
            for c in x:
                if c not in valid_hex_chars:
                    raise DeserializationError('Invalid character: percent encoded hex values must be between 0-F')
            y = int(x, 16)
            z = chr(y)
            ret += z
            i += 3
        else:
            ret += marshalled_complex_string[i]
            i += 1
        

    # decode percent encoded characters 
    #ret = urllib.parse.unquote(ret)

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    ret = marshalled_integer.lstrip('i')

    # check to make sure if there is '-' in string it is only at the front
    if '-' in ret and ret[0] != '-':
        raise DeserializationError('Invalid character: int type can only contain \'-\' at beginning of number')
    # check to make sure '-' is not the only character in the string
    if '-' in ret and len(ret) < 2:
        raise DeserializationError('Invalid character: int type can only have character \'-\' with at least one number following it')

    # check to make sure string is all valid integer characters
    if ret[0] == '-':
        for c in ret[1:]:
            if c not in ints:
                raise DeserializationError('Invalid character: int type can only contain characters 0-9')
    else:
        for c in ret:
            if c not in ints:
                raise DeserializationError('Invalid character: int type can only contain characters 0-9')

    ret = int(ret)

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    left_bracket = 0
    inside_map = ''

    valid_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
        'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ',
        '-', '_', '+', '.']

    marshalled_map = marshalled_map.strip()

    # make sure input is another valid map, otherwise error
    if marshalled_map[0] == '{' and marshalled_map[-1] == '}':
        inside_map = marshalled_map[1:-1]
    else:
        raise DeserializationError('Invalid braces: Input must be surrounded by {} or there are invalid {} in string')

    # loop to iterate through multiple potential values per map
    while inside_map != '':
        list = inside_map.split(':',1) # split key and remainder on first colon
        key = list[0]
        key = key.strip(whitespace_without_space) # strip any trailing/leading whitespace
        value = list[1]
        inside_map = list[1]

        # if invalid character in key, error
        for c in key:
            if c not in valid_keys:
                raise DeserializationError('Invalid character: Map key value contains invalid character')

        if len(value) < 2:
            raise DeserializationError('Error: Map value cannot be empty')

        # if there is another map or multiple values in map, check to find the end of each value
        if '{' in value or '}' in value or ',' in value:

            for i, c in enumerate(value):
                if c == '{':
                    left_bracket += 1
                elif c == '}':
                    left_bracket -= 1
                elif left_bracket > 0:
                    continue
                elif c == ',' or c == '':
                    value = value[:i]
                else:
                    continue

        inside_map = inside_map.replace(value, '')
        inside_map = inside_map.lstrip(',')

        value = value.strip(whitespace_without_space) # strip any trailing/leading whitespace

        # check if there is another map inside of current one, if so call again
        if '{' in value or '}' in value:
            dict_value = __unmarshal_map(value)
        # if there is %, must be a complex string
        elif '%' in value:
            dict_value = __unmarshal_complex_string(value)
        # if not a complex string, and value ends with 's' the only other option is simple string
        elif value[-1] == 's':
            dict_value = __unmarshal_simple_string(value)
        # if not any other type and the first non-whitespace character is i, must be int
        elif value.strip()[0] == 'i':
            value = "".join(value.split())
            dict_value = __unmarshal_integer(value)
        # if none of these, something is wrong with the input, error
        else:
            raise DeserializationError('Error: Invalid characters in input string or input string is not encoded correctly')
        
        ret[key] = dict_value

    return ret

# function to check if number of braces match
# from https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-python/
def __check(myStr):

    open_list = ["{"]
    close_list = ["}"]

    stack = []
    for i in myStr:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False


def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Error: Input cannot be None')
    if type(marshalled_state) != str:
        raise DeserializationError('Error: Input is not a string')

    # check if number of curly bois match, to see if any invalid maps
    if __check(marshalled_state) is False:
        raise DeserializationError('Error: Input contains uneven number of braces')

    # check if input is empty string
    if marshalled_state == '':
        raise DeserializationError('Error: Input cannot be an empty string')

    # check if there is at least one correct map in input
    if '{' not in marshalled_state:
        raise DeserializationError('Invalid braces: Input must have at least one map enclosed by \'{}\'')
    if '}' not in marshalled_state:
        raise DeserializationError('Invalid braces: Input must have at least one map enclosed by \'{}\'')

    # if the map is not empty, make sure there is a ':' and is long enough for a key-value pair
    if marshalled_state[0] == '{' and marshalled_state[1] != '}':
        if ':' not in marshalled_state or len(marshalled_state) < 5:
            raise DeserializationError('Error: A non-empty map must contain at least one key-value pair')

    # check that map encloses the entire string
    if marshalled_state[0] != '{':
        raise DeserializationError('Invalid braces: Input must start with \'{\' and end with \'}\' to be a valid map')
    if marshalled_state[-1] != '}':
        raise DeserializationError('Invalid braces: Input must start with \'{\' and end with \'}\' to be a valid map')

    return __unmarshal_map(marshalled_state)
