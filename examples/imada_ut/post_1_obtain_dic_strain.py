#%% [markdown]
# This is a file for post-processing the pydic results


# %%
# ====== IMPORTING MODULES
import pathlib
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt

from npp_materialslab_tools.dic import pydic
from npp_materialslab_tools.dic.pydicGrid import grid


OUTPUT_DIR = pathlib.Path("output")
UTDATA = pathlib.Path("data_tensile")/"1mm_5% overlap Infill.csv"
IMG_DIR = pathlib.Path("img_png")
DIC_ANALYSIS_OUTPUT = OUTPUT_DIR/'result.dic'
DIC_EXCEL_OUTPUT = OUTPUT_DIR/"myexcel.xlsx"
DIC_META_DATA_FILE = IMG_DIR/'_meta-data.txt'
# %%
# loading the analysis result file

grid_listres = pydic.read_dic_file(result_file=DIC_ANALYSIS_OUTPUT, 
            interpolation='spline', 
            strain_type='cauchy', 
            save_image=True, 
            scale_disp=10, 
            scale_grid=25, 
            meta_info_file=DIC_META_DATA_FILE)

# %%

last_grid = grid_listres[100]
assert isinstance(last_grid, grid)
last_grid.plot_field(last_grid.strain_xx, 'xx strain')
last_grid.plot_field(last_grid.strain_yy, 'yy strain')
plt.show()
# last_grid.reference_image
# last_grid.strain_xx
# last_grid.strain_xx.mean(), last_grid.strain_xx.std()

# print(last_grid.size_x)
# print(last_grid.size_y)
# print(last_grid.size_y)
# last_grid.meta_info

# %%
# show as image
plt.figure(figsize=(last_grid.size_x,last_grid.size_y))
plt.contourf(last_grid.strain_xx.T)
# %%
def obtainStrainCurve(grid_list)->pd.DataFrame:
    """this is a function to obtain one data point per image

    Args:
        grid_list (list): List of grids 

    Returns:
        pd.DataFrame: Dataframe with "id", "image_fname", "e_xx", "e_xx_std","e_yy", "e_yy_std"
    """    
    adic =[]
    for j, gr in enumerate(grid_list):
        adic.append({"id":j+1, "file": pathlib.Path(gr.image).name,
                     "e_xx":gr.strain_xx.mean(), "e_xx_std": gr.strain_xx.std(),
                     "e_yy":gr.strain_yy.mean(), "e_yy_std": gr.strain_yy.std()})

    # dfres.image_fname = dfres.image_fname.apply(lambda x:pathlib.Path(x).name)
    df = pd.DataFrame(adic)
    return df

df_dic = obtainStrainCurve(grid_list=grid_listres)

#%% 
# Read the data from the *_meta-data.txt* 
df_img_meta = pd.read_csv(DIC_META_DATA_FILE, sep="\t")

# merge the two files
df_dic_tot = pd.merge(df_dic,df_img_meta,  how="inner", on="file")
#%%
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df_dic_tot.to_excel(DIC_EXCEL_OUTPUT)
#%% [markdown]
# TODO: see below
#
# At this point it is still necessary to add the data from _image_times.txt in the columns excel. 
# 
# this ought to be automatic. 


# %%
df_dic.e_xx.plot()
# %%
df_dic[:-1].plot(kind="scatter", x='id', y='e_xx', yerr='e_xx_std')
# %%
