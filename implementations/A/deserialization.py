from exceptions import DeserializationError
import urllib
import string

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert
    if '%' in marshalled_string:
        ret = urllib.parse.unquote(marshalled_string)
    else:
        ret = marshalled_string[:-1]
    
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    # TODO: Validate and convert
    ret = int(marshalled_integer[1:])
    return ret

def isBalanced(bString):
    bStack = []
    for char in bString:
        if char == '{':
            bStack.append(char)
        else:
            fs = bStack.pop()
            if fs == '{':
                if char != '}':
                    return False
    if bStack:
        return False
    return True

def findStop(fStack, count):
    counter = count
    buffer = ''
    for f in fStack:
        if f == '{':
            counter += 1
        if f == '}':
            counter -= 1
        buffer += f
        if counter == 0:
            return buffer


def __unmarshal_map(marshalled_map):
    ret = {}
    # TODO: Validate and parse using the data-type specific functions
    current_value = ''
    
    dictionaryList = []
    buffer = ''
    
    counter = 0
    if marshalled_map[0] == '{' and marshalled_map[len(marshalled_map)-1] == '}':
        marshalled_map = marshalled_map[1:-1]
    else:
        raise DeserializationError('Input string has charachters outside of the dictionary')
    
    for i in range(len(marshalled_map)):
        if marshalled_map[i] == '{':
            counter += 1
        if marshalled_map[i] == '}':
            counter -= 1
        if marshalled_map[i] != ',':
            buffer += marshalled_map[i]
            if i == len(marshalled_map) - 1:
                dictionaryList.append(buffer)
                buffer = ''
        elif counter == 0:
            dictionaryList.append(buffer)
            buffer = ''
        
    
    for dict_string in dictionaryList:
        stack = []
        key = ''
        
        for i in dict_string:
            stack.append(i)
        
        stack.reverse() 
        
        char1 = stack.pop()
        if char1 == '}':
            return dict()
        if char1 == ':':
            raise DeserializationError('Input has no key')
        while char1 != ':':
            key += char1
            char1 = stack.pop()

        stack.reverse()
        
        stack_string = ""
        for x in stack:
            stack_string += x

        stack.reverse()

        #print(stack)
        #print(stack_string)

        if stack[-1] == '{':
            #print(stack_string)
            current_value = __unmarshal_map(findStop(stack_string, 0))
        else:
            if stack[-1] != 'i':
                current_value = __unmarshal_string(stack_string)
            else:
                current_value = __unmarshal_integer(stack_string)
        
    
        if (not isinstance(key, str) or not any(k in key for k in string.ascii_letters + string.digits + " " + "-" + "_" + "+" + ".")):
            raise DeserializationError('key is not a string or does not contain at one of required characters')
    
        ret.update({key:current_value})
    
    return ret



def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    if marshalled_state == '':
        raise DeserializationError('Input is an empty string')
    if not('{' in marshalled_state and '}' in marshalled_state):
        raise DeserializationError('Input string does not contain a dictionary')
    if marshalled_state != '{}' and not(':' in marshalled_state):
        raise DeserializationError('Input string does not contain a key:value pair and is not empty')
    
    bracket_string = ''
    balanced = True
    stack = []
    for s in marshalled_state:
        if s == '{' or s == '}':
            bracket_string += s
    
    balanced = isBalanced(bracket_string)
    if not balanced:
        raise DeserializationError('brackets are not ballanced')


    return __unmarshal_map(marshalled_state)
