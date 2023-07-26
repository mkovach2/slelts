'''
[file name]
[project]
Author: miles @ hyperlightcorp.com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  import numpy as np
  if 1:
    file = "C:\\Users\\miles.HYPERLIGHT\\HyperLight Corporation\\HyperLight " + \
           "General - General\\Simulations\\Lumerical_Miles\\modeConverter\\heuwu\\"
  else:
    file = "C:\\Users\miles.HYPERLIGHT\HyperLight Corporation\HyperLight " + \
           "General - General\Simulations\Lumerical_Miles\modeConverter\heuwu\\"
  t=[]
  q = np.load(file + "huhhhh.npy")
  r = np.unique(q)
  for i in r:
    t.append([i,np.count_nonzero(i==q)])
    
  t = np.array(t)
  
  ind_t = np.argsort(t[:,1])
  t[50-ind_t]
