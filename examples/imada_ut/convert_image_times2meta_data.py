#%%

# this is for converting the _images_times.txt to meta-data.txt
#%%
import pandas as pd
import pathlib
DATADIR = pathlib.Path('img')
INPUTFILE = DATADIR /"_image_times.txt"
OUTPUTFILE = DATADIR /"meta-data.txt"

# %%
df = pd.read_csv(INPUTFILE, delimiter="\t", header=None, names=['ImgNo', "Timestamp", 'ElapsedTime'])

# %%
df.columns 
df.ImgNo
# %%
df['filename'] = df.ImgNo.apply(lambda x: f"Cam_{x:05d}.bmp")

# %%
df = df.loc[:, ['filename', "ElapsedTime"]]
# %%
df['force'] = df['ElapsedTime'].round(decimals=0)
# %%
df.columns= ['file', 'time(s)', 'force(N)']
df
# %%
df.to_csv(OUTPUTFILE, index=False, sep='\t')
# %%
