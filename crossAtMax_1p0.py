'''
[file name]
[project]
Author: miles @ hyperlightcorp.com
Created: [YYYY-mm-dd]
Modified: 2023-03-16

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import sys
userPath = "C:/Users/miles.HYPERLIGHT"
longPath = userPath + r"/HyperLight Corporation/HyperLight General - General"
sys.path.append(longPath + "/miles/pyScripts")
sys.path.append(longPath + "/miles/pyScripts/modeToPic")
import numpy as np
import matplotlib.pyplot as plt
from crossAtMaxSuite_2p1 import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime
from matplotlib.colors import ListedColormap
import re

euler = 2.7182818284590452353602874
bAlph = ListedColormap(([1,1,1,0],[1,1,1,1]))
outline = 1
colorScheme = 'jet' #also consider 'turbo'
lineWidth = 0.6
labelsize = 6
xTnum = 11 # number of x ticks.  ensure this is odd
comfySize = (9.6, 4.69375) # (9.6, 4.69375) is the size that makes the final
  # plot comfortably fill my laptop monitor.

uid_regex = r'_[\d]{7}_'
# uid_regex = r'_[\d]{5}_' # use this one for old UIDs

saveyn = 'y' # set to 'y' or 'n' to automatically assign that value and 
  # suppress the prompt.  Set to 'None' to be prompted during runtime.


def nowSave(fileToDo,inDir,imageMetadata = {}):
  splittie = fileToDo.split('.')[0]
  # splittie = fileToDo.split('_',maxsplit=2)
  outName = splittie + '_' + 'crosssections'
  # outName = splittie[0] + '_' + splittie[1] + '_' + 'crosssections'
    
  # plt.savefig(outName,metadata=imageMetadata)
  plt.savefig(inDir + '/' + outName,metadata=imageMetadata)
#end def nowSave()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  if 1: # debugging_if
    plt.close("all")
  #end debugging_if
  
  if 0: # debugging_if
    inDir = input("paste one individual file to convert:\n")
    inDir = inDir.replace('\\','/')
    inDir = inDir.strip('\"') # remove quotes
    # if inDir[-1] != '/' and \
    #    inDir[-4:] != ".txt":
    #    # add a trailing slash
    if (0): #debugging_if
      print(inDir)
  else:
    # inDir = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/HyperLight General - General/miles/pyScripts/sandbox"
    inDir = "T:/Layout/Chips/Ciena Passive Chip Batch 3/20230209_MFD_sims/numpy_arrays"
    # inDir = "C:/Users/miles.HYPERLIGHT/Documents/LumericalSimulations/smf28/numpy_arrays"
    # inDir = longPath + "/Simulations/Lumerical_Miles/modeConverter/" +\
    #         "fullSuite_tests/roy800_testcopy"
  
  
  rows = 0
  cols = 1  
    
  longSet = 0
  if longSet:
      fileparts = inDir.rpartition('/')
      inDir = fileparts[0]
      fileToDo = fileparts[2]
  else:
    if 1: #debugging_if
      fileToDo = input("put Esq file:\t")
    #end if 1
    else:
      fileToDo = 'MC__2827883_mode_TE%100n1p44413_rawData_EsqOut.npy'
      # fileToDo = "800nmTop_66793_mode_TE%100_n1.78755_rawData_EsqOut.npy"
    #end else
  
  shortName = fileToDo.rpartition('.')[0]
  fileX = shortName + "_xMat" + ".npy"
  fileY = shortName + "_yMat" + ".npy"

  lumNp = np.load(inDir + '/' + fileToDo)
  xax = np.load(inDir + '/' + fileX)
  yax = np.load(inDir + '/' + fileY)
  
  
  (lumNp,lel,xax) = stretchMat(lumNp,xax,axis_=cols)
  (lumNp,lel,yax) = stretchMat(lumNp,yax,axis_=rows)
  
  mfdDict = getMfd(lumNp,xax,yax)
  
  lumNp = mfdDict['lumNp']
  xax = mfdDict['xax']
  yax = mfdDict['yax']
  maxLo = mfdDict['maxLo']
  xMaxLo = mfdDict['xMaxLo']
  yMaxLo = mfdDict['yMaxLo']
  lowRow = mfdDict['lowRow']
  lowCol = mfdDict['lowCol']
  xPoints = mfdDict['xPoints']
  yPoints = mfdDict['yPoints']
  xMfd = mfdDict['xMfd']
  yMfd = mfdDict['yMfd']
  
  xax2 = xax/1E-6
  yax2 = yax/1E-6
  
  # y ticks
  yTickLocs = np.arange(0,len(yax),round(len(yax)/11))
  yTlabs = np.around(yax[yTickLocs]/1e-6,3)

  # x ticks
  xTickLocs = np.arange(0,len(xax),round(len(xax)/11))
  xTlabs = np.around(xax[xTickLocs]/1e-6,3)
  
  pMosaic = [["twoPl","xPl"],
             ["twoPl","yPl"]]

  fige,axAll = plt.subplot_mosaic(pMosaic,figsize=(22,15),\
                                  gridspec_kw={"width_ratios":[2,1]})
  
  save_p = {
    'format' : 'png',
    'vmin'   : 0,
    'origin' : 'lower',
    'cmap'   : colorScheme
  } 

  plot_p = {
    'vmin'          : 0, #produces really weird warning
    'vmax'          : None, #default by putting "None"
    'origin'        : 'lower',
    'cmap'          : colorScheme,
    'aspect'        : 1,
    'interpolation' : 'none',
    'resample'      : False,
    'filternorm'    : False,
    # 'existing_fig'  : fige,
    # 'splot'         : axAll['twoPl']
  }
  
  contour_p = {
    "num_of_contours" : 1, # each contour n represents the 1/(n * e^2) field
    "thiccPx"         : 3 # stretchIt
    # "thiccLine"       : 1  # stretchIt
  }
    
  
  crop = (xMfd/1E-6,yMfd/1E-6)
  
  ax,xellex = mode2pic(
    inDir + '/' + fileToDo,
    save_presets=save_p,
    plot_presets=plot_p,
    contour_presets=contour_p,
    returnAxisObj=1,
    saveOuts=0,
    crop_um=crop,
    contour=outline
  )
  
  ax.set_position(axAll['twoPl'].get_position())
  ax.set_title('uid ' + re.search(uid_regex,fileToDo)[0].strip('_'))
  
  
  
  plot_UR = xellex.add_subplot(222)
  plot_DR = xellex.add_subplot(224)
  plot_UR.set_position(axAll['xPl'].get_position())
  plot_DR.set_position(axAll['yPl'].get_position())
  plt.close(fige)
  
  upperY = maxLo*1.1
  
  yTpos = [9,0.6]
  plot_UR.plot(xax2,lowRow,lw=lineWidth)
  # plot_UR.plot(xax2,lowRow)
  plot_UR.vlines([
    xax2[xPoints[0]],xax2[xPoints[1]]],
    # xax2[xPoints[0]],xax2[xPoints[1]]],
    0,maxLo/euler**2,color = 'r',
    lw=lineWidth)
  plot_UR.set_title(
    "mode cross section at y = " + str(np.around(yax2[yMaxLo],3)) + " μm",
    fontsize = labelsize
  )
  plot_UR.set_xlabel("x (μm)",fontsize = labelsize)
  plot_UR.set_ylabel("scaled optical intensity vs overall max",fontsize = labelsize)
  plot_UR.set_xlim(-crop[0],crop[0])
  
  xAxHalf = crop[0]
  xIntHalf = int(xAxHalf+1)
  xLabsHalf = np.arange(-xIntHalf,0,xIntHalf / (0.5 * (xTnum-1)))
  xLabs = np.hstack((xLabsHalf,0,abs(np.flip(xLabsHalf))))
  
  xLabs = np.around(xLabs,decimals=1)
  
  plot_UR.set_xticks(xLabs,xLabs,fontsize = labelsize)
  ytick = np.around(plot_UR.get_yticks(),decimals=1)
  plot_UR.set_yticks(ytick/2,ytick/2,fontsize = labelsize)
  plot_UR.set_ylim(bottom=0, top=upperY)
  
  mfdXrounded = np.around(xMfd/1E-6, decimals=2)
  plot_UR.text(
    np.mean([xax2[xPoints[0]],xax2[xPoints[1]]]),0.5*maxLo/euler**2,
    "MFD = " + str(mfdXrounded) + " μm",
    ha='center',
    fontsize = labelsize
  )
  
  
  
  yTpos = [9,0.6]
  plot_DR.plot(yax2,lowCol,lw=lineWidth)
  # plot_DR.plot(xax2,lowRow)
  plot_DR.vlines([
    yax2[yPoints[0]],yax2[yPoints[1]]],
    # xax2[xPoints[0]],xax2[xPoints[1]]],
    0,maxLo/euler**2,color = 'r',
    lw=lineWidth)
  plot_DR.set_title(
    "mode cross section at x = " + str(np.around(xax2[xMaxLo],3)) + " μm",
    fontsize = labelsize
  )
  plot_DR.set_xlabel("y (μm)",fontsize = labelsize)
  plot_DR.set_ylabel("scaled optical intensity vs overall max",fontsize = labelsize)
  plot_DR.set_xlim(-crop[1],crop[1])
  
  xAxHalf = crop[1]
  xIntHalf = int(xAxHalf+1)
  xLabsHalf = np.arange(-xIntHalf,0,xIntHalf / (0.5 * (xTnum-1)))
  xLabs = np.hstack((xLabsHalf,0,abs(np.flip(xLabsHalf))))
  
  xLabs = np.around(xLabs,decimals=1)
  
  plot_DR.set_xticks(xLabs,xLabs,fontsize = labelsize)
  # ytick = np.around(plot_DR.get_yticks(),decimals=1)
  # ytick set above
  plot_DR.set_yticks(ytick/2,ytick/2,fontsize = labelsize)
  plot_DR.set_ylim(bottom=0, top=upperY)
  
  mfdYrounded = np.around(yMfd/1E-6, decimals=2)
  plot_DR.text(
    np.mean([yax2[yPoints[0]],yax2[yPoints[1]]]),0.5*maxLo/euler**2,
    "MFD = " + str(mfdYrounded) + " μm",
    ha='center',
    fontsize = labelsize
  )
    
  
  imageMetadata = { # these follow the suggestions of the PNG spec
    "Description" : "waveguide mode generated from raw data exported by "+\
                    "Lumerical MODE",
    "Copyright" : "probably Hyperlight, probably current year, idk #FIfXME",
    "Creation Time" : str(datetime.utcnow()),
    "Software" : "crossAtMax",
    "Source File" : inDir + '/' + fileToDo
  }
  
  ax.figure.set_size_inches(comfySize)
    
  if saveyn is None:
    saveyn = input("save? [Y/n]")
  #end if saveyn is None

  if saveyn.lower() != 'n':
    nowSave(fileToDo,inDir,imageMetadata=imageMetadata)
    # splittie = fileToDo.split('.')[0]
    # # splittie = fileToDo.split('_',maxsplit=2)
    # outName = splittie + '_' + 'crosssections'
    # # outName = splittie[0] + '_' + splittie[1] + '_' + 'crosssections'
      
    # # plt.savefig(outName,metadata=imageMetadata)
    # plt.savefig(inDir + '/' + outName,metadata=imageMetadata)

#end if __name__ == "__main__"