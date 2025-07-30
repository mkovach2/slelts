# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

#-------10--------20--------30--------40--------50--------60--------70--------
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
        "20250602_apo_+8_g2f11_o_band/ov_curiosity_2_pd0/grouped/2axis.csv"
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

abs_columns = True
abs_index = True
use_transpose = True

combo_to_use = "o_band_contours" # None to not use a preset combo

presets = {
    "title" : "transmission to waveguide, dB",
    "format" : "contour",
        # "contour" for just a contour plot.
        # "both" for pcolormesh with contour.
        # defaults to pcolormesh otherwise.
    # "shade_between" : (-15.5, -14.5), # comment out for no fillski tweenor
    "shade_color" : 'black',
    "shade_alpha" : 0.1,
    "xtick_spacing" : 25,
    "xtick_start" : 1125,
    # "num_xticks" : 10,
    "xlabel" : 'wavelength (nm)',
    "ytick_spacing" : 0.01,
    # "num_yticks" : 10,
    "ylabel" : 'pd0',
    "yscale" : 'linear', # choices: "lin", "log"
    "max_marker_color" : 'red',
}

presets_combos = {
    "o_band_colormesh" : {
        "verts_at" : (1260, 1310, 1360), # put empty for no vert lines
        "verts_colors" : ('black',), # put empty for no vert lines
        "verts_widths" : (0.75, 1.25, 0.75), # put empty for no vert lines
    },
    "c_band_colormesh" : {
        "verts_at" : (1530, 1550, 1565), # put empty for no vert lines
        "verts_colors" : ('black',), # put empty for no vert lines
        "verts_widths" : (0.75, 1.25, 0.75), # put empty for no vert lines
    },
    "o_band_contours" : {
        "verts_at" : (1310,), # put empty for no vert lines
        "verts_colors" : ('black',), # put empty for no vert lines
        "verts_widths" : (1.75,), # put empty for no vert lines
        "shade_between" : (1260, 1360), # put empty for no fillski tweenor
    },
    "c_band_contours" : {
        "verts_at" : (1550,), # put empty for no vert lines
        "verts_colors" : ('black',), # put empty for no vert lines
        "verts_widths" : (1.75,), # put empty for no vert lines
        "shade_between" : (1530, 1565), # put empty for no fillski tweenor
    }
}

if not(combo_to_use is None):
    presets.update(presets_combos[combo_to_use])

