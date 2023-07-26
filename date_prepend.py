'''
[file name]
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import os.path
from datetime import datetime
winCmd = 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  fileTo = input("enter path of file to add \"last modified\" date:\n")
  commentChar = '#'
  
  modDate = int(os.path.getmtime(fileTo))
  modDate = commentChar + ' Last Modified:  ' + str(datetime.fromtimestamp(modDate))
  
  
  with open(fileTo, 'r') as f:
    line1 = f.readline()
    orig = f.read()
  #end with open(fileTo, 'r') as f:
  with open(fileTo, 'w') as f2:
    if "Last Modified:" in line1:
      f2.write(modDate + '\n' + orig)
    #end if "Last Modified:" in line1
    else:
      f2.write(modDate + '\n' + line1 + orig)
    #end else
  #end with open(fileTo, 'w') as f2
  
  if winCmd:
    closeMe = input("finished.  press Enter to close.")
  #end if winCmd
  
# end if __name__ == "__main__"