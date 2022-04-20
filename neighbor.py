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





if __name__ == "__main__":
    test_string = "1234"
    new_string = mutate(test_string)
    print("Old String{}\nNew String{}".format(test_string,new_string))