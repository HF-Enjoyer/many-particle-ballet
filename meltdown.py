from functions import *
import numpy as np
import random
from matplotlib import pyplot as plt
from pathlib import Path
import sys

if __name__ == '__main__':
    # if len(sys.argv) != 2:
        # print('Usage: python mc.py <inp filename>')
    # print('Starting 2D Monte Carlo')
    filename = Path(__file__).with_name(sys.argv[1])

    iterations = get_info(filename)['iterations'] # number of iterations (test)
    shp = get_info(filename)['size'] # shape of the lattice
    Parts_num = get_info(filename)['N'] # number of particles
    Temp = get_info(filename)['temp'] # temperature
    potential = get_info(filename)['potential'] # type of potential
    particles_init = get_info(filename)['configuration'] # initial configuration of the particles
    polymer_true = get_info(filename)['polymer'] # condition whether the system is polymer or monoatomic 

    particle_distance = []
    part_now = particles_init
    i = 0
    energy_arr = []

    # something like monte carlo 

    while i <= iterations:
        i += 1
        part_now = MC_stepper(shp, potential, Temp, Parts_num, part_now, polymer_true, outfile)            
        particle_distance.append(avg_distance(part_now))
        energy_arr.append(pot_calc(part_now, potential)) 

    avg_distance_tot = Average_value(particle_distance[1500:], energy_arr[1500:], Temp)
    helmholtz = Helmholtz_free(energy_arr[1500:], Temp)
    print(avg_distance_tot)
    print(helmholtz)