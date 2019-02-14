import numpy as np

class Individual(object):
    """docstring for Individual"""
    def __init__(self, num_city):
        super(Individual, self).__init__()
        # property
        self.distance = 0
        self.fitness = 0.0
        # routes begin at 0 and finish at 0
        self.len_of_routes = num_city + 1 
        self.routes = [0 for i in range(self.len_of_routes)]
        temp = np.random.permutation(range(1, num_city))
        self.routes[1:-1] = temp

    def get_routes_distance(self, distances):
        self.distance = 0
        for i in range(self.len_of_routes - 1):
            self.distance += distances[self.routes[i], self.routes[i + 1]]
        return self.distance

    def get_fitness(self, distances):
        """
        Paramester
        @distances: the distances matrix of cities
        """
        _ = self.get_routes_distance(distances)
        if self.distance != 0:
            self.fitness = 1 / self.distance
        return self.fitness

    def _copy(self):
        pass
        