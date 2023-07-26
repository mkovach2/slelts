'''
picFromFLD.py
[project]
Author: miles at hyperlightcorp dot com
Created: 2022-11-15
Modified: 2022-11-15

imshowPlus takes all the kwargs of imshow and applies them to your input data, 
consisting of two axes and a matrix.  it then applies these to a rather
nice-looking 

1--------10--------20--------30--------40--------50--------60--------70--------
'''

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def imshowPlus(hAxis,vAxis,dMatrix,flipv=0,title = '',
    lessTicks = 10,grid=1,cmap='jet',**ims_params): #also consider 'turbo'

  if len(hAxis) < len(vAxis):
    vpix = 1080
    hpix = int(len(hAxis)/len(vAxis) * vpix)
    numXticks = lessTicks
    numYticks = int(len(vAxis)/len(hAxis) * numXticks)
  #end if len(hAxis)/len(vAxis):
  else:
    hpix = 1920
    vpix = int(len(vAxis)/len(hAxis) * hpix)
    numYticks = lessTicks
    numXticks = int(len(hAxis)/len(vAxis) * numYticks)
  #end else
  dpi_ = 160
  
  if plt.get_fignums() == []:
    figNo = 1
  else:
    figNo = max(plt.get_fignums()) + 1
  #end if
  
  figgie = plt.figure(num=figNo,figsize=(hpix/dpi_,vpix/dpi_),dpi=dpi_)
  ax = plt.subplot()
  
  if flipv:
    plt.imshow(np.flipud(dMatrix),cmap=cmap,**ims_params)
  else:
    plt.imshow(dMatrix,cmap=cmap,**ims_params)
  
  if np.max(hAxis) > 0 and np.min(hAxis) < 0:
    numXticks += not(np.mod(numXticks,2))
    xStep = (np.max(hAxis) - np.min(hAxis)) / (numXticks)
    xLeft = np.flip(np.arange(-xStep,np.min(hAxis),-xStep))
    xRight = np.arange(xStep,np.max(hAxis),xStep)
    hAxislin = np.hstack([xLeft,0,xRight])
  #end if max(hAxis) > 0 and min(hAxis) < 0
  else:
    hAxislin = np.matrix(np.linspace(np.min(hAxis),np.max(hAxis),numXticks))
  #end else
  
  if np.max(vAxis) > 0 and np.min(vAxis) < 0:
    numXticks += not(np.mod(numXticks,2))
    yStep = (np.max(vAxis) - np.min(vAxis)) / (numYticks)
    yLeft = np.flip(np.arange(-yStep,np.min(vAxis),-yStep))
    yRight = np.arange(yStep,np.max(vAxis),yStep)
    vAxislin = np.hstack([yLeft,0,yRight])
  #end if max(vAxis) > 0 and min(vAxis) < 0
  else:
    vAxislin = np.matrix(np.linspace(np.min(vAxis),np.max(vAxis),numXticks))
  #end else
  
  rows = 0 # so that i dont get confused when using functions that 
  cols = 1 # have this notation

  axTicX = np.argmin(np.abs(np.transpose(np.matrix(hAxis)) - hAxislin),rows)
  axTicY = np.argmin(np.abs(np.transpose(np.matrix(vAxis)) - vAxislin),rows)
  
  axTicX = axTicX[0,:].tolist()[0]
  axTicY = axTicY[0,:].tolist()[0]
  
  # try:
  #   xL = list(np.around(hAxislin,1))
  # #end try
  # except:
    # 1
  xL = list(list(np.around(hAxislin,1))[0])
  #end except
  yL = list(np.around(vAxislin,1))
  
  if flipv: 
    ax.set_yticks(axTicY,np.flip(yL))
  else:
    ax.set_yticks(axTicY, yL)
  
  try:
    ax.set_xticks(axTicX, xL)
  #end try
  except:
    print("problem with the function that generates axis labels.  if youre"+\
          " still seeing this, remind miles to #FIXME")
  #end except
  
  if not(title == ''):
    plt.title(title)
  #end if not(title_in == '')
  
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

  divider = make_axes_locatable(ax)
  colorbar_axes = divider.append_axes("right", size="3%", pad="1%")
  # colorbar_axes.set_yticks([1e5,2e5,3e5,4e5,5e5])
  plt.colorbar(cax=colorbar_axes)
  
  return figgie
#end def imshowPlus(hAxis,vAxis,dMatrix,cmap = 'jet')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":

  # input("enter name of ")
  inF = "T:/Device Components/Segmented CPW/reduced_100_10min_recalcs/"+\
    "60997_X_cut_mono_sgw_51.67946464u_10.0GHz_math.fld"
  # inF = "T:/Device Components/Segmented CPW/vs_measured_2_deMbed/"+\
  #   "62857_X_cut_mono_wL_1.31u_10.0GHz.fld"
    
  juh = pd.read_csv(inF,sep=' ',header=None, skiprows=2,\
    names=['x','y','z','','r','i']).\
    dropna(axis='columns',how='all')
  
  juh = juh.drop(columns='x')
  
  juh['mag'] = ((juh.r)**2 + (juh.i)**2)**0.5
  
  unit = {
    "um" : 1e-6,
    "nm" : 1e-9
  }
  
  yAx = pd.unique(juh.y)/unit["um"]
  zAx = pd.unique(juh.z)/unit["um"]
  
  allMat = np.rot90(np.reshape(np.array(juh.mag),(len(yAx),len(zAx))),1)

  imshowPlus(yAx,zAx,allMat,title="PAN!",lessTicks=20,cmap='jet',vmax = 1000e3)
  plt.savefig("knoonus3.png")
# end if __name__ == "__main__"