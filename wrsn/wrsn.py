# @author [thang nguyen dinh]
# @email [thangyk97@gmail.com]
# @create date 2019-03-26 11:02:32
# @modify date 2019-04-04 10:23:11
# @desc [description]

from population import Population
from individual import Individual
import numpy as np
import copy
import random

class WRSN(object):
    """
    Implement of HPSOGA for Wireless Rechargeable Sensor Networks (WRSNs)
    Properties:
    ---------

    """

    fittest_individual = None
    generation_count = 0

    def __init__(self, size_of_population, c_1, c_2, data, sensor_info, distances,):
        """
        Parameters:
        ----------
        distances (numpy 2d array): the distance matrix
        size_of_population (int):
        """
        super(WRSN, self).__init__()
        self.distances = distances
        self.size_of_population = size_of_population
        self.c_1 = c_1
        self.c_2 = c_2
        self.data = data
        self.sensor_info = sensor_info
        self.num_sensor = distances.shape[0] - 1
        self.num_come_back = 1
        self.population = Population(num_sensor=self.num_sensor,
                                    num_come_back=self.num_come_back,
                                    size_of_population=size_of_population,
                                    data = self.data,
                                    sensor_info = self.sensor_info,
                                    distances = self.distances)

        # Calculate fitness for each individual
        self.population.calculate_fitness(distances)

    def selection(self):
        """
        Select individual for new generation
        """
        highest_index = self.population.get_highest_fitness_index()
        lowest_index = self.population.get_least_fitness_index()
        highest = self.population.individuals[highest_index]
        if highest.fitness > self.population.global_best_individual.fitness:
            self.population.global_best_individual = highest
        self.population.individuals[lowest_index] = self.population.global_best_individual
        self.population.population_best_individual = self.population.individuals[highest_index]

    def breed(self, individual_a, individual_b):
        """
        Acording to Order Crossover (OX)
        Return 2 children
        """
        # Calculate p and q
        _rand = np.random.randint(1, individual_a.cycle_length-1, 2)
        p = min(_rand)
        q = max(_rand)

        cycle_a = individual_a.cycle[q+1:] + individual_a.cycle[0:q+1]
        cycle_b = individual_b.cycle[q+1:] + individual_b.cycle[0:q+1]
        interval_a = individual_a.cycle[p: q+1]
        interval_b = individual_b.cycle[p: q+1]
        for i in range(q-p+1):
            try :
                cycle_a.remove(interval_b[i])
                cycle_b.remove(interval_a[i])
            except ValueError:
                pass

        children_a = Individual(num_sensor=self.num_sensor,
                                num_come_back=self.num_come_back,
                                data = self.data,
                                sensor_info = self.sensor_info)
        children_b = Individual(num_sensor=self.num_sensor,
                                num_come_back=self.num_come_back,
                                data = self.data,
                                sensor_info = self.sensor_info)

        cycle_a = interval_b + cycle_a
        cycle_b = interval_a + cycle_b

        # Rotate
        children_a.cycle = cycle_a[self.num_sensor + self.num_come_back - q -1:] +\
                                 cycle_a[:self.num_sensor + self.num_come_back - q -1]
        children_b.cycle = cycle_b[self.num_sensor + self.num_come_back - q -1:] +\
                                 cycle_b[:self.num_sensor + self.num_come_back - q -1]
        return [children_a, children_b]

    def crossover(self, k1, k2):
        """
        Has 2 part:
        1. Select random pair and calculate crossover probability
        2. Breed 2 parents of each pair
        """
        p_c = 1.0

        avg_fitness = self.population.get_avg_fitness()
        f_max = self.population.individuals[self.population.get_highest_fitness_index()].fitness
        
        random_list_index = np.reshape(np.random.permutation(self.size_of_population), (-1, 2))
        for pair_index in random_list_index:
            indv0 = self.population.individuals[pair_index[0]]
            indv1 = self.population.individuals[pair_index[1]]

            # Calculate crossover probability
            higher_fitness_of_pair = indv0.fitness if indv0.fitness > indv1.fitness else indv1.fitness
            if higher_fitness_of_pair < avg_fitness:
                p_c = k1
            else:
                p_c = k1 - k2 * ((f_max- higher_fitness_of_pair) / (f_max - avg_fitness))

            # Breed
            if random.random() <= p_c:
                child0, child1 = self.breed(indv0, indv1)
                # Replace parent by children
                if child0.is_satify_constraints(self.distances):
                    self.population.individuals[pair_index[0]] = child0
                if child1.is_satify_constraints(self.distances):
                    self.population.individuals[pair_index[1]] = child1

    def evolution(self, maxIter):
        it = 0
        m_obj = Mutation(self.c_1, self.c_2, self.population)
        while it < maxIter:
            print("Generation " + str(it))
            self.selection()
            self.crossover(k1=0.5, k2=0.5)
            m_obj.mutation()

            it += 1
    def solve(self, maxIter=100):
        self.evolution(maxIter)
        idx = self.population.get_highest_fitness_index()
        best = self.population.individuals[idx]
        print(best.fitness)

class Mutation():
    def __init__(self, c_1, c_2, population):
        self.c_1 = c_1
        self.c_2 = c_2
        self.population = population

    def encode_cycle2position(self, cycle):
        """
        Encode chromosome of cycle to position
        Parameters:
        ---------
        cycle (list):
        Return: list

        """
        position = [0]*len(cycle)
        for i in range(len(cycle)):
            position[i] = cycle[(cycle.index(i) + 1) % len(cycle)]
        return position

    def add_position_and_speed(self, position, speed):
        """
        """
        for i, v in enumerate(speed):
            if position[i] != v and v != 0:
                position[speed[i-1]] = position[speed[i]]
                position[speed[i]] = position[i]
                position[i] = speed[i]
        return position

    def subtract_positions(self, position_1, position_2):
        """
        """
        return [position_2[i] if position_1[i] != position_2[i] else 0 for i in range(len(position_2))]
        
    def multiply_c_and_speed(self, c, speed):
        """
        """
        speed_new = [random.random() for _ in speed]
        return [speed[i] if speed_new[i] < c else 0 for i in range(len(speed))]

    def add_speed_and_speed(self, speed_1, speed_2):
        """
        """
        return [speed_2[i] if speed_2[i] != 0 else speed_1[i] for i in range(len(speed_2))]

    def mutation(self):
        """
        """
        for indv in self.population.individuals:
            if np.random.rand() < 0.1:
                A = self.multiply_c_and_speed(self.c_1,
                                self.subtract_positions(self.population.population_best_individual.cycle,
                                                        indv.cycle))
                B = self.multiply_c_and_speed(self.c_2,
                                    self.subtract_positions(self.population.global_best_individual.cycle,
                                                            indv.cycle))
                V_r = self.add_speed_and_speed(A, B)
                indv.cycle = self.add_position_and_speed(indv.cycle, V_r)