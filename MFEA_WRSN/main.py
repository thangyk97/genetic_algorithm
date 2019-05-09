import numpy as np
from utils import read_data_wrsn, calculate_distances

if __name__ == "__main__":
    data_1 = read_data_wrsn("")
    data_2 = read_data_wrsn("")
    distances_1 = calculate_distances(data_1['cordinations'])
    distances_2 = calculate_distances(data_2['cordinations'])