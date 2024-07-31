# colink.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: 2024-05-31

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

win_cmd = True

if win_cmd:
    newfoldername = input("new folder name:\n").strip("\"")
else:
    newfoldername = "/Device Components/Grating Coupler/1064_test"

c_folder = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation"+\
    "/General - Products/+NewFileSystem" + newfoldername
t_folder = "T:" + newfoldername

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    
    if os.path.isdir(c_folder):
        print(f'file already exists:\n{c_folder}')
    else:
        os.mkdir(c_folder)
        print(f'file created:\n{c_folder}')
    
    if os.path.isdir(t_folder):
        print(f'file already exists:\n{t_folder}')
    else:
        os.mkdir(t_folder)
        print(f'file created:\n{t_folder}')
    
    # c_shortcut = c_folder + "/t_data"
    # if os.path.exists(c_shortcut):
    #     if os.path.abspath(c_shortcut) == t_folder:
    #         os.symlink(t_folder, c_shortcut)
    #     else:
    #         print("shortcut exists:\n{c_shortcut}")
    #         print(os.path.abspath(c_shortcut))
    # else:
        
    if win_cmd:
        input("done lol press enter")
#end if __name__ == "__main__"
