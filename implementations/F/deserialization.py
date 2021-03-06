from exceptions import DeserializationError
import urllib
from urllib.parse import unquote
import re




def __unmarshal_string(marshalled_string):
    ret = ""
    if "%" in marshalled_string:
        #Complex string
        return urllib.parse.unquote(marshalled_string)
    else:
        #Strips simple string s tag
        if not marshalled_string.endswith("s"):
            raise DeserializationError("Invalid String Format")
        ret = marshalled_string[:-1] 
        return ret


def __unmarshal_integer(marshalled_integer):
    #Validates if the integer string is correct
    pattern = re.compile("^i-?[0-9]\d*")
    if pattern.match(marshalled_integer):
        ret = marshalled_integer.strip("i")
        ret = int(ret)
        return ret
    else:
        raise DeserializationError("Incorrect Int format")

def __unmarshal_map(marshalled_map):
    if marshalled_map == "{}":
        return {}
    #Checks for map balance
    __validate_balance(marshalled_map)
    ret = {}
    if __validate_balance(marshalled_map):
        return __parse_map(marshalled_map)
    else:
        raise DeserializationError("Incorrect map formatuio")

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')


    return __unmarshal_map(marshalled_state)

#Verifies if map fulfills correct bracket balance and form
def __validate_balance(marshalled_map):
    #Since marshalled strings will have %encoded brackets except for "{","}",
    #Any other brackets will be invalid.
    wrong_braces = ["(",")", "[","]"]
    bracket_stack = []
    for char in marshalled_map:
        if char in wrong_braces:
            #Invalid format error
            raise DeserializationError("Wrong format. Expected either { or }, got: " + char )
        if char == "{":
            bracket_stack.append(char)
        elif char == "}":
            #Unbalanced bracket error
            if len(bracket_stack) == 0:
                raise DeserializationError("Map is not balanced")
            bracket_stack.pop()
    if len(bracket_stack) !=0:
        raise DeserializationError("Map is not balanced.")
    else:
        return True 

#Function for handling nested maps with recursion.
def __parse_map(map,starting_index=0):
    ret = {}
    if len(map) == 0:
        return ret
    key = ""
    value = ""
    #Switches between key and value
    isKey = True
    for index, char in enumerate(map[starting_index+1:], start = 1):
        if char == "}":
            if __endOfMapCheck(map[index:]) and len(ret) != 0:
                return ret
            __validate_key(key)
            ret[key] = sort(value)
            isKey = not isKey
            key = ""
            value = ""
            break
        if char == ",":
            __validate_key(key)
            ret[key] = sort(value)
            isKey = not isKey
            key = ""
            value = ""
            continue
        if char == ":":
            isKey = not isKey
            continue
        if isKey:
            if char == "{" and index != starting_index + 1:
                raise DeserializationError("Incorrect formatting")
            else:
                key = key + char
                continue
        else:
            if char == "{":
                __validate_key(key)
                ret[key] = __parse_map(map,index)
                key = ""
                value =""
                isKey = not isKey
                continue
            else:    
               value = value + char
               continue
    return ret

#Validates both key and value and inserts the pair into the map. Raises any errors for incorrect formatting for either key
#or value
# def __unmarshal_value(key, value, map):
#     if __validate_key(key):
#         integer_pattern = re.compile("^i-?[0-9]\d*")
#         if integer_pattern.match(value):
#             finalValue = __unmarshal_integer(value)
#         elif "{" or "}" in value:
#             pass
#         else:
#             finalValue = __unmarshal_string(value)
#     map[key] = finalValue
    

def __validate_key(key):
    if type(key) is not str:
        raise DeserializationError("Key is not a str")
    valid_strings = re.compile("[^\w\ \-\_\+\.]")
    key = valid_strings.search(key)
    if bool(key):
        raise DeserializationError("Invalid key format")
    return not bool(key)        

#takes in marshalled value and returns correct unmarshalled state.
def sort(value):
    integer_pattern = re.compile("^i-?[0-9]\d*")
    if integer_pattern.match(value):
        return __unmarshal_integer(value)
    else:
        return __unmarshal_string(value)

#Function to help ignore trailing }. Balance is checked with other functions
def __endOfMapCheck(string):
    pattern = re.compile("[^}]")
    if len(string) == 0:
        return True
    return not pattern.search(string)