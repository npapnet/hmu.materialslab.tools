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
# %%
# loading the analysis result file

grid_listres = pydic.read_dic_file(result_file='result.dic', 
            interpolation='spline', 
            strain_type='cauchy', 
            save_image=True, 
            scale_disp=10, 
            scale_grid=25, 
            meta_info_file='img_png/meta-data.txt')

# %%

last_grid = grid_listres[100]
assert isinstance(last_grid, grid)
last_grid.plot_field(last_grid.strain_xx, 'xx strain')
last_grid.plot_field(last_grid.strain_yy, 'yy strain')
plt.show()

# %%
last_grid.reference_image
# %%
print(last_grid.size_x)
print(last_grid.size_y)
print(last_grid.size_y)
# %%

last_grid.strain_xx
# %%
last_grid.strain_xx.mean(), last_grid.strain_xx.std()
# %%
# show as image
plt.figure(figsize=(last_grid.size_x,last_grid.size_y))
plt.contourf(last_grid.strain_xx.T)
# %%
def obtainStrainCurve(grid_list)->pd.DataFrame:
    """this is a fucntion to obtain 

    Args:
        grid_list (list): List of grids 

    Returns:
        pd.DataFrame: Dataframe with "id", "image_fname", "e_xx", "e_xx_std","e_yy", "e_yy_std"
    """    
    adic =[]
    for j, gr in enumerate(grid_list):
        adic.append({"id":j+1, "image_fname": gr.image,
                     "e_xx":gr.strain_xx.mean(), "e_xx_std": gr.strain_xx.std(),
                     "e_yy":gr.strain_yy.mean(), "e_yy_std": gr.strain_yy.std()})

    df = pd.DataFrame(adic)
    return df

dfres = obtainStrainCurve(grid_list=grid_listres)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
dfres.to_excel(OUTPUT_DIR/"myexcel.xlsx")
#%% [markdown]
# TODO: see below
#
# At this point it is still necessary to add the data from _image_times.txt in the columns excel. 
# 
# this ought to be automatic. 


#%%
last_grid.meta_info



# %%
df.strain_xx.plot()
# %%
df[:-1].plot(kind="scatter", x='id', y='strain_xx', yerr='strain_xx_std')
# %%
