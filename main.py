#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

import copy
import time

import evolutionary_algorithm


def print_progress(current, max):
	progress = int(current / max * 100)
	print(f'{progress}%')


def find_best(population_size, target, valid_genes, mutation_chance, max_expenses):
	evolution = evolutionary_algorithm.EvolutionaryAlgorithm(population_size, target, valid_genes, mutation_chance)
	expenses = evolution.get_fitness_expenses()
	last_time = time.time()
	best_individual = None
	while max_expenses is None or (expenses < max_expenses):
		evolution.do_next_iteration()
		expenses = evolution.get_fitness_expenses()
		if max_expenses is not None and expenses > max_expenses:
			break
		current_time = time.time()
		if current_time > last_time + 1:
			if max_expenses is None:
				print(".", end = "", flush = True)
			else:
				print_progress(expenses, max_expenses)
			last_time = current_time
		best_individual = copy.deepcopy(evolution.get_one_best())
		if best_individual.get_fitness() == 0:
			break
	if max_expenses is None:
		print()
	return best_individual


if __name__ == "__main__":
	population_size = 100
	target = 'Wstęp do sztucznej inteligencji - zad 2.1'
	valid_genes = list('aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżźAĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUVWXYZŻŹ1234567890!@#$%^&*() .,?<>[]{};:"-_=+~`| \\\'')
	mutation_chance = 0.01
	
	print(f"{population_size = }\n")
	
	max_expenses = 50000
	print(f"{max_expenses = }")
	best_individual = find_best(population_size, target, valid_genes, mutation_chance, max_expenses)
	print(best_individual.get_phenotype())
	
	print()
	
	max_expenses = None
	print(f"{max_expenses = }")
	best_individual = find_best(population_size, target, valid_genes, mutation_chance, max_expenses)
	print(best_individual.get_phenotype())
	