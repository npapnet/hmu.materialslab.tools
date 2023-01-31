#%%
import numpy as np
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pathlib



# @dataclass
class TestingData():
    """package for loading testing data from M2 machine
    #TODO Find machine details

    """    
    
    def __init__(self, fname):
        self._fname = fname
        self._rawdata = pd.read_csv(filepath_or_buffer=fname, skiprows=13, names=[ 'load','displacement'])
        self._preprocess_data()

    def _preprocess_data(self):
        """preprocesses data
        
        creates calculation for each displacement point:
        - load average
        - load std
        - load min 
        - load max
        - ci for +/- 2SD
        """        
        df = self._rawdata
        df_mean = pd.concat( [
            df.groupby('displacement').mean().rename(columns={"load": 'load_avg'}), 
            df.groupby('displacement').std().rename(columns={"load": 'load_std'}),
            df.groupby('displacement').min().rename(columns={"load": 'load_min'}), 
            df.groupby('displacement').max().rename(columns={"load": 'load_max'})],axis=1)
        df_mean.eval('ci2sdm = load_avg - 2*load_std', inplace=True)
        df_mean.eval('ci2sdp = load_avg + 2*load_std', inplace=True)
        self._data = df_mean

    @property
    def load_displacement_avg_data(self):
        """returns the displacement and average data

        Returns:
            _type_: _description_
        """        
        return self._data.iloc[:,0].reset_index()

    @property
    def data_avg_table(self):
        return self._data


#%%
if __name__ == '__main__':
    FNAME = pathlib.Path('data')/"new XY 0 ABS_CNT 2%.csv"
    # %%
    td = TestingData(fname=FNAME)

    # %%

    # %%
    df_mean = td.data_avg_table
    fig, ax = plt.subplots()
    ax.plot(df_mean.index, df_mean.iloc[:,0].values, alpha=.1, label= 'avg')
    ax.plot(df_mean.index, df_mean.iloc[:,2:].values, alpha=.3, label=df_mean.iloc[:,2:].columns)# ['min', 'max', 'ci:2SD','c2'])
    # plt.ylim([155,165])
    # plt.xlim([4,8])
    ax.legend()
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
