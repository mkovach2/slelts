'''
modeToPic.py
hyperlight : modeConverter
Author: miles @ hyperlightcorp.com
Created: 2022-05-05
Modified: 2022-05-09 miles @ hyperlightcorp.com

takes a text file of raw data exported by lumerical 
and creates a mode illustration of it.

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from os import listdir, getcwd
from sys import argv


def mode2pic(inData, xyBounds, saveTo, saveOuts=1, xLab="μm", yLab="μm"):
  
  '''
  inputs:
    inData, the path to a raw data file to be converted.  Such files
                should be exported using Lumerical's "write" command, as in:
            
    write(somePath + "exampleFile_lumDat.txt", num2str(varNam), "append");
    
    xyBounds, a four value matrix of the minimum and maximum values
              of the x and y axes, saved similarly and in the form 
             ┌           ┐              
             │ xMin xMax │
             │ yMin yMax │
             └           ┘
  '''
      
  saveName = inData.rpartition('_')[0]
  splitted_name = inData.split('\\')[-1].split('_')
  
  if(len(splitted_name) > 2):
    chTitle = ' '.join(splitted_name[1:-2])
  else:
    chTitle = splitted_name[0]
  
  modeIn = np.matrix(np.loadtxt(inData, delimiter = '\t', unpack=True))
  
  xMin = xyBounds[0,0] * 10**6
  xMax = xyBounds[0,1] * 10**6
  yMin = xyBounds[1,0] * 10**6
  yMax = xyBounds[1,1] * 10**6
  
  inDimX = np.shape(modeIn)[1]
  inDimY = np.shape(modeIn)[0]
  heightNess = 10 # user defined
  wideNess = heightNess * inDimX/inDimY
  fig, ax = plt.subplots(figsize = (wideNess,heightNess))
  thePlot = plt.imshow(modeIn, vmin=0, origin = 'lower', cmap='jet',\
                       aspect=2, interpolation='none',\
                       resample = False, filternorm=False)
  plt.title(chTitle)
  plt.xlabel(xLab)
  plt.ylabel(yLab)
  
  print((xMax-xMin)/(yMax-yMin))

  numXt = 20 #make this an even number
  numYt = np.ceil(numXt * inDimY/inDimX) + 1
  numYt = numYt.astype(int)
  if (numYt/2 != int(numYt/2)): # sorry, this ones gotta be even too.  I can 
    numYt += 1                  # only fiddle with the labels so much.
  
  if (xMin < 0) and (xMax > 0): #FIXME the axes dont scale tru
    xAxArr = np.concatenate((np.linspace(xMin,0,int(numXt/2)),\
                            np.linspace(0,xMax,int(numXt/2))[1:]))
    xIndexArr = np.linspace(0,inDimX,numXt-1)
  else:
    xAxArr = np.linspace(xMin,xMax,numXt)
    xIndexArr = np.linspace(0,inDimX,numXt)
    
  if (yMin < 0) and (yMax > 0):
    yAxArr = np.concatenate((np.linspace(yMin,0,int(numYt/2)),\
                            np.linspace(0,yMax,int(numYt/2))[1:]))
    yIndexArr = np.linspace(0,inDimY,numYt-1)
  else:
    yAxArr = np.linspace(yMin,yMax,numYt)
    yIndexArr = np.linspace(0,inDimY,numYt)

  plt.xticks(xIndexArr,np.around(xAxArr,4))
  plt.yticks(yIndexArr,np.around(yAxArr,4))
  
  divider = make_axes_locatable(ax)
  colorbar_axes = divider.append_axes("right", size="2%", pad=0.1)
  
  plt.show(block=False)
  
  plt.colorbar(thePlot, cax=colorbar_axes)
  if saveOuts:
    plt.savefig(saveName + ".png", format = 'png', dpi = 120)
    np.save(saveName + ".npy", modeIn)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  import time
  
  winCmd = 1 # set to 1 if running from the windows command line
  
  if(len(argv)) >= 2:
    baseDir = argv[1] + "\\"
  else:
    # default dir if no inline arguments are specified
    baseDir = "C:\\Users\\miles.HYPERLIGHT\\HyperLight Corporation\\" + \
              "HyperLight General - General\\Simulations\\Lumerical_Miles\\" + \
              "modeConverter\\tests\\"
  sourcePath = baseDir
  saveDir = baseDir

  if 1: # set to 1 to close all windows before running
    plt.close('all')

  filesInDir = listdir(sourcePath)  # bring in matrix for x,y labels
  if "xyBounds.txt" in filesInDir:
    xyMat = np.matrix(np.loadtxt(sourcePath + "xyBounds.txt", \
                                 delimiter = '\t'))
  else:
    print("file xyBounds.txt could not be found in this directory.\n" + \
          "plot axes will be normalized to 1.")
    xyMat = np.matrix([[0,10**-6],[0,10**-6]])
  
  lumDatFiles = []
    
  for fileName in filesInDir:
    [imgName, fileSuff] = fileName.rpartition('_')[0::2]

    if fileSuff.lower() == "lumdat.txt":
      lumDatFiles.append(fileName)
    
  if len(lumDatFiles) > 0:
    print("files to convert: " + str(len(lumDatFiles)))
    beginTime = time.monotonic()
    for aFile in lumDatFiles:
      print("converting " + aFile)
      mode2pic(sourcePath + aFile, xyMat, saveDir, saveOuts=1)
    endTime = time.monotonic()
    print("\ndone.")
    print("time elapsed:\t\t" + str(endTime - beginTime))
    print("average sec/file:\t" + str((endTime - beginTime)/len(lumDatFiles)))
  
  if winCmd:
    input("Press Enter to close.  This also closes all plot windows.\n" + \
          "If saveOuts == 1, then the plots will still be saved in\n" + \
          saveDir)
  
  
  
  
  
  
  
  
  
  
  
  
  
  