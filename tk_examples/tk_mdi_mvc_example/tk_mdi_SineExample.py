# this is a damped down version of multiple_tk.py in iesl.dlp_printer.dg repository 
# 
# also see https://www.pythontutorial.net/tkinter/tkinter-mvc/
# 
# this only plot a sin graph. 
#%%
import logging
import pathlib
import tkinter as tk
import tkinter.font as tkfont
from pickle import FALSE
from tkinter import filedialog, messagebox, ttk
import numpy as np

from npp_materialslab_tools.tktools import TLImageProjection, TLMatplotlibGraph

# from npp_dlp_printer import TLImageProjection, DLP_Model
# from npp_dlp_printer.control.dlp_control import DLP_Controller
# from npp_dlp_printer.actuator import *
# from npp_dlp_printer.actuator.tk_kdc101_app import TLKinesisControl




logging.basicConfig(level=logging.ERROR)

#%% following code is useful for seeing the tk variables. 
# btnUp = tk.Button( text='+', name='up (+)')
# for k,v in btnUp.config().items():
#     print(k, v)
#%%
BORDERWIDTH = 5
DLP_Y_SIZE =600
DLP_X_SIZE =800


class MVC_Model():
    # isFolderSelected = False
    FolderPath = None
    FileList = []


    def __init__(self):
        # self._exposure_ms = tk.IntVar(value=10)
        # self._delay_ms = tk.IntVar(value=10)
        # self._travel_mm = tk.DoubleVar(value=0.01)
        # self._travel_init = tk.DoubleVar(value=0)
        self._isFolderSelected = tk.BooleanVar(value=False)

        self._emergency_stop_flag = False
        pass

    def reset(self):
        """resets the DLP model
        """        
        self._isFolderSelected = False
        self.FolderPath = None
        self.FileList = []


    @property   
    def isFolderSelected(self):
        return self._isFolderSelected.get()
    
    @isFolderSelected.setter
    def isFolderSelected(self, state:bool):
        """is the folder selected 

        """        
        self._isFolderSelected.set(state)

    def isFolderSelectd_var(self)->tk.BooleanVar:
        """function that returns the isFolderSelected intvar object so that it can be placed in an entry box

        Returns:
            tk.BooleanVar: the reference to the intvar object
        """        
        return self._isFolderSelected

    @property   
    def isEmergencyStopActivated(self):
        return self._emergency_stop_flag
    
    @isEmergencyStopActivated.setter
    def isEmergencyStopActivated(self, state:bool):
        """Sets the emergency stop 

        """
        if state ==True:
            logging.error('Setting true')  
        self._emergency_stop_flag = state


class MVC_Controller():

    def __init__(self, model, view_dashboard, view_ldgraph:TLMatplotlibGraph):
        self.model = model
        self.view = view_dashboard
        self.view_ldgraph = view_ldgraph

    def plot_simple_graph(self):
        print('This should plot a graph')
        x = np.linspace(0, np.pi*2 ,100)
        y = np.sin(x)
        self.view_ldgraph.ax.plot(x,y)
        self.view_ldgraph.canvas.draw() # this is important to show the graph

    def show_file_list(self):
        """Create a disposable file window to display a file list 

        TODO: this spawns a new window every time the button is pressed 
              I shoudl replace it with a constant file
        """        
        file_list_window = tk.Toplevel()
        file_list_window.geometry('200x100')
        file_list_window.resizable(True, True)
        file_list_window.title('Listbox')

        file_list_window.columnconfigure(0, weight=1)
        file_list_window.rowconfigure(0, weight=1)

        # create a list box
        basenames = [x.name for x in self.FileList]

        var_image_filenames = tk.StringVar(value=basenames)

        listbox = tk.Listbox(
            file_list_window,
            listvariable=var_image_filenames,
            height=6,
            selectmode='extended')

        listbox.grid(
            column=0,
            row=0,
            sticky='nwes'
        )


