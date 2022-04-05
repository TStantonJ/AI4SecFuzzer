"""
YOU MAY CHANGE THIS FILE IN ANY WAY YOU SEE FIT.
"""
import base64
from curses import A_ALTCHARSET
from pickletools import markobject
import random
import argparse
import sys
import string
import urllib.parse
import os.path
from os import path
import random

import preprocessor

#TODO:
# New matrix recording system (TS)
# Implement matrix output
# Add stocastic chance to pick incorrect value in string and int functions(CB)
# Add global configuration values for error_chance, recursion depth limit
# Move error chance from generate_strings to its sub functions
# Add recusion depth limit _make_map(CT)

# Import the given implementations
marshal_implementation_container = []
unmarshal_implementation_container = []
if path.exists('serialization1.py') and path.exists('deserialization1.py'):
    from serialization1 import marshal as m1                                    #type:ignore
    from deserialization1 import unmarshal as um1                               #type:ignore
    unmarshal_implementation_container.append(um1)
    marshal_implementation_container.append(m1)
if path.exists('serialization2.py') and path.exists('deserialization2.py'):
    from serialization2 import marshal as m2                                    #type:ignore
    from deserialization2 import unmarshal as um2                               #type:ignore
    unmarshal_implementation_container.append(um2)
    marshal_implementation_container.append(m2)
if path.exists('serialization3.py') and path.exists('deserialization3.py'):
    from serialization3 import marshal as m3                                    #type:ignore
    from deserialization3 import unmarshal as um3                               #type:ignore
    unmarshal_implementation_container.append(um3)
    marshal_implementation_container.append(m3)
if path.exists('serialization4.py') and path.exists('deserialization4.py'):
    from serialization4 import marshal as m4                                    #type:ignore
    from deserialization4 import unmarshal as um4                               #type:ignore
    unmarshal_implementation_container.append(um4)
    marshal_implementation_container.append(m4)
if path.exists('serialization5.py') and path.exists('deserialization5.py'):
    from serialization5 import marshal as m5                                    #type:ignore
    from deserialization5 import unmarshal as um5                               #type:ignore
    unmarshal_implementation_container.append(um5)
    marshal_implementation_container.append(m5)
if path.exists('serialization6.py') and path.exists('deserialization6.py'):
    from serialization6 import marshal as m6                                    #type:ignore
    from deserialization6 import unmarshal as um6                               #type:ignore
    unmarshal_implementation_container.append(um6)
    marshal_implementation_container.append(m6)

from exceptions import SerializationError, DeserializationError

    
# Global Variables Go Here
NUMBER_OF_STRINGS = 10

MAX_NEST = 2
MAX_INPUT_SIZE = 20
MAX_KEY_SIZE = 10
MAX_VALUE_SIZE = 10
MAX_MAP_SIZE = 3
#Error chance is the chances out of 10 that an error will occur. Used to determine an error in all aspects of the map.
ERROR_CHANCE = 1 #Currently 1/10 chance for an error to occur in any part of the function



def main():
    global nest_cnt
    nest_cnt = 0
    unmarshal_implementation_container = preprocessor.import_files()
    print('Testing on', len(unmarshal_implementation_container), 'files')
    # Create random inputs
    input_strings = generateStrings('random', NUMBER_OF_STRINGS)
    for i in range(len(input_strings)):
        print('Input',i,': ',input_strings[i])

    # Apply list of generated strings to each implementation and log responses
    response_dict = {}
    for j in range(len(unmarshal_implementation_container)):                      # Itterates through every implementation present
        response_dict[j] = {'pass':0}
        for k in range(len(input_strings)):                                     # Tries every generated string on current implementation
            try:
                nest_cnt = 0
                unmarshal_implementation_container[j](input_strings[k])
                response_dict[j]['pass'] = response_dict[j].get('pass') + 1    
            except:
                e = sys.exc_info()[0]
                e = str(e)
                if response_dict[j].get(e) is not None:
                    response_dict[j][e] = response_dict[j].get(e) + 1
                else:
                    response_dict[j][e] = 1
                continue
    

    # ---- Format result dictonarys into a matrix and print ---


    # Debug print results of run
    print('\nResults:')
    for l in response_dict:
        print('Result of Implementation:',l)
        print(response_dict[l])

