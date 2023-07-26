'''
[file name]
[project]
Author: miles @ hyperlightcorp.com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import numpy as np
import matplotlib.pyplot as plt
#import re

def easyim(dataIn):
  plt.imshow(dataIn, vmin=0, origin = 'lower', cmap='jet', aspect=1, \
             interpolation='none',resample = False, filternorm=False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == "__main__":
  # put main here
  if 0:
    commonPath = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/HyperLight "+\
                 "General - General/Simulations/Lumerical_Miles/modeConverter/"
    
    #lumRDfile = input("lumRDfile?").replace('\\','/')
    #lumRDfile = commonPath + "gould/RAWWWW.txt"
    #lumRDfile = commonPath + "deleet soone/fatty.txt"
    lumRDfile = commonPath + "scriptProving/" + \
                "Mode_1550nmWL_200nmHeight_3400nmTop_62deg_7umBOX_830nmCLAD" + \
                "_1bgn_68813_rawData.txt"
    lumRDfile=lumRDfile.strip("\"") # strip of quotes
    
    lrd = open(lumRDfile)
    fulltext = lrd.read()
    lrd.close()
    
    fulltext = fulltext.split('~')
    rD = {}
    for rawItem in fulltext:
      if (len(rawItem) > 0) and (rawItem.isalpha()):
        aKey = rawItem
      elif len(rawItem) > 0:
        rD[aKey] = np.fromstring(rawItem,sep='\t')
        
    ###############################################################################
    
    def stretchMat(matrIn,axIn,axis_=0):
      d = axIn[1:] - axIn[:-1]
      print()
      dRatio = d/np.min(d)
      print(np.shape(matrIn))
      if axis_:
        mInIndex = matrIn[:,:-1]
      else:
        mInIndex = matrIn[:-1,]
      print(np.shape(mInIndex))
      matrOut = np.repeat(mInIndex,dRatio.astype(int),axis=axis_)
      return (matrOut,d)
     
    ###############################################################################
    # minInt = np.around(np.min(rD['xMat'][1:]-rD['xMat'][0:-1]),12)
    # # minInt: smallest interval between x values, rounded to 12 digits
    rD['EsqOut'] = np.transpose(np.reshape(rD['EsqOut'],[len(rD['xMat']),len(rD['yMat'])]))
    # dx = rD['xMat'][1:] - rD['xMat'][:-1]
    # minX = dx/np.min(dx)
    # dy = rD['yMat'][1:] - rD['yMat'][:-1]
    # minY = dy/np.min(dy)
    
    # hX = np.repeat(rD['EsqOut'][:,:-1],minX.astype(int),axis=1)
    # hY = np.repeat(hX[:-1],minY.astype(int),axis=0)
    
    # plt.figure(1),easyim(hX)
    # plt.figure(2),easyim(hY)
    
    n = stretchMat(rD['EsqOut'], rD['xMat'],axis_=1)
    easyim(n[0])
    n = stretchMat(n[0], rD['yMat'],axis_=0)
    easyim(n[0])


from os import listdir
attemptFile = "Mode_1550nmWL_200nmHeight_3400nmTop_62deg_7umBOX_830nmCLAD_1bgn_68813_matData.png"
dirTo = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/HyperLight General - General/Simulations/Lumerical_Miles/modeConverter/deleet soone/"
attemptFileA = attemptFile.rpartition('.')[0]
aFtype = attemptFile.rpartition('.')[2]
attemptFileB = attemptFileA
suffix = ''
if attemptFile in listdir(dirTo):
  suffix = 0
  attemptFileB = attemptFileA + str(suffix)
while attemptFileA + str(suffix) + '.' + aFtype in listdir(dirTo):
  suffix += 1
  attemptFileB = attemptFileA + str(suffix)
  print("attemptFileB\t" + attemptFileB)
print(dirTo + attemptFileB + '.' + aFtype)

