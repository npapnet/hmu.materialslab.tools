#%%
import pathlib
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class TensileSpecimenDimensions():
    width_mm:float
    thickness_mm:float
    gauge_length_mm:float

    @property
    def csArea_mm2(self):
        """returns the cross-sectional area in mm2

        Returns:
            _type_: _description_
        """        
        return self.width_mm*self.thickness_mm
