'''
[file name]
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import os
import numpy as np
import sys

winCmd = 1

yourPath = "C:/Users/miles.HYPERLIGHT"

# adding HLcadlib to the path
winstr = yourPath + "/HyperLight Corporation/"+\
         "HyperLight General - General/miles/pyScripts"
         
sys.path.append(winstr)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  another = 1 # tells the script whether to repeat
  while(another):
    if winCmd:
      EMEpath = input("Enter path to EME output file:\n")
      EMEpath = EMEpath.replace("\\",'/')
      EMEpath = EMEpath.strip("\"\'")
    #end if 0
    else:
      EMEpath = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
        "Products - General/+NewFileSystem/Device Components/Mode Converter/"+\
        "20220922_civitanavi/simulation/yspl_power.txt"
    #end else
    
    foil = EMEpath.rpartition('/')
    
    sweepData = np.genfromtxt(EMEpath,delimiter = ",")
  
    notNum = np.argwhere(np.isnan(sweepData[:,0]))
    
    if not(np.size(notNum) == 0):
      h00=np.array(sweepData[notNum[0][0]:notNum[1][0],:])
      for nnRow in np.arange(1,len(notNum)-1):
        pleurf = sweepData[notNum[nnRow][0]:notNum[nnRow+1][0],1]
        h00 = np.hstack((h00,pleurf.reshape(np.shape(h00)[0],1)))
      #end for nnRow in notNum
      pleurf = sweepData[notNum[len(notNum)-1][0]:,1]
      h00 = np.hstack((h00,pleurf.reshape(np.shape(h00)[0],1)))
      
      hCols = np.shape(h00)[1]
      hLab = np.arange((hCols - 1.0)**0.5)+1
      hLab.resize(1,len(hLab))
      hLab = np.ravel(hLab*10+hLab.T)
      
      hLabStr = 'x,'
      for labelle in hLab:
        hLabStr += 's' + str(int(labelle)) + ','
      #end for labelle in hLab
    #end if not(notNum == [[0]])
    else:
      h00 = sweepData
    #end else
    outfName = foil[-1].split('.')[0] + "_np.csv"

    np.savetxt(foil[0] + '/' + outfName,h00[1:,:],header = hLabStr,delimiter=',')
    
    anoT = input("continue [Y/n] ?\n")
    if anoT.lower() == 'n':
      another = 0
    #end if anoT.lower() == 'n'
  #end while(another)
  
  if winCmd:
    closeMe = input("finished.  press Enter to close.")
  #end if winCmd
# end if __name__ == "__main__"