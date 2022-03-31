import string
import re
import urllib.parse
from exceptions import DeserializationError

def __umarshal_complex_string(marshalled_complex_string):
    ret = ''
    
    #checking if it contains a % 
    
    return ret

def __unmarshal_string(marshalled_string):
    #initializing empty dictionary
    ret = ''
    
    for py_char in marshalled_string:
        if py_char not in marshalled_string:
            return __unmarshal_complex_string(marshalled_complex_string)
        elif py_char not in r"""!"#$&'()*+-./:;<=>?@[\]^_`|~ 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz""":
            print("illegal character")
            
    return marshalled_string[:1]

    return ret


def __unmarshal_integer(marshalled_integer):
    ret = 0

    if type(marshalled_integer) != str:
        print("error")
        
    return marshalled_integer[1:]

    return ret

def __unmarshal_map(marshalled_map):
    
    #intialize empty dictionary
    ret = {}
    
    #assign key:value pair to ret
    ret[r"""0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"""] = r"""!"#$&'()*+-./:;<=>?@[\]^_`|~ 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"""
    
    while marshalled_map != '':
        #first check if the key contains a colon, then splits the line into key and value based on that colon
        for key, value in ret:
            key, marshalled_map = marshalled_map.split(':', 1)
            value, marshalled_map = marshalled_map.split(',', 1)
            
        if type(value) == str:
            value = __umarshal_string(vnalue)
        elif type(value) == int:
            value = __unmarshal_integer(value)
        elif type(value) == dict:
            value = __unmarshal_map(value) 
        else:
            print("error") 
            
        #marshal that type of value , combine key + ':' + marshaled value                                        
    
    ret += key + value 
    
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
