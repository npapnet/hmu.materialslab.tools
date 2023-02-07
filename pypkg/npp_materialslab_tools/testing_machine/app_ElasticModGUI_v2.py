#%%[markdown]
# This is a version Point Selector2 (separating the selection process from the gui creation)
#%% 
import datetime
import logging
import pathlib
from dataclasses import dataclass
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Button, TextBox
from npp_materialslab_tools.plottools import PointsSelector2
from npp_materialslab_tools.testing_machine import TensileData, TensileSpecimenDimensions
from npp_materialslab_tools.testing_machine.app_ElasticModGUI_v1 import  ElasticityModulusCalcs

DEVELOPMENT_FLAG = True
DEVELOPMENT_FNAME = "testingMachine/data/new XY 0 ABS_CNT 2%.csv"  

if DEVELOPMENT_FLAG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)


class ElasticityModulusCalculatorGUIv2(object):
    """
    Like Cursor but the crosshair snaps to the nearest x, y point.
    For simplicity, this assumes that *x* is sorted.

    This is a simple state machine, with the following states:
    - 0: uninitialised (ready to select first point)
    - 1: selected first point (ready to select first point)
    - 2: selected two points (perform computation)
    
    # TODO split GUI from calculations
    """

    def __init__(self,  filename=None):
        self._res_filename = None
        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        plt.subplots_adjust(bottom=0.25, top=0.98)
        self.txt = self.ax.text(0.7, 0.05, '', transform=self.ax.transAxes)
    
        
        self.load_data(filename=filename)
        self.create_plot()
        self.ps2 =  PointsSelector2(fig = self.fig, ax = self.ax)
        
        self.ps2.reset_SM()
        self._createTBs()

    def load_data(self, filename=None):
        """function that loads the data

        Args:
            filename (_type_, optional): _description_. Defaults to None.
        """ 
        if DEVELOPMENT_FLAG:
            filename = DEVELOPMENT_FNAME    
        if not filename:
            filename = "testingMachine/data/new XY 0 ABS_CNT 2%.csv"
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename(initialdir = "./")
        try:
            self._fname = pathlib.Path(filename)
            # self._tdobj = TestingData(fname=filename)

            self.emc = ElasticityModulusCalcs(tdobj=TensileData(fname=filename))
            
        except Exception as e:
            print(e)        

    @property 
    def displacement(self):
        """Delegates displacement to the ElasticityModulusCalcs

        Returns:
            _type_: _description_
        """        
        return self.emc.displacement
    @property 
    def F_Ns(self):
        """Delegates the F_Ns to the  ElasticityModulusCalcs

        Returns:
            _type_: _description_
        """        
        return self.emc.F_Ns

    def create_plot(self):
        # text location in axes coords
        self.ax.cla()
        self.ax.plot(self.displacement, self.F_Ns, 'o')
        self.ax.set_xlabel( 'Displacement [mm]')
        self.ax.set_ylabel( 'F[N]')
        self.ax.figure.canvas.draw()
        

    def _createTBs(self):
        '''
        Creates textBoxes and Reset button
        plt.axes([x, y, dx, dy])
        - x from lower left corner
        - y from lower left corner
        - dx horizontal width 
        - dy Vertical width 
        '''

        row1y,row2y =   0.12, 0.02
        col1x, col2x, col3x, col4x = 0.15, 0.35, 0.65, 0.85
        btnWidth, btnHeight = 0.10, 0.05

        self.axWidthBtn = plt.axes([col1x, row1y, btnWidth, btnHeight])
        self.tbWidth = TextBox(self.axWidthBtn, 'Width [mm]', initial='10.1')
        self.axThicknessBtn = plt.axes([col2x, row1y, btnWidth, btnHeight])
        self.tbThickness = TextBox(self.axThicknessBtn, 'Thickness [mm]', initial='3.1')
        self.axGaugeLengthBtn = plt.axes([col1x, row2y, btnWidth, btnHeight])
        self.tbGaugeLength = TextBox(self.axGaugeLengthBtn, 'G. Length [mm]', initial='90')
        
        self.tbWidth.on_submit(lambda event: self.computations())
        self.tbThickness.on_submit(lambda event: self.computations())
        
        # Reset button
        self.axResetBtn = plt.axes([col4x, row1y, btnWidth, btnHeight])
        self.btnReset = Button(self.axResetBtn, 'Reset')
        self.btnReset.on_clicked(self.on_reset)

        # Computations  button
        self.axComputationsBtn = plt.axes([col3x, row1y, btnWidth, btnHeight])
        self.btnComputations = Button(self.axComputationsBtn, 'computations')
        self.btnComputations.on_clicked(lambda event: self.computations())

        # Open new data set
        self.axOpenNewFileBtn = plt.axes([col3x, row2y, btnWidth, btnHeight])
        self.btnNewFile = Button(self.axOpenNewFileBtn, 'New file')
        self.btnNewFile.on_clicked(lambda event: self.new_file())

        # append to file button
        self.axAppendToFileBtn = plt.axes([col4x, row2y, btnWidth, btnHeight])
        self.btnAppend = Button(self.axAppendToFileBtn, 'To File')
        self.btnAppend.on_clicked(lambda event: self.appendToFile())

    def on_reset(self, event):
        self.ps2.reset_SM()
        self.create_plot()
        self.txt = self.ax.text(0.01, 0.95, self._fname.stem, transform=self.ax.transAxes)

    def new_file(self):
        """loads new file
        """        
        self.load_data(filename=None)
        self.reset_SM()

    def appendToFile(self):
        if self._sm != 2:
            print ('Cannot estimate E yet!')
            return 
        if not self._res_filename:
            self._res_filename = datetime.datetime.now().strftime("res%Y%m%d%H%M%S.txt")
            #self._res_filename = 'results_log.txt'
            with open(self._res_filename, 'w') as file:
                file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format('Timestamp','Filename','Width', 'Thickness', 'start_Ind', 'end_Ind', 'E_GPA_pt', 'E_GPA_lrg'))
       
        with open(self._res_filename, 'a') as file:
            E_GPa_pt = self._compute_mod_elasticity()
            E_GPa_lnr = self._compute_mod_elasticity_lnr(self._points_collected[1].indx, self._points_collected[2].indx)
            file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), self._fname.stem ,self._dim_w, self._dim_t, self._points_collected[1].indx, self._points_collected[2].indx, E_GPa_pt, E_GPa_lnr))
       
    

    def get_specimenDimensions(self):
        ''' calcate crossection'''
        self._dim_w = float(self.tbWidth.text)
        self._dim_t = float(self.tbThickness.text)
        self._dim_l = float(self.tbGaugeLength.text)

        self._specimenDimensions = TensileSpecimenDimensions(gauge_length_mm=self._dim_l, thickness_mm= self._dim_t, width_mm=self._dim_w)
        return self._specimenDimensions

    def computations(self):
        specimenDimensions= self.get_specimenDimensions()
        self.exxs = self.displacement / specimenDimensions.gauge_length_mm
        res= self.emc.computations(specimen=specimenDimensions, points_collected = self.ps2._points_collected)
        E_GPa_pt = res['E_MPa_simple']
        E_GPa_lnr = res['E_MPa_lsq']
        #output to plot and console
        start_ind = self.ps2._points_collected[1].indx
        end_ind = self.ps2._points_collected[2].indx
        self._l_selected = self.ax.plot(self.displacement[start_ind:end_ind], self.F_Ns[start_ind:end_ind], 'r')
        self.txt = self.ax.text(0.7, 0.05, '', transform=self.ax.transAxes)
        self.txt.set_text('E = {:.2f}[Mpa]'.format (E_GPa_lnr))
        # console
        print('E (pt): {:0.2f}[MPa]       E (linear regression): {:0.2f}[MPa] '.format(E_GPa_pt, E_GPa_lnr))



#%%
if __name__ == "__main__":

    # snap_cursor = ElasticityModulusCalculator('../Results/20190327-tests/D00_02.xlsx')
    snap_cursor = ElasticityModulusCalculatorGUIv2()

    plt.show()