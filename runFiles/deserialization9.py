from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
  check = "ABCDFabcdf0123456789"
  if marshalled_string.find("%") == -1 and marshalled_string[-1] == "s":
    marshalled_string = marshalled_string[:-1]
    print(marshalled_string)
  else: 
    i = 0
    while i < len(marshalled_string):
      if marshalled_string[i] == "%":
        print(i)
        if marshalled_string[i+1] not in check and marshalled_string[i+2] not in check:
          raise DeserializationError("Error")
        else:
          marshalled_string = marshalled_string.replace(marshalled_string[i:i+3],chr(int(marshalled_string[i+1:i+3],16)))
          print(marshalled_string)
      i += 1

  return marshalled_string
  #done



  def __unmarshal_integer(marshalled_integer):
    ret = 0
    checkString = "0123456789-"
    for characters in marshalled_integer:
        if characters not in checkString and marshalled_integer[0] == "i":
            if "-" in marshalled_integer:
                ret = int(marshalled_integer[1:])
            else:
                ret = int(marshalled_integer[1:])
    return ret 
#done

    

  def __unmarshal_map(marshalled_map):
    key = ''
    array = {}
    if type(key) == str:
      i = 0
      while i < len(map): # for the string sections
        index = map.find(":")
        key = map[:index]
        #print(key)
        for l in range(len(map)): # checks for {}
          if map[l] == "{":
           side += 1
          elif map[l] == "}":
           side -= 1
          elif side > 0:
           continue
          if value.find("{") != -1 or value.find("}") != -1: # type checking for dict
             value = unmarshal_map(value)
          elif value.find("%") != -1:   # type checking for string
             value = unmarshal_string(value)
          elif value[len(value)-1] == "s":  # basic string
            value = unmarshal_string(value)
          elif value[0] == "i":
            value = unmarshal_integer(value)
            result[key] = value
            #print(result)
          #print(value)
    return array    
     

  

    def unmarshal(marshalled_state):
      if marshalled_state is None:
        raise DeserializationError('Input is None')
      if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

      return __unmarshal_map(marshalled_state)

