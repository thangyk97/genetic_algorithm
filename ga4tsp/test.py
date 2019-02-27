import numpy as np
import itertools


distances = np.array(     [[ 0,  4, 13, 15, 24,  4, 31, 18,  6, 21],
                           [ 4,  0,  8, 33,  9, 61,  7, 61,  7, 31],
                           [13,  8,  0, 22,  6, 33,  2, 33, 19, 41],
                           [15, 33, 22,  0,  3,  5, 62,  9, 41,  5],
                           [24,  9,  6,  3,  0, 18, 12,  4, 17,  9],
                           [ 4, 61, 33,  5, 18,  0,  1, 35,  9, 17],
                           [31,  7,  2, 62, 12,  1,  0, 19, 91,  8],
                           [18, 61, 33,  9,  4, 35, 19,  0, 77,  7],
                           [ 6,  7, 19, 41, 17,  9, 91, 77,  0, 11],
                           [21, 31, 41,  5,  9, 17,  8,  7, 11,  0]])

def cal_distance(routes):
    distance = 0
    for i in range(len(routes[:-1])):
        distance += distances[routes[i], routes[i+1]]
    return distance


a = list(range(distances.shape[0]))
list_routes = list(itertools.permutations(a[1:]))


min_distance = float('inf')
min_routes = []
for r in list_routes:
    r = (0,) + r + (0,)
    d = cal_distance(r)
    if d < min_distance:
        min_distance = d
        min_routes = r

print("min distance : ", min_distance)
print('route: ', min_routes)
