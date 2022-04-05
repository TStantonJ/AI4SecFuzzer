from exceptions import DeserializationError

import string
import urllib.parse
import re

#Converts a nosj string to a python string
def __unmarshal_string(marshalled_string):
    ret = ''
    if '%' in marshalled_string:
        ret = urllib.parse.unquote(marshalled_string)
    else:
        if marshalled_string[-1] != 's':
            raise DeserializationError('Improper format. Simple string must have "s" at end')
        ret = marshalled_string[0:-1]

    return ret

#Converts nosj substring to an int
def __unmarshal_integer(marshalled_integer):
    ret = 0
    pattern = r'[^0-9/-]+'
    prog = re.compile(pattern)
    if re.search(prog, marshalled_integer) != None:
        raise DeserializationError('Improper format. Anything following i must be an integer')
    ret = int(marshalled_integer)

    return ret

#Deserializes a "map" in the nosj. Really, is the main area but 
#is able to use recursion to find the inner mapsl, treating them like the overall map string
def __unmarshal_map(marshalled_map):
    ret = {}
    #if the marshalled map isn't None, empty or just whitespace
    #validate and parse
    if marshalled_map is None or marshalled_map.isspace() or not marshalled_map:
        return ret
    else:
        #get string up to ':'
        start = 0
        at = 0
        while at < len(marshalled_map):
            #get key
            at = marshalled_map.find(':', start)
            if(at == -1):
                raise DeserializationError('Missing key')
            key = marshalled_map[start:at]
            #determine what type of unsmarshalling needs to be done and call
            if at+1 >= len(marshalled_map):
                raise DeserializationError('No value for key')
            
            #Finds the dict within the nosj string, uses recursion to convert into a dict
            #then sets the value to said dict
            if marshalled_map[at+1] == '{':
                # Bracket matching
                at += 1
                start = at

                queue = []
                queue.append('{')
                #find last matching bracket
                while len(queue) > 0:
                    at += 1
                    if at >= len(marshalled_map):
                        raise DeserializationError('Improperly formatted input')
                    if marshalled_map[at] == '{':
                        queue.append('{')
                    elif marshalled_map[at] == '}':
                        queue.pop()
                new_map = marshalled_map[start+1:at]
                map_value = __unmarshal_map(new_map)
                #add dict as value to dict
                ret.update({key: map_value})
                
                #finds the , or sets at to the end of the string
                start = at
                at = marshalled_map[start:].find(',')
                if at == -1:
                    at = len(marshalled_map)
                else:
                    at = start + at
            else: #Converts the string to an integer or string
                at = at+1
                start = at
                if at+1 >= len(marshalled_map):
                    raise DeserializationError('Improperly formatted input. No integer')
                
                #Finds where the current value ends
                at = marshalled_map[start:].find(',')
                if at == -1:
                    at = len(marshalled_map)
                else:
                    at = start + at
                
                #Determines if the substring needs to be converted to an int or a string
                if marshalled_map[start] == 'i':
                    int_value = __unmarshal_integer(marshalled_map[start+1:at])
                    ret.update({key: int_value})
                else:
                    str_value = __unmarshal_string(marshalled_map[start:at])
                    ret.update({key: str_value})
            at +=1
            start = at
    return ret

#Main Deserialization method
def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    else:
        #checks if the string is empty
        if not marshalled_state:
            raise DeserializationError('Input string is empty')
        #checks if the string starts and ends with {}
        if marshalled_state[0] != '{' and marshalled_state[-1] != '}':
            raise DeserializationError('Input string must be enlosed by { and }')
        #checks if there are colons
        if not ':' in marshalled_state:
            sub = marshalled_state[1:-1]
            #determines if the input is just empty or whitespace (which is valid)
            if not sub.isspace() and sub:
                raise DeserializationError('Input string is not converable to dict')
        #checks if there if the number of brackets match 
        if marshalled_state.count('{') != marshalled_state.count('}'):
            raise DeserializationError('Input string has mismatched number of brackets')
        return __unmarshal_map(marshalled_state[1:-1])