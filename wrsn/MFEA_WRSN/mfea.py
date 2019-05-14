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
        self.population.cal_fitness()
        self.population.rank_all()
        self.population.cal_scalar_fitness()
        it = 0
        while (it < self.maxIter):
            self.population.crossover()
            self.population.mutation()
            self.population.update_scalar_fitness()
            self.population.selection()
            self.log_state(it)
            it += 1

    def get_result(self)->list:
        result = []
        for i in range(self.data.__len__()):
            for x in self.population.individuals:
                if (x.skill_factor == i):
                    x
                    result.append(x)
                    break
        return result

    
    def log_state(self, it):
        print("---------------------------------------------------------------------------------------------------------------")
        print("Generation : ", it)
        result = self.get_result()
        for i, r in enumerate(result):
            print("Task " + str(i) + ": " + str(r.fitness[i]))


