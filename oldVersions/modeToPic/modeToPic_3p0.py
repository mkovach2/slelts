'''
modeToPic_3p0.py
hyperlight : modeConverter
Author: miles @ hyperlightcorp.com
Created: 2022-06-22
Modified: 2022-08-04 miles @ hyperlightcorp.com

takes a directory containing files of raw data exported by lumerical 
and creates a mode illustration of each.

this version should be able to look over a directory and 
convert all the files that end with "rawData.txt" or "matData.txt"

1--------10--------20--------30--------40--------50--------60--------70--------
'''
wincmd = 1 # a bool to set if you plan to run this from the windows
           # command line
           
versionNumber = "1.0"

if 0: # debugging_if
  userPath = input("enter path to your cloud's file called " +\
                   "\"Hyperlight Corporation\".\nFor example, user \"miles\""+\
                   " might type\n" + "C:/Users/miles.HYPERLIGHT/\n"+\
                   "(with no quotes)\t:\n")
else:
  userPath = "C:/Users/miles.HYPERLIGHT/"

if userPath[-1] != "/":
  userPath += "/"

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import sys
from datetime import datetime
import re # regexes will help with a prior format of outputs

priorWd = os.getcwd()
  
sys.path.append(userPath + "HyperLight Corporation/"+\
                "HyperLight General - General/miles/pyScripts")
from goodToHave import tryUntilGood # function that appends a number to an
                                    # output file if a file with that name
                                    # already exists in the directory
