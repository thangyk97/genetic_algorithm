from individual import Individual

class Population:
    def __init__(self, size, gens_len, data):
        self.data = data
        self.individuals = []
        self.size = size
        self.gens_len = gens_len
        

    def initial_population(self):
        it = 0
        while (it < self.size):
            i = Individual(self.gens_len)
            if i.is_satified(self.data):
                self.individuals.append(i)
                it += 1
        print("\nInitial population complete.\n")
    
    def crossover(self):
        pass

    def breed(self, individual_1, individual_2):
        pass

    def mutation(self):
        pass

    def selection(self):
        pass

    def update_fitness(self):
        pass