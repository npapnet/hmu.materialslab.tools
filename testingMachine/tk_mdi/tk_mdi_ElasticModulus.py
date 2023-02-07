# this is a damped down version of multiple_tk.py in iesl.dlp_printer.dg repository 
# 
# also see https://www.pythontutorial.net/tkinter/tkinter-mvc/
# 
# this is intended for Elastic Modulus calculations. 
#%%
import logging
import pathlib
import tkinter as tk
from pickle import FALSE

import numpy as np
from em_controller import MVC_Controller
from em_model import MVC_Model
from em_viewDashboard import FrameDashboard

from npp_materialslab_tools.tktools import TLMatplotlibGraph

logging.basicConfig(level=logging.DEBUG)

#%% following code is useful for seeing the tk variables. 
# btnUp = tk.Button( text='+', name='up (+)')
# for k,v in btnUp.config().items():
#     print(k, v)




#%%
# BORDERWIDTH = 5
# DLP_Y_SIZE =600
# DLP_X_SIZE =800


class App_DLPcontrol(tk.Tk):

    def __init__(self):
        super().__init__()

        # self.protocol('WM_DELETE_WINDOW', self.onclosing) # protocol handler
        sizeXY = (300, 300 )
        upperleftCornerPosition = (500,400)
        self.geometry(f'{sizeXY[0]}x{sizeXY[1]}+{upperleftCornerPosition[0]}+{upperleftCornerPosition[1]}')
        self.title('Simple TK mdi window ')




        #create model
        self.__model =  MVC_Model() 

        # create views 
        self._create_widgets()
        # see https://www.pythontutorial.net/tkinter/tkinter-mvc/
        
        # create Controller
        views = {
            'Dashboard': self.TFDashBoard, 
            'LDcurve':self._tlLoadDisplacementGraph,
            'SScurve':self._tlStressStrainGraph
            }
        self.__controller =  MVC_Controller(model = self.__model, views = views)
        self.TFDashBoard.set_controller(self.__controller)

    def _create_widgets(self):
        # place a button on the root window
        self.btnToggleLDGraph = tk.Button(self,
                text='Toggle \n LD Graph ',
                command=self.toggle_LoadDisplacement_visibility)
        self.btnToggleLDGraph.grid(row=0, column=0)       
        self.btnToggleSSGraph = tk.Button(self,
                text='Toggle \n SS Graph ',
                command=self.toggle_SS_visibility).grid(row=0, column=1)       

        ## row 1
        self.TFDashBoard = FrameDashboard(self, mvc_model=self.__model)
        self.TFDashBoard.grid(column=0, row=1, columnspan=2, sticky='nesw')

        self._tlLoadDisplacementGraph = TLMatplotlibGraph(self)
        self._tlLoadDisplacementGraph.withdraw()

        self._tlStressStrainGraph = TLMatplotlibGraph(self)
        self._tlStressStrainGraph.withdraw()


    def toggle_SS_visibility(self):
        self.update()
        if self._tlStressStrainGraph.winfo_viewable():
            self._tlStressStrainGraph.withdraw()
        else:
            self._tlStressStrainGraph.deiconify()

    def toggle_LoadDisplacement_visibility(self):
        self.update()
        if self._tlLoadDisplacementGraph.winfo_viewable():
            self._tlLoadDisplacementGraph.withdraw()
        else:
            self._tlLoadDisplacementGraph.deiconify()

if __name__ == "__main__":

    app = App_DLPcontrol()
    app.mainloop()