from exceptions import DeserializationError
import urllib.parse # default with python3




################################
# String Unmarshalling
################################
def __unmarshal_string(marshalled_string):

    # variables
    ret = ''

    # TODO: Validate and convert
    # valid characters
    valid_chars = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$&'()*+-./:;<=>?@[]^_`|~ \\"""
    convert = ""
    get_encode = False

    # check if a complex string
    if ("%" in marshalled_string):

        # go character by character
        for item in marshalled_string:

            # add item if an encoded item
            if (get_encode == True):
                convert += item

                # check if all items are ready to convert
                if (len(convert) == 3):
                    ret += urllib.parse.unquote(convert)
                    # reset flags
                    get_encode = False
                    convert = ""

            # get ready to encode if % is found
            elif (item == "%"):
                get_encode = True
                convert += item

            # add if in the valid characters
            elif (item in valid_chars):
                ret += item

            # if not in any valid characters then it is invalid
            else:
                raise DeserializationError('Input value contains illegal character')

    # otherwise a simple string
    else:
        # check all items for valid characters
        for item in marshalled_string:
            if (item in valid_chars):
                ret += item

            # if not valid then error
            else:
                raise DeserializationError('Input value contains illegal character')

        # check for end nosj s
        if (ret[-1] == "s"):
            ret = ret[:-1]

        # otherwise if it doesn't have an s on the end, it is invalid
        else:
            raise DeserializationError('Input value does not contain ending simple string character')

    # return valid simple or complex string
    return ret


#############################################
# Integer Unmarshalling
#############################################
def __unmarshal_integer(marshalled_integer):
    
    # variables
    ret = 0
    temp = ''

    # TODO: Validate and convert
    # remove nosj i from end
    temp = marshalled_integer[1:]

    # convert to int
    ret = int(temp)

    # return valid int
    return ret


############################################
# Map Unmarshalling
############################################
def __unmarshal_map(marshalled_map):
    
    # variables
    ret = {}
    map_lst = []
    bracket_check = 0
    chunk = ""

    # TODO: Validate and parse using the data-type specific functions
    # check for empty map
    if (marshalled_map == "{}"):
        return ret

    # split dictionary by character
    # this section checks for correct number of brackets by looking character by character
    for bit in range(0, len(marshalled_map)):

        # break out of this if there are not any brackets 
        if ("{" not in marshalled_map):
            map_lst = marshalled_map.split(',')
            break

        # add to list if correct brackets and a comma is reached
        if (marshalled_map[bit] == "," and bracket_check == 0):
            map_lst.append(chunk)
            chunk = ""

        # check for correct number of brackets
        # check for opening bracket
        elif (marshalled_map[bit] == "{"):
            bracket_check += 1
            chunk += marshalled_map[bit]

        # check for closing bracket
        elif (marshalled_map[bit] == "}"):
            bracket_check += -1
            chunk += marshalled_map[bit]

        # add to chunk
        else:
            chunk += marshalled_map[bit]

        # check if final bracket
        if (marshalled_map[bit] == "}" and bracket_check == 0):
            map_lst.append(chunk)
            chunk = ""

        # check if the last item in the list
        elif (bit == len(marshalled_map)-1 and marshalled_map[bit] != "}"):
            map_lst.append(chunk)
            chunk = ""

    # if map_lst is empty then there was no valid input to add
    if (len(map_lst) < 1):
        raise DeserializationError('Input does not have valid bracket amount')

    # check each valid dictionary chunk
    # correct number of brackets are varified
    for item in map_lst:

        # make sure the item is not blank, otherwise skip
        whitespace = " \n\t\b\r"
        if (item == "" or item in whitespace):
            continue

        # check if key is in chunk
        if (":" not in item):
            raise DeserializationError('Input value does not contain a dictionary key')
        
        # split key by ":"
        data = item.split(":")

        # check if key is valid
        valid_chars = " -_+."
        key = ""
        for char in data[0]:
            # check for python whitespace
            if (char.isalpha() or char.isnumeric() or (char in valid_chars)):
                key += char
            else:
                raise DeserializationError('Input dictionary key is invalid')
        
        # add all other ':' seperated chunks together
        final_data = ""
        if (len(data) > 2):
            for i in data[1:]:
                final_data += ":" + i

        else:
            # otherwise just add the one chunk
            final_data = data[1]

        # remove extra ':' if there
        if (final_data[0] == ":"):
            final_data = final_data[1:]

        # strip off leading and end spaces from brackets
        if ('{' in final_data and '}' in final_data):
            final_data = final_data.strip()

        # check if input is a dictionary
        if (final_data[0] == "{" and final_data[-1] == "}"):
            
            # send to unmarshal for recursion
            ret[key] = unmarshal(final_data)

        # check if chunk is an integer
        elif (final_data[0] == "i" and (final_data[1:].isnumeric() or final_data[1] == '-')):

            # check if items after '-' are number
            if (len(final_data) >= 3 and final_data[2:].isnumeric()):

                # send to unmarshal int
                ret[key] = __unmarshal_integer(final_data)

            # send to int if lower than 2
            elif (len(final_data) <= 2):

                # send to integer
                ret[key] = __unmarshal_integer(final_data)

            # otherwise it is a string
            else:
                # send to string to check if complex or simple string
                ret[key] = __unmarshal_string(final_data)

        # check if chunk is a complex or simple string
        else:
            
            # send to string to perform more checks
            ret[key] = __unmarshal_string(final_data)

    # return correct converted nosj format
    return ret


#######################################
# Recursive and Initial Unmarshalling
#######################################
def unmarshal(marshalled_state):

    # check if input is none
    if marshalled_state is None:
        raise DeserializationError('Input is None')

    # check if input is type string
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    # check to make sure it is a dictionary
    if (len(marshalled_state) > 2):
        if (marshalled_state[0] != '{' and marshalled_state[-1] != '}'):

            # not a valid dictionary
            raise DeserializationError('Input is not a valid string dictionary')

        # take off brackets and send to map for processing
        marshalled_state = marshalled_state[1:]
        marshalled_state = marshalled_state[:-1]

    # send to map unmarshall for processing
    return __unmarshal_map(marshalled_state)
