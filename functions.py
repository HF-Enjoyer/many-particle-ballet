from collections import Counter
import numpy as np
import random
import pygame
from matplotlib import pyplot as plt
from math import exp as exp
import sys
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
    polymer_true = eval((info[5].split()[1])) # polymer or free particles
    if polymer_true == True:
        coords = generate_polymer_chain(Np, grid_size)
    else:
        if info[7] == 'random':
            coords = smart_randomizer(Np, grid_size)
        else:
            for i in info[6:-1]:
                coords[i.split()[0]] = (int(i.split()[1]), int(i.split()[2]))
    return {'N': Np, 
            'size': grid_size, 
            'iterations': iterations, 
            'temp': temp,
            'configuration': coords,
            'potential':potential,
            'polymer':polymer_true}
    
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

def generate_polymer_chain(length, lattice_size):
    start_x, start_y = lattice_size // 2, lattice_size // 2
    polymer = {0: (start_x, start_y)}  # Initialize with the first monomer
    occupied = {polymer[0]}  # Set of occupied positions for quick lookup
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Possible moves: right, left, up, down

    for idx in range(1, length):
        x, y = polymer[idx - 1]  # Get the last monomer's position
        np.random.shuffle(directions)  # Randomize move order for variety
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check lattice boundaries and avoid overlap
            if (0 <= nx < lattice_size and 0 <= ny < lattice_size) and (nx, ny) not in occupied:
                polymer[idx] = (nx, ny)  # Add the new monomer
                occupied.add((nx, ny))  # Mark the position as occupied
                break
        else:
            # If no valid moves, restart the chain
            return generate_polymer_chain(length, lattice_size)
    
    return polymer

def generate_new_config(polymer, lattice_size):
    idx = np.random.choice(list(polymer.keys()))
    x, y = polymer[idx]
    
    # Define possible moves
    possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    np.random.shuffle(possible_moves)
    
    for nx, ny in possible_moves:
        # Check lattice boundaries
        if not (0 <= nx < lattice_size and 0 <= ny < lattice_size):
            continue
        
        # Check overlap
        if any(pos == (nx, ny) for pos in polymer.values()):
            continue
        
        # Check connectivity
        if idx > 0:  # Ensure it remains connected to the previous monomer
            prev_x, prev_y = polymer[idx - 1]
            if abs(nx - prev_x) + abs(ny - prev_y) != 1:
                continue
        if idx < len(polymer) - 1:  # Ensure it remains connected to the next monomer
            next_x, next_y = polymer[idx + 1]
            if abs(nx - next_x) + abs(ny - next_y) != 1:
                continue
        
        # If all checks pass, apply the move
        new_polymer = polymer.copy()
        new_polymer[idx] = (nx, ny)
        return new_polymer  # Return updated configuration
    
    # If no valid move, return the original configuration
    return polymer
    

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

def Helmholtz_free(E_arr,T):
    if T != 0:
        weights = [exp(-(E-min(E_arr))/T) for E in E_arr]
    else:
        weights = [1]*len(E_arr)
    Z = sum(weights)
    return -T*np.log(Z)
    
def print_progress_bar(iteration, total, length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))  # Calculate percentage
    filled_length = int(length * iteration // total)  # Calculate filled part of the bar
    bar = '█' * filled_length + '-' * (length - filled_length)  # Create bar with '█' and '-'
    sys.stdout.write(f'\r|{bar}| {round(float(percent))}% Completed')
    sys.stdout.flush()

def MC_stepper(shp, potential, Temp, Parts_num, part_now, polymer_true, outfile):
    if polymer_true:
            part_rand = generate_new_config(part_now, shp)
            if jump_estimator(part_now, part_rand, Temp, potential) == True:
                outfile.write(f'NEW: {part_rand} \nENERGY: {pot_calc(part_rand, potential)} \nJUMP? {jump_estimator(part_now, part_rand, Temp, potential)} \n')
                # part_now = part_rand
                part_inter = generate_polymer_chain(Parts_num, shp) # intermediate check of random configuration being less in energy (to ensure faster convergence)
                if jump_estimator(part_rand, part_inter, Temp, potential) == True:
                    outfile.write(f'SHOOK: {part_inter} \nENERGY: {pot_calc(part_inter, potential)} \nACCEPT SHOOK? {jump_estimator(part_now, part_inter, Temp, potential)} \n')
                    part_now = part_inter
                else:
                    part_now = part_rand
            else:
                outfile.write(f'NEW: {part_rand} \nENERGY: {pot_calc(part_rand, potential)} \nJUMP? {jump_estimator(part_now, part_rand, Temp, potential)} \n')
    else:
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
    return part_now

def GUI_demonstrator(trajectory, shape, polymer_true):

    L = shape  # Size of the lattice
    particle_radius = 10  # Size of each particle in pixels
    cell_size = 50
    width, height = (L+1) * cell_size, (L+1)* cell_size  # Screen size

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particle Simulation")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (0,0,255)
    def draw_grid():
        for x in range(L+1):
            pygame.draw.line(screen, GRAY, (x * cell_size, 0), (x * cell_size, height))
        for y in range(L+1):
            pygame.draw.line(screen, GRAY, (0, y * cell_size), (width, y * cell_size))

    def draw_particles(particles):
        for (x, y) in particles.values():
            # Calculate the position of the vertex
            pos_x = x * cell_size
            pos_y = y * cell_size
            pygame.draw.circle(screen, RED, (pos_x, pos_y), particle_radius)
        pygame.display.flip()  # Update the display
    def draw_bonds(particles):
        connection_order = list(particles.keys())
        for i in range(len(connection_order) - 1):
            key1 = connection_order[i]
            key2 = connection_order[i + 1]
            # Get the positions of the two particles
            x1, y1 = particles[key1]
            x2, y2 = particles[key2]
            # Convert lattice coordinates to screen coordinates
            pos1 = (x1 * cell_size, y1 * cell_size)
            pos2 = (x2 * cell_size, y2 * cell_size)
            # Draw a line between the two particles
            pygame.draw.line(screen, BLUE, pos1, pos2, 2)
    def main():
        clock = pygame.time.Clock()
        running = True
        i = 0
        while i < len(trajectory):
            print('Iteration', i)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the loop when the user closes the window
            screen.fill((0, 0, 0))
            # Update particle positions (this is where your simulation logic would go)
            # For demonstration, let's just move one particle
            particles = trajectory[i]
            draw_grid()
            if polymer_true:
                draw_bonds(particles)        
            # Draw particles
            draw_particles(particles)

            # Control the frame rate (1 frame per second)
            clock.tick(8)  # Decreased frame rate to 1 FPS
            i += 1
        # Clean up and quit
        pygame.quit()
        sys.exit()

    main()
