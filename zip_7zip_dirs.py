# zip_dirs.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: 2024-10-02

# slam all files with a given extension into a zip

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import py7zr
import pathlib
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/"+\
#     "onedrtibe BARP!/HyperLight General - General/Simulations/"+\
#     "Lumerical_Miles/modeConverter/tenMillionDollars"

win_cmd = False

in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/test_compress"
# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/od/OneDrive - HyperLight Corporation"
# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/od/test_buppin"
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
    
    print(f'Getting subdirectories from\n{in_dir}...')
    
    compress_list = []
    
    for infilename in os.listdir(in_dir):
        print(f"file = {os.path.join(in_dir, infilename)}")
        print(os.path.splitext(infilename)[-1].lower())
        if os.path.isdir(os.path.join(in_dir, infilename)) and\
        os.path.splitext(infilename)[-1].lower() != '.zip':
            compress_list.append(infilename)
    
    print(f'Done getting subdirectories from\n{in_dir}.\n')
    
    num_errs = 0
    num_done_here = 0
    for compress_name in compress_list:
        
        deletion_paths = []
        
        subdir_name = os.path.join(os.path.abspath(in_dir), compress_name)
        out_file_path = subdir_name + '.7z'
        subdir_as_path = pathlib.Path(subdir_name)
        nc_csv = "not_compressed.csv"
        not_compressed_record = os.path.join(in_dir, nc_csv)
        
        print(f'\nCompressing {compress_name}...\n')
        done_in_glob = 0
        perc_last = 0
        
        with py7zr.SevenZipFile(out_file_path, 'w') as archive:
            
            print("finding files...\n")
            
            glob_len = len(list(subdir_as_path.rglob("*")))
            
            print(f"files found = {glob_len}")
            
            for pathe in subdir_as_path.rglob("*"):
                add_to_uncompressed = False
                
                archive_dict = {
                    "file" : os.path.abspath(pathe),
                    "arcname" : os.path.relpath(pathe, start = subdir_as_path),
                    "filters" : {"preset": compresslevel},
                }
                
                winstat_str = hex(os.stat(archive_dict['file']).st_file_attributes).split('x')[-1]
                if len(winstat_str) < 8:
                    winstat_str = winstat_str.zfill(8)
                    
                if winstat_str == "00400020":
                    add_to_uncompressed = True
                else:
                    try:
                        if loud_mode:
                            print(f"current path = {pathe}")
                        archive.write(**archive_dict)
                        
                    except Exception as exx:
                        num_errs += 1
                        add_to_uncompressed = True
                        
                        if loud_mode:
                            print(exx)
                
                num_done_here += 1
                done_in_glob += 1
                
                if add_to_uncompressed:
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
                            "0x 0040 0000,signifies the item \"fully present locally\"\n"+\
                            "0x 0000 0020,signifies it is \"an archive file or directory\"\n"
                            
                        outstr += "win_attr,"
                        outstr += ','.join(archive_dict.keys()) + '\n'
                    
                    # print(f"outstr = {outstr}")
                    
                    winstat_str = hex(os.stat(archive_dict['file']).st_file_attributes).split('x')[-1]
                    if len(winstat_str) < 8:
                        winstat_str = winstat_str.zfill(8)
                    winstat_str = f'{winstat_str[:4]} {winstat_str[4:]},'
                    
                    outstr += winstat_str
                    outstr += ','.join(str(list(archive_dict.values())).strip(']').strip('[').split(','))
                    
                    outstr_subbed = outstr.replace('\\\\','/')
                    if outstr_subbed.isascii():
                        new_outstr = outstr_subbed
                    else:
                        new_outstr = ""
                        for char in outstr_subbed:
                            if ord(char) < 128:
                                new_outstr += char
                    
                    
                    with open(not_compressed_record, opentype) as ncr:
                        ncr.write(new_outstr)
                
                elif os.path.isfile(archive_dict['file']):
                    deletion_paths.append(archive_dict['file'])
                    
                perc = 100 * done_in_glob / glob_len
                
                if glob_len > 1000:
                    big_condition = perc > 99.99
                    small_condition = perc - perc_last > 0.5
                else:
                    big_condition = perc > 99
                    small_condition = perc / (perc_last + 10) > 0.95
                
                if big_condition:
                    print(f"{compress_name}: Done.\n")
                elif small_condition:
                    prog_str =\
                        f'{compress_name}: finished ({perc:.2f}%)'
                    
                    print(prog_str)
                    perc_last = perc
                    
            if os.path.isfile(not_compressed_record):
                csv_arc = os.path.join(subdir_as_path, nc_csv)
                archive_dict = {
                    "filename" : os.path.abspath(not_compressed_record),
                    "arcname" :  os.path.relpath(csv_arc, start = subdir_as_path),
                    "compress_type" : zipfile.ZIP_DEFLATED,
                    "compresslevel" : compresslevel,
                }
                
                archive.write(**archive_dict)
                
                os.remove(not_compressed_record)
        
        num_done += 1
        
        if len(deletion_paths) > 0:
            del_record = os.path.join(subdir_as_path, f"{compress_name}_deletions.txt")
            with open(del_record, 'w') as dt:
                for item in deletion_paths:
                    print(item)
                    dt.write(item + '\n')
            
            yslashn = input(
                f"\ndelete these items\n(see {del_record})? (y/N)\n_"
            )
            if yslashn.lower() == 'y':
                for item in deletion_paths:
                    try:
                        os.remove(item)
                    except:
                        print(f"couldnt delete {item}.\n")
            else:
                print("none deleted.\n")
        
    print(f'Done.')



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if win_cmd:
        in_dir = input("directory to look in?\n_")
    
    try:
        parp = zip_dirs(in_dir = in_dir, logging = False, loud_mode = False)
    except Exception as eee:
        print(eee)
        shawty = eee.__traceback__
        
        while not(shawty is None):
            print(f"line = {shawty.tb_lineno}")
            print(f"code = {shawty.tb_frame.f_code}")
            shawty = shawty.tb_next
    
    if win_cmd or False:
        input('Done.  Press [enter] to close.')
    
    
    

    
#end if __name__ == "__main__"