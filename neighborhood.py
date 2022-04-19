# Iteratively tests string on implementations to see what parts of NOSJ string breaks the implementations
import os
import importlib
import re
import sys
import string
import fuzzer as fuzz
import random
import time

def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__

CHARACTER_LIST = ["%, }{"] + [" !#$&'()*+-./:;<=>?@[\]^_`|~", string.ascii_letters, string.digits] + [string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase, string.printable,string.punctuation]
SPECIAL_CHARACTERS = [string.punctuation,"%, }{"," !#$&'()*+-./:;<=>?@[\]^_`|~"]
def get_nosj(string):
    pattern = r"\{[^}]*:[^}]*\}"
    return re.findall(pattern,string)


def get_implementations():
    # Puts all the implementations into a list of functions
    unmarshal_implementation_container = []
    files = os.listdir("./runFiles")
    for file in files:
        tmp = 'runFiles.' + file.replace('.py', '')
        if file.startswith("deserialization"):
            try:
                
                module = importlib.import_module(str(tmp))
                unmarshal_implementation_container.append(module.unmarshal)
            except Exception as e:
                print(e)
    return unmarshal_implementation_container

#gets a string given valid nosj inside the string,
# Recursion error/Keyerror: Ending parts of nosj strings 
# Unbound/value error: Opening { brackets
# Syntax Error: Captilized characters? / incomplete nosj
def mutate(string):
    nosj_set = get_nosj(string)
    final_string = string

    if len(nosj_set) != 0:
        mutation_length = int(len(string) / len(nosj_set))
    else:
        return final_string
    generated_mutation = "{"
    choice = random.choice([0,1])

    #Recursion/Keyerror:
    if choice == 0:
        for i in range(mutation_length):
            generated_mutation += random.choice(random.choice(CHARACTER_LIST))
        generated_mutation+="}"
        final_string = final_string.replace(random.choice(nosj_set), generated_mutation)
    if choice == 1:
        generated_mutation = ""
        for i in range(mutation_length):
            generated_mutation += random.choice(random.choice(CHARACTER_LIST))
        generated_mutation+="}"
        final_string = final_string.replace(random.choice(nosj_set), generated_mutation)
    else:
        pass
    return final_string

def mutateString(_string):
    # print(_string)
    _points_to_spend = 30
    points_spent = 0

    selection_probability = 0.10
    alpha_chance = 0.33
    num_chance = 0.33
    symb_chance = 0.33

    alphabet_cost = 1
    alphabet_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    number_cost = 2
    number_chars = [1,2,3,4,5,6,7,8,9,0]

    symbol_cost = 3
    symbol_chars = "!#$&'()*+-./:;<=>?@[\]^_`|~]"

    while points_spent < _points_to_spend:
        for i in range(len(_string)-1):
            if points_spent > _points_to_spend:
                break
            
            mutate_choice = random.uniform(0,1)
            if mutate_choice <= selection_probability:
                character_category = random.uniform(0,1)

                if character_category < alpha_chance:
                    character_choice = random.randint(0, len(alphabet_chars)-1)
                    character = str(alphabet_chars[character_choice])
                    _string = _string[:i] + alphabet_chars[character_choice] + _string[i+1:]
                    points_spent += alphabet_cost

                elif character_category < alpha_chance+num_chance:
                    character_choice = random.randint(0, len(number_chars)-1)
                    character = str(number_chars[character_choice])
                    _string = _string[:i] + character + _string[i+1:]
                    points_spent += number_cost

                elif character_category < alpha_chance+num_chance+symb_chance:
                    character_choice = random.randint(0, len(symbol_chars)-1)
                    _string = _string[:i] + symbol_chars[character_choice] + _string[i+1:]
                    points_spent += symbol_cost
    return(_string)

# Takes how many neighbors to find, a set of  strings to mutate, whether or not to repeat process on best string(expiramental)
# Returns a set of strings mutated to have a higher fitness and the neighbors of each mutated stirng
def findNeighbors(_neighbors_range, _input_set, _search_depth = 1):
    # Return Var of new mutated set of strings
    ret_set = []
    # Return Var of neighbors of each string search(first value in each list is original)
    neighborhood_set = []
    # Search every string in the input set
    for cur_string in range(len(_input_set)):
        # Get orginal fitness of string to be mutated
        starting_fitness=fuzz.main(_custom_input = _input_set[cur_string])

        # Add first value to neighborhood log
        neighborhood_set.append([(_input_set[cur_string],starting_fitness)])

        best_new_ftiness = 0
        better_string_check = False
        best_string = _input_set[cur_string]
        interest_string = _input_set[cur_string]
        for j in range(_search_depth):
            # If searching for best neighbor or best neighbor, use best neighbor
            if j != 0:
                interest_string = best_string
            
            # Find _search_depth neighbors and look at their fitness's
            for i in range(_neighbors_range):
                # Mutate String
                mutation_string = mutate(interest_string)
                
                # Get fitness of new String
                test_fitness = fuzz.main(_custom_input = mutation_string, _evalNum= 99)
                #print('New String Fitness:', test_fitness)
                
                # Log String
                neighborhood_set[cur_string].append((mutation_string,test_fitness))
                # Log best mutation if applicable
                if test_fitness > starting_fitness and test_fitness > best_new_ftiness:
                    best_string = mutation_string
                    best_new_ftiness = test_fitness
                    better_string_check = True
                    #print('\t\t\t\t\tNew Best at:0 _',i+1)
            time.sleep(0.1)
        
        if best_new_ftiness > test_fitness:
            ret_set.append(best_string)
        else:
            ret_set.append(_input_set[cur_string])
    return ret_set, neighborhood_set, better_string_check
    
if __name__ == "__main__":
    container = get_implementations()
    string = fuzz.generateStrings('random', 2)
    #string = "{FXVETM8R41YM:760217948826516496488752679886854375s,TZRKUO-:372377560253928204833793414000065840007872381612226217109806076007682196052676499486610052523119s,-p+KK UquvF:76378571329322943992106937348829110570371766753767646291057149241672044620761500104483532i}"
    new_strings, neigh, better_check = findNeighbors(10,string,1)
    for stri in range(len(new_strings)):
        print('\n')
        print('Original String:', string[stri], 'Better:', new_strings[stri])
        print('Neighbors', neigh[stri])
        print('\n')
    #test_string(string, container)
