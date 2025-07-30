# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if True:
    lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
        "General - Products/+NewFileSystem/Device Components/Grating Coupler/"
        
    csv_in_path = lonj +\
        "20250602_apo_+8_g2f11_o_band/ov_curiosity_1_pd1/jmp_data_11835688.csv"

else:
    csv_in_path = "T:/Device Components/Grating Coupler/"+\
        "20250519_apodized_+8_g2f11/stage_2_xe/for_graphing/grouped/no_sweep = 1.csv"


# graphs_ratio = np.array((2.0,1.0)) # num rows, num columns

# # top_margin_percent = 0.95
# # top_margin_percent = 0.80 # good for column-favoring ratios like (1, 7)
# top_margin_percent = 0.965 # a good top for graphs_ratio = (2,1)

# plt.style.use("bmh")
# # plt.style.use("seaborn-v0_8")

combo_to_use = "o_band" # None to not use a preset combo


if __name__ == "__main__":
    
    deeta = pd.read_csv(csv_in_path)
    
    # allmax = int(np.max(deeta[:,1:])) + 1
    allmin = -60
    
    fig,ax = plt.