contour_presets = {
    "levels" : (-3,-4,-5,-6,-9,-12,-15,-20,-30,-40),
    # "levels" : np.arange(-32, 0, 4),
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

plt.rcParams['contour.negative_linestyle'] = 'solid'

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



def not_ab_emp(
        in_dict,
        key,
        and_eq = None
):
    '''
    NOT ABsent or EMPty: i got tired of having multiple if statements every
    time i needed to do this.

    "and_eq" can be set to a value that will cause the function to return FALSE
    in the additional case that in_dict["key"] != and_eq.
    this way you can say "if 'key' exists in 'in_dict' and in_dict["key"] is equal to A" by using
    if not_ab_emp(in_dict, key, and_eq = A)
    '''

    if not(key in in_dict.keys()):
        return False
    elif hasattr(in_dict[key], '__len__'):
        if len(in_dict[key]) < 1:
            return False
        elif and_eq is None:
            return True
        else:
            return in_dict[key] == and_eq
    elif in_dict[key] is None:
        return False
    elif and_eq is None:
        return True
    else:
        return in_dict[key] == and_eq

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if True:
        plt.close('all')
    
    deeta = pd.read_csv(csv_in_path, index_col = 0)
    
    deeta.columns = deeta.columns.astype(float)
    deeta.set_index(deeta.index.astype(float), inplace = True)
    
    if abs_columns:
        deeta.columns = np.abs(deeta.columns)
    if abs_index:
        deeta.set_index(np.abs(deeta.index), inplace = True)
    
    x,y = np.meshgrid(deeta.index, deeta.columns)
    fig,ax = plt.subplots()
    
    if not_ab_emp(presets, "format", and_eq = "both"):
        contour_presets.update(both_contour_presets)
    
    contour_presets["levels"] = np.sort(contour_presets["levels"])
    # this is what plt sounds like:
    # *pathetic bawling* ValueError: Contour levels must be increasing
    
    
    
    #---- main plot
    if not_ab_emp(presets, "format", and_eq = "contour"):
        if use_transpose:
            # why cant i just say deeta = deeta.T at the beginning?  WHO KNOWS!
            deeta_c = ax.contour(x, y, deeta.T, **contour_presets)
        else:
            deeta_c = ax.contour(x, y, deeta, **contour_presets)
        
        ax.clabel(deeta_c, **contour_label_presets)
        
    else:
        if use_transpose:
            # why cant i just say deeta = deeta.T at the beginning?  WHO KNOWS!
            ax.pcolormesh(x, y, deeta.T)
        else:
            ax.pcolormesh(x, y, deeta)
    
    ax.set(
        xlabel = presets["xlabel"],
        ylabel = presets["ylabel"],
        yscale = presets["yscale"],
        title = presets["title"],
    )
    
    
    
    #---- y axis
    if presets["yscale"] == 'log':
        ytickmat = np.arange(0,10,1) * np.atleast_2d(10**np.arange(0,4,1)).T
        ax.set(
            yticks = np.reshape(ytickmat , (np.size(ytickmat),)),
            ylim = (np.min(y),np.max(y)),
        )
    else:
        if not("ytick_spacing" in presets.keys()):
            presets["ytick_spacing"] = (np.max(deeta.columns) - np.min(deeta.columns)) / presets["num_yticks"]
            
        ytick_arr = np.arange(
            start = np.min(deeta.columns),
            stop = np.max(deeta.columns) + presets["ytick_spacing"],
            step = presets["ytick_spacing"]
        )
        
        if np.size(ytick_arr) > 200:
            yslashn = input(f"number of yticks = {np.size(ytick_arr)}.  really (y/N)? ")
        else:
            yslashn = 'y'
        
        if yslashn.lower() == 'y':
            ax.set_yticks(ytick_arr)
    
    
    
    #---- xticks
    if not("xtick_spacing" in presets.keys()):
        presets["xtick_spacing"] = (np.max(deeta.index) - np.min(deeta.index)) / presets["num_xticks"]
    
    if not(not_ab_emp(presets, "xtick_start")):
        presets["xtick_start"] = np.min(deeta.index)
    
    xtick_arr = np.arange(
        start = presets["xtick_start"],
        stop = np.max(deeta.index) + presets["xtick_spacing"],
        step = presets["xtick_spacing"]
    )
    
    if np.size(xtick_arr) > 200:
        yslashn = input(f"number of xticks = {np.size(xtick_arr)}.  really (y/N)? ")
    else:
        yslashn = 'y'
    
    if yslashn.lower() == 'y':
        ax.set_xticks(xtick_arr)
    
    
    
    #---- max markers
    if "max_marker_color" in presets.keys():
        ax.scatter(
            deeta.index[np.argmax(deeta, axis = 0)],
            deeta.columns,
            marker = '+',
            color = presets["max_marker_color"],
        )
        ax.legend(("row maximum",))
    
    
    
    #---- overlay contours
    if not_ab_emp(presets, "format", and_eq = "both"):
        if use_transpose:
            # why cant i just say deeta = deeta.T at the beginning?  WHO KNOWS!
            deeta_c = ax.contour(x, y, deeta.T, **contour_presets)
        else:
            deeta_c = ax.contour(x, y, deeta, **contour_presets)
            
        ax.clabel(deeta_c, **contour_label_presets)
    
    
    
    #---- more overlays
    if len(presets["verts_at"]) > 0:
        ax.vlines(
            x = presets["verts_at"],
            ymin = np.min(y),
            ymax = np.max(y),
            colors = presets["verts_colors"],
            linestyles = '--',
            linewidths = presets["verts_widths"]
        )
    
    if len(presets["shade_between"]) > 0:
        ax.fill_between(
            x = presets["shade_between"],
            y1 = np.min(y),
            y2 = np.max(y),
            color = presets["shade_color"],
            alpha = presets["shade_alpha"]
        )

