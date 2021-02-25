#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

import copy
import random


class Individual:

	def __init__(self, genome):
		self.__genome = genome
		self.__fitness = None

	def get_fitness(self):
		return self.__fitness

	def set_fitness(self, fitness):
		self.__fitness = fitness

	def get_genome(self):
		return self.__genome

	def set_genome(self, genome):
		self.__genome = genome

	def get_phenotype(self):
		return ''.join(self.__genome)


class EvolutionaryAlgorithm:

	def __init__(self, population_size, target, valid_genes, mutation_chance):
		self.__target = target
		self.__valid_genes = valid_genes
		self.__mutation_chance = mutation_chance
		self.__population = []
		self.__population_size = 0
		self.__iteration = 0
		self.__fitness_expenses = 0
		self.__add_individuals(population_size)
		self.__calculate_fitness_for_population()

	def __add_individuals(self, num_of_individuals):
		for _ in range(num_of_individuals):
			self.__population.append(self.__generate_random_individual())
		self.__population_size += num_of_individuals

	def __generate_random_individual(self):
		genome = self.__generate_random_genome()
		individual = Individual(genome)
		return individual

	def __calculate_fitness_for_population(self):
		for individual in self.__population:
			fitness = self.__calculate_fitness(individual)
			individual.set_fitness(fitness)
			self.__fitness_expenses += 1

	def __calculate_fitness(self, individual):
		phenotype = individual.get_phenotype()
		fitness = len(self.__target)
		for i in range(fitness):
			if self.__target[i] == phenotype[i]:
				fitness -= 1
		return fitness  # less = better

	def __get_random_gene(self):
		selected_gene_index = random.randint(0,len(self.__valid_genes) - 1)
		return self.__valid_genes[selected_gene_index]

	def __generate_random_genome(self):
		genome_len = len(self.__target)
		genome = []
		for _ in range(genome_len):
			genome.append(self.__get_random_gene())
		return genome

	def __get_better_opponent(self, opponent_1, opponent_2):
		if opponent_1.get_fitness() < opponent_2.get_fitness():
			return opponent_1
		elif opponent_1.get_fitness() > opponent_2.get_fitness():
			return opponent_2
		else:
			return random.choice([opponent_1, opponent_2])

	def __do_tournament_selection(self):
		num_of_fights = self.__population_size
		new_population = []
		for _ in range(num_of_fights):
			opponent_1 = random.choice(self.__population)
			opponent_2 = random.choice(self.__population)
			better_opponent = self.__get_better_opponent(opponent_1, opponent_2)
			new_population.append(copy.deepcopy(better_opponent))
		return new_population

	def __do_generational_succession(self, new_population):
		self.__population = new_population

	def __mutate_population(self, population):
		for individual in population:
			genome = individual.get_genome()
			for i in range(len(genome)):
				if random.random() < self.__mutation_chance:
					genome[i] = self.__get_random_gene()
			individual.set_genome(genome)

	def get_iteration(self):
		return self.__iteration

	def get_fitness_expenses(self):
		return self.__fitness_expenses

	def do_next_iteration(self):
		new_population = self.__do_tournament_selection()
		self.__mutate_population(new_population)
		self.__do_generational_succession(new_population)
		self.__calculate_fitness_for_population()
		self.__iteration += 1

	def get_best_individuals(self):
		best_fitness = None
		for individual in self.__population:
			if best_fitness is None or individual.get_fitness() < best_fitness:
				best_fitness = individual.get_fitness()
		best_individuals = []
		for individual in self.__population:
			if individual.get_fitness() == best_fitness:
				best_individuals.append(individual)
		return best_individuals

	def get_one_best(self):
		best_individuals = self.get_best_individuals()
		example_best_individual = random.choice(best_individuals)
		return example_best_individual

	def print_one_best(self):
		example_best_individual = self.get_one_best()
		phenotype = example_best_individual.get_phenotype()
		fitness = example_best_individual.get_fitness()
		print(f'iteration: {self.get_iteration()}, fitness: {fitness}, phenotype: \'{phenotype}\'')