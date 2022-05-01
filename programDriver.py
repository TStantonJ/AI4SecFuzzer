from re import L

from numpy import average
import fuzzer as fuzz
import matplotlib.pyplot as plt
import time
import numpy as np
from neighbor import mutate_set
from config import config
import evolution

STRINGS_PER_SET = int(config["STRINGS_PER_SET"])

# Define runs and evals/run
NUMBER_OF_RUNS = 2
NUMBER_OF_ASSESSMENTS  = 40

#TODO: add convergence and update graph labels
def randomSearch():
    # Data storage for information that lasts more than one run
    best_run_holder = []        # Holds list of best_eval_holders
    general_run_holder = []     # Holds list of results of each eval per run
    best_run_fitness = 0.00
    best_run = []
    best_run_info = ''

    # Collect 30 runs of data
    for run in range(NUMBER_OF_RUNS):
        time.sleep(0.01)
        print('Starting Run Series:',run)
        
        # Data storage for information that lasts only one run
        best_eval_holder = []           # Holds best eval log
        general_eval_holder = []        # Hold results of each eval
        best_eval = 0.00                # Hold best eval total
        set_holder = []
        best_eval_info = ''             # Hold run and eval num of best

        # Collect NUMBER_OF_EVALS evals of data per run
        for assessment in range(NUMBER_OF_ASSESSMENTS):
            # Run fuzzer and have it gernate new strings each assesment
            print('\t\t\t\t\tCurrent Eval :',eval, end='\r')
            time.sleep(0.001)
            set_holder = fuzz.generateStrings("random", STRINGS_PER_SET)
            result = fuzz.testStrings(_runNum=run,_evalNum=eval, _custom_input = set_holder)

            # Test if new string set is better than old
            if assessment == 0:
                best_string = set_holder
                best_eval = result
            else:
                if best_eval < result:
                    best_string = set_holder
                    best_eval = result
                    best_eval_info = str(run) + '__' + str(eval)
            #Log evaluation result       
            best_eval_holder.append(best_eval)
            general_eval_holder.append(result)
            
        print('\n')

        # Check if last run is better than current best run
        if float(best_eval) > float(best_run_fitness):
            best_run_fitness = best_eval
            best_run = best_eval_holder
            best_run_info = best_eval_info
        
        # Add last run to run storage
        best_run_holder.append(best_eval_holder)
        general_run_holder.append(general_eval_holder)


    #Plot resutls of all runs
    print('Best Fitness:', best_run_fitness)
    #print(best_run_holder)
    print('Best Location:', best_run_info)

    # Graph of best fitness seen by eval for every runs
    for run in range(len(best_run_holder)):
            bestxpoints = range(NUMBER_OF_ASSESSMENTS)
            bestypoints = best_run_holder[run]
            plt.plot(bestxpoints, bestypoints)
    plt.xlabel('Evaluation')
    plt.ylabel('Best Fitness Seen')
    #plt.title('Best Fitness Seen Graph for all Runs')
    fig1 = plt.figure()

    # Best Graph
    overallbestxpoint = range(NUMBER_OF_ASSESSMENTS)
    overallbestypoint = best_run
    plt.xlabel('Evaluation')
    plt.ylabel('Best Fitness Seen')
    plt.title('Best Fitness Seen Graph for Best Run')
    plt.plot(overallbestxpoint,overallbestypoint)

    # Box plot graph
    data_holder = []
    for eval_num in range(NUMBER_OF_ASSESSMENTS):
        average_at_eval = []
        for run in range(len(best_run_holder)):
                average_at_eval.append(best_run_holder[run][eval_num])
        data_holder.append(average_at_eval)
    fig, ax = plt.subplots()
    ax.set_xlabel('Evaluation')
    ax.set_ylabel('Fitness Range')
    ax.boxplot(data_holder)
    # Show graphs


    fig = plt.figure(1)
    fig.canvas.set_window_title('Figure 1')
    fig = plt.figure(2)
    fig.canvas.set_window_title('Figure 2')
    fig = plt.figure(3)
    fig.canvas.set_window_title('Figure 3')
    plt.show()

