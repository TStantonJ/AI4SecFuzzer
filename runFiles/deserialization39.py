from exceptions import DeserializationError #used to throw error as needed
import urllib.parse #used in validating data for nosj compliance
def __unmarshal_string(marshalled_string):        
    #same as in marshalled_integer, converting to list for easier handling
    stringVals = [marshalled_string]
    
    #split on colon and load as key/val pair
    nosjDict = dict(string.split(':') for string in stringVals)
    #loop through items in dict
    for key, val in nosjDict.items():
        #check for percent encoding and unquote if needed
        if '%' in val:
            nosjDict[key] = urllib.parse.unquote(val)
        #convert and return as-is
        else:
            nosjDict[key] = val[:-1] #simple string if no %, remove 's'

    #return dict
    return nosjDict

def __unmarshal_integer(marshalled_integer):
    #get index of : (for split)
    keySplit = marshalled_integer.index('i')
    #slice 'i' from string
    marshalled_integer = marshalled_integer[0: keySplit : ] + marshalled_integer[keySplit + 1 : : ]

    #load string to list (easier to handle in dictionary)
    stringVals = [marshalled_integer] 
                 
    #split on colon and load as key/val pair
    nosjDict = dict(string.split(':') for string in stringVals)
    #convert vals to int
    for key, val in nosjDict.items():
        nosjDict[key] = int(val) 

    return nosjDict

def __unmarshal_map(marshalled_map):
    
    #remove nosj brackets (not needed regardless of type)
    marshalled_map = marshalled_map[1:-1]
    
    # Parse string **THIS MAY NEED TO MOVE TO MARSHALLED_STATE
    if ':i' in marshalled_map:
        return __unmarshal_integer(marshalled_map)
    
    else:
        return __unmarshal_string(marshalled_map)
     

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    invalidChar = ['%', ',', '(0x2C', '{', '}'] #list of illegal chars
    isInvalid = [char in invalidChar for char in marshalled_state]

    if marshalled_state[0] != '{' and marshalled_state[len(marshalled_state) - 1] != '}':
        raise DeserializationError('Input is not in nosj format')


    if isInvalid == True:
        raise DeserializationError('Input is an invalid string')
    # TODO: Validate things about the overall marshalled state
    
    return __unmarshal_map(marshalled_state)
