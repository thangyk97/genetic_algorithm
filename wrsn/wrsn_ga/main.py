import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import numpy as np
import os, time
import sys, getopt
from utils import read_data_wrsn, calculate_distances, get_max_needed_energy, decode, read_cli_argv, write_output
from wrsn import WRSN

def main(maxIter, size, data_file)->list:
    # Load data
    path = os.getcwd() + "/../data/"
    data = read_data_wrsn(path + "infor_cm.txt", path + data_file)
    data['distances'] = calculate_distances(data['cordination'])

    s = WRSN(data=data, maxIter=maxIter, size=size)
    s.solver()
    i = s.get_result()
    print("Finished !")
    print("Result: ", decode(data, i.gens))
    # temp = get_max_needed_energy(data=data, gens=decode(data, i.gens))
    return [i], [data]

if __name__ == "__main__":
    n, maxIter, size, data_file = read_cli_argv(sys.argv[1:])
    results = []
    _times = []
    for i in range(n):
        _start = time.time()
        best, data = main(maxIter, size, data_file[0])
        _end = time.time()
        results.append(best)
        _times.append(_end - _start)

    path = os.getcwd() + "/../results/"

    write_output(path + "wrsn_ga_" + data_file[0], data_file, results, _times, data)
    print("Success, check output in results folder.")
    

