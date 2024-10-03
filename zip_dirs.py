# zip_dirs.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: 2024-10-02

# slam all files with a given extension into a zip

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import zipfile
import pathlib
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/"+\
#     "onedrtibe BARP!/HyperLight General - General/Simulations/"+\
#     "Lumerical_Miles/modeConverter/tenMillionDollars"

win_cmd = False

in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/od/OneDrive - HyperLight Corporation"
loud_mode = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def zip_dirs(
        in_dir: str,
        compresslevel: int = 9, # 0 = minimum compression, 9 = maximum compression
        loud_mode: bool = True,
        logging: bool = True,
):
    in_dir = os.path.abspath(in_dir.strip('\"'))
    
    num_done = 0
    
    if loud_mode:
        print(f'Getting subdirectories from\n{in_dir}...')
    
    compress_list = []
    
    for infilename in os.listdir(in_dir):
        print(f"file = {os.path.join(in_dir, infilename)}")
        print(os.path.splitext(infilename)[-1].lower())
        if os.path.isdir(os.path.join(in_dir, infilename)) and\
        os.path.splitext(infilename)[-1].lower() != '.zip':
            compress_list.append(infilename)
    
    if loud_mode:
        print(f'Done getting subdirectories from\n{in_dir}.\n')
    
    # print(compress_list)
    
    for compress_name in compress_list:
        
        try:
            # raise Exception("test exception")
            subdir_name = os.path.join(os.path.abspath(in_dir), compress_name)
            out_file_path = subdir_name + '.zip'
            
            if loud_mode:
                print(f'Compressing {compress_name}...')
            
            
            with zipfile.ZipFile(out_file_path, mode="w") as archive:
                subdir_as_path = pathlib.Path(subdir_name)
                for pathe in subdir_as_path.rglob("*"):
                # for aeae in os.listdir(subdir_name):
                    print(f"current path = {pathe}")
                    archive.write(
                        filename = pathe,
                        arcname = pathe.relative_to(subdir_as_path),
                        compress_type = zipfile.ZIP_DEFLATED,
                        compresslevel = compresslevel
                    )
                    
        except Exception as exx:
            print(exx)
            if logging:
                with open(os.path.join(in_dir, "zip_dirs_log.txt"), 'a') as log:
                    log.write(f'{exx}\n')
                    
                    tbo = exx.__traceback__
                    for ii in range(4):
                        log.write(f'{tbo.tb_frame.f_back}\n')
                        tbo = tbo.tb_next
                        if tbo is None:
                            break
                    log.write('\n')
                    break
                
        num_done += 1
        
        if loud_mode:
            perc = 100 * num_done / len(compress_list)
            prog_str =\
                f'Compressed.  finished {num_done} of '+\
                f'{len(compress_list)} ({perc:.1f}%)\n'
                
            print(prog_str)
                    
    print(f'Done.')



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if win_cmd:
        in_dir = input("directory to look in?\n_")
    
    parp = zip_dirs(in_dir = in_dir, logging = True)
    
    if win_cmd:
        input('Done.  Press [enter] to close.')
    
    
    

    
#end if __name__ == "__main__"
