import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import numpy as np
from utils import read_data_wrsn, calculate_distances, read_cli_argv, write_output
import os, sys, time
from mfea import MFEA

def main(maxIter, size, data_file):
    path = os.getcwd() + "/../data/"
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

    s = MFEA(data=data, maxIter=maxIter, size=size, gens_len=max_num_nodes)
    s.solver()
    results = s.get_result()
    return results, data

if __name__ == "__main__":
    n, maxIter, size, data_file = read_cli_argv(sys.argv[1:])
    results = []
    _times = []
    for i in range(n):
        _start = time.time()
        best, data = main(maxIter, size, data_file)
        _end = time.time()
        results.append(best)
        _times.append(_end - _start)

    path = os.getcwd() + "/../results/"

    write_output(path + "mfea_wrsn.txt", data_file, results, _times, data)
    print("Success, check output in results folder.")