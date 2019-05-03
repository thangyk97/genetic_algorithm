import numpy as np

class Individual(object):
    """docstring for Individual"""
    def __init__(self, num_city):
        super(Individual, self).__init__()
        
        self.skill_factor = None
        self.distances = []
        self.scalar_fitness = float('-inf')
        self.rank = []
        self.len_of_routes = num_city + 1  # routes begin at 0 and finish at 0
        # self.routes         = [0 for i in range(self.len_of_routes)]
        self.routes = np.random.permutation(range(1, num_city)).tolist()
        self.output = []

    def cal_routes_distances(self, distances_matrix, q, Q):
        self.rank = [0 for _ in distances_matrix]

        self.distances = [0 for i in distances_matrix]
        for i, _ in enumerate( distances_matrix ):
            self.cal_routes_distances_4_specific_task(distances_matrix[i], i, q[i], Q[i])
        return self.distances

    def cal_routes_distances_4_specific_task(self, distances_task, task, q, Q):
        # Decode
        remove = list(range(len(distances_task), self.len_of_routes - 1))
        decode_routes = self.routes.copy()
        for r in remove:
            decode_routes.remove(r)
        # 
        decode_routes = self.split_base_decode(decode_routes, distances_task, q, Q)
        self.output = decode_routes
        for j in range(len(distances_task) - 1):
            self.distances[task] += distances_task[decode_routes[j], decode_routes[j + 1]]
    
    def split_base_decode(self, routes, c, q, Q):
        N = len(routes)
        F = [0] + [float('inf')] * (N)
        P = [0] * (N + 1)

        for i in range(1, N + 1):
            demand = 0
            cost = 0
            j = i
            # print("====================================")
            while j <= N and demand < Q:
                demand += q[routes[j-1]]
                if i == j:
                    cost = c[0, routes[j-1]] + c[routes[j-1], 0]
                else:
                    cost += c[routes[j-2], routes[j-1]] + c[routes[j-1], 0] - c[routes[j-2], 0]

                if demand < Q:
                    if F[i-1] + cost < F[j]:
                        F[j] = F[i-1] + cost
                        P[j] = i - 1
                j += 1
        # split
        it = N
        routes.insert(it, 0)
        while it > 0:
            routes.insert(P[it], 0)
            it = P[it]

        return routes