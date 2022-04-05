from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    #the string parameter is checked to be a valid string in __unmarshal_map() and unmarshal()

    #saves string parameter in ret
    ret = marshalled_string

    # TODO: Validate and convert

    #tempList contains all complex characters and their corresponding percent-encoded counterparts
    tempList = [("%", "%25"),(":", "%3A") , ("/", "%2F"), ("?", "%3F" ), ("#", "%23") , ("[", "%5B"), ("]", "%5D"), ("@", "%40"), ("!", "%21"), ("$", "%24"), ("&", "%26"), ("'", "%27"), ("(", "%28"), (")", "%29"), ("*", "%2A"), ("+", "%2B"), (",", "%2C"), (";", "%3B"), ("=", "%3D"), ("\x01", "%00"), ("{", "%7B"), ("}", "%7D")]

    #if a '%' is located in the given string, then the string must be complex
    #the percent-encoded substring is replaced or swapped with their corresponding counterpart from the tempList
    #the final result is a decoded string
    #if a '%' is never detected in the given string, then the string must be simple
    #in this case, 's' is removed from the end of the given string
    size = len(ret)
    if '%' in ret:
        for (reserved, swap) in tempList:
            if swap in ret:
                ret = ret.replace(swap, reserved)
    elif ret[size - 1] == 's':
        ret = ret[0:(size - 1)]

    return ret

def __unmarshal_integer(marshalled_integer):
    #the string parameter is checked to be a valid formatted integer in __unmarshal_map() and unmarshal()

    temp = ""
    ret = 0
    
    # TODO: Validate and convert

    #if the given string contains an 'i' at the start, then 'i' is "removed"
    #otherwise, the string parameter is untouched
    #before returning the result, the string is converted to an integer value
    if marshalled_integer[0] == 'i':
        temp = temp + marshalled_integer[1:len(marshalled_integer)]
    else:
        temp = temp + marshalled_integer
    
    ret = int(temp)

    return ret

def __unmarshal_map(marshalled_map):
    #the entire string parameter as a whole is validated in unmarshal()
    #__unmarshal_map() performs further validation by checking for each acceptable type and format when looking through the parameter's contents

    # TODO: Validate and parse using the data-type specific functions
    
    tempStr = ""
    tempStr2 = ""
    counter = 0
    ret = ""

    #this approach goes over each character in the string parameter
    #a temporary string populated and built upon as the string parameter is searched
    #this temporary string is formatted like a dictionary for future conversion
    #the values found in the string parameter are validated by checking for nosj characteristics
    #once the temporary string is complete, it is converted to a dictionary and assigned to Dict
    #Dict is passed a parameter in looking_for_null() in order to locate and change the value that represents null (\x00)
    #   this was done to avoid issues caused when converting the string to a dictionary that contained null bytes
    #the result of looking_for_null() is assigned to Dict and returned 
    if '{' in marshalled_map:
        for element in marshalled_map:
            if element.isalpha():
                if marshalled_map[counter + 1] == ':':
                    ret = ret + "'" + element + "'"
            if element == ':':
                ret = ret + ":"
                if marshalled_map[counter + 1] != '{':
                    tempStr = marshalled_map[counter + 1 : len(marshalled_map) - 1]
                    for elmnt in tempStr:
                        if (elmnt == '}') or (elmnt == ','):
                            break
                        else:
                            tempStr2 = tempStr2 + elmnt
                    if (tempStr2[0] == 'i') and (tempStr2[1].isdigit()):
                        ret = (ret + "% d") % __unmarshal_integer(tempStr2)
                        tempStr2 = ""
                    elif (tempStr2[1] == '-') and (tempStr2[0] == 'i'):
                        ret = (ret + "% d") % __unmarshal_integer(tempStr2)
                        tempStr2 = ""
                    elif tempStr2[0].isdigit():
                        ret = (ret + "% d") % __unmarshal_integer(tempStr2)
                        tempStr2 = ""
                    else:
                        ret = ret + "'" + __unmarshal_string(tempStr2) + "'"
                        tempStr2 = ""
            if element == '{':
                ret = ret + "{"
            if element == ',':
                ret = ret + ", "
            if element == '}':
                ret = ret + "}"
            counter = counter + 1

    Dict = eval(ret)
    Dict = looking_for_null(Dict)

    return Dict



def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    #the validation in unmarshal() checks the entire string as a whole for valid characteristics of nosj
    #if anything unfamiliar is found, then DeserializationError is raised
    tempList = [":" , "/" , "?" , "#" , "[" , "]" , "@" , "!" , "$" , "&" , "'" , "(" , ")" , "*" , "+" , "," , ";" , "="]


    if (len(marshalled_state) == 2) and ('{' in marshalled_state) and ('}' in marshalled_state):
            return __unmarshal_map(marshalled_state)
    if isinstance(marshalled_state, dict):
        for key, val in marshalled_state.items():
            if isinstance(val, int):
                temp2 = str(val)
                if temp2[0] == 'i':
                    pass
                else:
                    raise DeserializationError('Input contains unmarshalled variables')
            if isinstance(val, str):
                for i in tempList:
                    if i in val:
                        pass
                    else:
                        raise DeserializationError('Input contains unmarshalled variables')
        return __unmarshal_map(marshalled_state) 
    elif isinstance(marshalled_state, int):
        temp3 = str(marshalled_state)
        if temp3[0] == 'i':
            return __unmarshal_map(marshalled_state)
        else:
            raise DeserializationError('Input contains unmarshalled variables')
    elif isinstance(marshalled_state, str):
        for i in tempList:
            if i in marshalled_state:
                return __unmarshal_map(marshalled_state)
            else:
                raise DeserializationError('Input contains unmarshalled variables')
    
    
#this function was created to go over the keys and values of a dictionary parameter to locate and replace any values that are meant to be null bytes
def looking_for_null(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            value = looking_for_null(value)
        if type(value) is str:
            if "\x01" in value:
                value = value.replace("\x01", "\x00")
                dictionary[key] = value
    return dictionary
