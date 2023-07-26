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
import shutil as su
winCMD = 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  if 1:
    theD = input("enter path to directory\n")
  #end if
  else:
    theD = r"C:\Users\miles.HYPERLIGHT\HyperLight Corporation" +\
      r"\\Products - General\+NewFileSystem\Device Components\Mode "+\
      r"Converter\20220926_cladding_h_sweep_metal\simulation_thick_sep"+\
      r"\800n_clad"
    # theD
  #end else
  os.chdir(theD)
  filesD = os.listdir()
  
  for dee in filesD:
    if dee[-8:] == ".csv.txt":
      print(dee[:-4])
      su.copyfile(dee,dee[:-4])
    #end if dee[-8:] == ".csv.txt"
  #end for dee in filesD
  
  if winCMD:
    input("finished.  press enter to close.")
  #end if winCMD
  
# end if __name__ == "__main__"