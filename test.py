import numpy as np 

with open("/home/thangnd/git/python/genetic_algorithm/datatsp/E-n101-k8.txt", 'r') as f:
    # Load num of vertex
    for i in range(4): 
        _line = f.readline()
    N = int(_line[_line.index(':')+2:-1])
    # Load capacity of vehicle
    for i in range(2):
        _line = f.readline()
    Q = int(_line[_line.index(':')+2:-1])
    # Load cordination of vertex
    f.readline()
    print(N)
    cordination = [f.readline() for _ in range(N)]
    cordination = np.loadtxt(cordination)[:, 1:]
    # Load demand of customer
    f.readline()
    demand = [f.readline() for _ in range (N)]
    demand = np.loadtxt(demand)[:, 1]

    # print(cordination[0, 0])
    print(cordination)