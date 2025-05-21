# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# import pandas as pd
import numpy as np

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

lonj = "C:/Users/miles.HYPERLIGHT/OneDrive - HyperLight Corporation/"+\
    "General - Products/+NewFileSystem/Device Components/Grating Coupler/"
csv_in_path = lonj +\
    "20250519_apodized_+8_g2f11/stage_1/grouped/no_sweep = 1.csv"

diffs_tup = (-10,)# -20, -30, -40)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    deeta = np.loadtxt(csv_in_path, delimiter = ',', skiprows = 1)
    
    with open(csv_in_path, "r") as ci:
        uid_row = ci.readline().split(',')
    
    deetamax = deeta.max(axis = 0)
    deetalam = deeta[:,0][deeta.argmax(axis = 0)]
    
    d_over = np.zeros((10, deeta.shape[1] - 1))
    for aa in range(1,11):
        d_over[aa-1, :] = np.count_nonzero(deeta[:,1:] > -aa * 5, axis = 0) / deeta.shape[0]
    
    # doiter_in = pd.read_csv(csv_in_path)
    
    # doiter_maxes = pd.DataFrame(
    #     data = (
    #         doiter_in.max(axis = 0),
    #         doiter_in.idxmax(axis = 0),
    #     ),
    #     index = ("xmit", "lam"),
    #     columns = doiter_in.columns,
    # )
    
    # # index_df = pd.DataFrame(
    # #     data = doiter_in.index,
    # #     index = doiter_in.index,
    # #     columns = doiter_in.columns
    # # )
    
    
    
    # # doiter_in_lo = pd.DataFrame(
    # #     data = doiter_in,
    # #     index = doiter_in.index,
    # #     columns = doiter_in.columns
    # # )
    # # doiter_in_hi = pd.DataFrame(
    # #     data = doiter_in,
    # #     index = doiter_in.index,
    # #     columns = doiter_in.columns
    # # )
    
    
    
    # # diffs_df_lo = pd.DataFrame(
    # #     index = diffs_tup,
    # #     columns = doiter_in.columns
    # # )
    # # diffs_df_hi = pd.DataFrame(
    # #     index = diffs_tup,
    # #     columns = doiter_in.columns
    # # )
    # for diff in diffs_tup:
    #     pjoop = (
    #         (doiter_in.iloc[:-1,:] <= doiter_maxes.loc['xmit',:] + diff) &
    #         (doiter_in.iloc[1:,:] > doiter_maxes.loc['xmit',:] + diff)
    #     ) | (
    #         (doiter_in.iloc[1:,:] <= doiter_maxes.loc['xmit',:] + diff) &
    #         (doiter_in.iloc[:-1,:] > doiter_maxes.loc['xmit',:] + diff)
    #     )
    #     doiter_diff = doiter_in - (diff + doiter_maxes.loc["xmit",:])
    #     for col in doiter_in.columns:
    #         sgoop = doiter_in.loc[:doiter_maxes.at["lam",col], col]
    #         # print(diff)
            # print(col)
            # print(doiter_in.loc[:doiter_maxes.at["lam",col], col].idxmin())
            # # diffs_df_lo.at[diff, col] = doiter_in.loc[:doiter_maxes.at["lam",col], col].idxmin()
    
    
    
    
    
    
#end if __name__ == "__main__"
