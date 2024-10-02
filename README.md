# Many particle disco

Special thanks to my dearest friend Iaroslav Kutuzov (as known as Kusoslaw Intheforest).

Metropolis algorithm and pairwise potential by *Ilya Mikhailov*.
Temperature, RDF plot, average distance calculation, many bug fixes and valuable advice by *Iaroslav Kutuzov*.

## How to use this code

### How to run

1. Edit the **input.txt** file according to the sample
2. Cmd:
```shell
py mc.py input.txt
```
3. Wait for it...

### Editable parameters in input.txt:

1. Number of particles N
2. Lattice size (basically all the coordinates) - don't set too much. 10-50 is OK.
3. Iterations. After this number of iterations the code stops. I recommend using 1000-20000 depending on N.
4. Temperature(K). In the scale of this code 0.1 is low and 5K is extremely high. 
5. Potentials. Currently there are two to choose from: inverse (which is a gravitational-like potential) and Lennard-Jones (set in the way that he depth of the well $\varepsilon=-5.0$, the $\sigma$ parameter is set so as to have $r_{min}=2^{1/6}\sigma=1$). Can be called by the names `inverse` and `LJ`.
6. Coordinates. In this version just leave `random`.

### Outputs and useful data 

- In the output file (currently called **input.txt.out**) you can find every state along the path of the simulation stored in the following format:
```
SHOOK: {'part1': (3, 1), 'part2': (9, 2), 'part3': (9, 5), 'part4': (9, 8), 'part5': (10, 3), 'part6': (10, 9), 'part7': (1, 6), 'part8': (2, 8), 'part9': (7, 7), 'part10': (4, 2), 'part11': (4, 8), 'part12': (3, 6), 'part13': (8, 5), 'part14': (9, 4), 'part15': (8, 8), 'part16': (1, 5), 'part17': (6, 1), 'part18': (2, 10), 'part19': (6, 10), 'part20': (4, 4), 'part21': (8, 4), 'part22': (9, 3), 'part23': (10, 1), 'part24': (6, 3), 'part25': (6, 9)} 
ENERGY: -12.772163824882293 
ACCEPT SHOOK? True 
NEW: {'part1': (3, 1), 'part2': (9, 2), 'part3': (9, 5), 'part4': (9, 8), 'part5': (10, 3), 'part6': (10, 9), 'part7': (1, 6), 'part8': (2, 8), 'part9': (7, 7), 'part10': (4, 2), 'part11': (4, 8), 'part12': (3, 6), 'part13': (8, 5), 'part14': (9, 4), 'part15': (8, 8), 'part16': (1, 5), 'part17': (6, 1), 'part18': (2, 10), 'part19': (6, 10), 'part20': (4, 4), 'part21': (8, 4), 'part22': (9, 9), 'part23': (10, 1), 'part24': (6, 3), 'part25': (6, 9)} 
ENERGY: -11.7148260020514 
JUMP? False 
```
- You can observe the changes in the positions of particles on the picture **before-after.png**. 
- The program **mc.py** gathers data about the average distance between particles and stores it along with the energy of every step. They are then plotted on the graphs **part_distance.png** and **energy.png**.
- Finally, if you want to look at the radial distribution function for your system, you can look it up on the graph **RDF.png**. The intial and the final state are both plotted there. 
- File **meltdown.py** is a shortened version of the main code that has been used to "melt" the system by incremental increase in temperature parameter. There occurs something resembling phase transition at $T=2.1$ for the `inverse` potential. `LJ` is yet to be studied.

Feel free to play with any of the parameters!
