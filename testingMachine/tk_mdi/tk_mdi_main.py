# this is a damped down version of multiple_tk.py in iesl.dlp_printer.dg repository 
#%%
import logging
import pathlib
import tkinter as tk
import tkinter.font as tkfont
from pickle import FALSE
from tkinter import filedialog, messagebox, ttk

# import npp_dlp_printer
from PIL import Image, ImageTk

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

class DLPModel():
    pass
    def exposure_var(self):
        pass
    def delay_var(self):
        pass
    def travel_mm_var(self):
        pass
class FrameDashboard(tk.Frame):
    model = DLPModel()
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
        self.btnShowFileList=tk.Button(self, text='Show \n file list', width=self.COL_WIDTH,  command=self.show_file_list, name='btnShowFileList')
        self.btnShowFileList.grid(column=0, row=2, sticky='ew')

        ######################################  PARAMETERS 
        #row3
        self.lblExposure=tk.Label(self, text='Exposure [ms]:', width=self.COL_WIDTH,  name='lblExposureLabel')
        self.lblExposure.grid(column=0, row=3, sticky='ew')
        self.txtExposure=tk.Entry(self, text='10', width=self.COL_WIDTH, name='txtExposure', textvariable=self.model.exposure_var())
        self.txtExposure.grid(column=1, row=3, sticky='ew')
        #row4
        self.lblDelay=tk.Label(self, text='Delay [ms]:', width=self.COL_WIDTH,  name='lblDelay')
        self.lblDelay.grid(column=0, row=4, sticky='ew')
        self.txtDelay=tk.Entry(self, text='10', width=self.COL_WIDTH, name='txtDelay', textvariable=self.model.delay_var())
        self.txtDelay.grid(column=1, row=4, sticky='ew')
        #row5
        self.lblDelay=tk.Label(self, text='Travel [mm]:', width=self.COL_WIDTH,  name='lblTravel_mm')
        self.lblDelay.grid(column=0, row=6, sticky='ew')
        self.txtDelay=tk.Entry(self, text='10', width=self.COL_WIDTH, name='txtTravel_mm', textvariable=self.model.travel_mm_var())
        self.txtDelay.grid(column=1, row=6, sticky='ew')
        #row7
        self.btnShowFileList=tk.Button(self, text='Start printing', width=self.COL_WIDTH,  command=self.start_printing, name='btnStartPrinting')
        self.btnShowFileList.grid(column=0, row=7, sticky='ew')
        
        for widget in self.winfo_children():
            widget.grid(padx=5, pady=3)
        # variables
        self.boolOverride = tk.BooleanVar(self, name='bool_override', value=True)

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

    def show_file_list(self):
        """Show the file list in a widnow

        TODO: this spawns a new window every time the button is pressed 
              I shoudl replace it with a constant file
        """        
        root = tk.Toplevel()
        root.geometry('200x100')
        root.resizable(True, True)
        root.title('Listbox')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # create a list box
        basenames = [x.name for x in self.FileList]

        var_image_filenames = tk.StringVar(value=basenames)

        listbox = tk.Listbox(
            root,
            listvariable=var_image_filenames,
            height=6,
            selectmode='extended')

        listbox.grid(
            column=0,
            row=0,
            sticky='nwes'
        )

    def start_printing(self):

        # logging.error('NOT IMPLEMENTED YET')
        self.master.control.start_printing()


class App_DLPcontrol(tk.Tk):

    def __init__(self):
        super().__init__()

        # self.protocol('WM_DELETE_WINDOW', self.onclosing) # protocol handler
        self.geometry('300x300+100+100')
        self.title('DLP Printer Dashboard - IESL')


        self._create_widgets()


    def _create_widgets(self):
        # place a button on the root window
        tk.Button(self,
                text='Motor Controls',
                command=self.toggle_motorcontrol_visibility).grid(row=0, column=0)
        
        tk.Button(self,
                text='Image Projection',
                command=self.toggle_image_visibility).grid(row=0, column=1)
        

        ## row 1
        self.DashBoard = FrameDashboard(self)
        self.DashBoard.grid(column=0, row=1, columnspan=2, sticky='nesw')

        ## row 2
        tk.Button(self,
                text='Show image',
                command=self.testing_show_image).grid(row=2, column=0)

            
    def testing_show_image(self):
        """TODO I should remove this and replace it with a proper code.
        """        
        pilimage = Image.open("src/sample_data/Barnard_33_bw.png")
        self._tlImageProjection.update_canvas(pilImage=pilimage)


    def toggle_motorcontrol_visibility(self):
        self.update()
        if self._tlMotorControlWindow.winfo_viewable():
            self._tlMotorControlWindow.withdraw()
        else:
            self._tlMotorControlWindow.deiconify()

        # window.grab_set()  # this block 
    def toggle_image_visibility(self):
        self.update()
        if self._tlImageProjection.winfo_viewable():
            self._tlImageProjection.withdraw()
        else:
            self._tlImageProjection.deiconify()
        # window.grab_set()  # this block 

if __name__ == "__main__":

    app = App_DLPcontrol()
    app.mainloop()