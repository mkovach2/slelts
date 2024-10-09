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
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/"+\
#     "onedrtibe BARP!/HyperLight General - General/Simulations/"+\
#     "Lumerical_Miles/modeConverter/tenMillionDollars"

win_cmd = True

in_dir = "T:/uh_oh/pleeelp"
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
        prompts_on: bool = False,
        prompt_before_delete: bool|None = None,
        exclude_list: list = [],
):
    in_dir = os.path.abspath(in_dir.strip('\"'))
    logfile = os.path.join(in_dir, "log.txt")
    
    num_done = 0
    
    print(f'Getting subdirectories from\n{in_dir}...')
    
    compress_list = []
    
    for infilename in os.listdir(in_dir):
        print(f"file = {os.path.join(in_dir, infilename)}")
        # print(f"infilename = {infilename}")
        # print(os.path.splitext(infilename)[-1].lower())
        if os.path.isdir(os.path.join(in_dir, infilename)) and\
        not(os.path.splitext(infilename)[-1].lower() in ('.zip', '.7z')) and\
        not(infilename in exclude_list):
            print('included')
            compress_list.append(infilename)
        else:
            print('excluded')
    
    print(f'Done getting subdirectories from\n{in_dir}.\n')
    # print(compress_list)
    
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
        
        ofpnum = None
        tries = 0
        while os.path.exists(out_file_path) and (ofpnum is None or tries < 100):
            tries += 1
            try:
                ofpnum = int(out_file_path.rpartition('.')[0][-2:]) + 1
            except:
                ofpnum = 00
            
            ofpstr = str(ofpnum)
            if ofpnum < 10:
                ofpstr = '0' + ofpstr
            
            out_file_path = f"{subdir_name}_{ofpstr}.7z"
        
        imdumbstr = "oop!  I'm dumb.  I cant figure out how to use the "+\
            "\"append\" functionality of py7zr.  creating archive called:\n"+\
            out_file_path + "\n"
        
        if not(ofpnum is None):
            print(imdumbstr)
        
        if tries > 99:
            exstr = "iunno whats going on but the rename attempts in "+\
                "zip_7zip_dirs.py has attempted more than 99 times to generate "+\
                f"a valid name for:\n\t{out_file_path}"
            tryprint(exstr)
            trywrite(
                filepath = logfile,
                mode = 'a',
                str_in = exstr + '\n'
            )
            if prompts_on:
                big_yslashn = input(f"Overwrite {out_file_path}? (y/N)\n_")
            else:
                big_yslashn = 'n'
                log_if(
                    logging,
                    logfile = logfile,
                    str_in = f'skipping {compress_name}.\n'
                )
        else:
            big_yslashn = 'y'
        
        if big_yslashn.lower() == 'y':
            with py7zr.SevenZipFile(
                    file = out_file_path,
                    mode = 'w',
                    filters = [{"id": py7zr.FILTER_LZMA, "preset": compresslevel},]
            ) as archive:
                
                print("finding files...\n")
                
                glob_len = len(list(subdir_as_path.rglob("*")))
                
                print(f"files found = {glob_len}")
                print("starting...")
                time_of_last_msg = int(time.time())
                
                for pathe in subdir_as_path.rglob("*"):
                    add_to_uncompressed = False
                    
                    archive_dict = {
                        "file" : os.path.abspath(pathe),
                        "arcname" : os.path.relpath(pathe, start = subdir_as_path),
                    }
                    
                    winstat_str = hex(os.stat(archive_dict['file']).st_file_attributes).split('x')[-1]
                    if len(winstat_str) < 8:
                        winstat_str = winstat_str.zfill(8)
                        
                    if winstat_str == "00400020":
                        add_to_uncompressed = True
                    else:
                        
                        if loud_mode:
                            tryprint(str_in = f"current path = {pathe}")
                        
                        try:
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
                            
                            try:
                                thiscode = __file__
                            except:
                                thiscode = "the code that generated this file, \"zip_7zip_dirs.py\""
                            
                            outstr = "note the following references:\n"+\
                                f"{thiscode}\n"+\
                                "for columns 1 thru 3\n"+\
                                "https://docs.python.org/3/library/os.html#os.stat_result,"+\
                                "for info about getting the windows file attributes\n"+\
                                "https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants,"+\
                                "for the meanings of different windows file attributes."+\
                                "specifically of note:\n"+\
                                "0x 0040 0000,signifies the item \"fully present locally\"\n"+\
                                "0x 0000 0020,signifies it is \"an archive-file or directory\"\n"
                                
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
                        time_of_last_msg = int(time.time())
                    elif small_condition or int(time.time()) - time_of_last_msg > 60:
                        prog_str =\
                            f'{compress_name}: finished {done_in_glob} of {glob_len} ({perc:.2f}%)'
                        print(prog_str)
                        time_of_last_msg = int(time.time())
                        perc_last = perc
                        
                if os.path.isfile(not_compressed_record):
                    csv_arc = os.path.join(subdir_as_path, nc_csv)
                    archive_dict = {
                        "file" : os.path.abspath(not_compressed_record),
                        "arcname" : os.path.relpath(csv_arc, start = subdir_as_path),
                    }
                    
                    archive.write(**archive_dict)
                    
                    os.remove(not_compressed_record)
        
            num_done += 1
            
            if len(deletion_paths) > 0:
                del_record = os.path.join(subdir_as_path, f"{compress_name}_deletions.txt")
                for item in deletion_paths:
                    
                    canteven_print = f"uhhh.  couldnt print an item.  weird."
                    canteven_write = f"uhhh.  couldnt add an item to {del_record}.  weird."
                    
                    recordstr = tryprint(
                        str_in = item,
                        str_else = canteven_print,
                    )
                    tryw_str = trywrite(
                        filepath = del_record,
                        mode = 'a',
                        str_in = item + '\n',
                        str_else = canteven_write + '\n',
                    )
                    print(tryw_str)
                    log_if(logging, logfile = logfile, str_in = tryw_str)
                    
                if prompts_on:
                    yslashn = input(
                        f"\ndelete these items\n(see {del_record})? (y/N)\n_"
                    )
                else:
                    yslashn = 'y'
                
                if yslashn.lower() == 'y':
                    for item in deletion_paths:
                        try:
                            os.remove(item)
                        except:
                            print(f"couldnt delete {item}.\n")
                else:
                    print("none deleted.\n")
                    log_if(logging, logfile = logfile, str_in = f"none deleted from {compress_name}\n")
        
    print(f'Done.')


