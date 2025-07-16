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
        "20250602_apo_+8_g2f11_o_band/vert_st6_o_band/grouped_o/no_sweep = 1.csv"
        # "20250611_apo_combined_proposal/g2f11_c_h/grouped/no_sweep = 1.csv"
        # "20250607_apodized_+8_TEOS_o_band_vert/stage_4/grouped/54636_thru_55738.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/grouped/96678_thru_97182.csv"
        # "20250519_apodized_+8_g2f11_c_band/horiz_stage_2/86450_thru_87401.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st2_o_band/grouped/6692_thru_7240.csv"
        # "20250602_apodized_+8_g2f11_o_band/horiz_st1_o_band/grouped/no_sweep = 1.csv"
        
else:
    csv_in_path = "T:/Device Components/Grating Coupler/"+\
        "20250519_apodized_+8_g2f11/stage_2_xe/for_graphing/grouped/no_sweep = 1.csv"

graphs_ratio = np.array((2.0,1.0)) # num rows, num columns

plt.style.use("bmh")
# plt.style.use("seaborn-v0_8")

verts_at = (1310,) # put empty for no vert lines
verts_colors = ('red',) # put empty for no vert lines
verts_widths = (1.75,) # put empty for no vert lines

# verts_at = (1260,1310,1360) # put empty for no vert lines
# verts_colors = ('orange', 'red', 'orange') # put empty for no vert lines
# verts_widths = (1, 1.75, 1) # put empty for no vert lines

# shade_between = (1530, 1565) # put empty for no fillski tweenor
shade_between = (1260, 1360) # put empty for no fillski tweenor
shade_color = 'blue'
shade_alpha = 0.075

deebs_at = (-3,-6) # put empty for no deebs lines
deebs_colors = ('black','orange') # put empty for no vert lines
deebs_widths = (1,1) # put empty for no vert lines

ytick_spacing = 10

horiz_percentiles = ()
# horiz_percentiles = (10, 50, 75)
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
    
    # deeta = pd.read_csv(csv_in_path, index_col = 0)
    skip_number = 1
    deeta = np.loadtxt(csv_in_path, delimiter = ',', skiprows = skip_number)
    with open(csv_in_path, "r") as ci:
        for aa in range(skip_number):
            uid_row = ci.readline()
        uid_row = uid_row.split(',')
    
    # allmax = int(np.max(deeta[:,1:])) + 1
    allmin = -70
    # allmin = int(np.min(deeta[:,1:])) - 1
    
    num_graphs = np.shape(deeta)[1] - 1
    tru_ratio = (np.around((num_graphs/np.product(graphs_ratio))**0.5 * graphs_ratio)).astype(int)
    
    if any(tru_ratio == 1):
        axs = np.atleast_2d(axs)
        if any(np.shape(axs) != tru_ratio):
            axs = axs.T
    
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
            # "top"   : 0.94,
            "top"   : 0.965, # a good top for graphs_ratio = (2,1)
            "right" : 0.96,
            
        },
    )
    
    super_str = ""
    if len(horiz_percentiles) > 0:
        super_str += f"percentiles = {tuple(np.flip(np.sort(horiz_percentiles)))}; "
    if len(verts_at) > 0:
        super_str += f"vertical lines = {tuple(np.sort(verts_at))}; "
    if len(shade_between) > 0:
        super_str += f"shaded area = {tuple(np.sort(shade_between))}; "
    if len(deebs_at) > 0:
        super_str += f"dB drops from max = {deebs_at}; "
    
    
    fig.suptitle(super_str, y = 0.99)
    
    for col in range(num_graphs):
        aqses = axs[col // tru_ratio[1], col % tru_ratio[1]]
        aqses.plot(deeta[:,0], deeta[:,col + 1])
        
        hp_vals = np.percentile(deeta[:,col + 1], horiz_percentiles)
        
        
        title_str = f"{uid_row[col + 1]}\n"+\
            f"max = {np.max(deeta[:,col + 1])}\n"
        
        if len(horiz_percentiles) > 0:
            title_str += f"{tuple(np.flip(np.sort(np.around(hp_vals, 2))))}"
        
        aqses.set(
            # title = title_str,
            ylim = (allmin, 0),
            yticks = np.arange(allmin, ytick_spacing, ytick_spacing)
        )
        
        
        if len(deebs_at) > 0:
            drop_list = []
            for deebski in range(len(deebs_at)):
                lar = nearest_lr(
                    in_data_x = deeta[:,0],
                    in_data_y = deeta[:,col + 1],
                    target_y = deeta[:,col + 1].max() - abs(deebs_at[deebski]),
                    lin_interp = True
                )
                
                aqses.vlines(
                    x = lar[:,0],
                    ymin = allmin,
                    ymax = lar[:,1],
                    colors = deebs_colors[deebski],
                    linestyles = '--',
                    linewidths = deebs_widths[deebski]
                )
                
                drop_list.append(np.round(max(lar[:,0]) - min(lar[:,0]),2))
            
            title_str += str(tuple(drop_list))
                
                
        if len(verts_at) > 0:
            aqses.vlines(
                x = verts_at,
                ymin = allmin,
                ymax = 0,
                colors = verts_colors,
                linestyles = '--',
                linewidths = verts_widths
            )
        if len(horiz_percentiles) > 0:
            aqses.hlines(
                y = hp_vals,
                xmin = np.min(deeta[:,0]),
                xmax = np.max(deeta[:,0]),
                colors = 'g',
                linestyles = '--',
                linewidth = 1
            )
        if len(shade_between) > 0:
            aqses.fill_between(
                x = shade_between,
                y1 = allmin,
                y2 = 0,
                color = shade_color,
                alpha = shade_alpha
            )
        
        aqses.set_title(title_str, fontsize = 8)
