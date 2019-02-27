from Individual import Individual

class Population(object):
    """docstring for Population"""
    def __init__(self, num_city, size_of_population):
        super(Population, self).__init__()
        self.num_city = num_city

        # Initial population of routes
        self.individuals = []
        for i in range(size_of_population):
            self.individuals.append(Individual(num_city))

    def calculate_fitness(self, distances):
        """Calculate fitness of each individual"""
        for indiv in self.individuals:
            _ = indiv.get_fitness(distances)

    def get_least_fittest_index(self):
        min_fitness = float('-inf')
        least_fittest_index = 0
        for i, indiv in enumerate(self.individuals):
            if indiv.fitness < min_fitness:
                min_fitness = indiv.fitness
                least_fittest_index = i
        return least_fittest_index

    def rank_individuals(self):
        self.individuals = sorted(self.individuals, key=lambda x: x.fitness, reverse=True)

    def get_tot_fitness(self):
        tot_fitness = 0.0
        for i in self.individuals:
            tot_fitness += i.fitness
        return tot_fitness
