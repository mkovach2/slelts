# zip_ext.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: 2024-10-02

# slam all files with a given match_str into a zip

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import zipfile
import os
import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/"+\
#     "onedrtibe BARP!/HyperLight General - General/Simulations/"+\
#     "Lumerical_Miles/modeConverter/tenMillionDollars"

in_dir = "C:/Users/miles.HYPERLIGHT/Desktop/zip_test"
match_str = 'txt'
loud_mode = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def zip_ext(
        in_dir: str,
        match_str: str = 'txt',
        compresslevel: int = 9, # 0 = minimum compression, 9 = maximum compression
        loud_mode: bool = True,
        case_sensitive: bool = False
):
    in_dir = os.path.abspath(in_dir.strip('\"'))
    in_list = os.listdir(in_dir)
    
    if match_str[0] == '.':
        out_name = os.path.basename(in_dir) + f'_{match_str[1:].upper()}.zip'
    else:
        out_name = os.path.basename(in_dir) + f'_{match_str.upper()}.zip'
        
    out_file_path = os.path.join(os.path.abspath(in_dir), out_name)
    compress_list = []
    
    if loud_mode:
        print(f'Getting {match_str} files from\n{in_dir}...')
    
    if not(case_sensitive):
        match_str = match_str.lower()
    
    if os.path.isfile(out_file_path):
        prompt_str = f"\n{out_file_path}\nalready exists. wat do?\n"+\
            "[0]\t\tonly add non-duplicate files, without updating files that would be duplicates (default)\n"+\
            "[1]\t\tcompress all files to a new archive, with a new name\n_"
        
        wat_do = input(prompt_str)
        if wat_do == "1":
            zipmode = "w"
            exist_list = []
            # new_name = input("enter new name.\n_")
            out_file_path = os.path.join(os.path.abspath(in_dir), input("enter new name.\n_"))
            if not(os.path.splitext(out_file_path)[1] == '.zip'):
                out_file_path += '.zip'
        else:
            zipmode = "a"
            with zipfile.ZipFile(out_file_path, mode = 'r') as archive:
                exist_list = archive.namelist()
    else:
        zipmode = "w"
        exist_list = []
    
    for in_name in in_list:
        if not(in_name == out_name):
            if case_sensitive:
                infile_str = in_name
            else:
                infile_str = in_name.lower()
            
            if re.search(match_str, infile_str) and not(in_name in exist_list):
                compress_list.append(in_name)
    
    if loud_mode:
        print(f'Done getting {match_str} files from\n{in_dir}.')
    
    num_done = 0
    
    with zipfile.ZipFile(out_file_path, mode = zipmode) as archive:
        for compress_name in compress_list:
            
            if loud_mode:
                print(f'Compressing {compress_name}...')
            
            archive.write(
                filename = os.path.join(os.path.abspath(in_dir), compress_name),
                arcname = compress_name,
                compress_type = zipfile.ZIP_DEFLATED,
                compresslevel = compresslevel
            )
            
            num_done += 1
            
            if loud_mode:
                perc = 100 * num_done / len(compress_list)
                prog_str =\
                    f'Compressed.  finished {num_done} of '+\
                    f'{len(compress_list)} ({perc:.1f}%)\n'
                    
                print(prog_str)
                
    print(f'Done.  zip archive saved as\n{out_file_path}')
    
    return compress_list



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    in_dir = input("directory to look in?\n_")
    match_str = input("match_str to compress?\n_")
    
    c_list = zip_ext(
        in_dir = in_dir,
        match_str = match_str,
        compresslevel = 5,
        loud_mode = True
    )
    
    yslashn = input("delete originals? (y/N)\n_")
    if yslashn.lower() == 'y':
        for c_name in c_list:
            os.remove(os.path.join(os.path.abspath(in_dir), c_name))
    
    input("\nEnter to quit.")
    
#end if __name__ == "__main__"
