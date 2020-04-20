# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import numpy as np

from scipy.signal import savgol_filter
import matplotlib.pyplot as plot

#Load Data
data = np.loadtxt('CIR_B3_020420_0.txt', delimiter ='\t', skiprows = 10)
data2 = np.loadtxt('CIR_B3_020420_1.txt', delimiter ='\t')
data3 = np.loadtxt('CIR_B3_020420_2.txt', delimiter ='\t')
data4 = np.loadtxt('CIR_B3_020420_3.txt', delimiter ='\t')

#Concat Files
#data2[:,0] = data2[:, 0] + data[-1, 0]
#data3[:,0] = data3[:, 0] + data2[-1, 0]

data = np.concatenate((data, data2))
data = np.concatenate((data, data3))
data = np.concatenate((data, data4))

#data = np.concatenate((data, data3))
#data = np.concatenate((data, data4))

Time = data[:, 0]
Light_intensity = data[:,1]
#Smoothing

# interpolate + smooth

window_size, poly_order = 2605, 3
O = 0.1 + np.log10(Light_intensity[0]/Light_intensity[:]) #Optical Density
sg_O = savgol_filter(O, window_size, poly_order)
window_size, poly_order = 13227, 3
sg_O = savgol_filter(sg_O, window_size, poly_order, mode = 'mirror')
oo = np.log(sg_O) # Ln(O.D.)

#sg_LI = savgol_filter(Light_intensity, window_size, poly_order)
#O = 0.1 + np.log10(sg_LI[0]/sg_LI[:]) #Optical Density
#oo = np.log(O) # Ln(O.D.)

O_diff = np.gradient(oo, Time) #Numerical Differential
O_diff = savgol_filter(O_diff, 5265, poly_order)

figure = plot.figure(constrained_layout = True)
grid = figure.add_gridspec(4,4)
f_axes1 = figure.add_subplot(grid[0:2,:]) # Plot OD
f_axes2 = figure.add_subplot(grid[2:,0:2]) # Plot LI
f_axes3 = figure.add_subplot(grid[2:,2:]) # Plot d(DO)/dt

#ln1, = f_axes1.plot(Time, O) 
ln2, = f_axes1.plot(Time, sg_O)
ln4, = f_axes2.plot(Time, oo)

ln3, = f_axes3.plot(Time, O_diff)

plot.show()
