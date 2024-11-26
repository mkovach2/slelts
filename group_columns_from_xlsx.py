# <sheet>.py
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

win_cmd = False
save_outputs = True

excel_path = 'T:/Device Components/Grating Coupler/20241108_did52/+8deg/1550xe'+\
    '/doe_3/compact_data_fibx_16p7.xlsx'

save_dir = os.path.dirname(excel_path)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    if win_cmd:
        excel_path = input('input path to XLSX file\n')
        save_dir = excel_path
    
    df_dict = {}
    column_list = []
    excel_sheets = pd.ExcelFile(excel_path).sheet_names
    # pd.read_excel()
    for sheet in excel_sheets:
        df_dict[sheet] = (pd.read_excel(excel_path, sheet_name = sheet, index_col=0))
        column_list += list(df_dict[sheet].columns)
    
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
        
        excel_name = os.path.basename(excel_path)[:-5] + '_sorted.xlsx'
        full_excel_save_path = os.path.join(save_dir, excel_name)
        with pd.ExcelWriter(full_excel_save_path) as writer:
            for col_name in col_df_dict.keys():
                if len(col_df_dict[col_name].columns) == 1:
                    solo_columns[f'{col_df_dict[col_name].columns[0]}:{col_name}'] = col_df_dict[col_name]
                else:
                    col_df_dict[col_name].to_csv(f'{save_dir}/grouped/{col_name}.csv')
                    col_df_dict[col_name].to_excel(writer, sheet_name = col_name)
            solo_columns.to_csv(f'{save_dir}/grouped/solo_columns.csv')
            solo_columns.to_excel(writer, sheet_name = "solo_columns")
        print(f"excel file saved as:\n{full_excel_save_path}")
    
    
    if win_cmd:
        input('\ndone.  press [enter] to continue.\n')
    
#end if __name__ == "__main__"
