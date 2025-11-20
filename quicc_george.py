'''
quicc_reorg.py

1--------10--------20--------30--------40--------50--------60--------70--------
'''

import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  newFolder = 0
  
  uIn = input("enter path to folder containing files:\n")
  uIn = os.path.abspath(uIn.strip('\"')).replace('\\','/')

for numgur in range(1,10):
    # oldStr = f"p{numgur}u"
    # newStr = f"p{numgur}0u"
    oldStr = f'_{numgur}_'
    newStr = f'_0{numgur}_'
   
    err = 0
    
    if os.path.isfile(uIn):
        oldDir = uIn.rpartition('/')[0]
        allFiles = [uIn.rpartition('/')[-1],]
   
    elif os.path.isdir(uIn):
        oldDir = uIn
        allFiles = os.listdir(oldDir)
        
    os.chdir(oldDir)
    
    if newFolder:
        try:
            os.mkdir(oldDir + "/" + newStr)
        #end try
        except FileExistsError:
            print("files already exists oops")
            err = 1
    #end if newFolder
      
    if not(err):
        for fileN in allFiles:
            if oldStr in fileN:
                if newFolder:
                    os.replace(fileN,oldDir + "/" + newStr + '/' + fileN.replace(oldStr,newStr))
                #end if newFolder
                else:
                    os.replace(fileN,oldDir + "/" + fileN.replace(oldStr,newStr))
                #end else
            #end if oldStr in fileN
        #end for fileN in allFiles
    #end if !err


input("\nFinished.  Press [enter] to close.")
#end if winSetting
# end if __name__ == "__main__"