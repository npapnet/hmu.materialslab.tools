import pathlib
import pandas as pd

def read_imada_csv(fname:pathlib.Path|str, decimation:int=100)->pd.DataFrame:
    """Reads imada csv file and returns a decimated Dataframe

    with columns 	
        - force_N	
        - disp_mm	
        - time_s

    Args:
        fname (pathlib.Path|str): imada csv export (from z3a file)
        decimation (int, optional): reduce the data by the decimation factor. Defaults to 100.

    Returns:
        pd.DataFrame: a Dataframe containing columns = ["force_N", "disp_mm", "time_s"]
    """
    COLNAMES = ["force_N", "disp_mm", "time_s"]
    # obtain the meta data 
    df_ut_meta = pd.read_csv(fname, sep="=",nrows=13, header=None, index_col=0, names=["Description", "Value"])
    RECORDING_DT = float(df_ut_meta.loc['RECORDING RATE ','Value'].strip()[:-1])
    # obtain the dataframe of the test
    df_ut = pd.read_csv(fname, skiprows=13, names = ["Force (N)", "Disp (mm)"])
    df_ut['Time (s)'] = df_ut.index*RECORDING_DT
    # df_ut.head()
    df_decimated = df_ut.iloc[::decimation,:]
    df_decimated.columns = COLNAMES
    return df_decimated