from exceptions import SerializationError
import urllib.parse
import re

def __marshal_string(py_string):
    if __validate_string(py_string) == 0:
        return py_string.strip() + "s"
    elif __validate_string(py_string) == 1:
        return urllib.parse.quote(py_string)
    else:
        raise SerializationError("Invalid input")


def __marshal_integer(py_int):
    if py_int is None:
        raise SerializationError("Input is none")
    if type(py_int) != int:
        raise SerializationError("Input is not an int")

    return "i" + str(py_int)



def __marshal_map(py_dict):
    ret = '{'
    if type(py_dict) is not dict:
        raise SerializationError("Value is not a dict.")
    for key, value in py_dict.items():
        #Checks if key is valid. Recursively iterates through the entire dict.
        if __validate_key(key):
            ret += str(key) + ":"
            if type(value) is int:
                ret += __marshal_integer(value) + ","
            elif type(value) is str:
                ret += __marshal_string(value)  + ","
            elif type(value) is dict:
                ret += __marshal_map(value) + ","
            else:
                raise SerializationError("Value for Key: " + key +" is invalid." )

        else:
            raise SerializationError("Key: " + key + " is an invalid key.")
    #Strips trailing comma only if map is not empty
    ret = ret[:-1] if ret != "{" else "{"
    ret += "}"    

    return ret


def marshal(unmarshalled_state):
    if unmarshalled_state is None:
        raise SerializationError('Input is None')
    if type(unmarshalled_state) != dict:
        raise SerializationError('Input is not a dict')

    # TODO: Validate things about the overall Python3 dict

    return __marshal_map(unmarshalled_state)

#Validates input for strings. Returns 0 or 1 if input is simple or complex respectively. Raises exception if input is invalid.
def __validate_string(py_string):
    if py_string is None or py_string == "":
        raise SerializationError("Input is none")
    if type(py_string) != str:
        raise SerializationError("Input is not a str")

    #Array of simple string exceptions
    exceptions = ['%',",","{","}"]
    if py_string.isprintable():
        if any(x in py_string for x in exceptions):
            #Complex string
             return 1
        else:
            #Simple string
            return 0            
    else:
        return 1

#Validates map key using regex. Searches key for everything not containing valid characters.
def __validate_key(key):
    if type(key) is not str:
        raise SerializationError("Key is not a str")
    valid_strings = re.compile("[^\w\ \-\_\+\.]")
    key = valid_strings.search(key)
    return not bool(key)