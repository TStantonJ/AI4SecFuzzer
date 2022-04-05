from exceptions import DeserializationError

import ast
import re

def __unmarshal_string(marshalled_string):
    ret = ''
    # TODO Validate and convert
    t_str = marshalled_string
    print('string inside')
    if t_str[len(t_str)-1:len(t_str)] == "s":
        t_str = t_str[:len(t_str)-1]

    elif '%' in t_str:

        idx = t_str.find('%')
        t_char = t_str[idx:idx+3]
        if t_char == '%00':
            t_str = t_str.replace('%00', '\\x00')

        else:
            t_str = t_str.replace(t_char, bytes.fromhex(t_char[1:3]).decode('utf-8'))   

    ret = "'"+t_str+"'"
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    # TODO: Validate and convert

    t_int = marshalled_integer
    print(t_int, 'i:',t_int.find('i'))
    if t_int.find('i') == 0:
        t_int = t_int[t_int.find('i')+1:len(t_int)]
    print(t_int) 
    ret = t_int 
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    t_str = marshalled_map
    s_key_i = -1
    e_key_i = -1
    key = ""

    s_val_i = -1
    e_val_i = -1
    val = ""
    
    # TODO: Validate and parse using the data-type specific functions
    
#    print(t_str)
#    print("AFTER")

    output = ""
    skp_cmma = False
    for i in range(len(t_str)):
        
        if t_str[i] == "{":
            output += t_str[i]
        # value
        if t_str[i] == "{" or t_str[i] == ",":
            s_key_i = i+1
            
        elif s_key_i > -1 and t_str[i] == ":":
            e_key_i = i

        if s_key_i > -1 and e_key_i > -1:
            key = t_str[s_key_i:e_key_i]
            output += "'"+key+"'"
            s_key_i = -1
            e_key_i = -1
        

        if t_str[i] == ":":
            output += t_str[i]
            s_val_i = i+1
        elif s_val_i > -1 and (t_str[i] == "," or  t_str[i] == "}"):
            e_val_i = i

        if s_val_i > -1 and e_val_i > -1:
            val = t_str[s_val_i:e_val_i]
            s_val_i = -1
            e_val_i = -1
        
            
            if val.count('i') == 1 and not '%' in val:
                print('intger')
                output += str(__unmarshal_integer(val))
            else:
                print('string')
                output += __unmarshal_string(val)

        if t_str[i] == ",": 
            output += t_str[i]
   
        if t_str[i] == "}":
            output += t_str[i]

    ret = eval(output)
    print(ret)
    return ret

def chkStr(obj):
    for i in range(len(obj)-1):
        if obj[i] == "{" and (obj[i+1] == ":" or obj[i+1] == ","):
            raise DeserializationError('Input has a wrong format')
        elif ((obj[i] == ":" or obj[i] == ",") and obj[i+1] == "}"):
            raise DeserializationError('Input has a wrong format')

def unmarshal(marshalled_state):
    print(marshalled_state)
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if not "{" in marshalled_state or not "}" in marshalled_state:
        raise DeserializationError('Input does not have the curly braces')
    if len(marshalled_state) == 0:
        raise DeserializationError('Input is Empty')
    if len(marshalled_state) > 2 and marshalled_state.find(":") == -1:
        print(marshalled_state)
        raise DeserializationError('Input is not formed with key, value')

    chkStr(marshalled_state)
    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
