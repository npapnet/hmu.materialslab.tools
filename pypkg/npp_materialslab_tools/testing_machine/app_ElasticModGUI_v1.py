# from https://matplotlib.org/gallery/misc/cursor_demo_sgskip.html
import datetime
import pathlib
from dataclasses import dataclass
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Button, TextBox
from npp_materialslab_tools.plottools import Cursor
from npp_materialslab_tools.testing_machine import TensileData, TensileSpecimenDimensions

DEVELOPMENT_FLAG = False
DEVELOPMENT_FNAME = "testingMachine/data/new XY 0 ABS_CNT 2%.csv"   


class ElasticityModulusCalcs():
    """class for performing the calculations

    Returns:
        _type_: _description_

    #TODO move this out of the file
    """    
    def __init__(self, tdobj:TensileData):
        self._testing_data_obj= tdobj
        self._df = self._testing_data_obj._data
        self.displacement = np.array(self._df .index)
        self.F_Ns = np.array(self._df ['load_avg'])

    def computations(self, specimen:TensileSpecimenDimensions, points_collected:dict):
        """perform computations

        Args:
            specimen (SpecimenDimensions): _description_
            points_collected (dict): _description_

        Returns:
            _type_: _description_
        """        
        start_ind = points_collected[1].indx
        end_ind = points_collected[2].indx
        self.csArea_mm2 = specimen.csArea_mm2
        self.exxs = self.displacement / specimen.gauge_length_mm
        E_GPa_pt = self._compute_mod_elasticity(start_ind=start_ind, end_ind=end_ind )
        ''' compute modulus of elasticity using  linear regression '''
        E_GPa_lnr = np.polyfit(self.exxs[start_ind:end_ind],self.F_Ns[start_ind:end_ind]/self.csArea_mm2,deg=1)[0]
        # print('E (pt): {:0.2f}[MPa]       E (linear regression): {:0.2f}[MPa] '.format(E_GPa_pt, E_GPa_lnr))
        return {'E_MPa_simple':E_GPa_pt, 'E_MPa_lsq':E_GPa_lnr}

    def _compute_mod_elasticity(self, start_ind, end_ind):
        '''Calculate modulus of elasticity using two points on the curve'''
        exxs  = np.zeros((2,))
        Fs  = np.zeros((2,)) # N
        
        indices = [start_ind, end_ind]
        for l in range(2):
            indx = indices[l]
            exxs[l] = self.exxs[indx]
            Fs[l] = self.F_Ns[indx] 
        E_GPa_pt = np.diff(Fs)/( self.csArea_mm2 * np.diff(exxs))
        return E_GPa_pt[0]
    
class ElasticityModulusCalculatorGUI(object):
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
        self._points_collected = {} # pseudo not required.

        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        plt.subplots_adjust(bottom=0.25, top=0.98)
        self.txt = self.ax.text(0.7, 0.05, '', transform=self.ax.transAxes)
        
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)

        self.load_data(filename=filename)
        self.create_plot()
        
        self.reset_SM()
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
        self.ax.plot(self.displacement, self.F_Ns, 'o')
        self.ax.set_xlabel( 'Displacement [mm]')
        self.ax.set_ylabel( 'F[N]')

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
        self.btnReset.on_clicked(lambda event: self.reset_SM())

        # Open new data set
        self.axOpenNewFileBtn = plt.axes([col3x, row2y, btnWidth, btnHeight])
        self.btnNewFile = Button(self.axOpenNewFileBtn, 'New file')
        self.btnNewFile.on_clicked(lambda event: self.new_file())

        # append to file button
        self.axAppendToFileBtn = plt.axes([col4x, row2y, btnWidth, btnHeight])
        self.btnAppend = Button(self.axAppendToFileBtn, 'To File')
        self.btnAppend.on_clicked(lambda event: self.appendToFile())

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
       
    def reset_SM(self):
        ''' resets state machine status'''
        try:
            for i in self._points_collected.keys():
                self._points_collected[i].remove_line()
            self.ax.lines.remove(self._l_selected[0])
            self._l_selected = []
        except Exception as e:
            print (e)
        finally:
            self.ax.figure.canvas.draw() 

        self._points_collected = {}
        self._sm = 0
        self.txt.set_text('')

        self.ax.cla()
        self.create_plot()
        self.txt = self.ax.text(0.01, 0.95, self._fname.stem, transform=self.ax.transAxes)

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
        res= self.emc.computations(specimen=specimenDimensions, points_collected = self._points_collected)
        E_GPa_pt = res['E_MPa_simple']
        E_GPa_lnr = res['E_MPa_lsq']
        #output to plot and console
        start_ind = self._points_collected[1].indx
        end_ind = self._points_collected[2].indx
        self._l_selected = self.ax.plot(self.displacement[start_ind:end_ind], self.F_Ns[start_ind:end_ind], 'r')
        self.txt = self.ax.text(0.7, 0.05, '', transform=self.ax.transAxes)
        self.txt.set_text('E = {:.2f}[Mpa]'.format (E_GPa_lnr))
        # console
        print('E (pt): {:0.2f}[MPa]       E (linear regression): {:0.2f}[MPa] '.format(E_GPa_pt, E_GPa_lnr))

    def _calc_x_y_ind(self, x_event, y_event ):
        ''' calculates the x, y and index from the event data

        It does that by finding the closest point.

        Callers: mouse_click
        '''
        indx = min(np.searchsorted(self.displacement, x_event), len(self.displacement) - 1)
        x = self.displacement[indx]
        y = self.F_Ns[indx]
        return x, y, indx       

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
            self.computations()
        else:
            print ("State status: {} | x={:1.2f}, y={:1.2f}".format(self._sm,x,y))
        self.ax.figure.canvas.draw()



#%%
if __name__ == "__main__":

    # snap_cursor = ElasticityModulusCalculator('../Results/20190327-tests/D00_02.xlsx')
    snap_cursor = ElasticityModulusCalculatorGUI()

    plt.show()