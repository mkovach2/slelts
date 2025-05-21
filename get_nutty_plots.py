# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
    "General - Products/+NewFileSystem/Device Components/Grating Coupler/"

csv_in_path = lonj +\
    "20250519_apodized_+8_g2f11/stage_1/grouped/no_sweep = 1.csv"

graphs_ratio = np.array((2,1)) # num rows, num columns

plt.style.use("seaborn-v0_8")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    # deeta = pd.read_csv(csv_in_path, index_col = 0)
    deeta = np.loadtxt(csv_in_path, delimiter = ',', skiprows = 1)
    with open(csv_in_path, "r") as ci:
        uid_row = ci.readline().split(',')
    
    # allmax = int(np.max(deeta[:,1:])) + 1
    allmin = int(np.min(deeta[:,1:])) - 1
    
    num_graphs = np.shape(deeta)[1] - 1
    tru_ratio = (np.around((num_graphs/np.product(graphs_ratio))**0.5 * graphs_ratio)).astype(int)
    if np.product(tru_ratio) < num_graphs:
        tru_ratio[np.argmax(tru_ratio)] += 1
    
    fig, axs = plt.subplots(
        tru_ratio[0],
        tru_ratio[1],
        gridspec_kw={"wspace": 0.5, "hspace": 0.5}
    )
    
    for col in range(num_graphs):
        axs[col // tru_ratio[1], col % tru_ratio[1]].plot(deeta[:,0], deeta[:,col + 1])
        axs[col // tru_ratio[1], col % tru_ratio[1]].set(
            title = uid_row[col + 1],
            ylim = (allmin, 0)
        )
        
