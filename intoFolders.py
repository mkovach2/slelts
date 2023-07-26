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
import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  # inD = "T:/Device Components/Segmented CPW/e/"
  inD = "T:/Device Components/Segmented CPW/reduced_100_10min/"
  
  fileList = os.scandir(inD)
  folders = []
  files = []
  
  for anItem in fileList:
    if anItem.is_dir():
      folders.append(anItem.name)
    #end if anItem.is_file()
    else:
      files.append(anItem)
    #end else
  #end for anItem in fileList
  
  for file in files:
    hasUid = re.match('[\d]{5}',file.name)
    if hasUid:
      if hasUid.group(0) in folders:
        print("moving " + file.name)
        os.rename(inD + file.name, inD + hasUid.group(0) + '/' + file.name)
    #end if hasUid
  #end for folder in folders
  
# end if __name__ == "__main__"