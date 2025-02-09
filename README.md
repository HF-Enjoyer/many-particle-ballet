# Many Particle Disco 0.6.0

> NOW WITH POLYMERS!

Special thanks to my dearest friend Iaroslav Kutuzov (also known as Kusoslaw Intheforest).

Metropolis algorithm and pairwise potential by *Ilya Mikhailov*.
Temperature, RDF plot, average distance calculation, many bug fixes and valuable advice by *Iaroslav Kutuzov*.

Read the article about this code [here](https://blog.sklad.observer/posts/2025-01-30-many-particle-ballet/).

## How to use this code

This is a playful tackling of the problem that arose during the course on Statistical Thermodynamics a couple years back: there are two particles on the lattice that interact with some sort of potential. What are the properties of such system and how can we evaluate them?

Below you will find instructions for running Monte-Carlo simulations of N particles (or N-mer polymer) on 2D lattice using Metropolis-Hastings algorithm. You can observe configurations, radial distributions, energy and distance graphs and more yet to come...

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
4. Temperature (K). In the scale of this code 0.1 is low and 5K is extremely high. 
5. Potentials. Currently there are two to choose from: inverse (which is a gravitational-like potential) and Lennard-Jones.
    The latter is set in the way that the depth of the well $\varepsilon=-5.0$, the $\sigma$ parameter is set so as to have $r_{min}=2^{1/6}\sigma=1$. Potentials are selected in the input file by the names `inverse` and `LJ`.
6. Polymer parameter. `True` if you want to look at the polymer chain of length N, `False` if you want to look at the monoatomic system. (see below)
6. Coordinates. In this version just leave `random`.

### Outputs and useful data 

- In the output file (currently called **input_out.txt**) you can find every state along the path of the simulation stored in the following format:
```
INITIAL: {'part1': (3, 1), 'part2': (9, 2), 'part3': (8, 3), 'part4': (10, 3), 'part5': (2, 5), 'part6': (2, 8), 'part7': (7, 10), 'part8': (6, 8), 'part9': (8, 5), 'part10': (9, 10), 'part11': (1, 5), 'part12': (7, 9), 'part13': (4, 1), 'part14': (3, 5), 'part15': (3, 8), 'part16': (5, 5), 'part17': (8, 7), 'part18': (10, 4), 'part19': (2, 3), 'part20': (2, 6)} 
NEW: {'part1': (3, 1), 'part2': (9, 2), 'part3': (8, 3), 'part4': (10, 3), 'part5': (2, 5), 'part6': (2, 8), 'part7': (7, 10), 'part8': (6, 8), 'part9': (8, 5), 'part10': (9, 10), 'part11': (1, 5), 'part12': (7, 9), 'part13': (4, 1), 'part14': (3, 5), 'part15': (3, 8), 'part16': (5, 5), 'part17': (8, 7), 'part18': (10, 4), 'part19': (2, 3), 'part20': (10, 5)} 
ENERGY: -8.20486765785515 
JUMP? False 
NEW: {'part1': (3, 1), 'part2': (9, 2), 'part3': (10, 8), 'part4': (10, 3), 'part5': (2, 5), 'part6': (2, 8), 'part7': (7, 10), 'part8': (6, 8), 'part9': (8, 5), 'part10': (9, 10), 'part11': (1, 5), 'part12': (7, 9), 'part13': (4, 1), 'part14': (3, 5), 'part15': (3, 8), 'part16': (5, 5), 'part17': (8, 7), 'part18': (10, 4), 'part19': (2, 3), 'part20': (2, 6)} 
ENERGY: -8.376037727332575 
JUMP? True 
NEW: {'part1': (8, 9), 'part2': (9, 2), 'part3': (10, 8), 'part4': (10, 3), 'part5': (2, 5), 'part6': (2, 8), 'part7': (7, 10), 'part8': (6, 8), 'part9': (8, 5), 'part10': (9, 10), 'part11': (1, 5), 'part12': (7, 9), 'part13': (4, 1), 'part14': (3, 5), 'part15': (3, 8), 'part16': (5, 5), 'part17': (8, 7), 'part18': (10, 4), 'part19': (2, 3), 'part20': (2, 6)} 
ENERGY: -8.891048243803478 
JUMP? True 
SHOOK: {'part1': (3, 7), 'part2': (9, 5), 'part3': (9, 8), 'part4': (10, 3), 'part5': (1, 6), 'part6': (2, 8), 'part7': (6, 5), 'part8': (4, 8), 'part9': (5, 9), 'part10': (9, 10), 'part11': (1, 2), 'part12': (2, 7), 'part13': (6, 10), 'part14': (9, 3), 'part15': (8, 1), 'part16': (10, 4), 'part17': (9, 6), 'part18': (2, 9), 'part19': (7, 2), 'part20': (6, 6)} 
ENERGY: -9.244309838550498 
ACCEPT SHOOK? True 
```
- You can observe the changes in the positions of particles on the picture **before_after.png**. Follow the CLI prompt.
- The main script **mc.py** gathers data about the average distance between particles and stores it along with the energy of every step. They are then plotted on the graphs **part_distance.png** and **energy.png**. Follow the CLI prompt.
- If you want to look at the radial distribution function for your system, you can look it up on the graph **RDF.png**. The initial and the final state are both plotted there. Follow the CLI prompt.
- Starting ver 0.6.0 you can animate the evolution of the system (implemented with pygame). Follow the CLI prompt.

### Other scripts

- Script **polymer_test.py** is a copy of the **mc.py** with some additions regarding the before-after image plotting and no RDF calculation for polymer case.
- Script **meltdown.py** is a shortened version of the main code that has been used to "melt" the system by incremental increase in temperature parameter. There occurs something resembling phase transition at $T=2.1$ for the `inverse` potential (UPD: may be not true). `LJ` shows more promising results with melting.
- File **bunch_runner.py** is a script to run simulations with increases in temperature
- File **critical_analysis.py** is yet-to-be-tested-and-maybe-removed analyzer of the critical phenomena in the system

Feel free to play with any of the parameters!

TODO:
- take final configuration as a previous in the chain of simulations
- merge **mc.py** and **polymer_test.py**
- revise the algorithm for polymers at T = 0 and find why they are getting stuck
