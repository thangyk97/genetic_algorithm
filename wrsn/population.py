# @author [thang nguyen dinh]
# @email [thangyk97@gmail.com]
# @create date 2019-03-26 11:02:37
# @modify date 2019-03-26 11:02:37
# @desc [description]

from individual import Individual
import sys

class Population(object):
    """
    Properties:
    ----------
    individuals (list): list of Individual objects
    num_sensor (int): the sum number of sensor and 
                times to car come to station in each cycle
    num_come_back (int): the number of times to car come back to service station
                        in each cycle
    global_best_individual (Individual): 
    """
    def __init__(self, num_sensor, num_come_back, size_of_population, data, sensor_info, distances):
        """
        Initial randomly individuals, they satify all constraints
        Parameters:
        ----------
        num_sensor: the sum the number of sensor
        num_come_back: the number of times to car come back to service station
                        in each cycle.
        size_of_population: the number of individuals in population
        """
        super(Population, self).__init__()
        self.num_sensor = num_sensor
        self.num_come_back = num_come_back
        self.data = data
        self.sensor_info = sensor_info
        self.size_of_population = size_of_population

        # Initial population of cycle
        self.individuals = []
        it = 0
        while it < size_of_population:
            new_individuals = Individual(num_sensor=num_sensor, 
                                        num_come_back=num_come_back,
                                        data=self.data,
                                        sensor_info=self.sensor_info)
            if new_individuals.is_satify_constraints(distances):
                self.individuals.append(new_individuals)
                it += 1
                print(it)

        highest_index = self.get_highest_fitness_index()
        self.population_best_individual = self.individuals[highest_index]
        self.global_best_individual = self.individuals[highest_index]

        print("Initial population success !")

    def calculate_fitness(self, distances):
        """
        Calculate fitness of each individual
        Parameters:
        ----------
        distances: the distance matrix
        """
        for indiv in self.individuals:
            _ = indiv.get_fitness()

    def get_least_fitness_index(self):
        """
        Return index of one least fitness individual
        Returns:
        -------
        least_fitness_index: integer
        """
        min_fitness = float('inf')
        least_fitness_index = 0
        for i, indiv in enumerate(self.individuals):
            if indiv.fitness < min_fitness:
                min_fitness = indiv.fitness
                least_fitness_index = i
        return least_fitness_index

    def get_highest_fitness_index(self):
        """
        Return index of one high fitness individual
        Returns:
        -------
        highest_fitness_index: integer
        """
        min_fitness = float('-inf')
        highest_fitness_index = 0
        for i, indiv in enumerate(self.individuals):
            if indiv.fitness > min_fitness:
                min_fitness = indiv.fitness
                highest_fitness_index = i
        return highest_fitness_index

    def rank_individuals(self):
        """
        Order descently the individuals of population by their fitness
        """
        self.individuals = sorted(self.individuals, key=lambda x: x.fitness, reverse=True)

    def get_tot_fitness(self):
        """
        Return total fitness of the population
        Returns:
        -------
        tot_fitness: float
        """
        tot_fitness = 0.0
        for i in self.individuals:
            tot_fitness += i.fitness
        return tot_fitness

    def get_avg_fitness(self):
        """
        Return average of fitness in population
        """
        _sum = 0
        for indv in self.individuals:
            _sum += indv.fitness
        return _sum / self.size_of_population
