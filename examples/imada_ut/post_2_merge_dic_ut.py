# %%
# ====== IMPORTING MODULES
import pathlib
# from scipy import stats

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from npp_materialslab_tools.dic import pydic
from npp_materialslab_tools.dic.pydicGrid import grid
import logging
logging.basicConfig(level = logging.DEBUG)

OUTPUT_DIR = pathlib.Path("output")
INFILE_UT = OUTPUT_DIR/"1mm_100 overlap infill.csv"
INFILE_DIC = OUTPUT_DIR/"myexcel-withTimes.xlsx"

# %%

def read_imada_csv(INFILE, decimation:int=100)->pd.DataFrame:
    """Reads imada csv file and returns a decimated Dataframe

    wiht columns 	
        - force_N	
        - disp_mm	
        - time_s

    Args:
        INFILE (_type_): _description_
        decimation (int, optional): _description_. Defaults to 100.

    Returns:
        _type_: _description_
    """
    COLNAMES = ["force_N", "disp_mm", "time_s"]
    df_ut_meta = pd.read_csv(INFILE, sep="=",nrows=13, header=None, index_col=0, names=["Description", "Value"])
    RECORDING_DT = float(df_ut_meta.loc['RECORDING RATE ','Value'].strip()[:-1])

    df_ut = pd.read_csv(INFILE, skiprows=13, names = ["Force (N)", "Disp (mm)"])
    df_ut['Time (s)'] = df_ut.index*RECORDING_DT
    # df_ut.head()
    df_decimated = df_ut.iloc[::100,:]
    df_decimated.columns = COLNAMES
    return df_decimated

df_ut = read_imada_csv(INFILE=INFILE_UT, decimation=100)
# %%

# %%
df_ut.plot.scatter(x="time_s", y="force_N")
# %%[markdown]
# Read dic file
# %%

df_dico = pd.read_excel(INFILE_DIC, index_col=0, usecols="B,D:G,I")
df_dico.head()

#%%
# Select subset
index_start = 0
index_end = -1
df_dic = df_dico.iloc[index_start:index_end]
df_dic.tail()
# %%
time_offset = 1.7
df_dic["time_synced"] = df_dic["elapsed time"]-time_offset
fig, axs = plt.subplots(ncols=1,nrows=1,sharex=True)
axs = [axs]
axs[0].plot(df_ut.time_s,df_ut.force_N/df_ut.force_N.max(), '.', label ="Normalised Force")
axs[0].plot(df_dic["time_synced"][:-1], df_dic.e_xx[:-1]/df_dic.e_xx[:-1].max(), '.',label ="Normalised strain ")
plt.xlabel("Time (s)")
plt.title(f"Normalised Forces (from Imada) and Strains (from dic)\n Used to determine time offset: {time_offset} (s)")
# %%
fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)

axs[0].plot(df_ut.time_s,df_ut.force_N, '.', label ="Normalised Force")
axs[1].plot(df_dic["time_synced"][:-1], df_dic.e_xx[:-1], '.',label ="Normalised strain ")
axs[1].set_xlabel("Time (s)")
axs[0].set_ylabel("Force (N)")
axs[1].set_ylabel("Strain $e_{xx}$ ()")

# plt.title("Normalised Forces (from Imada) and Strains (from dic)\n Used to match the correct time offset")

# %%
index_td = pd.to_timedelta(df_dic['time_synced'], unit ="s")
# index_td = pd.to_datetime(df_dic['time_synced'], unit ="s")
df_dict = df_dic.set_index(index_td )
# %%
df_dict.resample('100ms',origin=0).interpolate('linear')
# %%


# %%
ts = np.arange(0,14,step=0.5)
exxs = np.interp(ts, df_dic['time_synced'],df_dic['e_xx'])
# %%
plt.plot(ts, exxs, ".")
plt.plot(df_dic['time_synced'], df_dic['e_xx'], ".")
# %%
def resample_dic_df(df_dic:pd.DataFrame,  ts:np.ndarray|str)->pd.DataFrame:
    """resamples the 

    Args:
        df_dic (pd.DataFrame): DIC Dataframe 
        ts (np.ndarray): new time vector. eg: np.arange(0,14,step=0.5).

    Returns:
        pd.DataFrame: new DataFrame with results 
    """
    dss = []
    for columnname in df_dic.iloc[:,:4]:

        interp_data = np.interp(ts, df_dic['time_synced'],df_dic[columnname])
        ds_new = pd.Series(interp_data, index = ts, name=columnname)
        dss.append(ds_new)
    res_df = pd.concat(dss,axis=1)
    return res_df 


ts = np.arange(0, df_dic['time_synced'].max(), step=0.5)
df_dicrs = resample_dic_df(df_dic=df_dic, ts=ts)
# %%
df_ut
# %%
def resample_ut(df_ut:pd.DataFrame,  ts:np.ndarray|str)->pd.DataFrame:
    """resamples the 

    Args:
        df_dic (pd.DataFrame): DIC Dataframe 
        ts (np.ndarray): new time vector. eg: np.arange(0,14,step=0.5).

    Returns:
        pd.DataFrame: new DataFrame with results 
    """
    dss = []
    for columnname in df_ut.iloc[:,:2]:
        logging.debug(columnname)
        interp_data = np.interp(ts, df_ut['time_s'],df_ut[columnname])
        ds_new = pd.Series(interp_data, index = ts, name=columnname)
        dss.append(ds_new)
    res_df = pd.concat(dss,axis=1)
    return res_df
df_utrs = resample_ut(df_ut=df_ut, ts=ts)


# %%
df_fin = pd.concat([df_utrs, df_dicrs],axis=1)
df_fin.to_excel(OUTPUT_DIR/'total_data.xlsx')
# %%
df_fin.plot.scatter(x='e_xx', y= 'force_N')
# %%
