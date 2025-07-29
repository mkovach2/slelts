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
        "20250602_apo_+8_g2f11_o_band/ov_curiosity_1_pd1/grouped/2_axis.csv"
        # "20250602_apo_+8_g2f11_o_band/ov_curiosity_1_pd1/grouped/no_sweep = 1.csv"
        # "20250321_fab_var_study/20250528_stage_alt9/grouped/no_sweep = 1.csv"
        # "20250611_apo_combined_proposal/g2f11_ov/ccd/grouped/no_sweep = 1.csv"
        # "20250607_apodized_+8_TEOS_o_band_vert/stage_4/grouped/54636_thru_55738.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/grouped/96678_thru_97182.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/86450_thru_87401.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st2_o_band/grouped/6692_thru_7240.csv"

else:
    csv_in_path = "T:/Device Components/Grating Coupler/"+\
        "20250519_apodized_+8_g2f11/stage_2_xe/for_graphing/grouped/no_sweep = 1.csv"


graphs_ratio = np.array((2.0,1.0)) # num rows, num columns

# top_margin_percent = 0.95
# top_margin_percent = 0.80 # good for column-favoring ratios like (1, 7)
top_margin_percent = 0.965 # a good top for graphs_ratio = (2,1)

plt.style.use("bmh")
# plt.style.use("seaborn-v0_8")

combo_to_use = "o_band" # None to not use a preset combo

presets = {
    "verts_at" : (1310,), # put empty for no vert lines
    "verts_colors" : ('red',), # put empty for no vert lines
    "verts_widths" : (1.75,), # put empty for no vert lines
    "shade_between" : (1260, 1360), # put empty for no fillski tweenor
    "shade_color" : 'blue',
    "shade_alpha" : 0.075,
    "deebs_relative" : True,
    "deebs_at" : (-3,-9), # put empty for no deebs lines
    "deebs_colors" : ('black','orange'), # put empty for no vert lines
    "deebs_widths" : (1,1), # put empty for no vert lines
    # "xtick_spacing" : 10,
    "xlabel" : 'wavelength (nm)',
    # "ytick_spacing" : 10,
    "ylabel" : 'abs(ff1)',
    "yscale" : 'log',
    "horiz_percentiles" : (),
    "horiz_values" : (-15,),
    "max_marker_color" : 'red',
}

presets_combos = {
    "o_band" : {
        "verts_at" : (1310,), # put empty for no vert lines
        "verts_colors" : ('red',), # put empty for no vert lines
        "verts_widths" : (1.75,), # put empty for no vert lines
        "shade_between" : (1260, 1360), # put empty for no fillski tweenor
    },
    "c_band" : {
        "verts_at" : (1550,), # put empty for no vert lines
        "verts_colors" : ('red',), # put empty for no vert lines
        "verts_widths" : (1.75,), # put empty for no vert lines
        "shade_between" : (1530, 1565), # put empty for no fillski tweenor
    }
}

if not(combo_to_use is None):
    presets.update(presets_combos[combo_to_use])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def lin_interp_func(a_in, a0, a1, b0, b1):
    b = (a_in - a0) * (b1 - b0) / (a1 - a0) + b0
    return float(b)



def nearest_lr(
        in_data_x,
        in_data_y,
        target_y, # target dependent variable value
        lin_interp = True
            # if lin_interp is True, nearest_lr will be calculated using target_y exactly,
            # and will linearly interpolate between the nearest data points if target_y isnt
            # in the dataset
):
    max_at = np.argmax(in_data_y)
    maxpoint = (in_data_x[max_at], in_data_y[max_at])

    crossings_eq = np.where(in_data_y == target_y)[0]
    
    crossings_ud = np.where(np.logical_or(
        np.logical_and(in_data_y[:-1] < target_y, in_data_y[1:] > target_y),
        np.logical_and(in_data_y[:-1] > target_y, in_data_y[1:] < target_y)
    ))[0]
    
    x_points = list(crossings_eq)
    y_points = list(target_y * np.ones(np.shape(x_points)))
    
    for cn in crossings_ud:
        if lin_interp:
            x_points.append(lin_interp_func(
                a_in = target_y,
                a0 = in_data_y[cn],
                a1 = in_data_y[cn + 1],
                b0 = in_data_x[cn],
                b1 = in_data_x[cn + 1],
            ))
            y_points.append(target_y)
        else:
            # just chooses the closest data point without interpolating
            if abs(in_data_y[cn] - target_y) < abs(in_data_y[cn + 1] - target_y):
                x_points.append(in_data_x[cn])
                y_points.append(in_data_y[cn])
            else:
                x_points.append(in_data_x[cn + 1])
                y_points.append(in_data_y[cn + 1])
    
    x_points = np.array(x_points)
    y_points = np.array(y_points)
    
    x_left = x_points[x_points < maxpoint[0]]
    y_left = y_points[x_points < maxpoint[0]]
    x_right = x_points[x_points > maxpoint[0]]
    y_right = y_points[x_points > maxpoint[0]]
    
    
    ret_arr = np.zeros((2,2))
    
    if len(x_left) > 0:
        ret_arr[0, 0] = x_left[np.argmax(x_left)]
        ret_arr[0, 1] = y_left[np.argmax(x_left)]
    else:
        ret_arr[0, 0] = np.nan
        ret_arr[0, 1] = np.nan
    
    if len(x_right) > 0:
        ret_arr[1, 0] = x_right[np.argmin(x_right)]
        ret_arr[1, 1] = y_right[np.argmin(x_right)]
    else:
        ret_arr[1, 0] = np.nan
        ret_arr[1, 1] = np.nan
    
    return ret_arr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    deeta = pd.read_csv(csv_in_path, index_col = 0)
    
    # allmax = int(np.max(deeta[:,1:])) + 1
    allmin = -60
    # allmin = int(np.min(deeta[:,1:])) - 1
    
    abs_deeta_col = np.abs(deeta.columns.astype(float))
    x,y = np.meshgrid(deeta.index, abs_deeta_col)
    fig,ax = plt.subplots()
    ax.pcolormesh(x, y, deeta.T)
    # ax.semilogy()
    
    ax.set(
        xlabel = presets["xlabel"],
        ylabel = presets["ylabel"],
        yscale = presets["yscale"],
        # 
    )
    
    if presets["yscale"] == 'log':
        ytickmat = np.arange(0,10,1) * np.atleast_2d(10**np.arange(0,4,1)).T
        ax.set(
            yticks = np.reshape(ytickmat , (np.size(ytickmat),)),
            ylim = (np.min(y),np.max(y)),
        )
    else:
        ax.set(
            yticks = ax.get_yticks()/10 + ax.get_yticks()[0]
        )
    
    ax.scatter(
        deeta.index[np.argmax(deeta, axis = 0)],
        abs_deeta_col,
        marker = '+',
        color = presets["max_marker_color"],
    )
