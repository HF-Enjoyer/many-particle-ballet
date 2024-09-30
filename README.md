# Many particle disco
Special thanks to my dearest friend Iaroslav Kutuzov (as known as Kusoslaw Intheforest).

Metropolis algorithm and pairwise potential by *Ilya Mikhailov*.
Temperature, RDF plot, average distance calculation, many bug fixes and valuable advise by *Iaroslav Kutuzov*.

## How to use
### Editable parameters in input.txt:
1. Number of particles N
2. Lattice size (basically all the coordinates) - don't set too much. 10-50 is OK.
3. Iterations. After this number of iterations the code stops. I recommend using 1000-20000 depending on N.
4. Temperature(K). In the scale of this code 0.1 is low and 5K is extremely high.
5. Coordinates. In this version just leave random.

### Instructions
1. Edit the **input.txt** file according to the sample
2. Cmd:
```shell
py mc.py input.txt
```
3. Wait for a while...

