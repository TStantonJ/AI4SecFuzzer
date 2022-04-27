import random
import copy
import numpy


# ------------Functions for parent selction------------



# Uniform Random Selection(Fitness Indipendent)
# -Takes a population and how many individuals(n) to return from it
# -Returns n individuals
def uniform_random_selection(population, n, **kwargs):
	# Pick n random individuals 
	return random.choices(population, k=n)


# K Tournament With Replacement
# -Takes a population, how many individuals(n) to return from it, and how many individuals
#   should be in a tournament(k)
# -Returns n individuals who won their k sized tournaments(can win multiple times)
def k_tournament_with_replacement(population, n, **kwargs):
	# Initalize pool of chosen parents
	winners_bracket = []
	
	# Itterator for how many winners there should be
	current_member = 0
	while current_member < n:
		# Refresh sample population for each tournament to make this with replacement
		holder = []
		for individual in population:
			holder.append(individual)

		# Destructively draw k individuals from population holder
		tourney = random.sample(holder, kwargs.get('k'))
        # Best Fighter's fitness variable
		best_fighter = 0
		# Hold a brawl between the k chosen individuals
		for i in range(len(tourney)):
			# Fist one always is the best fighter in the first round
			if i == 0:
				best_fighter = tourney[i]
			# Compare to previous best fighter
			if tourney[i].fitness > best_fighter.fitness:
				best_fighter = tourney[i]
		# Add winner to the bracket
		winners_bracket.append(best_fighter)
		current_member += 1
	return winners_bracket



# ------------Fuctions for Survival Selectoion------------



# K Tournament without Replacement Selection
# -Takes a population, how many individuals(n) to return from it, and tournament size(k)
# -Returns n individuals who won their k sized tournaments(can not win multiple times)
def k_tournament_without_replacement(population, n, **kwargs):
	winners_bracket = []
	# Copy population
	#holder = [copy.deepcopy(x) for x in population]
	holder = []
	for individual in population:
		holder.append(individual)

	# Make sure tournament size isn't too small
	if kwargs.get('k') >= len(population) - n + 1:
		raise Exception('k >= popsize - selecsize + 1')
	
	# Itterator how how many winners there should be
	current_member = 0
	while current_member < n:
		# Refresh population for each tournament to make this with replacement (Sans winner if one already)
		holder = []
		for individual in population:
			if individual not in winners_bracket:
				holder.append(individual)

		# Destructively draw k individuals from population holder
		tourney = random.sample(holder, kwargs.get('k'))
		best_fighter = None

		# Hold a brawl between the k chosen individuals
		for i in range(len(tourney)):
			# Fist one always is the best fighter in the first round unless it already won
			if best_fighter == None:
				if tourney[i] in winners_bracket:
					pass
				else:
					best_fighter = tourney[i]

			# Compare to previous best fighter unless there is none or someone like has won already
			if best_fighter != None:
				if tourney[i].fitness > best_fighter.fitness:
					if tourney[i] in winners_bracket:
						pass
					else:
						best_fighter = tourney[i]

		# Add winner to the bracket unless there is none
		if best_fighter != None:
			winners_bracket.append(best_fighter)
			current_member += 1

	return winners_bracket