#import imp
import os
import importlib.util

def import_files():
    functions = []
    folder = './implementations'

    for dirname, dirs, files in os.walk(folder):
        for filename in files:
            filename_without_extension, extension = os.path.splitext(filename)
            if extension == '.py':
                holder = importlib.util.spec_from_file_location('implementations',os.path.join(dirname, filename))
                functions.append(holder)
    return functions

if __name__ == '__main__':
    import_files()