#Mutates a set of strings.
import re
import random
import string
import fuzzer
DEFAULT_MUTATION_LENGTH = 10
CHARACTER_LIST = ["%, }{"] + [" !#$&'()*+-./:;<=>?@[\]^_`|~", string.ascii_letters, string.digits] + [string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase, string.printable,string.punctuation]
SPECIAL_CHARACTERS = [string.punctuation,"%, }{"," !#$&'()*+-./:;<=>?@[\]^_`|~"]
def get_nosj(string):
    pattern = r"\{[^}]*:[^}]*\}"
    return re.findall(pattern,string)
            
        


#gets a string given valid nosj inside the string,
# Recursion error/Keyerror: Ending parts of nosj strings 
# Unbound/value error: Opening { brackets
# Syntax Error: Captilized characters? / incomplete nosj
def mutate(string):
    generated_mutation = "{"
    nosj_set = get_nosj(string)
    #If no 'valid' nosj in string
    if (len(nosj_set) == 0):
        for i in range(DEFAULT_MUTATION_LENGTH):
            choice = random.choice([0,1])
            if choice == 0:
                generated_mutation += random.choice(random.choice(CHARACTER_LIST))
            else:
                generated_mutation += random.choice(random.choice(SPECIAL_CHARACTERS))
        generated_mutation+="}"
        return string.replace(string[random.choice(range(0,len(string))):-1], generated_mutation)

    mutation_length = int(len(string) / len(nosj_set))
    choice = random.choice([0,1])

    #General Mutation
    if choice == 0:
        for i in range(mutation_length):
            generated_mutation += random.choice(random.choice(CHARACTER_LIST))
        generated_mutation+="}"
        final_string = final_string.replace(random.choice(nosj_set), generated_mutation)
    #Recursion/KeyError
    if choice == 1:
        generated_mutation = ""
        for i in range(mutation_length):
            generated_mutation += random.choice(random.choice(CHARACTER_LIST))
        generated_mutation+="}"
    else:
        pass
    return  string.replace(random.choice(nosj_set), generated_mutation)

#choices
#0 general string random use Tom existing function
#1 replace key or value of a random pair
#3 Remove the opening { from a nosj
#4 Remove the closing } from a nosj
#
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
    test_string = "1234"
    new_string = mutate(test_string)
    print("Old String{}\nNew String{}".format(test_string,new_string))
