'''
[file name]
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''

import numpy as np
import matplotlib.pyplot as plt

def plotNice():
  if plt.get_fignums() == []:
    figNo = 1
  else:
    figNo = max(plt.get_fignums()) + 1
  #end if

  resLim = (2160,3840) #(vertical px, horizontal px)
  # resolution limits.  currently, this corresponds to 4k
  # i know that it's backwards, but i wanted it to be consistent
  # with matrix addressing.
  
  if len(longX) < len(longY):
    vpix = 2160
    hpix = len(longX)/len(longY) * vpix
  #end if len(longX)/len(longY):
  else:
    hpix = 3840
    vpix = len(longY)/len(longX) * hpix
  #end else
  dpi_ = 160
  
  plt.figure(num=figNo,figsize=(hpix/dpi_,vpix/dpi_),dpi=dpi_)
  ax = plt.subplot()

  plt.imshow(newMat,**plot_presets)
  
  numXticks = 2 * int(10*26/19)
  numYticks = 2 * 10
  
  if np.max(longX) > 0 and np.min(longX) < 0:
    numXticks += not(np.mod(numXticks,2))
    xStep = (np.max(longX) - np.min(longX)) / (numXticks)
    xLeft = np.flip(np.arange(-xStep,np.min(longX),-xStep))
    xRight = np.arange(xStep,np.max(longX),xStep)
    longXlin = np.hstack([xLeft,0,xRight])
  #end if max(longX) > 0 and min(longX) < 0
  else:
    longXlin = np.matrix(np.linspace(np.min(longX),np.max(longX),numXticks))
  #end else
  
  if np.max(longY) > 0 and np.min(longY) < 0:
    numXticks += not(np.mod(numXticks,2))
    yStep = (np.max(longY) - np.min(longY)) / (numYticks)
    yLeft = np.flip(np.arange(-yStep,np.min(longY),-yStep))
    yRight = np.arange(yStep,np.max(longY),yStep)
    longYlin = np.hstack([yLeft,0,yRight])
  #end if max(longY) > 0 and min(longY) < 0
  else:
    longYlin = np.matrix(np.linspace(np.min(longY),np.max(longY),numXticks))
  #end else
  
  rows = 0 # so that i dont get confused when using functions that 
  cols = 1 # have this notation

  axTicX = np.argmin(np.abs(np.transpose(np.matrix(longX)) - longXlin),rows)
  axTicY = np.argmin(np.abs(np.transpose(np.matrix(longY)) - longYlin),rows)
  
  axTicX = axTicX[0,:].tolist()[0]
  axTicY = axTicY[0,:].tolist()[0]
  
  xL = list(np.around(longXlin/10**-6,1))
  yL = list(np.around(longYlin/10**-6,1))
  
  ax.set_xticks(axTicX, xL)
  ax.set_yticks(axTicY, yL)
  plt.title(keye + " " + fileIn.rpartition('.')[0])
  plt.xlabel("um")
  plt.ylabel("um")
  
  gridParams = {
    "color"     : 'w', 
    "linestyle" : '--',
    "linewidth" : 0.3
  } # end gridParams
  
  axTicY = list(axTicY)
  
  if grid:
    for yT in axTicY:
      ax.axhline(y=yT,**gridParams)
    #end for yT in axTicY
    for xT in axTicX:
      ax.axvline(x=xT,**gridParams)
    #end for xT in axTicX
  #end if grid

  #────────────────██──────────────────█───────███─────────
  #─────────────────█──────────────────█──────────█────────
  #──███────███─────█─────███────███───████────████───███──
  #─█──────█───█────█────█───█──█───█──█───█──█───█──█───█─
  #──███────███─────██────███───█──────████────████──█─────          

  divider = make_axes_locatable(ax)
  colorbar_axes = divider.append_axes("right", size="3%", pad="1%")
  colorbar_axes.set_yticks([1,2,3,4,5])
  
  #──███────█───────────────────────────█────────────────────███──
  #─█───────█───────────────────────────█───────────────────█───█─
  #──███───█████───███───█───█───███───█████──█───█───███───█████─
  #─────█───█─────█───█──█───█──█───────█─────█───█──█───█──█─────
  #──███─────███──█───────███────███─────███───███───█───────████─
  
  if inFn.lower() == "matdata.txt" and showMatl:
    overlayDict[fPrefix] = material_outline(newMat,thiccLine = stretch)
  #end if inFn.lower() == "matdata.txt" and showMatl
  elif showMatl:
    ax.imshow(
      overlayDict[fPrefix],
      cmap=bAlphPink,
      vmin=0,
      origin='lower'
    )#end ax.imshow
  #end elif showMatl
#end def plotNice()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  1# put main here
# end if __name__ == "__main__"