import logging
import pathlib
import tkinter as tk
from tkinter import filedialog

import numpy as np
from npp_materialslab_tools import TestingData
from npp_materialslab_tools.testing_machine.appElasticityCalculator import \
    ElasticityModulusCalcs, SpecimenDimensions
from npp_materialslab_tools.tktools import TLMatplotlibGraph
from em_model import MVC_Model
from em_viewDashboard import FrameDashboard

DEVELOPMENT_FLAG = True
DEVELOPMENT_FNAME = "testingMachine/data/new XY 0 ABS_CNT 2%.csv"   

class MVC_Controller():

    def __init__(self, model:MVC_Model, views:dict):

        self.model = model
        self.views = views 
        self._init_bindings()

    def _init_bindings(self):
        self.view_dashboard.btnPlotLoadDisplacement.configure(command=self.plot_load_displacement)
        self.view_dashboard.btnStressStrainPlot.configure(command=self.plot_stress_strain)

    @property
    def view_dashboard(self)->FrameDashboard:
        return self.views['Dashboard']

    @property
    def view_ldgraph(self)->TLMatplotlibGraph:
        return self.views['LDcurve']
    @property
    def view_ss_graph(self)->TLMatplotlibGraph:
        return self.views['SScurve']

    def plot_load_displacement(self):
        logging.debug('This should plot the load displacement curve')
        self.view_ldgraph.ax.cla()
        self.view_ldgraph.ax.plot(self.emc.displacement, self.emc.F_Ns, 'o')
        self.view_ldgraph.ax.set_xlabel( 'Displacement [mm]')
        self.view_ldgraph.ax.set_ylabel( 'F[N]')
        
        if self._fname is not None:
            self.model.isFolderSelected = True
            self.view_dashboard.lbLFolderSelected.config(bg=self.view_dashboard.COLOR_ENABLE)
        else:
            self.model.isFolderSelected = False
            self.view_dashboard.lbLFolderSelected.config(bg=self.view_dashboard.COLOR_DISABLE)

        self.view_ldgraph.canvas.draw() # this is important to show the graph


    def plot_stress_strain(self):
        logging.debug('This should plot the stress-strain graph')
        self.view_ss_graph.ax.cla()
        sd = self.get_specimen_data()

        self.view_ss_graph.ax.plot(self.emc.displacement/sd.gauge_length_mm, self.emc.F_Ns/sd.csArea_mm2, 'o')
        self.view_ss_graph.ax.set_xlabel( 'Strain []')
        self.view_ss_graph.ax.set_ylabel( 'Stress [MPa]')
        self.view_ss_graph.canvas.draw() # this is important to show the graph
  
    def get_specimen_data(self)->SpecimenDimensions:
        width = float(self.model.width_tkvar.get())
        thickness = float(self.model.thickness_tkvar.get())
        gauge_length = float(self.model.gaugelength_tkvar.get())
        sd = SpecimenDimensions(width_mm=width, thickness_mm=thickness, gauge_length_mm=gauge_length)
        logging.debug(f'SpecimenCrosssection : {sd.csArea_mm2} [mm^2]')
        return sd



    def select_testfile(self):
        """select an test file to display data, and load data

        change the label of the folder selected
        """        

        if DEVELOPMENT_FLAG:
            filename = DEVELOPMENT_FNAME    
        if not filename:
            filename = "testingMachine/data/new XY 0 ABS_CNT 2%.csv"
            filename = filedialog.askopenfilename(initialdir = "./")
        try:
            self._fname = pathlib.Path(filename)
            # self._tdobj = TestingData(fname=filename)

            self.emc = ElasticityModulusCalcs(tdobj=TestingData(fname=filename))
        except Exception as e:
            print(e)   