def tryprint(str_in, str_else = ''):
    try:
        print(str_in)
        can_print = True
    except:
        print(str_else)
        can_print = False
    
    if can_print:
        return str_in
    else:
        return str_else


def trywrite(filepath, mode, str_in, str_else = ''):
    try:
        with open(filepath, mode) as file:
            try:
                file.write(str_in)
                can_write = True
            except:
                file.write(str_else)
                can_write = False
    except:
        can_write = False
    
    if can_write:
        return str_in
    else:
        return str_else
    
def log_if(enable = True, logfile = 'log.txt', str_in = ''):
    if enable:
        trywrite(
            filepath = logfile,
            mode = 'a',
            str_in = str_in,
        )
    return enable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if win_cmd:
        in_dir = input("directory to look in?\n_")
        # in_dir = "T:/uh_oh/pleeelp"
        
        exlist_str = "enter a directory to exclude, or press [Enter] "
        exclude_list = []
        exitem = input(exlist_str + f"to include all files in\n{in_dir}.\n_")
        while not(len(exitem) == 0):
            exclude_list.append(exitem)
            exitem = input(exlist_str + f"if done adding items.\n_")
        
        print(exclude_list)
    
        try:
            parp = zip_dirs(
                in_dir = in_dir,
                logging = True,
                loud_mode = False,
                prompts_on = True,
                exclude_list = exclude_list
            )
        except Exception as eee:
            print(eee)
            shawty = eee.__traceback__
            
            while not(shawty is None):
                print(f"line = {shawty.tb_lineno}")
                print(f"code = {shawty.tb_frame.f_code}")
                shawty = shawty.tb_next
    else:
        parp = zip_dirs(in_dir = in_dir, logging = False, loud_mode = False)
    
    if win_cmd:
        input('Done.  Press [enter] to close.')
    
    
    

    
#end if __name__ == "__main__"
