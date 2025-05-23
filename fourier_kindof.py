import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

filepath = "C:/Users/miles.HYPERLIGHT/Desktop/sneep.csv"
# filepath = "C:/Users/miles.HYPERLIGHT/Desktop/high-vibe.csv"
use_stem = True
indata = np.loadtxt(filepath,delimiter=',',skiprows=1)
time_col = True
common_axes = True # uses the input axis for the output curves
export_csv = True
csv_path = "C:/Users/miles.HYPERLIGHT/Desktop/stage_8a_top10_ez_fft_2comp.csv"
# csv_path = "C:/Users/miles.HYPERLIGHT/Desktop/outie_high_2.csv"

# f_cutoff = 0.01 # to use as a kind of DC block
# range_filter = (362,364)
# range_filter = (6e-5, 6.4e-5)
range_filter = (0.03,)
filter_mode = "lo"
# enter 1 number for a HPF, a range for anything else
delta = 7.27
# delta = 1

# plotmax = min((np.shape(indata)[0]), f_cutoff*2)
plotmax = int(np.shape(indata)[0]/2)

plt.close('all')

fig, axs = plt.subplots(1, 2)
fig2, axs2 = plt.subplots(1, 2)
colors = ('r','g','b','orange','black')

fft_presets = {
    "xscale" : 'log',
    # "yscale" : 'log',
    "xlim" : (0, 1.55)
}

biggest_array = None
header_str = ""

# for column in (1,):
for column in np.arange(1,np.shape(indata)[1]):
    current_color = colors[(column-1) % len(colors)]
    
    if time_col:
        axs[0].plot(indata[:,0], indata[:,column], color = current_color)
    else:
        axs[0].plot(indata[:,column], color = current_color)
    
    axs[0].set_title('input')
    
    ft = np.fft.rfft(indata[:,column])
    ft_x = np.arange(0,plotmax-1)
    
    if time_col:
        ft_x = np.fft.rfftfreq(n = np.shape(indata)[0], d = indata[1, 0] - indata[0, 0])
    
    ft_for_plot = ft
    # ft_for_plot = ft[1:plotmax]
    
    if use_stem == True:
        axs[1].stem(ft_x,np.abs(ft_for_plot),markerfmt = current_color)
    else:
        axs[1].plot(ft_x,np.abs(ft_for_plot),color = current_color)
    # axs[1].stem(ft_x,np.imag(ft_for_plot),markerfmt = current_color)
    axs[1].set_title('first ft')
    axs[1].set(**fft_presets)
    
    axs[0].grid(True)
    axs[0].grid(which="minor", color="0.9")
    axs[1].grid(True)
    axs[1].grid(which="minor", color="0.9")
    
    if len(range_filter) == 1: # HPF
        if filter_mode.lower() in ("high", "hi", "hpf"):
            if time_col:
                fil = np.array(np.arange(len(ft)) > np.argmin(np.abs(ft_x - range_filter[0])),dtype = int)
            else:
                fil = np.array(np.arange(len(ft)) > range_filter[0],dtype = int) # int conversion because they start as bools
        elif filter_mode.lower() in ("low", "lo", "lpf"):
            if time_col:
                fil = np.array(np.arange(len(ft)) < np.argmin(np.abs(ft_x - range_filter[0])),dtype = int)
            else:
                fil = np.array(np.arange(len(ft)) < range_filter[0],dtype = int) # int conversion because they start as bools
    else:
        if filter_mode.lower() == "pass":
            if time_col:
                fil_lo = np.array(np.arange(len(ft)) > np.argmin(np.abs(ft_x - min(range_filter))),dtype = int)
                fil_hi = np.array(np.arange(len(ft)) < np.argmin(np.abs(ft_x - max(range_filter))),dtype = int)
            else:
                fil_lo = np.array(np.arange(len(ft)) > min(range_filter),dtype = int) # int conversion because they start as bools
                fil_hi = np.array(np.arange(len(ft)) < max(range_filter),dtype = int) # int conversion because they start as bools
            
            fil = fil_lo * fil_hi
       
        elif filter_mode.lower() == "stop":
            if time_col:
                fil_lo = np.array(np.arange(len(ft)) < np.argmin(np.abs(ft_x - min(range_filter))),dtype = int)
                fil_hi = np.array(np.arange(len(ft)) > np.argmin(np.abs(ft_x - max(range_filter))),dtype = int)
            else:
                fil_lo = np.array(np.arange(len(ft)) < min(range_filter),dtype = int) # int conversion because they start as bools
                fil_hi = np.array(np.arange(len(ft)) > max(range_filter),dtype = int) # int conversion because they start as bools
            
            fil = fil_lo + fil_hi
    
    newft = np.multiply(fil,ft)
    
    if time_col:
        newft_x = ft_x
        newft_for_plot = newft
    else:
        newft_x = np.arange(1,plotmax)
        newft_for_plot = newft[1:plotmax]
    
    if use_stem == True:
        axs2[1].stem(newft_x,np.abs(newft_for_plot),markerfmt = current_color)
    else:
        axs2[1].plot(newft_x,np.abs(newft_for_plot),color = current_color)
    # axs2[0].stem(newft_x,np.imag(newft_for_plot),markerfmt = current_color)
    axs2[1].set_title('new ft')
    axs2[1].set(**fft_presets)
    
    axs2[0].grid(True)
    axs2[0].grid(which="minor", color="0.9")
    axs2[1].grid(True)
    axs2[1].grid(which="minor", color="0.9")
    
    i_new = np.fft.irfft(newft)
    
    i_new_x = np.arange(len(i_new))
    if common_axes:
        i_new_x = indata[:np.shape(i_new)[0],0]
    else:
        if time_col:
            i_new_x = i_new_x * (indata[1, 0] - indata[0, 0])
    
    axs2[0].plot(i_new_x, i_new, color = current_color)
    axs2[0].set_title('new linear')
    
    if export_csv:
        # np_paired = np.vstack((delta * np.shape(indata)[0]/np.arange(2,np.shape(indata)[0]/2 + 1),np.abs(ft)[2:]))
        if time_col:
            np_paired = np.vstack((ft_x,np.abs(ft)))
        else:
            np_paired = np.vstack((np.arange(2,np.shape(indata)[0]/2 + 1),np.abs(ft)[2:]))
        
        np_filtered = np.vstack((newft_x,np.abs(newft_for_plot)))
        ifft_paired = np.vstack((i_new_x, i_new))
        
        maxsize = max(np.shape(np_paired)[1], np.shape(np_filtered)[1], np.shape(ifft_paired)[1])
        
        huge_arr = np.zeros((6,maxsize))
        huge_arr[0:2,:np.shape(np_paired)[1]] = np_paired
        huge_arr[2:4,:np.shape(np_filtered)[1]] = np_filtered
        huge_arr[4:6,:np.shape(ifft_paired)[1]] = ifft_paired
        
        if biggest_array is None:
            biggest_array = huge_arr
        else:
            biggest_array = np.vstack((biggest_array, huge_arr))
        
        header_str += f"column_{column}a,"+\
            f"column_{column}a,"+\
            f"column_{column}b,"+\
            f"column_{column}b,"+\
            f"column_{column}c,"+\
            f"column_{column}c,"
        
        np.set_printoptions(suppress=True)
        
if export_csv:
    np.savetxt(csv_path, biggest_array.T, delimiter = ',', header = header_str)
    print(f"saved as:\n{csv_path}")
if False:
    print(f'column: {column}\n{np_paired.T}')
