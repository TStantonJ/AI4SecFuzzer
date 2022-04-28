
# Fuzzer Set Class Definition
    Fuzzer String: String of generated characters to test on implentations
    Fuzzer Set: Set of fuzzer strings. Fuzzer sets are what we evaluate fitness of. Contains
        - string_set: A list of all fuzzer strings in the set
        - preferred_strings: A list of preferable strings we will use to determine combination
        - fitness: overall fitness of the given set
        - set_number: enumeration for population 

    Population: Set of fuzzer sets. This is what we perform evolution on. Contains:
        - fuzzer_sets: A list of all fuzzer strings in the set
        - number_of_children: number of children in population
        - population_size: The size of the Population
        - best_fitness: A list with the highest fitness and the string set for it respectively


    
    

