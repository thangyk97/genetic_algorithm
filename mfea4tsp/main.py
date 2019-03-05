import numpy as np
from mfea4tsp import mfea4tsp


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
    file_names = ['ch130.txt', 'a280.txt']
    path = '/home/thangnd/git/python_workspace/geneticalgorithms/datatsp/'

    distances = load_data(file_names, path)
    s = mfea4tsp(distances, 100)
    r = s.solve(10)
    
    for i, f in enumerate(file_names):
        print("Min distance for " + f + ": ", r[i])

if __name__ == '__main__':
    main()