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

from math_utils_20251211 import (
    ratio_to_shape,
    lin_interp_func,
    nearest_lr
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if False:
    # lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
    #     "General - Products/+NewFileSystem/Device Components/Grating Coupler/"
    
    lonj = '/home/miles/Documents/T_local/device_components/grating_coupler/'+\
           '20251126_gc_1033/rd2/processed/grouped/'
    
    csv_in_path = lonj +\
        "transmission_dB.csv"
        # "20250519_apo_+8_g2f11_c_band/vert_stage_2_advanced_trap_remix/stage_2_atr_6249_thru_6601.csv"
        # "20250602_apo_+8_g2f11_o_band/horiz_st2_o_band_power_moves/grouped/no_sweep = 1.csv"
        # "20250602_apo_+8_g2f11_o_band/ov_procedure_test/grouped/no_sweep = 1.csv"
        # "20250519_apo_+8_g2f11_c_band/horiz_stage_2/grouped/11296678_thru_11297463.csv"
        # "20250602_apo_+8_g2f11_o_band/vert_st5_o_band/grouped/nosweep_snorted.csv"
        # "20250602_apo_+8_g2f11_o_band/ov_curi_procedural/stage_1/grouped/sorted.csv"
        # "20250321_fab_var_study/20250528_stage_alt9/grouped/no_sweep = 1.csv"
        # "20250611_apo_combined_proposal/g2f11_ov/ccd/grouped/no_sweep = 1.csv"
        # "20250607_apodized_+8_TEOS_o_band_vert/stage_4/grouped/54636_thru_55738.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/86450_thru_87401.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st2_o_band/grouped/6692_thru_7240.csv"

else:
    round_str = 'rd4'
    
    lonj = '/mnt/T/Device Components/Grating Coupler/' + \
           f'20251126_gc_1033/{round_str}/processed/'
    
    if round_str == 'rd1':
        csv_in_path = lonj + "jmp_data_13036610_loss_more.csv"
    elif round_str == 'rd2':
        csv_in_path = lonj + "jmp_data_13037635_xmit_more.csv"
    elif round_str == 'rd3':
        csv_in_path = lonj + "jmp_data_13056997_loss.csv"
    elif round_str == 'rd4':
        csv_in_path = lonj + "jmp_data_13186843_br.csv"
    
    csv_str = f'20251126_gc_1033 {round_str}'


columns_to_use = ['apparent_center', 'avg', 'max', 'value_at_1033', 'uid', 'linewidth']
# columns_to_use = []
columns_to_exclude = []
# if columns_to_use is an empty list, all columns will be selected except those
# in columns_to_exclude.
apparent_center_diff_wl = 1033



graphs_ratio = np.array((3, 2)) # num rows, num columns.
    # enter "None" for either rows or columns to force the other dimension.
    # eg graphs_ratio = np.array((10,0)) will give a plot with subplots in 
    # 10 rows, and however many columns it takes to include each data set.

# top_margin_percent = 0.95
# top_margin_percent = 0.80 # good for column-favoring ratios like (1, 7)
# top_margin_percent = 0.965 # a good top for graphs_ratio = (2,1)
top_margin_percent = 0.95 # a good top for graphs_ratio = (2,1)

plt.style.use("bmh")
# plt.style.use("seaborn-v0_8")



contour_presets = {
    # "levels" : (-2,-2.5,-3,-3.5,-4,-5,-6,-9,-12,-15,-20,-30,-40),
    # "levels" : np.arange(40, 160, 10),
    # "levels" : np.arange(1320, 1450, 10),
    "levels" : np.hstack((np.arange(-50, -20, 5),np.arange(-20, -10, 1))),
    # "levels" : np.hstack((np.arange(-50, -10, 5),np.arange(-10, 0, 1))),
    "cmap" : "turbo",
}

both_contour_presets = {
    "levels" : (-15,),
    "colors" : ('black',),
    "linewidths": (1,)
    # "linestyle" : 'solid',
    # "negative_linestyle" : 'solid',
}

contour_label_presets = {
    "fontsize" : 9,
    "inline" : True,
    "inline_spacing" : 0,
}

RES_LIMIT = 0.15

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if True:
        plt.close('all')
    
    deeta = pd.read_csv(csv_in_path)
    
    column_for_x = 'pd'
    column_for_y = 'ff'
    
    if abs(deeta['pd'].mean()) < 1e-5:
        deeta['pd'] = deeta['pd'] * 1e6
    
    if 'linewidth' not in deeta.columns:
        deeta['linewidth'] = deeta['pd'] * deeta['ff']
    
    if 'apparent_center' in columns_to_use or 'apparent_center' not in columns_to_exclude:
        deeta['neg_abs_appc_diff'] = -abs(deeta['apparent_center'] - apparent_center_diff_wl)
        columns_to_use.remove('apparent_center')
        columns_to_use.append('neg_abs_appc_diff')
    
    # if len(columns_to_use) > 0:
    #     num_graphs = len(columns_to_use)
    # else:
    #     num_graphs = len(deeta.columns) - len(columns_to_exclude) - 2
    if len(columns_to_use) < 1:
        columns_to_use = deeta.columns.drop([
            *columns_to_exclude,
            column_for_x,
            column_for_y
        ])
    
    num_graphs = len(columns_to_use)
    
    if graphs_ratio [0] is None:
        tru_ratio = np.around((num_graphs / graphs_ratio[1], graphs_ratio[1])).astype(int)
    elif graphs_ratio [1] is None:
        tru_ratio = np.around((graphs_ratio[0], num_graphs / graphs_ratio[0])).astype(int)
    else:
        tru_ratio = ratio_to_shape(
            ratio_in = graphs_ratio,
            num_devices = num_graphs
        )

    if np.product(tru_ratio) < num_graphs:
        tru_ratio[np.argmax(tru_ratio)] += 1
    
    fig, axs = plt.subplots(
        tru_ratio[0],
        tru_ratio[1],
        gridspec_kw={
            "wspace": 0.25,
            "hspace": 0.60,
            "bottom": 0.04,
            "left"  : 0.04,
            "top"   : top_margin_percent,
            "right" : 0.96,
            
        },
    )
    axs = np.atleast_2d(axs)
    if any(np.shape(axs) != tru_ratio): 
        axs = axs.T
    
    for col in range(len(columns_to_use)):
        aqses = axs[col // tru_ratio[1], col % tru_ratio[1]]
        x,y = np.meshgrid(
            pd.unique(deeta[column_for_x]),
            pd.unique(deeta[column_for_y])
        )
        
        z = pd.DataFrame(
            columns = pd.unique(deeta[column_for_x]),
            index = pd.unique(deeta[column_for_y]),
        )
        
        for num, row in deeta.iterrows():
            if row['linewidth'] >= RES_LIMIT:
                z.at[row[column_for_y], row[column_for_x]] = row[columns_to_use[col]]
        
        deeta_p = aqses.pcolormesh(x, y, z.astype(float), cmap = 'turbo')

        if columns_to_use[col] == 'uid':
            deccy = 0
            sizzy = 6
        else:
            deccy = 3
            sizzy = 8
        
        for num, row in deeta.iterrows():
            if row['linewidth'] >= RES_LIMIT:
                aqses.text(
                    row[column_for_x],
                    row[column_for_y],
                    np.round(row[columns_to_use[col]], decimals=deccy),
                    ha='center',
                    va='center',
                    size=sizzy,
                    color='black',
                    backgroundcolor='white',
                )
        
        # deeta_c = aqses.contour(x, y, z.astype(float), **contour_presets)
        # aqses.clabel(deeta_c, **contour_label_presets)

        aqses.set(
            xticks = pd.unique(deeta[column_for_x]),
            yticks = pd.unique(deeta[column_for_y]),
            xlabel = column_for_x,
            ylabel = column_for_y,
            title = columns_to_use[col],
        )
    
    fig.suptitle(csv_str)
    plt.show()