from exceptions import DeserializationError

def is_hex_number_digits(c):
    # used for nosj percent decoding
    return (c >= '0' and c<='9' ) or (c >= 'A' and c<='F' ) or (c >= 'a' and c<='f' )

# test if nosj string s is legit
def is_legit_nosj_string(s):
    if  ( s[-1]=='s' and all ( c not in ['%', ',', '{', '}'] for c in s ) and all (c.isprintable() for c in s) ) or ( any ( c == '%' for c in s) and all (c.isprintable() for c in s) ):
        return True
    else:
        return False

def __unmarshal_string(marshalled_string):


    # input must be a python string
    if not isinstance(marshalled_string, str):
        raise DeserializationError("Argument is not a string")

    # remove spaces on either end
    marshalled_string = marshalled_string.strip()

    # length of input cannot be less than 2. i.e., marshalled string cannot be empty
    if len(marshalled_string) <=1:
        raise DeserializationError("Invalid nosj string")

    # test trailing string indicator
    if marshalled_string[-1] !='s':
        if all( c != '%' for c in marshalled_string):
            raise DeserializationError("Invalid nosj string")

    # strip the trailing s if simple case
    if all( c != '%' for c in marshalled_string):
        marshalled_string=marshalled_string[:len(marshalled_string)-1]
    
    # input string must be printable
    if not marshalled_string.isprintable():
        raise DeserializationError("Invalid nosj string")

    is_simple = True
    non_simple_characters=[',', '{', '}']
    
    for i in range(len(marshalled_string)):
        if marshalled_string[i] in non_simple_characters:   # check validity of each character
            raise DeserializationError("Invalid nosj string")
        elif marshalled_string[i] == '%':   # find if athe simple string case
            is_simple = False
    
    # simple string: simply return the string as it's ready
    if is_simple:
        return marshalled_string
    
    # complex case
    string_parts=marshalled_string.split('%')
    
    converted_string_parts=[]
    
    # split the string by "%". Convert each sengments, and join the results
    if marshalled_string[0]=='%': # '%1234%ef jjj' will be split to ['', '1234', 'ef jjj']
        start_counter=1
    else:   # 'hh%1234%ef jjj' will be split to ['hh', '1234', 'ef jjj']
        start_counter=1
        converted_string_parts.append(string_parts[0])
    
    for i in range(start_counter,len(string_parts)):
        if len(string_parts[i]) < 2:  # not sufficient for URL format percent-encoded case
            raise DeserializationError("Invalid nosj string")

        # separate the percent-encoded part from the rest
        escaped_part=string_parts[i][:2]
        non_escaped_parts=string_parts[i][2:]
        
#        if all( c in string.hexdigits for c in escaped_part): # percent-encodedpart is legit
        if all(is_hex_number_digits(c) for c in escaped_part):  # percent-encodedpart is legit

            converted_string_parts.append(chr(int(escaped_part,16)) + non_escaped_parts)
        else:
            raise DeserializationError("Invalid nosj string")

    return ''.join(converted_string_parts)
    
    
    #ret = ''

    # TODO: Validate and convert

    #return ret

def __unmarshal_integer(marshalled_integer):
    # argument must be string
    if not isinstance(marshalled_integer, str):
        raise DeserializationError("Invalid argument")

    # input is string
    is_negative = False
    
    if len(marshalled_integer) >=2:
        if marshalled_integer[0] == 'i':    # leading character must be "i"
            marshalled_integer=marshalled_integer[1:]   # strip the leading "i"

            if len(marshalled_integer) >=2: # if a negative number, the remained length must be at least 2
                if marshalled_integer[0]=='-':  # negative sign
                    is_negative=True
                    marshalled_integer=marshalled_integer[1:]   # obtain absolute value
                    
            for i in range(len(marshalled_integer)):    # check all characters are digits
                if not ( marshalled_integer[i] >='0' and marshalled_integer[i] <='9' ):
                    raise DeserializationError("Invalid nosj integer format")

            integer_value = int(marshalled_integer) # convert string to integer
            
            if is_negative: # make it negative
                integer_value = -integer_value
                
            return integer_value
            
        else:
            # first charcter is not 'i'
            raise DeserializationError("Invalid nosj integer")
            
    else:   # length must be at least 2
        raise DeserializationError("Invalid nosj integer format")
    
    
#    ret = 0

    # TODO: Validate and convert

#    return ret

