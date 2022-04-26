#Mutates a set of strings.
import re
import random
import string
import fuzzer as fuzz
import numpy 
import urllib.parse
import copy
import fuzzer_set_class as fs
DEFAULT_NEIGHBORS_GENERATED = 2
DEFAULT_MUTATION_LENGTH = 10
PERCENTS = re.findall("%..", urllib.parse.quote(string.punctuation))
VALID_CHARS = [string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase, string.printable,string.punctuation,string.digits]
CHARACTER_LIST = ["%, }{"] + [" !#$&'()*+-./:;<=>?@[\]^_`|~", string.ascii_letters, string.digits] + [string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase, string.printable,string.punctuation]
SPECIAL_CHARACTERS = [string.punctuation,"%, }{"," !#$&'()*+-./:;<=>?@[\]^_`|~"]  + [PERCENTS]
def get_nosj(string):
    pattern = r"\{[^}]*:[^}]*\}"
    return re.findall(pattern,string)
#Helper function to insert a string into a certian index
def insert(string,index,ins):
    return string[:index] + ins + string[index:]
            
def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))   


#Gaussian distribution to define how many steps (mutations) to generate on a given string
##IMPORT THIS FUNCTION
def mutate_set(set_of_strings, steps = 1):
    mutations = abs(int(numpy.random.normal(0,16.6)))
    temp = copy.deepcopy(set_of_strings)
    new_list = []
    for _ in range(DEFAULT_NEIGHBORS_GENERATED):
        new_list.append(get_neighbors(temp))
    
    for _ in range(mutations):
        random_list_index = random.choice(range(len(new_list)-1))
        random_string_in_list_index = random.choice(range(len(new_list[random_list_index])))
        new_list[random_list_index][random_string_in_list_index] = mutate(new_list[random_list_index][random_string_in_list_index])
    return fs.fuzzer_set(string_set = new_list)
    


def get_neighbors(list_of_strings):
    #Gets a string to perform neighbor function
    neighbor = copy.deepcopy(list_of_strings)
    neighbor_string = random.choice(list_of_strings)
    string_index = list_of_strings.index(neighbor_string)
    addition = "{"
    if len(get_nosj(neighbor_string)) == 0:
        number_of_chars = int(abs(numpy.random.normal(6,10)))
        for x in range(number_of_chars):
            addition += random.choice(random.choice(VALID_CHARS))
        addition += "}"
        addition = insert(addition, random.choice(range(len(addition)-1)), ":")
        neighbor[string_index] = addition
    else:
        number_of_chars = int(abs(numpy.random.normal(6,10)))
        key_or_value_to_mutate = random.choice(random.choice(get_nosj(neighbor_string)).split(":"))
        key_or_value_to_mutate = key_or_value_to_mutate.replace("{","")
        key_or_value_to_mutate = key_or_value_to_mutate.replace("}","")
        for x in range(number_of_chars):
            addition += random.choice(random.choice(VALID_CHARS))
        addition += "}"
        addition = insert(addition, random.choice(range(len(addition)-1)), ":")
        neighbor_string = neighbor_string.replace(key_or_value_to_mutate, addition)
        neighbor[string_index] = neighbor_string
        

    return neighbor
    

