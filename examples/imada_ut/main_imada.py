# this is based on 2017 Damien ANDRE pydic example
# 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pydic, a free digital correlation suite for computaing strain fields
#
# Author :  - Damien ANDRE, SPCTS/ENSIL-ENSCI, Limoges France
#             <damien.andre@unilim.fr>
#
# Copyright (C) 2017 Damien ANDRE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



# ====== INTRODUCTION
# The tensile example shows how to use the pydic module to compute
# the young's modulus and the poisson's ratio from picture captured
# during a tensile test. The loading were recorded during the test
# and the values are stored in the meta-data file (see 'img/meta-data.txt').
#
# Note that :
#  - pictures of the tensile test are located in the 'img' directory
#  - for a better undestanding, please refer to the 'description.png' file
#    that describes the tensile test 




# ====== IMPORTING MODULES
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import cv2
from npp_materialslab_tools.dic import pydic




#  ====== RUN PYDIC TO COMPUTE DISPLACEMENT AND STRAIN FIELDS (STRUCTURED GRID)
correl_wind_size = (80,80) # the size in pixel of the correlation windows
correl_grid_size = (20,20) # the size in pixel of the interval (dx,dy) of the correlation grid


# read image series and write a separated result file 
# pydic.init('./img/*.bmp', correl_wind_size, correl_grid_size, "result.dic")


# # and read the result file for computing strain and displacement field from the result file 
# pydic.read_dic_file('result.dic', interpolation='spline', strain_type='cauchy', save_image=True, scale_disp=10, scale_grid=25, meta_info_file='img/meta-data.txt')


#  ====== OR RUN PYDIC TO COMPUTE DISPLACEMENT AND STRAIN FIELDS (WITH UNSTRUCTURED GRID OPTION)
# note that you can't use the 'spline' or the 'raw' interpolation with unstructured grids 
# please uncomment the next lines if you want to use the unstructured grid options instead of the aligned grid
pydic.init('./img/*.png', 
           win_size_px=correl_wind_size, 
           grid_size_px=correl_grid_size, 
           result_file="result.dic", 
           unstructured_grid=(20,5))
pydic.read_dic_file(result_file='result.dic', 
                    interpolation='cubic', 
                    save_image=True, 
                    scale_disp=10, 
                    scale_grid=25, 
                    meta_info_file='img/meta-data.txt')



#  ====== RESULTS
# Now you can go in the 'img/pydic' directory to see the results :
# - the 'disp', 'grid' and 'marker' directories contain image files
# - the 'result' directory contain raw text csv file where displacement and strain fields are written  



# ======= STANDARD POST-TREATMENT : STRAIN FIELD MAP PLOTTING
# the pydic.grid_list is a list that contains all the correlated grids (one per image)
# the grid objects are the main objects of pydic  
last_grid = pydic.grid_list[-1]
last_grid.plot_field(last_grid.strain_xx, 'xx strain')
last_grid.plot_field(last_grid.strain_yy, 'yy strain')
plt.show()




# ======== NON-STANDARD POST-TREATMENT : COMPUTE ELASTIC CONSTANTS (E & Nu)

# extract force from meta-data file 
force = np.array([float(x.meta_info['force(N)']) for x in pydic.grid_list])

# compute the main normal stress with this force 
sample_width     = 0.012
sample_thickness = 0.002
stress = force/(sample_width * sample_thickness)


# now extract the main average strains on xx and yy
# - first, we need to reduce the interest zone where the average values are computed

test = pydic.grid_list[0].size_x/4

x_range = range(int(pydic.grid_list[0].size_x/4), int(3*pydic.grid_list[0].size_x/4)) 
y_range = range(int(pydic.grid_list[0].size_y/4), int(3*pydic.grid_list[0].size_y/4))
# - use grid.average method to compute the average values of the xx and yy strains
ave_strain_xx = np.array([grid.average(grid.strain_xx, x_range, y_range) for grid in pydic.grid_list])
ave_strain_yy = np.array([grid.average(grid.strain_yy, x_range, y_range) for grid in pydic.grid_list])



# now compute Young's modulus thanks to scipy linear regression
E, intercept, r_value, p_value, std_err = stats.linregress(ave_strain_xx, stress)
# and compute Poisson's ratio thanks to scipy linear regression
Nu, intercept, r_value, p_value, std_err = stats.linregress(ave_strain_xx, -ave_strain_yy)



# and print results !
print ("\nThe computed elastic constants are :")
print ("  => Young's modulus E={:.2f} GPa".format(E*1e-9))
print ("  => Poisson's ratio Nu={:.2f}".format(Nu))



# enjoy !
# damien.andre@unilim.fr
