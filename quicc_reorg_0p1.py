'''
quicc_reorg.py

1--------10--------20--------30--------40--------50--------60--------70--------
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

winSetting = True # set when running directly from cmd
userAsk = True
newFolder = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def quicc_reorg(
        in_dir,
        oldStr,
        newStr,
        out_dir = None,
):
    if os.path.isfile(in_dir):
        allFiles = [in_dir.rpartition('/')[-1],]
   
    elif os.path.isdir(in_dir):
        allFiles = os.listdir(in_dir)
        
    if out_dir is None:
        out_dir = in_dir
    
    cant_str = ""
    for fileN in allFiles:
        if oldStr in fileN:
            try:
                os.replace(in_dir + '/' + fileN, out_dir + '/' + fileN.replace(oldStr,newStr))
            except:
                cant_str += fileN + "\n"
        #end if oldStr in fileN
    #end for fileN in allFiles
    
    if len(cant_str) > 0:
        print("couldnt do it for these files:\n" + cant_str)
        return 1
    else:
        return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    # initial conditions
    keepGoing = True
    err = 0
    
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
            keepGoing = False
            newStr = "0p173_81p6_51p4_6p60_0p789_1p444"
        
        if os.path.isfile(uIn):
            oldDir = uIn.rpartition('/')[0]
        elif os.path.isdir(uIn):
            oldDir = uIn
            
        if newFolder:
            out_dir = oldDir + "/" + newStr
        else:
            out_dir = uIn
        
        if not(os.path.isdir(out_dir)):
            try:
                os.mkdir(out_dir)
            #end try
            except FileExistsError:
                print("files already exists oops")
                err = 1
        #end if newFolder
        
        if not(err):
            err = quicc_reorg(
                in_dir = uIn,
                oldStr = oldStr,
                newStr = newStr,
                out_dir = out_dir,
            )
        
        if userAsk:
            yslashn = input("keep going (using the same folder)? (y/N)\n")
            if yslashn.lower() == 'y':
                keepGoing = True
            else:
                keepGoing = False
                
    if winSetting:
        input("\nFinished.  Press [enter] to close.")
    #end if winSetting
# end if __name__ == "__main__"