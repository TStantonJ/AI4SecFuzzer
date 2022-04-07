from re import L
from fuzzer import main as fuzz
import matplotlib.pyplot as plt


NUMBER_OF_EVALS  = 300
NUMBER_OF_RUNS = 1

run_holder = []
best_fitness = 0
# Collect 30 runs of data
for run in range(NUMBER_OF_RUNS):
    eval_holder = []
    best_eval = 0

    # Collect 30 evals of data per run
    for eval in range(NUMBER_OF_EVALS):
        result = fuzz()
        if result >= best_eval:
            best_eval = result
        eval_holder.append(best_eval)

    # Add last run to the others
    run_holder.append(eval_holder)
    if best_eval >= best_fitness:
        best_fitness = best_eval
    
    #Plot resutls of run
    xpoints = range(NUMBER_OF_EVALS)
    ypoints = eval_holder
    
    plt.plot(xpoints, ypoints)
    plt.show()

print('Best Fitness:', best_fitness)
print(run_holder)
