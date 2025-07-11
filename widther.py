


import numpy as np
import matplotlib.pyplot as plt
plt.style.use("bmh")



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




if __name__ == "__main__":
    
    plt.close('all')
    
    r = 100
    c = 2
    plotstep_x =5
    plotstep_y = 0.1
    
    tval = 0.15
    
    # aree = np.zeros((r,c))
    in_data_x = np.arange(r) + 1
    
    # modnum = 4
    # print(f"in_data_x % modnum =\n{in_data_x % modnum}\n")
    # print(f"in_data_x // modnum =\n{in_data_x // modnum}\n")
    
    # blelb = (in_data_x % modnum + 1) * (in_data_x // modnum)
    # print(f"blelb =\n{blelb}\n")
    # in_data_y = in_data_x - blelb * 2
    
    in_data_y = np.sin(in_data_x * np.pi/10) * in_data_x / r
    
    lin_interp = True
    
    # print(in_data_y)
    
    fig = plt.figure()
    axes = plt.gca()
    axes.plot(in_data_x, in_data_y)
    
    
    axes.set_xticks(np.arange(min(in_data_x) - plotstep_x, max(in_data_x) + plotstep_x, plotstep_x))
    axes.set_yticks(np.arange(min(in_data_y) - plotstep_y, max(in_data_y) + plotstep_y, plotstep_y))
    
    # max_at = np.argmax(in_data_y)
    # maxpoint = (in_data_x[max_at], in_data_y[max_at])
    
    # axes.scatter(maxpoint[0], maxpoint[1])
    
    # # leftmat = aree[in_data_x < maxpoint[0]]
    # # rightmat = aree[in_data_x > maxpoint[0]]
    
    # diffmat = in_data_y - tval
    
    # # if lin_interp:
    # #     1
    # # else:
    # #     points = np.argmin()
    
    # # aree2 = np.zeros((r,c))
    
    # # crossings_up = np.where(np.logical_and(in_data_y[:-1] < tval, in_data_y[1:] > tval))[0]
    # # crossings_down = np.where(np.logical_and(in_data_y[:-1] > tval, in_data_y[1:] < tval))[0]
    # crossings_eq = np.where(in_data_y == tval)[0]
    
    # crossings_ud = np.where(np.logical_or(
    #     np.logical_and(in_data_y[:-1] < tval, in_data_y[1:] > tval),
    #     np.logical_and(in_data_y[:-1] > tval, in_data_y[1:] < tval)
    # ))[0]
    
    # x_points = list(crossings_eq)
    # y_points = list(tval * np.ones(np.shape(x_points)))
    
    # # for nn in (crossings_up,):
    # # for nn in (crossings_down, crossings_up):
    #     # if nn is crossings_down:
    #         # 1 = 1
    #     # else:
    #         # 1 = 1
        
    # for cn in crossings_ud:
    #     axes.scatter(in_data_x[cn], in_data_y[cn])
    #     axes.scatter(in_data_x[cn + 1], in_data_y[cn + 1])
    #     if lin_interp:
    #         x_points.append(lin_interp_func(
    #             a_in = tval,
    #             a0 = in_data_y[cn],
    #             a1 = in_data_y[cn + 1],
    #             b0 = in_data_x[cn],
    #             b1 = in_data_x[cn + 1],
    #         ))
    #         y_points.append(tval)
    #     else:
    #         # just chooses the closest data point without interpolating
    #         if abs(in_data_y[cn] - tval) < abs(in_data_y[cn + 1] - tval):
    #             x_points.append(in_data_x[cn])
    #             y_points.append(in_data_y[cn])
    #         else:
    #             x_points.append(in_data_x[cn + 1])
    #             y_points.append(in_data_y[cn + 1])
    
    # x_points = np.array(x_points)
    # x_left_at = np.argmax(x_points[x_points < maxpoint[0]])
    # x_right_at = np.argmin(x_points[x_points > maxpoint[0]])
    
    xy_points = nearest_lr(
        in_data_x = in_data_x,
        in_data_y = in_data_y,
        target_y = tval,
        lin_interp = lin_interp
    )
    
    print(xy_points)
    
    axes.fill_between(
        x = (min(xy_points[:,0]), max(xy_points[:,0])),
        y1 = min(in_data_y),
        y2 = max(in_data_y),
        color = 'blue',
        alpha = 0.1
    )
    
    # axes.vlines(
    #     x = x_points,
    #     ymin = min(in_data_y),
    #     ymax = max(in_data_y),
    #     colors = ('orange',),
    #     linestyles = '--',
    #     linewidths = (1,)
    # )
    # # crossings = np.logical_or(
    # #     np.logical_and(in_data_y[:-1] < tval, in_data_y[1:] > tval),
    # #     np.logical_and(in_data_y[:-1] > tval, in_data_y[1:] < tval),
    # #     # in_data_y[:-1] == tval
    # # )
    
    # # print(in_data_x[:-1], in_data_y[:-1][crossings])
    
    # # aree * np.logical_and(aree[:-1,1] <= tval, aree[1:,1] > tval)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
