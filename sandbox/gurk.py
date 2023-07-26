'''
<filename>.py
<project>
Author: miles at hyperlightcorp dot com
Created: <date>
Modified: <date>

<description>

1--------10--------20--------30--------40--------50--------60--------70--------
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import numpy as np
import matplotlib.pyplot as plt
from crossAtMaxSuite_1p5 import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

npy_in = r"C:/Users/miles.HYPERLIGHT/HyperLight Corporation/HyperLight General"+\
  " - General/miles/pyScripts/sandbox/MC__2827883_mode_TE%100n1p44413_rawData_EsqOut.npy"

num_of_contours = 1
thiccLine = 0
# euler = 2.71828182845904523536
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# def stretchMat(matrIn,axIn,axis_=0,shouty=1): # requires numpy
#   #import numpy as np.  # just uncomment this if its the only thing
#   # that needs numpy or if declaring the function independently
#   d = axIn[1:] - axIn[:-1]
#   dRatio = d/np.min(d)
#   if axis_:
#     if shouty:
#       print(np.shape(matrIn))
#       print("axis=" + str(axis_))
#     mInIndex = matrIn[:,:-1]
#   else:
#     if shouty:
#       print(np.shape(matrIn))
#       print("axis=" + str(axis_))
#     mInIndex = matrIn[:-1,:]
#   matrOut = np.repeat(mInIndex,dRatio.astype(int),axis=axis_)
#   longAxis = np.repeat(axIn[:-1],dRatio.astype(int))
#   return (matrOut,d,longAxis)
# #end def stretchMat(matrIn,axIn,axis_=0,shouty=0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":

  outline = 1
  
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
    inDir = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/HyperLight "+\
      "General - General/miles/pyScripts/sandbox"
    # inDir = "T:/Layout/Chips/Ciena Passive Chip Batch 3/20230209/numpy_arrays"
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
    if 0: #debugging_if
      fileToDo = input("put Esq file:\t")
    #end if 1
    else:
      fileToDo = "MC__2827883_mode_TE%100n1p44413_rawData_EsqOut.npy"
      # fileToDo = "800nmTop_66793_mode_TE%100_n1.78755_rawData_EsqOut.npy"
    #end else
  
  if outline:
    tMd = mf_contour(inDir + '/' + fileToDo,thiccLine=1)
  #end if 1
  
  shortName = fileToDo.rpartition('.')[0]
  fileX = shortName + "_xMat" + ".npy"
  fileY = shortName + "_yMat" + ".npy"

  lumNp = np.load(inDir + '/' + fileToDo)
  xax = np.load(inDir + '/' + fileX)
  yax = np.load(inDir + '/' + fileY)
  
  (lumNp,lel,xax) = stretchMat(lumNp,xax,axis_=cols)
  (lumNp,lel,yax) = stretchMat(lumNp,yax,axis_=rows)
  
  fudgeFactor = 200 # maximum number of units above y=0 to be an upper bound
                  # when finding max value. set to negative to find max
                  # in BOx
                  # enter fudgeFactor = ridge height for max in ridge
  boxBound = npClosest(yax,0) + fudgeFactor
  
  
  
  
  
  # #findmaxlo
  
  # npClosest(lumNp,np.max(lumNp))
  
  # #findmaxlo
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  # where y = 0, ie the oxide's maximum height
  # maxLo = 0.4195
  maxLo = np.max(lumNp[0:boxBound,:])
  maxLoAddrs = npClosest(lumNp[0:boxBound,:],maxLo)
  
  # maxLoAddrs = np.where(np.abs(xax)==np.min(np.abs(xax)))
  
  yMaxLo = round(np.mean(maxLoAddrs[0]))
    
  if fudgeFactor < 0:
    xMaxLo = round(np.mean(maxLoAddrs[1]))
  #end if fudgeFactor > 0
  else:
    xMaxLo = np.round(maxLoAddrs)[0]
  #end else
  
  # maxLo = 0.4195/euler**2
  lowRow = lumNp[yMaxLo,:]
  lowCol = lumNp[:,xMaxLo]
  
  locExt = np.multiply(abs(d_1d(lowRow)) < 0.0008,np.arange(len(lowRow[:-1])))
  # locExt = np.multiply(abs(d_1d(lowRow)) < 0.0008,lowRow[:-1])
  # locExt = np.where(d_1d(lowRow) < 0.0008)[0]
  # locExt = npClosest(d_1d(lowRow),0)
  xMaxLo = locExt[npClosest(xax,0)]
  maxLo = lowRow[xMaxLo]
  # porp = npClosest(locExt,npClosest(xax,0))
  # xMaxLo2 = lowRow[npClosest(xax,0)]
  
  # mfdX = np.where(np.abs(lowRow-maxLo/euler**1) < 0.03)[0]
  # mfdY = np.where(np.abs(lowCol-maxLo/euler**1) < 0.01)[0]
  mfdX = np.where(np.abs(lowRow-maxLo/euler**2) < 0.03)[0]
  mfdY = np.where(np.abs(lowCol-maxLo/euler**2) < 0.01)[0]
  # mfdY = npClosest(lowCol,maxLo/euler**2)
  
  # xPo = npClosest(d_1d(mfdX),np.max(d_1d(mfdX)))#[0]
  # yPo = npClosest(d_1d(mfdY),np.max(d_1d(mfdY)))#[0]
  xPo = np.where(d_1d(mfdX)!=1)[0]
  yPo = np.where(d_1d(mfdY)!=1)[0]
  
  xPoints = [mfdX[xPo],mfdX[xPo+1]]
  yPoints = [mfdY[yPo],mfdY[yPo+1]]
  
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
  
  axAll["twoPl"].imshow(lumNp,cmap='jet',vmin=0,origin='lower')
  if outline:
    axAll["twoPl"].imshow(tMd,cmap=bAlph,vmin=0,origin='lower')
  #end if outline
  #also consider "turbo"
  axAll["twoPl"].axhline(y=yMaxLo, color='w', linestyle='-')
  axAll["twoPl"].axvline(x=xMaxLo, color='w', linestyle='-')
  axAll["twoPl"].set_yticks(yTickLocs,yTlabs)
  axAll["twoPl"].set_xticks(xTickLocs,xTlabs)
  axAll["twoPl"].set_title("mode")
  axAll["twoPl"].set_xlabel("x (μm)")
  axAll["twoPl"].set_ylabel("y (μm)")
  
  yax2 = yax/1e-6
  xax2 = xax/1e-6
  
  yTpos = [9,0.6]
  axAll["xPl"].plot(xax2,lowRow)
  axAll["xPl"].vlines([xax2[xPoints[0]],\
                       xax2[xPoints[1]]],\
                      0,maxLo/euler**2,color = 'r')
  axAll["xPl"].set_title("mode cross section at y = " + 
                         str(np.around(yax2[yMaxLo],3)) + " μm")
  axAll["xPl"].set_xlabel("x (μm)")
  axAll["xPl"].set_ylabel("scaled optical intensity vs overall max")
  axAll["xPl"].set_ylim(bottom=0, top=1.0)
  axAll["xPl"].text(yTpos[0],yTpos[1], "MFD = " + \
                    str(xax2[xPoints[1]]-xax2[xPoints[0]]) + " μm",\
                    ha='right')
  
  xTpos = [9,0.6]
  axAll["yPl"].plot(yax2,lowCol)
  axAll["yPl"].vlines([yax2[yPoints[0]],\
                       yax2[yPoints[1]]],\
                      0,maxLo/euler**2,color = 'r')
  axAll["yPl"].set_title("mode cross section at x = " + 
                         str(np.around(xax2[xMaxLo])) + " μm")
  axAll["yPl"].set_xlabel("y (μm)")
  axAll["yPl"].set_ylabel("scaled optical intensity vs overall max")
  axAll["yPl"].set_ylim(bottom=0, top=1.0)
  axAll["yPl"].text(xTpos[0],xTpos[1], "MFD = " + \
                    str(yax2[yPoints[1]]-yax2[yPoints[0]]) + " μm",\
                    ha='right')
  
  plt.show()
  
  imageMetadata = { # these follow the suggestions of the PNG spec
    "Description" : "waveguide mode generated from raw data exported by "+\
                    "Lumerical MODE",
    "Copyright" : "probably Hyperlight, probably current year, idk #FIfXME",
    "Creation Time" : str(datetime.utcnow()),
    "Software" : "crossAtMax",
    "Source File" : inDir + '/' + fileToDo
  }
  
  saveyn = 'n'
  # saveyn = input("save? [Y/n]")
  if saveyn.lower() != 'n':
    splittie = fileToDo.split('.')[0]
    # splittie = fileToDo.split('_',maxsplit=2)
    outName = splittie + '_' + 'crosssections'
    # outName = splittie[0] + '_' + splittie[1] + '_' + 'crosssections'
      
    # plt.savefig(outName,metadata=imageMetadata)
    plt.savefig(inDir + '/' + outName,metadata=imageMetadata)

  
  
  
  
#end if __name__ == "__main__"