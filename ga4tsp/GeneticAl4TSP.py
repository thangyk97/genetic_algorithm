from Population import Population

import numpy as np
import copy
import random

class GeneticAl4TSP(object):

    fittest_individual = None

    generation_count = 0

    """docstring for GeneticAl4TSP"""
    def __init__(self, distances, size_of_population, Rc, Rm):
        super(GeneticAl4TSP, self).__init__()
        self.distances = distances
        self.Rc = Rc
        self.Rm = Rm
        self.size_of_population = size_of_population
        self.elite_size = self.size_of_population // 4
        self.population = Population(distances.shape[0], size_of_population)
        self.population.calculate_fitness(distances)
        self.parents = []

    def select_parents(self):
        """"""
        tot_fitness = self.population.get_tot_fitness()
        parents_index = set()
        while len(parents_index) < self.size_of_population // 2:
            rd = random.random()*tot_fitness
            for idx, item in enumerate(self.population.individuals):
                rd = rd - item.fitness
                if rd <= 0:
                    parents_index.add(idx)
                    break

        parents_index = list(parents_index)
        random.shuffle(parents_index)

        self.parents = []
        print(len(parents_index), "   ",parents_index)
        for idx in parents_index:
            self.parents.append(copy.deepcopy(self.population.individuals[idx]))

    def breed(self, individual_a, individual_b):
        points = random.sample(range(1, individual_a.len_of_routes), 2)
        first_point = points[0] if points[0] < points[1] else points[1]
        second_point = points[0] if points[0] >= points[1] else points[1]
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
        for i in range(0, len(self.parents), 2):
            if random.random() <= self.Rc:
                self.breed(self.parents[i], self.parents[i+1])
        for indiv in self.parents:
            _ = indiv.get_fitness(self.distances)
        self.population.individuals = self.population.individuals + self.parents


        # remove least fitness individual
        self.population.rank_individuals()
        self.population.individuals = self.population.individuals[:self.size_of_population]
        self.fittest_individual = self.population.individuals[0]

    def mutation(self):
        for i in range(self.size_of_population):
            if random.random() <= self.Rm:
                points = random.sample(range(1, self.population.individuals[i].len_of_routes - 1), 2)
                temp = self.population.individuals[i].routes[points[0]]
                self.population.individuals[i].routes[points[0]] = self.population.individuals[i].routes[points[1]]
                self.population.individuals[i].routes[points[1]] = temp

    def evolution(self):
        it = 0
        while it < 10:
            print("Generation " + str(it))
            self.select_parents()
            self.crossover()
            self.mutation()
            # print(1 / self.fittest_individual.fitness)
            it += 1

def cal_distance_matrix_from_coordinate(coord):
    n = coord.shape[0]
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i][j] = np.sqrt((coord[i][1] - coord[j][1])**2 + (coord[i][2] - coord[j][2])**2)
    return distances

def main():
    # Load data
    coord = np.loadtxt('ch150.txt')
    distances = cal_distance_matrix_from_coordinate(coord)

    # Calculate and get min result after N running times
    result = float('-inf')
    r = []
    for i in range(2):
        ga = GeneticAl4TSP(distances=distances, size_of_population=100, Rc=0.6, Rm=0.01)
        ga.evolution()
        if ga.fittest_individual.fitness > result:
            result = ga.fittest_individual.fitness
            r = ga.fittest_individual.routes
    print(1 / result)
    print(r)



if __name__ == '__main__':
    main()