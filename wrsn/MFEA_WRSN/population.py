from individual import Individual
import random
import numpy as np

class Population:
    def __init__(self, size, gens_len, data):
        self.data = data
        self.individuals = []
        self.size = size
        self.gens_len = gens_len
        self.Rmp = 0.1
        self.Rm = 0.01
        

    def initial_population(self):
        it = 0
        while (it < self.size):
            i = Individual(self.gens_len)
            if i.is_satified(self.data):
                self.individuals.append(i)
                it += 1
        print("\nInitial population complete.\n")
    
    def crossover(self):
        pairs = np.random.permutation(self.size)
        for i in range(0, self.size , 2):
            indiv_a = self.individuals[pairs[i]]
            indiv_b = self.individuals[pairs[i+1]]
            if indiv_a.skill_factor == indiv_b.skill_factor or random.random() <= self.Rmp:
                child_1, child_2 = self.breed(indiv_a, indiv_b)
                child_1.cal_fitness(self.data)
                child_2.cal_fitness(self.data)
                self.individuals.append(child_1)
                self.individuals.append(child_2)

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
        child_a = Individual(self.gens_len)
        child_a.gens = gens_a
        child_a.skill_factor = skill_a
        child_b = Individual(self.gens_len)
        child_b.gens = gens_b
        child_b.skill_factor = skill_b
        return child_a, child_b

    def mutation(self):
        for i in range(self.size):
            if random.random() <= self.Rm:
                points = random.sample(range(1, self.individuals[i].gens_len - 2), 2)
                temp = self.individuals[i].gens[points[0]]
                self.individuals[i].gens[points[0]] = self.individuals[i].gens[points[1]]
                self.individuals[i].gens[points[1]] = temp

    def selection(self):
        self.individuals = sorted(self.individuals, key=lambda x: x.scalar_fitness, reverse=True)
        self.individuals = self.individuals[:self.size]

    def cal_fitness(self):
        for x in self.individuals:
            x.cal_fitness(self.data)

    def update_scalar_fitness(self):
        self.rank_individual()
        for x in self.individuals:
            x.cal_scalar_fitness()

    def cal_scalar_fitness(self):
        for x in self.individuals:
            x.cal_scalar_fitness()

    def rank_all(self):
        for i in range(self.data.__len__()):
            self.individuals = sorted(self.individuals, key=lambda x: x.fitness[i], reverse=True)
            for idx, idv in enumerate(self.individuals):
                idv.ranks.append(idx + 1)

    def rank_individual(self):
        for i in range(self.data.__len__()):
            temp = [idv for idv in self.individuals if idv.skill_factor == i]
            temp = sorted(temp, key=lambda x: x.fitness[i], reverse=True)
            for idx, idv in enumerate(temp):
                idv.ranks = [float('inf')] * self.data.__len__()
                idv.ranks[i] = idx + 1