import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import numpy as np
from utils import read_data_wrsn, calculate_distances, read_cli_argv
import os, sys
from mfea import MFEA

if __name__ == "__main__":
    path = os.getcwd() + "/../data/"
    maxIter, size, data_file = read_cli_argv(sys.argv[1:])
    # Load data
    data = []
    for _file in data_file:
        temp = read_data_wrsn(path + "infor_cm.txt", path + _file)
        temp['distances'] = calculate_distances(temp['cordination'])
        data.append(temp)

    # Genetic
    max_num_nodes = 0
    for d in data:
        if d['num_nodes'] > max_num_nodes:
            max_num_nodes = d['num_nodes']

    s = MFEA(data=data, maxIter=200, size=100, gens_len=max_num_nodes)
    s.solver()
    s.get_result()
    print("Finished !")
