from exceptions import DeserializationError
#Checks if the string has any percent encoding.
#If it does, it replaces it with its relevant value.
#The flag checks if the method needs to remove trailing 's'
def __unmarshal_string(marshalled_string):
    
    ret = ''
    length = len(marshalled_string)
    
    #TODO: Validate and convert
    
    flag = False
    
    if '%25' in marshalled_string:
      marshalled_string = marshalled_string.replace('%25', '%')
      flag = True
    
    if '%00' in marshalled_string:
      marshalled_string = marshalled_string.replace('%00','\x00')
      flag = True
    
    if '%2C' in marshalled_string:
      marshalled_string = marshalled_string.replace('%2C',',')
      flag = True
    
    if '%7B' in marshalled_string:
      marshalled_string = marshalled_string.replace('%7B','{')
      flag = True
    
    if '%7D' in marshalled_string:
      marshalled_string = marshalled_string.replace('%7D', '}')
      flag = True

    if flag == False:
      ret = ret + marshalled_string[0: length - 1]
    else:
      ret = ret + marshalled_string     
        
      
     
    return ret
#Checks if strings first letter is i and then removes it if present.
#The string with 'i' remove is then converted to a integer.
def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    if marshalled_integer[0] == 'i':
      ret = ret + int(marshalled_integer[1:])

    return ret
#Method first removes the leading and trailing curly braces.
#It then takes the new string and splits it based on commas making a list.
#The list items are gone through and split by ':' to get key and value.
#The method then checks the first character to see if it is a int or dict.
#If not then it is sent to be unmarshall string.
#At the end the data is entered to the dict.
def __unmarshal_map(marshalled_map):


    ret = {}

    mm = marshalled_map[1:len(marshalled_map) - 1]
    
    list = mm.split(',')
    
    # TODO: Validate and parse using the data-type specific functions
    

    for i in list:
      temp = i.split(':', 1)
      key = temp[0]
      value = temp[1]
      
      if value.find('i') == 0:
        if value[1] == '-' or value[1].isnumeric():
          value =__unmarshal_integer(value)
          ret[key] = value
      
      elif value.find('{') == 0:
        value = unmarshal(value)
        ret[key] = value
      
      else:
        value = __unmarshal_string(value)
        ret[key] = value

    return ret

#The method checks if the input to the program is valid or acceptable format.
def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    
    if '{' not in marshalled_state or '}' not in marshalled_state:
        raise DeserializationError('Input is not valid for dictionary')
    
    if '{}' == marshalled_state:
        ret = {}
        return ret
    
    if len(marshalled_state) < 2:
        raise DeserializationError('Input is not long enough')
    
    if ':' not in marshalled_state:
        raise DeserializationError('Input is not valid for dictionary')
    
    return __unmarshal_map(marshalled_state)
