'''
crossAtMax2.py
lumSweep project
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: 2022-08-17

a set of functions useful in converting raw lumerical output files to images
of modes

1--------10--------20--------30--------40--------50--------60--------70--------
'''

userPath = "C:/Users/miles.HYPERLIGHT"

hlgg = userPath + "/HyperLight Corporation/"+\
       "HyperLight General - General"
       
import sys
import os

firstDir = os.getcwd()

sys.path.append(hlgg + "/miles/pyScripts")

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import re # regexes will help with a prior format of outputs

from goodToHave import tryUntilGood

euler = 2.7182818284590452353602874
bAlph = ListedColormap(([1,1,1,0],[1,1,1,1])) #for transparent layer
bAlphPink = ListedColormap(([1,1,1,0],[1,0.5,0.5,1]))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getRD(lumRDfile): # this function takes a single raw-data text file
                      # and separates the individual data matrices into
                      # items in a numpy array
  lumRDfile=lumRDfile.strip("\"") # strip of quotes
  
  lrd = open(lumRDfile)
  fulltext = lrd.read()
  lrd.close()
  
  fulltext = re.sub(r"(\~[a-zA-Z]+)(\n)",r"\1~\2",fulltext)
  
  fulltext = fulltext.split('~')
  #print(len(fulltext))
  if(0): #debugging_if
    for p in fulltext:
      print(p[0:6])
  rawNumpy = {}
  for rawItem in fulltext:
    if(0): #debugging_if
      print("dooky:\t" + rawItem[0:25])
    if (len(rawItem) > 0) and (rawItem.isalpha()):
      if(0): #debugging_if
        print("HUUUUDGE\n")
      aKey = rawItem
    elif len(rawItem) > 0:
      rawItem = re.sub(r"\+\d+\.?(\d+)?i","", rawItem)
      # ^this removes the imaginary parts of all the entries in data files
      # created before i fixed my script to only export reals
      # luv, miles @ hyperlightcorp.com
      rawNumpy[aKey] = np.fromstring(rawItem,sep='\t')
      if (0): #debugging_if
        print("hmm" + aKey + str(np.shape(rawNumpy[aKey])))
      #print(rawNumpy[aKey])
      
  return rawNumpy

  # the two ways windows pastes paths
  # C:\Users\miles.HYPERLIGHT\Documents\pyScripts\oldVersions\modeToPic
  # "C:\Users\miles.HYPERLIGHT\Documents\pyScripts\oldVersions\modeToPic"
#end def getRD(lumRDfile)



def stretchMat(matrIn,axIn,axis_=0,shouty=1): # requires numpy
  #import numpy as np.  # just uncomment this if its the only thing
  # that needs numpy or if declaring the function independently
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
  longAxis = np.repeat(axIn[:-1],dRatio.astype(int))
  return (matrOut,d,longAxis)
#end def stretchMat(matrIn,axIn,axis_=0,shouty=0)



def mf_contour(npy_in,num_of_contours = 1,thiccLine = 0):
  
  if type(npy_in) == list:
    lumNp = npy_in[0]
    xax = npy_in[1]
    yax = npy_in[2]
  #end if fromFile
  else:
    shortName = npy_in.rpartition('.')[0]
    fileX = shortName + "_xMat" + ".npy"
    fileY = shortName + "_yMat" + ".npy"
  
    lumNp = np.load(npy_in)
    xax = np.load(fileX)
    yax = np.load(fileY)
  #end else
  
  rows = 0
  cols = 1 
  
  expand = 0
  if expand and type(npy_in) != list:
    (lumNp,lel,xax) = stretchMat(lumNp,xax,axis_=cols)
    (lumNp,lel,yax) = stretchMat(lumNp,yax,axis_=rows)
  #end if expand
  else:
    (lumNp,lel,xax) = (lumNp,xax,cols)
    (lumNp,lel,yax) = (lumNp,yax,rows)
  #end else
  
  oldTmd = np.zeros(np.shape(lumNp))
  
  for contLevel in np.arange(1,num_of_contours + 1,1):
    truthMat = (lumNp >= 1/(contLevel * euler**2))
    # a contour which separates the MFD inside from outside
    
    if thiccLine: #thicc version
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
    
    tMd += oldTmd
    oldTmd = tMd

  return tMd
  
    # implement later
    # tmdWhere = np.where(tMd)
    # tMux = np.unique(tmdWhere[0],return_index=1)[1]
    # tMuy = np.unique(tmdWhere[1],return_index=1)[1]
    
    # xMaxs = []
    # for xUn in np.arange(1:len(tMux)):
    #   xmaxs[xUn] = 
    
    #lumNp1 = lumNp[0:-1,0:-1]
  #end   for contLevel in np.arange(1,num_of_contours + 1,1)
  
  # bAlph = ListedColormap(([1,1,1,0],[1,1,1,1]))
  # plots bottom-half values as transparent, top-half values as white
  # ex:
  # plt.imshow(tMd,cmap=bAlph,vmin=0,origin='lower')
  # now you can put clear overlays on your graphs!
  
