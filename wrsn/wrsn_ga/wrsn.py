from population import Population

class WRSN :
    def __init__(self, data, maxIter, size):
        self.data = data
        self.maxIter = maxIter
        self.size = size
        self.gens_len = data['num_nodes']
        self.population = None

    def solver(self):
        self.population = Population(self.size, self.gens_len, self.data)
        self.population.initial_population()
        self.population.cal_fitness()
        it = 0
        while (it < self.maxIter):
            self.population.crossover()
            self.population.mutation()
            self.population.selection()
            self.log_state(it)
            it += 1

    def get_result(self):
        result = self.population.individuals[0]
        return result
    
    def log_state(self, it):
        print("---------------------------------------------------------------------------------------------------------------")
        print("Generation : ", it + 1)
        print("Best fitness: ", self.get_result().fitness)