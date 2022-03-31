#Deserialization error is imported so that an exception can be raised when the source data
#    fails to adhere to the required source data format.
#The json module is imported because the nosj format is similar to the json format this module
#    works with. The json module functions allow the code to be simpler, safer, and more readable
#    since any personal code would likely have been less readable and accurate.
from exceptions import DeserializationError
import json

def __unmarshal_string(marshalled_string):
    '''__unmarshal_string receives one string, determines if it\'s a simple string or a complex one,
    then reverts it back to it\'s plain text form.'''

    specialChar = []

    #This if statement breaks up the function into two sections that deal with complex
    #    and simple strings separately.
    if "%" in marshalled_string:
        #This first for loop identifies and stores all of the special characters in a
        #    given complex string. Since all the special characters in the nosj format
        #    are denoted with a %, we can use the % to identify each character that occurs
        #    in the string.
        for index, char in enumerate(marshalled_string):
            if char == "%":
                specialChar.append(marshalled_string[index+1:index+3])
       
        #This for loop takes each of special characters in the string and replaces them
        #    with them with the actual character.
        for char in specialChar:
            marshalled_string = marshalled_string.replace("%" + char, chr(int(char, 16)))

        ret = marshalled_string
                
    else:
        #This section fixes simple strings. Since complex strings are guaranteed to contain
        #    a %, we know that all of the strings that don't contain them are simple strings.
        #    (Note: The previous assumption about simple strings assumes that marshalled integers
        #    are not being wrongfully passed to this function.) Fixing these strins is as simple
        #    as removing the trailing s.
        ret = marshalled_string[:-1]


    return ret

def __unmarshal_integer(marshalled_integer):
    '''__unmarshal_integer takes in a string that contains an integer in the nosj format
    and returns the integer as an int'''

    #Integers in the nosj format have a leading i follows by the int. This data can be
    #    converted to the int data type by stripping the 'i' and converting the data
    #    type.
    ret = int(marshalled_integer.strip('i'))

    return ret

def __unmarshal_map(marshalled_map):
    '''__unmarshal_map takes in a dictionary using the nosj format and passes the keys\' values to
    other functions for decoding.'''
    ret = {}

    #Since this function is running on the assumption that it is being passed an nosj
    #   the function iterates through the key value pairs. Using data type checks
    #   and other criteria, the function determines which function needs to handle
    #   the value.

    for key, value in marshalled_map.items():

        #The keys in the dictioanry need to be validated before parsing the values
        #    in order to prevent unnecessary processing.
        for char in key:
            if ord(char) < 20 or ord(char) > 126:
                raise DeserializationError('Key contains a nonprintable character(s)')
            if char in "!\"#$%&'()*,/:;<=>?@[\\]^`{|}~":
                raise DeserializationError('Key contains an illegal character')


        #Since complex strings are the only type of data that contain percent signs
        #    and each complex string is guaranteed to have a percent sign, we
        #    can check to see if they are present in the data and send the value
        #    to the string function.
        if isinstance(value, str) and "%" in value:
            ret[key] = __unmarshal_string(value)

        #Since nosj integers are represented by a string we have to check the first and
        #    last character to make that the string contains the integer identifier
        #    and does not have the string identifier. Once an integer is identified
        #    it's sent to the __unmarshal_integer function.
        elif isinstance(value, str) and value[0] == 'i' and value[-1] != 's':
            ret[key] = __unmarshal_integer(value)

        #This is the check for simple strings. Since complex strings and integers have already
        #    been flagged we just have to check if the string has the proper indicator as the
        #    last character.
        elif isinstance(value,str) and value[-1] == 's':
            ret[key] = __unmarshal_string(value)

        #If a dictionary is discovered the function is recursively called so the nested strings 
        #    and integers can be processed.
        elif isinstance(value, dict):
            ret[key] = __unmarshal_map(value)

        #The else statement signals that there's a problem with the data. In each of the previous
        #    ifs the date type of the value was checked. This means that any invalid data type
        #    would reach this section and signal an error. This also applies to improperly formatted
        #    strings.
        else:
            raise DeserializationError('Invalid data format. The structure contains an invalid data type or improperly formatted data')


    return ret

def unmarshal(marshalled_state):
    '''unmarshal takes in a string that represents a dataset in the nosj format and returns a dictionary
    of that data as decoded strings, integers, and dictionaries'''

    #Raise error if there is no input
    if marshalled_state is None:
        raise DeserializationError('Input is None')

    #Raise error if the input isn't a string
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    #The input is a string that has the basic structure of a dictionary.
    #    Without a starting brace the structure will be broken and fail.
    if "{" not in marshalled_state:
        raise DeserializationError('Input is missing a starting brace')
    
    #The input must have matching braces to be valid, so an error is raised
    #    if there aren't an equal amount of opposing braces. This doesn't
    #    guarantee the form is right, but it does identify some syntax errors.
    if marshalled_state.count("{") != marshalled_state.count("}"):
        raise DeserializationError('Input has mismatching braces')

    #This checks to see if the dictionary is empty. Since you can have n number
    #    of whitespaces in a valid empty dictionary, the spaces are stripped 
    #    and the structure is compared to {}. If the input is empty, there's no
    #    need to perform additional processing. Just return an empty dictionary.
    if marshalled_state.replace(" ","") == "{}":
        return {}

    #The only valid use case for a dictionary to not have a colon is if the dictionary
    #    is empty. Since that case has been handled, any input at this point would need
    #    at least one colon. If there are no colons, there's a data problem.
    if ":" not in marshalled_state:
        raise DeserializationError('Input is missing colon to denote key value pairing')


    #In this next block quotes are added around each element in the nosj string.
    #    This is done so the json module's functions can parse the string.
    #    THe difficult part of this sectionmaking sure there are no misplaced
    #    quotes. The most problematic is the } character. A quote is needed 
    #    before } to denote the end of a value, but it's also possible for
    #    multiple }s to appear next to each other. The variable doubleBraceFlag
    #    represents the presence of two or more back to back } at the current
    #    location in the in string. If the flag is true a quote won't be added,
    #    but if the flag is false a quote will be placed.
    #    A similar but less complex check occurs for colons. If the value for a
    #    given key is a dict, the following quote isn't needed. Non dict values
    #    require a quote, so we check what the following character is before placing
    #    quote.
    parsableState = ""
    doubleBraceFlag = False

    for index, char in enumerate(marshalled_state):
        if char == '{':
            parsableState += '{"'
            doubleBraceFlag = False
        elif char == ':' and marshalled_state[index+1] != "{":
            parsableState += '":"'
            doubleBraceFlag = False
        elif char == ':':
            parsableState += '":'
            doubleBraceFlag = False
        elif char == ',' and marshalled_state[index-1] != "}":
            parsableState += '","'
            doubleBraceFlag = False            
        elif char == ',':
            parsableState += ',"'
            doubleBraceFlag = False
        elif char == '}' and not doubleBraceFlag:
            parsableState += '"}'
            doubleBraceFlag = True
        elif char == '}' and doubleBraceFlag:
            parsableState += char
        else:
            parsableState += char

    marshalDict = json.loads(parsableState)

    return __unmarshal_map(marshalDict)
