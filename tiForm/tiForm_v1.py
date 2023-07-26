'''
tiForm_v1.py
ohm sensor
Author: miles @ hyperlightcorp.com
Created: 2022-04-21
Modified: 2022-04-22

plots data from a ti-tina "export to txt" file, and exports it as a csv.
also allowes you to do stats.
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  from datetime import datetime
  import matplotlib.pyplot as plt
  import tiForm_funcs as tff
  import numpy as np
  
  #User Set Block~~~~~~~~~~~~~~~~~~
  defaultPathe = \
    r"C:\Users\miles.HYPERLIGHT\Documents\ohmSensor\curvewithdr_2.txt"
  numTicksX = 11
  numTicksY = 16
  
  customMinX = 0
  customMinY = 0
  customXlabel = 1 #set to 0 to automatically label axis "Time (s)"
                   #set to 1 to prompt user for X labels
  doPlots = 0
  plotsSave = 0
  csvSave = 1
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
  if 1: #debugging_if
    pathe = input("path to file:\n").strip("\"")
  else:
    pathe = ''
    
  if pathe == '':
    pathe = defaultPathe
    
  getTiForm = tff.tiForm(pathe)
  allData = getTiForm["contentArr"]
  if 0:
    allData = {key: value for key, value in sorted(allData.items())}
    # ^ don't need to do this, but its kind of nice to have here
  
  plottedParams = []
  plotsMade = {}
  paramLeg = []
  Xbounds = [customMinX,customMinX]
  Ybounds = [customMinY,customMinY]
  if customXlabel == 0:
    xLab = "Time (s)"
  else:
    xLab = input("Enter X Label:\n")
  
  if doPlots:     
    for param in allData.keys():
      #if not(param[0] in plottedParams):
      if (len(plottedParams) == 0) or (param[0] != plottedParams[-1]):
        if (len(plottedParams) != 0):
          paramLeg = []
          onePlot.grid(True)
          onePlot.set_yticks(np.linspace(Ybounds[0],Ybounds[1],numTicksY))
          onePlot.set_xticks(np.linspace(Xbounds[0],Xbounds[1],numTicksX))
          Xbounds = [np.amin(allData[param][:,0]),np.amax(allData[param][:,0])]
          Ybounds = [np.amin(allData[param][:,1]),np.amax(allData[param][:,1])]
        
          Xbounds = [min(np.amin(allData[param][:,0]),customMinX),\
                     np.amax(allData[param][:,0]) * 1.1]
          Ybounds = [min(np.amin(allData[param][:,1]),customMinY),\
                     np.amax(allData[param][:,1]) * 1.1]
        
        plottedParams.append(param[0])
        plotsMade[param[0]] = plt.figure(figsize=(11,8.5))
        onePlot = plotsMade[param[0]].add_subplot()
        onePlot.set_xlabel(xLab)
        onePlot.set_ylabel(param[0])
        
      Xbounds = [min(np.amin(allData[param][:,0]),Xbounds[0]),\
                 max(np.amax(allData[param][:,0]),Xbounds[1])]
      Ybounds = [min(np.amin(allData[param][:,1]),Ybounds[0]),\
                 max(np.amax(allData[param][:,1]),Ybounds[1])]
      paramLeg.append(param)
      onePlot.plot(allData[param][:,0],allData[param][:,1])
      onePlot.legend(paramLeg)
      
      if 0: #debgging_if
        print(allData[param][:,0],allData[param][:,1])
      
    onePlot.legend(paramLeg)
    onePlot.grid(True)
    onePlot.set_yticks(np.linspace(Ybounds[0],Ybounds[1],numTicksY))
    onePlot.set_xticks(np.linspace(Xbounds[0],Xbounds[1],numTicksX))
    if 0: #debugging_if
      print(allData)
    
  if plotsSave or csvSave:
    nowe = datetime.now()
    realNow = datetime.strftime(nowe,"%Y%m%d%H%M")
  if plotsSave:
    for plotItem in plottedParams:
      plotsMade[plotItem].savefig(getTiForm["patheStart"] + getTiForm["patheEnd"] + "_" + plotItem + \
                                  "_" + realNow + ".png")


[csvReady,dataKeys] = list(tff.csvForm(allData))
statMat = tff.doStats(csvReady)
[csvStats,statKeys] = list(tff.csvForm(statMat))
csvStats = csvStats.T

if csvSave:
  tff.csvSave([csvReady,dataKeys],getTiForm["patheStart"],getTiForm["patheEnd"])
  tff.csvSave([csvStats,statKeys],getTiForm["patheStart"],getTiForm["patheEnd"] + "_stats",0)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  