def __unmarshal_map(marshalled_map):

    dict1 = {}  # result initialization

    # argument must be string
    if not isinstance(marshalled_map, str):
        raise DeserializationError("Invalid map argument")

    # remove spaces on either end
    marshalled_map=marshalled_map.strip()

    # shortest possible is "{}". the length is 2
    if len(marshalled_map) < 2:
        raise DeserializationError("Invalid nosj map format")


    # being a map, the first and last characters must be brackets
    if not (marshalled_map[0] == '{' and marshalled_map[-1] == '}'):
        raise DeserializationError("Invalid nosj map format")

    # strip the brackets {...}
    marshalled_map=marshalled_map[1:len(marshalled_map)-1]

    left_righthalf=marshalled_map.strip()   # initialize left_righthalf to be the complete string. The idea is to divide the string into valid segmented separated
                                            # by ",", and process each segment indivisually until the remaining valid segment after the first "," of left_righthalf is empty
    while left_righthalf !='':

        split_rest=left_righthalf.split(':',1)  # obtain the key

        if len(split_rest)==2:  # ":" must exist. rightvalue is the string part after ":"
            firstkey, rightvalue = split_rest
        else:
            raise DeserializationError("Invalid nosj map format")

        firstkey=firstkey.strip()   # remove spaces on ends
        
        if firstkey == '':  # key is blank
            raise DeserializationError("nosj map key empty")

        rightvalue=rightvalue.strip()   # remove end spaces

        if rightvalue != '':
            if rightvalue[0] == '{':    # segment is a submap

                count_left_bracket = 1

                # scan for maching '}' to get a complete map
                for right_bracket_position in range(1, len(rightvalue)):
                    if rightvalue[right_bracket_position] == '{':
                        count_left_bracket += 1
                    elif rightvalue[right_bracket_position] == '}':
                        count_left_bracket -= 1

                    if count_left_bracket == 0:
                        break;

                if count_left_bracket !=0 :
                    raise DeserializationError("Brackets mismatch")
                    return

                firstvalue = rightvalue[:right_bracket_position + 1]    # this is the map value

                # the rest of maps to be processed
                left_righthalf = rightvalue[right_bracket_position + 1:].strip()

                if left_righthalf != '':    # remained part still exists
                    left_righthalf_split = left_righthalf.split(',', 1)   # find the dividing point by ","

                    if len(left_righthalf_split) == 2:  # list has 2 elements
                        if left_righthalf_split[0].strip() != '':  # there's some chars after '}' in fornt of ','
                            raise DeserializationError("Invalid nosj map format")
                            return
                        else: 
                            left_righthalf = left_righthalf_split[1]
                    else:  # list has 1 element. This means "," is immediately after "}"
                        left_righthalf = left_righthalf_split[0]

                dict1[firstkey] = __unmarshal_map(firstvalue)   # create a map element

            else:   # segment is integer or string
                firstvalue_1stpart = rightvalue.split(',',1)[0].strip()

                #if ( firstvalue_1stpart[-1]=='s' and all( c not in ['%', ',', '{', '}'] for c in firstvalue_1stpart ) and all (c.isprintable() for c in firstvalue_1stpart) ) or ( any ( c == '%' for c in firstvalue_1stpart) and all (c.isprintable() for c in firstvalue_1stpart) ):  # segment is simple or complex string
                if is_legit_nosj_string(firstvalue_1stpart):
                    marshalled_firstvalue=__unmarshal_string(firstvalue_1stpart)

                elif firstvalue_1stpart[0]=='i':    # segment is integer
                    marshalled_firstvalue=__unmarshal_integer(firstvalue_1stpart)
                else:
                    raise DeserializationError("Invalid nosj map format")

                if len(rightvalue.split(',', 1)) > 1:   # there's something remained for next stage of processing
                    left_righthalf=rightvalue.split(',',1)[1].strip()
                else:   # complete nosj has been processed
                    left_righthalf=''   

                dict1[firstkey] = marshalled_firstvalue
        else:
            raise DeserializationError("Invalid nosj map format")   # map can't be empty
    
    return dict1

#ret = {}

    # TODO: Validate and parse using the data-type specific functions

#    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state

    return __unmarshal_map(marshalled_state)


#print(__unmarshal_map('{a:is,b:{a:i-1,c:%89123%20%2fs},d:i-123,e:{a:{b:{c:i123}}}}')) #,{}))
#print(__unmarshal_map('{e:{a:{b:{c:i123}}}')) #,{}))
#print(__unmarshal_map('{a:ab<cd>efs}'))

#print(__unmarshal_map('{}'))

#print(__unmarshal_map({'a': 'ab\x00ef'}))

#print(__unmarshal_map('{a:{b:i1},c:{d:i2}}'))

#{'a': {'b': 1}, 'c': {'d': 2}}
