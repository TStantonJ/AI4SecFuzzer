from dataclasses import dataclass, field, asdict


@dataclass
class fuzzer_set:
    string_set : list =  field(default_factory = list)
    preferred_strings : list = field(default_factory = list)
    fitness : int = field(default = 0)
    set_number : int = field(default = 0)




if __name__ == "__main__":
    #Set of nosj strings
    foo = ["{A:B}", "{B:C}"]

    #Example initialization of set class with the nosj strings
    example_set = fuzzer_set(string_set = foo, preferred_strings = [foo[0]])
    #Example of how to manually set fitness. Can be done with any of the class variables.
    example_set.fitness = 20

    print(example_set)
    print(example_set.string_set)
    print(example_set.preferred_strings)

    #Example of how to make a string set with params as a dict
    params = {"fitness" : 10, "string_set" : foo, "preferred_strings" : [foo[1]]} 
    example_set_2 = fuzzer_set(**params)
    print(example_set_2)
    #You can also print it as justa dict as well. 
    print(asdict(example_set))