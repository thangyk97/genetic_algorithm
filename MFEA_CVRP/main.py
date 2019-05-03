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
    distances = []
    q = []
    capacity = []
    for _file in file_names:
        with open(path + _file, 'r') as f:
            # Load num of vertex
            for i in range(4): 
                    _line = f.readline()
            N = int(_line[_line.index(':')+2:-1])
            # Load capacity of vehicle
            for i in range(2):
                    _line = f.readline()
            Q = int(_line[_line.index(':')+2:-1])
            capacity.append(Q)
            # Load cordination of vertex
            f.readline()
            print(N)
            cordination = [f.readline() for _ in range(N)]
            cordination = np.loadtxt(cordination)
            distances.append(cal_distance_matrix_from_coordinate(cordination))
            # Load demand of customer
            f.readline()
            demand = [f.readline() for _ in range (N)]
            demand = np.loadtxt(demand)[:, 1]
            q.append(demand)
    return distances, capacity, q

def main():
    file_names = ['E-n101-k8.txt', 'E-n76-k8.txt']
    path = '/home/thangnd/git/python/genetic_algorithm/datatsp/'

    distances, capacity, q = load_data(file_names, path)
    s = MFEA(distances, 100, q, capacity)
    r = s.solve(10)
    
    for i, f in enumerate(file_names):
        print("Min distance for " + f + ": ", r[i].distances[i])
        print("Route: ", r[i].output)

if __name__ == '__main__':
    main()