from collections import Counter
import numpy as np
import random
from matplotlib import pyplot as plt
from math import exp as exp
# Functions

def get_info(filename: str):
    with open(filename, 'r') as f1:
        info = []
        for i in f1:
            info.append(i.rstrip('\n'))
    Np = int(info[0].split()[1]) # number of particles
    grid_size = int(info[1].split()[1]) # number of points in lattice
    iterations = int(info[2].split()[1]) # number of iterations
    temp = float(info[3].split()[1]) # dimensionless
    potential = (info[4].split()[1]) #type of potential LJ or inverse
    coords = {}
    if info[6] == 'random':
        coords = smart_randomizer(Np, grid_size)
    else:
        for i in info[6:-1]:
            coords[i.split()[0]] = (int(i.split()[1]), int(i.split()[2]))
    return {'N': Np, 
            'size': grid_size, 
            'iterations': iterations, 
            'temp': temp,
            'configuration': coords,
            'potential':potential}
    
def smart_randomizer(parts_num, Shape: int): # randomly generate configuration of parts_num particles
    coords = set()
    parts = {}
    j = 0
    while len(coords) != parts_num:
        coords.add((random.randint(1, Shape), random.randint(1, Shape)))
    for i in coords:
        j += 1
        parts.update({'part'+str(j): i})
    return parts

def randomize_1particle(parts_1: dict, Shape, N: int): # костыли... changes randomly the position of 1 particle
    num_part = random.randint(1, N)
    while True:
        new_coords = (random.randint(1, Shape), random.randint(1, Shape))
        if new_coords not in parts_1.values():
            break
    parts_2 = {}
    for i in parts_1:
        parts_2[i] = parts_1[i]
    parts_2[f'part{num_part}'] = new_coords
    return parts_2

def dist(part1, part2):  
    return np.sqrt((part1[0] - part2[0])**2 + (part1[1] - part2[1])**2)

def avg_distance(parts):
    a = [] # matrix of distances of a given configuration
    for i in parts:
        for j in parts:
            if i > j:
                a.append(dist(parts[i], parts[j]))
            else:
                continue
    sum_len = np.sum(np.array(a))
    avg_len = sum_len/len(a)
    return avg_len

def pot_calc(parts, potential):
    a = [] 
    sigma = 0.890899
    epsilon = 1
    for i in parts:
        c = [] # generate an empty list to append it to a after filling
        for j in parts:
            if i == j:
                c.append(0)
            else:
                distance = dist(parts[i], parts[j])
                if potential == 'inverse':
                    c.append(-1/distance)
                elif potential == 'LJ':
                    c.append(4*epsilon*(np.power((sigma/distance),12) - np.power((sigma/distance),6)))
        a.append(c)
    pot = np.sum(np.array(a))/2
    return pot

def jump_estimator(parts1, parts2, Temp, potential):
    # deltaE = pot_calc(parts2) - pot_calc(parts1)
    if Temp == 0:
        if (pot_calc(parts2, potential)-pot_calc(parts1, potential)) < 0:
            return True
        else: 
            return False
    else:
        Prob = np.exp((pot_calc(parts1, potential)-pot_calc(parts2, potential))/Temp)
        u = random.uniform(0,1)
        if u <= Prob:
            return True
        else:
            return False

def RDF(parts):
    a = []
    for i in parts:
        b = []
        for j in parts:
            if j!=i:
                distance = dist(parts[i], parts[j])
                # b.append(round(distance*2)/2)
                b.append(distance)
        a+=b
    distance_count = [[x,a.count(x)/len(parts)] for x in set(a)]
    return distance_count

def Average_value(A_arr, E_arr, T):
    E_arr = E_arr
    A_arr = A_arr
    if T != 0:
        weights = [exp(-(E-min(E_arr))/T) for E in E_arr]
    else:
        weights = [1]*len(E_arr)
    weights_sum = sum(weights)
    A_avg = 0
    for i in range(len(A_arr)):
        A_avg += A_arr[i]*weights[i]
    A_avg = A_avg/weights_sum
    return A_avg

        