# Function that builds a list of input strings
def generateStrings(_method, _length):
    ret_strings = []
    if _method == 'random':
        for i in range(_length):
            # Stocastically pick either a proper nosj string(0-0.5) or random string(0.5-1)
            validity = random.uniform(0,1)
            if validity < 0.5:
                ret_strings.append(__make_map(valid=True)[1])
            else:
                ret_strings.append(__make_map(valid=False)[1])
        return ret_strings
    else:
        print('Invalid generation method')
        return ret_strings


#------------CARLO's Imp---------------
#given already created keys and values, creates either an unmarshalled or marshalled map.
def __make_map(valid = True, map_size = random.randint(1, MAX_MAP_SIZE)):
    global nest_cnt
    r = map_size
    if map_size <= 0:
        return ({},{})
    #Length = # of KV pairs
    if map_size <= 0:
        return (0)
    unmarshalled_map = {}
    marshalled_map = "{"
    if valid:
        for i in range(map_size):
            key = __make_key(valid = True)
            choice = random.randint(0,2)
            if (choice == 2 and nest_cnt >= MAX_NEST):
                # If we have reached max map nesting limit generate a string instead
                choice = 1
                print ("Max cnt reached")
            # Make an int
            if choice == 0:
                val = __nosj_int(valid = True)
                unmarshalled_map[key] = val[0]
                marshalled_map = marshalled_map + key + ":" + val[1]
                if i != map_size:
                    marshalled_map = marshalled_map + ","
            # Make a str
            if choice == 1:
                val = __nosj_string(valid = True)
                unmarshalled_map[key] = val[0]
                marshalled_map = marshalled_map + key + ":" + val[1]
                if i != map_size:
                    marshalled_map = marshalled_map + ","     
            # make a map      
            if choice == 2:
                #map nesting
                nest_cnt += 1
                val = __make_map(valid = True)
                unmarshalled_map[key] = val[0]
                marshalled_map = marshalled_map + key + ":" + val[1]
                if i != map_size:
                    marshalled_map = marshalled_map + ","
        if marshalled_map[len(marshalled_map)-1] == ",":
            marshalled_map = marshalled_map.rstrip(",")
        marshalled_map = marshalled_map + "}"
        return (unmarshalled_map, marshalled_map)
    else:
        for i in range(map_size):
            key = __make_key(valid = False)
            choice = random.randint(0,2)
            if (choice == 2 and nest_cnt >= MAX_NEST):
                # If we have reached max map nesting limit generate a string instead
                choice = 1
                print ("Max cnt reached")

                more_invalids = (random.randint(0,1) == 1)
                val = __make_map(valid = more_invalids, map_size = r - 1)
                unmarshalled_map[key] = val[0]
                marshalled_map = marshalled_map + key + ":" + str(val[1])
                if i != map_size:
                    marshalled_map = marshalled_map + ","
        if marshalled_map[len(marshalled_map)-1] == ",":
            marshalled_map = marshalled_map.rstrip(",")
        marshalled_map = marshalled_map + "}"
        return (unmarshalled_map, marshalled_map)
            

#-----MIGHT BE UNECESSARY------
#Returns fully formatted input string
def create_input():
    # is_invalid = False
    ret = "{"
    #First, randomly determines the size of the input
    input_size = random.randint(0, MAX_INPUT_SIZE)
    for i in range(input_size):
        #Determines the next key-value pair to be added
        if(random.uniform(0,1)) <= 0.5: # 0 = String, 1 = int
            ret = ret + __make_key()
            ret = ret + __nosj_string()
        else:
            ret = ret + __nosj_int()
    ret +="}"
    return ret


# ----------- Helper functions -----------

