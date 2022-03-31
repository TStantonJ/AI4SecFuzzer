from exceptions import DeserializationError

import re

def __unmarshal_string(marshalled_string):
    ret = ''
    #Find Length of string strip off ending S
    str_length = len(marshalled_string)
    #If simple string, strip off S
    string_check = re.search(r'^\D', marshalled_string)
    if string_check == None:
        str_holder = (marshalled_string[:str_length-1])
    else:
        str_holder = (marshalled_string[:str_length-1])
    ret = str_holder
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    #Strip off i
    int_holder =(marshalled_integer[1:])
    #Search for Neg
    int_check = re.search(r'\W', int_holder)
    #Cast to int for sum
    int_holder = int(int_holder)
    #If neg then sub from ret, else just add it
    if int_check == True:
        ret -= int_holder
    else:
        ret += int_holder
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    tmp_map = str(marshalled_map)

    #Vars to hold key and value pairs
    key_holder = ''
    value_holder = ''
    #Flag to alert what point in the string we are at
    key_flag = 0
    valueStart_flag = 0
    valueEnd_flag = 0
    colon_flag = 0
    #Counters to keep track of place when finding values
    postKey_counter = 0
    place_counter = 0

    #Itterate through entire string
    for map_pointer in tmp_map:
        #If we located a key
        if key_flag == 1:
            #assign current lcoation to key
            key_holder = map_pointer
            key_flag = 0
            postKey_counter = 0

        if colon_flag == 1:
            valueStart_flag = 1
            colon_flag = 0
        if valueStart_flag == 1:
            #Itterate through value to find end or next key
            for tmp_pointer in tmp_map[place_counter:]:

                if tmp_pointer == '{':
                    break
                elif tmp_pointer == '}':
                    break
                else:
                    postKey_counter += 1
            valueStart_flag = 0
            #Strip out value to pass on
            pass_var = marshalled_map[place_counter:place_counter+postKey_counter]
            #If its an int then pass to int function
            if pass_var.startswith('i'):
                value_holder = __unmarshal_integer(pass_var)
                ret[key_holder] = value_holder
                postKey_counter = 0
            #Else pass to string
            else:
                value_holder = __unmarshal_string(pass_var)
                ret[key_holder] = value_holder
                postKey_counter = 0

        if map_pointer == ':':
            colon_flag = 1
            
        #Check if location is the start of key
        if map_pointer == '{':
            key_flag = 1

        place_counter += 1

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)
