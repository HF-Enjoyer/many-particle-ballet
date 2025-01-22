import numpy as np
from functions import *

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
    polymer_true = get_info(filename)['polymer'] # polymer or single-particle system
    print('Starting energy', pot_calc(particles_init, potential), '\n')

    particle_distance = []
    part_now = particles_init
    i = 0
    energy_arr = []

    with open(f'{sys.argv[1].split(".")[0]}_out.txt', 'w') as outfile:
        outfile.write(f'INITIAL: {particles_init} \n')
        while i <= iterations:
            i += 1
            part_now = MC_stepper(shp, potential, Temp, Parts_num, part_now, polymer_true, outfile)            
            particle_distance.append(avg_distance(part_now))
            energy_arr.append(pot_calc(part_now, potential)) 
            print_progress_bar(i, iterations)

    print('\n')
    print('Final Energy', pot_calc(part_now, potential), '\n')
    print('Montecarlo-ed!')

    print('Plotting energy...')
    plt.plot(energy_arr, '-', color='black', linewidth=1.15)
    #print(len(energy_arr))
    plt.ylabel('Energy', fontsize=15)
    plt.xlabel('Monte-Carlo iterations', fontsize=15)
    plt.grid()
    #plt.show()
    plt.savefig('energy.png', dpi=300, bbox_inches="tight")
    plt.close()

    print('Plotting average distances...')
    plt.plot(particle_distance, '-', color='black', linewidth=1.15)
    #print(len(energy_arr))
    plt.ylabel('Average distance', fontsize=15)
    plt.xlabel('Monte-Carlo iterations', fontsize=15)
    plt.grid()
    #plt.show()
    plt.savefig('part_distance.png', dpi=300, bbox_inches="tight")
    plt.close()

    def plot_polymer_side_by_side(polymer1, polymer2,shp, title1="Initial Configuration", title2="Final Configuration"):
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        # First plot
        x1, y1 = zip(*polymer1.values())
        axes[0].plot(x1, y1, '-o', markersize=8, color="blue", label="Polymer Chain")
        axes[0].scatter(x1, y1, s=100, c="red", zorder=3, label="Monomers")
        axes[0].set_title(title1)
        axes[0].set_xlim(0,shp)
        axes[0].set_ylim(0,shp)
        axes[0].grid(True)
        axes[0].legend()
        axes[0].set_xticks(np.arange(0, shp+1, 1))
        axes[0].set_yticks(np.arange(0, shp+1, 1))

        # Second plot
        x2, y2 = zip(*polymer2.values())
        axes[1].plot(x2, y2, '-o', markersize=8, color="blue", label="Polymer Chain")
        axes[1].scatter(x2, y2, s=100, c="red", zorder=3, label="Monomers")
        axes[1].set_title(title2)
        axes[1].set_xlim(0,shp)
        axes[1].set_ylim(0,shp)
        axes[1].grid(True)
        axes[1].legend()
        axes[1].set_xticks(np.arange(0, shp+1, 1))
        axes[1].set_yticks(np.arange(0, shp+1, 1))
        plt.tight_layout()
        plt.savefig('before_after.png', dpi=300, bbox_inches="tight")
        plt.close()
    print('Plotting initial and final configurations...')
    plot_polymer_side_by_side(particles_init,part_now,shp)