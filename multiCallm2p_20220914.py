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
import sys
sys.path.append("C:/Users/miles.HYPERLIGHT/Documents/LumericalSimulations")
#import modeToPic_4p0

#'C:\Users\miles.HYPERLIGHT\Documents\LumericalSimulations\modeToPic_4p0.py'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  wincmd = 1
  
  homeD = \
    "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/Products - General"+\
    "/+NewFileSystem/Device Components/Mode Converter/"+\
    "20220831_parametric_swp/simulation/data_softlinks/"+\
    "MC_Space_Filling_Uniform_Design/"
    #"MC_Central_Composite_Design/"
    
  m2p = \
    "C:/Users/miles.HYPERLIGHT/Documents/LumericalSimulations/modeToPic_4p0.py"
    #"modeToPic_4p0"
    
  cAm = \
    "C:/Users/miles.HYPERLIGHT/Documents/LumericalSimulations/crossAtMax.py"
    
  alg = cAm # just make this the name of the algorithm to use
  
  os.chdir(homeD)
  files = os.listdir('.')
  for f in files:
    if not(os.path.isdir(f) and f[0:2] == "0p"):
      files.remove(f)
    #end if not(os.path.isdir(f) and f[0:2] == "0p")
  #end for f in files
  numF = len(files)
  
  numDone = 0
  for item in files:
    if alg == cAm:
      a = os.listdir(homeD + item + "/numpy_arrays/")
      for b in a:
        if b[-10:] == "EsqOut.npy":
          item += "/numpy_arrays/" + b
          break
        #end if b[-10:] == "EsqOut.npy"
      #end for b in a
    #end if alg == cAm
    try:
      os.system("py " + alg + " \"" + homeD + item + "\"")      
    #end try
    except KeyboardInterrupt:
      break
    #end except
    numDone += 1
    print("finished " + str(numDone) + " of " + str(numF))
  #end for item in files
  
  if wincmd:
    input("\nfinished.  press enter to close.\n")
  else:
    print("\nfinished.")
  
# end if __name__ == "__main__"