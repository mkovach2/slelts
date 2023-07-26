# update_words.py
# 
# Author: miles at hyperlightcorp dot com
# Created: 2023-04-27
# Modified: 2023-04-27

# input csv of words to replace and file.
# column 1 should contain all the 
# this program then saves a backup version of the file untouched, and updates 
# the first file with all the dict keys replaced by their values.

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import shutil
import os
import csv

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

use_prompts = 0
in_reverse = 0 # swaps columns
original = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/Products - General/+NewFileSystem/Device Components/Mode Converter/20230322_MC_EME_DOE/mc_measurement_DoE.py"
# original = "T:/Device Components/Mode Converter/20230322_MC_EME_DOE/TE_screen_20230515/gamer_doc.txt"
# original = "T:/Device Components/Mode Converter/20230322_MC_EME_DOE/TE_screen_20230515/verification_for_speed/speed_11.csv"
# original = "T:/Device Components/Mode Converter/20230322_MC_EME_DOE/EME_univ_mk_20230509.lsf"
# original = "C:/Users/miles.HYPERLIGHT/Documents/_git_repos/eme_sweep-py/EME_univ_mk_20230506.lsf"
keys_csv = "C:/Users/miles.HYPERLIGHT/Desktop/test_table_2.csv"
# keys_csv = "C:/Users/miles.HYPERLIGHT/Desktop/test_table.csv"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if use_prompts:
        inputStr = 'input path to original file:\n'
        original = input(inputStr).replace("\\","/").strip('\"')
        inputStr = 'input path to CSV keys file:\n'
        keys_csv = input(inputStr).replace("\\","/").strip('\"')
    
    keypairs = []
    with open(keys_csv,'r') as ke:
        key_reader = csv.reader(ke, dialect='excel')
        for row in key_reader:
            keypairs.append(row)
    
    
    shutil.copy(original,original + '.bak')
    # os.rename(original,original + '.bak')
    outStr = 'backup saved as\n{}.bak\n'.format(original)
    print(outStr)
    
    os.remove(original)
    file_out = original
        
    with open(original + '.bak','r') as og:
        with open(file_out,'a') as fo:
            for line in og:
                for keyp in keypairs:
                    if in_reverse:
                        line = line.replace(keyp[1],keyp[0])
                    else:
                        line = line.replace(keyp[0],keyp[1])
                fo.write(line)
    
#end if __name__ == "__main__"
