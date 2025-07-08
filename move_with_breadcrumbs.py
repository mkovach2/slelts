# move_with_breadcrumbs.py
# Author: miles at hyperlightcorp dot com
# Created: 2025-07-07

# moves a 

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import shutil
import time
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



src_file = "C:/Users/miles.HYPERLIGHT/Desktop/test_source/9134812_1dbc_TE_short_mode_palik_thicc.hdf5"
dest_dir = "T:/Users/miles.HYPERLIGHT/Desktop/test_dest"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def move_bc(
    source_file,
    dest_dir,
    breadcrumb_df
):
    shutil.move(
        src = source_file,
        dst = dest_dir,
    )
    
    
    
    return breadcrumb_df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    src_file = os.path.abspath(src_file.strip('\"'))
    
    breadcrumb_file = os.path.split(src_file)[0] + "/bropcrom.csv"
    
    print(f"src_file = {src_file}\n")
    print(f"dest_dir = {dest_dir}\n")
    print(f"breadcrumb_file = {breadcrumb_file}\n")
    
    if os.path.isfile(breadcrumb_file):
        breadcrumb_df = pd.read_csv(breadcrumb_file, header = 0)
    else:
        breadcrumb_df = pd.DataFrame(columns = (
            'name', 'former', 'current', 'date_created',
            'date_moved', 'created_timestamp', 'moved_timestamp'
        ))
    
    
    
#end if __name__ == "__main__"
