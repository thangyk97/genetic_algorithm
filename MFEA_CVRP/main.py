import numpy as np
from mfea import MFEA


def cal_distance_matrix_from_coordinate(coord):
    n = coord.shape[0]
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i][j] = np.sqrt((coord[i][1] - coord[j][1])**2 + (coord[i][2] - coord[j][2])**2)
    return distances

def load_data(file_names, path):
    # Load data
    distances = []
    for f in file_names:
        coord = np.loadtxt(path +f)
        distances.append(
            cal_distance_matrix_from_coordinate(coord))
    return distances

def main():
    file_names = ['ch130.txt', 'a280.txt', 'berlin52.txt']
    path = 'D:/thangnd/git/genetic_algorithm/datatsp/'

    distances = load_data(file_names, path)
    s = MFEA(distances, 100)
    r = s.solve(100)
    
    for i, f in enumerate(file_names):
        print("Min distance for " + f + ": ", r[i])

if __name__ == '__main__':
    main()