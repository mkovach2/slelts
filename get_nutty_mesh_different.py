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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def lin_interp_func(a_in, a0, a1, b0, b1):
    b = (a_in - a0) * (b1 - b0) / (a1 - a0) + b0
    return float(b)


def nearest_lr(
        in_data_x,
        in_data_y,
        target_y,  # target dependent variable value
        lin_interp=True
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
                a_in=target_y,
                a0=in_data_y[cn],
                a1=in_data_y[cn + 1],
                b0=in_data_x[cn],
                b1=in_data_x[cn + 1],
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

    ret_arr = np.zeros((2, 2))

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
        and_eq=None
):
    '''
    NOT ABsent or EMPty: i got tired of having multiple if statements every
    time i needed to do this.

    "and_eq" can be set to a value that will cause the function to return FALSE
    in the additional case that in_dict["key"] != and_eq.
    this way you can say "if 'key' exists in 'in_dict' and in_dict["key"] is equal to A" by using
    if not_ab_emp(in_dict, key, and_eq = A)
    '''

    if not (key in in_dict.keys()):
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if False:
    lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
        "General - Products/+NewFileSystem/Device Components/Grating Coupler/"
    
    csv_str = ''
    # csv_str = '-12_dB_bw'
    
    csv_in_path = lonj +\
        f"20250602_apo_+8_g2f11_o_band/ov_procedure_test/{csv_str}.csv"
        # "20250602_apo_+8_g2f11_o_band/ov_curiosity_3_ff0_adj_ff1/grouped/2axis.csv"
        # "20250602_apo_+8_g2f11_o_band/ov_curiosity_3_ff0/grouped/2axis.csv"
        # "20250602_apo_+8_g2f11_o_band/ov_curiosity_1_pd1/grouped/2axis.csv"
        # "20250321_fab_var_study/20250528_stage_alt9/grouped/no_sweep = 1.csv"
        # "20250611_apo_combined_proposal/g2f11_ov/ccd/grouped/no_sweep = 1.csv"
        # "20250607_apodized_+8_TEOS_o_band_vert/stage_4/grouped/54636_thru_55738.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/grouped/96678_thru_97182.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/86450_thru_87401.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st2_o_band/grouped/6692_thru_7240.csv"

else:
    lonj = '/home/miles/Documents/T_local/device_components/grating_coupler/' + \
           '20251126_gc_1033/rd2/processed/'

    csv_in_path = lonj + \
                  "jmp_data_13037635_xmit_more.csv"
                  # "transmission_dB.csv"
    
    csv_str = '20251126_gc_1033 rd2'


graphs_ratio = np.array((2.0,1.0)) # num rows, num columns

# top_margin_percent = 0.95
# top_margin_percent = 0.80 # good for column-favoring ratios like (1, 7)
top_margin_percent = 0.965 # a good top for graphs_ratio = (2,1)

plt.style.use("bmh")
# plt.style.use("seaborn-v0_8")

abs_columns = False
abs_index = False
use_transpose = True

# combo_to_use = "o_band_contours" # None to not use a preset combo
combo_to_use = None

presets = {
    "title" : "20251126_gc_1033 rd2",
    # "title" : "effective_center, nm",
    # "title" : "transmission to waveguide, dB",
    # "title" : "transmission to waveguide, dB (pd0 = 0.779, ff1 = -0.0371)",
    # "title" : "transmission to waveguide, dB (pd0 = 0.7353)",
    "format" : "contour",
        # "contour" for just a contour plot.
        # "both" for pcolormesh with contour.
        # defaults to pcolormesh otherwise.
    # "shade_between" : (-15.5, -14.5), # comment out for no fillski tweenor
    "shade_color" : 'black',
    "shade_alpha" : 0.1,
    "xtick_spacing" : 10,
    # "xtick_spacing" : 0.01,
    # "xtick_start" : 1125,
    # "num_xticks" : 10,
    "xlabel" : 'pd0 (um)',
    # "xlabel" : 'wavelength (nm)',
    # "ytick_spacing" : 0.01,
    "num_yticks" : 9,
    "ylabel" : 'ff1 (um^-1)',
    # "ylabel" : 'pd1',
    "yscale" : 'linear', # choices: "linear", "log"
    "max_marker_color" : 'red',
}

if abs_columns:
    presets["ylabel"] = "abs(" + presets["ylabel"] + ")"

if abs_index:
    presets["xlabel"] = "abs(" + presets["xlabel"] + ")"

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

plt.rcParams['contour.negative_linestyle'] = 'solid'

if not("title" in presets.keys()):
    presets["title"] = csv_str

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if True:
        plt.close('all')
    
    deeta = pd.read_csv(csv_in_path, index_col = 0)
    
    column_for_x = 'pd'
    column_for_y = 'ff'
    
    
    
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
            deeta.index[np.nanargmax(deeta, axis = 0)],
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
    if "verts_at" in presets.keys():
        if len(presets["verts_at"]) > 0:
            ax.vlines(
                x = presets["verts_at"],
                ymin = np.min(y),
                ymax = np.max(y),
                colors = presets["verts_colors"],
                linestyles = '--',
                linewidths = presets["verts_widths"]
            )
    
    if "shade_between" in presets.keys():
        if len(presets["shade_between"]) > 0:
            ax.fill_between(
                x = presets["shade_between"],
                y1 = np.min(y),
                y2 = np.max(y),
                color = presets["shade_color"],
                alpha = presets["shade_alpha"]
            )

    plt.show()