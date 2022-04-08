from re import L
from fuzzer import main as fuzz
import matplotlib.pyplot as plt
import time


NUMBER_OF_EVALS  = 300
NUMBER_OF_RUNS = 30

best_run_holder = []        # Holds list of best_eval_holders
general_run_holder = []     # Holds list of results of each eval per run
best_run_fitness = 0
best_run = []
# Collect 30 runs of data
for run in range(NUMBER_OF_RUNS):
    time.sleep(0.1)
    print('Starting Run Series:',run)
    best_eval_holder = []           # Holds best eval log
    general_eval_holder = []        # Hold results of each eval
    best_eval = 0                   # Hold best eval total

    # Collect 300 evals of data per run
    for eval in range(NUMBER_OF_EVALS):
        # Run fuzzer
        print('\t\t\t\t\tCurrent Eval :',eval, end='\r')
        time.sleep(0.01)
        result = fuzz()
        # Update best eval so far
        if result >= best_eval:
            best_eval = result
        best_eval_holder.append(best_eval)
        # Add eval to data from this run
        general_eval_holder.append(result)
    print('\n')

    # Check if last run is better than current best run
    if best_eval >= best_run_fitness:
        best_fitness = best_eval
        best_run = best_eval_holder
    
    # Add last run to run storage
    best_run_holder.append(best_eval_holder)
    general_run_holder.append(general_eval_holder)

#Plot resutls of all runs
for run in best_run_holder:
    xpoints = range(NUMBER_OF_EVALS)
    ypoints = run
    plt.plot(xpoints, ypoints)

plt.show()

print('Best Fitness:', best_fitness)
print(best_run_holder)
