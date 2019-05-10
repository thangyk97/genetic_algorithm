from population import Population

class MFEA :
    def __init__(self, data, maxIter, size, gens_len):
        self.data = data
        self.maxIter = maxIter
        self.size = size
        self.gens_len = gens_len
        self.population = None

    def solver(self):
        self.population = Population(self.size, self.gens_len, self.data)
        self.population.initial_population()
        self.population.update_fitness()
        it = 0
        while (it < self.maxIter):
            self.population.crossover()
            self.population.mutation()
            self.population.selection()
            self.log_state(it)
            it += 1
    
    def log_state(self, it):
        print("---------------------------------------------------------------------------------------------------------------")
        print("Generation : ", it)
        print("best fitness = ", 0)


