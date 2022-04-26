import fuzzer as fuzz
import neighbor
import fuzzer_set_class as fs
from config import config

DEFAULT_NEIGHBORS_GENERATED = config["DEFAULT_NEIGHBORS_GENERATED"]
INITIAL_POPULATION = int(config["INITIAL_POPULATION"])
STRINGS_PER_SET = int(config["STRINGS_PER_SET"])


#Takes in a set of strings and the evaluation function, and sets population's evaluations.
def evaluate_fitness(string_sets, evaluation_function):
    for current_set in string_sets:
        evaluation = evaluation_function(current_set.string_set)
        string_set.fitness = evaluation

def turn_to_class(population):
    pass


if __name__ == "__main__":
    #CREATES INITIAL POPULATION
    initial_population = []
    for i in range(INITIAL_POPULATION):
        initial_population.append(fs.fuzzer_set(string_set = fuzz.generateStrings("random", STRINGS_PER_SET), set_number = i))
    evaluate_fitness(initial_population, fuzz.getFitness) 
    print("Starting population with: {} ".format(initial_population))