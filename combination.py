#TODO implement a more robust version of combinations
#Implements the fuzzer set class
import random
import numpy
import fuzzer as fz
from neighbor import mutate
import fuzzer_set_class as fs
from config import config


MUTATION_RATE = int(config["MUTATION_RATE"])
MAXIMUM_STRINGS_PER_SET = int(config["MAXIMUM_STRINGS_PER_SET"])

#POC for combination. Will randomly mutate from neighbor
#Implements fuzzer set class
def combine(parent1, parent2):
    #For choosing length of child
    average_parent_length = int((len(parent1.string_set) + len(parent2.string_set)) / 2)
    child = []
    parent_genes = parent1.string_set + parent2.string_set
    #Chooses a length for the child. Length can vary but is based off parent.
    #TODO REDIFINE CHILD_LENGTH
    child_length = int(numpy.random.normal(average_parent_length, 3))
    #Limits the length of child
    if child_length > MAXIMUM_STRINGS_PER_SET:
        child_length = MAXIMUM_STRINGS_PER_SET
    mutation_count = 0
    #Randomly chooses from both sets of strings of both parents
    for i in range(child_length):
        if len(parent_genes) <= 0:
            break
        gene = random.choice(parent_genes)
        while gene in parent_genes:
            parent_genes.remove(gene)
        #Chance to do mutations with combination
        if MUTATION_RATE > random.choice(range(0,100)):
            gene = mutate(gene)
            mutation_count += 1
        child.append(gene)

    return fs.fuzzer_set(string_set = child, number_of_mutations = mutation_count)

if __name__ == "__main__":
    mom = fs.fuzzer_set(string_set = fz.generateStrings("random", 3))
    dad = fs.fuzzer_set(string_set = fz.generateStrings("random", 3))
    child = combine(mom,dad)
    print(f"Mom : {mom}")
    print(f"Dad: {dad}")
    print(f"Child : {child}")