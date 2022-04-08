from re import L

from numpy import average
from fuzzer import main as fuzz
import matplotlib.pyplot as plt
import time
import statistics
import numpy as np


NUMBER_OF_EVALS  = 30
NUMBER_OF_RUNS = 5

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
        time.sleep(0.001)
        result = fuzz()
        # Update best eval so far
        if result >= best_eval:
            best_eval = result
        best_eval_holder.append(best_eval)
        # Always add eval to data from this run
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

# Graph of best fitness seen by eval for all runs
for run in best_run_holder:
    bestxpoints = range(NUMBER_OF_EVALS)
    bestypoints = run
    plt.plot(bestxpoints, bestypoints)
# Box plot graph
data_holder = []
for eval_num in range(NUMBER_OF_EVALS):
    average_at_eval = []
    for run in range(len(general_run_holder)):
        average_at_eval.append(general_run_holder[run][eval_num])
    data_holder.append(average_at_eval)
fig, ax = plt.subplots()
ax.boxplot(data_holder)
# Show graphs
plt.show()

print('Best Fitness:', best_fitness)
print(best_run_holder)
