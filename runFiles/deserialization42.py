from exceptions import DeserializationError
import urllib.parse
import string
def __unmarshal_string(marshalled_string):
    ret = ''
    ret = marshalled_string[:-1]

    return ret
def __unmarshal_compstring(marshalled_string):
    ret = urllib.parse.unquote(marshalled_string, 'utf-8')
   

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    ret = marshalled_integer.replace('i','')

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    sep = marshalled_map.split(',')
    sep += marshalled_map.replace('{','').replace('}','')

    for keyvalue in sep:
        key = keyvalue.partition(':')[0]
        value = keyvalue.partition(':')[2]
        
        if value[1] == 'i':
           value = __unmarshal_integer(value)
        elif value[-1] == 's':
           value = __unmarshal_string(value)
        elif '%' in value:
            value = __unmarshal_compstring(value)
        elif value == '{':
           value = __unmarshal_map(value)

    ret[key] = value

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
