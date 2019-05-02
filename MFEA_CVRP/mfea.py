import numpy as np
import random
import copy
from population import Population

class MFEA(object):
    
    def __init__(self, distances_matrix, size_of_population):
        super(MFEA, self).__init__()
        self.distances_matrix   = distances_matrix
        self.num_task           = len(distances_matrix)
        self.size_of_population = size_of_population
        self.offspring          = []
        self.Rmp                = 0.2
        self.Rm                 = 0.01

    def generate_population(self):
        num_city = 0
        for d in self.distances_matrix:
            if len(d) > num_city : num_city = len(d)
        self.population = Population(num_city, self.size_of_population)
        self.population.generate_rd_population()

    def evaluate_population(self):
        self.population.calculate_routes_distances(self.distances_matrix)

    def cal_skill_factor(self):
        self.population.calculate_scalar_fitness_and_skill_factor()

    def crossover(self):
        pairs = np.random.permutation(self.size_of_population)
        for i in range(0, self.size_of_population , 2):
            indiv_a = self.population.individuals[pairs[i]]
            indiv_b = self.population.individuals[pairs[i+1]]
            if indiv_a.skill_factor == indiv_b.skill_factor or random.random() <= self.Rmp:
                self.breed(indiv_a, indiv_b)
    
    def breed(self, indiv_a, indiv_b):
        individual_a = copy.deepcopy(indiv_a)
        individual_b = copy.deepcopy(indiv_b)

        points = random.sample(range(1, individual_a.len_of_routes - 1), 2)
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

        # Assign skill factor for offspring
        if indiv_a.skill_factor == indiv_b.skill_factor:
            individual_a.skill_factor = indiv_a.skill_factor
            individual_b.skill_factor = indiv_a.skill_factor
        elif random.random() <= 0.5:
            individual_a.skill_factor = indiv_a.skill_factor
            individual_b.skill_factor = indiv_a.skill_factor
        else:
            individual_a.skill_factor = indiv_b.skill_factor
            individual_b.skill_factor = indiv_b.skill_factor

        self.offspring.append(individual_a)
        self.offspring.append(individual_b)

    def mutation(self):
        for i in range(self.size_of_population):
            if random.random() <= self.Rm:
                points = random.sample(range(1, self.population.individuals[i].len_of_routes - 1), 2)
                temp = self.population.individuals[i].routes[points[0]]
                self.population.individuals[i].routes[points[0]] = self.population.individuals[i].routes[points[1]]
                self.population.individuals[i].routes[points[1]] = temp

    def evaluate_offspring(self):
        for idv in self.offspring:
            idv.cal_routes_distances_4_specific_task(self.distances_matrix[idv.skill_factor], idv.skill_factor)
    
    def re_cal_scalar_fitness(self):
        for i in range(self.num_task):
            temp = [idv for idv in self.population.individuals if idv.skill_factor == i]
            temp = sorted(temp, key=lambda x: x.distances[i], reverse=False)
            for idx, idv in enumerate(temp):
                idv.rank[i] = idx + 1
                idv.scalar_fitness = 1 / (idx + 1)

    def selection(self):
        self.population.individuals = sorted(self.population.individuals, key=lambda x: x.scalar_fitness, reverse=True)
        self.population.individuals = self.population.individuals[:self.size_of_population]

    def solve(self, max_it):
        it = 0
        self.generate_population()
        self.evaluate_population()
        self.cal_skill_factor()

        while it < max_it:
            print("it : ", it, ", population size = ", len(self.population.individuals))
            # Crossover and Mutation
            self.crossover()
            self.mutation()
            # Evaluate off-spring for selecting optimization task
            self.evaluate_offspring()
            # Concate current population and off-springs
            self.population.individuals = self.population.individuals + self.offspring
            # Selection individual to survive
            self.re_cal_scalar_fitness()
            self.selection()

            it += 1
        
        output = [0 for _ in range(self.num_task)]
        for i in range(self.num_task):
            for idv in self.population.individuals:
                if idv.skill_factor == i:
                    output[i] = idv
                    break

        return [indv.distances[indv.skill_factor] for indv in output]