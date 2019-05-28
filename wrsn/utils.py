import numpy as np
import sys, getopt

def read_file_c_huong(s)->list:
    x = np.loadtxt(s)
    return x[:, :2].tolist(), x[:, 2].tolist()

def read_data_wrsn(s, s2)->dict:
    with open(s, 'r') as file:
        # Number of nodes
        # num_nodes = int(get_number_of(file.readline())[0])
        # EM
        EM = get_number_of(file.readline())[0]
        # v
        v = get_number_of(file.readline())[0]
        # U
        U = get_number_of(file.readline())[0]
        # PM
        PM = get_number_of(file.readline())[0]
        # Emax
        Emax = get_number_of(file.readline())[0]
        # Emin
        Emin = get_number_of(file.readline())[0]
        # Cordination and p[i]
        # file.readline()
        # p_information = []
        # for _ in range(num_nodes + 1):
        #     p_information.append(get_number_of(file.readline()))
        # cordination = [c[0:-1] for c in p_information]
        # p = [c[-1] for c in p_information]
        # Hamilton cycle
        # hamilton_cycle = [int(c) for c in file.readline().split() if c.isdigit()]
        # length
        # length = get_number_of(file.readline())[0]
    ############
    cordination, p = read_file_c_huong(s2)
    cordination.insert(0, [0.0, 0.0])
    p.insert(0, 0.0)
    num_nodes = p.__len__() - 1
    #############
    return {
        'num_nodes': num_nodes,
        'EM': EM,
        'v': v,
        'U': U,
        'PM': PM,
        'Emax': Emax,
        'Emin': Emin,
        'cordination': cordination,
        'p': p,
        # 'hamilton_cycle': hamilton_cycle,
        # 'length': length,
    }

def get_number_of(s)->list:
    out = []
    for c in s.split():
        try :
            t = float(c)
        except ValueError as _:
            continue
        out.append(t)
    return out

def calculate_distances(cordination)->list:
    n = len(cordination)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = np.sqrt((cordination[i][0] - cordination[j][0])**2 + (cordination[i][1] - cordination[j][1])**2)
    return matrix

def calculate_T(data)->float:
    T = float('inf')
    for pi in data['p']:
        if pi != 0:
            temp = (data['Emax'] - data['Emin']) / (pi) + (data['Emax'] - data['Emin']) / (data['U'] - pi)
            if temp < T:
                T = temp
    return T

def get_distance(data, gens)->float:
    distance = 0
    for i in range(len(gens)-1):
        distance += data['distances'][gens[i], gens[i + 1]]
    return distance

def get_max_needed_energy(data, gens)->float:
    _max = 0
    service_station_index = [i for i, v in enumerate(gens) if v == 0]
    # Loop per each part cycle, if car is out of energy in the part cycle, return True
    for i in range(len(service_station_index)-1):
        temp = gens[service_station_index[i]: service_station_index[i+1] + 1]
        part_cycle_distance = 0.0
        # Calculate distance of the part cycle
        for j in range(len(temp) - 1):
            part_cycle_distance += data['distances'][temp[j], temp[j + 1]]
        
        # Check E' < E
        if ((part_cycle_distance / data['v']) * data['PM']) > _max: 
            _max = ((part_cycle_distance / data['v']) * data['PM'])
    return _max

def get_sum_to_i(data, T)->float:
    _sum = 0
    for i in range(data['num_nodes']):
        _sum += data['p'][i] * T / data['U']
    return _sum

def decode(d, gens)->list:
    distances = d['distances']
    cycle = [0] + gens.copy() + [0]
    # insert 0 to gens
    _max_len = d['EM'] * d['v'] / d['PM']
    _len = 0
    i = 0
    temp = 0
    while(True):
        temp = distances[cycle[i]][cycle[i+1]] + distances[cycle[i+1]][0]
        if _len + temp > _max_len:
            _len = 0
            cycle.insert(i+1, 0)
            if cycle[i] == 0:
                _err = "can not decode this gens at " + str(cycle[i+2])  
                raise Exception(_err)
        else :
            _len += distances[cycle[i]][cycle[i+1]]
        i += 1
        if i >= (cycle.__len__() - 2):
            break
    return cycle

def read_cli_argv(argv):
    blah = 'Run with :\n python main.py -n <num running> -i <maxIter> -s <population size> data_file.txt'
    try:
        opts, args = getopt.getopt(argv,"hn:i:s:")
    except getopt.GetoptError:
        print (blah)
        sys.exit(2)
    maxIter = 1000
    size = 100
    n = 1
    for opt, arg in opts:
        if opt == '-h':
            print (blah)
            sys.exit()
        elif opt == '-i':
            maxIter = arg
        elif opt == '-s':
            size = arg
        elif opt == '-n':
            n = arg
    return int(n), int(maxIter), int(size), args

def write_output(path, data_file, results, times, data):
    with open(path, 'w'):
        pass

    fitness_arr = []
    for r in results:
        temp = []
        for t in r:
            _fitness = t.fitness[t.skill_factor] if isinstance(t.fitness, list) else t.fitness
            temp.append(_fitness)
        fitness_arr.append(temp)
    fitness_arr = np.array(fitness_arr)
    with open(path, 'a') as out:
        out.writelines("Summarization: \n")
        out.writelines("Time average: "+ str(np.mean(times)) +"\n")
        for i, v in enumerate(data_file):
            out.writelines("------------------------------------------------------------\n")
            out.writelines("Task: " + v + "\n")
            out.writelines("Fitness: \n")
            out.writelines("\tmax: " + str(np.max(fitness_arr[:, i])) + "\n")
            out.writelines("\taverage: " + str(np.mean(fitness_arr[:, i])) + "\n")
            out.writelines("\tmin: " + str(np.min(fitness_arr[:, i])) + "\n")
    
    with open(path, 'a') as out:
        for i, v in enumerate(results):
            out.writelines("\n\n*********************** Time " + str(i) +" *******************************\n")
            # out.writelines("Time " + str(i) + "\n")
            for j, t in enumerate(data_file):
                out.writelines("--------------------------------------------------------------\n")
                out.writelines("Task: " + t + "\n")
                _fitness = v[j].fitness[v[j].skill_factor] if isinstance(v[j].fitness, list) else v[j].fitness
                out.writelines("Fitness: " + str(_fitness) + "\n")
                out.writelines("Cycle: " + str(v[j].decode(data[j], j)) + "\n")

if __name__ == "__main__":
    """Test functions"""
    import os
    d = read_data_wrsn(os.getcwd() + "/../datatsp/situation1.txt",
                       os.getcwd() + "/../datatsp/u20.txt")
    # m = calculate_distances([[1,1], [0,0]])
    # print(m)