from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    complex_string = False
    #convert one percent-encoded representation into character
    for val in marshalled_string:
        if val == '%':
            complex_string = True
            replacement = chr(int(marshalled_string[marshalled_string.index('%')+1:marshalled_string.index('%')+3],16))
            ret = marshalled_string[:marshalled_string.index('%')] + replacement + marshalled_string[marshalled_string.index('%')+3:]
    if not complex_string:
        ret = marshalled_string[:-1]
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    #converts into integer not include 'i'
    ret = int(marshalled_integer[2:])
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    if marshalled_map == '{}':
        return ret
    #removes outer {}
    marshalled_map = marshalled_map[1:-1]

    #splits string into list of inputs
    # example: {a:123,b:345} becomes list ['a:123','b:345'] 
    if (marshalled_map.find(',') != -1):
        temp_map_list = marshalled_map.split(",")
    #if there is only one entry into the dictionary
    else:
        temp_map_list = [marshalled_map]
    #go through each index in the list and do the corresponding unmarshal function
    for item in temp_map_list:
        #checks to see if it's in the correct key:value format required for a dictionary
        if (item.find(':') != 1):
            raise DeserializationError('Not it correct key:value format')
        #checks to see if key is in dictionary, dictionaries can't have duplicate keys
        key = item[:item.find(':')]
        if key in ret.keys():
            key = ret.val
            raise DeserializationError('Dictionary cannot have duplicate keys.')
        #value is an integer - taking into account positive and negative numbers
        if (item.find(":i")== 1):
            ret[key] = __unmarshal_integer(item[item.find(':'):])
        #value is a map
        elif (item[-1] == '}'):
            ret[key] = __unmarshal_map(item[item.find(':')+1:])
        #value is a string
        else:
            ret[key] = __unmarshal_string(item[item.find(':')+1:])
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if (marshalled_state.find('{') == 1 and marshalled_state.find('}') == 1):
        raise DeserializationError('Not in correct format')
    if not all(ord(c) < 128 for c in marshalled_state):
        raise DeserializationError('Input is not ASCII.')
    
    return __unmarshal_map(marshalled_state)
