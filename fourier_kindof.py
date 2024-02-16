
import numpy as np

import matplotlib.pyplot as plt
 
filepath = "C:/Users/miles.HYPERLIGHT/Desktop/ff0p3.csv"
use_stem = True
indata = np.loadtxt(filepath,delimiter=',',skiprows=1)

f_cutoff = 4
delta = 7.27
# delta = 1

# plotmax = min((np.shape(indata)[0]), f_cutoff*2)
plotmax = int(np.shape(indata)[0]/2)

plt.close('all')

fig, axs = plt.subplots(1, 2)
fig2, axs2 = plt.subplots(1, 2)
colors = ('r','g','b','orange','black')

for column in (1,2):
# for column in np.arange(1,np.shape(indata)[1]):
    axs[0].plot(indata[:,column], color = colors[column-1])
    axs[0].set_title('input')
    
    ft = np.fft.rfft(indata[:,column])
    
    ft_x = np.arange(1,plotmax)
    ft_for_plot = ft[1:plotmax]
    
    if use_stem == True:
        axs[1].stem(ft_x,np.abs(ft_for_plot),markerfmt = colors[column-1])
    else:
        axs[1].plot(ft_x,np.abs(ft_for_plot),color = colors[column-1])
    # axs[1].stem(ft_x,np.imag(ft_for_plot),markerfmt = colors[column-1])
    axs[1].set_title('first ft')
    
    fil = np.array(np.arange(len(ft)) > f_cutoff,dtype = int) # int conversion because they start as bools
     
    newft = np.multiply(fil,ft)
    newft_x = np.arange(1,plotmax)
    newft_for_plot = newft[1:plotmax]
    
    if use_stem == True:
        axs2[1].stem(newft_x,np.abs(newft_for_plot),markerfmt = colors[column-1])
    else:
        axs2[1].plot(newft_x,np.abs(newft_for_plot),color = colors[column-1])
    # axs2[0].stem(newft_x,np.imag(newft_for_plot),markerfmt = colors[column-1])
    axs2[1].set_title('new ft')
    
    i_new = np.fft.irfft(newft)
    
    axs2[0].plot(i_new,color = colors[column-1])
    axs2[0].set_title('new linear')
    
    if True:
        # np_paired = np.vstack((delta * np.shape(indata)[0]/np.arange(2,np.shape(indata)[0]/2 + 1),np.abs(ft)[2:]))
        np_paired = np.vstack((np.arange(2,np.shape(indata)[0]/2 + 1),np.abs(ft)[2:]))
        np.set_printoptions(suppress=True)
        print(f'column: {column}\n{np_paired.T}')
