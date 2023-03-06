#%%
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


# ====== IMPORTING MODULES
# import cv2
import pathlib

import numpy as np
from matplotlib import pyplot as plt
from npp_materialslab_tools.dic import pydic
from npp_materialslab_tools.dic.misc import convert_labview_to_metainfo
# from scipy import stats



#%% [markdown]
# #  INTRODUCTION
# The tensile example shows how to use the pydic module to compute
# the young's modulus and the poisson's ratio from picture captured
# during a tensile test. The loading were recorded during the test
# and the values are stored in the meta-data file (see 'img/meta-data.txt').
#
# Note that :
#  - pictures of the tensile test are located in the 'img' directory
#  - for a better undestanding, please refer to the 'description.png' file
#    that describes the tensile test 


# %% 
#Convert Labview output to meta data that pydic can include

IMG_DIR = pathlib.Path('img_png')
OUTPUT_DIR = pathlib.Path('output')
LABVIEWFILE = IMG_DIR /"_image_times.txt"
DIC_META_FILE = IMG_DIR /"_meta-data.txt"

convert_labview_to_metainfo(in_fname=LABVIEWFILE, out_fname=DIC_META_FILE)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
#%%

#  ====== RUN PYDIC TO COMPUTE DISPLACEMENT AND STRAIN FIELDS (STRUCTURED GRID)
correl_wind_size = (80,80) # the size in pixel of the correlation windows
correl_grid_size = (20,20) # the size in pixel of the interval (dx,dy) of the correlation grid

# correl_wind_size = (16,16) # the size in pixel of the correlation windows
# correl_grid_size = (4,4) # the size in pixel of the interval (dx,dy) of the correlation grid

# area_of_interest = [(307, 114), (596, 189)]
area_of_interest = None


# read image series and write a separated result file 
pydic.init(image_pattern='./img_png/*.png', 
    win_size_px=correl_wind_size, 
    grid_size_px=correl_grid_size, 
    area_of_interest= area_of_interest,
    result_file=OUTPUT_DIR/"result.dic")

#%%
# # and read the result file for computing strain and displacement field from the result file 
grid_listres = pydic.read_dic_file(result_file=OUTPUT_DIR/'result.dic', 
            interpolation='spline', 
            strain_type='cauchy', 
            save_image=True, 
            scale_disp=10, 
            scale_grid=25, 
            meta_info_file=IMG_DIR/'_meta-data.txt')


#  ====== OR RUN PYDIC TO COMPUTE DISPLACEMENT AND STRAIN FIELDS (WITH UNSTRUCTURED GRID OPTION)
# note that you can't use the 'spline' or the 'raw' interpolation with unstructured grids 
# please uncomment the next lines if you want to use the unstructured grid options instead of the aligned grid
# pydic.init('./img_png/*.png', 
#            win_size_px=correl_wind_size, 
#            grid_size_px=correl_grid_size, 
#            result_file="result.dic", 
#            unstructured_grid=(20,5))

# pydic.read_dic_file(result_file='result.dic', 
#                     interpolation='cubic', 
#                     save_image=True, 
#                     scale_disp=10, 
#                     scale_grid=25, 
#                     meta_info_file='img/meta-data.txt')

#%%
