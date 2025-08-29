# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
from slelts.quicc_reorg_0p1 import quicc_reorg

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    err = 0
    
    in_dir = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/General - Products/"+\
        "+NewFileSystem/Device Components/Grating Coupler/20250820_DoR_br"
    
    for subfolder in os.listdir(in_dir):
        if subfolder[-3:] == '111':
            if not(err):
                err = quicc_reorg(
                    in_dir = in_dir + '/' + subfolder,
                    oldStr = "v.hdf5",
                    newStr = "v_111.hdf5",
                    # out_dir = out_dir,
                )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#end if __name__ == "__main__"
