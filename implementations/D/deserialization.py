from exceptions import DeserializationError
import re
import urllib.parse

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Checks if the value is a simple string and decodes it. If a complex string, it unquotes the url parsing

    if marshalled_string[len(marshalled_string) - 1] == "s":
        ret = marshalled_string[0:len(marshalled_string) - 1]

    else:
        ret = re.sub(r"(%00)", "\x00", marshalled_string)
        ret = urllib.parse.unquote(ret)
    
    
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # Converts the string into an int, without the encoded i in front
    ret = int(marshalled_integer[1:len(marshalled_integer)])

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}

    # First, checks to see if the map is empty, and then returns it. If it is not empty, it checks if there are at least one value and key pair

    if marshalled_map == "{}":
        return ret

    elif marshalled_map.find(":") == -1:
        raise DeserializationError('The Marshalled Map must have a key and a value')

    #Removes the curly brackets from the string and splits the items

    sub = marshalled_map.replace("{", "", 1)
    if sub[len(sub) - 1] == "}":
        sub = sub[:-1]

    splt = sub.split(",")
    tempDict = ""
    tempKey = ""

    #Goes through the items and grabs the values, then runs them through their respective functions
    for item in splt:
        
        temp = item.split(":", 1)
    
        #Checks if the value is a full dict, then passes it back into the function via recursion
        if "{" in temp[1] and "}" in temp[1]:
            ret[temp[0]] = __unmarshal_map(temp[1])

        #Checks if the value is the beginning of a dict, and stores it in a string named tempDict, and stores the original key in tempKey
        elif "{" in temp[1] and "}" not in temp[1]:
            tempDict += temp[1] + ","
            tempKey = temp[0]

        #Checks if the value is the end of a nested dict, and returns the tempDict back into the function via recursion
        elif "{" not in temp[1] and "}" in temp[1]:
            tempDict += temp[0] + ":" + temp[1]
            ret[tempKey] = __unmarshal_map(tempDict)

        else:
            typ = check_marshalled_type(temp[1])

            if typ == "integer":
                ret[temp[0]] = __unmarshal_integer(temp[1])

            else:
                ret[temp[0]] = __unmarshal_string(temp[1])

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if marshalled_state == "" or marshalled_state[0] != "{" or marshalled_state[len(marshalled_state) - 1] != "}":
        raise DeserializationError('Input does not match the syntax for a marshalled state')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)

#Custom function to test if a value is a string or an int
def check_marshalled_type(marshalled_data):
    
    test_int = marshalled_data[0:2]
    test_str = marshalled_data[len(marshalled_data) - 2: len(marshalled_data)]

    if test_int[0] == "i" and test_int[1].isnumeric() or test_int[0] == "i" and test_int[1] == "-":
        return "integer"

    return "string"


