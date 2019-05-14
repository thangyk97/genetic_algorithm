# import os
# import sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)
import numpy as np
from utils import calculate_T, get_distance, get_max_needed_energy, get_sum_to_i, decode, calculate_distances

class Individual:
    def __init__(self, gens_len):
        self.gens_len = gens_len
        self.gens = []
        self.fitness = 0
        self._random_initial()

    def _random_initial(self):
        temp = np.random.permutation(range(1, self.gens_len + 1))
        self.gens = temp.tolist()

    def cal_fitness(self, data):
        self.fitness = self.get_fitness(data)

    def get_fitness(self, d)->float:
        decode_gens = decode(d, self.gens)
        T = calculate_T(d)
        distance = get_distance(d, decode_gens)
        sum_to_i = get_sum_to_i(d, T)
        t_vac = T - sum_to_i - distance / d['v']
        return t_vac / T

    def is_satified(self, d)->bool:
        decode_gens = decode(d, self.gens)
        T = calculate_T(d)
        distance = get_distance(d, decode_gens)
        max_needed_energey = get_max_needed_energy(d, decode_gens)
        sum_to_i = get_sum_to_i(d, T)
        t_tsp = distance / d['v']
        # t_vac > 0
        if (T - sum_to_i - t_tsp < 0):
            return False
        # check out of energy
        if (max_needed_energey > d['EM']):
            return False
        return True

    def get_gens(self)->list:
        return self.gens


if __name__ == "__main__":
    d = {}
    d['v'] = 1
    d['EM'] = 13
    d['PM'] = 1
    d['cordination'] = [[0, 0], [1, 2], [1, 6], [0, 2], [3, 6], [3, -1], [3, 1]]
    d['distances'] = calculate_distances(d['cordination'])


    gens = [3, 1, 2, 4, 6, 5]
    x = Individual(7)
    decoded = decode(d, gens)
    print(decoded)
