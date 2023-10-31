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
  
  print_new_names = True
  actually_move = True
  
  # inD = "T:/Device Components/Segmented CPW/e/"
  inD = "T:/Device Components/Mode Converter/20230913_layer_to_layer/doe/"
  
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
    hasUid = re.match('[\d]{3}',file.name)
    if hasUid:
      if hasUid.group(0) in folders:
        print("moving " + file.name)
        if print_new_names:
            print(inD + file.name, inD + hasUid.group(0) + '/' + file.name)
        if actually_move:
            os.rename(inD + file.name, inD + hasUid.group(0) + '/' + file.name)
    #end if hasUid
  #end for folder in folders
  
# end if __name__ == "__main__"