import numpy as np

class Individual(object):
    """docstring for Individual"""
    def __init__(self, num_city):
        super(Individual, self).__init__()
        
        self.skill_factor   = None
        self.distances      = []
        self.fitness        = []
        self.rank           = []
        self.len_of_routes  = num_city + 1  # routes begin at 0 and finish at 0
        self.routes         = [0 for i in range(self.len_of_routes)]
        self.routes[1:-1]   = np.random.permutation(range(1, num_city))

    def get_routes_distances(self, distances_matrix):
        self.distances = [0 for i in distances_matrix]
        for i, v in enumerate( distances_matrix ):
            # Decode routes for each task
            remove = list(range(len(v), self.len_of_routes - 1))
            decode_routes = self.routes.copy()
            for r in remove:
                decode_routes.remove(r)
            # 
            for j in range(len(v) - 1):
                self.distances[i] += v[decode_routes[j], decode_routes[j + 1]]
        return self.distances

    def get_fitness(self, distances_matrix):
        """
        Paramester
        @distances: the distances matrix of cities
        """
        self.rank = [0 for _ in distances_matrix]
        self.fitness = []
        _ = self.get_routes_distances(distances_matrix)
        for d in self.distances:
            self.fitness.append( 1 / d )

        return self.fitness
        