#end def mf_contour()


def material_outline(npy_in,fileNameOut,thiccLine = 1):
    if thiccLine: #thicc version
      matMaty = (npy_in[:-3,:] != npy_in[3:,:])
      matMatx = (npy_in[:,:-3] != npy_in[:,3:])
      matOut = np.zeros(np.shape(npy_in))
      matOut[2:-1,1:-2] = matMatx[:-3,:] + matMaty[:,:-3] + matMatx[3:,:] + matMaty[:,3:]
    #end if 1: #thicc version
    else:
      matMaty = (npy_in[:-1,:] != npy_in[1:,:])
      matMatx = (npy_in[:,:-1] != npy_in[:,1:])
      matOut = np.zeros(np.shape(npy_in))
      matOut[1:,:-1] = matMatx[:-1,:] + matMaty[:,:-1] + matMatx[1:,:] + matMaty[:,1:]  
    #end else
    np.save(fileNameOut,matOut)
    return(fileNameOut + '.npy')
#end def material_outline(npy_in,num_of_contours = 1,thiccLine = 0)


def niceTile(newMat,longX,longY,plotPresets = {},grid=1):
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
    vpix = resLim[0]
    hpix = len(longX)/len(longY) * vpix
  #end if len(longX)/len(longY):
  else:
    hpix = resLim[1]
    vpix = len(longY)/len(longX) * hpix
  #end else
  dpi_ = 160
  
  plt.figure(num=figNo,figsize=(hpix/dpi_,vpix/dpi_),dpi=dpi_)
  ax = plt.subplot()  
  
  numXticks = 2 * int(10*hpix/vpix)
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
    numYticks += not(np.mod(numYticks,2))
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
  
  if len(xL) == 1 and type(xL[0]) == np.ndarray:
    xL = xL[0]
  #end if type(xL[0]) == np.ndarray
  
  if len(yL) == 1 and type(yL[0]) == np.ndarray:
    yL = yL[0]
  #end if type(xL[0]) == np.ndarray
  
  ax.set_xticks(axTicX, xL)
  ax.set_yticks(axTicY, yL)
  #plt.title(keye + " " + fileIn.rpartition('.')[0])
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
  plt.imshow(newMat,**plotPresets)
  #────────────────██──────────────────█───────███─────────
  #─────────────────█──────────────────█──────────█────────
  #──███────███─────█─────███────███───████────████───███──
  #─█──────█───█────█────█───█──█───█──█───█──█───█──█───█─
  #──███────███─────██────███───█──────████────████──█─────

  divider = make_axes_locatable(ax)
  colorbar_axes = divider.append_axes("right", size="3%", pad="1%")
  colorbar_axes.set_yticks([1,2,3,4,5])
  plt.colorbar(cax=colorbar_axes)
  
  return colorbar_axes,ax
#end def niceTile(newMat,longX,longY,plotPresets = {})



