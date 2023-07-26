'''
modeToPic_4p0.py
hyperlight : modeConverter
Author: miles @ hyperlightcorp.com
Created: 2022-06-22
Modified: 2022-08-10 miles @ hyperlightcorp.com

takes a directory containing files of raw data exported by lumerical 
and creates a mode illustration of each.

this version should be able to look over a directory and 
convert all the files that end with "rawData.txt" or "matData.txt"

1--------10--------20--------30--------40--------50--------60--------70--------
'''
wincmd = 0 # a bool to set if you plan to run this from the windows
           # command line
           
versionNumber = "4.0"

if 0: # debugging_if
  userPath = input("enter path to your cloud's file called " +\
                   "\"Hyperlight Corporation\".\nFor example, user \"miles\""+\
                   " might type\n" + "C:/Users/miles.HYPERLIGHT/\n"+\
                   "(with no quotes)\t:\n")
else:
  userPath = "C:/Users/miles.HYPERLIGHT"

if userPath[-1] != "/":
  userPath += "/"
#end if userPath[-1] != "/"

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import sys
from datetime import datetime
import re # regexes will help with a prior format of outputs

priorWd = os.getcwd()
  
sys.path.append(userPath + "/HyperLight Corporation/"+\
                "HyperLight General - General/miles/pyScripts")
from goodToHave import tryUntilGood # function that appends a number to an
                                    # output file if a file with that name
                                    # already exists in the directory
import crossAtMaxSuite as cams
# includes functions needed to support this program

os.chdir(priorWd)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  
  colorScheme = 'jet' #also consider 'turbo'
  mOverlays = {} # a dict to keep the material data overlays
  
  stretchIt = 0
  matBounds = 1
  
  if 1: # debugging_if
    plt.close("all")
  #end debugging_if
  
  if 0: # debugging_if
    pathToData = input("paste path to directory containing data files,\n"+\
                       "or one individual file to convert:\n")
    pathToData = pathToData.replace('\\','/')
    pathToData = pathToData.strip('\"') # remove quotes
    if pathToData[-1] != '/' and \
       pathToData[-4:] != ".txt":
         pathToData += '/' # add a trailing slash
    #end if pathToData[-1]
    if (0): #debugging_if
      print(pathToData)
      #end debugging_if
  #end debugging_if
  else:
    pathToData = userPath + "HyperLight Corporation/HyperLight " +\
                 "General - General/Simulations/Lumerical_Miles" +\
                 "/modeConverter/fullSuite_tests/20220809"
  #end else
                           
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
  
  contour_p = {
    "num_of_contours" : 1, # each contour n represents the 1/(ne^2) field
    "thiccLine"       : stretchIt
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
    mDfiles = [] # to ensure the matdata files get done first, so that 
                 # there is data to superimpose if need be
    for fileName in allIn:
      inFn = fileName.rpartition('_')[-1]
      if inFn.lower() == "matdata.txt":
        mDfiles.append(fileName)
      #end if inFn.lower() == "matdata.txt"
      elif inFn.lower() in ("rawdata.txt","lumdat.txt"):
        # "lumdat" is a legacy suffix. dont name anything new lumdat.
        filesToDo.append(fileName)
      #end elif
    #end for fileName in allIn
  print(os.getcwd())
  # suppressing plots on large file counts, except where necessary
  showPlots = 1
  filesToDo = mDfiles + filesToDo
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
  
  if 1: #debugging_if
    fax = 1
  #end deubugging_if
  else:
    fax = input("output mode images with axes (Y/n)?\n")
    if fax.lower() == 'n':
      fax = 0
    else:
      fax = 1
  #end else
  
  for fileA in range(len(filesToDo)):
 # for fileA in [0]:
    print("working on " + filesToDo[fileA])
    doSave = 1
    reNum = 1
    
    if(filesToDo[fileA].rpartition(".")[0] + ".png" in allIn or
      filesToDo[fileA].rpartition(".")[0] + ".npy" in allIn):
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
    
    cams.mode2pic(
      filesToDo[fileA],
      plot_presets = plot_p,
      save_presets = save_p,
      stretch = stretchIt, # if 1, mode will be actual scale.  else, equal mesh squares
      saveOuts = doSave,
      forceAxes = fax,
      plotOuts = showPlots,
      contour = 1,
      grid = 1,
      showMatl = matBounds,
      overlayDict = mOverlays, # a dict to keep the material data overlays
      contour_presets = contour_p,
      matrices = ["EsqOut","nZ"],
      imageMeta = imageMetadata,
      renameWithNumbers = reNum
    )# end mode2pic

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

































