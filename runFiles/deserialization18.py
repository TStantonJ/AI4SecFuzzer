from exceptions import DeserializationError
import string
import urllib.parse

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert

    # If the string contains a '%' then it requires percent encoding 
    if marshalled_string.find('%') != -1:
        ret = urllib.parse.unquote(marshalled_string)
        return ret

    # If it ends in a 's', it is a simple string and the 's' needs to be removed
    elif marshalled_string.endswith('s'):
        ret = marshalled_string[:-1]
        return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert

    # Check to make sure that the string starts with an 'i'
    if marshalled_integer.startswith('i'):

    # Remove the 'i' and turn the string into an integer
            ret = marshalled_integer[1:]
            ret = int(ret)

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    bracket_counter = 0
    vindex = ''
    value = ''
    key = ''
    # TODO: Validate and parse using the data-type specific functions

    # Check to see if the string is empty and raise an error if it is
    if not marshalled_map:
        raise DeserializationError('The input string is empty')

    # If the string is not empty, but check and make sure the string contains '{ }' else raise an error
    elif marshalled_map.find('{') == -1 or marshalled_map.find('}') == -1:
        raise DeserializationError('The input does not contain the correct brackets ({})')

    # Remove the first and last bracket from the intial string
    start = marshalled_map[1:-1]
    
    # While start is not empty determine the value type and turn into a dictionary
    while start: 

    # Determine the key and store its value
        kindex = start.find(':')
        key = start[:kindex]

    # Determine value and store it
        value = start[kindex + 1:]

    # Loop through value and check to see if there are nested loops or multiple items that need to be added
        for i, c in enumerate(value):
            if c == '{':
                bracket_counter += 1
            elif c == '}':
                bracket_counter -= 1
            elif bracket_counter > 0:
                continue

    # This determines if there are multiple items in the string dictionary, if detected save the first item 
            elif c == ',':
    # Save the vindex value to be able to search the items behind the one found
                vindex = value 
                value = value[:i]
                break

    # Sets the value equal to sindex
        sindex = value
    # Determine the type of value and send to correct functions, else raise error
        if value.find('{') != -1 or value.find('}') != -1:
            value = __unmarshal_map(value)
        elif value.find('%') != -1:
            value =__unmarshal_string(value)
        elif value.endswith('s'):
            value = __unmarshal_string(value)
        elif value.startswith('i'): 
            value = __unmarshal_integer(value)
        else:
            raise DeserializationError('The value type could not be determined')
        
    # Allows to trim the string input so the items after the first one detected will be processed
        if vindex.find(',') != -1:

    # Cut start into a smaller string to prevent infinite loops
            start = vindex[i+1:]
            vindex = sindex

    # If there is only one item in the string dictionary just cut the values processed from the start string
        else:
            start = sindex[i+1:]

    # Add the key and its value to the dictionary 
        ret[key] = value
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
