'''
[file name]
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import os
import numpy as np
import gdspy
import sys
import math

yourPath = "C:/Users/miles.HYPERLIGHT/"

# adding HLcadlib to the path
winstr = yourPath + "/HyperLight Corporation/"+\
         "HyperLight General - General/miles/pyScripts"

sys.path.insert(0, os.path.join(os.path.dirname( __file__ ), "..", "..",\
                "GDS-Python"))
sys.path.append(winstr)

from HLcadlib import *
from HLcadlib.Optical_Components import *
from HLcadlib.RF_Components import *

from functools import partial

# from phidl import quickplot as qp
# from phidl import Device
# import phidl.geometry as pg

lib = gdspy.GdsLibrary()

longPath = yourPath + "HyperLight Corporation"+\
  "/HyperLight General - General/miles/misc/"
cell_name = 'mz'
cell = lib.new_cell(cell_name)
saveLoc = longPath + cell_name + '.gds'

Bottom_Left = (0,0) # center
number = 1 #placeholder

def Window(cell, center=(0,0), width=50, height=50, layer=21):
    window = gdspy.Rectangle((center[0]-width/2,center[1]-height/2),\
                             (center[0]+width/2,center[1]+height/2), layer)
    window.fillet(2)
    cell.add(window)
    return
#end def Window(cell, center=(0,0), width=10, height=10, layer=21)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  startWg1 = Waveguide(cell,[(0,0),2.0,'+x'],10)
  startWg2 = Waveguide(cell,[(0,20),2.0,'+x'],10)
  
  Electrode_CPW_EBL_DirectLiftOff(
    cell,
    WG_parameter1 = startWg1,
    WG_parameter2 = startWg2,
    length = 1000,
    gap_metal = 2.5,
    opt_WG_width = 2.0,
    opt_taper_length = 100,
    type_ground='Segmented',
    type_signal='Segmented',
    met_width_EBL1 = 6,
    met_width_EBL2_signal = None,
    met_width_EBL2_ground = 70,
    met_width_metal2_ground = 102.5,
    met_overlap_EBL = 0,
    shift_EBL_Etch = 0,
    shift_Etch_metal2 = -3,
    etch_width_sig = None,
    etch_width_ground = 10,
    seg_sig_h = 7,
    seg_sig_r = 0.25,
    seg_sig_s = 0.25,
    seg_sig_length = 25,
    seg_sig_duty = 0.05,
    seg_ground_h = 7,
    seg_ground_r = 0.25,
    seg_ground_s = 0.25,
    seg_ground_length = 25,
    seg_ground_duty = 0.05,
    layer_WG = 2,
    layer_EBL1 = 14,
    layer_EBL2 = 42,
    layer_etch = 29,
    layer_metal2 = 13
  )
  
  if 0: #debugging_if  
    gdspy.LayoutViewer(lib)
  #end if 1: #debugging_if
  else:
    gdspy.write_gds(saveLoc, unit=1.0e-6,\
                    precision=1.0e-9)  
  # end else
  
# end if __name__ == "__main__"