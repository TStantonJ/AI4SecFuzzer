from exceptions import DeserializationError
import re

def __unmarshal_string(marshalled_string):

    ret = ''
    is_simple = True # simple until proven guilty
    if '%' in marshalled_string:
        is_simple = False

    if is_simple:
        if marshalled_string[-1] != 's':
            raise DeserializationError(f"'{marshalled_string}' does not match nosj STRING restraints.")

        if is_allowed(marshalled_string[0:-1]):
            return marshalled_string[0:-1] # removes trailing s for simple strings
        else:
            raise DeserializationError(f"'{marshalled_string[0:-1]}' contains illegal character and does not match nosj STRING restraints.")

    else:
        # entering here means my parser has decided that the string in a complex on
        # remove all instances of % to check if there are any illegal characters

        if not is_allowed(marshalled_string,skip_parenth=True):
            raise DeserializationError(f"'{marshalled_string}' contains illegal character and does not match nosj STRING restraints.")
        i = 0
        while i < len(marshalled_string):
            if marshalled_string[i] == "%":
                for each in marshalled_string[i+1:i+3]:
                    if each.lower() not in ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f']: # legal chars for hex
                        raise DeserializationError(f"percent encoded '%{marshalled_string[i+1:i+3]}' contains illegal character and does not match nosj STRING restraints.")
                ret += chr(int(marshalled_string[i+1:i+3],16)) #decodes the percent encoding to \x__ format
                i += 2
            else:
                ret += marshalled_string[i]
            i += 1
        # ret += marshalled_string[i]

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0
    i = 0

    # takes care of leading white space
    while marshalled_integer[i] == ' ':
        if i == len(marshalled_integer)-1:
            raise DeserializationError(f"'{marshalled_integer[i:]}' does not match nosj INTEGER restraints.")
        i += 1
    marshalled_integer = marshalled_integer[i:]

    # now there should be no whitespace on the front
    # checks format
    if marshalled_integer[0] != 'i':
        raise DeserializationError(f"'{marshalled_integer}' does not match nosj INTEGER restraints.")
    if marshalled_integer.count('-') > 1:
        raise DeserializationError(f"'{marshalled_integer}' does not match nosj INTEGER restraints.")
    if not re.match('[-+]?[0-9]',marshalled_integer[1:]):
        raise DeserializationError(f"Integer value '{marshalled_integer[1:]}' doesn't match nosj restraints.")
    if '-' in marshalled_integer[1:] and marshalled_integer[1:][0] != '-':
        raise DeserializationError(f"Integer value contains '-', but is not at the start of number. This doesn't match nosj restraints.")
    else:
        num = marshalled_integer[1:].lstrip().rstrip() #strips any whitespace on both sides of strings so that we can see if there is whitespace inbetween numbers
        if ' ' in num:
            raise DeserializationError(f"White space between numbers. This doesn't match nosj restraints.")
        ret = int(num)

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    # some catches for edge cases
    if marshalled_map == '':
        raise DeserializationError("empty boi")
    if marshalled_map == '{}':
        return ret

    # checks that brackets adhere to format
    if marshalled_map.count('{')-marshalled_map.count('}') != 0:
        raise DeserializationError("brackets do not match for nosj format")
    if marshalled_map[0] != '{':
        raise DeserializationError("incorrect format for nosj")

    # a map is defined as { }
    # go till find next map then put that in __unmarshal_map to validate
    # ex. '{a: {b:i1} ,c: {d:i2} }'

    i = 1
    key = ''

    while i < len(marshalled_map):
        # searching for new keys
        # validating key format
        if marshalled_map[i] == '}':
            raise DeserializationError(f"Format does not match nosj restraints.")
        if marshalled_map[i] != ':':
            key += marshalled_map[i]
        else:
            # first check that the key is valid
            if not re.match(r'^[\w\-+. ]*$',key):
                raise DeserializationError(f"Key value '{key}' doesn't match nosj restraints.")


            # Now process and validate value
            value = ''
            i += 1
            LPC = 0 # Left parenth count
            RPC = 0 # Right parenth count
            new_map_start = 0

            # searching for values
            while True:
                # This next part is complex
                # need to find next } but if there is another { need to find two }} ect.
                # just searching for maps aka {} or values

                # THIS PORTION DEALS WITH MAPS RECURSIVELY
                if marshalled_map[i] == '{':
                    if LPC == 0:
                        new_map_start = i

                    LPC += 1
                    i += 1
                    continue
                if marshalled_map[i] == '}':
                    RPC += 1
                    if RPC == LPC:
                        # then complete map is found put that sucker in __unmarshal_map(marshalled_map)
                        i += 1
                        internal_dict = __unmarshal_map(marshalled_map[new_map_start:i])
                        ret[key] = internal_dict
                        break_loop = False
                        while i < len(marshalled_map):
                            if marshalled_map[i] == ',':
                                break_loop = True
                                break
                            if marshalled_map[i] == '}':
                                return ret
                            if marshalled_map[i] == ' ':
                                i += 1
                                continue
                            else:
                                raise DeserializationError(DeserializationError("unexpected value"))

                        if break_loop:
                            key = ''
                            break

                    if RPC > LPC:
                        raise DeserializationError("parentheses out of wack")


                # THIS PORTION DEALS WITH IF A MAP HASNT BEEN FOUND
                # if we've made it here the parser has determined that there is not a map so its either a string or int
                if LPC == 0 and RPC == 0: # removed marshalled_map[i] != ' ' and

                    # ex. '{a: {b:i1} ,c: {d:i2} }'
                    # this means its not {,},or whitespace so...
                    # its the start to a string of some sort...
                    # first get the whole shebang.
                    # getting the whole thing means grabing untill ','

                    # will determine what kind of value is found and return the json format for that data type
                    def determine_type(value):
                        if '%' in value:
                            internal_dict = __unmarshal_string(value)

                        value = value.rstrip()

                        if value[-1] == 's':

                            internal_dict = __unmarshal_string(value) #will be validate inside method
                        elif '%' in value:
                            internal_dict = __unmarshal_string(value)
                        else:
                            internal_dict = __unmarshal_integer(value)

                        return internal_dict

                    start_of_obj = i

                    outer_break = False
                    while i < len(marshalled_map):
                        if marshalled_map[i] == ',':
                            value = marshalled_map[start_of_obj:i]
                            ret[key] = determine_type(value)
                            key = ''
                            outer_break = True
                            break
                        elif marshalled_map[i] == '}':
                            value = marshalled_map[start_of_obj:i]
                            ret[key] = determine_type(value)
                            return ret
                        i += 1
                    if not outer_break:
                        raise DeserializationError("reached end without finding ',' or '}'")
                    else:
                        break
                i += 1
        i += 1

    return ret

def check_key_format(key):
    if not re.match(r'^[\w\-+. ]*$',key):
        raise DeserializationError("incorrect format for nosj key")

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # overall marshalled state is validated within __unmarshal_map()

    return __unmarshal_map(marshalled_state)

# checks that all characted are allowed by nosj format
# optional: allow parentheses
def is_allowed(s, skip_parenth = False):
    if skip_parenth:
        return all((ord(c) < 128 and ord(c) not in [44,123,125]) for c in s)
    else:
        return all((ord(c) < 128 and ord(c) not in [37,44,123,125]) for c in s)
