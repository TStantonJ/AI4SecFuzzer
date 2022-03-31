from exceptions import DeserializationError
import re
import urllib
import string


def __unmarshal_string(marshalled_string):
    ret = {}

    # TODO: Validate and convert
    
    newString = marshalled_string.strip("{}")
    newString = newString[0:len(newString)-1]
    newString = newString.split(":")
    
    ret[newString[0]] = newString[1]
    
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = {}

    # TODO: Validate and convert
    newInt = marshalled_integer.strip("{}")
    newInt = newInt[1:len(newInt)]
    newInt = newInt.split(":")
    
    ret[newInt[0]] = int(newInt[1])

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}

    # TODO: Validate and parse using the data-type specific functions
#    __checkInt(marshalled_map.split(':')[1])
#    __checkString(marshalled_map)
    
    if marshalled_map[len(marshalled_map)-2] == 's':
        ret = __unmarshal_string(marshalled_map)

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    
    if __balanceCheck(marshalled_state) != 0:
        raise DeserializationError('Unbalanced brackets/braces/parantheses in string')
    if len(marshalled_state) <= 0:
        raise DeserializationError('String cannot be empty')
#    if marshalled_state[3] != 'i' or marshalled_state[len(marshalled_state)] != 's':
#        raise DeserializationError('String is not formatted properly')

    return __unmarshal_map(marshalled_state)
  
  
#Balanced bracket code from https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-python/
def __balanceCheck(checkString):
    opened = ["[","{","("]
    closed = ["]","}",")"]
    
    stack = []
    for i in checkString:
        if i in opened:
            stack.append(i)
        elif i in closed:
            position = closed.index(i)
            if ((len(stack) > 0) and (opened[position] == stack[len(stack)-1])):
                stack.pop()
            else:
                return -1
    if len(stack) == 0:
        return 0
    else:
        return -1
    
