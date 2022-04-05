from exceptions import DeserializationError
import urllib.parse

def __unmarshal_string(marshalled_string):
    # If there are no percent encodings, then it is a simple simple string. Only
    # the trailing 's' has to be removed. If there is no s, then raise an error
    # since there is no 's' in a simple string.
    if not "%" in marshalled_string:
        if marshalled_string[-1] != 's':
            raise DeserializationError("Simple string does not end in 's'")
        ret = marshalled_string[:-1]
    else:
        # Unquoting using urllib converts percent encoded strings to UTF-8
        ret = urllib.parse.unquote(marshalled_string)

    return ret

def __unmarshal_integer(marshalled_integer):
    # Removing the leading i
    formatted_marshalled_integer = marshalled_integer[1:]

    if len(formatted_marshalled_integer) == 0:
        raise DeserializationError("Integer value has length of 0")

    # Test if the integer is negative. If it is, then check the length of the number
    # actually following the negative sign and make sure it is not 0. Also check that
    # the number, excluding the negative sign, is a digit so as not to cause runtime
    # errors.
    if formatted_marshalled_integer[0] == "-":
        if len(formatted_marshalled_integer[1:]) == 0 or not formatted_marshalled_integer[1:].isdigit():
            raise DeserializationError("Marshalled integer is not an integer: " + marshalled_integer)

    # Check that the number is a digit before casting it.
    else:
        if not formatted_marshalled_integer.isdigit():
            raise DeserializationError("Marshalled integer is not an integer: " + marshalled_integer)
    ret = int(formatted_marshalled_integer)

    # TODO: Validate and convert

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    # Remove starting and ending braces.
    marshalled_map = marshalled_map[1:-1]
    i = 0
    cur_key = ""
    while i < len(marshalled_map):
        # Loop through the string until you reach the ':' which denotes the end of the key
        if marshalled_map[i] != ":":
            cur_key += marshalled_map[i]
            i += 1

            # If the loop reaches the end of the string without finishing a key, then there
            # is a mismatch in keys and values pairs
            if i == len(marshalled_map):
                raise DeserializationError("Unmatched key and values")

        # When you reach the end of the key
        else:
            # Use to check if if cases are triggered or the int test fails.
            isString = True
            i += 1
            # Check if value is start of a dict
            if marshalled_map[i] == "{":
                isString = False
                start = i
                i += 1
                bracket_count = 1

                # Count ahead in the string until the bracket count balances or the loop
                # reaches the end of the string
                while i < len(marshalled_map) and bracket_count != 0:
                    if marshalled_map[i] == '}':
                        bracket_count -= 1
                    elif marshalled_map[i] == '{':
                        bracket_count += 1
                    i += 1
                if bracket_count != 0:
                    raise DeserializationError('Brackets do not match')

                # Recursively unmarshal the inner map
                ret[cur_key] = __unmarshal_map(marshalled_map[start:i])
                i += 1
                cur_key = ""

            # If the value starts with an i, and all values are digits with the first character
            # having the option of being a negative sign, then marshal it as an int
            elif marshalled_map[i] == "i":
                isString = False;
                start = i
                i += 1
                # Check if first digit is a digit or a negative sign
                if len(marshalled_map) <= i or (not marshalled_map[i].isdigit() and not marshalled_map[i] == '-'):
                    i = start
                    isString = True
                i += 1

                # Count ahead to find length of the int, while checking that each character is a number
                while i < len(marshalled_map) and marshalled_map[i] != "," and marshalled_map[i] != "}":
                    if not marshalled_map[i].isdigit():
                        i = start
                        isString = True
                        break
                    i += 1
                if not isString:
                    ret[cur_key] = __unmarshal_integer(marshalled_map[start:i])
                    i += 1
                    cur_key = ""
            # If no if statements were triggered or the int case failed because a character was not a number,
            # treat the value as a string
            if isString:
                start = i
                while i < len(marshalled_map) and marshalled_map[i] != "," and marshalled_map[i] != "}":
                    i += 1
                ret[cur_key] = __unmarshal_string(marshalled_map[start:i])
                i += 1
                cur_key = ""

    # TODO: Validate and parse using the data-type specific functions

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if len(marshalled_state) == 0:
        raise DeserializationError('Input has a length of 0')
    if not ("{" in marshalled_state and "}" in marshalled_state):
        raise DeserializationError('String does not contain a marshalled dictionary')


    # TODO: Validate things about the overall marshalled state
    marshalled_state = marshalled_state.strip()
    if marshalled_state[0] != "{" or marshalled_state[-1] != "}":
        raise DeserializationError('String does not have a start or end bracket')
    return __unmarshal_map(marshalled_state)
