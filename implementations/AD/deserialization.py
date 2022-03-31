from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    
    if (not marshalled_string.isprintable()):
        raise DeserializationError('String contains nonprintable characters')

    # TODO: Validate and convert
    if (marshalled_string[-1] == "s"):
        marshalled_string = marshalled_string[:-1]

    while ("%" in marshalled_string):
        charIndex = marshalled_string.find("%")
        hexCode = marshalled_string[charIndex+1:charIndex+3]
        tempByte = bytes.fromhex(hexCode)
        asciiChar = tempByte.decode("ASCII")
        marshalled_string = marshalled_string[:charIndex]+asciiChar+marshalled_string[charIndex+3:]

    ret = marshalled_string
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert

    ret = marshalled_integer[1:]
    ret = int(ret)
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    multEntries = False
    marshalled_map = marshalled_map[1:-1]
    # TODO: Validate and parse using the data-type specific functions
    colIndex = marshalled_map.find(":")

    key = marshalled_map[:colIndex]
    value = marshalled_map[colIndex+1:]

    bannedChars = "!@#$%^&*(),<>/"
    for char in key:
        if char in bannedChars:
            raise DeserializationError('Invalid symbol in Dictionary Key')
    
    if not value:
        return ret

    if ("," in value):
        multEntries = True
        endIndex = value.find(",")
        remaining = value[endIndex+1:]
        value = value[:endIndex]

    if (":" in value):
        value = __unmarshal_map(value)
    elif (value[0] == "i"):
        value = __unmarshal_integer(value)
    elif ("%" in value or value[-1] == "s"):
        value = __unmarshal_string(value)
    else:
        raise DeserializationError("Value not recognized in Map")

    if key:
        ret[key] = value

    if multEntries:
        remaining = "{" + remaining + "}"
        otherDict = __unmarshal_map(remaining)
        ret.update(otherDict)
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    if marshalled_state == "":
        raise DeserializationError('Empty')

    if "{" in marshalled_state:
        if not "}" in marshalled_state:
            raise DeserializationError('Incomplete Dictionary')

        elif not ":" in marshalled_state and len(marshalled_state) > 2:
            raise DeserializationError('Dictionary Missing Value')

    if "[" in marshalled_state:
        if not "]" in marshalled_state:
            raise DeserializationError('Missing Matching Bracket')
        elif len(marshalled_state) == 2:
            raise DeserializationError('Empty List')

    return __unmarshal_map(marshalled_state)
