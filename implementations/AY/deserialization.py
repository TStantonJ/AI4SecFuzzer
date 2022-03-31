from exceptions import DeserializationError
import urllib.parse

def __unmarshal_string(marshalled_string):
    ret = ''
    simpleStringValidCharacters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"#$&'()*+-./:;<=>?@[\\]^_`|~ "
    isSimpleString = False
    isPercentEncoded = False
    invalidCharacters = "\t\n\r"
    # TODO: Validate and convert
    for character in marshalled_string:
        if character in invalidCharacters:
            raise DeserializationError("Invalid character: non-percent encoded character detected")
        if character in simpleStringValidCharacters:
            isSimpleString = True
        else:
            isSimpleString = False
            break

    if isSimpleString:
        if marshalled_string[-1] == 's':
            ret = marshalled_string[:-1]
        else:
            raise DeserializationError("Invalid string encoding, missing trailing encoded character")
    else:
        # complex string processing, checking for percent character
        for character in marshalled_string:
            if character == '%':
                isPercentEncoded = True
        
        if '{' in marshalled_string or '}' in marshalled_string or ',' in marshalled_string:
            raise DeserializationError("Detected character not encoded properly")
                
        
        if isPercentEncoded:
            stringLength = len(marshalled_string)
            index = 0
            while index < stringLength:
                character = marshalled_string[index]
                if character == '%' and index <= (stringLength - 3):
                    encodedCharacter = marshalled_string[index:index+3]
                    ret += urllib.parse.unquote(encodedCharacter)
                    index += 3
                    continue
                ret += character
                index += 1
        else:
            raise DeserializationError("Invalid string, missing percent encoding character")

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    ret = int(marshalled_integer[1:])

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}    
    validCharacters = " -_+."
    # TODO: Validate and parse using the data-type specific functions
    
    braceCount = 0
    chunkList = []
    key = ""
    # if marshaled_map is not empty then process the nosj string
    if marshalled_map != "":
        temp = ''
        # Detect if comma exests, if found then only split on the first level
        # it will ignore nested dictionaries that contain comma
        if ',' in marshalled_map:
            # Check for Ballance the braces and only split on comma
            # when ballaance braces are detected before comma
            for character in marshalled_map:
                if character == '{':
                    braceCount += 1
                elif character == '}':
                    braceCount -= 1
                temp += character
                if braceCount == 0 and character == ',':
                    chunkList.append(temp[:-1])
                    temp = ''
            if temp != '':
                chunkList.append(temp)

        # if chunkList is empty then add marshalled_map to chunkList
        if not chunkList:
            chunkList.append(marshalled_map)

        # itterate through the chunkList 
        for chunk in chunkList:
            # if no : detected then no key exists and string is malformed
            if ":" not in chunk:
                raise DeserializationError("No Key present")

            # Attempt to parse key
            data = chunk.split(':')
            key = data[0]
            data = ':'.join(data[1:])


            # Validating dictionary Key
            isKeyValid = False
            for character in key:
                if character.isalpha() or character.isnumeric() or (character in validCharacters):
                    isKeyValid = True
                else:
                    isKeyValid = False
                    raise DeserializationError("Dictionary Key contains invalid character")
            
            # is data a nested dictionary, if so send it through
            # unmarshal function again
            if '{' in data and '}' in data:
                data = data.strip()
            
            if data != '':
                if data[0] == '{' and data[-1] == '}':
                    ret[key] = unmarshal(data)
                # if data is encoded nosj integer then send it to the integer function
                elif data[0] == 'i' and (data[1:].isnumeric() or (data[1] == '-' and data[2:].isnumeric())):
                    ret[key] = __unmarshal_integer(data)
                # Anything not a map or integer should be a nosj string
                else:
                    ret[key] = __unmarshal_string(data)
            else:
                ret = {}

    else:
        ret = {}

    return ret



def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    # if string is empty
    # if len(marshalled_state) < 2 or marshalled_state == '':
    #     DeserializationError("Invalid and too short")
    ballancedBraces = 0
    braceDetected = False
    # strip leading and trailing whitespace
    marshalled_state = marshalled_state.strip()
    for character in marshalled_state:
        if character == '{':
            ballancedBraces += 1
            braceDetected = True
        elif character == '}':
            ballancedBraces -= 1
    
    if (ballancedBraces != 0) or (braceDetected == False):
        raise DeserializationError("Input is invalid, not ballanced or no braces found")

    # Strip outer braces
    if len(marshalled_state) >= 2:
        if marshalled_state[0] == '{' and marshalled_state[-1] == '}':
            marshalled_state = marshalled_state[1:-1]
    else:
        raise DeserializationError("Input is invalid, string is to short")

    return __unmarshal_map(marshalled_state)
