from functions import *
import numpy as np
import random
from matplotlib import pyplot as plt
from pathlib import Path
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python mc.py <inp filename>')
    print('Starting 2D Monte Carlo')
    filename = Path(__file__).with_name(sys.argv[1])

    iterations = get_info(filename)['iterations'] # number of iterations (test)
    shp = get_info(filename)['size'] # shape of the lattice
    Parts_num = get_info(filename)['N'] # number of particles
    Temp = get_info(filename)['temp']
    potential = get_info(filename)['potential']
    particles_init = get_info(filename)['configuration']
    print('Starting energy', pot_calc(particles_init, potential), '\n')
    
    # coords_path = []
    particle_distance = []
    part_now = particles_init
    # coords_path.append(particles_init)
    i = 0
    energy_arr = []

    # something like monte carlo 

    print('iterations',iterations)

    while i <= iterations:
        i += 1
        part_rand = randomize_1particle(part_now, shp, Parts_num)
        if jump_estimator(part_now, part_rand, Temp, potential) == True:
            # part_now = part_rand
            part_inter = smart_randomizer(Parts_num, shp) # intermediate check of random configuration being less in energy (to ensure faster convergence)
            if jump_estimator(part_rand, part_inter, Temp, potential) == True:
                part_now = part_inter
            else:
                part_now = part_rand
  
        particle_distance.append(avg_distance(part_now))
        energy_arr.append(pot_calc(part_now, potential)) 
        print('step: ',i)



    print('Final Energy', pot_calc(part_now, potential), '\n')
    print('Montecarlo-ed!')
    print('Temp: ', Temp)
    print(len(particle_distance),len(energy_arr))
    avg_distance_tot = Average_value(particle_distance[100:], energy_arr[100:], Temp)

    print(avg_distance_tot)