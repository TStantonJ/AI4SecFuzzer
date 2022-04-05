#import imp
import os
import importlib

def import_files():
    functions = []
    folder = 'implementations.'

    for dirname, dirs, files in os.walk(folder):
        for filename in files:
            filename_without_extension, extension = os.path.splitext(filename)
            
            if extension == '.py':
                if filename_without_extension == '__init__':
                    pass
                else:
                    #holder = importlib.import_module(os.path.join(dirname, filename))
                    holder = importlib.import_module('implementations.AA/deserialization')
                    functions.append(holder)
    print(functions)
    return functions

if __name__ == '__main__':
    import_files()  