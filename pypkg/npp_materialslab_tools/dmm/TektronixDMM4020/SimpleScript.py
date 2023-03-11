#%%
import serial
import time
from typing import TextIO
# # %%


# %%
def record_from_DMM4020(
        fname:str|TextIO, n:int, 
        fs:float=1, 
        port:str="COM1", baudrate:int= 19200,
        verbose:bool=1):
    """Starts a recording session for a Tektronix DMM4020

    Args:
        fname (str|typing.TextIO) : Filenama or fileobject.
        n (int): number of data points (The duration in [seconds] is n/fs. )
        fs (float, optional): Sampling frequency in Hz. Defaults to 1.
        port (str, optional): . Defaults to "COM1".
        baudrate (int, optional): Baud rate. Defaults to 19200.
        verbose (bool, optioal): More verbose output. Defaults to True.
    """    
    # TODO SCPI Commands for fast rate
    # https://forum.tek.com/viewtopic.php?t=138561
    if isinstance(fname , "str"):
        file_object = open(fname, 'w')
    elif isinstance(fname , TextIO):
        file_object = fname
    dt = 1/fs
    # Append 'hello' at the end of file
    with serial.Serial(port=port,  baudrate=baudrate) as ser:
        for j in range(n):
            ser.write("val?\n".encode())
            data = ser.read_all().decode()
            data=data.split('\r')[0]
            file_object.write(f"{j}: {data}\n")
            if(verbose):
                print(f"{j}: {data}")
            time.sleep(dt)
    # Close the file
    file_object.close()



#%%
class TekDMM4020():
    """Class for controlling the TekDMM4020
    """    
    pass