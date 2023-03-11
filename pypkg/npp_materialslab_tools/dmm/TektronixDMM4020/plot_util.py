# this is a script for Tektronix DMM4020 Multimeter writen for a linux PC
#
# This is NOT COMPLETE YET. 
# 

#!/usr/bin/python
'''
    A simple script to draw a live graph 
    from the data output of a Tektronix DMM4020 Multimeter.
    Copyright (C) 2013  JP Meijers
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
Sources: 
    http://stackoverflow.com/questions/18791722/can-you-plot-live-data-in-matplotlib
    https://gist.github.com/electronut/5641933
TODO: 
    h5py for logging on disk
'''

import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt
import threading

#Graph size in pixels
plt_width = 1800
plt_height = 950
plt_dpi = 100

#Y axis min and max
y_min = -10e-3
y_max = 20e-3

#X axis
#Remeber that the time per tick is the rate at which the multimeter samples
x_tick_count = 1000

#GUI refresh time in seconds
update_interval = 0.1

# class that holds analog data for N samples
class AnalogData:
    # constr
    def __init__(self, maxLen):
        self.value = deque([0.0]*maxLen)
        self.unit = "Unit"
        self.maxLen = maxLen
 
    # ring buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)
    
    # add data
    def add(self, value, unit):
        self.addToBuf(self.value, value)
        self.unit = unit
    
# plot class
class AnalogPlot:
    # constr
    def __init__(self, analogData):
        #set plot size
        fig = plt.figure(figsize=(plt_width/plt_dpi, plt_height/plt_dpi), dpi=plt_dpi)
        # set plot to animated
        plt.ion() 
        self.axline, = plt.plot(analogData.value)
        plt.ylim([y_min, y_max])
        plt.ylabel(analogData.unit)
 
    # update plot
    def update(self, analogData):
        self.axline.set_ydata(analogData.value)
        plt.ylabel(analogData.unit)
        plt.draw()

def data_listener(strPort, analogData, ser):
  
    while True:
        try:
            line = ser.readline()
            
            line_tuple = line.split()
            if(len(line_tuple)==2):
                value = float(line.split()[0])
                unit = line.split()[1]

                analogData.add(value, unit)
                
        except ValueError:
            pass
        except IndexError:
            pass

# main() function
def main():
    # expects 1 arg - serial port string
    if(len(sys.argv) != 2):
        print ('Example usage: python showdata.py "/dev/tty.usbmodem411"')
        exit(1)

    #strPort = '/dev/tty.usbserial-A7006Yqh'
    strPort = sys.argv[1];

    # plot parameters
    analogData = AnalogData(x_tick_count)
    analogPlot = AnalogPlot(analogData)

    print ('plotting data...')

    # open serial port
    ser = serial.Serial(strPort, 9600)
    line = ser.readline()

    thread = threading.Thread(target=data_listener,args=(strPort,analogData,ser))
    thread.daemon = True
    thread.start()

    while True:
        try:
            analogPlot.update(analogData)
            sleep(update_interval)


        except KeyboardInterrupt:
            print( 'exiting')
            break
    # close serial
    ser.flush()
    ser.close()

# call main
if __name__ == '__main__':
     main()