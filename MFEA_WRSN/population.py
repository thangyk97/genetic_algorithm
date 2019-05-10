from individual import Individual
import random

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

    def breed(self, indiv_a, indiv_b):
        gens_a = indiv_a.get_gens().copy()
        gens_b = indiv_b.get_gens().copy()

        skill_a = indiv_a.skill_factor
        skill_b = indiv_b.skill_factor
        
        points = random.sample(range(1, gens_a.__len__() - 1), 2)
        first_point = points[0] if points[0] < points[1] else points[1]
        second_point = points[0] if points[0] >= points[1] else points[1]

        # Copy cross 2 parent at between 2 slash point
        for i in range(first_point, second_point):
            # individual a
            if gens_a[i] != indiv_b.gens[i]:
                gens_a[gens_a.index(indiv_b.gens[i])] = gens_a[i]
                gens_a[i] = indiv_b.gens[i]
            # individual b
            if gens_b[i] != indiv_a.gens[i]:
                gens_b[gens_b.index(indiv_a.gens[i])] = gens_b[i]
                gens_b[i] = indiv_a.gens[i]

        # Assign skill factor for offspring
        if indiv_a.skill_factor == indiv_b.skill_factor:
            skill_a = indiv_a.skill_factor
            skill_b = indiv_a.skill_factor
        elif random.random() <= 0.5:
            skill_a = indiv_a.skill_factor
            skill_b = indiv_a.skill_factor
        else:
            skill_a = indiv_b.skill_factor
            skill_b = indiv_b.skill_factor

        return 

    def mutation(self):
        pass

    def selection(self):
        pass

    def update_fitness(self):
        
        pass

    def rank_individual(self):
        pass