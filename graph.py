#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

import copy
import os
import random
import time

import matplotlib.pyplot as plt

import evolutionary_algorithm


FILENAME_COUNTER = 1
SAVE_TO_FILE = 1  # 0 = display on the screen, don't save; 1 = save to file, don't display
NUM_OF_ITERATIONS = 3  # Number of test iterations, smoothens out the graph. Higher numbers require more time. More than 3 is not worth it.


def print_progress(current, max):
	progress = int(current / max * 100)
	print(f'{progress}%')


def find_best(population_size, target, valid_genes, mutation_chance, max_expenses):
	evolution = evolutionary_algorithm.EvolutionaryAlgorithm(population_size, target, valid_genes, mutation_chance)
	expenses = evolution.get_fitness_expenses()
	#print(expenses)
	#evolution.print_best()
	last_time = time.time()
	while expenses < max_expenses:
		evolution.do_next_iteration()
		expenses = evolution.get_fitness_expenses()
		if expenses > max_expenses:
			break
		current_time = time.time()
		if current_time > last_time + 1:
			print_progress(expenses, max_expenses)
			last_time = current_time
		#evolution.print_best()
	return evolution.get_one_best()


def get_best_of_x(function, *args, **kwargs):
	fitness_sum = 0
	num_of_iterations = NUM_OF_ITERATIONS
	for i in range(num_of_iterations):
		print(f'{i}/10')
		result = function(*args, **kwargs)
		fitness_sum += result.get_fitness()
	fitness_avg = fitness_sum / num_of_iterations
	print(fitness_avg)
	return fitness_avg


def show_plot(plt, y_max):
	global FILENAME_COUNTER
	plt.xlabel("number of individuals")
	plt.ylabel("fitness (less = better)")
	axes = plt.gca()
	axes.set_ylim([0, y_max])
	plt.legend()
	plt.grid()
	if SAVE_TO_FILE:
		folder_name = "graphs"
		if not os.path.exists(folder_name):
			os.makedirs(folder_name)
		plt.savefig(f'{folder_name}/{FILENAME_COUNTER}.png')
	else:
		plt.show()
	plt.clf()
	FILENAME_COUNTER += 1


def test_population_sizes(function, population_sizes, target, valid_genes, mutation_chance, max_expenses_list, colors):
	i = 0
	for max_expenses in max_expenses_list:
		y_data = []
		print(f"max_expenses: {max_expenses} <===========")
		for population_size in population_sizes:
			print(f"population_size: {population_size}")
			y_data.append(get_best_of_x(function, population_size, target, valid_genes, mutation_chance, max_expenses))
		plt.plot(population_sizes, y_data, f"{colors[i]}-", label = f"max_expenses: {max_expenses}")
		i += 1
	plt.title(f"Results quality for a given population size")
	show_plot(plt, len(target))


if __name__ == "__main__":
	population_sizes = [2, 4, 6, 8, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
	target = 'Wstęp do sztucznej inteligencji - zad 2.1'
	valid_genes = list('aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżźAĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUVWXYZŻŹ1234567890!@#$%^&*() .,?<>[]{};:"-_=+~`| \\\'')
	mutation_chance = 0.01
	max_expenses_list = [5000, 10000, 50000, 100000, 200000]
	graph_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
	
	if len(max_expenses_list) > len(graph_colors):
		print("Not enough colors!")
		exit(0)
	
	test_population_sizes(find_best, population_sizes, target, valid_genes, mutation_chance, max_expenses_list, graph_colors)
	