os.chdir(priorWd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

def stretchMat(matrIn,axIn,axis_=0,shouty=0): # requires numpy
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

def mode2pic(fileIn, save_presets = {}, plot_presets = {},\
             saveOuts=1,plotOuts=1,forceAxes=0,matrices=["EsqOut","nZ"],\
             imageMeta = {},renameWithNumbers=0):
  '''
  The hardcore function that does the work of this script.
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
        rD[keye] = np.transpose(np.reshape(rD[keye],\
                      [len(rD['xMat']),len(rD['yMat'])]))
        if saveOuts:
          outName = fileIn.rpartition('.')[0] + "_" + keye
          outNameX = outName + "_xMat"
          outNameY = outName + "_yMat"
          if(0): #debugging_if
            print(outName)
          if renameWithNumbers:
            outName = tryUntilGood(os.getcwd() + '/',outName + ".npy")
            outNameX = tryUntilGood(os.getcwd() + '/',outNameX + ".npy")
            outNameY = tryUntilGood(os.getcwd() + '/',outNameY + ".npy")
           # outName = tryUntilGood(fileIn.rpartition('\\')[0] + "\\",\
            #                       fileIn.rpartition('\\')[-1])
            #print(outName.rpartition('\\')[0] + "\\")
            if 0: #debugging_if
              print(fileIn.rpartition('\\'))
          np.save(outName,rD[keye])
          np.save(outNameX,rD["xMat"])
          np.save(outNameY,rD["yMat"])
       
        if 0: # leave this as zero usually.   set to "1" to output uncorrected
              # images with a focus on the mode, sort of pseudo-log-scale
          (newMat,dx,longX) = (rD[keye], rD['xMat'], rD['xMat'])
          (newMat,dy,longY) = (rD[keye], rD['yMat'], rD['yMat'])
        #end if
        else:
          (newMat,dx,longX) = stretchMat(rD[keye], rD['xMat'],axis_=1)
          (newMat,dy,longY) = stretchMat(newMat, rD['yMat'], axis_=0)
        
        if plt.get_fignums() == []:
          figNo = 1
        else:
          figNo = max(plt.get_fignums()) + 1
        #end if
        if (plotOuts or (inFn.lower() == "matdata.txt") or forceAxes):
          if not(plotOuts):
            plt.close("all")
          #end if
          plt.figure(num=figNo,figsize=(12,12))
          ax = plt.subplot()
          plt.imshow(newMat,**plot_presets)
          axTicX = np.linspace(0,len(longX),int(10*26/19))
          axTicY = np.linspace(0,len(longY),10)
          ax.set_xticks(axTicX.astype(int), \
                        np.around(longX[axTicX.astype(int)-1]/10**-6,1))
          ax.set_yticks(axTicY.astype(int), \
                        np.around(longY[axTicY.astype(int)-1]/10**-6,1))
          plt.title(keye + " " + fileIn.rpartition('.')[0])
          plt.xlabel("um")
          plt.ylabel("um")
          divider = make_axes_locatable(ax)
          colorbar_axes = divider.append_axes("right", size="3%", pad="1%")
          colorbar_axes.set_yticks([1,2,3,4,5])
          plt.colorbar(cax=colorbar_axes)
        
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
#end function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  
  colorScheme = 'jet' #also consider 'turbo'
  
  if 1: # debugging_if
    plt.close("all")
  
  if 1: # debugging_if
    pathToData = input("paste path to directory containing data files,\n"+\
                       "or one individual file to convert:\n")
    pathToData = pathToData.replace('\\','/')
    pathToData = pathToData.strip('\"') # remove quotes
    if pathToData[-1] != '/' and \
       pathToData[-4:] != ".txt":
         pathToData += '/' # add a trailing slash
    if (0): #debugging_if
      print(pathToData)
  else:
    pathToData = userPath + "HyperLight Corporation/HyperLight " +\
                 "General - General/Simulations/Lumerical_Miles/"+\
                 "modeConverter/deleet soone/fattuy_rawData.txt"
                             
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
    'filternorm'    : False
  }
  
  priorWd = os.getcwd() # getting current dir to return to after running
  if pathToData[-4:] == ".txt":
    if pathToData[0:8] == "file:///":
      pathToData = pathToData[8:]
    filesToDo = [pathToData.rpartition("/")[-1]]
    os.chdir(pathToData.rpartition("/")[0])
    allIn = [filesToDo[0]]
    fileName = filesToDo[0]
  else:
    os.chdir(pathToData)
    allIn = os.listdir(pathToData)
    filesToDo = []
    for fileName in allIn:
      inFn = fileName.rpartition('_')[-1]
      if inFn.lower() in ("matdata.txt","rawdata.txt","lumdat.txt"):
        # "lumdat" is a legacy suffix. dont name anything new lumdat.
        filesToDo.append(fileName)
      #end if
    #end for
  print(os.getcwd())
  # suppressing plots on large file counts, except where necessary
  showPlots = 1
  if len(filesToDo) > 5:
    ySlashN = input("This folder contains " + str(len(filesToDo)) +\
                    " files to convert.  suppress plots (Y/n)? ")
    if ySlashN.lower() != 'n':
      showPlots = 0
    # end if
  # end if
  
  sPrompt = "not_set_yet"
  
  # below: "force Axes": this makes the exported mode plots have 
  # axes and stuff, not unlike the material data plots
  fax = input("output mode images with axes (Y/n)?\n")
  if fax.lower() == 'n':
    fax = 0
  else:
    fax = 1
    
  for fileA in range(len(filesToDo)):
    print("working on " + filesToDo[fileA])
    doSave = 1
    reNum = 1
    
    if(filesToDo[fileA].rpartition(".")[0] + ".png" in allIn) or\
      (filesToDo[fileA].rpartition(".")[0] + ".npy" in allIn):
      if sPrompt == "not_set_yet":
        sPrompt = input(\
          "Some of the files in the destination folder\n"+\
          "have the same names as the ones to be created.\n"+\
          "how should these be handled?\n"+\
          "\"0\"	skip these files (default)\n"+\
          "\"1\"	overwrite the existing files\n"+\
          "\"2\"	keep both files, with a number appended to the new one\n")
      #end if sPrompt == "not_set_yet"
      if sPrompt == "2":
        doSave = 1
        reNum = 1
      elif sPrompt == "1":
        doSave = 1
        reNum = 0
      else:
        doSave = 0
        reNum = 0
      #end if sPrompt == "2"
    #end very long if

    imageMetadata = { # these follow the suggestions of the PNG spec
      "Description" : "waveguide mode generated from raw data exported by "+\
                      "Lumerical MODE",
      "Copyright" : "probably Hyperlight, probably current year, idk #FIfXME",
      "Creation Time" : str(datetime.utcnow()),
      "Software" : "modeToPic, version " + versionNumber,
      "Source File" : fileName
    }
    
    mode2pic(filesToDo[fileA],\
             plot_presets=plot_p,\
             save_presets=save_p,\
             saveOuts=doSave,\
             forceAxes=fax,\
             plotOuts=showPlots,\
             matrices=["EsqOut","nZ"],\
             imageMeta=imageMetadata,\
             renameWithNumbers=reNum)

    if (wincmd and showPlots):
      plt.show(block=False)
    print(str(fileA + 1) + " of " + str(len(filesToDo)) + " done")
  
  os.chdir(priorWd) # yes

  if wincmd:
    input("\nfinished.  press enter to close.\n")
  else:
    print("\nfinished.")

# bonus track: it's the regex that matches the imaginary parts of complex
#              numbers again : r"\+\d+\.?(\d+)?i"

































