from re import L
from fuzzer import main as fuzz
import matplotlib.pyplot as plt


NUMBER_OF_EVALS  = 300
NUMBER_OF_RUNS = 2

best_run_holder = []
general_run_holder = []
best_fitness = 0
# Collect 30 runs of data
for run in range(NUMBER_OF_RUNS):
    best_eval_holder = []
    general_eval_holder = []
    best_eval = 0

    # Collect 30 evals of data per run
    for eval in range(NUMBER_OF_EVALS):
        # Run fuzzer
        result = fuzz()
        # Update best eval so far
        if result >= best_eval:
            best_eval = result
        best_eval_holder.append(best_eval)
        # Add eval to data from this run
        general_eval_holder.append(result)

    # Check if last run is better than current best run
    if best_eval >= best_fitness:
        best_fitness = best_eval
        best_run_holder.append(best_eval_holder)
    # Add last run to run storage
    general_run_holder.append(general_eval_holder)

#Plot resutls of all runs
for run in general_run_holder:
    xpoints = range(NUMBER_OF_EVALS)
    ypoints = general_run_holder[run]
    plt.plot(xpoints, ypoints)

plt.show()

print('Best Fitness:', best_fitness)
print(best_run_holder)
