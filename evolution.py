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
# PERCENTAGE_SELECTED = int(config["PERENTAGE_SELECTED"])
# MATING_PERCENT = int(INITIAL_POPULATION - (PERCENTAGE_SELECTED)(INITIAL_POPULATION)) #FOR POC--- probably needs to change


#Takes in a set of fuzzer sets and the evaluation function, and sets population's evaluations.
# Use this to get the fitness of every current population
#Currently implements fuzz.getStrings() which takes a run num counter and input string.
def evaluate_fitness(population, evaluation_function):
    counter = 0
    for fuzzer_set in population.fuzzer_sets:
        evaluation = evaluation_function(_runNum = counter,_custom_input = fuzzer_set.string_set)
        counter += 1
        fuzzer_set.fitness = evaluation



#TODO: Implement a better selection
#Right now randomly selects people to win
def perform_selection(population):
    fuzzer_sets = population.fuzzer_sets
    return selection.uniform_random_selection(fuzzer_sets, SELECTION_SIZE)


#Finds and sets the best fitness to the population
#Call after evaluating the fitness
def set_best_fitness(population):
    best_fitness = -1
    best_fitness_string = ""
    for fuzz_set in population.fuzzer_sets:
        if fuzz_set.fitness > best_fitness:
            best_fitness = fuzz_set.fitness
            best_fitness_string = fuzz_set.string_set
        else:
            pass
    population.best_fitness = best_fitness
    population.best_fitness_fuzz_set = best_fitness_string



#Creates initial population
def create_initial_population(initial_population_length = INITIAL_POPULATION):
    initial_population = []
    #Uses the fuzzer class to generate random strings for population
    for i in range(INITIAL_POPULATION):
        initial_population.append(fs.fuzzer_set(string_set = fuzz.generateStrings("random", STRINGS_PER_SET), set_number = i))
    
    return fs.population(fuzzer_sets = initial_population)

#
def combine_and_add_children(population, selection):
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
        child.set_number = number_of_children + population.population_size
        #Puts child into population
        population.fuzzer_sets.append(child)
        #FOR DEBUGGING - puts children in list for return
        children.append(child)
    #Increments the number of children in population
    population.number_of_children += number_of_children
    population.population_size += number_of_children
    return children
    



if __name__ == "__main__":
    #Creates initial population
    current_population = create_initial_population()
    print(f"Current Population size: {current_population.population_size}")

    #Gets fitness of initial population
    evaluate_fitness(current_population, fuzz.testStrings)
    set_best_fitness(current_population)
    print(f"Best current fitness: {current_population.best_fitness}\nBest current fuzz_set: {current_population.best_fitness_fuzz_set}")

    #Selects the population for reproduction
    selection = perform_selection(current_population)

    #Creates children and updates population accordingly with selection
    children = combine_and_add_children(current_population, selection)
    for child in children:
        print("\n")
        time.sleep(0.5)
        print(f"Adding child with index : {child.set_number},\n{child.string_set}")
        if(child.number_of_mutations != 0):
            print(f"------This child has {child.number_of_mutations} mutations!------")

    