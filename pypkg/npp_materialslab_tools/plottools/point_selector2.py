#%% 
import logging
from dataclasses import dataclass
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy as np
from npp_materialslab_tools import TensileData
from npp_materialslab_tools.plottools import Cursor

# DEVELOPMENT_FLAG = True
# DEVELOPMENT_FNAME = "testingMachine/data/new XY 0 ABS_CNT 2%.csv"  

# if DEVELOPMENT_FLAG:
#     logging.basicConfig(level=logging.DEBUG)
# else:
#     logging.basicConfig(level=logging.ERROR)
class PointsSelector2():
    def __init__(self, fig, ax):

        self.fig = fig
        self.ax = ax
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)

        self.reset_SM()
        
    def reset_SM(self):
        ''' resets state machine status'''
        self._points_collected = {}
        self._sm = 0
        # self.txt.set_text('')

        # self.ax.cla()

    def _calc_x_y_ind(self, x_event, y_event ):
        ''' calculates the x, y and index from the event data

        It does that by finding the closest point.

        Callers: mouse_click
        '''
        try:
            line = self.ax.lines[0]
            self.xdata = line.get_xdata()
            self._F_Ns = line.get_ydata()
            indx = min(np.searchsorted(self.xdata, x_event), len(self.xdata) - 1)
            x = self.xdata[indx]
            y = self._F_Ns[indx]
            return x, y, indx   
        except:
            return 

    def mouse_click(self, event):
        ''' change the state machine on each click
        ''' 
        if not event.inaxes:
            ''' only continue when a point is picked'''
            return

        # update state machine
        if self._sm == 0:
            crsrID  = self._sm+1
            x,y, indx = self._calc_x_y_ind(event.xdata, event.ydata)
            # update the line positions
            self._points_collected[crsrID] = Cursor(self.ax, crsrID, x, y, indx)
            self._points_collected[crsrID].plot_cursor()
            self._sm = 1
        elif self._sm == 1:
            crsrID  = self._sm+1
            x,y, indx = self._calc_x_y_ind(event.xdata, event.ydata)
            # update the line positions
            self._points_collected[crsrID] = Cursor(self.ax, crsrID, x, y, indx)
            self._points_collected[crsrID].plot_cursor()
            
            self._sm = 2            
        if self._sm ==2:
            logging.debug ("ready to plot")
            # self.computations()
            pass
        else:
            print ("State status: {} | x={:1.2f}, y={:1.2f}".format(self._sm,x,y))
        self.ax.figure.canvas.draw()
