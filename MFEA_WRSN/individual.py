import numpy as np
from utils import calculate_T, get_distance, get_max_needed_energy, get_sum_to_i, decode

class Individual:
    def __init__(self, gens_len):
        self.gens_len = gens_len
        self.gens = []
        self.ranks = []
        self.fitness = []
        self.scalar_fitness = 0.0
        self.skill_factor = None
        self._random_initial()

    def _random_initial(self):
        temp = np.random.permutation(range(1, self.gens_len + 1))
        self.gens = temp.tolist()

    def decode(self, d, i)->list:
        remove = list(range(d['num_nodes'] + 2, self.gens_len + 1))
        decode_routes = self.gens.copy()
        for r in remove:
            decode_routes.remove(r)
        #
        # decode_routes[decode_routes.index(d['num_nodes'] + 1)] = 0
        return decode(d, decode_routes)

    def cal_scalar_fitness(self):
        temp = [i for i, x in enumerate(self.ranks) if x == np.min(self.ranks)]
        self.skill_factor = temp[np.random.randint(0, temp.__len__())]
        self.scalar_fitness = 1 / (np.min(self.ranks) + 1)

    def cal_fitness(self, data):
        self.fitness = []
        for i, d in enumerate(data):
            self.fitness.append(self.get_fitness(d, i))

    def get_fitness(self, d, i)->float:
        decode_gens = self.decode(d, i)
        T = calculate_T(d)
        distance = get_distance(d, decode_gens)
        sum_to_i = get_sum_to_i(d, T)
        t_vac = T - sum_to_i - distance / d['v']
        return t_vac / T

    def is_satified(self, data)->bool:
        for i, d in enumerate(data):
            decode_gens = self.decode(d, i)
            T = calculate_T(d)
            distance = get_distance(d, decode_gens)
            max_needed_energey = get_max_needed_energy(d, decode_gens)
            sum_to_i = get_sum_to_i(d, T)
            # t_vac > 0
            if (T - sum_to_i - distance / d['v'] < 0):
                return False
            # check out of energy
            if (max_needed_energey > d['EM']):
                return False
        return True

    def get_gens(self)->list:
        return self.gens