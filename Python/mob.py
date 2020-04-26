#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:19:46 2019

@author: Alexis
"""

import time
import numpy as np
import serial
import os

        
class MB(object):
    T_setpoint = 28.3
    rpm_setpoint = 1500

    def __init__(self, experiment_name = 'Exp1', port=None, baud=57600):
        print('Opening connection')
        self.sp = serial.Serial(port='/dev/ttyACM1', baudrate=baud, timeout=2)
        self.sp.flushInput()
        self.sp.flushOutput()
        self.rpm_integral = 0
        self.T_integral = 0
        self.experiment_name = experiment_name
        self.file_number = 0
        self.file_name = self.experiment_name+'_%d.txt' %(self.file_number,)
        self.max_file_size = 5000000 #File size in bytes
        self.file = open(self.file_name, 'w+')
        self.file.close()
        time.sleep(2)
           
    def Laser(self,pwm):
        self.write('1',pwm)
        return pwm

    def Heater(self,pwm):
        self.write('2',pwm)
        return pwm
        
    def Stirrer(self,pwm):
        self.write('3',pwm)
        return pwm
    
    def Gas(self,pwm):
        self.write('5',pwm)
        return pwm
    
    def T_pid(self, T, T_last, dt):
    
        kp = 70
        ki = 0.04
        kd = 1000
        u_hi = 120
        u_low = 0
        
        T_error = self.T_setpoint - T
        self.T_integral = self.T_integral + ki*T_error*dt
        T_derivative = kd*(T - T_last)/dt
        
        u = kp*T_error + self.T_integral - T_derivative
        
        if(u > u_hi):
            u = u_hi
            self.T_integral = self.T_integral - ki*T_error*dt
        if(u < u_low):
            u = 0
            self.T_integral = self.T_integral - ki*T_error*dt
        
        return u
    
    def rpm_pid(self, rpm, dt):
            kp = 0.165;
            ki = 0.180;
            u_hi = 200;
            u_low = 60;
            
            rpm_error = self.rpm_setpoint - rpm
            self.rpm_integral = self.rpm_integral + ki*rpm_error*dt
            
            u = kp*rpm_error + self.rpm_integral
            if(u > u_hi):
                u = u_hi
                self.rpm_integral = self.rpm_integral - ki*rpm_error*dt
            if(u < u_low):
                u = u_low
                self.rpm_integral = self.rpm_integral - ki*rpm_error*dt
            
            return u
                

    
    def save_data(self, Time, ODF, stdodf, varodf, ODS, stdods, varods, Tw, stdtw, vartw, Twall, stdtwall, vartwall, Ta, stdta, varta, rpm):
        
        stat = os.stat(self.file_name)
        if(stat.st_size < self.max_file_size):
            self.file = open(self.file_name,'a+')
                                                   #Tiempo      , ODF        , ODS      , Tw    , Twall     , rpm   
            self.file.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n"%(Time, ODF, stdodf, varodf, ODS, stdods, varods, Tw, stdtw, vartw, Twall, stdtwall, vartwall, Ta, stdta, varta, rpm))
            self.file.close()
        else:
            self.file.close()
            self.file_number = self.file_number + 1
            self.file_name = self.experiment_name+'_%d.txt' %(self.file_number,)
            self.file = open(self.file_name,'w+')
                                                   #Tiempo      , ODF        , ODS      , Tw    , Twall     , rpm   
            self.file.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n"%(Time, ODF, stdodf, varodf, ODS, stdods, varods, Tw, stdtw, vartw, Twall, stdtwall, vartwall, Ta, stdta, varta, rpm))
            self.file.close()
        

    def get(self):
        cmd_str = self.build_cmd_str('4','')
        try:
            self.sp.write(cmd_str.encode())
            self.sp.flushInput()
        except Exception:
            return None
        return self.sp.readline().decode('UTF-8')
    
    def read(self):
        try:
            data = self.get()
            data = data.split("\t")
            data = np.asarray(data, dtype = np.float64, order = 'C')
            data[0] = (1/( 8.294e-4 + 2.624e-4*np.log(data[0]) + 1.369e-7*np.log(data[0])**3)) - 273.15
            data[1] = (1/( 8.294e-4 + 2.624e-4*np.log(data[1]) + 1.369e-7*np.log(data[1])**3)) - 273.15
            data[2] = (1/( 8.294e-4 + 2.624e-4*np.log(data[2]) + 1.369e-7*np.log(data[2])**3)) - 273.15
            if data[3] > 0:
                data[3] = (1000000/(2*data[3]))*60/2 
                
            data[4] = ((data[4]*1000 - 0.1)/(2300*0.95))
            data[5] = ((1/(data[5]/1e6) - 0.1)/(2300*0.95))
            return np.array([data[0], data[2], data[3], data[4], data[5]], dtype = np.float64).reshape(1, 5)
        except:
            print(data)
    
    def write(self,cmd,pwm):       
        cmd_str = self.build_cmd_str(cmd,(pwm,))
        try:
            self.sp.write(cmd_str.encode())
            self.sp.flush()
        except:
            return None
        return self.sp.readline().decode('UTF-8').replace("\r\n", "")
    
    def build_cmd_str(self,cmd, args=None):
        """
        Build a command string that can be sent to the arduino.
    
        Input:
            cmd (str): the command to send to the arduino, must not
                contain a % character
            args (iterable): the arguments to send to the command
        """
        if args:
            args = ' '.join(map(str, args))
        else:
            args = ''
        return "{cmd} {args}\n".format(cmd=cmd, args=args)
        
    def close(self):
        try:
            self.sp.close()
            print('Arduino disconnected successfully')
        except:
            print('Problems disconnecting from Arduino.')
            print('Please unplug and reconnect Arduino.')
        return True