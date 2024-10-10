# dumbs.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# renames all thumbs.db files so that you can delete the containing directory

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import pathlib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

win_cmd = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if win_cmd:
        roote = input("what\n_")
    else:
        roote = 'T:/Device Components/Grating Coupler/20241010_PoR_t3d/2d'
    
    
    roote = pathlib.Path(roote)
    for pathe in roote.rglob(pattern = "thumbs.db"):
        spleety = os.path.split(pathe)
        try:
            os.rename(pathe, os.path.join(spleety[0], 'dumbs.db'))
        except:
            print(f"couldnt rename {pathe}")
        else:
            print(f"renamed {pathe} to \"dumbs.db\"")
    
    if win_cmd:
        input("done. press enter to close\n_")
    
#end if __name__ == "__main__"
