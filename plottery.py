# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

sns.set_theme(style="darkgrid")

excelfolder = os.path.expanduser("~") + "/OneDrive - HyperLight Corporation/"+\
    "General - Products/+NewFileSystem/Device Components/Mode Converter/"+\
    "20240722_vs_beam"
    
excelname = "20240722_vs_beam_pt3.xlsx"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    plt.close("all")
    
    lensdata = pd.read_excel(f"{excelfolder}/{excelname}", sheet_name = "brief_lens", skiprows = 2)
    bgndata = pd.read_excel(f"{excelfolder}/{excelname}", sheet_name = "brief_bgn", skiprows = 2)
    
    lens_dict = {
        "glass_g" : lensdata.iloc[:,0:4],
        "ld11" : lensdata.iloc[:,5:9],
        "ld12" : lensdata.iloc[:,10:14],
        "ld21" : lensdata.iloc[:,15:19],
        "ld22" : lensdata.iloc[:,20:24],
    }
    
    for lens in lens_dict.keys():
        lens_dict[lens] = lens_dict[lens].set_index(lens_dict[lens].columns[0])
    #     plt.figure()
    #     plt.plot(lens_dict[lens])
    #     plt.gca().set_title(lens)
    #     plt.gca().legend(lens_dict[lens].columns)
    
        plt.figure()
        prrt = sns.lineplot(data = lens_dict[lens])
        sns.grid = True
    
#end if __name__ == "__main__"
