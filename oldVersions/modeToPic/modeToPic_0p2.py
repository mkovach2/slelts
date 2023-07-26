'''
modeToPic_0p2.py
hyperlight : modeConverter
Author: miles @ hyperlightcorp.com
Created: 2022-05-17
Modified: 2022-06-01 miles @ hyperlightcorp.com

takes a text file of raw data exported by lumerical 
and creates a mode illustration of it.

1--------10--------20--------30--------40--------50--------60--------70--------
'''

userPath = "C:/Users/miles.HYPERLIGHT/" # change this to reflect your path 
                                        # on the cloud

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def easyim(dataIn): # this one just plots with good presets
  return plt.imshow(dataIn, vmin=0, origin = 'lower', cmap='jet', aspect=1, \
                    interpolation='none',resample = False, filternorm=False)

def getRD(lumRDfile): # this function takes a single raw-data text file
                      # and separates the individual data matrices into
                      # items in a numpy array, and in turn arranges those
                      # numpy arrays into a neatly organized struct.
  lumRDfile=lumRDfile.strip("\"") # strip of quotes
  
  lrd = open(lumRDfile)
  fulltext = lrd.read()
  lrd.close()
  
  fulltext = fulltext.split('~')
  rawNumpy = {}
  for rawItem in fulltext:
    if (len(rawItem) > 0) and (rawItem.isalpha()):
      aKey = rawItem
    elif len(rawItem) > 0:
      rawNumpy[aKey] = np.fromstring(rawItem,sep='\t')
      
  return rawNumpy

  # the two ways windows pastes paths
  # C:\Users\miles.HYPERLIGHT\Documents\pyScripts\oldVersions\modeToPic
  # "C:\Users\miles.HYPERLIGHT\Documents\pyScripts\oldVersions\modeToPic"

def stretchMat(matrIn,axIn,axis_=0,shouty=0):
  d = axIn[1:] - axIn[:-1]
  dRatio = d/np.min(d)
  if axis_:
    if shouty:
      print(np.shape(matrIn))
      print("axis=" + str(axis_))
    mInIndex = matrIn[:,:-1]
  else:
    if shouty:
      print(np.shape(matrIn))
      print("axis=" + str(axis_))
    mInIndex = matrIn[:-1,:]
  matrOut = np.repeat(mInIndex,dRatio.astype(int),axis=axis_)
  return (matrOut,d)

priorWd = os.getcwd()
os.chdir(userPath + "HyperLight Corporation/HyperLight General - General/" + \
         "miles/pyScripts/")
from goodToHave import tryUntilGood # function that appends a number to an
                                    # output file if a file with that name
                                    # already exists in the directory
os.chdir(priorWd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":


  commonPath = userPath + "HyperLight Corporation/HyperLight " +\
               "General - General/Simulations/Lumerical_Miles/modeConverter/"
               
  sourceDir = "deleet soone/"
  inFn = "Mode_1550nmWL_200nmHeight_3400nmTop_62deg_7umBOX_830nmCLAD" +\
         "_1bgn_68813_matData.txt"
         
  #lumRDfile = input("lumRDfile?").replace('\\','/')
  #lumRDfile = commonPath + "gould/RAWWWW.txt"
  lumRD = commonPath + sourceDir + inFn
  #lumRD = commonPath + "deleet soone/fatty.txt"
  # bools which tell the program whether to save the newly generated NP arrays,
  # the stretched NP arrays, and the images created from those, respectively
  
  inFnSplit = inFn.rpartition('_')[-1]
  longFn = inFn.rpartition('.')[0] + '.png'
  if inFnSplit == "rawData.txt":
    mainMat = "EsqOut"
  elif inFnSplit == "matData.txt":
    mainMat = "nZ" # refractive index in Z, 
                   # but "nX" and "nY" are also available
  
  save_presets = {
    'format' : 'png',
    'vmin' : 0,
    'origin' : 'lower',
    'cmap' : 'jet'
    } 
  
  saveRDs = 1
  saveImages = 1
  
  rD = getRD(lumRD)
  rD[mainMat] = np.transpose(np.reshape(rD[mainMat],\
                 [len(rD['xMat']),len(rD['yMat'])]))
  (newMat,dx) = stretchMat(rD[mainMat], rD['xMat'],axis_=1)
  (newMat,dy) = stretchMat(newMat, rD['yMat'], axis_=0)
  
  fig, ax = plt.subplots()
  easyim(newMat)
  plt.title(longFn)
  divider = make_axes_locatable(ax)
  colorbar_axes = divider.append_axes("right", size="5%", pad=0.1)
  plt.show(block=False)
  
  plt.colorbar(easyim(newMat), cax=colorbar_axes)
  plt.title(mainMat)
  # FIXME: put these here
  
  # plt.xlabel(xLab)
  # plt.ylabel(yLab)
  
  for rdKey in rD.keys(): #pick up here
    if saveRDs:
      outData = tryUntilGood(commonPath + sourceDir, rdKey + ".npy")
      print("saving\n" + outData)
      np.save(outData, rD[rdKey])
      print("Done")
    if 0: # debugging_if
      print(rdKey)
  
  if saveImages:
    outImg = tryUntilGood(commonPath + sourceDir, longFn)
    print("saving\n" + outImg)
    plt.imsave(outImg,newMat,**save_presets)
    print("Done")
  print("Finished")
  
  
  
  
  
  
  
  
  
  
  
  
  