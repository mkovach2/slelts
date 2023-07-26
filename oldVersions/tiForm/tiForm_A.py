'''
tiForm.py
ohm sensor
Author: miles @ hyperlightcorp.com
Created: 2022-04-21
Modified: 2022-04-21

formats calculated columns into a nice grid.  will eventually be implemented
entirely in tiToCsv.py as a function
'''
import re
import numpy as np

def tiForm(pathe):
  
  typeArr = {}
  contentArr = {}
  
  pathe = re.sub(r'\\','/',pathe)
  newPathe = re.sub('txt','csv',pathe)
  patheStart = pathe.rsplit('/',1)[0]
  if 0: #debugging_if
    print(pathe + '\n' + newPathe)
  
  tiFile = open(pathe, "r")
  for line in tiFile:
    if not(line.isspace()):
      line = line.strip()
      lineList = re.split('\s+',line)
      if not(line[0][0].isnumeric()):
        headList = lineList
      if line[0][0].isnumeric():
        for linePos in range(1,len(lineList)):
          hllp = headList[linePos] # heading retrieved from the last non-
                                   # ... numeric line
          LLLp = lineList[linePos] # data corresponding to the heading at hllp
          if not(hllp in contentArr.keys()) \
             or (contentArr[hllp] is None):
            if 0: #debugging_if
              print("contentarr:\t\t\t",contentArr)
              print("headList[linePos]: ",hllp)
              print("headList: ",headList)
            contentArr[hllp] = np.array([float(lineList[0]), float(LLLp)])
            if 0: #debugging_if
              print(contentArr[hllp],hllp)
          else:
            if 0: #debugging_if
              print("lineList[linePos]:\t\t\t",LLLp)
            contentArr[hllp] = np.vstack((contentArr[hllp],\
                                          [float(lineList[0]), float(LLLp)]))
          
  tiFile.close()
  return contentArr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  samplePath = r"C:\Users\miles.HYPERLIGHT\Documents\ohmSensor\sampleF.txt"
  print(tiForm(samplePath))