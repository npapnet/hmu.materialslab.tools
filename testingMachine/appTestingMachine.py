
#%% 
# this is a proof of concept with an app that 
# - plots a graphs
# - allows selection of points
# - draws a polygon. 
#%%

import pathlib
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Button

from npp_materialslab_tools import TensileData


class TensileTestApp():
    def __init__(self, fname:pathlib.Path=None):
        self._fig, self._axs = plt.subplots()
        if not isinstance(self._axs, list):
            self._axs  =  [self._axs]
    
        try:
            self._FNAME = pathlib.Path('data')/"new XY 0 ABS_CNT 2%.csv"
            self._tdobj = TensileData(fname=self._FNAME)
        except:
            self._FNAME = pathlib.Path('testingMachine/data')/"new XY 0 ABS_CNT 2%.csv"
            self._tdobj = TensileData(fname=self._FNAME)

        self._prepare_figure()
        self.select_points()

    def _prepare_figure(self):
        ax = self._axs[0]
        df_mean = self._tdobj.data_avg_table

        ax.plot(df_mean.index, df_mean.iloc[:,0].values, alpha=.1, label= 'avg')
        for d, label in zip(df_mean.iloc[:,2:].values.T, ['min', 'max', 'ci:2SD','c2']):
            ax.plot(df_mean.index,d , alpha=.3, label=label ) # df_mean.iloc[:,2:].columns)
        self._set_labels(xlabel="Displacement [mm]", ylabel="Force [N]")
        # ax.legend()

        # adding buttons 
        self._fig.subplots_adjust(bottom=0.2)
        self._axSelectPoints = self._fig.add_axes([0.1, 0.05, 0.1, 0.075])
        self._bSelectPoints = Button(self._axSelectPoints, 'Select')
        self._bSelectPoints.on_clicked(self.select_points)

        # axnext = self._fig.add_axes([0.81, 0.05, 0.1, 0.075])


    def _set_labels(self, xlabel:str, ylabel:str, ax=None):
        """sets labels

        Args:
            xlabel (str): _description_
            ylabel (str): _description_
            ax (_type_, optional): _description_. Defaults to None.
        """        
        if ax is None:
            ax = self._axs[0]
        # plt.ylim([155,165])
        # plt.xlim([4,8])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    def _tellme(self,s):
        """auxilliary function to provide info

        Args:
            s (_type_): _description_
        """        
        print(s)
        assert isinstance(self._fig, plt.Figure)
        self._axs[0].set_title(s, fontsize=16)
        self._fig.canvas.draw_idle()

    def select_points(self, event=None):
        """select points
        """        
        ax = self._axs[0]
        self._tellme('Select two points, click to begin')
        plt.waitforbuttonpress()

        no_points = 2
        while True:
            pts = []
            while len(pts) < no_points :
                self._tellme(f'Select {no_points } points with mouse (left click)')
                pts = np.asarray(plt.ginput(no_points, timeout=-1))
                if len(pts) < no_points :
                    self._tellme('Too few points, starting over')
                    time.sleep(1)  # Wait a second

            ph =ax.fill_between(pts[:, 0], pts[:, 1], 'r', lw=2)

            self._tellme('Happy? Key click for yes, mouse click for no')

            if plt.waitforbuttonpress():

                break

            # Get rid of fill
            ph.remove()
# %%
if __name__=="__main__":
    TensileTestApp()