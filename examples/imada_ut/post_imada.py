#%% [markdown]
# This is a file for post-processing the pydic results

# %%
# ====== IMPORTING MODULES
from matplotlib import pyplot as plt
from scipy import stats
from npp_materialslab_tools.dic import pydic

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
