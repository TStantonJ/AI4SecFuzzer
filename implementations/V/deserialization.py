from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert
    ret += marshalled_string
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    ret = marshalled_integer
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    if marshalled_map.__contains__("[") or marshalled_map.__contains__("]") :
        raise DeserializationError('Input has wrong symbol')
    # TODO: Validate and parse using the data-type specific functions
    
    marshalled_map = marshalled_map[1:-1] # decrease bracket level
    keyb = marshalled_map.find("{",0) # key for internal dicts
    keyc = marshalled_map.rfind("}",0) # key for internal dicts

    if marshalled_map.__contains__(":"):
        key = marshalled_map.find(":",0) #find a key point
        key2 = marshalled_map.find(",")  #find a key point for splitting data
        
        if marshalled_map[key+1] == "{": # check for internal dict
            keyc2 = marshalled_map.find("}",0) # find matching pair
            if keyc2 < key2: #checking for availability to recursion
                test_str = marshalled_map.split(",")
                for i in test_str:
                    dicti = __unmarshal_map("{" + i + "}") #increase level up to parse correctly
                    for key_dict, value in dicti.items():
                        ret[key_dict] = value
            else:
                ret[marshalled_map[key-1]] = __unmarshal_map(marshalled_map[keyb:keyc+1])
        

        if key2 != -1 and keyc == -1:
            test_str = marshalled_map.split(",")
            for i in test_str:
                dicti = __unmarshal_map("{" + i + "}") # #increase level up to parse correctly
                for key_dict, value in dicti.items():
                    ret[key_dict] = value
        else: # check for str or int data type 
            if marshalled_map[-1] == "s":
                ret[marshalled_map[key-1]] = __unmarshal_string(marshalled_map[key+1:-1])

            elif marshalled_map[key+1] == "i":
                ret[marshalled_map[key-1]] = __unmarshal_integer(int(marshalled_map[key+2:]))

            elif marshalled_map.__contains__("%2C"):
                comma = marshalled_map.find("%2C",0)
                tmp_str =  marshalled_map[:comma] + "," + marshalled_map[comma+3:]
                ret[marshalled_map[key-1]] = __unmarshal_string(tmp_str[key+1:]) 
            elif marshalled_map.__contains__("%00"):
                comma = marshalled_map.find("%00",0)
                tmp_str =  marshalled_map[:comma] + "\x00" + marshalled_map[comma+3:]
                ret[marshalled_map[key-1]] = __unmarshal_string(tmp_str[key+1:]) 
    elif  len(marshalled_map) > 0:
        raise DeserializationError('Input can not be parsed')

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    if not isinstance(marshalled_state,str):
        raise DeserializationError('Input is not a string')
    if not marshalled_state.__contains__("{") or not marshalled_state.__contains__("}"): # check for lack of one brackets
        raise DeserializationError('Input can not be parsed')

    return __unmarshal_map(marshalled_state)
