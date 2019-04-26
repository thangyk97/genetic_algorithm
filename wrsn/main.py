# @author [thang nguyen dinh]
# @email [thangyk97@gmail.com]
# @create date 2019-03-26 11:02:21
# @modify date 2019-03-26 11:02:21
# @desc [description]

from wrsn import WRSN
import numpy as np

def cal_distance_matrix_from_coordinate(coord):
    """
    Calculate distance between 2 cities from their coordinate
    """
    n = coord.shape[0]
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i][j] = np.sqrt((coord[i][0] - coord[j][0])**2 + (coord[i][1] - coord[j][1])**2)
    return distances

def main():
    """
    Main , load data and call Class WRSN solve problem
    """
    _path = '/home/thangnd/git/python/genetic_algorithm/datatsp/'

    with open(_path+'my_situation2.txt', 'r') as _file:
        data = {}
        data['num_node'] = int(_file.readline())
        data['EM'] = int(_file.readline())
        data['v'] = int(_file.readline())
        data['U'] = int(_file.readline())
        data['PM'] = int(_file.readline())
        data['Emax'] = int(_file.readline())
        data['Emin'] = int(_file.readline())

        sensor_info = np.array([[float(x) for x in line.split()] for line in _file])
    print(data)
    s = WRSN(distances=cal_distance_matrix_from_coordinate(sensor_info[:, :2]),
            size_of_population=100,
            c_1 = 0.5,
            c_2 = 0.5,
            data = data,
            sensor_info = sensor_info,)
    s.solve()

if __name__ == "__main__":
    main()