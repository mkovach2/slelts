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
    
    num_errs = 0
    num_done_here = 0
    for compress_name in compress_list:
        
        subdir_name = os.path.join(os.path.abspath(in_dir), compress_name)
        out_file_path = subdir_name + '.zip'
        subdir_as_path = pathlib.Path(subdir_name)
        not_compressed_record = os.path.join(subdir_as_path, "not_compressed.csv")
        
        print(f'\nCompressing {compress_name}...\n')
        
        with zipfile.ZipFile(out_file_path, mode="w") as archive:
            for pathe in subdir_as_path.rglob("*"):
                try:
                    print(f"current path = {pathe}")
                    
                    archive_dict = {
                        "filename" : os.path.abspath(pathe),
                        "arcname" : os.path.relpath(pathe, start = subdir_as_path),
                        "compress_type" : zipfile.ZIP_DEFLATED,
                        "compresslevel" : compresslevel,
                    }
                    
                    archive.write(**archive_dict)
                    
                except Exception as exx:
                    num_errs += 1
                    
                    if loud_mode:
                        print(exx)
                    
                    if os.path.isfile(not_compressed_record):
                        opentype = 'a'
                        outstr = '\n'
                    else:
                        opentype = 'w'
                        outstr = "note the following references:\n"+\
                            "https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.write,"+\
                            "for columns 1 thru 4\n"+\
                            "https://docs.python.org/3/library/os.html#os.stat_result,"+\
                            "for info about getting the windows file attributes\n"+\
                            "https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants,"+\
                            "for the meanings of different windows file attributes."+\
                            "specifically of note:\n"+\
                            "0x 0004 0000,signifies the item \"fully present locally\"\n"+\
                            "0x 0000 0020,signifies it is \"an archive file or directory\"\n"
                            
                        outstr += "win_attr,"
                        outstr += ','.join(archive_dict.keys()) + '\n'
                    
                    print(f"outstr = {outstr}")
                    
                    winstat_str = hex(os.stat(archive_dict['filename']).st_file_attributes).split('x')[-1]
                    if len(winstat_str) < 8:
                        winstat_str = winstat_str.zfill(8)
                    winstat_str = f'{winstat_str[:4]} {winstat_str[4:]},'
                    
                    outstr += winstat_str
                    outstr += ','.join(str(list(archive_dict.values())).strip(']').strip('[').split(','))
                    
                    with open(not_compressed_record, opentype) as ncr:
                        ncr.write(outstr.replace('\\\\','/'))
                
                num_done_here += 1
        
        if os.path.isfile(not_compressed_record):
            archive_dict = {
                "filename" : os.path.abspath(not_compressed_record),
                "arcname" : os.path.relpath(not_compressed_record, start = subdir_as_path),
                "compress_type" : zipfile.ZIP_DEFLATED,
                "compresslevel" : compresslevel,
            }
            
            archive.write(**archive_dict)
        
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
