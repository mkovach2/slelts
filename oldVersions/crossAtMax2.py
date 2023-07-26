'''
crossAtMax2.py
lumSweep project
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''

hlgg = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
       "HyperLight General - General"
       
import sys
sys.path.append(hlgg + "/miles/pyScripts/modeToPic")

import os
import numpy as np
import matplotlib.pyplot as plt
from crossAtMaxSuite import stretchMat
from datetime import datetime
from matplotlib.colors import ListedColormap

euler = 2.7182818284590452353602874
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  if 1: # debugging_if
    plt.close("all")
  #end debugging_if
  
  if 0: # debugging_if
    inDir = input("pastre one individual file to convert:\n")
    inDir = inDir.replace('\\','/')
    inDir = inDir.strip('\"') # remove quotes
    # if inDir[-1] != '/' and \
    #    inDir[-4:] != ".txt":
    #    # add a trailing slash
    if (0): #debugging_if
      print(inDir)
  else:
    inDir = hlgg + "/Simulations/Lumerical_Miles/modeConverter/"+\
            "fullSuite_tests/roy800_testcopy"
  
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
      fileToDo = "800nmTop_66793_mode_TE%100_n1.78755_rawData_EsqOut.npy"
    #end else
  
  shortName = fileToDo.rpartition('.')[0]
  fileX = shortName + "_xMat" + ".npy"
  fileY = shortName + "_yMat" + ".npy"

  lumNp = np.load(inDir + '/' + fileToDo)
  xax = np.load(inDir + '/' + fileX)
  yax = np.load(inDir + '/' + fileY)
  
  expand = 1
  if expand:
    (lumNp,lel,xax) = stretchMat(lumNp,xax,axis_=cols)
    (lumNp,lel,yax) = stretchMat(lumNp,yax,axis_=rows)
  #end if expand
  else:
    (lumNp,lel,xax) = (lumNp,xax,cols)
    (lumNp,lel,yax) = (lumNp,yax,rows)
  #end else
  
  truthMat = (lumNp >= 1/euler**2)
  # a contour which separates the MFD inside from outside
  
  if 0: #thicc version
    tMy = (truthMat[:-3,:] != truthMat[3:,:])
    tMx = (truthMat[:,:-3] != truthMat[:,3:])
    tMd = np.zeros(np.shape(truthMat))
    tMd[2:-1,1:-2] = tMx[:-3,:] + tMy[:,:-3] + tMx[3:,:] + tMy[:,3:]
  #end if 1: #thicc version
  else:
    tMy = (truthMat[:-1,:] != truthMat[1:,:])
    tMx = (truthMat[:,:-1] != truthMat[:,1:])
    tMd = np.zeros(np.shape(truthMat))
    tMd[1:,:-1] = tMx[:-1,:] + tMy[:,:-1] + tMx[1:,:] + tMy[:,1:]  
  #end else
  
  tmdWhere = np.where(tMd)
  tMux = np.unique(tmdWhere[0],return_index=1)[1]
  tMuy = np.unique(tmdWhere[1],return_index=1)[1]
  
  xMaxs = []
  # for xUn in np.arange(1:len(tMux)):
  #   xmaxs[xUn] = 
  
  plt.close("all")
  lumNp1 = lumNp[0:-1,0:-1]
  plt.figure(1)
  plt.imshow(lumNp1,cmap='jet',vmin=0,origin='lower')
  bAlph = ListedColormap(([1,1,1,0],[1,1,1,1]))
  #plt.imshow(tMd2,cmap=bAlph2,vmin=0,origin='lower')
  plt.imshow(tMd,cmap=bAlph,vmin=0,origin='lower')


  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
