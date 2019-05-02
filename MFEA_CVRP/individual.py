import numpy as np

class Individual(object):
    """docstring for Individual"""
    def __init__(self, num_city):
        super(Individual, self).__init__()
        
        self.skill_factor   = None
        self.distances      = []
        self.scalar_fitness = float('-inf')
        self.rank           = []
        self.len_of_routes  = num_city + 1  # routes begin at 0 and finish at 0
        self.routes         = [0 for i in range(self.len_of_routes)]
        self.routes[1:-1]   = np.random.permutation(range(1, num_city))

    def get_routes_distances(self, distances_matrix):
        self.rank = [0 for _ in distances_matrix]

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

    def get_routes_distances_4_specific_task(self, distances_matrix, task):
        remove = list(range(len(distances_matrix[task]), self.len_of_routes - 1))
        decode_routes = self.routes.copy()
        for r in remove:
            decode_routes.remove(r)
        # 
        for j in range(len(distances_matrix[task]) - 1):
            self.distances[task] += distances_matrix[task][decode_routes[j], decode_routes[j + 1]]
        