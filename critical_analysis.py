from scipy.misc import derivative
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

df = pd.read_csv('simulation_results_LJ.csv')

df['red Temp'] = (df['T']-1)/1
F_arr = np.array(df['F'])/20
temp = np.array(df['T'])
dist  = np.array(df['d'])
T_c = 1.2
reduced_temp = (temp-T_c)/T_c
gradient_1 = np.gradient(F_arr,temp)
gradient_2 = np.gradient(gradient_1,temp)
C = np.multiply(temp*-1,gradient_2)
log_f = np.log(abs(F_arr))/np.log(abs(reduced_temp))
log_d = np.log(abs(dist))/np.log(abs(reduced_temp))

fig1, ax1 = plt.subplots(3)
ax1[0].plot(temp, F_arr)
ax1[1].plot(temp, gradient_1)
ax1[2].plot(temp, gradient_2)
plt.show()

fig, axs = plt.subplots(2,2)
axs[0][0].plot(temp, log_f, color='green',label='log F/log tau')
axs[0][0].plot(temp, log_d, color='red',label='log d/log tau')
axs[0][0].legend()
# axs[0].set_ylim(-3,1)
axs[0][1].plot(temp, dist,color='r', label='distance')
    
axs[0][1].legend()

# plot by the reduced temperature
axs[1][0].plot(reduced_temp, log_f, color='green',label='log F/log tau')
axs[1][0].plot(reduced_temp, log_d, color='red',label='log d/log tau')
axs[1][0].legend()
axs[1][1].plot(reduced_temp, dist,color='r', label='distance')

axs[1][1].legend()
# plt.plot(temp, gradient_1, color = 'b', label='gradient 1')
# plt.plot(temp, gradient_2, color = 'g', label='gradient 2')

plt.show()
