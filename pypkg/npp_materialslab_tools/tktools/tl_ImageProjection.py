import logging
import pathlib
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk


class TLImageProjection(tk.Toplevel):
    """top level window to project the image

    can maximize window without border (in windows)

    Args:

    """    
    fullScreen = False
    def __init__(self, parent, image_size=(800, 600)):
        super().__init__(parent)

        self._img_size = image_size 
        self.protocol('WM_DELETE_WINDOW', self.withdraw)
        # windows only (remove the minimize/maximize button)
        self.attributes('-toolwindow', True)
        self.resizable(1, 1)

        self.title('Image Projection Window (F11:maximize, Esc: Emergency Stop)')
        self.geometry(f'{image_size[0]}x{image_size[1]}')

        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.__create_widgets()

    @property
    def imgsize_x(self):
        return self._img_size[0]
    @property   
    def imgsize_y(self):
        return self._img_size[1]

    def __create_widgets(self):
        # create the input frame
        # input_frame = InputFrame(self)
        # input_frame.grid(column=0, row=1)

        # set bindings
        self.bind("<F11>", func=self.toggleFullScreen)
        self.bind("<Alt-Return>", func=self.toggleFullScreen)
        self.bind("<Escape>", func=self.activateEmergencyStop)

        self.canvas = tk.Canvas(self, width=self.imgsize_y, height=self.imgsize_x,  highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='black')

    def update_canvas(self, pilImage):
        """main function. This requires a pilImage 

        Usage 
            pilImage  =  Image.open(IMAGE_NAME)
            self.update_canvas(pilImage=pilImage)

        Args:
            pilImage (_type_): _description_
        """        
        self.image = ImageTk.PhotoImage(pilImage)
        self.imagesprite = self.canvas.create_image(self.imgsize_y / 2, self.imgsize_x / 2, image=self.image)
        # self.imagesprite = self.canvas.create_image(0 , 0, image=self.image)
        self.canvas.image = self.imagesprite

    def toggleFullScreen(self, event):
        if self.fullScreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullScreen = True

        # Store geometry for reset
        self._geometry_old = self.geometry()

        # Hides borders and make truly fullscreen
        self.overrideredirect(True)

        # Maximize window (Windows only). Optionally set screen geometry if you have it
        self.state("zoomed")

        # # code for linux 
        # self.geometry = self.geometry()
        # # Hides borders and make truly fullscreen
        # self.overrideredirect(True)
        # # Maximize window (Windows only). Optionally set screen geometry if you have it
        # if sys.platform.startswith('linux'):
        #     # this should work on linux
        #     self.attributes('-zoomed', True)
        # else:
        #     # this should work on macos and windows
        #     self.state("zoomed")

    def deactivateFullscreen(self):
        self.fullScreen = False
        self.state("normal")
        self.geometry(self._geometry_old)
        self.overrideredirect(False)

        # code for linux compatibility
        # if sys.platform.startswith('linux'):
        #     # this should work on linux
        #     self.root.attributes('-zoomed', False)
        # else:
        #     # this should work on macos and windows
        #     self.root.state("normal")
        
        # self.root.geometry(self.geometry)
        # self.root.overrideredirect(False)

    def activateEmergencyStop(self,event):
        """activates the emergency stop
        """        
        logging.debug('Emergency stop Activated from Image Projection window')
        self.master.model.isEmergencyStopActivated = True