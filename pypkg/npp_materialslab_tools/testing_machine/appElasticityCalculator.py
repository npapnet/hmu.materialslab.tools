# from https://matplotlib.org/gallery/misc/cursor_demo_sgskip.html
import datetime
import pathlib
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Button, TextBox
from npp_materialslab_tools import TestingData


class Cursor():
    def __init__(self, ax, ID, x, y, indx):
        '''
        '''
        self.ID = ID
        self.ax = ax # make cursor aware of the ax that's been plotted to. 
        self.x = x
        self.y = y
        self.indx = indx
        self.col = 'k'

    def __str__(self):
        return "ID:{}, (x:{}, y:{}) @ ind:{}".format(self.ID, self.x, self.y, self.indx)

    def plot_cursor(self, new = True):
        ''' Plots a cursor 
        '''
        if new:
            self.lx = self.ax.axhline(self.y, color='k')  # the horiz line
            self.ly = self.ax.axvline(self.x, color='k')  # the vert line
        else:
            self.lx.set_ydata(self.y)
            self.ly.set_xdata(self.x)

    def remove_line(self):
            self.ax.lines.remove(self.lx)
            self.ax.lines.remove(self.ly)        
            self.lx = None
            self.ly = None

class ElasticityModulusCalculator(object):
    """
    Like Cursor but the crosshair snaps to the nearest x, y point.
    For simplicity, this assumes that *x* is sorted.

    This is a simple state machine, with the following states:
    - 0: uninitialised (ready to select first point)
    - 1: selected first point (ready to select first point)
    - 2: selected two points (perform computation)
    
    """

    def __init__(self,  filename=None):
        self._res_filename = None
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25, top=0.98)
        self.txt = self.ax.text(0.7, 0.05, '', transform=self.ax.transAxes)
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)


        self.load_data(filename=filename)
        self.create_plot()

        self._points_collected = {} # pseudo not required.
        
        self.reset_SM()
        self._createTBs()

    def load_data(self, filename=None):
        if not filename:
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename(initialdir = "./")
        try:
            self._fname = pathlib.Path(filename)
            self._tdobj = TestingData(fname=filename)

            df = self._tdobj._data
            self._df = df
            self.displacement = np.array(df.index)
            self.F_Ns = np.array(df['load_avg'])
            # self.exxs = np.ones_like(self.F_Ns)
        except Exception as e:
            print(e)        

    def create_plot(self):
        # text location in axes coords
        self.ax.plot(self.displacement, self.F_Ns, 'o')
        self.ax.set_xlabel( 'time[s]')
        self.ax.set_ylabel( 'F[N]')

    def _createTBs(self):
        '''
        Creates textBoxes and Reset button
        '''
        self.axbox1 = plt.axes([0.15, 0.12, 0.10, 0.05])
        self.tbWidth = TextBox(self.axbox1, 'Width [mm]', initial='10.1')
        self.axbox2 = plt.axes([0.5, 0.12, 0.10, 0.05])
        self.tbThickness = TextBox(self.axbox2, 'Thickness [mm]', initial='3.1')
        self.axbox3 = plt.axes([0.15, 0.02, 0.10, 0.05])
        self.tbGaugeLength = TextBox(self.axbox3, 'G. Length [mm]', initial='90')
        
        self.tbWidth.on_submit(lambda event: self.computations())
        self.tbThickness.on_submit(lambda event: self.computations())
        
        # Reset button
        self.axResetBtn = plt.axes([0.8, 0.10, 0.15, 0.05])
        self.btnReset = Button(self.axResetBtn, 'Reset')
        self.btnReset.on_clicked(lambda event: self.reset_SM())

        # Open new data set
        self.axOpenNewFileBtn = plt.axes([0.5, 0.02, 0.15, 0.05])
        self.btnNewFile = Button(self.axOpenNewFileBtn, 'New file')
        self.btnNewFile.on_clicked(lambda event: self.new_file())

        # append to file button
        self.axAppendToFileBtn = plt.axes([0.8, 0.02, 0.15, 0.05])
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


    def calc_crossection(self):
        ''' calcate crossection'''
        self._dim_w = float(self.tbWidth.text)
        self._dim_t = float(self.tbThickness.text)
        self._dim_l = float(self.tbGaugeLength.text)

        self.csArea_mm2 = self._dim_w*self._dim_t # cross-sectional area
        return self.csArea_mm2

    def computations(self):
        self.calc_crossection()
        self.exxs = self.displacement / self._dim_l
        E_GPa_pt = self._compute_mod_elasticity()
        E_GPa_lnr = self._compute_mod_elasticity_lnr(self._points_collected[1].indx, self._points_collected[2].indx)
        print('E (pt): {:0.2f}[GPa]       E (linear regression): {:0.2f}[GPa] '.format(E_GPa_pt, E_GPa_lnr))
        # self.txt.set_visible(False)
        self.txt = self.ax.text(0.7, 0.05, '', transform=self.ax.transAxes)
        self.txt.set_text('E = {:.2f}[Gpa]'.format (E_GPa_lnr))
        # self.txt.set_visible(True)



    def _compute_mod_elasticity(self):
        '''Calculate modulus of elasticity using two points on the curve'''
        self.calc_crossection()
        exxs  = np.zeros((2,))
        Fs  = np.zeros((2,))
        
        for k in range(2):
            exxs[k] = self.exxs[self._points_collected[k+1].indx]
            Fs[k] = self._points_collected[k+1].y 
        E_GPa_pt = np.diff(Fs)/( self.csArea_mm2 * np.diff(exxs))
        # print('E: {:0.2f}[GPa]'.format(E_GPa_pt[0]))
        return E_GPa_pt[0]
    

    def _compute_mod_elasticity_lnr(self, start_ind, end_ind):
        ''' compute modulus of elasticity using  linear regression '''
        self.calc_crossection()
        E_GPa_lnr = np.polyfit(self.exxs[start_ind:end_ind],self.F_Ns[start_ind:end_ind]/self.csArea_mm2,deg=1)
        self._l_selected = self.ax.plot(self.displacement[start_ind:end_ind], self.F_Ns[start_ind:end_ind], 'r')
        # print('E: {:0.2f}[GPa] (linear regression)'.format(E_GPa_lnr[0]))
        return E_GPa_lnr[0]

    def _calc_x_y_ind(self, x_event, y_event ):
        ''' calculates the x, y and index from the event data
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
            
            self._sm  = 1
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
    snap_cursor = ElasticityModulusCalculator()

    plt.show()