# zip_ext.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: 2024-10-02

# slam all files with a given extension into a zip

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import zipfile
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# in_dir = "C:/Users/miles.HYPERLIGHT/old onedrive/"+\
#     "onedrtibe BARP!/HyperLight General - General/Simulations/"+\
#     "Lumerical_Miles/modeConverter/tenMillionDollars"

in_dir = "C:/Users/miles.HYPERLIGHT/Desktop/zip_test"
extension = 'txt'
loud_mode = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def zip_ext(
        in_dir: str,
        extension: str = 'txt',
        compresslevel: int = 9, # 0 = minimum compression, 9 = maximum compression
        loud_mode: bool = True
):
    in_dir = os.path.abspath(in_dir.strip('\"'))
    in_list = os.listdir(in_dir)
    
    extension = extension.lower()
    if extension[0] == '.':
        out_name = os.path.basename(in_dir) + f'_{extension[1:].upper()}.zip'
    else:
        out_name = os.path.basename(in_dir) + f'_{extension.upper()}.zip'
        extension = '.' + extension
        
    out_file_path = os.path.join(os.path.abspath(in_dir), out_name)
    compress_list = []
    
    if loud_mode:
        print(f'Getting {extension} files from\n{in_dir}...')
    
    for infilename in in_list:
        if os.path.splitext(infilename)[-1].lower() == extension:
            compress_list.append(infilename)
    
    if loud_mode:
        print(f'Done getting {extension} files from\n{in_dir}.')
    
    num_done = 0
    
    with zipfile.ZipFile(out_file_path, mode="w") as archive:
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



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    in_dir = input("directory to look in?\n_")
    extension = input("extension to compress?\n_")
    
    zip_ext(
        in_dir = in_dir,
        extension = extension,
        compresslevel = 5,
        loud_mode = True
    )
    
    input("\nEnter to quit.")
    
#end if __name__ == "__main__"
