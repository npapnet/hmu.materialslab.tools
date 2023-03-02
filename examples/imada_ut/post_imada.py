#%% [markdown]
# This is a file for post-processing the pydic results

# %%
# ====== IMPORTING MODULES
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
from npp_materialslab_tools.dic import pydic
from npp_materialslab_tools.dic.pydicGrid import grid

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
last_grid.plot_field(last_grid.strain_xx, 'xx strain')
last_grid.plot_field(last_grid.strain_yy, 'yy strain')
plt.show()

# %%
assert isinstance(last_grid, grid)
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
adic =[]
for j, gr in enumerate(grid_listres):
    adic.append({"id":j+1, "strain_xx":gr.strain_xx.mean(), "strain_xx_std": gr.strain_xx.std()})

df = pd.DataFrame(adic)
#%%
last_grid.meta_info



# %%
df.strain_xx.plot()
# %%
df[:-1].plot(kind="scatter", x='id', y='strain_xx', yerr='strain_xx_std')
# %%
