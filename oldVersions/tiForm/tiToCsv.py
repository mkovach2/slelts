'''
tiToCsv.py
ohm sensor
Author: miles @ hyperlightcorp.com
Created: 2022-04-20
Modified: 2022-04-21

This script will convert the output of a TI-TINA spice
simulation (saved as text) to a series of plots, separated
by variable name.
'''

import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# user defined:
saveMode = 0 #if 1, this program will save the output graphs
             #as PNGs

def AxScale(whichArray, numTicks):
  if type(whichArray) is np.ndarray:
    return (np.amax(whichArray) - np.amin(whichArray)) * np.arange(0, 1.1, 1/numTicks)
  else:
    return (whichArray * np.arange(0, 1.1, 1/numTicks))

if 1: #debugging_if
  pathe = input("path to file:\n").strip("\"")
else:
  pathe = r"C:\Users\miles.HYPERLIGHT\Documents\ohmSensor\tcurveeeeeeeeeeeee.txt"
pathe = re.sub(r'\\','/',pathe)
newPathe = re.sub('txt','csv',pathe)
patheStart = pathe.rsplit('/',1)[0]
if 0: #debugging_if
  print(pathe + '\n' + newPathe)

titleRow = np.genfromtxt(pathe, dtype = str)[0]
tiImport = np.genfromtxt(pathe, delimiter='\t', skip_header = 1)

xAx = tiImport[:,0]

pl1 = plt.figure(figsize=(11,8.5))
plotV = pl1.add_subplot()
pl2 = plt.figure(figsize=(11,8.5))
plotA = pl2.add_subplot()
pl3 = plt.figure(figsize=(11,8.5))
plotO = pl3.add_subplot()

plotV.set_xlabel(titleRow[0])
plotV.set_ylabel("Voltage (V)")
plotA.set_xlabel(titleRow[0])
plotA.set_ylabel("Current (A)")
plotO.set_xlabel(titleRow[0])
plotO.set_ylabel("Other")

iMax = 0
vMax = 0
oMax = 0

iLeg = []
vLeg = []
oLeg = []

for rNum in range(1,titleRow.size):
  if titleRow[rNum][0] == 'A':
    plotA.plot(xAx,tiImport[:,rNum])
    iMax = max(iMax,np.amax(tiImport[:,rNum]))
    iLeg.append(titleRow[rNum])
  elif titleRow[rNum][0] == 'V':
    plotV.plot(xAx,tiImport[:,rNum])
    vMax = max(vMax,np.amax(tiImport[:,rNum]))
    vLeg.append(titleRow[rNum])
  else:
    plotO.plot(xAx,tiImport[:,rNum])
    oMax = max(oMax,np.amax(tiImport[:,rNum]))
    oLeg.append(titleRow[rNum])
  
plotV.legend(vLeg)
plotA.legend(iLeg)
plotO.legend(oLeg)

numTicksX = 10
numTicksY = 15
plotV.set_xticks(AxScale(xAx,numTicksX))
plotA.set_xticks(AxScale(xAx,numTicksX))
plotO.set_xticks(AxScale(xAx,numTicksX))
plotV.set_yticks(AxScale(vMax,numTicksY))
plotA.set_yticks(AxScale(iMax,numTicksY))
plotO.set_yticks(AxScale(oMax,numTicksY))

plotV.grid(True)
plotA.grid(True)
plotO.grid(True)

if saveMode:
  nowe = datetime.now()
  realNow = datetime.strftime(nowe,"%Y%m%d%H%M")
  pl1.savefig(patheStart + "/Voltage_" + realNow + ".png")
  pl2.savefig(patheStart + "/Current_" + realNow + ".png")
  if len(oLeg) > 0:
    pl3.savefig(patheStart + "/Other_" + realNow + ".png")
  
