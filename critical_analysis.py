from scipy.misc import derivative
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

df = pd.read_csv('simulation_results_inverse.csv')

temp = np.array(df['T'])
dist  = np.array(df['d'])

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

p0 = [max(dist), np.median(temp),1,min(dist)] # this is an mandatory initial guess

popt, pcov = curve_fit(sigmoid, temp, dist,p0, method='dogbox')
X = temp
Y = sigmoid(X, *popt)

plt.plot(temp, dist, color='green',label='Average distance')
plt.plot(X,Y, color='red', label='Sigmoid function')
plt.legend()

# plt.plot(temp, gradient_1, color = 'b', label='gradient 1')
# plt.plot(temp, gradient_2, color = 'g', label='gradient 2')

plt.show()