class FrameDashboard(tk.Frame):
    __mvc_controller = None # needs initialisation
    COL_WIDTH=10
    COLOR_ENABLE = 'green'
    COLOR_DISABLE = 'red'
    COLOR_DISABLEd_STATE = 'gray'

    @property
    def FolderPath(self):
        return self.model.FolderPath
    @FolderPath.setter
    def FolderPath(self,val:pathlib.Path):
        self.model.FolderPath = val

    @property
    def mvc_controller(self):
        return self.__mvc_controller
    
    def set_controller(self, controller):
        self.__mvc_controller =controller

    @property
    def FileList(self):
        return self.model.FileList
    @FileList.setter
    def FileList(self,val:pathlib.Path):
        self.model.FileList = val

    def __init__(self, master):
        """Constructor 

        Args:
            master(_type_):  this assumes that the container has the attribute ._stage so this should be propagated
        """        
        super().__init__(master)

        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self['borderwidth'] = BORDERWIDTH
        self['relief'] = 'ridge'

        self.model =  MVC_Model()
        self.__create_widgets()


    def __create_widgets(self):
        #  widgets
        #row0
        self.lblTitle = tk.Label(self, text='Dashboard')
        self.lblTitle['font']  = tkfont.Font(weight='bold')
        self.lblTitle.grid(column=0, row=0, columnspan=2)
        #row1
        self.btnFolder=tk.Button(self, text='Select \nImg Folder', width=self.COL_WIDTH,  command=self.select_image_directory, name='btnSelectImageDirectory')
        self.btnFolder.grid(column=0, row=1, sticky='ew')
        self.lbLFolderSelected=tk.Label(self, text=' --NA--', width=self.COL_WIDTH, bg=self.COLOR_DISABLE, name='lblSelectImageDirectory')
        self.lbLFolderSelected.grid(column=1, row=1, sticky='ewns')
        #row2
        self.btnPlotSimpleFile=tk.Button(self, text='Show \n file list', width=self.COL_WIDTH,  command=self.showPlot, name='btnShowFileList')
        self.btnPlotSimpleFile.grid(column=0, row=2, sticky='ew')

        ######################################  PARAMETERS 

        ###################################### Apply customisation to all widges        
        for widget in self.winfo_children():
            widget.grid(padx=5, pady=3)
        # # variables
        # self.boolOverride = tk.BooleanVar(self, name='bool_override', value=True)

    def showPlot(self):
        """this is a dummy function that only callsthe controller. It is required because of cyclic loading. 
        """        
        self.mvc_controller.plot_simple_graph()

    def select_image_directory(self):
        """select an directory that contains an image.

        change the label of the folder selected
        """        

        self.FolderPath = pathlib.Path(filedialog.askdirectory(title = "select image directory"))
        no_images = self.prepare_filelist()
        
        if no_images>0:
            self.model.isFolderSelected = True
            self.lbLFolderSelected.config(bg=self.COLOR_ENABLE)
        else:
            self.model.isFolderSelected = False
            self.lbLFolderSelected.config(bg=self.COLOR_DISABLE)
        
    def prepare_filelist(self)-> int:
        """prepares the filenames 
        - validates the names 
        - TODO :changes te isFolderSelected? 
        """        
        filetypes = [
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
            ("image", ".bmp"),
        ]
        IMAGE_EXTS = [x[1] for x in filetypes]

        all_files = []
        for path in self.FolderPath.glob(r'*'):
            if path.suffix in IMAGE_EXTS:
                all_files.append(path)

        self.FileList = all_files

        
        noImages = len(self.FileList)
        self.lbLFolderSelected.config(text=str(noImages )+" imgs")
        return noImages


    def start_printing(self):

        # logging.error('NOT IMPLEMENTED YET')
        self.master.control.start_printing()


class App_DLPcontrol(tk.Tk):

    def __init__(self):
        super().__init__()

        # self.protocol('WM_DELETE_WINDOW', self.onclosing) # protocol handler
        sizeXY = (300, 300 )
        upperleftCornerPosition = (500,400)
        self.geometry(f'{sizeXY[0]}x{sizeXY[1]}+{upperleftCornerPosition[0]}+{upperleftCornerPosition[1]}')
        self.title('Simple TK mdi window ')

        self._tlLoadDisplacementGraph = TLMatplotlibGraph(self)
        self._tlLoadDisplacementGraph.withdraw()

        self._create_widgets()

        # see https://www.pythontutorial.net/tkinter/tkinter-mvc/
        self.__model =  MVC_Model()
        self.__controller =  MVC_Controller(model = self.__model, view_dashboard= self.TFDashBoard, view_ldgraph= self._tlLoadDisplacementGraph)

        self.TFDashBoard.set_controller(self.__controller)



    def _create_widgets(self):
        # place a button on the root window
        tk.Button(self,
                text='Toggle Graph Window',
                command=self.toggle_motorcontrol_visibility).grid(row=0, column=0)       
        ## row 1
        self.TFDashBoard = FrameDashboard(self)
        self.TFDashBoard.grid(column=0, row=1, columnspan=2, sticky='nesw')



    def toggle_motorcontrol_visibility(self):
        self.update()
        if self._tlLoadDisplacementGraph.winfo_viewable():
            self._tlLoadDisplacementGraph.withdraw()
        else:
            self._tlLoadDisplacementGraph.deiconify()

if __name__ == "__main__":

    app = App_DLPcontrol()
    app.mainloop()