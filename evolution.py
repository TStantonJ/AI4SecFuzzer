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
CONVERGENCE_PERCENT = float(config["CONVERGENCE_PERCENT"])
# PERCENTAGE_SELECTED = int(config["PERENTAGE_SELECTED"])
# MATING_PERCENT = int(INITIAL_POPULATION - (PERCENTAGE_SELECTED)(INITIAL_POPULATION)) #FOR POC--- probably needs to change

#Takes in a set of fuzzer sets and the evaluation function, and sets population's evaluations.
# Use this to get the fitness of every current population
#Currently implements fuzz.getStrings() which takes a run num counter and input string.
def evaluate_fitness(population, evaluation_function):
    for fuzzer_set in population.fuzzer_sets:
        evaluation = evaluation_function(_custom_input = fuzzer_set.string_set)
        #print(len(fuzzer_set.string_set))
        fuzzer_set.fitness = evaluation



#Finds individuals from a given population. 
#Call with a population and which type of selection being perfomred( survival or parent )
def perform_selection(population, selection_type):
    fuzzer_sets = population.fuzzer_sets
    if selection_type == 'survival':
        return selection.k_tournament_without_replacement(fuzzer_sets, n = INITIAL_POPULATION)
    elif selection_type == 'parent':
        return selection.k_tournament_with_replacement(fuzzer_sets, SELECTION_SIZE)


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
    for i in range(initial_population_length):
        initial_population.append(fs.fuzzer_set(string_set = fuzz.generateStrings("random", STRINGS_PER_SET), set_number = i))
    
    return fs.population(fuzzer_sets = initial_population, highest_set_number = initial_population_length)

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


#Convergence tester
#From the last 3 generation's (TODO) if the best fitness is consistently closer to the average fitness
def test_convergence(population):

    conv_per = CONVERGENCE_PERCENT
    #conv_per = 3

    #TODO will have to do the 'consistent' part later but just average comparison now
    #That has some complexity
    #if len(population.fuzzer_set) <= 3:
        #return false

    distance = population.best_fitness - population.average_fitness

    #print("CONV "+ str(distance) + " % " + str(population.average_fitness*conv_per/100) + "REf Perc" + str(conv_per))

    #if the distnace is x% from the average
    if distance <= population.average_fitness*conv_per/100:
        return True
    else:
        return False




# #TODO implement a better way of keeping the population a certain number. For now removes the worst fitness sets until it reaches 50.
# def cull_population(population):
#     #Sorts fuzz sets by fitness.
#     fuzz_sets = population.fuzzer_sets
#     sorted_population = sorted(fuzz_sets, key = fs.fuzzer_set.findFitness)
#     #Sets amount of sets to cull according to population size
#     amount_to_cull = population.population_size - POPULATION_SIZE

#     if amount_to_cull == 0:
#         print("No need to cull")
#         return
#     elif amount_to_cull < 0:
#         print(f"ERROR, population less than {POPULATION_SIZE}")
#         exit

#     population.fuzzer_sets = sorted_population[amount_to_cull - 1: len(sorted_population)]
#     population.population_size = len(population.fuzzer_sets)
#     population.number_of_children = 0
#     return amount_to_cull

def evolutionDriver(_evalNum = 0, _runNum = 0):
    # Data logging variables
    best_fitness_at_gen = []


    # Create inital population
    print("**Creating initial population**")
    current_population = create_initial_population()
    
    #Gets fitness of initial population and display info about it
    evaluate_fitness(current_population, fuzz.testStrings)
    set_best_fitness(current_population)
    print(f"Best fitness of initial population: {current_population.best_fitness}")
    print(f"Average fitness of initial population: {current_population.average_fitness}")
    print(f"Current Population size: {current_population.population_size}")
    # Log data
    best_fitness_at_gen.append(current_population.best_fitness)


    #LOOP UNTIL CONVERGANCE or 100 generations to convserve time
    generation = 0
    while generation < 100:
        generation += 1
        print(f"-------------Generation {generation}----------------")


        # Perform parent Selction
        print("**Starting selection process of population**")
        parents = perform_selection(current_population, selection_type = 'parent')
        # Perform crossover/recombination
        print("**Starting children generation process**")
        children = combine_and_add_children(current_population, parents)

        # Perfrom mutation on children
        children_mutations = 0
        temp = "Created children with set numbers : "
        for child in children:
            children_mutations += child.number_of_mutations
            temp += f",{child.set_number} "
        print(temp)
        print("A total of {} mutations occured during the process".format(children_mutations))

        # Perform Fitness evalution
        evaluate_fitness(current_population, fuzz.testStrings)
        set_best_fitness(current_population)


        # Perform Survival Selection
        print("**Culling population back to size**")
        #Log size of pop before cull, then cull, then log size after
        precullNumber = len(current_population.fuzzer_sets)
        current_population.fuzzer_sets = perform_selection(current_population, selection_type = 'survival')
        postcullNumber = len(current_population.fuzzer_sets)
        # Update population_size with actually size
        current_population.population_size = precullNumber - (precullNumber-postcullNumber)
        print('Culled # of individuals:', precullNumber-postcullNumber)
        print('Population Size:', current_population.population_size)


        # Re-evalute final population fitness
        print("**Evaluating fitness of population**") 
        evaluate_fitness(current_population, fuzz.testStrings)
        set_best_fitness(current_population)
        print(f"Best current fitness of generation {generation}: {current_population.best_fitness}")
        print(f"Average fitness of generation {generation} : {current_population.average_fitness}")
        # Log data
        best_fitness_at_gen.append(current_population.best_fitness)

        # Test for convergence
        if test_convergence(current_population) == True :
            print ("Converged!!!!")
            break

    # Print strings of population at end to file called EvolutionOut.txt
    outputFile = 'EvolutionOut.txt'
    data_out = open(outputFile, 'w')
    printItem = current_population.fuzzer_sets

    best_set = []
    best_set_fitness = []
    for setNum in range(len(printItem)):
        if setNum == 0:
            best_set_fitness = printItem[setNum].fitness
            best_set = printItem[setNum].string_set
        else:
            if printItem[setNum].fitness > best_set_fitness:
                best_set_fitness = printItem[setNum].fitness
                best_set = printItem[setNum].string_set
        data_out.write('Fitness:')
        data_out.write(str(printItem[setNum].fitness))
        data_out.write('||len')
        data_out.write(str(len(printItem[setNum].string_set)))
        data_out.write(str(printItem[setNum].string_set))
        data_out.write('\n')

    # Log strings and matrix in runLog/0_0
    fuzz.testStrings(_evalNum = _evalNum, _runNum = _runNum, _custom_input = best_set)
    #print('Best Strings:', best_set)
    print('Best Fitness:', best_set_fitness)

    return (best_set_fitness, best_fitness_at_gen,generation)




if __name__ == "__main__":
    evolutionDriver()
    
    

    
