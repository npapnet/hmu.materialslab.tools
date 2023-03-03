# %%
# ====== IMPORTING MODULES
import pathlib
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt

from npp_materialslab_tools.dic import pydic
from npp_materialslab_tools.dic.pydicGrid import grid


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
# %%
# %%
df_dic = pd.read_excel(INFILE_DIC, index_col=0, usecols="B,D:G,I")
df_dic.head()
# %%
time_offset = 1.7
fig, axs = plt.subplots(ncols=1,nrows=1,sharex=True)
axs = [axs]
axs[0].plot(df_ut.time_s,df_ut.force_N/df_ut.force_N.max(), '.', label ="Normalised Force")
axs[0].plot(df_dic["elapsed time"][:-1]-time_offset, df_dic.e_xx[:-1]/df_dic.e_xx[:-1].max(), '.',label ="Normalised strain ")
plt.xlabel("Time (s)")
plt.title(f"Normalised Forces (from Imada) and Strains (from dic)\n Used to determine time offset: {time_offset} (s)")
# %%
fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)

axs[0].plot(df_ut.time_s,df_ut.force_N, '.', label ="Normalised Force")
axs[1].plot(df_dic["elapsed time"][:-1]-time_offset, df_dic.e_xx[:-1], '.',label ="Normalised strain ")
axs[1].set_xlabel("Time (s)")
axs[0].set_ylabel("Force (N)")
axs[1].set_ylabel("Strain $e_{xx}$ ()")

# plt.title("Normalised Forces (from Imada) and Strains (from dic)\n Used to match the correct time offset")

# %%
