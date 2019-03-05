from Individual import Individual
import numpy as np

class Population(object):
    """docstring for Population"""
    def __init__(self, num_city, size_of_population):
        super(Population, self).__init__()
        
        self.num_city           = num_city
        self.size_of_population = size_of_population

    def generate_rd_population(self):
        # Initial population of routes
        self.individuals = []
        for _ in range(self.size_of_population):
            self.individuals.append(Individual(self.num_city))

    def calculate_fitness(self, distances_matrix):
        """Calculate fitness of each individual"""
        for indiv in self.individuals:
            _ = indiv.get_fitness(distances_matrix)
        self.num_task = len(distances_matrix)

    def calculate_skill_factor(self):
        # Rank with each task
        for i in range(self.num_task):
            self.individuals = sorted(self.individuals, key=lambda x: x.fitness[i], reverse=True)
            for idx, idv in enumerate( self.individuals ):
                idv.rank[i] = idx
        # Calculate skill factor
        max_idv_per_task = self.size_of_population // self.num_task
        count_idv = [0 for _ in range(self.num_task)]
        for idv in self.individuals:
            for _ in range(self.num_task):
                skill_factor = np.argmin(idv.rank)
                if count_idv[skill_factor] < max_idv_per_task:
                    idv.skill_factor = skill_factor
                    count_idv[skill_factor] += 1
                    break
                else: 
                    idv.rank[skill_factor] = float('inf')



    def get_least_fittest_index(self):
        min_fitness = float('-inf')
        least_fittest_index = 0
        for i, indiv in enumerate(self.individuals):
            if indiv.fitness < min_fitness:
                min_fitness = indiv.fitness
                least_fittest_index = i
        return least_fittest_index

    def get_tot_fitness(self):
        tot_fitness = 0.0
        for i in self.individuals:
            tot_fitness += i.fitness
        return tot_fitness