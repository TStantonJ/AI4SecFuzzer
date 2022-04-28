import fuzzer as fuzz
import neighbor
import fuzzer_set_class as fs
from config import config
import random
import selection
import combination
import time
DEFAULT_NEIGHBORS_GENERATED = config["DEFAULT_NEIGHBORS_GENERATED"]
INITIAL_POPULATION = int(config["INITIAL_POPULATION"])
STRINGS_PER_SET = int(config["STRINGS_PER_SET"])
SELECTION_SIZE = int(config["SELECTION_SIZE"])
NUMBER_OF_CHILDREN = int(config["NUMBER_OF_CHILDREN"])
POPULATION_SIZE = int(config["POPULATION_SIZE"])
# PERCENTAGE_SELECTED = int(config["PERENTAGE_SELECTED"])
# MATING_PERCENT = int(INITIAL_POPULATION - (PERCENTAGE_SELECTED)(INITIAL_POPULATION)) #FOR POC--- probably needs to change

#Takes in a set of fuzzer sets and the evaluation function, and sets population's evaluations.
# Use this to get the fitness of every current population
#Currently implements fuzz.getStrings() which takes a run num counter and input string.
def evaluate_fitness(population, evaluation_function):
    for fuzzer_set in population.fuzzer_sets:
        evaluation = evaluation_function(_custom_input = fuzzer_set.string_set)
        fuzzer_set.fitness = evaluation



#TODO: Implement a better selection
#Right now randomly selects people to win
def perform_selection(population):
    fuzzer_sets = population.fuzzer_sets
    return selection.uniform_random_selection(fuzzer_sets, SELECTION_SIZE)


#Finds and sets the best fitness to the population. Also calculates average fitness.
#Call after evaluating the fitness
def set_best_fitness(population):
    total_fitness = 0.0
    best_fitness = -1
    best_fitness_string = ""
    for fuzz_set in population.fuzzer_sets:
        total_fitness += fuzz_set.fitness
        #Finds best fitness
        if fuzz_set.fitness > best_fitness:
            best_fitness = fuzz_set.fitness
            best_fitness_string = fuzz_set.string_set
        else:
            pass
    population.best_fitness = best_fitness
    population.best_fitness_fuzz_set = best_fitness_string
    population.average_fitness = total_fitness / population.population_size



#Creates initial population
def create_initial_population(initial_population_length = INITIAL_POPULATION):
    initial_population = []
    #Uses the fuzzer class to generate random strings for population
    for i in range(INITIAL_POPULATION):
        initial_population.append(fs.fuzzer_set(string_set = fuzz.generateStrings("random", STRINGS_PER_SET), set_number = i))
    
    return fs.population(fuzzer_sets = initial_population, highest_set_number = INITIAL_POPULATION)

#Takes in the selection created by selection function and adds them to population
def combine_and_add_children(population, selection):
    starting_set_number = population.highest_set_number
    number_of_children = 0
    #LIST FOR DEBUGGING
    children = []
    for i in range(NUMBER_OF_CHILDREN):
        number_of_children += 1
        #Selects parents
        parent1 = random.choice(selection)
        parent2 = random.choice(selection)
        #creates child
        child =  combination.combine(parent1,parent2)
        child.set_number = number_of_children + starting_set_number
        #Puts child into population
        population.fuzzer_sets.append(child)
        #FOR DEBUGGING - puts children in list for return
        children.append(child)
    
    #Increments the number of children in population
    population.number_of_children += number_of_children
    population.population_size += number_of_children
    population.highest_set_number = starting_set_number + number_of_children
    return children

#TODO implement a better way of keeping the population a certain number. For now removes the worst fitness sets until it reaches 50.
def cull_population(population):
    #Sorts fuzz sets by fitness.
    fuzz_sets = population.fuzzer_sets
    sorted_population = sorted(fuzz_sets, key = fs.fuzzer_set.__eq__)
    #Sets amount of sets to cull according to population size
    amount_to_cull = population.population_size - POPULATION_SIZE

    if amount_to_cull == 0:
        print("No need to cull")
        return
    elif amount_to_cull < 0:
        print(f"ERROR, population less than {POPULATION_SIZE}")
        exit

    population.fuzzer_sets = sorted_population[amount_to_cull - 1: -1]
    population.population_size = len(population.fuzzer_sets)
    population.number_of_children = 0
    return amount_to_cull




if __name__ == "__main__":

    print("**Creating initial population**")
    #Creates initial population
    current_population = create_initial_population()
    print(f"Current Population size: {current_population.population_size}")
    #Gets fitness of initial population
    evaluate_fitness(current_population, fuzz.testStrings)
    set_best_fitness(current_population)
    print(f"Best fitness of initial population: {current_population.best_fitness}")
    print(f"Average fitness of initial population: {current_population.average_fitness}")



    #LOOP UNTIL CONVERGANCE. TODO: REPLACE WHILE FUNCTION WITH A CONVERGENCE FUNCTION

    generation = 0
    while generation < 4:
        generation += 1
        print(f"-------------Generation {generation}----------------")
        #Selects the population for reproduction
        print("**Starting selection process of population**")
        parents = perform_selection(current_population)

        #Creates children and updates population accordingly with selection
        print("**Starting children generation process**")
        children = combine_and_add_children(current_population, parents)
        children_mutations = 0
        temp = "Created children with set numbers : "
        for child in children:
            children_mutations += child.number_of_mutations
            temp += f",{child.set_number} "
        print(temp)
        print("A total of {} mutations occured during the process".format(children_mutations))

        print("**Evaluating fitness of population**")
        #Gets fitness of new population
        evaluate_fitness(current_population, fuzz.testStrings)
        set_best_fitness(current_population)
        print(f"Best current fitness of generation {generation}: {current_population.best_fitness}")
        print(f"Average fitness of generation {generation} : {current_population.average_fitness}")
        ("**Culling population back to size**")
        #Culling population back to initial size
        print(f"Deleted {cull_population(current_population)} from population.")

    

    