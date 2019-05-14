import numpy as np
from utils import read_data_wrsn, calculate_distances, get_max_needed_energy, decode
import os
from wrsn import WRSN

if __name__ == "__main__":
    # Load data
    path = os.getcwd()
    data = read_data_wrsn(path + "/../datatsp/situation1.txt")
    data['distances'] = calculate_distances(data['cordination'])

    s = WRSN(data=data, maxIter=1000, size=100)
    s.solver()
    i = s.get_result()
    print("Finished !")
    print("Result: ", decode(data, i.gens))
    temp = get_max_needed_energy(data=data, gens=decode(data, i.gens))
    print("Max energy: ", temp) 
