#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:27:31 2020

@author: alexis
"""

#### Initialize figure
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
import numpy as np

plot.style.use('seaborn')

figure = plot.figure(constrained_layout = True)
grid = figure.add_gridspec(4,4)

ax_ODF = figure.add_subplot(grid[0:2,0:2:]) # Plot OD
ax_ODS = figure.add_subplot(grid[0:2,2:]) # Plot ODS
ax_Temp = figure.add_subplot(grid[2:,0:2]) # Plot Tw
ax_rpm = figure.add_subplot(grid[2:,2:]) # Plot rpm

ln_ODF, = ax_ODF.plot([],[]) # Plot ODF
ln_ODS, = ax_ODS.plot([],[]) # Plot ODS
ln_Tw, = ax_Temp.plot([],[]) # Plot Tw
ln_rpm, = ax_rpm.plot([],[]) # Plot rpm

def init(): 
    ax_ODF.set_ylim(5,30)
    ax_ODS.set_ylim(0,6)
    ax_Temp.set_ylim(27, 29)
    ax_rpm.set_ylim(1300,1800)


#Data plot
def update(i):
    data = np.loadtxt('CIR_CI_020420_0.txt', delimiter ='\t', skiprows = 1)
    Time = data[:,0]
    ODF = data[:,1]
    ODS = data[:,4]
    Tw = data[:,7]
    rpm = data[:,16]
    
    ln_ODF.set_data(Time, ODF)
    ax_ODF.relim()
    ax_ODF.autoscale_view(scaley = False)
    
    ln_ODS.set_data(Time, ODS)
    ax_ODS.relim()
    ax_ODS.autoscale_view(scaley = False)
    
    ln_Tw.set_data(Time, Tw)
    ax_Temp.relim()
    ax_Temp.autoscale_view(scaley = False)
    
    ln_rpm.set_data(Time, rpm)
    ax_rpm.relim()
    ax_rpm.autoscale_view()

ani = FuncAnimation(figure, update, init_func = init, interval = 8000)    
plot.show()
