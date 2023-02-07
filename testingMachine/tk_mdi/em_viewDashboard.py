# import logging
import pathlib
import tkinter as tk
import tkinter.font as tkfont

# from em_model import MVC_Model
# logging.basicConfig(level=logging.ERROR)

BORDERWIDTH = 5
# DLP_Y_SIZE =600
# DLP_X_SIZE =800

class FrameDashboard(tk.Frame):
    __mvc_controller = None # needs initialisation
    COL_WIDTH=10
    COLOR_ENABLE = 'green'
    COLOR_DISABLE = 'red'
    COLOR_DISABLEd_STATE = 'gray'

    def __init__(self, master, mvc_model):
        """Constructor 

        Args:
            master(_type_):  this assumes that the container has the attribute ._stage so this should be propagated
        """        
        super().__init__(master)

        self.__model = mvc_model
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self['borderwidth'] = BORDERWIDTH
        self['relief'] = 'ridge'

        # self.model =  MVC_Model()
        self.__create_widgets()


    @property
    def mvc_controller(self):
        return self.__mvc_controller
    
    def set_controller(self, controller):
        self.__mvc_controller =controller

    def __create_widgets(self):
        #  widgets
        #row0
        self.lblTitle = tk.Label(self, text='Dashboard')
        self.lblTitle['font']  = tkfont.Font(weight='bold')
        self.lblTitle.grid(column=0, row=0, columnspan=2)
        #row1
        self.btnFolder=tk.Button(self, text='Select \nData File', width=self.COL_WIDTH,  
            command=lambda : self.mvc_controller.select_testfile(), name='btnSelectImageDirectory')
        self.btnFolder.grid(column=0, row=1, sticky='ew')
        self.lbLFolderSelected=tk.Label(self, text=' --NA--', width=self.COL_WIDTH, bg=self.COLOR_DISABLE, name='lblSelectImageDirectory')
        self.lbLFolderSelected.grid(column=1, row=1, sticky='ewns')
        #row2
        self.btnPlotLoadDisplacement=tk.Button(self, text='plot Load \n Displacement', width=self.COL_WIDTH  
            #,command=lambda :self.mvc_controller.plot_load_displacement()
            , name='btnLoadDisplacementPlot')
        self.btnPlotLoadDisplacement.grid(column=0, row=3, sticky='ew')
        
        self.btnStressStrainPlot=tk.Button(self, text='plot Stress \n Strain', width=self.COL_WIDTH  
            
            , name='btnStressStrainPlot')
        self.btnStressStrainPlot.grid(column=1, row=3, sticky='ew')

        ######################################  PARAMETERS 

        ###################################### Apply customisation to all widges        
        for widget in self.winfo_children():
            widget.grid(padx=5, pady=3)
        # # variables
        
        self.fsd = FrameSpecimenData(master=self, mvc_model=self.__model)
        self.fsd.grid(column=0, row=2, columnspan=2, sticky='nesw')

class FrameSpecimenData(tk.Frame):
    __mvc_controller = None # needs initialisation
    COL_WIDTH=10
    COLOR_ENABLE = 'green'
    COLOR_DISABLE = 'red'
    COLOR_DISABLEd_STATE = 'gray'
        

    @property
    def mvc_controller(self):
        return self.__mvc_controller
    
    def set_controller(self, controller):
        self.__mvc_controller =controller
        

    def __init__(self, master, mvc_model):
        """Constructor 

        Args:
            master(_type_):  this assumes that the container has the attribute ._stage so this should be propagated
            mvc_model (MVC_model): 
        """        
        super().__init__(master)

        self.__model = mvc_model
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self['borderwidth'] = BORDERWIDTH
        self['relief'] = 'ridge'

        # self.model =  MVC_Model()
        self.__create_widgets()
        


    def __create_widgets(self):
        #  widgets
        #row0
        self.lblTitle = tk.Label(self, text='Specimen Data')
        self.lblTitle['font']  = tkfont.Font(weight='bold')
        self.lblTitle.grid(column=0, row=0, columnspan=2)
        #row1
        self.lblWidth=tk.Label(self, text='Width [mm]:', width=self.COL_WIDTH,  name='lblWidthLabel')
        self.lblWidth.grid(column=0, row=1, sticky='ew')
        self.txtWidth_mm=tk.Entry(self, text='10', width=self.COL_WIDTH, name='txtWidth', textvariable=self.__model.width_tkvar)
        self.txtWidth_mm.grid(column=1, row=1, sticky='ew')
        #row4
        self.lblThickness_mm=tk.Label(self, text='Thickness [mm]:', width=self.COL_WIDTH,  name='lblThickness_mm')
        self.lblThickness_mm.grid(column=0, row=2, sticky='ew')
        self.txtThickness_mm=tk.Entry(self, text='10', width=self.COL_WIDTH, name='txtThickness_mm', textvariable=self.__model.thickness_tkvar)
        self.txtThickness_mm.grid(column=1, row=2, sticky='ew')
        #row5
        self.lblGaugeLength=tk.Label(self, text='GaugeLength [mm]:', width=self.COL_WIDTH,  name='lblGaugeLength_mm')
        self.lblGaugeLength.grid(column=0, row=3, sticky='ew')
        self.txtGaugeLength=tk.Entry(self, text='10', width=self.COL_WIDTH, name='txtGaugeLength_mm')
        self.txtGaugeLength.grid(column=1, row=3, sticky='ew')
        self.txtGaugeLength.configure(textvariable=self.__model.gaugelength_tkvar)

        ######################################  PARAMETERS 

        ###################################### Apply customisation to all widges        
        for widget in self.winfo_children():
            widget.grid(padx=5, pady=3)
        
