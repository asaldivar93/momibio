# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import numpy as np

from scipy.signal import savgol_filter
import matplotlib.pyplot as plot

#Load Data
data = np.loadtxt("CIR_B1_020420_0.txt", delimiter ='\t', skiprows = 11)
data2 = np.loadtxt('CIR_B2_020420_0.txt', delimiter ='\t', skiprows = 11)

#Concat Files
data2[:,0] = data2[:, 0] + data[-1, 0]
data = np.concatenate((data, data2[:,0:6]))

Time = data[:, 0]
Light_intensity = data[:,1]

#Smoothing

# interpolate + smooth

window_size, poly_order = len(Time[Time<6])+1, 3
OD = 0.1 + np.log10(Light_intensity[0]/Light_intensity[:]) #Optical Density
sg_OD = savgol_filter(OD, window_size, poly_order)
window_size, poly_order = len(Time[Time<25])+1, 3
sg_OD = savgol_filter(sg_OD, window_size, poly_order, mode = 'mirror')
ln_OD = np.log(sg_OD) # Ln(O.D.)

#sg_LI = savgol_filter(Light_intensity, window_size, poly_order)
#O = 0.1 + np.log10(sg_LI[0]/sg_LI[:]) #Optical Density
#oo = np.log(O) # Ln(O.D.)

mu = np.gradient(ln_OD, Time) #Numerical Differential
mu[mu<0] = 0
#mu = savgol_filter(ln_OD, len(Time[Time<6]) , poly_order)
gen_time = np.log(2)/mu
gen_num = np.zeros((len(Time),1))

for t in range(len(Time)-1):
    gen_num[t+1] = gen_num[t] + (Time[t+1] - Time[t])/gen_time[t]

save = np.stack((Time, sg_OD, mu), axis = -1)
np.savetxt('resultados_0401_1.txt', save, delimiter = '\t')


figure = plot.figure(constrained_layout = True)
grid = figure.add_gridspec(6,4)

ax_gen = figure.add_subplot(grid[4:,:])
ax_OD = figure.add_subplot(grid[0:2,:],sharex = ax_gen)
ax_mu = figure.add_subplot(grid[2:4,:], sharex = ax_gen)

plot.setp(ax_mu.get_xticklabels(), visible = False)
plot.setp(ax_OD.get_xticklabels(), visible = False)

ln1, = ax_OD.plot(Time, OD, label = "Unfiltered")
ln2, = ax_OD.plot(Time, sg_OD, label ="sg_filter")
ax_OD.set_yscale("log")
ax_OD.set_ylim(0, 10**0)
ax_OD.set_ylabel("$D.O._{600nm}$")
ax_OD.legend()
ln3, = ax_mu.plot(Time, mu)
ax_mu.set_ylabel("$ \mu (h^{⁻1})$")
ln4, = ax_gen.plot(Time, gen_num)
ax_gen.set_ylabel("Generaciones")
ax_gen.set_xlabel("Tiempo (h)")

plot.show()
