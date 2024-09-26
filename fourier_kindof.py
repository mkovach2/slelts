import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

filepath = "C:/Users/miles.HYPERLIGHT/Desktop/low-vibe.csv"
# filepath = "C:/Users/miles.HYPERLIGHT/Desktop/high-vibe.csv"
use_stem = True
indata = np.loadtxt(filepath,delimiter=',',skiprows=1)
time_col = True
export_csv = True
csv_path = "C:/Users/miles.HYPERLIGHT/Desktop/outie_lo_2.csv"
# csv_path = "C:/Users/miles.HYPERLIGHT/Desktop/outie_high_2.csv"

# f_cutoff = 0.6 # to use as a kind of DC block
# pass_range = (362,364)
# pass_range = (6e-5, 6.4e-5)
pass_range = (10,12.6)
# enter 1 number for a HPF, a range for anything else
delta = 7.27
# delta = 1

# plotmax = min((np.shape(indata)[0]), f_cutoff*2)
plotmax = int(np.shape(indata)[0]/2)

plt.close('all')

fig, axs = plt.subplots(1, 2)
fig2, axs2 = plt.subplots(1, 2)
colors = ('r','g','b','orange','black')

for column in (3,):
# for column in np.arange(1,np.shape(indata)[1]):
    if time_col:
        axs[0].plot(indata[:,0], indata[:,column], color = colors[column-1])
    else:
        axs[0].plot(indata[:,column], color = colors[column-1])
    
    axs[0].set_title('input')
    
    ft = np.fft.rfft(indata[:,column])
    ft_x = np.arange(0,plotmax-1)
    
    if time_col:
        ft_x = np.fft.rfftfreq(n = np.shape(indata)[0], d = indata[1, 0] - indata[0, 0])
    
    ft_for_plot = ft
    # ft_for_plot = ft[1:plotmax]
    
    if use_stem == True:
        axs[1].stem(ft_x,np.abs(ft_for_plot),markerfmt = colors[column-1])
    else:
        axs[1].plot(ft_x,np.abs(ft_for_plot),color = colors[column-1])
    # axs[1].stem(ft_x,np.imag(ft_for_plot),markerfmt = colors[column-1])
    axs[1].set_title('first ft')
    
    if len(pass_range) == 1: # HPF
        if time_col:
            fil = np.array(np.arange(len(ft)) < np.argmin(np.abs(ft_x - pass_range[0])),dtype = int)
        else:
            fil = np.array(np.arange(len(ft)) < pass_range[0],dtype = int) # int conversion because they start as bools
    else:
        if time_col:
            fil_lo = np.array(np.arange(len(ft)) > np.argmin(np.abs(ft_x - min(pass_range))),dtype = int)
            fil_hi = np.array(np.arange(len(ft)) < np.argmin(np.abs(ft_x - max(pass_range))),dtype = int)
        else:
            fil_lo = np.array(np.arange(len(ft)) > min(pass_range),dtype = int) # int conversion because they start as bools
            fil_hi = np.array(np.arange(len(ft)) < max(pass_range),dtype = int) # int conversion because they start as bools
        fil = fil_lo * fil_hi
        
    newft = np.multiply(fil,ft)
    
    if time_col:
        newft_x = ft_x
        newft_for_plot = newft
    else:
        newft_x = np.arange(1,plotmax)
        newft_for_plot = newft[1:plotmax]
    
    if use_stem == True:
        axs2[1].stem(newft_x,np.abs(newft_for_plot),markerfmt = colors[column-1])
    else:
        axs2[1].plot(newft_x,np.abs(newft_for_plot),color = colors[column-1])
    # axs2[0].stem(newft_x,np.imag(newft_for_plot),markerfmt = colors[column-1])
    axs2[1].set_title('new ft')
    
    i_new = np.fft.irfft(newft)
    i_new_x = np.arange(len(i_new))
    
    if time_col:
        i_new_x = i_new_x * (indata[1, 0] - indata[0, 0])
    
    axs2[0].plot(i_new_x, i_new, color = colors[column-1])
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
        
        np.set_printoptions(suppress=True)
        
        np.savetxt(csv_path, huge_arr.T, delimiter = ',')
        print(f"saved as:\n{csv_path}")
    if False:
        print(f'column: {column}\n{np_paired.T}')
        
    
