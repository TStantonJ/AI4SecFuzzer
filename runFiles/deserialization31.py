from exceptions import DeserializationError


def __unmarshal_string(marshalled_string):
  check_string  = "ABCDFabcdf0123456789"
  result = ''
  flag = False
  
  for char in marshalled_string:
    if char == "%":
      flag = True

  #check it the marshalled_string is validate and determ if it is simple or complex by check it has "s" at end or contain least one "%"
  if flag == True:
    m = 0
    while m < len(marshalled_string):
      newchar = marshalled_string[m]
      if marshalled_string[m] == "%":
        new = marshalled_string[m:m+3]
        new_marshalled_string = new[1:]
        if new[1] not in check_string or new[2] not in check_string:
          raise DeserializationError("Error statement")
          #print("it is not validate")
        else:
          old_marshalled_string = chr(int(new_marshalled_string,16))
          result += old_marshalled_string
        marshalled_string = marshalled_string[:m+1] + marshalled_string[m+3:]
      else:
        result += newchar
      m += 1
  elif marshalled_string[-1] == "s":
    result = marshalled_string[:len(marshalled_string)-1]
    #print(result)
  else:
    #print("not formating")
    raise DeserializationError("Error statement")
  #print(result)

    

  return result

def __unmarshal_integer(marshalled_integer):
  check_string = "0123456789-"
  string_int = 0
  flag = False

  for char in marshalled_integer[1:]:
    if check_string.find(char) == -1:
      flag = True
    
  if flag == False and marshalled_integer[0] == "i" and marshalled_integer[1:].find("-") == -1:
    marshalled_integer = marshalled_integer[1:]
    string_int = int(marshalled_integer)
    #print(string_int)
    #print("it is pasitive valid int string")
  elif flag == False and marshalled_integer[0] == "i" and marshalled_integer[1] == "-" and marshalled_integer[2:].find("-") == -1:
    marshalled_integer = marshalled_integer[1:]
    string_int = int(marshalled_integer)
    #print(string_int)
    #print("it is negative validate int string")
  else:
    #print("it is not valite formate")
    raise DeserializationError("Error statement")

  return string_int

def __unmarshal_map(marshalled_map):
  result = {}
  
  # check the validate marshalled_ map formate first and then convert the key with the vaule with the formate with the py version
  if len(marshalled_map) == 0:
    raise DeserializationError("Error statement")
  else:
    if len(marshalled_map[1:len(marshalled_map)-1]) != 0 and type(marshalled_map) == str and marshalled_map[0] == "{" and marshalled_map[len(marshalled_map)-1] == "}":
      map_string = marshalled_map[1:len(marshalled_map)-1] + ','
      flag = False
      leftbrackets = 0
      count = 0
      vali_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 +-_."
      m = 0
      while m < len(map_string):
        index = map_string.find(":")
        key = map_string[:index]
        map_string = map_string[index+1:]
        for char in key:
          if vali_key.find(char) == -1:
            flag = True         
        #print(key)
        
        if flag == True and type(key) == str:
          raise DeserializationError("Error statement")
        else:
          for c in range(len(map_string)):
            if map_string[c] == "{":
              leftbrackets += 1
            elif map_string[c] == "}":
              leftbrackets -= 1
            elif leftbrackets > 0:
              continue
            elif map_string[c] == ',':
              count = c
              value = map_string[:c]
              if value.find("{") != -1 or value.find("}") != -1:
                value = __unmarshal_map(value)
                result[key] = value
                #print("it is map")
              elif value.find("%") != -1:
                value = __unmarshal_string(value)
                result[key] = value
                #print(result)
              elif value[len(value)-1] == "s":
                value = __unmarshal_string(value)
                result[key] = value
                #print(result)
              elif value[0] == "i":
                value = __unmarshal_integer(value)
                result[key] = value
                #print(result)
              else:
                raise DeserializationError("Error statement")
              #print(value)
              break
          map_string = map_string[count+1:]
          #print(map_string)

      m += 1
  
    
    elif len(marshalled_map[1:len(marshalled_map)-1]) == 0 and type(marshalled_map) == str and marshalled_map[0] == "{" and marshalled_map[len(marshalled_map)-1] == "}":
      return result
    else:
      raise DeserializationError("Error statement")
    
  return result 

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
