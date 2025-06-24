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
undo_mode = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if undo_mode:
        from_str = "dumbs.db"
        to_str = "thumbs.db"
        print("undo mode is TRUE.  This will change Dumbs back to THumbs.\n\n")
    else:
        from_str = "thumbs.db"
        to_str = "dumbs.db"
    
    if win_cmd:
        roote = input("what\n_")
    else:
        roote = 'T:/Device Components/Grating Coupler/20241010_PoR_t3d/2d'
    
    roote = roote.replace("\\","/").strip("\"").strip("\'") # de-widowfy the path
    
    if os.path.isdir(roote):
        roote = pathlib.Path(roote)
        dumbs_list = list(roote.rglob(pattern = from_str))
    elif os.path.isfile(roote):
        dumbs_list = [roote]
    else:
        print(f"yo?\n\n{roote}\n\ndoesnt seem to be a file or directory.")
        dumbs_list = []
    
    for pathe in dumbs_list:
        spleety = os.path.split(pathe)
        try:
            os.rename(pathe, os.path.join(spleety[0], to_str))
        except:
            print(f"couldnt rename {pathe}")
        else:
            print(f"renamed {pathe} to \"{to_str}\"")
    
    if win_cmd:
        input("done. press enter to close\n_")
    
#end if __name__ == "__main__"
