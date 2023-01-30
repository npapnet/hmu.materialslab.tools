#%%
import numpy as np
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pathlib

#%%


@dataclass
class DCLoadDisplacement():
    displacement: np.array
    load: np.array


# %%
FNAME = pathlib.Path('data')/"new XY 0 ABS_CNT 2%.csv"

# %%
df = pd.read_csv(filepath_or_buffer=FNAME, skiprows=13, names=[ 'load','displacement'])
# %%
df_mean = pd.concat( [
        df.groupby('displacement').mean().rename(columns={"load": 'load_avg'}), 
        df.groupby('displacement').std().rename(columns={"load": 'load_std'}),
        df.groupby('displacement').min().rename(columns={"load": 'load_min'}), 
        df.groupby('displacement').max().rename(columns={"load": 'load_max'})],axis=1)
df_mean.eval('ci2sdm = load_avg - 2*load_std', inplace=True)
df_mean.eval('ci2sdp = load_avg + 2*load_std', inplace=True)
df_mean.head()
# %%
fig, ax = plt.subplots()
ax.plot(df_mean.index, df_mean.iloc[:,0].values, alpha=.1, label= 'avg')
ax.plot(df_mean.index, df_mean.iloc[:,2:].values, alpha=.3, label=df_mean.iloc[:,2:].columns)# ['min', 'max', 'ci:2SD','c2'])
# plt.ylim([155,165])
# plt.xlim([4,8])
ax.legend()
#%%
# df_mean.plot()
# %%
# %%
# %%
#%%
# 3, for example, is tolerance for picker i.e, how far a mouse click from
# the plotted point can be registered to select nearby data point/points.

def on_pick(event):
    global points
    line = event.artist
    xdata, ydata = line.get_data()
    print('selected point is:',np.array([xdata, ydata]).T)

cid = fig.canvas.mpl_connect('pick_event', on_pick)
# %%

plt.show()
