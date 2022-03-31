import urllib.parse
from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):     # COMPLETE FOR NOW
    ret = ''
    if marshalled_string is None:
        raise DeserializationError('Input is None')
    if type(marshalled_string) != str or len(marshalled_string) == 0:
        raise DeserializationError('Invalid input for str unmarshalling')

    # if here, then marshalled_string has at least 1 char
    # possibly a marshalled complex string
    if '%' in marshalled_string:
        if len(marshalled_string) < 3:
            raise DeserializationError('Input is not a marshalled str')
        else:
            i = 0
            while i < len(marshalled_string):
                if marshalled_string[i:i + 1] != '%':
                    ret += marshalled_string[i:i + 1]
                    i += 1
                else:
                    # '%' is last char or only 1 char comes after '%'
                    if i == (len(marshalled_string) - 1) or len(marshalled_string[(i + 1):]) == 1:
                        raise DeserializationError('Input is not a marshalled str')
                    else:
                        charToDecode = marshalled_string[i:(i + 3)]
                        pieceToAdd = urllib.parse.unquote(charToDecode)  # import urllib.parse
                        ret += pieceToAdd
                        i += 3

    # possibly a marshalled simple string
    else:
        if marshalled_string[(len(marshalled_string) - 1):] == 's':
            if len(marshalled_string) == 1:
                ret = ''
            else:
                ret = marshalled_string[0:(len(marshalled_string) - 1)]
        else:
            raise DeserializationError('Input is not a marshalled str')
    return ret

def __unmarshal_integer(marshalled_integer):     # COMPLETE FOR NOW
    ret = 0
    if marshalled_integer is None:
        raise DeserializationError('Input is None')
    if type(marshalled_integer) != str or len(marshalled_integer) == 0:
        raise DeserializationError('Invalid input for int unmarshalling')
    if marshalled_integer[0:1] != 'i':  # Does the input start with 'i'?
        raise DeserializationError('Input is not a marshalled int')
    if len(marshalled_integer) > 1:
        if marshalled_integer[1:2] == '-':
            if len(marshalled_integer) > 2 and marshalled_integer[2:].isnumeric():
                ret = int(marshalled_integer[1:])
            else:
                raise DeserializationError('Input is not a marshalled int')
        elif marshalled_integer[1:2].isnumeric():
            if marshalled_integer[1:].isnumeric():
                ret = int(marshalled_integer[1:])
            else:
                raise DeserializationError('Input is not a marshalled int')
        else:
            raise DeserializationError('Input is not a marshalled int')
    else:
        raise DeserializationError('Input is not a marshalled int')
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    if marshalled_map is None:
        raise DeserializationError('Input is None')
    if type(marshalled_map) != str or len(marshalled_map) == 0 or marshalled_map[0:1] != '{' or marshalled_map[len(marshalled_map) - 1:] != '}':
        raise DeserializationError('Invalid input for map unmarshalling')

    # if here, then input begins w/ '{' and ends w/ '}'
    if marshalled_map == '{}':
        return ret
    # import pdb; pdb.set_trace()
    i = 1
    firstTimeExecutingLoop = True
    while i < len(marshalled_map) and marshalled_map[i:i + 1] != '}':
        if not (firstTimeExecutingLoop):
            i += 1

        # looking for potential key
        potentialKey = ''
        while i < len(marshalled_map) and marshalled_map[i:i + 1] != ':':
            potentialKey += marshalled_map[i:i + 1]
            i += 1

        # no ':' detected after reaching end of input or the immediate next char in input is ':', causing nothing to be added to potentialKey
        if i >= len(marshalled_map) or (potentialKey == '' and marshalled_map[i:i + 1] == ':'):
            raise DeserializationError('Invalid input for map unmarshalling')

        if not (potentialKey.isascii() and potentialKey.isprintable()) or '!' in potentialKey or '\"' in potentialKey or '#' in potentialKey or '$' in potentialKey or '%' in potentialKey or '&' in potentialKey or '\'' in potentialKey or '(' in potentialKey or ')' in potentialKey or '*' in potentialKey or ',' in potentialKey or '/' in potentialKey or ':' in potentialKey or ';' in potentialKey or '<' in potentialKey or '=' in potentialKey or '>' in potentialKey or '?' in potentialKey or '@' in potentialKey or '[' in potentialKey or '\\' in potentialKey or ']' in potentialKey or '^' in potentialKey or '`' in potentialKey or '{' in potentialKey or '|' in potentialKey or '}' in potentialKey or '~' in potentialKey:
            raise DeserializationError('Encountered an invalid key while unmarshalling map')

        keyToAdd = potentialKey
        indexOfColon = i
        i += 1

        # looking for potential value
        potentialValue = ''

        # value might be a map
        if marshalled_map[i:i + 1] == '{':
            counter = 1
            j = i + 1
            while j < len(marshalled_map) and counter != 0:
                if marshalled_map[j:j + 1] == '{':
                    counter += 1
                if marshalled_map[j:j + 1] == '}':
                    counter -= 1
                j += 1
            if counter == 0 and j < len(marshalled_map) and (marshalled_map[j:j + 1] == ',' or marshalled_map[j: j + 1] == '}'):
                potentialValue = marshalled_map[i:j]
                valueToAdd = __unmarshal_map(potentialValue)
                ret[keyToAdd] = valueToAdd
                i = j
            else:
                raise DeserializationError('Invalid input for map unmarshalling')

        # value might be something else besides a map
        else:
            while i < len(marshalled_map) and marshalled_map[i:i + 1] != ',' and marshalled_map[i:i + 1] != '}':
                potentialValue += marshalled_map[i:i + 1]
                i += 1

            # no ',' or '}' detected after reaching end of input or the immediate next char in input is ',' or '}'
            if i >= len(marshalled_map) or (i == indexOfColon + 1 and (marhsalled_map[i:i + 1] == ',' or marhsalled_map[i:i + 1] == '}')):
                raise DeserializationError('Invalid input for map unmarshalling')

            # determine the type of potentialValue
            if ':' in potentialValue or '{' in potentialValue:
                raise DeserializationError('Encountered an invalid value while unmarshalling map')
            elif '%' in potentialValue:
                valueToAdd = __unmarshal_string(potentialValue)
                ret[keyToAdd] = valueToAdd
            elif potentialValue[len(potentialValue) - 1:] == 's':
                valueToAdd = __unmarshal_string(potentialValue)
                ret[keyToAdd] = valueToAdd
            elif potentialValue[0:1] == 'i':
                valueToAdd = __unmarshal_integer(potentialValue)
                ret[keyToAdd] = valueToAdd
            else:
                raise DeserializationError('Encountered an invalid value while unmarshalling map')

        if firstTimeExecutingLoop:
            firstTimeExecutingLoop = False
    if i != len(marshalled_map) - 1:
        raise DeserializationError('Invalid input for map unmarshalling')
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