#Helper function to generate random nosj string. If valid and issimple, will return valid simple string...etc
#returns unmarshalled and marshalled state in a tuple respectively
def __nosj_string(valid = True, isSimple = True):
    valid_complex_strings = [string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase, string.printable,string.whitespace\
        ,string.punctuation]
    valid_simple_strings = [" !#$&'()*+-./:;<=>?@[\]^_`|~", string.ascii_letters, string.digits]
    invalid_simple_strings = "%, }{"
    generated_string = ""
    string_size = random.randint(1, MAX_VALUE_SIZE)
    if isSimple:
        if valid:
            for x in range(random.randint(1,3)):
                generated_string = generated_string + valid_simple_strings[random.randint(0, 2)]
            ret = "".join([random.choice(generated_string) for n in range(string_size)])
            return (ret, ret + "s")
        else:
            #Creates a completely invalid simple string
            ret = "".join([random.choice(invalid_simple_strings) for n in range(string_size)])
            #Sprinkles some printables
            ret = "".join('%s%s' % (x, random.choice(string.printable) if random.randint(1,10) > ERROR_CHANCE else '') for x in ret)
            return (ret,ret + "s")
    else: #Complex strings
        if valid:
            for x in range(random.randint(1,5)):
                generated_string = generated_string + valid_complex_strings[random.randint(0,5)]
                ret = "".join([random.choice(generated_string) for n in range(string_size)])
            #garunteed at least one percent encoded value
            random_insert = random.randint(0,len(ret)-1)
            ret = ret[:random_insert] + random.choice(string.whitespace) + ret[random_insert:]
            return (ret, str(urllib.parse.quote(ret)))
        #Does the same thing as the previous if statement, however an invalid marshalled complex string will not be percent encoded,
        # an invalid unmarshalled complex string will not be a string        
        else:
            for x in range(random.randint(1,5)):
                generated_string = generated_string + valid_complex_strings[random.randint(0,5)]
                ret = "".join([random.choice(generated_string) for n in range(string_size)])
                #garunteed at least one percent encoded value
                random_insert = random.randint(0,len(ret)-1)
                ret = ret[random_insert:] + random.choice(string.whitespace) + ret[:random_insert]
            return (ret,ret)

#Helper function to generate random nosj int.
#returns unmarshalled and marshalled state in a tuple respectively
def __nosj_int(valid = True):
    int_size = random.randint(1,MAX_VALUE_SIZE)
    if valid:
            ret = int("".join([random.choice(string.digits) for n in range(int_size)]))
            return(ret, str(ret) + "i")
    else:
            ret = int("".join([random.choice(string.digits) for n in range(int_size)]))
            return(str(ret) + "i", str(ret))

#Helper function to nest next part of nosj map
def __nest():
    return None


def generate_really_bad_input():
    # TODO: Delete this function.
    return 'b' * random.randint(1, 10)

def __make_key(valid = True):
    #Randomly create a combination of different valid/invalid string types. If valid parameter is true, will return a valid key. Will not otherwise.\
    #randomly chooses which combination of characters from their respective lists\
    #to create a random string from
    key_size = random.randint(1, MAX_KEY_SIZE)
    valid_characters = [string.ascii_letters, string.ascii_uppercase, string.ascii_lowercase, string.digits, " -_+."]
    invalid_characters = [string.punctuation, string.whitespace]

    #Chooses the number of appendages in either array to create a random string from
    combination = random.randint(1,5)
    generated_string = ""
    ret = ""
    #Creation of invalid string
    if not valid:
        #First generates an absolutely invalid string
        for x in range(combination):
            generated_string = generated_string + (invalid_characters[random.randint(0,len(invalid_characters) - 1)])
        ret = "".join([random.choice(generated_string) for n in range(key_size)])
        #Sprinkles printables in invalid key
        ret = "".join('%s%s' % (x, random.choice(string.printable) if random.randint(1,10) > ERROR_CHANCE else '') for x in ret)
        return ret
    
    else:
        for x in range(combination):
            generated_string = generated_string + (valid_characters[random.randint(0,len(valid_characters) - 1)])
        return "".join([random.choice(generated_string) for n in range(key_size)])



if __name__ == '__main__':
    main()
