'''
tiForm_funcs.py
ohm sensor
Author: miles @ hyperlightcorp.com
Created: 2022-04-22
Modified: 2022-04-25

functions supporting tiForm_vX

1--------10--------20--------30--------40--------50--------60--------70--------
'''

import re
import numpy as np
from datetime import datetime

realNow = datetime.strftime(datetime.now(),"%Y%m%d%H%M")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def csvForm(dictIn: dict):
  '''
  inputs:
    dictIn (dict): a dictionary of numpy arrays to be converted to csv-friendly 
                   form
  outputs:
    csvReady (numpy array): the converted arrays, arranged as columns
    dataKee (list): headers of converted data
    
  remember to check your data.  It may need a transpose.
  This function doesn't do that automatically so that nesting it doesnt
  produce unexpected results.
  '''
  dataKee = list(dictIn)
  if 0: #debugging_if
    print(dataKee)
    print(dictIn[dataKee[0]])
  csvReady = np.array(dictIn[dataKee[0]])
  if len(csvReady.shape) == 1:
    csvReady = np.expand_dims(csvReady, 1)
  if 0: #debugging_if
    print(csvReady.shape)
  for param in dataKee[1:]:
    if len(dictIn[param].shape) == 1:
      dictIn[param] = np.expand_dims(dictIn[param], 1)
    csvReady = np.concatenate((csvReady,dictIn[param]),axis=1)
    if 0: #debugging_if
      print(csvReady.shape)
  #csvReady = np.transpose(csvReady)
  
  return [csvReady,dataKee]


def doStats(theNpArr: np.ndarray, analysAxis=0): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  inputs:
    theNpArr (np array): an array of raw data to be analyzed
    analysAxis (int): if 0, doStats performs the operation on the columns.
                      if 1, on the rows.
  
  outputs:
    statsDone (dict): a dictionary containing these stats about the input data
                      min, 15p, mean, median, 85p, max, sigma, range, 85p-15p
                      "15p" and "85p" are the 15th and 85th percentiles,
                      respectively
  '''
  if 0: #debugging_if
    print(theNpArr)  
  
  statsDone = {
    "min" : theNpArr.min(axis=analysAxis),
    "15p" : np.percentile(theNpArr, 15, axis=analysAxis),
    "mean" : theNpArr.mean(axis=analysAxis),
    "median" : np.median(theNpArr, axis=analysAxis),
    "85p" : np.percentile(theNpArr, 85, axis=analysAxis),
    "max" : theNpArr.max(axis=analysAxis),
    "sigma" : theNpArr.std(axis=analysAxis),
  }
  statsDone["range"] = statsDone["max"] - statsDone["min"]
  statsDone["85p-15p"] = statsDone["85p"] - statsDone["15p"]
  
  if 0: #debugging_if
    print(statsDone)
  
  return statsDone


def normStats(arrToNorm: np.ndarray, mu: np.ndarray, sigma: np.ndarray):
  return True


def tiForm(pathe): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  document this
  '''
  contentArr = {}
  
  pathe = re.sub(r'\\','/',pathe)
  newPathe = re.sub('txt','csv',pathe)
  patheStart = pathe.rsplit('/',1)[0] + "/"
  patheEnd = pathe.rsplit('/',1)[1]
  patheEnd = re.sub('.txt','',patheEnd)
  
  if 0: #debugging_if
    print(pathe + '\n' + newPathe)
  
  tiFile = open(pathe, "r")
  for line in tiFile:
    if not(line.isspace()):
      line = line.strip()
      lineList = re.split('\t+',line)
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
  return {
          "contentArr":contentArr,
          "patheStart":patheStart,
          "patheEnd":patheEnd,
          "newPathe":newPathe
          }


def csvSave(csvForm_in,patheS_in,patheE_in, horizLabels=1): #~~~~~~~~~~~~~~~~~~~
  '''
  inputs:
    horizLabels (bool): set to 1 for horizontal labels, 0 for vertical ones
  '''  
  (csvSubstance,dataSquees) = csvForm_in
  csvPath = patheS_in + patheE_in + "_" + realNow + ".csv"
  csvF = open(csvPath, "a")
  if horizLabels:
    csvF.write(',' + (',,').join(dataSquees))
  else:
    csvF.write('\n'.join(dataSquees))
  np.savetxt(csvPath,csvSubstance,delimiter = ',')
  csvF.close()
  
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' fix this NO.
def AxScale(whichArray, numTicks):
  if type(whichArray) is np.ndarray:
    return np.arange(0.9 * np.amin(whichArray), 1.1 * np.amax(whichArray), 1/numTicks)
  else:
    return (whichArray * (0.9 * min(whichArray),\
                          1.1 * max(whichArray),\
                          1/numTicks))
'''


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  downArro = "v" * 44
  upArro = "^" * 44
  verbose = 0 # set to 1 to print all outputs generated
  
  if 1:
    tiForm_test = tiForm(r"C:\Users\miles.HYPERLIGHT\Documents\ohmSensor\curvewithdr_2.txt")
    if verbose:
      print("tiForm_test" + downArro)
      print(tiForm_test)
      print("tiForm_test" + upArro)
  if 1:
    csvForm_test = csvForm(tiForm_test["contentArr"])
    if verbose:
      print("csvForm_testv" + downArro)
      print(csvForm_test)
      print("csvForm_test" + upArro)
  if 1:
    #testArr = np.array([[6,4,8],[1,0,7]])
    doStats_test = doStats(csvForm_test[0])
    if verbose:
      print("doStats_test" + downArro)
      print(doStats_test)
      print("doStats_test" + upArro)
  if 1:
    statsCsv = list(csvForm(doStats_test))
    statsCsv[0] = statsCsv[0].T

  if 1:
    csvSave(csvForm_test,tiForm_test["patheStart"],tiForm_test["patheEnd"])
    csvSave(statsCsv,tiForm_test["patheStart"],tiForm_test["patheEnd"]+"_stats",0)
  







