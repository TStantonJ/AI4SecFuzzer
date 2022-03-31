
import re
from enum import Enum
from enum import IntEnum
from urllib import parse

from exceptions import DeserializationError


class __Error(Enum):
    '''
    Enumeration for classifying input error states.
        NO_ERR: Input is a valid map.
        MAP_ERR: Input has invalid formatting.
        KEY_ERR: Input contains restricted characters in a key.
        VALUE_ERR: Input contains restricted characters in a value.
    '''
    NO_ERR = 0
    MAP_ERR = 1
    KEY_ERR = 2
    VALUE_ERR = 3

class __Legend(IntEnum):
    '''Indexes of map key and value after parsing to individual pair.'''
    KEY = 0
    VALUE = 1


def __is_map(marshalled_map):
    '''
    Returns basic input validity status concerning formatting.
        nosj map representations are key-value pairs in the format of {key-1:value-1, key-2:value-2, ...}.

        Parameters:
            marshalled_map (str):   A string representing a nosj marshalled map
        
        Returns:
            NO_ERR (__Error):   Validy state of valid map
            MAP_ERR (__Error):  Validity state of invalid map
    '''

    # Return NO_ERR if input is an empty map.
    if marshalled_map.replace(' ', '') == '{}':
        return __Error.NO_ERR

    # Parse commas before validation.
    map_string = marshalled_map.replace(',', '}{')

    format_stack = []
    num_balanced_braces = 0

    # Validating the format of the input as a map.
    #    Searching for even pairs of matching braces with a colon separating the key and value pairs.
    #    Does not validate key and value formats to nosj specification.
    for char in map_string:
        if char == '{' or char == ':':
            format_stack.append(char)
        elif char == '}':
            if len(format_stack) > 1 and format_stack[len(format_stack) - 2] == '{' and format_stack[len(format_stack) - 1] == ':':
                format_stack.pop()
                format_stack.pop()
                num_balanced_braces += 1
            else:
                return __Error.MAP_ERR

    if num_balanced_braces == 0:
        return __Error.MAP_ERR

    return __Error.NO_ERR


def __unmarshal_string(marshalled_string):
    '''
    Returns a string when given a nosj formatted string.
        nosj simple string representations are allowed ASCII characters
            with the exception of [% , { }] with a singular 's' appended at the end.
        nosj complex string representations are allowed ASCII characters
            with percent encoding of certain ASCII symbols.

        Parameters:
            marshalled_string (str): A nosj string

        Returns:
            return_string (str): An unmarshalled string
    '''
    return_string = marshalled_string

    if '%' in marshalled_string: 
        return_string = parse.unquote(return_string.replace(' ', '%20'), encoding = 'ASCII', errors = None)
    else:
        return_string = return_string[0:-1]

    return return_string

def __unmarshal_integer(marshalled_integer):
    '''
    Returns an integer when given a nosj formatted integer.
        nosj integer representations require beginning with ASCII character 'i',
        an optional '-' denoting negative integers, and ASCII characters [0-9].

        Parameters:
            marshalled_integer (int): A nosj integer
        
        Returns:
            (int): An unmarshalled integer
    '''
    return int(marshalled_integer[1:]) 

def __unmarshal_map(marshalled_map):
    '''
    Returns a python dictionary or an enumerated error state when given a nosj marshalled map.
        Contains key-value pairs in the format of {key-1:value-1, key-2:value-2, ...}
            Key representations are in the form of ASCII strings allowed characters
            [a-z] [A-Z] [0-9] [-_+.] [whitespace].
        Value representations can be in the form of nosj strings, nosj integers, or nosj maps.

        Parameters:
            marshalled_map (str): A nosj marshalled map

        Returns:
            map_dictionary (dict): Python dictionary representation of unmarshalled map
            KEY_ERR (__Error): Validity state when restricted characters are in a key
            VALUE_ERR (__Error): Validity state when restricted characters are in a value
    '''
    # Empty maps do not require processing.
    if marshalled_map.replace(' ', '') == '{}':
        return {}

    map_list = marshalled_map.strip()[1:-1].split(',')
    key_stack = []
    map_dictionary = dict()

    for map in map_list:
        # Traverse to the lowest map in the nested map to process.
        #    Append all higher keys found to the key stack.
        while '{' in map or '}' in map:
            map_elements = str(map).split(':', 1)
            key_stack.append(map_elements[__Legend.KEY])
            map = map_elements[__Legend.VALUE].strip('{}')
        else:    
            map_elements = map.split(':')

        if not re.fullmatch(r'^[a-zA-Z0-9 \-_+.]+$', map_elements[__Legend.KEY], re.ASCII.IGNORECASE):
            return __Error.KEY_ERR

        # If value is of a nosj integer format unmarshall according to integer schema.
        if re.fullmatch(r'^i\-?[0-9]+$', str(map_elements[__Legend.VALUE]), re.ASCII):
            map_elements[__Legend.VALUE] = __unmarshal_integer(map_elements[__Legend.VALUE])
        # If value is of a nosj string format unmarshall according to string schemas.
        elif re.fullmatch(r'.*[%].*|.*[s]$', map_elements[__Legend.VALUE], re.ASCII.IGNORECASE):
            map_elements[__Legend.VALUE] = __unmarshal_string(map_elements[__Legend.VALUE])
        else:
            return __Error.VALUE_ERR

        # Handle assembling the dictionary in the case of nested dictionaries.
        if key_stack:
            current_key = key_stack.pop()
            map_dictionary.update({current_key: {map_elements[__Legend.KEY]: map_elements[__Legend.VALUE]}})

            # For every key remaining in the key stack,
            #    pop the last item added to the dictionary as the value
            while key_stack:
                next_key = key_stack.pop()
                map_dictionary.update({next_key: {current_key: map_dictionary.pop(current_key)}})
                current_key = next_key
        # Handle assembling non-nested dictionaries.
        else:
            map_dictionary.update({map_elements[__Legend.KEY]: map_elements[__Legend.VALUE]})

    return map_dictionary


def unmarshal(marshalled_state):
    '''
    Returns a python dictionary when given a nosj marshalled map.

        Parameters:
            marshalled_state (str): Supposed nosj marshalled map input

        Returns:
            unmarshalled_state (dict): Python dictionary representation of unmarshalled map

        Raises:
            DeserializationError:
                If marshalled_state is None, not a string, or empty
            DeserializationError:
                If input_state is invalid
            DeserializationError:
                If marshalled_state is found to have invalid keys or values
    '''
    if marshalled_state is None:
        raise DeserializationError('Input is Null')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if not marshalled_state.strip():
        raise DeserializationError('Input is empty')

    input_state = __is_map(marshalled_state)

    if input_state is __Error.MAP_ERR:
        raise DeserializationError('Input is not a map')

    unmarshalled_state = __unmarshal_map(marshalled_state)

    if unmarshalled_state is __Error.KEY_ERR:
        raise DeserializationError \
        ('A Dictionary Key is invalid\n' \
         + '\t' + str(marshalled_state) + '\n' \
         + '\tAllowed ASCII Key characters include:\n' \
         + '\t\t\'a-z\' \'A-Z\' \'0-9\' \'-_+.\' \'whitespace\'')
    if unmarshalled_state is __Error.VALUE_ERR:
        raise DeserializationError \
        ('A Dictionary Value is invalid\n' \
         + '\t' + str(marshalled_state) + '\n' \
         + '\tAllowed ASCII Value characters include:\n' \
         + '\t\tFirst Character: i\n' \
         + '\t\tOptional Character: \'-\'\n' \
         + '\t\tCharacters: \'0-9\'')

    return unmarshalled_state
