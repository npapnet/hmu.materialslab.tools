import logging 
import tkinter as tk

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
        
        self._width_mm_var = tk.StringVar(value="3.0")
        self._thickness_mm_var = tk.StringVar(value="3.0")
        self._gaugeLength_mm_var = tk.StringVar(value="10.0")
        
    def reset(self):
        """resets the DLP model
        """        
        self._isFolderSelected = False
        self.FolderPath = None
        self.FileList = []

    @property
    def width_tkvar(self):
        """tk string var 

        Returns:
            _type_: _description_
        """        
        return self._width_mm_var

    @property
    def thickness_tkvar(self):
        return self._thickness_mm_var

    @property
    def gaugelength_tkvar(self):
        return self._gaugeLength_mm_var


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
