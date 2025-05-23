'''
quicc_reorg.py

1--------10--------20--------30--------40--------50--------60--------70--------
'''

import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  winSetting = 1 # set when running directly from cmd
  
  userAsk = 1
  newFolder = 0
  keepGoing = 1
  
  if userAsk:
    uIn = input("enter path to folder containing files:\n")
  #end if 1
  else:
    longP = \
     "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/Products - General"+\
     "/+NewFileSystem/Device Components/Mode Converter/"+\
     "20220831_parametric_swp/simulation/data_softlinks/"
    uIn = longP + "test_vals_Combined"
    oldStr = "0p220_157p5_55p0_7p0_0p8_1p395"
    # oldStr = "0.159_185.5_54.3_5.959_0.934_1.440"
  #end else
  
  uIn = os.path.abspath(uIn.strip('\"')).replace('\\','/')

while keepGoing:
    if userAsk:
        oldStr = input("enter old string:\n")
        newStr = input("enter new string:\n")
    else:
        keepGoing = 0
        newStr = "0p173_81p6_51p4_6p60_0p789_1p444"
   
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
    
    cant_str = ""
    if not(err):
        for fileN in allFiles:
            if oldStr in fileN:
                try:
                    if newFolder:
                        os.replace(fileN,oldDir + "/" + newStr + '/' + fileN.replace(oldStr,newStr))
                    #end if newFolder
                    else:
                        os.replace(fileN,oldDir + "/" + fileN.replace(oldStr,newStr))
                    #end else
                except:
                    cant_str += fileN + "\n"
            #end if oldStr in fileN
        #end for fileN in allFiles
    #end if !err
    
    if len(cant_str) > 0:
        print("couldnt do it for these files:\n" + cant_str)
    
    if userAsk:
        yslashn = input("keep going (using the same folder)? (y/N)\n")
        if yslashn.lower() == 'y':
            keepGoing = 1
        else:
            keepGoing = 0

if winSetting:
    input("\nFinished.  Press [enter] to close.")
#end if winSetting
# end if __name__ == "__main__"