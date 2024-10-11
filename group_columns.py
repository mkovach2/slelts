# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>
# Modified: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import pandas as pd
import pandas.io.formats.excel
pd.io.formats.excel.ExcelFormatter.header_style = None
# ^this is so that we dont get obnoxious default formatting on the top row and
# index column

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

win_cmd = True
save_outputs = True

load_dir = 'T:/Device Components/Grating Coupler/20241010_PoR_t3d/2d_2'

save_dir = load_dir

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if win_cmd:
        load_dir = input('input directory containing CSVs\n')
        save_dir = load_dir
    
    df_dict = {}
    column_list = []
    for filename in os.listdir(load_dir):
        if filename.rpartition('.')[-1] == 'csv':
            filekey = filename.rpartition('.')[0]
            df_dict[filekey] = (pd.read_csv(f'{load_dir}/{filename}', index_col=0))
            column_list += list(df_dict[filekey].columns)
    
    column_list = pd.unique(pd.Series(column_list))
    # made it a series bc of a deprecation warning
    col_df_dict = {}
    for col in column_list:
        col_df_dict[col] = pd.DataFrame()
    
    # d0 = df_dict[list(df_dict.keys())[0]]
    
    # print(d0.loc[:,column_list])
    
    for df_name in df_dict.keys():
    # for df_name in df_dict.keys():
        for col_name in df_dict[df_name].columns.intersection(column_list):
        # for col_name in column_list:
            # print(f'{df_name}: {col_name}')
            # print(df_dict[df_name][col_name])
            col_df_dict[col_name][df_name] = df_dict[df_name][col_name]
        
    
    if save_outputs:
        solo_columns = pd.DataFrame()
        if not(os.path.isdir(f'{save_dir}/grouped')):
            os.mkdir(f'{save_dir}/grouped')
        
        excel_name = os.path.basename(load_dir) + '.xlsx'
        with pd.ExcelWriter(os.path.join(load_dir, excel_name)) as writer:
            for col_name in col_df_dict.keys():
                if len(col_df_dict[col_name].columns) == 1:
                    solo_columns[f'{col_df_dict[col_name].columns[0]}:{col_name}'] = col_df_dict[col_name]
                else:
                    col_df_dict[col_name].to_csv(f'{save_dir}/grouped/{col_name}.csv')
                    col_df_dict[col_name].to_excel(writer, sheet_name = col_name)
            solo_columns.to_csv(f'{save_dir}/grouped/solo_columns.csv')
            solo_columns.to_excel(writer, sheet_name = "solo_columns")
    
    
    if win_cmd:
        input('\ndone.  press [enter] to continue.\n')
    
#end if __name__ == "__main__"
