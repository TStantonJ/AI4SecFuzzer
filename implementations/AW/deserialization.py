from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    complex = False
    #check if string meets requirements of simple string
    lis = iter(enumerate(marshalled_string))
    for i,c in lis:
        if c == '%': #decode
            complex = True
            if i + 2 >= len(marshalled_string):#there are not 2 more characters for encoded character, cant decode
                raise DeserializationError("Input has invalid percent encoded char")
            raw = bytes.fromhex(marshalled_string[i+1:i+3])
            ret += raw.decode("ASCII")
            #skip the hex chars
            next(lis)
            next(lis)
        elif ord(c) == 44 or ord(c) == 123 or ord(c) == 125 or ord(c) < 32 or ord(c) > 126:
            raise DeserializationError("Input had illegal string char")
        else:
            ret += c
    
    if complex == False:
        if ret[-1] != "s":
            raise DeserializationError("NJOS simple string did not have an s at end of string")
        ret = ret[:-1]
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    #make sure it starts with 'i', again
    if marshalled_integer[0] != 'i':
        return __unmarshal_string(marshalled_integer)
    #remove the i
    marshalled_integer = marshalled_integer[1:]

    #Double check is numeric to be safe
    if marshalled_integer.isnumeric == False:
        return __unmarshal_string(marshalled_integer)

    ret = int(marshalled_integer)
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    if marshalled_map == "":
        return ret
    if len(marshalled_map.split(':')) == 1:
        raise DeserializationError('Input has no key')
    #take out key:values one at a time
    while len(marshalled_map) > 0:
        pair = marshalled_map.split(':', 1)
        
        # check key
        valid_key(pair[0])

        #take key out of marshalled_map
        marshalled_map = pair[1]
        
        split = marshalled_map.split(',', 1)

        #trim whitespace before value
        while split[0][0] == ' ' or split[0][0] == '\t' or split[0][0] == '\n' or split[0][0] == '\r' or split[0][0] == '\v' or split[0][0] == '\f':
            split[0] = split[0][1:]
        while split[0][-1] == ' ' or split[0][-1] == '\t' or split[0][-1] == '\n' or split[0][-1] == '\r' or split[0][0] == '\v' or split[0][0] == '\f':
            split[0] = split[0][:-1]
        
        #key is valid, now check type of value
        if split[0][0] == "{": #start of map, find matching }
            count = 0
            index = 0
            lis = iter(enumerate(marshalled_map))
            
            for i, c in lis:
                if c == '{':
                    count+=1                    
                if c == '}':                    
                    count-=1
                    if count == 0: #found the matching }
                        index = i
                        break
            if index == 0: # not found
                raise DeserializationError("Input has incomplete map")

            map = marshalled_map[:index+1]

            #ignore whitespace
            while map[0] == ' ' or map[0] == '\t' or map[0] == '\n' or map[0] == '\r' or map[0] == '\v' or map[0] == '\f':
                map = map[1:]
            while map[-1] == ' ' or map[-1] == '\t' or map[-1] == '\n' or map[-1] == '\r' or map[0] == '\v' or map[0] == '\f':
                map = map[:-1]

            #trim off the {}
            map =map[:-1]
            map = map[1:]
            
            #add unmarshalled map to ret
            ret[pair[0]] = __unmarshal_map(map)
            marshalled_map = marshalled_map[index+1:]
            
        elif split[0][0] != "i": #cannot be an int
            #take out the string from marshalled string
            ret[pair[0]] = __unmarshal_string(split[0])
            if len(split) == 1:
                marshalled_map = ""
            else:
                marshalled_map = split[1]
            
        else: #can be integer or string starting with i
            #check if rest of chars are a number
            if len(split[0]) > 1 and split[0][1] == '-': #negative number check
                if len(split[0]) > 2 and split[0][2:].isnumeric() == True: #is a negative number
                    ret[pair[0]] = __unmarshal_integer(split[0])
                else:
                    ret[pair[0]] = __unmarshal_string(split[0]) #string that starts with 'i-'
            elif len(split[0]) > 1 and split[0][1:].isnumeric(): #positive number check
                ret[pair[0]] = __unmarshal_integer(split[0])
            else:
                ret[pair[0]] = __unmarshal_string(split[0]) #string that starts with i
            
            #reduce marshalled_map while loop condition
            if len(split) == 1:
                marshalled_map = ""
            else:
                marshalled_map = split[1]
        
        if len(marshalled_map) > 0 and marshalled_map[0] == ",":
            marshalled_map = marshalled_map[1:]

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    if len(marshalled_state) == 0:
        raise DeserializationError('Input is empty string')
    if len(marshalled_state) == 1:
        raise DeserializationError('Input is only 1 character')

    #trim possible whitespace
    while marshalled_state[0] == ' ' or marshalled_state[0] == '\t' or marshalled_state[0] == '\n' or marshalled_state[0] == '\r' or marshalled_state[0] == '\v' or marshalled_state[0] == '\f':
        marshalled_state = marshalled_state[1:]
    while marshalled_state[-1] == ' ' or marshalled_state[-1] == '\t' or marshalled_state[-1] == '\n' or marshalled_state[-1] == '\r' or marshalled_state[0] == '\v' or marshalled_state[0] == '\f':
        marshalled_state = marshalled_state[:-1]

    # Needs to start with { and end with }
    if marshalled_state[0] != '{' or marshalled_state[-1] != '}':
        raise DeserializationError('Input is not wrapped with {{}}')
    
    #trim off outer dict
    marshalled_state = marshalled_state[:-1]
    marshalled_state = marshalled_state[1:]

    #Case for empty dict
    if len(marshalled_state) == 0:
        return {}

    #string has at least one char left, try to convert to dict
    return __unmarshal_map(marshalled_state)

def valid_key(key):
    #must be a str
    if type(key) != str:
        raise DeserializationError('Key is not a string')
    #validate chars
    for c in key:
        if c.isalpha() == False and c.isnumeric() == False:
            #check remaining valid chars
             if c != ' ' and c != '-' and c != '+' and c != '.' and c != "_":
                 raise DeserializationError("Input contains an illegal key: " + key)
    #valid :)
