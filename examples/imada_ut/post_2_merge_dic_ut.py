# %%
# ====== IMPORTING MODULES
import pathlib
# from scipy import stats

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from npp_materialslab_tools.dic import pydic
from npp_materialslab_tools.dic.pydicGrid import grid
from npp_materialslab_tools.dic.misc import resample_dic_df, resample_ut, plot_synced_graph
from npp_materialslab_tools.testing_machine.imada.imada_tools import read_imada_csv
import logging
# logging.basicConfig(level = logging.DEBUG)
logging.basicConfig(level = logging.ERROR)


TENSILEDATA_DIR = pathlib.Path("data_tensile")
INFILE_UT = TENSILEDATA_DIR/"1mm_100 overlap infill.csv"
OUTPUT_DIR = pathlib.Path("output")
INFILE_DIC = OUTPUT_DIR/"myexcel.xlsx"
RESULT_XLSX_FNAME = OUTPUT_DIR/'total_data.xlsx'


# %%
df_ut = read_imada_csv(fname=INFILE_UT, decimation=100)
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

time_offset = 1.3
plot_synced_graph(time_offset, dic_df=df_dic, ut_df=df_ut)
# %%
fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)

axs[0].plot(df_ut.time_s,df_ut.force_N, '.', label ="Normalised Force")
axs[1].plot(df_dic["time_synced"][:-1], df_dic.e_xx[:-1], '.',label ="Normalised strain ")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("$e_{xx}$ ()")
axs[0].set_ylabel("Force (N)")
# axs[1].set_ylabel("Strain $e_{xx}$ ()")

# plt.title("Normalised Forces (from Imada) and Strains (from dic)\n Used to match the correct time offset")


# %% This is the base of the resampling using the np.interp function
ts = np.arange(0,14,step=0.5)
exxs = np.interp(ts, df_dic['time_synced'],df_dic['e_xx'])
fig, ax = plt.subplots(ncols=1,nrows=1)
ax.plot(ts, exxs, ".", label="interp")
ax.plot(df_dic['time_synced'], df_dic['e_xx'], ".", alpha=0.3, label="original")
ax.legend()
ax.set_title("Interpolation Verification ")
# %%[markdown]
# ## Create a common time vector for both Dataframes
#%%

ts = np.arange(0, df_dic['time_synced'].max(), step=0.5)
df_dicrs = resample_dic_df(df_dic=df_dic, ts=ts)   # the DIC resampling
df_utrs = resample_ut(df_ut=df_ut, ts=ts) # the UT resampling

# %%  Concatenate the two dataframes (DIC, UT) and export to disk
df_fin = pd.concat([df_utrs, df_dicrs],axis=1)
df_fin.to_excel(RESULT_XLSX_FNAME)
# %%
df_fin.plot.scatter(x='e_xx', y= 'force_N')
# %%
