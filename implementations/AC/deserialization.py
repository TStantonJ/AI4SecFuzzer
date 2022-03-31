from exceptions import DeserializationError
import urllib

def __unmarshal_string(marshalled_string):
    ret = marshalled_string  
    # type 1
    if '%' not in marshalled_string and marshalled_string[-1] == 's':
        ret = marshalled_string[:-1] 
    # type 2
    elif '%' in marshalled_string:
        ret = urllib.parse.unquote(marshalled_string)
    return ret

def __unmarshal_integer(marshalled_integer):
    num = str(marshalled_integer)[1:]
    ret = int(num)
    return ret

# Makes sure that we have a valid dictionary to work with
# Checks the balance of the brackets '{' and '}'
def __checkBalance(string):
    i = 0
    for j in string:
        if j == '{':
            i += 1
        elif j == '}':
            i -= 1
    if i < 0 or i % 2:
        return False
    else:
        return True

def __unmarshal_map(marshalled_map):
    ret = {}
    # gotta split the string into keys and values i guess
    # little convoluted, but it works so
    open = 0 # if there are unclosed dict brackets
    valueFlag = 0
    endOfDictEntry = 0
    key = ''
    value = ''
    bracketId = []
    for i, x in enumerate(marshalled_map):
        if x == '{':
            open += 1
            bracketId.append(i)
        if valueFlag == 0:
            if x != '{' and x != ':':
                key += x # add to key until complete
            elif x == ':':
                valueFlag = 1 # set up to get value next
        else:
            if x != ',' and x != '}':
                value += x
            elif x == '}':
                open -= 1
                if open > 0:
                    ret[key] = __unmarshal_map(marshalled_map[bracketId.pop():i+1])
                else:
                    endOfDictEntry = 1
            else:
                endOfDictEntry = 1
        if endOfDictEntry == 1:
            valueFlag = 0
            endOfDictEntry = 0
            # with the completed value, must read whether an int or string
            if value[-1].isdigit() and value[0] == 'i':
                ret[key] = __unmarshal_integer(value)
                key = ''
                value = ''
            # This catches strings in nested dicts
            elif open > 0 and x != ',':
                ret[key] = __unmarshal_string(value)
            # This catches other strings
            elif x != ',' and '{' not in value:
                ret[key] = __unmarshal_string(value)
            else:
                key = ''
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if marshalled_state == '':
        raise DeserializationError('Input is empty')
    if '{' in marshalled_state:
        if __checkBalance(marshalled_state) == False:
            raise DeserializationError('Unbalanced brackets')
        if __checkBalance(marshalled_state) == True and ':' not in marshalled_state and len(marshalled_state) > 2:
            raise DeserializationError('Dictionary incomplete')
    if marshalled_state == '[]':
        raise DeserializationError('Honestly, not sure what the issue is with this input')

    return __unmarshal_map(marshalled_state)
