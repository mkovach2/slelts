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

if False:
    lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
        "General - Products/+NewFileSystem/Device Components/Grating Coupler/"
        
    csv_in_path = lonj +\
        "20250602_apo_+8_g2f11_o_band/ov_vars_proc/st3_bw_hi_ctr/grouped/no_sweep = 1.csv"
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
    # csv_in_path = "T:/Device Components/Grating Coupler/"+\
    #     "20250519_apodized_+8_g2f11/stage_2_xe/for_graphing/grouped/no_sweep = 1.csv"
    csv_in_path = '/home/miles/Desktop/MX0095A_FC3R5/g2f11/cv_stats/cv_'


graphs_ratio = np.array((None, 4)) # num rows, num columns.
    # enter "None" for either rows or columns to force the other dimension.
    # eg graphs_ratio = np.array((10,0)) will give a plot with subplots in 
    # 10 rows, and however many columns it takes to include each data set.

# top_margin_percent = 0.95
# top_margin_percent = 0.80 # good for column-favoring ratios like (1, 7)
# top_margin_percent = 0.965 # a good top for graphs_ratio = (2,1)
top_margin_percent = 0.95 # a good top for graphs_ratio = (2,1)

plt.style.use("bmh")
# plt.style.use("seaborn-v0_8")

combo_to_use = "o_band" # None to not use a preset combo

presets = {
    "verts_at" : (1310,), # put empty for no vert lines
    "verts_colors" : ('red',), # put empty for no vert lines
    "verts_widths" : (1.75,), # put empty for no vert lines
    "shade_between" : (1260, 1360), # put empty for no fillski tweenor
    "shade_color" : 'blue',
    "shade_alpha" : 0.1,
    # "shade_alpha" : 0.075,
    "deebs_relative" : False,
    "deebs_at" : (-15,), # put empty for no deebs lines
    "deebs_colors" : ('black','orange'), # put empty for no vert lines
    "deebs_widths" : (1,1), # put empty for no vert lines
    "ytick_spacing" : 10,
    "horiz_percentiles" : (),
    "horiz_values" : (-15,),
    "max_marker_color" : 'black',
    "max_marker_width" : 1,
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
        "shade_between_2" : (1565, 1625), # L band.  comment out for no L band shading
        "shade_color_2" : 'orange',
        "shade_alpha_2" :  0.1,
    }
}

if not(combo_to_use is None):
    presets.update(presets_combos[combo_to_use])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def lin_interp_func(a_in, a0, a1, b0, b1):
    b = (a_in - a0) * (b1 - b0) / (a1 - a0) + b0
    return float(b)


