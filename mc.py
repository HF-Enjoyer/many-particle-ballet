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
    Temp = get_info(filename)['temp'] # temperature
    potential = get_info(filename)['potential'] # type of potential
    particles_init = get_info(filename)['configuration'] # initial configuration of the particles
    print('Starting energy', pot_calc(particles_init, potential), '\n')

    particle_distance = []
    part_now = particles_init
    i = 0
    energy_arr = []

    # something like monte carlo 

    with open(f'{sys.argv[1]}.out', 'w') as outfile:
        outfile.write(f'INITIAL: {particles_init} \n')
        while i <= iterations:
            i += 1
            part_rand = randomize_1particle(part_now, shp, Parts_num)
            if jump_estimator(part_now, part_rand, Temp, potential) == True:
                outfile.write(f'NEW: {part_rand} \nENERGY: {pot_calc(part_rand, potential)} \nJUMP? {jump_estimator(part_now, part_rand, Temp, potential)} \n')
                # part_now = part_rand
                part_inter = smart_randomizer(Parts_num, shp) # intermediate check of random configuration being less in energy (to ensure faster convergence)
                if jump_estimator(part_rand, part_inter, Temp, potential) == True:
                    outfile.write(f'SHOOK: {part_inter} \nENERGY: {pot_calc(part_inter, potential)} \nACCEPT SHOOK? {jump_estimator(part_now, part_inter, Temp, potential)} \n')
                    part_now = part_inter
                else:
                    part_now = part_rand
            else:
                outfile.write(f'NEW: {part_rand} \nENERGY: {pot_calc(part_rand, potential)} \nJUMP? {jump_estimator(part_now, part_rand, Temp, potential)} \n')
            particle_distance.append(avg_distance(part_now))
            energy_arr.append(pot_calc(part_now, potential)) 

            # coords_path.append(part_now)
    print('Final Energy', pot_calc(part_now, potential), '\n')
    print('Montecarlo-ed!')

    fig, ax = plt.subplots(1, 2, figsize=(13, 6), sharey=True, sharex=False)

    for i in particles_init.values():
        ax[0].plot(i[0], i[1], 'o', color='red')
        ax[0].set_ylim(0, shp+1)
        ax[0].set_xlim(0, shp+1)
        ax[0].set_title('Before MC')
        ax[0].set_xticks(np.arange(0, shp+1, 1))
        ax[0].set_yticks(np.arange(0, shp+1, 1))
    for i in part_now.values():
        ax[1].plot(i[0], i[1], 'o', color='red')
        ax[1].set_ylim(0, shp+1)
        ax[1].set_xlim(0, shp+1)
        ax[1].set_title('After MC')
        ax[1].set_xticks(np.arange(0, shp+1, 1))
        ax[1].set_yticks(np.arange(0, shp+1, 1))
    ax[0].grid()
    ax[1].grid()
    #plt.show()
    plt.savefig('before-after.png', dpi=300, bbox_inches="tight")
    plt.close()

    plt.plot(energy_arr, '-', color='black', linewidth=1.15)
    #print(len(energy_arr))
    plt.ylabel('Energy', fontsize=15)
    plt.xlabel('Monte-Carlo iterations', fontsize=15)
    plt.grid()
    #plt.show()
    plt.savefig('energy.png', dpi=300, bbox_inches="tight")
    plt.close()

    plt.plot(particle_distance, '-', color='black', linewidth=1.15)
    #print(len(energy_arr))
    plt.ylabel('Average distance', fontsize=15)
    plt.xlabel('Monte-Carlo iterations', fontsize=15)
    plt.grid()
    #plt.show()
    plt.savefig('part_distance.png', dpi=300, bbox_inches="tight")
    plt.close()


    # fig, ax = plt.subplots(1, 2, figsize=(13, 6), sharey=True, sharex=False)
    # c_1 = [] # generate an empty list to append it to after fillin

    # for i in particles_init:
    #     for j in particles_init:
    #         if j > i:
    #             c_1.append(dist(particles_init[i], particles_init[j]))
    #         else:
    #             continue
    # ax[0].hist(c_1)

    # c_2 = []
    # for i in part_now:
    #     for j in part_now:
    #         if j > i:
    #             c_2.append(dist(part_now[i], part_now[j]))
    #         else:
    #             continue
    # ax[1].hist(c_2)
    # plt.show()
    # plt.close()


    rdf_1 = []
    rdf_2 = []
    for i in RDF(particles_init):
        rdf_1.append([float(i[0]),float(i[1])])
    for i in RDF(part_now):
        rdf_2.append([float(i[0]),float(i[1])])
    rdf_1= sorted(rdf_1, key=lambda x: x[0])
    rdf_2= sorted(rdf_2, key=lambda x: x[0])
    x_1 = [x[0] for x in rdf_1]
    y_1 = [x[1] for x in rdf_1]
    x_2 = [x[0] for x in rdf_2]
    y_2 = [x[1] for x in rdf_2]
    plt.plot(x_1,y_1,color='b')
    plt.plot(x_2,y_2,color='r')
    plt.ylabel('RDF', fontsize=15)
    plt.xlabel('Distance', fontsize=15)
    #plt.show()
    plt.legend(["Intitial", "Final"], loc="upper right")
    plt.savefig('RDF.png', dpi=300, bbox_inches="tight")
    plt.close()
