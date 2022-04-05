#import imp
import os
import importlib

def import_files():
    functions = []
    folder = './implementations'

    for dirname, dirs, files in os.walk(folder):
        for filename in files:
            filename_without_extension, extension = os.path.splitext(filename)
            if extension == '.py':
                holder = importlib.import_module('implementations',os.path.join(dirname, filename))
                functions.append(holder)
    print(functions)
    return functions

if __name__ == '__main__':
    import_files()  