def ratio_to_shape(
    ratio_in: tuple[float, float]
    | list[float, float]
    | np.ndarray,  # num of rows, num of cols
    num_devices: int | float,  # but should be int, lets be real
):
    # convert a target ratio and number of devices to actual shape in the form (rows, columns)
    if not (isinstance(ratio_in, np.ndarray)):
        ratio_in = np.array(ratio_in)

    grid_shape = np.zeros(np.shape(ratio_in))
    big = np.argmax(ratio_in)
    lil = (big + 1) % 2

    grid_shape[big] = (num_devices * ratio_in[big] / ratio_in[lil]) ** 0.5
    grid_shape[lil] = grid_shape[big] * ratio_in[lil] / ratio_in[big]
    max_remainder = np.argmax(grid_shape - np.floor(grid_shape))
    grid_shape = (np.floor(grid_shape)).astype(int)

    if np.prod(grid_shape) < num_devices:
        if grid_shape[0] == grid_shape[1]:
            grid_shape[(max_remainder + 1) % 2] += 1
        grid_shape[max_remainder] += 1

    return grid_shape


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
    
    # deeta = pd.read_csv(csv_in_path, index_col = 4)
    skip_number = 1
    deeta = np.loadtxt(csv_in_path, delimiter = ',', skiprows = skip_number)
    with open(csv_in_path, "r") as ci:
        for aa in range(skip_number):
            uid_row = ci.readline()
        uid_row = uid_row.strip().split(',')
    
    # allmax = int(np.max(deeta[:,1:])) + 1
    allmin = -60
    # allmin = int(np.min(deeta[:,1:])) - 1
    
    num_graphs = np.shape(deeta)[1] - 1
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
    
    super_str = f""
    if len(presets["horiz_percentiles"]) > 0:
        super_str += "percentiles = " + str(tuple(np.flip(np.sort(presets["horiz_percentiles"])))) + "; "
    if len(presets["horiz_values"]) > 0:
        super_str += "other horiz lines = " + str(tuple(np.flip(np.sort(presets["horiz_values"])))) + "; "
    if len(presets["verts_at"]) > 0:
        super_str += "vertical lines = " + str(tuple(np.sort(presets["verts_at"]))) + "; "
    if len(presets["shade_between"]) > 0:
        super_str += "shaded area = " + str(tuple(np.sort(presets["shade_between"]))) + "; "
    if len(presets["deebs_at"]) > 0:
        if presets["deebs_relative"]:
            super_str += "dB drops from max = " + str(presets["deebs_at"]) + "; "
        else:
            super_str += "dB drops from 0 = " + str(presets["deebs_at"]) + "; "
    
    
    fig.suptitle(super_str, y = 0.99)
    
    for col in range(num_graphs):
        aqses = axs[col // tru_ratio[1], col % tru_ratio[1]]
        aqses.plot(deeta[:,0], deeta[:,col + 1])
        
        hp_vals = np.percentile(deeta[:,col + 1], presets["horiz_percentiles"])
        
        max_arg = np.argmax(deeta[:,col + 1])
        maxcoords = (deeta[max_arg, 0], np.max(deeta[:,col + 1]))
        title_str = f"{uid_row[col + 1]}\n"+\
            f"max = {maxcoords}\n"
        
        if len(presets["horiz_percentiles"]) > 0:
            title_str += f"{tuple(np.flip(np.sort(np.around(hp_vals, 2))))}"
        
        aqses.set(
            # title = title_str,
            ylim = (allmin, 0),
            yticks = np.arange(0, allmin,  -abs(presets["ytick_spacing"]))
        )
        
        aqses.vlines(
            x = maxcoords[0],
            ymin = maxcoords[1] - allmin/8,
            ymax = maxcoords[1] + allmin/8,
            color = presets["max_marker_color"],
            linewidth = presets["max_marker_width"],
        )
        aqses.hlines(
            y = maxcoords[1],
            xmin = maxcoords[0] - (np.max(deeta[:,0]) - np.min(deeta[:,0]))/8,
            xmax = maxcoords[0] + (np.max(deeta[:,0]) - np.min(deeta[:,0]))/8,
            color = presets["max_marker_color"],
            linewidth = presets["max_marker_width"],
        )
        
        if len(presets["deebs_at"]) > 0:
            drop_list = []
            for deebski in range(len(presets["deebs_at"])):
                if presets["deebs_relative"]:
                    ty = deeta[:,col + 1].max() - abs(presets["deebs_at"][deebski])
                else:
                    ty = presets["deebs_at"][deebski]
                
                lar = nearest_lr(
                    in_data_x = deeta[:,0],
                    in_data_y = deeta[:,col + 1],
                    target_y = ty,
                    lin_interp = True
                )
                
                aqses.vlines(
                    x = lar[:,0],
                    ymin = allmin,
                    ymax = lar[:,1],
                    colors = presets["deebs_colors"][deebski],
                    linestyles = '--',
                    linewidths = presets["deebs_widths"][deebski]
                )
                
                drop_list.append(np.round(max(lar[:,0]) - min(lar[:,0]),2))
            
            title_str += str(tuple(drop_list))
                
                
        if len(presets["verts_at"]) > 0:
            aqses.vlines(
                x = presets["verts_at"],
                ymin = allmin,
                ymax = 0,
                colors = presets["verts_colors"],
                linestyles = '--',
                linewidths = presets["verts_widths"]
            )
        if len(presets["horiz_percentiles"]) > 0:
            aqses.hlines(
                y = hp_vals,
                xmin = np.min(deeta[:,0]),
                xmax = np.max(deeta[:,0]),
                colors = 'g',
                linestyles = '--',
                linewidth = 1
            )
        if len(presets["horiz_values"]) > 0:
            aqses.hlines(
                y = presets["horiz_values"],
                xmin = np.min(deeta[:,0]),
                xmax = np.max(deeta[:,0]),
                colors = 'g',
                linestyles = '--',
                linewidth = 1
            )
        if len(presets["shade_between"]) > 0:
            aqses.fill_between(
                x = presets["shade_between"],
                y1 = allmin,
                y2 = 0,
                color = presets["shade_color"],
                alpha = presets["shade_alpha"]
            )
        
        if "shade_between_2" in presets.keys():
            
            if "shade_color_2" in presets.keys():
                shade_color_2 = presets["shade_color_2"]
            else:
                shade_color_2 = presets["shade_color"]
            
            if "shade_alpha_2" in presets.keys():
                shade_alpha_2 = presets["shade_alpha_2"]
            else:
                shade_alpha_2 = presets["shade_alpha"]
            
            aqses.fill_between(
                x = presets["shade_between_2"],
                y1 = allmin,
                y2 = 0,
                color = shade_color_2,
                alpha = shade_alpha_2
            )
        
        aqses.set_title(title_str, fontsize = 8)

    plt.show()