def mutate(string):
    mutation = ""
    mutated_string = ""
    #Case where there is no valid kv pairs in the string. Generates new valid kv pair, puts it in the string, and mutates it.
    if len(get_nosj(string)) == 0:
        #Added mutation will be proportional to the string length
        mutation_length = random.choice(range(1,len(string)))
        mutation +="{"
        #Adds random valid characters inside mutation
        for character in range(mutation_length):
            mutation += random.choice(random.choice(VALID_CHARS))
        mutation +="}"
        bracket_index = random.choice(range(1,len(mutation)-1))
        mutation = insert(mutation, bracket_index, ":")
        try:
            mutation_index = random.choice(range(1,len(string)-1))
        except:
            mutation_index = 0
        mutated_string = insert(string,mutation_index,mutation)
        try:
            mutated_string = mutate(mutated_string)
        except:
            mutated_string = mutate(insert(string,0,"{ab:cd}"))
    #If the string has at least 1 kv pair, will choose one to mutate.
    else:
        pair_to_mutate = random.choice(get_nosj(string))
        #Randomly choose one of 3 mutations to perform
        # mutation_choice = random.choice(range(1,3))
        mutation_choice = random.choice(range(1,3))

        #Changing the ordering of {, }, or :
        if mutation_choice == 1:
            #Chooses which of the 3 to replace
            chosen_character = random.choice(["{","}",":"])
            mutation = pair_to_mutate.replace(chosen_character, "")
            mutation_index = random.choice(range(1,len(string)-1))
            mutation = insert(mutation, mutation_index, chosen_character)
            mutated_string = string.replace(pair_to_mutate,mutation,1)

        #Adding special characters to either key or value
        if mutation_choice == 2:
            #Chooses to either the key or value to add special characters. 
            number_of_specials = int(abs(numpy.random.normal(5,5)))
            pair_to_mutate = random.choice(get_nosj(string))
            #Randomly chooses key or value to mutate
            key_or_value_to_mutate = random.choice(string.split(":"))
            key_or_value_to_mutate = key_or_value_to_mutate.replace("{", "")
            key_or_value_to_mutate = key_or_value_to_mutate.replace("}", "")
            mutated_string = string
            special_character = ""

            for _ in range(number_of_specials):
                special_character += random.choice(random.choice(SPECIAL_CHARACTERS))  

            if len(key_or_value_to_mutate) != 0:
                index = random.choice(range(len(key_or_value_to_mutate)))
            else:
                index = 0
            mutation = insert(key_or_value_to_mutate, index, special_character)
            mutated_string = string.replace(key_or_value_to_mutate, mutation,1)

        #Omits either {,} or :
        if mutation_choice == 3:
            chosen_character = random.choice(["{","}",":"])
            mutation = pair_to_mutate.replace(chosen_character, "")
            mutated_string = string.replace(pair_to_mutate,mutation,1)
    return mutated_string
    
    
        
        


        


def mutString(inp, ch):

    if (ch == 0):
        return mutateString(inp)
    if (ch == 1):
        nosj = get_nosj(inp)
        # Randomly choose a pair from nosj list
        pair = nosj[random.randint(0,len(nosj)-1)]
        keypair = pair.split(':', 1)
        key = keypair[0]
        value = keypair[1]
        #50% random choice of key or value
        r = random.choice([0,1])
        if (r == 0):
            newkey = mutateString(key)
            #Replace key with newkey

            #This is not fool proof, What if the same apeared twice in the string.
            return inp.replace(key, newkey)
        else :
            newvalue = mutateString(value)
            return (inp.replace(value, newvalue))

    # Remove {
    if (ch == 2):
        nosj = get_nosj(inp)
        # Randomly choose a pair from nosj list
        pair = nosj[random.randint(0,len(nosj)-1)]
        #remove first char which shd be { and replace the pair
        return inp.replace(pair, pair[1:])
    # Remove }
    if (ch == 3):
        nosj = get_nosj(inp)
        # Randomly choose a pair from nosj list
        pair = nosj[random.randint(0,len(nosj)-1)]
        #remove last char which shd be } and replace the pair
        return inp.replace(pair, pair[1:-1])




if __name__ == "__main__":
    # lst = []
    # for i in range(50):
    #     string = "{" + "{}".format(random.choice(random.choice(CHARACTER_LIST))) + ":" + "{}".format(random.choice(random.choice(CHARACTER_LIST))) + "}"
    #     lst.append(string)
    # print(lst)
    # new_list = mutate_set(lst)
    
    # print("___________________")
    # print(new_list)
    x = [":32}","{abc:123}"]
    x = mutate_set(x)
    print(x.string_set)
    print(x.fitness)
