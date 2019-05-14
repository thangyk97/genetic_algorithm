import numpy as np
from utils import read_data_wrsn, calculate_distances
import os
from mfea import MFEA

if __name__ == "__main__":
    # Load data
    path = os.getcwd()
    data_1 = read_data_wrsn(path + "/datatsp/infor_cm.txt", path + "/datatsp/u20.txt")
    data_2 = read_data_wrsn(path + "/datatsp/infor_cm.txt", path + "/datatsp/u30.txt")
    data_3 = read_data_wrsn(path + "/datatsp/infor_cm.txt", path + "/datatsp/u40.txt")
    data_1['distances'] = calculate_distances(data_1['cordination'])
    data_2['distances'] = calculate_distances(data_2['cordination'])
    data_3['distances'] = calculate_distances(data_3['cordination'])
    data = [data_1, data_2, data_3]

    # Genetic
    max_num_nodes = 0
    for d in data:
        if d['num_nodes'] > max_num_nodes:
            max_num_nodes = d['num_nodes']

    s = MFEA(data=data, maxIter=200, size=100, gens_len=max_num_nodes)
    s.solver()
    s.get_result()
    print("asdf")
