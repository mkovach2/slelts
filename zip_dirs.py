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

def good_dict(dict_in: dict):
    dict_str = str(dict_in).replace(', ', ',\n')
    dict_str = dict_str.replace('{', '{\n')
    dict_str = dict_str.replace('}', '\n}')
    
    return dict_str


def stat_str(
        path_to,
        output_file,
        num_done: int,
        goodbadstr: str,
):
    stab = os.stat(path_to, follow_symlinks = True)
    # statistic = stab.st_size
    paf = os.path.abspath(path_to)
    
    # out_str = f'{num_done},{goodbadstr},{paf},{statistic}\n'
    stat_str = ','.join(str(list(stab)).strip(']').strip('[').split(','))
    out_str = f'{num_done},{goodbadstr},{paf},{hex(stab.st_file_attributes)}\n'
    
    with open(output_file, 'a') as yap:
        yap.write(out_str)
    
    return out_str


def zip_dirs(
        in_dir: str,
        compresslevel: int = 9, # 0 = minimum compression, 9 = maximum compression
        loud_mode: bool = True,
        logging: bool = True,
        err_limit: int|None = None
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
    
    num_errs = 0
    num_done_here = 0
    ya = os.path.join(in_dir, "zip_lenf_stat.csv")
    with open(ya, 'w') as yap:
        yap.write(
            'num_done,'+\
            'goodbadstr,'+\
            'paf,'+\
            # 'st_mode,'+\
            # 'st_ino,'+\
            # 'st_dev,'+\
            # 'st_nlink,'+\
            # 'st_uid,'+\
            # 'st_gid,'+\
            # 'st_size,'+\
            # 'st_atime,'+\
            # 'st_mtime,'+\
            # 'st_ctime\n'
            'attributes\n'
        )
    for compress_name in compress_list:
        
        subdir_name = os.path.join(os.path.abspath(in_dir), compress_name)
        out_file_path = subdir_name + '.zip'
        
        print(f'\nCompressing {compress_name}...\n')
        
        
        with zipfile.ZipFile(out_file_path, mode="w") as archive:
            subdir_as_path = pathlib.Path(subdir_name)
            
            for pathe in subdir_as_path.rglob("*"):
                try:
                    print(f"current path = {pathe}")
                    
                    archive_dict = {
                        "filename" : os.path.abspath(pathe),
                        # "arcname" : "shit50504",
                        "arcname" : os.path.relpath(pathe, start = subdir_as_path),
                        "compress_type" : zipfile.ZIP_DEFLATED,
                        "compresslevel" : compresslevel,
                    }
                    
                    archive.write(**archive_dict)
                    
                except Exception as exx:
                    num_errs += 1
                    
                    print("\nBAD one")
                    print(f"length = {len(os.path.abspath(pathe))}\n")
                    stat_str(
                        path_to = pathe,
                        output_file = ya,
                        num_done = num_done_here + 1,
                        goodbadstr = 'bad'
                    )
                    
                    if loud_mode:
                        print(exx)
                    if logging:
                        with open(os.path.join(in_dir, "zip_dirs_log.txt"), 'a') as log:
                            
                            prob_str = f"Problem happened while compressing: ({num_errs})\n"+\
                                f"{good_dict(archive_dict)}\n"
                            
                            if loud_mode:
                                print(prob_str)
                            
                            log.write(prob_str)
                            
                            tbo = exx.__traceback__
                            log.write(f'{exx}: line {tbo.tb_lineno}\n')
                            for ii in range(4):
                                log.write(f'{tbo.tb_frame.f_back}\n')
                                tbo = tbo.tb_next
                                if tbo is None:
                                    break
                            log.write('\n')
                            if not(err_limit is None):
                                if num_errs > err_limit:
                                    break
                else:
                    print("~" * 40 + "\ngood one")
                    print(f"length = {len(os.path.abspath(pathe))}")
                    print("~" * 40 + "\n")
                    
                    stat_str(
                        path_to = pathe,
                        output_file = ya,
                        num_done = num_done_here + 1,
                        goodbadstr = 'GOOD'
                    )
                
                num_done_here += 1
                        
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
    
    parp = zip_dirs(in_dir = in_dir, logging = False, loud_mode = False)
    
    if win_cmd:
        input('Done.  Press [enter] to close.')
    
    
    

    
#end if __name__ == "__main__"