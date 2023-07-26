'''
BRRT BRRT BRTT SANDBOX

aaaaaaaaaaa

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import numpy as np
import matplotlib.pyplot as plt
from modeToPic_3p0 import mode2pic
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  # zee=np.load("C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
  #             "HyperLight General - General/miles/pyScripts/modeToPic"+\
  #             "/copy_of_UHNA3_20220518_dont_use/Mode_1550nmWL_200nmHeight"+\
  #             "_3500nmTop_62deg_7umBOX_830nmCLAD_1bgn_matData_nZ.npy")
  # wai = np.load("C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
  #             "HyperLight General - General/miles/pyScripts/modeToPic"+\
  #             "/copy_of_UHNA3_20220518_dont_use/Mode_1550nmWL_200nmHeight"+\
  #             "_3500nmTop_62deg_7umBOX_830nmCLAD_1bgn_rawData_EsqOut.npy")
  
  zee=np.load("C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
              "HyperLight General - General/Simulations/"+\
              "Simulation Requests/fan_angle_20220711/1550/"+\
              "56p5deg_matData_nZ.npy")
  wai = np.load("C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
                "HyperLight General - General/Simulations/"+\
                "Simulation Requests/fan_angle_20220711/1550/"+\
                "56p5deg_67669_mode_TE%100n1p84399_rawData_EsqOut.npy")
  
  plt.close('all')
  fyuu = zee[1:,1:]
  waiuu = wai[1:,1:]
  
  jaaj = np.logical_or(zee[0:-1,1:]!=fyuu,zee[1:,0:-1]!=fyuu)
  
  fyuu2 = np.logical_not(fyuu)
  plt.figure()
  #plt.imshow(fyuu,origin="lower",cmap="jet",alpha=1.0)
  
  plt.imshow(waiuu,origin="lower",cmap="jet") # while "jet" matches the 
                                              # lumerical out, consider "turbo"
  #plt.imshow(jaaj,origin="lower",cmap="binary",alpha=0.1)
  #plt.figure()
  plt.imshow(np.maximum(jaaj,waiuu),origin="lower",cmap="jet")
  plt.show(block=False)