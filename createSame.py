'''
createSame.py
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

gets a list of the folders in sourceD 
and makes empty copies of all of them in destD

1--------10--------20--------30--------40--------50--------60--------70--------
'''

winCmd = 1
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  sourceD = input("Enter path to source directory:\n")
  destD = input("Enter path to destination directory:\n")
  
  sourceD = sourceD.replace("\\","/").strip('\"')
  destD = destD.replace("\\","/").strip('\"')
  
  # os.chdir(sourceD)
  for folder in os.listdir(sourceD):
    if os.path.isdir(sourceD + '/' + folder) and\
        not(os.path.isdir(destD + '/' + folder)):
            # print(destD + '/' + folder)
            os.mkdir(destD + '/' + folder)
    #end if os.path.isdir(folder)
  #end for folder in os.listdir(sourceD)
  
  # os.chdir(destD)
  
  if winCmd:
    input("finished.  press enter to close.\n")
  else:
    print("finished.")
    
# end if __name__ == "__main__"