from exceptions import DeserializationError
import re

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert

    return ret

def __unmarshal_map(marshalled_map):
    
        
    string = marshalled_map[3:-1]
    key = marshalled_map[1]
    
    
    if string[0] == 'i':
        ret = {key : int(marshalled_map[4:-1])} 
    elif string[-1] == 's':
        ret = {key : (marshalled_map[3:-2])}
    #elif:
        #ret = {'a' : (marshalled_map)
    else:
        raise DeserializationError('try sumn else')
        
    
   
    # if type(int(marshalled_map[4:(len(marshalled_map)-1)])) == int:
        
        # ret = {'a' : int(marshalled_map[4:(len(marshalled_map) - 1)])}
        
    # elif type(marshalled_map[3:(len(marshalled_map) - 2)]) == str:
    
        # ret = {'a' : int(marshalled_map[3:(len(marshalled_map) - 2)])}
        

    

    # TODO: Validate and parse using the data-type specific functions

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
