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

if True:
    lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
        "General - Products/+NewFileSystem/Device Components/Grating Coupler/"
    
    csv_in_path = lonj +\
        "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/grouped/96678_thru_97182.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/86450_thru_87401.csv"
        # "20250602_apodized_+8_g2f11_o_band/vert_st3_o_band/grouped/84739_thru_85232.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st2_o_band/grouped/6692_thru_7240.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st1_o_band/grouped/no_sweep = 1.csv"
        
else:
    csv_in_path = "T:/Device Components/Grating Coupler/"+\
        "20250519_apodized_+8_g2f11/stage_2_xe/for_graphing/grouped/no_sweep = 1.csv"

graphs_ratio = np.array((2,1)) # num rows, num columns

plt.style.use("seaborn-v0_8")
verts_at = (1550,) # put empty for no vert lines
horiz_percentiles = (10, 50, 90)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    # deeta = pd.read_csv(csv_in_path, index_col = 0)
    skip_number = 1
    deeta = np.loadtxt(csv_in_path, delimiter = ',', skiprows = skip_number)
    with open(csv_in_path, "r") as ci:
        for aa in range(skip_number):
            uid_row = ci.readline()
        uid_row = uid_row.split(',')
    
    # allmax = int(np.max(deeta[:,1:])) + 1
    allmin = -75
    # allmin = int(np.min(deeta[:,1:])) - 1
    
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
        aqses = axs[col // tru_ratio[1], col % tru_ratio[1]]
        aqses.plot(deeta[:,0], deeta[:,col + 1])
        aqses.set(
            title = f"{uid_row[col + 1]}: max = {np.max(deeta[:,col + 1])}",
            ylim = (allmin, 0)
        )
        if len(verts_at) > 0:
            aqses.vlines(
                x = verts_at,
                ymin = allmin,
                ymax = 0,
                colors = 'r',
                linestyles = '--'
            )
        if len(horiz_percentiles) > 0:
            aqses.hlines(
                y = np.percentile(deeta[:,col + 1], horiz_percentiles),
                xmin = np.min(deeta[:,0]),
                xmax = np.max(deeta[:,0]),
                colors = 'g',
                linestyles = '--',
                linewidth = 1
            )
        
