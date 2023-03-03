#%%

# this is for converting the _images_times.txt to meta-data.txt
#%%
import pandas as pd
import pathlib
DATADIR = pathlib.Path('img-bmp')
INPUTFILE = DATADIR /"_image_times.txt"
OUTPUTFILE = DATADIR /"meta-data.txt"


# %%
def conversion_procedure(in_fname:pathlib.Path,out_fname:pathlib.Path, img_ext:str="png"):
    """coverts the output file from labview to the "meta-data.txt" required by pydic

    Args:
        in_fname (pathlib.Path): input filename
        out_fname (pathlib.Path): output filename 
        img_ext (str): Image file extension 
    """    
    dfcols = ['ImgNo', "Timestamp", 'ElapsedTime']
    df = pd.read_csv(in_fname, delimiter="\t", header=None, names=dfcols)

    df['filename'] = df.ImgNo.apply(lambda x: f"Cam_{x:05d}.{img_ext}")

    df = df.loc[:, ['filename', "ElapsedTime"]]
    # The following mocks up the force 
    df['force'] = df['ElapsedTime'].round(decimals=0)

    df.columns= ['file', 'time(s)', 'force(N)']

    df.to_csv(out_fname, index=False, sep='\t')

conversion_procedure(in_fname=INPUTFILE, out_fname=OUTPUTFILE)
# %%
