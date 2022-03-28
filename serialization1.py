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