#%%
import npp_materialslab_tools as mpt
import matplotlib.pyplot as plt

#%%
if __name__ == "__main__":

    # snap_cursor = ElasticityModulusCalculator('../Results/20190327-tests/D00_02.xlsx')
    snap_cursor = mpt.ElasticityModulusCalculatorGUI()

    plt.show()