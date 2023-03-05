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
# logging.basicConfig(level = logging.DEBUG)
logging.basicConfig(level = logging.ERROR)


TENSILEDATA_DIR = pathlib.Path("data_tensile")
INFILE_UT = TENSILEDATA_DIR/"1mm_5% overlap Infill.csv"
OUTPUT_DIR = pathlib.Path("output")
INFILE_DIC = OUTPUT_DIR/"myexcel.xlsx"

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

df_dico = pd.read_excel(INFILE_DIC, index_col=0, usecols="B,D:G,H")
df_dico.head()

#%%
# Select subset for dic-analysis
index_start = 0
index_end = -1
df_dic = df_dico.iloc[index_start:index_end]
df_dic.tail()
# %%
# I could use cross-correlation but this would require similar timestep. 
def plot_synced_graph(time_offset, dic_df:pd.DataFrame, ut_df:pd.DataFrame):
    """plots the dic and tensile data to see if they correlate well
    
    Two plots are made:
    - one plot with the normalised force and the normalised strain
    - plot:
        - the force diff normalised wrt abs(max(force diff)
        - the strain diff normalised wrt abs(max(strain diff))

    Args:
        time_offset (float): Time offset in s
        dic_df (pd.DataFrame): dataframe obtained from dic
        ut_df (pd.DataFrame): dataframe obtained from imada
    """    
    # time_offset = 1.55
    dic_df["time_synced"] = dic_df["time(s)"]-time_offset
    # axs = [axs]
    ts_ut = ut_df.time_s
    Fs_ut = ut_df.force_N
    ts_dic = dic_df["time_synced"]
    exx_dic = dic_df.e_xx
    fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)

    # plot 1
    axs[0].plot(ts_ut, Fs_ut/Fs_ut.max(), '.', label ="Normalised Force")
    axs[0].plot(ts_dic[:-1], exx_dic[:-1]/exx_dic[:-1].max(), '.',label ="Normalised strain ")
    axs[0].set_title(f"Normalised Forces (from Imada) and Strains (from dic)\n Used to determine time offset: {time_offset} (s)")

    # plot 2 with normalised diffs (the  )
    axs[1].plot(ts_ut[:-1],np.abs(np.diff(Fs_ut))/np.abs(np.diff(Fs_ut)).max(), label ="force diff")
    axs[1].plot(ts_dic[:-1], np.abs(np.diff(exx_dic))/np.abs(np.diff(exx_dic)).max(),label ="Normalised strain ")
    axs[1].set_xlabel("Time (s)")

time_offset = 1.55
plot_synced_graph(time_offset, dic_df=df_dic, ut_df=df_ut)
# %%
fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)

axs[0].plot(df_ut.time_s,df_ut.force_N, '.', label ="Normalised Force")
axs[1].plot(df_dic["time_synced"][:-1], df_dic.e_xx[:-1], '.',label ="Normalised strain ")
axs[1].set_xlabel("Time (s)")
axs[0].set_ylabel("Force (N)")
# axs[1].set_ylabel("Strain $e_{xx}$ ()")

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
