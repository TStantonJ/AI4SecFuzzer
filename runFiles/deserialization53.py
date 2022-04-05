from exceptions import DeserializationError
import string
def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert
    # A marshalled string should be a string
    if isinstance(marshalled_string,str) == False:
        raise DeserializationError('Marshalled String given must be a string')
    
    # First check if string is complex or not:
    cmplx = False
    for c in marshalled_string:
        if c == %:
            cmplx = True
            break
    # A complex string needs to be un-percent encoded.
    if cmplx:
       ret = urllib.parse.unquote(marshalled_string)
   # A Simple String should end with an s. If it is neither percent encoded or ending with s, it cannot be deserializze
   elif not marshalled_string.endswith('s'):
       raise DeserializationError('Marshalled Simple Strings Must End With s')
  # A simple string needs its trailing s removed.
   else:
       ret = marshalled_string.removesuffix('s')
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    # A marshalled integer will be in ascii and have a leading i (optional -) 
    if not marshalled_integer.startswith('i'):
        raise DeserializationError('Marshalled Integers must start with i')
    # First check if the marshalled integer contains only decimals
    i_removed = ''
    if marshalled_integer.startswith('i-'):
        i_removed = marshalled_integer.removeprefix('i-')
        # With the i- removed, the string must only contain numbers to proceed
        if not i_removed.isdecimal():
            raise DeserializationError('Marshalled Integers must contain only numbers 0 through 9')
        ret = int(i_removed)
        # Now it is in it's itneger form, the number must be whole
        if ret%1 != 0:
            raise DeserializationError('Marhalled Integers must be whole numbers')
    else:
        i_removed = marshalled_integer.removeprefix('i')
        # With the i removed, the string needs to be all numbers
        if not i_removed.isdecimal():
            raise DeserializationError('Marshalled Integers must contain only numbers 0 through 9')
        ret = int(i_removed)
        # check if whole
        if ret%1 != 0:
            raise DeserializationError('Marshalled Integers must be whole numbers')


    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    
    # TODO: Validate and parse using the data-type specific functions
    # A valid marshalled map will be a string starting with a {
    if not isinstance(marshalled_map, str):
        raise DeserializationError('Marshalled Maps should be a string')
    if not marshalled_map.startswith('{'):
        raise DeserializationError('Marshalled Maps should start with a {')
    # to keep up with the brackets, a sta k needs to be created
    stack = []
    key = ''
    value = ''
    
    for c in unmarshalled_map:
        # The map starts with a {. Pop to the stack to maintain brackets
        if c == '{':
            stack.append()
            unmarshalled_map.removeprefix('{')
            # Scan for the key, then remove it from the string. When it hits : ,
            # it stops reading for the key and removes the :.
            for c in unmarshalled_map:
                key += c
                unmarshalled_map.removeprefix(c)
                if c == ':':
                    unmarshalled_map.removeprefix(':')
                    break
            break    
        
        
        elif c == '}':
            # Check for integers
            if value.startswith('i'):
                temp_val = value
                temp_val.removeprefix('i')
                
                # integers are all numbers, anything else could be a string
                if temp_val.isdecimal():
                   ret[key] = self.__demarshal_integer(value)
               else:
                   ret[key] = self.__demarshal_string(value)
            # Since the for loop catches {, and , there should not be any map caught here
            else:
                ret[key] = self.__demarshal_string(value)
           
           stack.pop()

        elif c == ',':
            unmarshalled_map.remove_prefix(c)
            break



       # After the key is found, find the value in order to unmarshall it
        value += c
        unmarshalled_map.removeprefix(c)
      
        
    
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
