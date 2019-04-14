# @author [thang nguyen dinh]
# @email [thangyk97@gmail.com]
# @create date 2019-03-26 11:01:48
# @modify date 2019-03-26 11:01:48
# @desc [description]

import numpy as np

class Individual(object):
    """
    Individual corresponds a success cycle
    """
    def __init__(self, num_sensor, num_come_back, data, sensor_info):
        """
        Parameters:
        ----------
        num_sensor: the sum number of sensor
        num_come_back: the number of times to car come back to service station
                        in each cycle.
        """
        super(Individual, self).__init__()
        self.distance = 0
        self.fitness = 0.0
        self.T = 0.0
        self.cycle_length = num_sensor + num_come_back
        self.cycle = [0 for _ in range(self.cycle_length)]
        self.to_i_list = [0.0 for _ in range(self.cycle_length)]
        self.data = data
        self.sensor_info = sensor_info

        self.random_init_cycle()

    def random_init_cycle(self):
        """
        Random init cycle path and when come back to service station
        """
        temp = np.random.permutation(range(0, self.cycle_length))
        self.cycle = temp.tolist()

    def cal_T(self):
        """
        """
        T = float('inf')
        for s in self.sensor_info[1:]:
            temp = (self.data['Emax'] - self.data['Emin']) / (s[2])
            if temp < T:
                T = temp
        self.T = T
        return self.T

    def cal_cycle_distance(self, distances):
        """
        Return the total distance of cycle
        Parameters:
        ----------
        distances: the square matrix with each element is
                    distance between two point
        """
        self.distance = 0
        full_cycle = [0] + self.cycle + [0]
        for i in range(len(full_cycle)-1):
            self.distance += distances[full_cycle[i], full_cycle[i + 1]]
        return self.distance

    def get_fitness(self):
        """
        """
        self.fitness = (self.T - sum(self.to_i_list) - self.distance / self.data['v']) / self.T

        return self.fitness
    
    def is_satify_constraints(self, distances):
        """
        Check all constraints , return True if satify them else return false
        """
        self.cal_T()
        self.cal_cycle_distance(distances)
        self.cal_to_i()
        self.get_fitness()
        temp = self.is_car_out_of_energy(distances, self.data['PM'],
                                                        self.data['v'], self.data['EM'])
        if self.fitness < 0 and temp:
            return True
        else:
            return False

    def cal_to_i(self):
        """
        Calculate to_i of each sensor at first cycle,
        use to calculate to_i
        """
        # while 
        for i in range(len(self.to_i_list)):
            self.to_i_list[i] = self.sensor_info[i][2]*self.T / self.data['U']


    def is_car_out_of_energy(self, distances, P_M, v, E_M):
        """
        Check car is out of energy in each part of cycle, from service station
        to next time come to one
        Return True if car is out of energy, False if not
        """
        cycle_full = [0] + self.cycle + [0]
        service_station_index = [i for i, v in enumerate(cycle_full) if v == 0]
        print(service_station_index)
        # Loop per each part cycle, if car is out of energy in the part cycle, return True
        for i in range(len(service_station_index)-1):
            temp = cycle_full[service_station_index[i], service_station_index[i+1]]
            part_cycle_distance = 0.0
            # Calculate distance of the part cycle
            for j in range(len(temp) - 1):
                part_cycle_distance += distances[temp[j], temp[j + 1]]
                print(part_cycle_distance)
            # Check E' < E
            # print(part_cycle_distance, v, P_M)
            if (part_cycle_distance / v) * P_M > E_M: 
                return False
        return True
        













