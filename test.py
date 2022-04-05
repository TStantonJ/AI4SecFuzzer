from asyncio import run_coroutine_threadsafe
import importlib
import os



files = os.listdir("./runFiles")
# #print(files)
functions = []
for file in files:
    tmp = 'runFiles.'+ file.replace('.py','')
    if file.startswith("deserialization"):
        print(tmp)
        try:
            module = importlib.import_module(str(tmp))
            functions.append(module.unmarshal)
        except:
            continue
test_string = "{A:a}"
for function in functions:
    print(function(test_string))