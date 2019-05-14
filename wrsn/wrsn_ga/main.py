import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import numpy as np
import os
import sys, getopt
from utils import read_data_wrsn, calculate_distances, get_max_needed_energy, decode, read_cli_argv
from wrsn_ga.wrsn import WRSN

if __name__ == "__main__":
    maxIter, size, data_file = read_cli_argv(sys.argv[1:])
    # Load data
    path = os.getcwd() + "/../data/"
    data = read_data_wrsn(path + "infor_cm.txt", path + data_file[0])
    data['distances'] = calculate_distances(data['cordination'])

    s = WRSN(data=data, maxIter=maxIter, size=size)
    s.solver()
    i = s.get_result()
    print("Finished !")
    print("Result: ", decode(data, i.gens))
    temp = get_max_needed_energy(data=data, gens=decode(data, i.gens))
    print("Max energy: ", temp) 
    
    