# TODO: add convergence and update graph labels
def hillClimb():
    best_run_holder = []        # Holds list of best_eval_holders
    general_run_holder = []     # Holds list of results of each eval per run
    best_run_fitness = 0.00
    best_run = []
    best_run_info = ''

    # Collect 30 runs of data
    for run in range(NUMBER_OF_RUNS):
        time.sleep(0.01)
        print('Starting Run Series:',run)
        best_eval_holder = []           # Holds best eval log
        general_eval_holder = []        # Hold results of each eval
        best_eval = 0.00                # Hold best eval total
        best_eval_info = ''             # Hold run and eval num of best

        # Collect NUMBER_OF_EVALS evals of data per run
        for eval in range(NUMBER_OF_ASSESSMENTS):
            # Run fuzzer
            print('\t\t\t\t\tCurrent Eval :',eval, end='\r')
            time.sleep(0.001)

            starting_string = fuzz.generateStrings('random', 50)
            starting_string_fitness=fuzz.testStrings(_custom_input = starting_string)
            mutated_strings = []
            if run >= 0:
                for k in range(2):
                    if k == 0:
                        mutated_strings = mutate_set(starting_string).string_set
                    else:
                        mutated_strings = mutate_set(best_string).string_set
                    for i in range(len(mutated_strings)):
                        mutated_fitness = fuzz.testStrings(_custom_input = mutated_strings[i])
                        if i == 0 or mutated_fitness >= starting_string_fitness:
                            starting_counter = 0
                            mutated_counter = 0
                            if mutated_fitness == starting_string_fitness:
                                for j in range(len(starting_string)):
                                    starting_counter += len(starting_string)
                                    mutated_counter += len(mutated_strings[i])
                                if starting_counter > mutated_counter:
                                    best_string_fitness = mutated_fitness
                                    best_string = mutated_strings[i]
                                    
                            else:
                                best_string_fitness = mutated_fitness
                                best_string = mutated_strings[i]
                #print(best_string_fitness)
            else:
                best_string = starting_string
                best_string_fitness = starting_string_fitness

            if best_string_fitness < starting_string_fitness:
                best_string = starting_string
                best_string_fitness = starting_string_fitness
            result = fuzz.main(_custom_input = best_string, _runNum=run, _evalNum=eval)
            # Update best eval so far
            if float(result) > float(best_eval):
                best_eval = result
                best_eval_info = str(run) + '__' + str(eval)
            best_eval_holder.append(best_eval)
            # Always add eval to data from this run
            general_eval_holder.append(result)
        print('\n')

        # Check if last run is better than current best run
        if float(best_eval) > float(best_run_fitness):
            best_run_fitness = best_eval
            best_run = best_eval_holder
            best_run_info = best_eval_info
        
        # Add last run to run storage
        best_run_holder.append(best_eval_holder)
        general_run_holder.append(general_eval_holder)


    #Plot resutls of all runs
    print('Best Fitness:', best_run_fitness)
    #print(best_run_holder)
    print('Best Location:', best_run_info)

    # Graph of best fitness seen by eval for every runs
    for run in range(len(best_run_holder)):
            bestxpoints = range(NUMBER_OF_ASSESSMENTS)
            bestypoints = best_run_holder[run]
            plt.plot(bestxpoints, bestypoints)
    plt.xlabel('Evaluation')
    plt.ylabel('Best Fitness Seen')
    #plt.title('Best Fitness Seen Graph for all Runs')
    fig1 = plt.figure()

    # Best Graph
    overallbestxpoint = range(NUMBER_OF_ASSESSMENTS)
    overallbestypoint = best_run
    plt.xlabel('Evaluation')
    plt.ylabel('Best Fitness Seen')
    plt.title('Best Fitness Seen Graph for Best Run')
    plt.plot(overallbestxpoint,overallbestypoint)

    # Box plot graph
    data_holder = []
    for eval_num in range(NUMBER_OF_ASSESSMENTS):
        average_at_eval = []
        for run in range(len(best_run_holder)):
                average_at_eval.append(best_run_holder[run][eval_num])
        data_holder.append(average_at_eval)
    fig, ax = plt.subplots()
    ax.set_xlabel('Evaluation')
    ax.set_ylabel('Fitness Range')
    ax.boxplot(data_holder)
    # Show graphs


    fig = plt.figure(1)
    fig.canvas.set_window_title('Figure 4')
    fig = plt.figure(2)
    fig.canvas.set_window_title('Figure 5')
    fig = plt.figure(3)
    fig.canvas.set_window_title('Figure 6')
    plt.show()

def EASearch():

    best_run_holder = []        # Holds list of best_eval_holders

    best_run_fitness = 0.00
    best_run = []
    best_run_info = ''
    generation_number_logger = []
    # Collect 30 runs of data
    for run in range(NUMBER_OF_RUNS):
        time.sleep(0.01)
        print('Starting Run Series:',run)

        run_fitness, run_log, generation = evolution.evolutionDriver(_evalNum = 0, _runNum = run)
        
        print('\n')

        # Check if last run is better than current best run
        if float(run_fitness) > float(best_run_fitness):
            best_run_fitness = run_fitness
            best_run = run_log
            best_run_info = str(run) + '__' + str(0)
            generation_number_logger.append(generation)
        
        # Add last run to run storage
        best_run_holder.append(run_log)

    #Plot resutls of all runs
    print('Best Fitness:', best_run_fitness)
    print('Best Location:', best_run_info)

    # Format data to account for different generation end numbers
    longest_generation = max(generation_number_logger)

    for run in range(len(best_run_holder)):
        run_length = len(best_run_holder[run])
        print('Run',str(run),' converged at generation', str(run_length))
        while len(best_run_holder[run]) < longest_generation:
            tmp_val = best_run_holder[run][len(best_run_holder[run])-1]
            best_run_holder[run].append(tmp_val)
    
    # Graph of best fitness seen by eval for every runs
    for run in range(len(best_run_holder)):
            bestxpoints = range(len(best_run_holder[run]))
            bestypoints = best_run_holder[run]
            runLabel = 'Run '+str(run)
            plt.plot(bestxpoints, bestypoints, label=runLabel)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Seen')
    #plt.title('Best Fitness Seen Graph for all Runs')
    fig1 = plt.figure()

    # Best Graph
    overallbestxpoint = range(len(best_run))
    overallbestypoint = best_run
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Seen')
    plt.title('Best Fitness Seen Graph for Best Run')
    plt.plot(overallbestxpoint,overallbestypoint)

    # Box plot graph
    data_holder = []
    for eval_num in range(longest_generation):
        average_at_eval = []
        for run in range(len(best_run_holder)):
                average_at_eval.append(best_run_holder[run][eval_num])
        data_holder.append(average_at_eval)
    fig, ax = plt.subplots()
    ax.set_xlabel('Evaluation')
    ax.set_ylabel('Fitness Range')
    ax.boxplot(data_holder)
    # Show graphs


    fig = plt.figure(1)
    fig.canvas.set_window_title('Figure 1')
    fig = plt.figure(2)
    fig.canvas.set_window_title('Figure 2')
    fig = plt.figure(3)
    fig.canvas.set_window_title('Figure 3')
    plt.show()

if __name__ == '__main__':
    #randomSearch()
    #hillClimb()
    EASearch()