from Population import Population

import numpy as np
import copy
import random

class GeneticAl4TSP(object):

    fittest_individual = None

    generation_count = 0

    """docstring for GeneticAl4TSP"""
    def __init__(self, distances, size_of_population):
        super(GeneticAl4TSP, self).__init__()
        self.distances = distances
        self.size_of_population = size_of_population
        self.elite_size = self.size_of_population // 4
        self.population = Population(distances.shape[0], size_of_population)
        self.selection_result = []

    def selection(self):
        """"""
        self.population.rank_individuals()
        random_selection = np.random.randint(self.elite_size, self.size_of_population, self.elite_size)
        
        # Select elite individuals and random elite_size other individual
        self.selection_result = []
        for i in range(self.elite_size):
            self.selection_result.append(copy.deepcopy(self.population.individuals[i]))
            self.selection_result.append(copy.deepcopy(self.population.individuals[random_selection[i]]))

    def breed(self, individual_a, individual_b):
        first_point = individual_a.len_of_routes // 3
        second_point = first_point * 2
        routes_a = individual_a.routes.copy()
        routes_b = individual_b.routes.copy()

        # Copy cross 2 parent at between 2 slash point
        for i in range(first_point, second_point):
            # individual a
            if individual_a.routes[i] != routes_b[i]:
                individual_a.routes[individual_a.routes.index(routes_b[i])] = individual_a.routes[i]
                individual_a.routes[i] = routes_b[i]
            # individual b
            if individual_b.routes[i] != routes_a[i]:
                individual_b.routes[individual_b.routes.index(routes_a[i])] = individual_b.routes[i]
                individual_b.routes[i] = routes_a[i]


    def crossover(self):
        for i in range(0, len(self.selection_result), 2):
            self.breed(self.selection_result[i], self.selection_result[i+1])
        for indiv in self.selection_result:
            _ = indiv.get_fitness(self.distances)
        self.population.individuals = self.population.individuals + self.selection_result
        self.population.rank_individuals()

        # remove least fitness individual
        self.population.individuals = self.population.individuals[:self.size_of_population]
        print(len(self.population.individuals))
        self.fittest_individual = self.population.individuals[0]

    def mutation(self):
        mutation_individuals = random.sample(range(self.size_of_population), 10)
        for i in mutation_individuals:
            points = random.sample(range(1, self.population.individuals[i].len_of_routes - 1), 2)
            temp = self.population.individuals[i].routes[points[0]]
            self.population.individuals[i].routes[points[0]] = self.population.individuals[i].routes[points[1]]
            self.population.individuals[i].routes[points[1]] = temp

    def evolution(self):
        it = 0
        while it < 10:
            self.selection()
            self.crossover()
            self.mutation()
            print(self.fittest_individual.fitness)
            it += 1

def main():
    distances = np.array(     [[ 0,  4, 13, 15, 24,  4, 31, 18,  6, 21],
                               [ 4,  0,  8, 33,  9, 61,  7, 61,  7, 31],
                               [13,  8,  0, 22,  6, 33,  2, 33, 19, 41],
                               [15, 33, 22,  0,  3,  5, 62,  9, 41,  5],
                               [24,  9,  6,  3,  0, 18, 12,  4, 17,  9],
                               [ 4, 61, 33,  5, 18,  0,  1, 35,  9, 17],
                               [31,  7,  2, 62, 12,  1,  0, 19, 91,  8],
                               [18, 61, 33,  9,  4, 35, 19,  0, 77,  7],
                               [ 6,  7, 19, 41, 17,  9, 91, 77,  0, 11],
                               [21, 31, 41,  5,  9, 17,  8,  7, 11,  0]])



    for i in range(10): distances[i, i] = 0

    ga = GeneticAl4TSP(distances, 400)
    ga.evolution()
    print(ga.fittest_individual.routes)



if __name__ == '__main__':
    main()