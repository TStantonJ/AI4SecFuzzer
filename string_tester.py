# Iteratively tests string on implementations to see what parts of NOSJ string breaks the implementations
import os
import importlib
import sys
import fuzzer as fuzz


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


def get_implementations():
    # Puts all the implementations into a list of functions
    unmarshal_implementation_container = []
    files = os.listdir("./runFiles")
    for file in files:
        tmp = 'runFiles.' + file.replace('.py', '')
        if file.startswith("deserialization"):
            try:
                module = importlib.import_module(str(tmp))
                unmarshal_implementation_container.append(module.unmarshal)
            except Exception as e:
                print(e)
    return unmarshal_implementation_container


def test_string(string, unmarshal_implementation_container):
    # Tests the string without any changes. If it doesn't throw a proper exception(anything other than passing or deserialization error),
    # will return
    exceptions = []
    exceptions_counter = []
    for i in range(len(unmarshal_implementation_container)):
        try:
            blockPrint()
            unmarshal_implementation_container[i](string)
            enablePrint()
        except:
            enablePrint()
            # Exception thrown
            e = str(sys.exc_info()[0])
            if e == '<class \'exceptions.DeserializationError\'>':
                continue
            # Increments the number of exceptions, only if the exception is already accounted for. Will add the exception otherwise.
            if e in exceptions:
                index = exceptions.index(e)
                exceptions_counter[index] += 1
                continue
            else:
                exceptions.append(e)
                exceptions_counter.append(1)
                continue
    return exceptions

#Gets a string and iterates through it.
def iterate_string(string, container):
    #Original number of exceptions
    original_exception_number = len(test_string(string, container))
    iterative_string = ""
    current_addition = ""
    string_before_addition = ""
    exception_counter = 0
    additions = []
    at_string = []
    isOriginal = True
    print("Testing on string: {}".format(string))
    print("This string will throw {} exceptions".format(original_exception_number))
    #Will add characters to the string until a new exception is thrown
    for character in string:
        iterative_string += character
        current_addition += character
        current_exceptions = test_string(iterative_string, container)
        new_exception_counter = len(current_exceptions)
        if new_exception_counter != 0 and isOriginal:
            tempctr = 0
            print("Original exceptions when string is {}".format(iterative_string))
            for exception in current_exceptions:
                print("{},{}\n".format(exception,tempctr))
                tempctr+=1
            isOriginal = False
                
        if new_exception_counter > exception_counter:
            print("Exception: {} is thrown: \nString added: {}\nCurrent String: {}".format(current_exceptions[new_exception_counter -1], current_addition, string_before_addition))
            print("Number of exceptions: {}\n".format(new_exception_counter))
            exception_counter = new_exception_counter
            additions.append(current_addition)
            at_string.append(iterative_string)
            string_before_addition += current_addition
            current_addition = ""
    





    


if __name__ == "__main__":
    container = get_implementations()
    string = "{0877152551497992634253787535376358572077544672202352148640754109066605034:{xanLSMOnVlDFqldjlsbNUrwqAYwmZgswjfTbOiXeYQEWlEbiGJOWBfJbc:{oUYjqZYrYmIgghABRMQVoWaBymXRQMIVrNGSPGGYPBICFZAjdVESDepSZH_gAREZEBXHEfNOBuZtbWRnGJLdHvAhKdGJ:OboAjUymZoovwTalkjgnCQbwOiPTTHnBJGfeojTCovvRoajlVTIjvPtqXs}}}"
    iterate_string(string,container)