def mode2pic(fileIn, save_presets = {}, plot_presets = {},crop_um = (None,None),
             stretch = 1,saveOuts=1,plotOuts=1,forceAxes=0,matrices=["EsqOut","nZ"],
             contour = 0, grid = 0, showMatl = 0,overlayDict = {}, 
             contour_presets = {},imageMeta = {},renameWithNumbers=0):
  '''
  fileIn is of course the file to be converted (or rejected if not 
    named in a compatible way),
  presets is a dict of user presets for the "plt.imsave" function,
    and should be specified in __main__.
  saveOuts is a bool to be set if you want to save the output images, and
    cleared if you only want to view the image generated without saving.
  matrices is a list of strings for possible names of matrices to convert 
    to images, in the case of raw data inputs that contain more than one 
    identically-sized matrix of data, excluding the 1-dimensional matrices 
    which represent the X and Y axes.  You may specify as many names as
    you would like in this list; the function will check whether a given
    matrix is in the list before converting it.  The two default values
    match the names of the electric field intensity and refractive index
    in the z-direction, as output by the lumerical script "lumSweep_2p0.lsf"
    
    modified 2022-10-12 miles at hyperlightcorp dot com
  '''
  inFn = fileIn.rpartition('_')[-1]
  
  if inFn.lower() in ("matdata.txt","rawdata.txt","lumdat.txt"):
    # "lumdat" is a legacy suffix. dont name anything new lumdat.
    if inFn.lower() == "lumdat.txt":
      rD = {
        "EsqOut" : np.transpose(np.loadtxt(fileIn, delimiter = '\t', unpack=True))
      }
      rD["xMat"] = np.arange(np.shape(rD["EsqOut"])[0])*10**-6
      rD["yMat"] = np.arange(np.shape(rD["EsqOut"])[1])*10**-6
    else:
      rD = getRD(fileIn)

    for keye in rD.keys():
      if keye in matrices:
        if 0: #debugging_if
          print("eeeeeeee",[len(rD['xMat']),len(rD['yMat'])])
        #end if 0: #debugging_if
        rD[keye] = np.transpose(np.reshape(rD[keye],\
                      [len(rD['xMat']),len(rD['yMat'])]))
        if 0: #debugging_if
          print("PRRRRRRRRRT",[len(rD['xMat']),len(rD['yMat'])])
        #end if 0: #debugging_if
        if saveOuts:
          if not(os.path.exists(os.getcwd() + "/numpy_arrays")):
            os.mkdir("numpy_arrays")
          #end if not(os.path.exists(os.getcwd() + "/numpy_arrays"))
          os.chdir("numpy_arrays")
          outName = fileIn.rpartition('.')[0] + "_" + keye
          outNameX = outName + "_xMat"
          outNameY = outName + "_yMat"
          if(0): #debugging_if
            print(outName)
          #end if 0: #debugging_if
          if renameWithNumbers:
            outName = tryUntilGood(os.getcwd() + '/',outName + ".npy")
            outNameX = tryUntilGood(os.getcwd() + '/',outNameX + ".npy")
            outNameY = tryUntilGood(os.getcwd() + '/',outNameY + ".npy")
           # outName = tryUntilGood(fileIn.rpartition('\\')[0] + "\\",\
            #                       fileIn.rpartition('\\')[-1])
            #print(outName.rpartition('\\')[0] + "\\")
            if 0: #debugging_if
              print(fileIn.rpartition('\\'))
            #end if 0: #debugging_if
          np.save(outName,rD[keye])
          np.save(outNameX,rD["xMat"])
          np.save(outNameY,rD["yMat"])
          os.chdir('..')
        
        fPrefix = "0000"
        for npart in fileIn.split('_'):
          if npart.isnumeric() and len(npart) > 4:
            fPrefix = npart
            break
          #end if isnumeric(npart)
        #end for npart in fileIn.split('_')
        if not(stretch):
              # images with a focus on the mode, sort of pseudo-log-scale
          (newMat,dx,longX) = (rD[keye], rD['xMat'], rD['xMat'])
          (newMat,dy,longY) = (rD[keye], rD['yMat'], rD['yMat'])
        #end if
        else:
          (newMat,dx,longX) = stretchMat(rD[keye], rD['xMat'],axis_=1)
          (newMat,dy,longY) = stretchMat(newMat, rD['yMat'], axis_=0)

        xCroppy = np.arange(np.shape(newMat)[0])
        yCroppy = np.arange(np.shape(newMat)[1])
        
        # print('xCroppy = ' + str(xCroppy))
        # print('yCroppy = ' + str(yCroppy))
        
        if not(crop_um[0] == None):
          xCroppy = np.nonzero((longX >= -crop_um[0]*10**-6)*(longX <= crop_um[0]*10**-6))[0]
          longX = longX[xCroppy]
        #end if not(crop_um == (None,None))

        if not(crop_um[1] == None):
          yCroppy = np.nonzero((longY >= -crop_um[1]*10**-6)*(longY <= crop_um[1]*10**-6))[0]
          longY = longY[yCroppy]
        #end if not(crop_um == (None,None))
        
        newMat = newMat[xCroppy,:]
        newMat = newMat[:,yCroppy]
        
        # newMat = newMat[:,xCroppy][yCroppy,:]
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        (nTn,ax) = niceTile(newMat,longX,longY,plot_presets)
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        
        #──███────█───────────────────────────█────────────────────███──
        #─█───────█───────────────────────────█───────────────────█───█─
        #──███───█████───███───█───█───███───█████──█───█───███───█████─
        #─────█───█─────█───█──█───█──█───────█─────█───█──█───█──█─────
        #──███─────███──█───────███────███─────███───███───█───────████─
        
        if inFn.lower() == "matdata.txt" and showMatl:
          print(fPrefix)
          # overlayDict[fPrefix] = material_outline(newMat,fPrefix,thiccLine = stretch)
          overlayDict[fPrefix] = material_outline(newMat,fPrefix,thiccLine = 0)
        #end if inFn.lower() == "matdata.txt" and showMatl
        elif showMatl:
          kErr=0
          try:
            overlay = np.load(overlayDict[fPrefix])
            ax.imshow(
              overlay,
              cmap=bAlphPink,
              vmin=0,
              origin='lower'
            )#end ax.imshow
          #end try
          except:
            print("whoopsie the materieal files is missing for this one");
            kErr = 1
          #end except KeyError
          # if not(kErr):
          #   os.remove(overlayDict[fPrefix])
          # #end if not(kErr)
        #end elif showMatl
        
        #───────────────────────█─────────────────────────
        #───────────────────────█─────────────────────────
        #──███────███───████───█████───███───█───█───███──
        #─█──────█───█──█───█───█─────█───█──█───█──█───█─
        #──███────███───█───█────███───███────███───█─────
        
        if contour and (inFn.lower() == "rawdata.txt"):
          ring1 = mf_contour(
            [newMat,longX,longY],
            **contour_presets
          )#end mf_contour
          #bAlph = ListedColormap(([1,1,1,0],[1,1,1,1]))
          ax.imshow(ring1,cmap=bAlph,vmin=0,origin='lower')
        #end if contour
        
        plt.colorbar(cax=nTn)

        if forceAxes:
          faxStr = "_fAx"
        else:
          faxStr = ""
        
        if saveOuts:
          outName = os.getcwd() + '\\' + \
                    fileIn.rpartition('.')[0] + faxStr + ".png"
          if renameWithNumbers:
            outName = tryUntilGood(outName.rpartition('\\')[0] + "\\",\
                                   outName.rpartition('\\')[-1])
          print(outName)
          if inFn.lower() == "matdata.txt" or forceAxes:
            plt.savefig(outName,metadata=imageMeta)
          elif inFn.lower() in ("rawdata.txt","lumdat.txt"):
            plt.imsave(outName,newMat,**save_presets,metadata=imageMeta)
      #end if keye in matrices
    #end for keye in rD.keys()[1:]
  #end if inFn.lower() in ("matdata.txt","rawdata.txt","lumdat.txt")
  return overlayDict
#end def mode2pic



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  #huuhuuhuu
  0
#end if __name__ == "__main__"

  


  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
