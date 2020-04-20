#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 15:40:52 2019

@author: Alexis
"""
import numpy as np
import mob
import time
from scipy.integrate import odeint

def heat_balance(T,t,Tp,Ta):
    m2 = 20;
    cp2 = 4.186;
    A1 = 36.71;
    A2 = 13.82;
    U2 = 4.02107E-02
    U3 = 2.99871E-03
    
    return (U2*A2*(Tp - T) + U3*A1*(Ta - T))/m2*cp2

##################
reactor = mob.MB(experiment_name = 'CIR_B1_1704')

#### Initialize Variables
print('Initializing')

    ##### Arrays to save data every t_sample
plot_window = 20
data = np.array(np.zeros((plot_window,5))) #Array of data recived from arduino
std =  np.array(np.zeros((plot_window,5))) #Std. Dev. of Data
varz =  np.array(np.zeros((plot_window,5))) #Variance of  Data
Tw = np.zeros((plot_window)) #Temperature of Water inside the Vessel
std_Tw = np.zeros((plot_window)) #Temperature of Water inside the Vessel
varz_Tw = np.zeros((plot_window)) #Temperature of Water inside the Vessel
Time = np.zeros((plot_window)) #Time
t_sample = 10 #Time period between samples in secs
timer_sample = -2*t_sample #Time since last sample

    ##### Arrays to save data every sampling rate and
    ##### store last average_window samples
average_window = 12
temp_data = np.array(np.zeros((average_window, 5)))
temp_Tw = np.zeros((average_window))
temp_Time = np.zeros((average_window))

 ##### Gas feed timer
timer_gas = 0 #Time pump has been on or off


######
A1 = 36.71;
A2 = 13.82;
U2 = 4.02107E-02
U3 = 2.99871E-03

time.sleep(1)
start_time = time.time()
j = 1

print('Experiment Started')
while(True):
    try:
        parameters = np.loadtxt('parameters_020420.txt', delimiter =',')
        #rpm_SP, T_SP, t_gas_on, t_off_t_on
        reactor.rpm_setpoint = parameters[0]
        reactor.T_setpoint = parameters[1]
        t_gas_on = parameters[2]
        t_off_t_on = parameters[3]
        t_gas_off = t_off_t_on*t_gas_on
        t_gas = t_gas_on
        
        temp_data = np.append(temp_data, reactor.read(), axis = 0)
        
        # Estimate water temperature
        if (j == 1):
            j = j + 1
            temp_Tw = np.append(temp_Tw, np.array([temp_data[-1,1] + U3*A1*(temp_data[-1,0]  - temp_data[-1,1])/(U2*A2)]), axis = 0)
            temp_Time = np.append(temp_Time, np.array([start_time - start_time]))
            dt = 1
            
            #Start Gas pump
            reactor.Gas(100)
            timer_gas = time.time() - start_time
            t_gas = t_gas_on
            gas_on = True
        else:
            try:
                temp_data = np.append(temp_data, reactor.read(), axis = 0)
            except:
                pass
            
            
            temp_Time = np.append(temp_Time,  np.array([time.time() - start_time]))
            T_hat = odeint(heat_balance, temp_Tw[-1] , np.linspace(temp_Time[-2], temp_Time[-1], 10), args = (temp_data[-1,1], temp_data[-1,0]))
            temp_Tw = np.append(temp_Tw, np.array([T_hat[-1]]))
            dt = temp_Time[-1] - temp_Time[-2]
        
            #Calculate absorbance
            #temp_data[-1,3] = np.log10(I0/temp_data[-1,3])
            
        #Control calculation
        u_T = reactor.T_pid(temp_Tw[-1], temp_Tw[-2], dt)
        u_rpm = reactor.rpm_pid(temp_data[-1,2], dt)
        
        #Control deploy
        reactor.Heater(u_T)
        reactor.Stirrer(u_rpm)
   
        
        # Turn on and off the gas pump
        if((temp_Time[-1] - timer_gas) > t_gas):
            if gas_on is False:
                reactor.Gas(80)
                timer_gas = time.time() - start_time
                t_gas = t_gas_on
                gas_on = True
            elif(gas_on):
                reactor.Gas(0)
                timer_gas = time.time() - start_time
                t_gas = t_gas_off
                gas_on = False
                
        #array shift
        temp_data = temp_data[-average_window:,:]
        temp_Tw = temp_Tw[-average_window:]
        temp_Time = temp_Time[-average_window:]
        
        if((temp_Time[-1] - timer_sample) > t_sample):
            timer_sample = time.time() - start_time
            
            data = np.append(data, np.mean(temp_data, axis = 0, keepdims = True), axis = 0)
            std = np.append(data, np.std(temp_data, axis = 0, keepdims = True), axis = 0)
            varz = np.append(data, np.var(temp_data, axis = 0, keepdims = True), axis = 0)
            Tw = np.append(Tw, np.mean(temp_Tw))
            std_Tw = np.append(Tw, np.std(temp_Tw))
            varz_Tw = np.append(Tw, np.var(temp_Tw))
            Time = np.append(Time, temp_Time[-1])
            
            #array shift
            data = data[-plot_window:,:]
            std = std[-plot_window:,:]
            varz = varz[-plot_window:,:]
            Tw = Tw[-plot_window:]
            std_Tw = std_Tw[-plot_window:]
            varz_Tw = varz_Tw[-plot_window:]
            Time = Time[-plot_window:]
            
            #Data save       #Tiempo  , ODF                               , ODS                             , Tw                             , Twall                            , Ta                               , rpm   
            reactor.save_data(Time[-1], data[-1,3], std[-1,3], varz[-1,3], data[-1,4], std[-1,4], varz[-1,4], Tw[-1], std_Tw[-1], varz_Tw[-1], data[-1,1], std[-1,1], varz[-1,1], data[-1,0], std[-1,0], varz[-1,0], data[-1,2])

    except KeyboardInterrupt:
        reactor.Heater(0)
        print('Heater turned off')
        reactor.file.close()
        print('Last Data Saved')
        break 
        
    except Exception as e:
        reactor.Heater(0)
        print('Heater turned off')
        reactor.file.close()
        print('Last Data Saved')
        print(e)
        break
 

