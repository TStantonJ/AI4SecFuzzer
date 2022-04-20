# Iteratively tests string on implementations to see what parts of NOSJ string breaks the implementations
import os
import importlib
import sys
import fuzzer as fuzz

#
def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

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
    exceptions = {}
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
                exceptions[e] += 1
                continue
            else:
                exceptions[e] = 1
                continue
    return exceptions

#Gets a string and iterates through it.
# def iterate_string(string, container):
#     #Original number of exceptions
#     original_exception_number = len(test_string(string, container))
#     iterative_string = ""
#     current_addition = ""
#     string_before_addition = ""
#     exception_counter = 0
#     additions = []
#     at_string = []
#     isOriginal = True
#     print("Testing on string: {}".format(string))
#     print("This string will throw {} exceptions".format(original_exception_number))
#     #Will add characters to the string until a new exception is thrown
#     for character in string:
#         iterative_string += character
#         current_addition += character
#         current_exceptions = test_string(iterative_string, container)
#         new_exception_counter = len(current_exceptions)
#         if new_exception_counter != 0 and isOriginal:
#             tempctr = 0
#             print("Original exceptions when string is {}".format(iterative_string))
#             for exception in current_exceptions:
#                 print("{},{}\n".format(exception,tempctr))
#                 tempctr+=1
#             isOriginal = False
                
#         if new_exception_counter > exception_counter:
#             print("Exception: {} is thrown: \nString added: {}\nCurrent String: {}".format(current_exceptions[new_exception_counter -1], current_addition, string_before_addition))
#             print("Number of exceptions: {}\n".format(new_exception_counter))
#             exception_counter = new_exception_counter
#             additions.append(current_addition)
#             at_string.append(iterative_string)
#             string_before_addition += current_addition
#             current_addition = ""
    


#Takes a list of strings, iterates through them 1 char at a time, and puts all the exception catching strings inside a dictionary
def iterate_string(strings, container):
    exception_dict = {}
    for string in strings:
        iterative_string = ""
        current_string = ""
        first_char_not_tested = True
        for char in string:
            last_exception_list = test_string(iterative_string, container)
            iterative_string += char
            current_string += char
            exception_list = test_string(iterative_string, container)
            for exception in (Diff(last_exception_list, exception_list)):
                if exception in exception_dict:
                    exception_dict[exception].append(current_string)
                else:
                    exception_dict[exception] = [current_string]
            if len(Diff(last_exception_list,exception_list)) != 0:
                current_string = ""
    return exception_dict

    


if __name__ == "__main__":
    container = get_implementations()

    string_list = fuzz.generateStrings("random", 2)
    print("Testing on strings: ")
    print(string_list)
    # string = ["{0877152551497992634253787535376358572077544672202352148640754109066605034:{xanLSMOnVlDFqldjlsbNUrwqAYwmZgswjfTbOiXeYQEWlEbiGJOWBfJbc:{oUYjqZYrYmIgghABRMQVoWaBymXRQMIVrNGSPGGYPBICFZAjdVESDepSZH_gAREZEBXHEfNOBuZtbWRnGJLdHvAhKdGJ:OboAjUymZoovwTalkjgnCQbwOiPTTHnBJGfeojTCovvRoajlVTIjvPtqXs}}}"]
    x = iterate_string(string_list, container)
    for exception in x.keys():
        print("Exception: {}".format(exception))
        for string in x[exception]:
            print("String : {}".format(string))

