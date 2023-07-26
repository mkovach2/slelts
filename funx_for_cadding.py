# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:22:34 2023

@author: miles
"""


#░░███░░░░█░░░░░░░░░░░░░░░░░░░░█░░░░░░███░░░░░░░░░
#░█░░░░░░░█░░░░░░░░░░░░░░░░░░░░█░░░░░█░░░█░░░░░░░░
#░░███░░░█████░░░███░░░░███░░░█████░░█████░░░███░░
#░░░░░█░░░█░░░░░█░░█░░░█░░░█░░░█░░░░░█░░░░░░█░░░█░
#░░███░░░░░███░░░████░░█░░░░░░░░███░░░████░░█░░░░░

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
you_are_miles = 1
import os
import numpy as np

import sys
import math

if you_are_miles:
  # adding HLcadlib to the path
  winstr = "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/"+\
           "HyperLight General - General/miles/pyScripts"
  
  sys.path.insert(0, os.path.join(os.path.dirname( __file__ ), "..", "..",\
                  "GDS-Python"))
  sys.path.append(winstr)
  sys.path.append(r'c:\users\miles.hyperlight\appdata\local\programs\python\python38\lib\site-packages')
#end if you_are_miles

import gdspy
  
  
from HLcadlib import *
from HLcadlib.Optical_Components import *
from HLcadlib.RF_Components import *

from functools import partial

lib = gdspy.GdsLibrary()

cell_name = __file__.split('\\')[-1].replace(' ','_').replace('.py','')
cell = lib.new_cell(cell_name)



lib = gdspy.GdsLibrary()

from HLcadlib import *


lib = gdspy.GdsLibrary()

Bottom_left = (0,0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:


#░░░███░░░█░░░░░░░░░░░░░███░░░█████░░░███░░░░░░░░░░░█░░░░
#░░█░░░░░░░░░░░░░░░░░░░█░░░█░░░░█░░░░█░░░█░░░░░░░░░░█░░░░
#░█████░░░█░░░░░████░░░█████░░░░█░░░░█████░░█░░░█░░█████░
#░░█░░░░░░█░░█░░█░░░█░░█░░░░░░░░█░░░░█░░░░░░░███░░░░█░░░░
#░░█░░░░░░░██░░░█░░░█░░░████░░░░█░░░░░████░░█░░░█░░░░███░

def fineText(strIn,startPos,enable=1,upper_h_um = 50, layer=2):
  '''
  tired of having to fiddle around with labels?  this function allows you to 
  just slap one right in, specifying uppercase letter height in microns, and 
  returns the opposite corner of a box which contains all the text!  spot on!
  '''
  if enable:
    cell.add(gdspy.Text(strIn, 9/7*upper_h_um,
      (startPos[0],startPos[1]-2/7*upper_h_um),
      layer=layer))
    gap_w_um = 3/7 * upper_h_um
    return (startPos[0] + len(strIn) * 8/7 * upper_h_um - gap_w_um,
      startPos[1] + upper_h_um)
  #end if enable
  else:
    return 0
#end def fineText(strIn,startpos)  


#░░███░░░░░░░░░░░░░░█░░░███░░░░░░░░░
#░█░░░█░░░░░░░░░░░░░█░░█░░░█░░░░░░░░
#░█████░░████░░░░████░░█████░░░███░░
#░█░░░░░░█░░░█░░█░░░█░░█░░░░░░█░░░█░
#░░████░░█░░░█░░░███░░░░████░░█░░░░░

if 0: #debugging_if
  gdspy.LayoutViewer(lib)
#end if 1: #debugging_if
else:
  saveStr = os.getcwd() + "\\..\\20221201_" + cell_name + '.gds'
  # '..' used to save file to one layer above in file structure
  gdspy.write_gds(saveStr, unit=1.0e-6,\
                  precision=1.0e-9)
  print("saved as " + saveStr)
# end else