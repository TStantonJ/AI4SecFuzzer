from exceptions import DeserializationError
import urllib.parse
import json 
import ast
def __unmarshal_string(marshalled_string):
    ret = ''
    if '%' in marshalled_string: 
        ret = urllib.parse.unquote(marshalled_string)
    else:
        ret = marshalled_string
        ret = ret.rstrip(ret[-1])
    return ret 

def __unmarshal_integer(marshalled_integer):
    ret = 0
    temp = marshalled_integer[1:]
    ret = int(temp)
    return ret

def checkme(val):
    if ':' not in val:
        return val
    else:
        key, value = val.split(':', 1)
        return {key: checkme(value)}

def __unmarshal_map(marshalled_map):
    ret = {}
    if ':' in marshalled_map:
        for item in marshalled_map.split(','):
            key, value = item.replace('{', '').replace('}', '').split(':', 1)
            ret.update({key: checkme(value)})
    else:
        pass
    for key, value in ret.items():
        if value[0] == 'i':
            ret[key] = __unmarshal_integer(value)
        elif type(value) is str:
            ret[key] = __unmarshal_string(value)
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if '{' not in marshalled_state or '}' not in marshalled_state:
        raise DeserializationError('Input not nosj')
    return __unmarshal_map(marshalled_state)
